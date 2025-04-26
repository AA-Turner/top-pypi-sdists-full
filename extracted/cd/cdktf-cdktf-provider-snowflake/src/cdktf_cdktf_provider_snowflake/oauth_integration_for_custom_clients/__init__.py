r'''
# `snowflake_oauth_integration_for_custom_clients`

Refer to the Terraform Registry for docs: [`snowflake_oauth_integration_for_custom_clients`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients).
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


class OauthIntegrationForCustomClients(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClients",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients snowflake_oauth_integration_for_custom_clients}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        oauth_client_type: builtins.str,
        oauth_redirect_uri: builtins.str,
        blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network_policy: typing.Optional[builtins.str] = None,
        oauth_allow_non_tls_redirect_uri: typing.Optional[builtins.str] = None,
        oauth_client_rsa_public_key: typing.Optional[builtins.str] = None,
        oauth_client_rsa_public_key2: typing.Optional[builtins.str] = None,
        oauth_enforce_pkce: typing.Optional[builtins.str] = None,
        oauth_issue_refresh_tokens: typing.Optional[builtins.str] = None,
        oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
        oauth_use_secondary_roles: typing.Optional[builtins.str] = None,
        pre_authorized_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients snowflake_oauth_integration_for_custom_clients} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Specifies the name of the OAuth integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#name OauthIntegrationForCustomClients#name}
        :param oauth_client_type: Specifies the type of client being registered. Snowflake supports both confidential and public clients. Valid options are: ``PUBLIC`` | ``CONFIDENTIAL``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_client_type OauthIntegrationForCustomClients#oauth_client_type}
        :param oauth_redirect_uri: Specifies the client URI. After a user is authenticated, the web browser is redirected to this URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_redirect_uri OauthIntegrationForCustomClients#oauth_redirect_uri}
        :param blocked_roles_list: A set of Snowflake roles that a user cannot explicitly consent to using after authenticating. By default, this list includes the ACCOUNTADMIN, ORGADMIN and SECURITYADMIN roles. To remove these privileged roles from the list, use the ALTER ACCOUNT command to set the OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST account parameter to FALSE. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#blocked_roles_list OauthIntegrationForCustomClients#blocked_roles_list}
        :param comment: Specifies a comment for the OAuth integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#comment OauthIntegrationForCustomClients#comment}
        :param enabled: Specifies whether this OAuth integration is enabled or disabled. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#enabled OauthIntegrationForCustomClients#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#id OauthIntegrationForCustomClients#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_policy: Specifies an existing network policy. This network policy controls network traffic that is attempting to exchange an authorization code for an access or refresh token or to use a refresh token to obtain a new access token. For more information about this resource, see `docs <./network_policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#network_policy OauthIntegrationForCustomClients#network_policy}
        :param oauth_allow_non_tls_redirect_uri: If true, allows setting oauth_redirect_uri to a URI not protected by TLS. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_allow_non_tls_redirect_uri OauthIntegrationForCustomClients#oauth_allow_non_tls_redirect_uri}
        :param oauth_client_rsa_public_key: Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_client_rsa_public_key OauthIntegrationForCustomClients#oauth_client_rsa_public_key}
        :param oauth_client_rsa_public_key2: Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_client_rsa_public_key_2 OauthIntegrationForCustomClients#oauth_client_rsa_public_key_2}
        :param oauth_enforce_pkce: Boolean that specifies whether Proof Key for Code Exchange (PKCE) should be required for the integration. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_enforce_pkce OauthIntegrationForCustomClients#oauth_enforce_pkce}
        :param oauth_issue_refresh_tokens: Specifies whether to allow the client to exchange a refresh token for an access token when the current access token has expired. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_issue_refresh_tokens OauthIntegrationForCustomClients#oauth_issue_refresh_tokens}
        :param oauth_refresh_token_validity: Specifies how long refresh tokens should be valid (in seconds). OAUTH_ISSUE_REFRESH_TOKENS must be set to TRUE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_refresh_token_validity OauthIntegrationForCustomClients#oauth_refresh_token_validity}
        :param oauth_use_secondary_roles: Specifies whether default secondary roles set in the user properties are activated by default in the session being opened. Valid options are: ``IMPLICIT`` | ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_use_secondary_roles OauthIntegrationForCustomClients#oauth_use_secondary_roles}
        :param pre_authorized_roles_list: A set of Snowflake roles that a user does not need to explicitly consent to using after authenticating. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#pre_authorized_roles_list OauthIntegrationForCustomClients#pre_authorized_roles_list}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528f8f9a1366d8cfe0bd8ffd145c6f15a4f9143c37463875f1fc1edb7f0c85c9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OauthIntegrationForCustomClientsConfig(
            name=name,
            oauth_client_type=oauth_client_type,
            oauth_redirect_uri=oauth_redirect_uri,
            blocked_roles_list=blocked_roles_list,
            comment=comment,
            enabled=enabled,
            id=id,
            network_policy=network_policy,
            oauth_allow_non_tls_redirect_uri=oauth_allow_non_tls_redirect_uri,
            oauth_client_rsa_public_key=oauth_client_rsa_public_key,
            oauth_client_rsa_public_key2=oauth_client_rsa_public_key2,
            oauth_enforce_pkce=oauth_enforce_pkce,
            oauth_issue_refresh_tokens=oauth_issue_refresh_tokens,
            oauth_refresh_token_validity=oauth_refresh_token_validity,
            oauth_use_secondary_roles=oauth_use_secondary_roles,
            pre_authorized_roles_list=pre_authorized_roles_list,
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
        '''Generates CDKTF code for importing a OauthIntegrationForCustomClients resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OauthIntegrationForCustomClients to import.
        :param import_from_id: The id of the existing OauthIntegrationForCustomClients that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OauthIntegrationForCustomClients to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd06f252dae3bb51aa9017d40531332aefa857283f16dfc2f99711bb871ae38)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetBlockedRolesList")
    def reset_blocked_roles_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockedRolesList", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetworkPolicy")
    def reset_network_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPolicy", []))

    @jsii.member(jsii_name="resetOauthAllowNonTlsRedirectUri")
    def reset_oauth_allow_non_tls_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthAllowNonTlsRedirectUri", []))

    @jsii.member(jsii_name="resetOauthClientRsaPublicKey")
    def reset_oauth_client_rsa_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthClientRsaPublicKey", []))

    @jsii.member(jsii_name="resetOauthClientRsaPublicKey2")
    def reset_oauth_client_rsa_public_key2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthClientRsaPublicKey2", []))

    @jsii.member(jsii_name="resetOauthEnforcePkce")
    def reset_oauth_enforce_pkce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthEnforcePkce", []))

    @jsii.member(jsii_name="resetOauthIssueRefreshTokens")
    def reset_oauth_issue_refresh_tokens(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthIssueRefreshTokens", []))

    @jsii.member(jsii_name="resetOauthRefreshTokenValidity")
    def reset_oauth_refresh_token_validity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRefreshTokenValidity", []))

    @jsii.member(jsii_name="resetOauthUseSecondaryRoles")
    def reset_oauth_use_secondary_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthUseSecondaryRoles", []))

    @jsii.member(jsii_name="resetPreAuthorizedRolesList")
    def reset_pre_authorized_roles_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreAuthorizedRolesList", []))

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
    def describe_output(self) -> "OauthIntegrationForCustomClientsDescribeOutputList":
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="relatedParameters")
    def related_parameters(
        self,
    ) -> "OauthIntegrationForCustomClientsRelatedParametersList":
        return typing.cast("OauthIntegrationForCustomClientsRelatedParametersList", jsii.get(self, "relatedParameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "OauthIntegrationForCustomClientsShowOutputList":
        return typing.cast("OauthIntegrationForCustomClientsShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="blockedRolesListInput")
    def blocked_roles_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "blockedRolesListInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPolicyInput")
    def network_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowNonTlsRedirectUriInput")
    def oauth_allow_non_tls_redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthAllowNonTlsRedirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKey2Input")
    def oauth_client_rsa_public_key2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthClientRsaPublicKey2Input"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKeyInput")
    def oauth_client_rsa_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthClientRsaPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientTypeInput")
    def oauth_client_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthClientTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthEnforcePkceInput")
    def oauth_enforce_pkce_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthEnforcePkceInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthIssueRefreshTokensInput")
    def oauth_issue_refresh_tokens_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthIssueRefreshTokensInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRedirectUriInput")
    def oauth_redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthRedirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidityInput")
    def oauth_refresh_token_validity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "oauthRefreshTokenValidityInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthUseSecondaryRolesInput")
    def oauth_use_secondary_roles_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthUseSecondaryRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="preAuthorizedRolesListInput")
    def pre_authorized_roles_list_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "preAuthorizedRolesListInput"))

    @builtins.property
    @jsii.member(jsii_name="blockedRolesList")
    def blocked_roles_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "blockedRolesList"))

    @blocked_roles_list.setter
    def blocked_roles_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced58dc01137c39cdde09281c1901b4cf8b2ecc26b2f56c3445a730e1f2bf010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockedRolesList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397b7bbb0f3fabc99d18d45d2116a9b3ed2939c14d5a08d289d32023117a3dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d1887dafe846d74e6c1ff60922690b6edf4466125580471eac5ae9d3392b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be64b703f8d2a05b7e06c2911a820f3bcb7e547f15cb0f08c9c25bb3ca1dee0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa199175dbe2d11e1d1c8fbb89938bb3266cb83b09c3687df08cc092cb741481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPolicy"))

    @network_policy.setter
    def network_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d5915b44fc88a9939216fa2bffb1bfa4fc7f5c4cdebba405645b789c412846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAllowNonTlsRedirectUri")
    def oauth_allow_non_tls_redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthAllowNonTlsRedirectUri"))

    @oauth_allow_non_tls_redirect_uri.setter
    def oauth_allow_non_tls_redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0bd260e8ebe3f7cfa5aacade2e4946072152d5325c39e91318bc2eacc43fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAllowNonTlsRedirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKey")
    def oauth_client_rsa_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientRsaPublicKey"))

    @oauth_client_rsa_public_key.setter
    def oauth_client_rsa_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eaba61f66cc78bbe0f5fefb01ecd1b234f69d379fcc4db66f2470aab0fad674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientRsaPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKey2")
    def oauth_client_rsa_public_key2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientRsaPublicKey2"))

    @oauth_client_rsa_public_key2.setter
    def oauth_client_rsa_public_key2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da100b4fb7eecd73217a3183758f841ab4e88c7caeefd91f013f4dddc96b7a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientRsaPublicKey2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClientType")
    def oauth_client_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientType"))

    @oauth_client_type.setter
    def oauth_client_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321d2e0f7b423724d86011746a713cc92faf4a805da931d9e1596cceb466ced8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClientType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthEnforcePkce")
    def oauth_enforce_pkce(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthEnforcePkce"))

    @oauth_enforce_pkce.setter
    def oauth_enforce_pkce(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a8686b93fa99375ecdf90886e2039f4cada62325448e46eb366bc664e6a383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthEnforcePkce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthIssueRefreshTokens")
    def oauth_issue_refresh_tokens(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthIssueRefreshTokens"))

    @oauth_issue_refresh_tokens.setter
    def oauth_issue_refresh_tokens(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f229873c3c7f093d3403cc836c93e667e8592c6b80f76edb07b13d33038c679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthIssueRefreshTokens", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthRedirectUri")
    def oauth_redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthRedirectUri"))

    @oauth_redirect_uri.setter
    def oauth_redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db67649c7040cc6897c5ad0e13c1ebe2a37412f4505a2787db10d0bb6626910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthRedirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oauthRefreshTokenValidity"))

    @oauth_refresh_token_validity.setter
    def oauth_refresh_token_validity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01730a1f005616561f9e5f35953606a73e365806c9c4cb23496152549a5cf17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthRefreshTokenValidity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthUseSecondaryRoles")
    def oauth_use_secondary_roles(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthUseSecondaryRoles"))

    @oauth_use_secondary_roles.setter
    def oauth_use_secondary_roles(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1fcf0d7a3f084c8ac48c03611d5d5438bc068c1cd81359e215a36a2b19cf3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthUseSecondaryRoles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preAuthorizedRolesList")
    def pre_authorized_roles_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "preAuthorizedRolesList"))

    @pre_authorized_roles_list.setter
    def pre_authorized_roles_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9d6723105d22e2b44f40bfef8e7466456d1942685c6e7f2c215334384dc0c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preAuthorizedRolesList", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "oauth_client_type": "oauthClientType",
        "oauth_redirect_uri": "oauthRedirectUri",
        "blocked_roles_list": "blockedRolesList",
        "comment": "comment",
        "enabled": "enabled",
        "id": "id",
        "network_policy": "networkPolicy",
        "oauth_allow_non_tls_redirect_uri": "oauthAllowNonTlsRedirectUri",
        "oauth_client_rsa_public_key": "oauthClientRsaPublicKey",
        "oauth_client_rsa_public_key2": "oauthClientRsaPublicKey2",
        "oauth_enforce_pkce": "oauthEnforcePkce",
        "oauth_issue_refresh_tokens": "oauthIssueRefreshTokens",
        "oauth_refresh_token_validity": "oauthRefreshTokenValidity",
        "oauth_use_secondary_roles": "oauthUseSecondaryRoles",
        "pre_authorized_roles_list": "preAuthorizedRolesList",
    },
)
class OauthIntegrationForCustomClientsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        oauth_client_type: builtins.str,
        oauth_redirect_uri: builtins.str,
        blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network_policy: typing.Optional[builtins.str] = None,
        oauth_allow_non_tls_redirect_uri: typing.Optional[builtins.str] = None,
        oauth_client_rsa_public_key: typing.Optional[builtins.str] = None,
        oauth_client_rsa_public_key2: typing.Optional[builtins.str] = None,
        oauth_enforce_pkce: typing.Optional[builtins.str] = None,
        oauth_issue_refresh_tokens: typing.Optional[builtins.str] = None,
        oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
        oauth_use_secondary_roles: typing.Optional[builtins.str] = None,
        pre_authorized_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Specifies the name of the OAuth integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#name OauthIntegrationForCustomClients#name}
        :param oauth_client_type: Specifies the type of client being registered. Snowflake supports both confidential and public clients. Valid options are: ``PUBLIC`` | ``CONFIDENTIAL``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_client_type OauthIntegrationForCustomClients#oauth_client_type}
        :param oauth_redirect_uri: Specifies the client URI. After a user is authenticated, the web browser is redirected to this URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_redirect_uri OauthIntegrationForCustomClients#oauth_redirect_uri}
        :param blocked_roles_list: A set of Snowflake roles that a user cannot explicitly consent to using after authenticating. By default, this list includes the ACCOUNTADMIN, ORGADMIN and SECURITYADMIN roles. To remove these privileged roles from the list, use the ALTER ACCOUNT command to set the OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST account parameter to FALSE. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#blocked_roles_list OauthIntegrationForCustomClients#blocked_roles_list}
        :param comment: Specifies a comment for the OAuth integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#comment OauthIntegrationForCustomClients#comment}
        :param enabled: Specifies whether this OAuth integration is enabled or disabled. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#enabled OauthIntegrationForCustomClients#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#id OauthIntegrationForCustomClients#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_policy: Specifies an existing network policy. This network policy controls network traffic that is attempting to exchange an authorization code for an access or refresh token or to use a refresh token to obtain a new access token. For more information about this resource, see `docs <./network_policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#network_policy OauthIntegrationForCustomClients#network_policy}
        :param oauth_allow_non_tls_redirect_uri: If true, allows setting oauth_redirect_uri to a URI not protected by TLS. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_allow_non_tls_redirect_uri OauthIntegrationForCustomClients#oauth_allow_non_tls_redirect_uri}
        :param oauth_client_rsa_public_key: Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_client_rsa_public_key OauthIntegrationForCustomClients#oauth_client_rsa_public_key}
        :param oauth_client_rsa_public_key2: Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_client_rsa_public_key_2 OauthIntegrationForCustomClients#oauth_client_rsa_public_key_2}
        :param oauth_enforce_pkce: Boolean that specifies whether Proof Key for Code Exchange (PKCE) should be required for the integration. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_enforce_pkce OauthIntegrationForCustomClients#oauth_enforce_pkce}
        :param oauth_issue_refresh_tokens: Specifies whether to allow the client to exchange a refresh token for an access token when the current access token has expired. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_issue_refresh_tokens OauthIntegrationForCustomClients#oauth_issue_refresh_tokens}
        :param oauth_refresh_token_validity: Specifies how long refresh tokens should be valid (in seconds). OAUTH_ISSUE_REFRESH_TOKENS must be set to TRUE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_refresh_token_validity OauthIntegrationForCustomClients#oauth_refresh_token_validity}
        :param oauth_use_secondary_roles: Specifies whether default secondary roles set in the user properties are activated by default in the session being opened. Valid options are: ``IMPLICIT`` | ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_use_secondary_roles OauthIntegrationForCustomClients#oauth_use_secondary_roles}
        :param pre_authorized_roles_list: A set of Snowflake roles that a user does not need to explicitly consent to using after authenticating. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#pre_authorized_roles_list OauthIntegrationForCustomClients#pre_authorized_roles_list}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c8a43e52794a2d6258812389d1b6fe33a164c43cdc9f5f38b31f618978995f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument oauth_client_type", value=oauth_client_type, expected_type=type_hints["oauth_client_type"])
            check_type(argname="argument oauth_redirect_uri", value=oauth_redirect_uri, expected_type=type_hints["oauth_redirect_uri"])
            check_type(argname="argument blocked_roles_list", value=blocked_roles_list, expected_type=type_hints["blocked_roles_list"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network_policy", value=network_policy, expected_type=type_hints["network_policy"])
            check_type(argname="argument oauth_allow_non_tls_redirect_uri", value=oauth_allow_non_tls_redirect_uri, expected_type=type_hints["oauth_allow_non_tls_redirect_uri"])
            check_type(argname="argument oauth_client_rsa_public_key", value=oauth_client_rsa_public_key, expected_type=type_hints["oauth_client_rsa_public_key"])
            check_type(argname="argument oauth_client_rsa_public_key2", value=oauth_client_rsa_public_key2, expected_type=type_hints["oauth_client_rsa_public_key2"])
            check_type(argname="argument oauth_enforce_pkce", value=oauth_enforce_pkce, expected_type=type_hints["oauth_enforce_pkce"])
            check_type(argname="argument oauth_issue_refresh_tokens", value=oauth_issue_refresh_tokens, expected_type=type_hints["oauth_issue_refresh_tokens"])
            check_type(argname="argument oauth_refresh_token_validity", value=oauth_refresh_token_validity, expected_type=type_hints["oauth_refresh_token_validity"])
            check_type(argname="argument oauth_use_secondary_roles", value=oauth_use_secondary_roles, expected_type=type_hints["oauth_use_secondary_roles"])
            check_type(argname="argument pre_authorized_roles_list", value=pre_authorized_roles_list, expected_type=type_hints["pre_authorized_roles_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "oauth_client_type": oauth_client_type,
            "oauth_redirect_uri": oauth_redirect_uri,
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
        if blocked_roles_list is not None:
            self._values["blocked_roles_list"] = blocked_roles_list
        if comment is not None:
            self._values["comment"] = comment
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if network_policy is not None:
            self._values["network_policy"] = network_policy
        if oauth_allow_non_tls_redirect_uri is not None:
            self._values["oauth_allow_non_tls_redirect_uri"] = oauth_allow_non_tls_redirect_uri
        if oauth_client_rsa_public_key is not None:
            self._values["oauth_client_rsa_public_key"] = oauth_client_rsa_public_key
        if oauth_client_rsa_public_key2 is not None:
            self._values["oauth_client_rsa_public_key2"] = oauth_client_rsa_public_key2
        if oauth_enforce_pkce is not None:
            self._values["oauth_enforce_pkce"] = oauth_enforce_pkce
        if oauth_issue_refresh_tokens is not None:
            self._values["oauth_issue_refresh_tokens"] = oauth_issue_refresh_tokens
        if oauth_refresh_token_validity is not None:
            self._values["oauth_refresh_token_validity"] = oauth_refresh_token_validity
        if oauth_use_secondary_roles is not None:
            self._values["oauth_use_secondary_roles"] = oauth_use_secondary_roles
        if pre_authorized_roles_list is not None:
            self._values["pre_authorized_roles_list"] = pre_authorized_roles_list

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
    def name(self) -> builtins.str:
        '''Specifies the name of the OAuth integration.

        This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#name OauthIntegrationForCustomClients#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_client_type(self) -> builtins.str:
        '''Specifies the type of client being registered.

        Snowflake supports both confidential and public clients. Valid options are: ``PUBLIC`` | ``CONFIDENTIAL``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_client_type OauthIntegrationForCustomClients#oauth_client_type}
        '''
        result = self._values.get("oauth_client_type")
        assert result is not None, "Required property 'oauth_client_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_redirect_uri(self) -> builtins.str:
        '''Specifies the client URI. After a user is authenticated, the web browser is redirected to this URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_redirect_uri OauthIntegrationForCustomClients#oauth_redirect_uri}
        '''
        result = self._values.get("oauth_redirect_uri")
        assert result is not None, "Required property 'oauth_redirect_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blocked_roles_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of Snowflake roles that a user cannot explicitly consent to using after authenticating.

        By default, this list includes the ACCOUNTADMIN, ORGADMIN and SECURITYADMIN roles. To remove these privileged roles from the list, use the ALTER ACCOUNT command to set the OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST account parameter to FALSE. For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#blocked_roles_list OauthIntegrationForCustomClients#blocked_roles_list}
        '''
        result = self._values.get("blocked_roles_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the OAuth integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#comment OauthIntegrationForCustomClients#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.str]:
        '''Specifies whether this OAuth integration is enabled or disabled.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#enabled OauthIntegrationForCustomClients#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#id OauthIntegrationForCustomClients#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies an existing network policy.

        This network policy controls network traffic that is attempting to exchange an authorization code for an access or refresh token or to use a refresh token to obtain a new access token. For more information about this resource, see `docs <./network_policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#network_policy OauthIntegrationForCustomClients#network_policy}
        '''
        result = self._values.get("network_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_allow_non_tls_redirect_uri(self) -> typing.Optional[builtins.str]:
        '''If true, allows setting oauth_redirect_uri to a URI not protected by TLS.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_allow_non_tls_redirect_uri OauthIntegrationForCustomClients#oauth_allow_non_tls_redirect_uri}
        '''
        result = self._values.get("oauth_allow_non_tls_redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_client_rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers.

        External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_client_rsa_public_key OauthIntegrationForCustomClients#oauth_client_rsa_public_key}
        '''
        result = self._values.get("oauth_client_rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_client_rsa_public_key2(self) -> typing.Optional[builtins.str]:
        '''Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers.

        External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_client_rsa_public_key_2 OauthIntegrationForCustomClients#oauth_client_rsa_public_key_2}
        '''
        result = self._values.get("oauth_client_rsa_public_key2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_enforce_pkce(self) -> typing.Optional[builtins.str]:
        '''Boolean that specifies whether Proof Key for Code Exchange (PKCE) should be required for the integration.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_enforce_pkce OauthIntegrationForCustomClients#oauth_enforce_pkce}
        '''
        result = self._values.get("oauth_enforce_pkce")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_issue_refresh_tokens(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to allow the client to exchange a refresh token for an access token when the current access token has expired.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_issue_refresh_tokens OauthIntegrationForCustomClients#oauth_issue_refresh_tokens}
        '''
        result = self._values.get("oauth_issue_refresh_tokens")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        '''Specifies how long refresh tokens should be valid (in seconds). OAUTH_ISSUE_REFRESH_TOKENS must be set to TRUE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_refresh_token_validity OauthIntegrationForCustomClients#oauth_refresh_token_validity}
        '''
        result = self._values.get("oauth_refresh_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oauth_use_secondary_roles(self) -> typing.Optional[builtins.str]:
        '''Specifies whether default secondary roles set in the user properties are activated by default in the session being opened.

        Valid options are: ``IMPLICIT`` | ``NONE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#oauth_use_secondary_roles OauthIntegrationForCustomClients#oauth_use_secondary_roles}
        '''
        result = self._values.get("oauth_use_secondary_roles")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_authorized_roles_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of Snowflake roles that a user does not need to explicitly consent to using after authenticating.

        For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_custom_clients#pre_authorized_roles_list OauthIntegrationForCustomClients#pre_authorized_roles_list}
        '''
        result = self._values.get("pre_authorized_roles_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0deaedca00c82bb06306695c557b59133220f15b715ad75bef9129ae6135f99d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2747e532c2851d2412987078a904035d3b657fee6545974f38ce96a9ff3260)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5add06ac140d3cc236fbba3b5489cb72bc32e84f443bad2eecb7dbc49ba7a77f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0a389ddbd7372f6b5762dcb9e4ec4a847a61770113ecd605482952c1ab23b72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fd201e4ecac4e3c3b1afe2ae8fbbe20c1ae65e8f2f594f414ada4e5749523bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__520fe6a5a4bc34038e4fae6aa590d08fa4f136ef81f6cc3f72908a8bce09db7d)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStruct]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79bc93ed366bacffd6ef3a50435848526a0e1aefc0656950d5c7a7cf05662b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputComment",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputComment:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputComment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputCommentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputCommentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bd0f3852957ff0451b3ffaea31bdcf0b1e07ac2b0b0b9011721b4304cbbf626)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputCommentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b412a7c2eea452fb91c4f616de1267cb415c1c210c6d0708ac86958d3b4df6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputCommentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446d8313ad3ce0f5b546c8fcaa3ae06851bbaaaeb9d769d0365bff2e1cd99d73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad65155508d1aa60235a388df250a52d9747c55bc15ed4c2c4ab8d3692edaa5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9921d3830c57bbcc97c0b8f617d7c003aac31f282cb42a5bafc21531a01957e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputCommentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputCommentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0527c8530a44981271665569a6ecd6fd55a8d12b443d46ed169f0e6842d7cc6)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputComment]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputComment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputComment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556a2f5ec6fd7b7906737f4f9f572a03bb9267d54a520617295a426a4f2a4d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputEnabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputEnabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputEnabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputEnabledList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputEnabledList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c205490a25dd4e432c7718dcec0ed8413a0b2c60c9758a858db4e87975dc0c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputEnabledOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9533cfb443b543e801651db3c4453e62864594db999f812d88a3108580abfdaa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputEnabledOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72739b7f3b8296f8704b2bd91675781b127b0cb9a21ce43e2074a282248f03d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__713ee42e357dfb7f3e71708755438d1de43ca69fe94df22e319285600a47de77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a9f892f89f0c068c221c4f5d3ffef724187ca399f6d0a23527d254d157562e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputEnabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputEnabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__939c24fc3d09f33a674aa5eba57b6191817b465b2839b5f60e6eda77036d00a6)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputEnabled]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputEnabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputEnabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8edc3675f5fe96f5bf1248c54230861ac0510c9e11ca6520b156c20e680932e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__673959c1ad904b3f38c5dfce81f4552f667b95c919ec924716f11d919401c758)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11736eacd278c4b5e14af96ddb0717d882c9a54c173828d43aeb90be585e27b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7754f8a10d2b14ce03dc779155aab111fff339f4e2632443e63bdaa34a81bf43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc95f5948c41030c9504c482ceaeb51c1d89036aff7f52f0b83b89d04165bd96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4d07509556eaea738456efac51edf42d37b60ebeb6364d49817de7272e91f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputNetworkPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputNetworkPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputNetworkPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9494dc02d9b5217d01213357401faa16150e1da8a1249923fee0335a1ee7df37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd3c13353deaaf09a9696b8be6728d31154ef4e8156688a88635e2ac8469eae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a33723b42f5138ded5a3eb5fe338fad3841cd5a26182b75cb8f8227ccc2b93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b70443a89a51b266c99c73d120314324e6108690d5ba1e7160dfc68adfc00011)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3509027ea05dc0f9af7909ffe6eeb128c44fdb34ab5294fd31561d24f10ab36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__474111b3ac2234d02a549fae4d8ea218837e22ca2d13b567f27cbfe6579d5a24)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputNetworkPolicy]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputNetworkPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputNetworkPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df7753f36df090f81a85f936c389bbb40de87850afcee6e8c97a2b74a83efe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUri",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUri:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3172e3bbf1799dcfee5b505b08f020a60fde3ba07d6be123d5e14348c0c7fe3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5f5d7da516bc0fe35bd3d03e497f6a7e17312aa4eeb33f1e78eb3e96cf9a61)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6e22fd4e53687bb812bbb8b28d1e024a5ef00dd09cb1b3a9f3bb232ae56a93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd11c1fc4ba553e9abe7e3408be3f1cd1905bf5c46c1cbae5f67d5733187f9de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96ccde2dbadf104bc804bdb6f790eb42cf9ef043c25a82d48d1dcb17f7d0a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c47d20acfc961451988047db42875725dc27e599e094ad747605e836a6393b)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUri]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUri], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUri],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e76c458598464d36411ef868ac5d222bca444a31d19db56360aafeb072d718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f3a9410a553f06c2015acca592749b1d655d626b26cf8d5d20eaf5be04b32b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b294aafb1b615fb1abe4aab710baf0a176f8f445a79acd8fb19786fb0f068a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283ef29315c21f8d4b31c4cd4e221a47b025723b62eca3d045fc007a4f86dd37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__383005dcd8aff11bcec3a7bec4ee591f7337c2ae40f0c8bb2762f0f4172547fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52286eae12bc1bc5eb274cab15e7e9e4570abed607c7727df9c4c3577df81ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__533ce540fbf5b155709c3bb037e5d3096025315e41324e3049d7241884f8e16a)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpoints]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2225e6901301c20b607b80e68fd636399a31ddb376044cd05085f63e91ce9e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53425d0322f2b061c07a11b6ab52c6570e03a5ecf20d27f8a1d8b0e35cd8a705)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f66bf21cf920d3e9995c162e7900f26b2bedf7164bd925055aeb054fa362af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d5ec8c8f1d051a6b5a96bff8c608f9f342eaaa2a4e08f532a380b1c7eff063)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab70e876d350b3f9dff405cb7209a348f20899bf651246dad4586182c029619a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03446c314c8a1aa8e8eb7b381a889e87ee0373669102ca88b3d5dc984ff0ed69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f234a30f275e5b4e307ef42781fec4ccd0f26e07098f65886d7eb66c7eff8d8a)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpoints]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d2e744733bd077dad7b026f352d23a3af9058cedce4fae1dedd380315c658a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28d00f138d4e2bcad74f51083536a35aa1409a4a7c346b0e5934ee2f2e0bdf44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2f9e3fb9042b01e9d0db2100ca05fad20970646f395628826d7670e32b4d0f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a89182943d1be4ad6e8a40d618c0d554871ec6d2f2262775ec82d4cb152ac75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96b0aa8a19e5134d004c6263b68f336ae6b8e581bc19ab7395f14a1994bbca14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71304569af8292d1532ddc9d86711709065788f3e4ef317765f546be120ddfa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a4863e2d5a53e593b3a860e754deac14085e9498c8bb3e56945a5362ff079c)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpoint]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90963a54baf87e4fa154644c2dedecaa58e93a7195e965aa9ec68592a0770f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientId",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthClientId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthClientId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthClientIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a1799b7e904e32da6ca3da2f887684938d6f94c2a57989800277ea24ce5d2da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthClientIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889f5309cecf42a1bb04378d6cce70ed1d592bfc8fec288acd180d7060238975)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthClientIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8838e8002bbf30f63a8f0df5202ebda80fef530848f46a8f54a62b8a52f17895)
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
            type_hints = typing.get_type_hints(_typecheckingstub__553dc0c1726ea03d7c7dd18a4b6c2f418250e82cab5bff8e28858c00a2e57ee1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__957246f4763db8cf9491a80ed3388a05a89b61f42de4d104bc8604bb0db6cf62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthClientIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fb2d199ac2f93660b5f8a35c13ab8154e83c473ccdd7fd3ca52ebb31b08edf3)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientId]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9edfec3399452781819042bb5db712cb2bdc5222ba56d552b2633b151d9393b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2Fp",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2Fp:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2Fp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a6d5999a797edf0d1ab6977590291304aa68e342d5e9467b1f4775f0b03a0df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8432dc1acb35c584d49866f6c78304d4fe46ef9fa18d5945186b5e1a9d8c0dd6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91e86f1f9afab0310f6aed7df11288da684910ebc5d33072ebc5bd32f801fac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6af6bbfdba70d7ebf870cd439a28bfd5cd2cab77210f63d65a07c5ad6c5aee22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c4cfd625f386350ce6ca018873b7663e520af52afc1222b41f15c81aabd67b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab87e390f4475b8d783c786db9def45f6725f08df9149c4884170d4509c57e12)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2Fp]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2Fp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2Fp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4156d4a634c3364ff4d78a89d27a59a4f6d83f5a517c3fb311a5fcad1ba2a02a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFp",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFp:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__625c1a42599b6988a228253e8e6f8b2482d0cb4c9f59f6fa47dfc40196c280b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ce3808cb4c68157ddd053b315128187947adc780d8ebd86e242d2ebef35be6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c610288263e2b1d1ae02bdaf7bb5332d186e2b5f13dcf8db58daab8d18f27f9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb1102d375c483f221d262c72bf340a3f796401468b6fd1ec7de64c7a97ddba0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__695fa6a2cb3b59c42cfdcca6d10889854491d7878c1f008cd0f83d5108d84c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12ce226d15a019e4770339691c39aeebd63e3a8745e29b049ba8479875ed0997)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFp]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1880f5ac341133df487e247e7ecaa9f5d7eaf385e8672e885968051cca882211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientType",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthClientType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthClientType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c10e1e2b7a2471adca9ceaf41d9d65c25c93c74efc761484d0b4dbb33f7ccaab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ffb082b6d691d948565c8104e6ce1d777d8634b373db413f2aeed9cb0ae1ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25237a4edfde58baa3c8de51356658f5898048a3a7e830be4aac79b5701b605a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d758cdd8d8a5608044bbe9545a79397a978a20582d529ef7900f4a347519c0c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ab514aab8b8e3471167ceae5a6e801b21b2976152ccb6aca0e2ab0d64687594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__953deea7b2f6b9e4c64a0259162e9d37f2e2e4e0c232a85b284f2a6e5a7e88e4)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientType]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351fc0f9b5e3fc8de7f9eb30e5713f2e0b39161b3c87552264966763008e343b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkce",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkce:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e82d223047efa0a73340eed40e59998be83dd61ef96c8d0d187c6fa7e516952)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02c2a018a21e11a93049591c1a1c823fad857841684ee172afe36448ca02ef1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26e267c44c2db58c2e3930baeb5be1b9cc3aebf65f6bf61918ac03d08d2b972)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f77e1b64486942978c1c9d77765922e18b63ec24f90e31980c1cd0cbb12f28bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4fdde43ad6ba7a618634151181e742d999eb570d2cf9496aded26887526642d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ecc8c72524e207cd571784f2d55f651b48ef70cc627c79524cecb409c9bcec4)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkce]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441766725939eb6f6d709d3e6736ec1893c69647c2cdd8b0b83d2a077d190635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokens",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokens:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokens(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0549ada9fc616f478bffade2a9a438f2bd7dd4722708c688efe844424603a20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23fd64191047946caa36e1ebb380d0b376644aff8b8234c8a349917a1e13480)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6bd35a0d6fefdf6b34e0507bd135e5a1ce7f43f130c1d98dae7726bb6e65e4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49ef9b446c3b9459368228e39d3544108b016c8f2a48e474b2b3468e4f136df6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b8b7c2b3f70f335cfcde6a1cfacf1a2c0ddfcff04189a86a0ae3a1a7c5e6b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e8977591a6ba2e330506d698dfb6bdf495016ac39a96bc79d87de0d3862972b)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokens]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokens], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokens],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ba979d4429d3b70da4350fe865cd3386f3116a79318e067493cbc8236ca29a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUri",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUri:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df6fa6df1e93d3b495f32f760674356753b492e2646c6feddfbb6d2ee46e42bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d14e8117392dfbdea597353d4f509db4c5e6253c202fe646aff39cef876d44e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d8bc09f558b3b96f9f95b703f9f63a4555e09f1302e307929d36bdfe2f3c0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99eb7eaeb83a328d4b8e163651a34ccb9bef88baf2e47a2923b5b49266d900f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db29a12a2b54607a330acabe5d1f397ad69450e1f8deb1aa21b6f2b381d096f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b2d0799d587d9ecdf7135d063511d6f29d27f0b595cf13fc560f022ef2d7238)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUri]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUri], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUri],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9cecf962612e57b1b8b7de79ed618688e47faba3823595a737c4a3a8f6d0c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9a1ffd14cbaa115f25d47f62a8621c2940aef1c8e4e7ecc3bfb954892f76699)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d94f0563d448a424b3632fab91f61d4042c57ea0dbc85aeec30e86740a329fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76176f04f3d09b09e38100228752850b68a1ef965808d1d2ebf1406a20c7cca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac23da4cc85ecdaf312a0fd3da4b8feff08de8cba28bf6601153ba6bffb836b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__982837efac23512ded7e17ff6e97070c89c495378d910b516ee89204ab8da8ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__012719a8b0ae68324da71440e32db78ca393607bab17392a3772c8c080a8116f)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidity]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ace2dd5efd6c7d5fcade28efb37560fa6a2d1c8122268897d749a7fb6aecaf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db0819c627e5901418cc14f0f59f4725498db53989d1849d7545478676374598)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4ff2419cae0b270e32945371c38b1f9e027ee872be8ac3fb1bf42a9790a93b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6c6d48decca6c3637584212976752b999160f197070a0e03ff9be977f2917f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfe8bb2d09da2fbf59248470d706427a7368743cfd752a988b7659d9dff216c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10c062c339c051a8fb233b338960837af5a83ccb11b39c61099624c7c7cb191f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3463954a35c2bc438a9530d99ba4f255f520afcb0e98b86f98d8fc1ad7e86065)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpoint]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6986562ecae1a4049b479088c4e97df14b2b1e55eb444bfcadb79106aef037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRoles",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRoles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cde613ac749af43a1fe92c64523fbbaa7c86490e079b7523ad867cbb1652e717)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6872f9af5c0e94d242d79aa63cfedf2cb92d51d0f1dc59f400ee415d7f37c581)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef629b2d545b089a368ff3e083c872be80291ecab06aae2c42f40e8cffb850cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0aa9cdc12fc2c08ab29b473fd046bb4ad8e66fc2dda025f706bcecd0aaf07c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a59f816ada58b8df9cfb3272980163b8e406621834f2285f2f0a85c649cccac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__408b7aa1dc9b73e16fddd9132b9a0054b0ae8706ce21bb79db1881c5734432bd)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRoles]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRoles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRoles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d60d168b855394e2c3da40a3082631bce5ccd5a634cb21241d527ea5872b78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3b94f8fd5b9c31f1d5f4d594ab362ef176a394bdd19bdbf526ec9223d2a98db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="blockedRolesList")
    def blocked_roles_list(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructList, jsii.get(self, "blockedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> OauthIntegrationForCustomClientsDescribeOutputCommentList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputCommentList, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> OauthIntegrationForCustomClientsDescribeOutputEnabledList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputEnabledList, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyList, jsii.get(self, "networkPolicy"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedAuthorizationEndpoints")
    def oauth_allowed_authorization_endpoints(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsList, jsii.get(self, "oauthAllowedAuthorizationEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedTokenEndpoints")
    def oauth_allowed_token_endpoints(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsList, jsii.get(self, "oauthAllowedTokenEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowNonTlsRedirectUri")
    def oauth_allow_non_tls_redirect_uri(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriList, jsii.get(self, "oauthAllowNonTlsRedirectUri"))

    @builtins.property
    @jsii.member(jsii_name="oauthAuthorizationEndpoint")
    def oauth_authorization_endpoint(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointList, jsii.get(self, "oauthAuthorizationEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthClientIdList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthClientIdList, jsii.get(self, "oauthClientId"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKey2Fp")
    def oauth_client_rsa_public_key2_fp(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpList, jsii.get(self, "oauthClientRsaPublicKey2Fp"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKeyFp")
    def oauth_client_rsa_public_key_fp(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpList, jsii.get(self, "oauthClientRsaPublicKeyFp"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientType")
    def oauth_client_type(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeList, jsii.get(self, "oauthClientType"))

    @builtins.property
    @jsii.member(jsii_name="oauthEnforcePkce")
    def oauth_enforce_pkce(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceList, jsii.get(self, "oauthEnforcePkce"))

    @builtins.property
    @jsii.member(jsii_name="oauthIssueRefreshTokens")
    def oauth_issue_refresh_tokens(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensList, jsii.get(self, "oauthIssueRefreshTokens"))

    @builtins.property
    @jsii.member(jsii_name="oauthRedirectUri")
    def oauth_redirect_uri(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriList, jsii.get(self, "oauthRedirectUri"))

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityList, jsii.get(self, "oauthRefreshTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpoint")
    def oauth_token_endpoint(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointList, jsii.get(self, "oauthTokenEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="oauthUseSecondaryRoles")
    def oauth_use_secondary_roles(
        self,
    ) -> OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesList:
        return typing.cast(OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesList, jsii.get(self, "oauthUseSecondaryRoles"))

    @builtins.property
    @jsii.member(jsii_name="preAuthorizedRolesList")
    def pre_authorized_roles_list(
        self,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructList":
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructList", jsii.get(self, "preAuthorizedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutput]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c7d006b78d3287c9b05380ac0128ba6b3032372b8be3b61b3cc9bc5b37f07d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af8622a8021a6bf6805cb04a09c86220d4e34195fc33a3ce647c34c5d2f478fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758b576d95ff160f4de925b39a2aa5b0a714a6ec571bf795d63497108e778063)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba4eb7b7b50c6d199889bc37685ad06751232dbe089382c6081e8d17e0b114b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44b1036d45791c8bf39bcfd630f360cd773daf06288efcfe592cb295adff596b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69118d10468d2d61ea557734cb822df12b0f680bff83a3ee76e8cdb26d00dd71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b801c4b7a91e43d8dbcec619bd85d6fb1db70a797edf50c8b4490c5aa75feea)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStruct]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4953c938f4c9120affd77ce2c3b134da050d87c85be92b1a7faa8dfa05882c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsRelatedParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsRelatedParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsRelatedParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsRelatedParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsRelatedParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1579219aa8e992bb8dec2bbb3034bfa9e32ac7e65d2e3996ddda6f1a7fd6228e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsRelatedParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1632a09f0c60b87105dd7372fa5a626d96d281323137a51df904038796438aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsRelatedParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709d9e952f2a2687abdb1af5e0e1f0cf2a1d2dc0202c020e33abdbc9b1df65a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b725448043c27c010c60338eddf54d7f1cac5ab378f8aeffde4ff7275b90df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9e04216b3abf01bff8dbb1a4cff8980a36c8621eae5609695da6075dd8df939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe442ee83ed0236fbb574cecb7b3bff32fd528c2b5057d5dc5d5746781141e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba47ba054d32f0c8efb8326e3c325111387950459d725a06b2d1871c6507d84f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675ba51451f2fc3dbdd18b075e195c27e0706c13ac3fc8cf0ddc126a6252b81f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__577dedc801b3ee8a99b6dd358f6611d7a7cb6e3f39cc3d37d6ca04ad490ba4da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99ca8c6f558b3130b477a55cc0af598fad45241a2b4b1af68999b6d551452055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd36644c870c42419eaa0d786821618b8f87fde09879060e32960f252366af8d)
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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d86b5714c1aceedf4f43c6e5b08feca6d03eef56c3e5e9cee86f84f50398dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsRelatedParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsRelatedParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05c3cd402c919a1c8f1fed5249eb8fb5649e7038905a1aaac7b0ec3f845bcce2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="oauthAddPrivilegedRolesToBlockedList")
    def oauth_add_privileged_roles_to_blocked_list(
        self,
    ) -> OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList:
        return typing.cast(OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList, jsii.get(self, "oauthAddPrivilegedRolesToBlockedList"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OauthIntegrationForCustomClientsRelatedParameters]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsRelatedParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsRelatedParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfaa8fdea2bb347685211bce483c5cf685f4582a4a52b6e3997a8c82bb41e303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForCustomClientsShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForCustomClientsShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForCustomClientsShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b08384ecc9f1f69b8a337b742ac4f0aa887ff0872e3bb8ea94e1a60bc27908f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForCustomClientsShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efd7e9b183fc0e76c7254846afc11199407b87de8e01a2f844b00bef5fe3379)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForCustomClientsShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf4a123aca141f080514b96232c8b6e39d4ecfd577863d217f6d064b6e5d134)
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
            type_hints = typing.get_type_hints(_typecheckingstub__570f734061f98c4d8212c6552090d4f64777520b49257d53a20e28da340b99e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83181a7a207dc30080904a3de897b95581b66acabea79c0d2762ea8c8113b9c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForCustomClientsShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForCustomClients.OauthIntegrationForCustomClientsShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bab1f00744dac839d07a3ae2a34a90b3853bc2fd66ea78dab975fd6e0e7d868)
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
    ) -> typing.Optional[OauthIntegrationForCustomClientsShowOutput]:
        return typing.cast(typing.Optional[OauthIntegrationForCustomClientsShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForCustomClientsShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a849ee5ba706f4934ccc23b202f7a0a2782764430cdbc9c4ed5389baebf174ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OauthIntegrationForCustomClients",
    "OauthIntegrationForCustomClientsConfig",
    "OauthIntegrationForCustomClientsDescribeOutput",
    "OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStruct",
    "OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructList",
    "OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStructOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputComment",
    "OauthIntegrationForCustomClientsDescribeOutputCommentList",
    "OauthIntegrationForCustomClientsDescribeOutputCommentOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputEnabled",
    "OauthIntegrationForCustomClientsDescribeOutputEnabledList",
    "OauthIntegrationForCustomClientsDescribeOutputEnabledOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputList",
    "OauthIntegrationForCustomClientsDescribeOutputNetworkPolicy",
    "OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyList",
    "OauthIntegrationForCustomClientsDescribeOutputNetworkPolicyOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUri",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpoints",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpoints",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpointsOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpoint",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpointOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientId",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientIdList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientIdOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2Fp",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2FpOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFp",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFpOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientType",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthClientTypeOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkce",
    "OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkceOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokens",
    "OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokensOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUri",
    "OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUriOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidity",
    "OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidityOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpoint",
    "OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpointOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRoles",
    "OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesList",
    "OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRolesOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputOutputReference",
    "OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStruct",
    "OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructList",
    "OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStructOutputReference",
    "OauthIntegrationForCustomClientsRelatedParameters",
    "OauthIntegrationForCustomClientsRelatedParametersList",
    "OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct",
    "OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList",
    "OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference",
    "OauthIntegrationForCustomClientsRelatedParametersOutputReference",
    "OauthIntegrationForCustomClientsShowOutput",
    "OauthIntegrationForCustomClientsShowOutputList",
    "OauthIntegrationForCustomClientsShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__528f8f9a1366d8cfe0bd8ffd145c6f15a4f9143c37463875f1fc1edb7f0c85c9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    oauth_client_type: builtins.str,
    oauth_redirect_uri: builtins.str,
    blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network_policy: typing.Optional[builtins.str] = None,
    oauth_allow_non_tls_redirect_uri: typing.Optional[builtins.str] = None,
    oauth_client_rsa_public_key: typing.Optional[builtins.str] = None,
    oauth_client_rsa_public_key2: typing.Optional[builtins.str] = None,
    oauth_enforce_pkce: typing.Optional[builtins.str] = None,
    oauth_issue_refresh_tokens: typing.Optional[builtins.str] = None,
    oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
    oauth_use_secondary_roles: typing.Optional[builtins.str] = None,
    pre_authorized_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__dbd06f252dae3bb51aa9017d40531332aefa857283f16dfc2f99711bb871ae38(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced58dc01137c39cdde09281c1901b4cf8b2ecc26b2f56c3445a730e1f2bf010(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397b7bbb0f3fabc99d18d45d2116a9b3ed2939c14d5a08d289d32023117a3dbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d1887dafe846d74e6c1ff60922690b6edf4466125580471eac5ae9d3392b0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be64b703f8d2a05b7e06c2911a820f3bcb7e547f15cb0f08c9c25bb3ca1dee0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa199175dbe2d11e1d1c8fbb89938bb3266cb83b09c3687df08cc092cb741481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d5915b44fc88a9939216fa2bffb1bfa4fc7f5c4cdebba405645b789c412846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0bd260e8ebe3f7cfa5aacade2e4946072152d5325c39e91318bc2eacc43fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eaba61f66cc78bbe0f5fefb01ecd1b234f69d379fcc4db66f2470aab0fad674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da100b4fb7eecd73217a3183758f841ab4e88c7caeefd91f013f4dddc96b7a04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321d2e0f7b423724d86011746a713cc92faf4a805da931d9e1596cceb466ced8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a8686b93fa99375ecdf90886e2039f4cada62325448e46eb366bc664e6a383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f229873c3c7f093d3403cc836c93e667e8592c6b80f76edb07b13d33038c679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db67649c7040cc6897c5ad0e13c1ebe2a37412f4505a2787db10d0bb6626910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01730a1f005616561f9e5f35953606a73e365806c9c4cb23496152549a5cf17(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1fcf0d7a3f084c8ac48c03611d5d5438bc068c1cd81359e215a36a2b19cf3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9d6723105d22e2b44f40bfef8e7466456d1942685c6e7f2c215334384dc0c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c8a43e52794a2d6258812389d1b6fe33a164c43cdc9f5f38b31f618978995f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    oauth_client_type: builtins.str,
    oauth_redirect_uri: builtins.str,
    blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network_policy: typing.Optional[builtins.str] = None,
    oauth_allow_non_tls_redirect_uri: typing.Optional[builtins.str] = None,
    oauth_client_rsa_public_key: typing.Optional[builtins.str] = None,
    oauth_client_rsa_public_key2: typing.Optional[builtins.str] = None,
    oauth_enforce_pkce: typing.Optional[builtins.str] = None,
    oauth_issue_refresh_tokens: typing.Optional[builtins.str] = None,
    oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
    oauth_use_secondary_roles: typing.Optional[builtins.str] = None,
    pre_authorized_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0deaedca00c82bb06306695c557b59133220f15b715ad75bef9129ae6135f99d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2747e532c2851d2412987078a904035d3b657fee6545974f38ce96a9ff3260(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5add06ac140d3cc236fbba3b5489cb72bc32e84f443bad2eecb7dbc49ba7a77f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a389ddbd7372f6b5762dcb9e4ec4a847a61770113ecd605482952c1ab23b72(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd201e4ecac4e3c3b1afe2ae8fbbe20c1ae65e8f2f594f414ada4e5749523bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520fe6a5a4bc34038e4fae6aa590d08fa4f136ef81f6cc3f72908a8bce09db7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79bc93ed366bacffd6ef3a50435848526a0e1aefc0656950d5c7a7cf05662b7(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputBlockedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd0f3852957ff0451b3ffaea31bdcf0b1e07ac2b0b0b9011721b4304cbbf626(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b412a7c2eea452fb91c4f616de1267cb415c1c210c6d0708ac86958d3b4df6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446d8313ad3ce0f5b546c8fcaa3ae06851bbaaaeb9d769d0365bff2e1cd99d73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad65155508d1aa60235a388df250a52d9747c55bc15ed4c2c4ab8d3692edaa5d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9921d3830c57bbcc97c0b8f617d7c003aac31f282cb42a5bafc21531a01957e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0527c8530a44981271665569a6ecd6fd55a8d12b443d46ed169f0e6842d7cc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556a2f5ec6fd7b7906737f4f9f572a03bb9267d54a520617295a426a4f2a4d3f(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputComment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c205490a25dd4e432c7718dcec0ed8413a0b2c60c9758a858db4e87975dc0c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9533cfb443b543e801651db3c4453e62864594db999f812d88a3108580abfdaa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72739b7f3b8296f8704b2bd91675781b127b0cb9a21ce43e2074a282248f03d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713ee42e357dfb7f3e71708755438d1de43ca69fe94df22e319285600a47de77(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9f892f89f0c068c221c4f5d3ffef724187ca399f6d0a23527d254d157562e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939c24fc3d09f33a674aa5eba57b6191817b465b2839b5f60e6eda77036d00a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8edc3675f5fe96f5bf1248c54230861ac0510c9e11ca6520b156c20e680932e(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputEnabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673959c1ad904b3f38c5dfce81f4552f667b95c919ec924716f11d919401c758(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11736eacd278c4b5e14af96ddb0717d882c9a54c173828d43aeb90be585e27b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7754f8a10d2b14ce03dc779155aab111fff339f4e2632443e63bdaa34a81bf43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc95f5948c41030c9504c482ceaeb51c1d89036aff7f52f0b83b89d04165bd96(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d07509556eaea738456efac51edf42d37b60ebeb6364d49817de7272e91f09(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9494dc02d9b5217d01213357401faa16150e1da8a1249923fee0335a1ee7df37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd3c13353deaaf09a9696b8be6728d31154ef4e8156688a88635e2ac8469eae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a33723b42f5138ded5a3eb5fe338fad3841cd5a26182b75cb8f8227ccc2b93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70443a89a51b266c99c73d120314324e6108690d5ba1e7160dfc68adfc00011(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3509027ea05dc0f9af7909ffe6eeb128c44fdb34ab5294fd31561d24f10ab36c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474111b3ac2234d02a549fae4d8ea218837e22ca2d13b567f27cbfe6579d5a24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df7753f36df090f81a85f936c389bbb40de87850afcee6e8c97a2b74a83efe2(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputNetworkPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3172e3bbf1799dcfee5b505b08f020a60fde3ba07d6be123d5e14348c0c7fe3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5f5d7da516bc0fe35bd3d03e497f6a7e17312aa4eeb33f1e78eb3e96cf9a61(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6e22fd4e53687bb812bbb8b28d1e024a5ef00dd09cb1b3a9f3bb232ae56a93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd11c1fc4ba553e9abe7e3408be3f1cd1905bf5c46c1cbae5f67d5733187f9de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96ccde2dbadf104bc804bdb6f790eb42cf9ef043c25a82d48d1dcb17f7d0a02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c47d20acfc961451988047db42875725dc27e599e094ad747605e836a6393b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e76c458598464d36411ef868ac5d222bca444a31d19db56360aafeb072d718(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowNonTlsRedirectUri],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f3a9410a553f06c2015acca592749b1d655d626b26cf8d5d20eaf5be04b32b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b294aafb1b615fb1abe4aab710baf0a176f8f445a79acd8fb19786fb0f068a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283ef29315c21f8d4b31c4cd4e221a47b025723b62eca3d045fc007a4f86dd37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383005dcd8aff11bcec3a7bec4ee591f7337c2ae40f0c8bb2762f0f4172547fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52286eae12bc1bc5eb274cab15e7e9e4570abed607c7727df9c4c3577df81ae7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533ce540fbf5b155709c3bb037e5d3096025315e41324e3049d7241884f8e16a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2225e6901301c20b607b80e68fd636399a31ddb376044cd05085f63e91ce9e7b(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowedAuthorizationEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53425d0322f2b061c07a11b6ab52c6570e03a5ecf20d27f8a1d8b0e35cd8a705(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f66bf21cf920d3e9995c162e7900f26b2bedf7164bd925055aeb054fa362af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d5ec8c8f1d051a6b5a96bff8c608f9f342eaaa2a4e08f532a380b1c7eff063(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab70e876d350b3f9dff405cb7209a348f20899bf651246dad4586182c029619a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03446c314c8a1aa8e8eb7b381a889e87ee0373669102ca88b3d5dc984ff0ed69(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f234a30f275e5b4e307ef42781fec4ccd0f26e07098f65886d7eb66c7eff8d8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d2e744733bd077dad7b026f352d23a3af9058cedce4fae1dedd380315c658a(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAllowedTokenEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d00f138d4e2bcad74f51083536a35aa1409a4a7c346b0e5934ee2f2e0bdf44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2f9e3fb9042b01e9d0db2100ca05fad20970646f395628826d7670e32b4d0f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a89182943d1be4ad6e8a40d618c0d554871ec6d2f2262775ec82d4cb152ac75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b0aa8a19e5134d004c6263b68f336ae6b8e581bc19ab7395f14a1994bbca14(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71304569af8292d1532ddc9d86711709065788f3e4ef317765f546be120ddfa4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a4863e2d5a53e593b3a860e754deac14085e9498c8bb3e56945a5362ff079c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90963a54baf87e4fa154644c2dedecaa58e93a7195e965aa9ec68592a0770f63(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthAuthorizationEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1799b7e904e32da6ca3da2f887684938d6f94c2a57989800277ea24ce5d2da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889f5309cecf42a1bb04378d6cce70ed1d592bfc8fec288acd180d7060238975(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8838e8002bbf30f63a8f0df5202ebda80fef530848f46a8f54a62b8a52f17895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553dc0c1726ea03d7c7dd18a4b6c2f418250e82cab5bff8e28858c00a2e57ee1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957246f4763db8cf9491a80ed3388a05a89b61f42de4d104bc8604bb0db6cf62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb2d199ac2f93660b5f8a35c13ab8154e83c473ccdd7fd3ca52ebb31b08edf3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edfec3399452781819042bb5db712cb2bdc5222ba56d552b2633b151d9393b5(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6d5999a797edf0d1ab6977590291304aa68e342d5e9467b1f4775f0b03a0df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8432dc1acb35c584d49866f6c78304d4fe46ef9fa18d5945186b5e1a9d8c0dd6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91e86f1f9afab0310f6aed7df11288da684910ebc5d33072ebc5bd32f801fac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af6bbfdba70d7ebf870cd439a28bfd5cd2cab77210f63d65a07c5ad6c5aee22(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4cfd625f386350ce6ca018873b7663e520af52afc1222b41f15c81aabd67b2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab87e390f4475b8d783c786db9def45f6725f08df9149c4884170d4509c57e12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4156d4a634c3364ff4d78a89d27a59a4f6d83f5a517c3fb311a5fcad1ba2a02a(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKey2Fp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625c1a42599b6988a228253e8e6f8b2482d0cb4c9f59f6fa47dfc40196c280b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ce3808cb4c68157ddd053b315128187947adc780d8ebd86e242d2ebef35be6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c610288263e2b1d1ae02bdaf7bb5332d186e2b5f13dcf8db58daab8d18f27f9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1102d375c483f221d262c72bf340a3f796401468b6fd1ec7de64c7a97ddba0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695fa6a2cb3b59c42cfdcca6d10889854491d7878c1f008cd0f83d5108d84c5a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ce226d15a019e4770339691c39aeebd63e3a8745e29b049ba8479875ed0997(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1880f5ac341133df487e247e7ecaa9f5d7eaf385e8672e885968051cca882211(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientRsaPublicKeyFp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10e1e2b7a2471adca9ceaf41d9d65c25c93c74efc761484d0b4dbb33f7ccaab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ffb082b6d691d948565c8104e6ce1d777d8634b373db413f2aeed9cb0ae1ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25237a4edfde58baa3c8de51356658f5898048a3a7e830be4aac79b5701b605a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d758cdd8d8a5608044bbe9545a79397a978a20582d529ef7900f4a347519c0c6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab514aab8b8e3471167ceae5a6e801b21b2976152ccb6aca0e2ab0d64687594(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953deea7b2f6b9e4c64a0259162e9d37f2e2e4e0c232a85b284f2a6e5a7e88e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351fc0f9b5e3fc8de7f9eb30e5713f2e0b39161b3c87552264966763008e343b(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthClientType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e82d223047efa0a73340eed40e59998be83dd61ef96c8d0d187c6fa7e516952(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02c2a018a21e11a93049591c1a1c823fad857841684ee172afe36448ca02ef1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26e267c44c2db58c2e3930baeb5be1b9cc3aebf65f6bf61918ac03d08d2b972(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77e1b64486942978c1c9d77765922e18b63ec24f90e31980c1cd0cbb12f28bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fdde43ad6ba7a618634151181e742d999eb570d2cf9496aded26887526642d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ecc8c72524e207cd571784f2d55f651b48ef70cc627c79524cecb409c9bcec4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441766725939eb6f6d709d3e6736ec1893c69647c2cdd8b0b83d2a077d190635(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthEnforcePkce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0549ada9fc616f478bffade2a9a438f2bd7dd4722708c688efe844424603a20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23fd64191047946caa36e1ebb380d0b376644aff8b8234c8a349917a1e13480(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bd35a0d6fefdf6b34e0507bd135e5a1ce7f43f130c1d98dae7726bb6e65e4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ef9b446c3b9459368228e39d3544108b016c8f2a48e474b2b3468e4f136df6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8b7c2b3f70f335cfcde6a1cfacf1a2c0ddfcff04189a86a0ae3a1a7c5e6b5b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8977591a6ba2e330506d698dfb6bdf495016ac39a96bc79d87de0d3862972b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ba979d4429d3b70da4350fe865cd3386f3116a79318e067493cbc8236ca29a(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthIssueRefreshTokens],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6fa6df1e93d3b495f32f760674356753b492e2646c6feddfbb6d2ee46e42bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d14e8117392dfbdea597353d4f509db4c5e6253c202fe646aff39cef876d44e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d8bc09f558b3b96f9f95b703f9f63a4555e09f1302e307929d36bdfe2f3c0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99eb7eaeb83a328d4b8e163651a34ccb9bef88baf2e47a2923b5b49266d900f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db29a12a2b54607a330acabe5d1f397ad69450e1f8deb1aa21b6f2b381d096f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2d0799d587d9ecdf7135d063511d6f29d27f0b595cf13fc560f022ef2d7238(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9cecf962612e57b1b8b7de79ed618688e47faba3823595a737c4a3a8f6d0c6(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthRedirectUri],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a1ffd14cbaa115f25d47f62a8621c2940aef1c8e4e7ecc3bfb954892f76699(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d94f0563d448a424b3632fab91f61d4042c57ea0dbc85aeec30e86740a329fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76176f04f3d09b09e38100228752850b68a1ef965808d1d2ebf1406a20c7cca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac23da4cc85ecdaf312a0fd3da4b8feff08de8cba28bf6601153ba6bffb836b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982837efac23512ded7e17ff6e97070c89c495378d910b516ee89204ab8da8ae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012719a8b0ae68324da71440e32db78ca393607bab17392a3772c8c080a8116f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ace2dd5efd6c7d5fcade28efb37560fa6a2d1c8122268897d749a7fb6aecaf3(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthRefreshTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0819c627e5901418cc14f0f59f4725498db53989d1849d7545478676374598(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4ff2419cae0b270e32945371c38b1f9e027ee872be8ac3fb1bf42a9790a93b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6c6d48decca6c3637584212976752b999160f197070a0e03ff9be977f2917f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe8bb2d09da2fbf59248470d706427a7368743cfd752a988b7659d9dff216c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c062c339c051a8fb233b338960837af5a83ccb11b39c61099624c7c7cb191f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3463954a35c2bc438a9530d99ba4f255f520afcb0e98b86f98d8fc1ad7e86065(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6986562ecae1a4049b479088c4e97df14b2b1e55eb444bfcadb79106aef037(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthTokenEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde613ac749af43a1fe92c64523fbbaa7c86490e079b7523ad867cbb1652e717(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6872f9af5c0e94d242d79aa63cfedf2cb92d51d0f1dc59f400ee415d7f37c581(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef629b2d545b089a368ff3e083c872be80291ecab06aae2c42f40e8cffb850cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0aa9cdc12fc2c08ab29b473fd046bb4ad8e66fc2dda025f706bcecd0aaf07c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59f816ada58b8df9cfb3272980163b8e406621834f2285f2f0a85c649cccac5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408b7aa1dc9b73e16fddd9132b9a0054b0ae8706ce21bb79db1881c5734432bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d60d168b855394e2c3da40a3082631bce5ccd5a634cb21241d527ea5872b78e(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputOauthUseSecondaryRoles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b94f8fd5b9c31f1d5f4d594ab362ef176a394bdd19bdbf526ec9223d2a98db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c7d006b78d3287c9b05380ac0128ba6b3032372b8be3b61b3cc9bc5b37f07d(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8622a8021a6bf6805cb04a09c86220d4e34195fc33a3ce647c34c5d2f478fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758b576d95ff160f4de925b39a2aa5b0a714a6ec571bf795d63497108e778063(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba4eb7b7b50c6d199889bc37685ad06751232dbe089382c6081e8d17e0b114b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b1036d45791c8bf39bcfd630f360cd773daf06288efcfe592cb295adff596b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69118d10468d2d61ea557734cb822df12b0f680bff83a3ee76e8cdb26d00dd71(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b801c4b7a91e43d8dbcec619bd85d6fb1db70a797edf50c8b4490c5aa75feea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4953c938f4c9120affd77ce2c3b134da050d87c85be92b1a7faa8dfa05882c2(
    value: typing.Optional[OauthIntegrationForCustomClientsDescribeOutputPreAuthorizedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1579219aa8e992bb8dec2bbb3034bfa9e32ac7e65d2e3996ddda6f1a7fd6228e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1632a09f0c60b87105dd7372fa5a626d96d281323137a51df904038796438aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709d9e952f2a2687abdb1af5e0e1f0cf2a1d2dc0202c020e33abdbc9b1df65a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b725448043c27c010c60338eddf54d7f1cac5ab378f8aeffde4ff7275b90df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e04216b3abf01bff8dbb1a4cff8980a36c8621eae5609695da6075dd8df939(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe442ee83ed0236fbb574cecb7b3bff32fd528c2b5057d5dc5d5746781141e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba47ba054d32f0c8efb8326e3c325111387950459d725a06b2d1871c6507d84f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675ba51451f2fc3dbdd18b075e195c27e0706c13ac3fc8cf0ddc126a6252b81f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__577dedc801b3ee8a99b6dd358f6611d7a7cb6e3f39cc3d37d6ca04ad490ba4da(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ca8c6f558b3130b477a55cc0af598fad45241a2b4b1af68999b6d551452055(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd36644c870c42419eaa0d786821618b8f87fde09879060e32960f252366af8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d86b5714c1aceedf4f43c6e5b08feca6d03eef56c3e5e9cee86f84f50398dfd(
    value: typing.Optional[OauthIntegrationForCustomClientsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c3cd402c919a1c8f1fed5249eb8fb5649e7038905a1aaac7b0ec3f845bcce2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfaa8fdea2bb347685211bce483c5cf685f4582a4a52b6e3997a8c82bb41e303(
    value: typing.Optional[OauthIntegrationForCustomClientsRelatedParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b08384ecc9f1f69b8a337b742ac4f0aa887ff0872e3bb8ea94e1a60bc27908f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efd7e9b183fc0e76c7254846afc11199407b87de8e01a2f844b00bef5fe3379(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf4a123aca141f080514b96232c8b6e39d4ecfd577863d217f6d064b6e5d134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570f734061f98c4d8212c6552090d4f64777520b49257d53a20e28da340b99e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83181a7a207dc30080904a3de897b95581b66acabea79c0d2762ea8c8113b9c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bab1f00744dac839d07a3ae2a34a90b3853bc2fd66ea78dab975fd6e0e7d868(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a849ee5ba706f4934ccc23b202f7a0a2782764430cdbc9c4ed5389baebf174ea(
    value: typing.Optional[OauthIntegrationForCustomClientsShowOutput],
) -> None:
    """Type checking stubs"""
    pass
