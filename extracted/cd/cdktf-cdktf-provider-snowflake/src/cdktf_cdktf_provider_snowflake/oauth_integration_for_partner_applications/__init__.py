r'''
# `snowflake_oauth_integration_for_partner_applications`

Refer to the Terraform Registry for docs: [`snowflake_oauth_integration_for_partner_applications`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications).
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


class OauthIntegrationForPartnerApplications(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplications",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications snowflake_oauth_integration_for_partner_applications}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        oauth_client: builtins.str,
        blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oauth_issue_refresh_tokens: typing.Optional[builtins.str] = None,
        oauth_redirect_uri: typing.Optional[builtins.str] = None,
        oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
        oauth_use_secondary_roles: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications snowflake_oauth_integration_for_partner_applications} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Specifies the name of the OAuth integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#name OauthIntegrationForPartnerApplications#name}
        :param oauth_client: Creates an OAuth interface between Snowflake and a partner application. Valid options are: ``LOOKER`` | ``TABLEAU_DESKTOP`` | ``TABLEAU_SERVER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_client OauthIntegrationForPartnerApplications#oauth_client}
        :param blocked_roles_list: A set of Snowflake roles that a user cannot explicitly consent to using after authenticating. By default, this list includes the ACCOUNTADMIN, ORGADMIN and SECURITYADMIN roles. To remove these privileged roles from the list, use the ALTER ACCOUNT command to set the OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST account parameter to FALSE. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#blocked_roles_list OauthIntegrationForPartnerApplications#blocked_roles_list}
        :param comment: Specifies a comment for the OAuth integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#comment OauthIntegrationForPartnerApplications#comment}
        :param enabled: Specifies whether this OAuth integration is enabled or disabled. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#enabled OauthIntegrationForPartnerApplications#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#id OauthIntegrationForPartnerApplications#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oauth_issue_refresh_tokens: Specifies whether to allow the client to exchange a refresh token for an access token when the current access token has expired. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_issue_refresh_tokens OauthIntegrationForPartnerApplications#oauth_issue_refresh_tokens}
        :param oauth_redirect_uri: Specifies the client URI. After a user is authenticated, the web browser is redirected to this URI. The field should be only set when OAUTH_CLIENT = LOOKER. In any other case the field should be left out empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_redirect_uri OauthIntegrationForPartnerApplications#oauth_redirect_uri}
        :param oauth_refresh_token_validity: Specifies how long refresh tokens should be valid (in seconds). OAUTH_ISSUE_REFRESH_TOKENS must be set to TRUE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_refresh_token_validity OauthIntegrationForPartnerApplications#oauth_refresh_token_validity}
        :param oauth_use_secondary_roles: Specifies whether default secondary roles set in the user properties are activated by default in the session being opened. Valid options are: ``IMPLICIT`` | ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_use_secondary_roles OauthIntegrationForPartnerApplications#oauth_use_secondary_roles}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90df3a7593055b3842f7b95a64f325944cea311964db1611991b757d07b480ff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OauthIntegrationForPartnerApplicationsConfig(
            name=name,
            oauth_client=oauth_client,
            blocked_roles_list=blocked_roles_list,
            comment=comment,
            enabled=enabled,
            id=id,
            oauth_issue_refresh_tokens=oauth_issue_refresh_tokens,
            oauth_redirect_uri=oauth_redirect_uri,
            oauth_refresh_token_validity=oauth_refresh_token_validity,
            oauth_use_secondary_roles=oauth_use_secondary_roles,
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
        '''Generates CDKTF code for importing a OauthIntegrationForPartnerApplications resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OauthIntegrationForPartnerApplications to import.
        :param import_from_id: The id of the existing OauthIntegrationForPartnerApplications that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OauthIntegrationForPartnerApplications to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81af47a2500d658202bd9c9404a232456360e71adc146e5112b549b16105b51)
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

    @jsii.member(jsii_name="resetOauthIssueRefreshTokens")
    def reset_oauth_issue_refresh_tokens(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthIssueRefreshTokens", []))

    @jsii.member(jsii_name="resetOauthRedirectUri")
    def reset_oauth_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRedirectUri", []))

    @jsii.member(jsii_name="resetOauthRefreshTokenValidity")
    def reset_oauth_refresh_token_validity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRefreshTokenValidity", []))

    @jsii.member(jsii_name="resetOauthUseSecondaryRoles")
    def reset_oauth_use_secondary_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthUseSecondaryRoles", []))

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
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputList":
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="relatedParameters")
    def related_parameters(
        self,
    ) -> "OauthIntegrationForPartnerApplicationsRelatedParametersList":
        return typing.cast("OauthIntegrationForPartnerApplicationsRelatedParametersList", jsii.get(self, "relatedParameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "OauthIntegrationForPartnerApplicationsShowOutputList":
        return typing.cast("OauthIntegrationForPartnerApplicationsShowOutputList", jsii.get(self, "showOutput"))

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
    @jsii.member(jsii_name="oauthClientInput")
    def oauth_client_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthClientInput"))

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
    @jsii.member(jsii_name="blockedRolesList")
    def blocked_roles_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "blockedRolesList"))

    @blocked_roles_list.setter
    def blocked_roles_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13fa251d973e7827d404e72ce4a8cef5663634c8c0f85e20d3e7e430730f46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockedRolesList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef751e18850b5e5d06f566c2951a7c9c6484cd9ec51229cf6ec037f8f56c66d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67876a938d4da45a828c401b79a825ccd4e6f96ae767b6c66ff650bfbf151216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9074eb2914c5efd8ff67e54e90a735df0a7a943465849d1eb77ad77d9bd232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9526a658fc6af9bec629030f9a668c92b6a3f6bf596bacd94e7cc342c2a4bf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthClient")
    def oauth_client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClient"))

    @oauth_client.setter
    def oauth_client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866b9ad82ff1d1eeec2cfcfa4965351873fa0f52ed490f008827c9297e9219a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthClient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthIssueRefreshTokens")
    def oauth_issue_refresh_tokens(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthIssueRefreshTokens"))

    @oauth_issue_refresh_tokens.setter
    def oauth_issue_refresh_tokens(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e0d69086f272ad18015009dbfd02cf706b92f1ba67180da6dd16d0858e79f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthIssueRefreshTokens", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthRedirectUri")
    def oauth_redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthRedirectUri"))

    @oauth_redirect_uri.setter
    def oauth_redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce6284fe41768761f1a6b83d5afea64e1e153a46802a842e37981b57f425a8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthRedirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oauthRefreshTokenValidity"))

    @oauth_refresh_token_validity.setter
    def oauth_refresh_token_validity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec047033cc11605405f34f834568974fc5ad265036c4990bb086f474da9594a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthRefreshTokenValidity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthUseSecondaryRoles")
    def oauth_use_secondary_roles(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthUseSecondaryRoles"))

    @oauth_use_secondary_roles.setter
    def oauth_use_secondary_roles(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a43067957980df671cf37ff72cd273e4e992039e765ffe24c9ca855a4d0f0dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthUseSecondaryRoles", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsConfig",
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
        "oauth_client": "oauthClient",
        "blocked_roles_list": "blockedRolesList",
        "comment": "comment",
        "enabled": "enabled",
        "id": "id",
        "oauth_issue_refresh_tokens": "oauthIssueRefreshTokens",
        "oauth_redirect_uri": "oauthRedirectUri",
        "oauth_refresh_token_validity": "oauthRefreshTokenValidity",
        "oauth_use_secondary_roles": "oauthUseSecondaryRoles",
    },
)
class OauthIntegrationForPartnerApplicationsConfig(
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
        name: builtins.str,
        oauth_client: builtins.str,
        blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oauth_issue_refresh_tokens: typing.Optional[builtins.str] = None,
        oauth_redirect_uri: typing.Optional[builtins.str] = None,
        oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
        oauth_use_secondary_roles: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Specifies the name of the OAuth integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#name OauthIntegrationForPartnerApplications#name}
        :param oauth_client: Creates an OAuth interface between Snowflake and a partner application. Valid options are: ``LOOKER`` | ``TABLEAU_DESKTOP`` | ``TABLEAU_SERVER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_client OauthIntegrationForPartnerApplications#oauth_client}
        :param blocked_roles_list: A set of Snowflake roles that a user cannot explicitly consent to using after authenticating. By default, this list includes the ACCOUNTADMIN, ORGADMIN and SECURITYADMIN roles. To remove these privileged roles from the list, use the ALTER ACCOUNT command to set the OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST account parameter to FALSE. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#blocked_roles_list OauthIntegrationForPartnerApplications#blocked_roles_list}
        :param comment: Specifies a comment for the OAuth integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#comment OauthIntegrationForPartnerApplications#comment}
        :param enabled: Specifies whether this OAuth integration is enabled or disabled. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#enabled OauthIntegrationForPartnerApplications#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#id OauthIntegrationForPartnerApplications#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oauth_issue_refresh_tokens: Specifies whether to allow the client to exchange a refresh token for an access token when the current access token has expired. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_issue_refresh_tokens OauthIntegrationForPartnerApplications#oauth_issue_refresh_tokens}
        :param oauth_redirect_uri: Specifies the client URI. After a user is authenticated, the web browser is redirected to this URI. The field should be only set when OAUTH_CLIENT = LOOKER. In any other case the field should be left out empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_redirect_uri OauthIntegrationForPartnerApplications#oauth_redirect_uri}
        :param oauth_refresh_token_validity: Specifies how long refresh tokens should be valid (in seconds). OAUTH_ISSUE_REFRESH_TOKENS must be set to TRUE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_refresh_token_validity OauthIntegrationForPartnerApplications#oauth_refresh_token_validity}
        :param oauth_use_secondary_roles: Specifies whether default secondary roles set in the user properties are activated by default in the session being opened. Valid options are: ``IMPLICIT`` | ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_use_secondary_roles OauthIntegrationForPartnerApplications#oauth_use_secondary_roles}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af96a8af16bdee37916ca1cc8a5b1aa4655ebee55f4ca4ac854bd690e858da8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument oauth_client", value=oauth_client, expected_type=type_hints["oauth_client"])
            check_type(argname="argument blocked_roles_list", value=blocked_roles_list, expected_type=type_hints["blocked_roles_list"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument oauth_issue_refresh_tokens", value=oauth_issue_refresh_tokens, expected_type=type_hints["oauth_issue_refresh_tokens"])
            check_type(argname="argument oauth_redirect_uri", value=oauth_redirect_uri, expected_type=type_hints["oauth_redirect_uri"])
            check_type(argname="argument oauth_refresh_token_validity", value=oauth_refresh_token_validity, expected_type=type_hints["oauth_refresh_token_validity"])
            check_type(argname="argument oauth_use_secondary_roles", value=oauth_use_secondary_roles, expected_type=type_hints["oauth_use_secondary_roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "oauth_client": oauth_client,
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
        if oauth_issue_refresh_tokens is not None:
            self._values["oauth_issue_refresh_tokens"] = oauth_issue_refresh_tokens
        if oauth_redirect_uri is not None:
            self._values["oauth_redirect_uri"] = oauth_redirect_uri
        if oauth_refresh_token_validity is not None:
            self._values["oauth_refresh_token_validity"] = oauth_refresh_token_validity
        if oauth_use_secondary_roles is not None:
            self._values["oauth_use_secondary_roles"] = oauth_use_secondary_roles

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#name OauthIntegrationForPartnerApplications#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_client(self) -> builtins.str:
        '''Creates an OAuth interface between Snowflake and a partner application. Valid options are: ``LOOKER`` | ``TABLEAU_DESKTOP`` | ``TABLEAU_SERVER``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_client OauthIntegrationForPartnerApplications#oauth_client}
        '''
        result = self._values.get("oauth_client")
        assert result is not None, "Required property 'oauth_client' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blocked_roles_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of Snowflake roles that a user cannot explicitly consent to using after authenticating.

        By default, this list includes the ACCOUNTADMIN, ORGADMIN and SECURITYADMIN roles. To remove these privileged roles from the list, use the ALTER ACCOUNT command to set the OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST account parameter to FALSE. For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#blocked_roles_list OauthIntegrationForPartnerApplications#blocked_roles_list}
        '''
        result = self._values.get("blocked_roles_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the OAuth integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#comment OauthIntegrationForPartnerApplications#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.str]:
        '''Specifies whether this OAuth integration is enabled or disabled.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#enabled OauthIntegrationForPartnerApplications#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#id OauthIntegrationForPartnerApplications#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_issue_refresh_tokens(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to allow the client to exchange a refresh token for an access token when the current access token has expired.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_issue_refresh_tokens OauthIntegrationForPartnerApplications#oauth_issue_refresh_tokens}
        '''
        result = self._values.get("oauth_issue_refresh_tokens")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Specifies the client URI.

        After a user is authenticated, the web browser is redirected to this URI. The field should be only set when OAUTH_CLIENT = LOOKER. In any other case the field should be left out empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_redirect_uri OauthIntegrationForPartnerApplications#oauth_redirect_uri}
        '''
        result = self._values.get("oauth_redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        '''Specifies how long refresh tokens should be valid (in seconds). OAUTH_ISSUE_REFRESH_TOKENS must be set to TRUE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_refresh_token_validity OauthIntegrationForPartnerApplications#oauth_refresh_token_validity}
        '''
        result = self._values.get("oauth_refresh_token_validity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oauth_use_secondary_roles(self) -> typing.Optional[builtins.str]:
        '''Specifies whether default secondary roles set in the user properties are activated by default in the session being opened.

        Valid options are: ``IMPLICIT`` | ``NONE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/oauth_integration_for_partner_applications#oauth_use_secondary_roles OauthIntegrationForPartnerApplications#oauth_use_secondary_roles}
        '''
        result = self._values.get("oauth_use_secondary_roles")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fc34e2dcd082c1624fede08616fa2b60e2b1c34ebb7caffa38ccb68b8cff88c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7c000bde434e29f6f317e2d878363bb96d94dde731b00064c47e868185f958)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce47f629fa5f181ef8dd46a49c3cec99089b0ae60e0fda46e54031bff340e0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55cba9f536d88e5a1c8cd4a1246eac6f3f2036bc963ac8f5aa2f691ab2dc2a33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90c7737b6c669d22a3e7cf2c1235eece0ead4873b312a10a0fad7df835255e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da382a5771427eab5c85210c445c6bddec0c8e64430a20570614201dc9dbf910)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStruct]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0eae5cead7b147a64a096d20eb3d4ffc8cfb589ea917509798bad4c1d4032e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputComment",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputComment:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputComment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputCommentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputCommentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c2cc5b49c0bd31d0a52398df633b7c6ceec0c09b8c6358ab53917cf96054339)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputCommentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3456fdfae4dd3b7401f9cc926124bbfab83f466d9a97d4e5a3a5c355d017f6aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputCommentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510ddf8896234b200860da95be214157274c28135284891c5ec622e39a8ed00c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90e6ce3369bbb918de84a6d174657b3f0c3d1b1ab28308b1910e753866b909e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a731aadeded676d1ebf8ae92e9a3adee831a839129ef93aeaece4fa6fdb344a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputCommentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputCommentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f72c47a738068666e26dd508ecbfe67adc026fbab9b94c392692a240e68e159e)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputComment]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputComment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputComment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0269e330b87c89391bfaff134bd0e4fa3ef07e532a5d1da590bb7e4e7aee3f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputEnabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputEnabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputEnabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputEnabledList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputEnabledList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e63127af1433a93b032e37575f260947c8a1fbc48b305ae9a964f3ca125ff49b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputEnabledOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0d154c62d572b20127322f602fea7f6339933f2be3512f953e792d59de4f52)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputEnabledOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388f816943d408e174accc5cb1a4ad1e137557acc098bcf3702ad5a972a079da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd2afea0986b39df5148927219e4cbe33a9d7dcc839d53eff76091003e8c5faa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__895cb96d687686f3eceec1864dce5b4366fc55ff2933aa9263fc8b8824706a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputEnabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputEnabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__981ad79556f593d1e0ec4b5b8668a83835d63e30a0d92d56746f98b485fa20df)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputEnabled]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputEnabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputEnabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c77818d43ae5ab684a652356514f47412081a2d760edc133a954e0d1afa97d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64a5d5259f92c92750c863a9b562819717df165838138616822972f753d6cc07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e15a6e530c16d64dffdeded063fda30ea6963fe49c3cb3dfff25560d162f60)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10682f295e12f2b278675f968cc9167662342ae6d7532689aa3f6dcf2df2c9fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be96d0f9bc27dbd54fc2f9721b203d6e39a3aba326e8326abf981051a98b83d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df2ea50a5a0e76a298ee329416c071e4ffaeb9a34817e63ebe9417324a86f7fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c05ca8d5b53dc06c5557794338b853389e2a5fe1d456788d4a69196a7134605d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868791f97ac9c96d7b70f0e57850a398850df18eaba43520dbc72523400b877c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbeecb08419f7054483d05c457938b5ab987f0728b23f1477e25854ad06d0883)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62dd9ad6a5e94046aa8f897813b5fd29a8ebf9daba77e22d2c063fc8890b9aa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71f88047ad549ec30f68fe71e507f348d5f27bebea9b9635991714f3ad75f04f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98703969320cef59a37021950c76ae8d96cbc49e951bfda451be310b55f146da)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicy]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021e4a6aac1e9f1d5389f6aec5dc374ebec75c4da78120daf00397d4bb12448d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUri",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUri:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53517dcf659178b4bba788d507d5ec9ae16a042567c2720122c679ed8761f1a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442245935e31fec7e4875b035d8a2491d7050784d170b4abba002dc37ee1b9ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782c3450607a3294abd82c229a2f04c838f1f3c310e000baa3a5ec793ce8bde8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__102495806f05d1975dacdcbfebd070f645ef22064f5f38916aab00f5376b3249)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7076452d321410d4c06df41425d3e8ba4db86aeeb0b50dbe33a903a1c2e73867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c01e0058481376503d75a0626391bcfec8577f752e14b05d5ba6b8beb35665)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUri]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUri], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUri],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7044283225091acd8fb1dcdd34d3f4971d12a05aa543f88b1b7f388fd44a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f168897b6c85d4cac83697cc1e162f2a9292dc1be46449b9f40f5531fda2cb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060b6f81d6eed7364e35cc030fe0fa3549096f04c250c253cad0bd4616c134d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28deb51719454c5e64c4a49de6d8f871f54e48852abb6e07b2fa78dbe666e2fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbb85123349b69ec3bd6795c457c80d33a2eb3c893662c5cc9a20efc96729a25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f41bda9f6dff345afbd928182a6b5df7ac1e18dcc71f099e1bdf28444319648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af5a548e9868a476bacfa1ad45cbb6c3b123e236bfdba39939970a0b7587df16)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpoints]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097f1d3abfa1a75e09739ff6dd0c81046c843b7c2fb9b45720258648df600851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f5ca0a0ec0bb6586db577999152e3ecccf539b1f114dbc4cf20554d956ff165)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6dbbb726e6d2ad4c701a4827ce152e32d938fe849fe315eb763d0eb9fa387b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b4c820c18ddaa584bea8d37514c46fb211a2ca8d8de092977934fd0b15d3e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f52f065543c2fa39929c1d2bdb0aa59b2cfe1d53cfeb9ec2f4c91d2d3104011)
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
            type_hints = typing.get_type_hints(_typecheckingstub__699428f5ade72d8b11da4843ab080b8b9c399748e595bfac3f502eec86ed5005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7ae8369ea829352e4accc3ed27f5e715ae3f0d1a20d24d215c03d5a8ac9f33b)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpoints]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c39e1d490955313f0d45fd1a83bbcc250167157cd3d9fe6dd7d7b74fedd7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdcb55e99dc741a6d4ad02630dd4eef77508a7e372ace6ccd59f1ef6fbe70382)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ecf226ca2ccf85644d06e1d147b5ea11364ada396845a49a5bd0898a19c6045)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8854e2848f0f21ec489be31b77e6bc805ac715e2304243850817ae70ba8bb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f0aec8530cce5c5ac95395d1cbb86e9e67a0fe37e372ef4af279a0d9f89f3f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cca241ea10da1c4014e36a998423582e170afd0f6f245009254ed2be501eb47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b6f7959d4742f2a5aba2f5d2a57f056d9f140f716103725a144637b07dc3b19)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpoint]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce4f0a1d253ed04b9964656e00e27e0a1eae2d47e68e30c87d6b0c5eaca0a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientId",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85a48425f29098596015346677962cd553df701ca9d4b8db217fcba6fe12f651)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1747f18d66cd8dd87ac17011ccb040f51b2da441316c0604f587eb0284912304)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721fb50ac413a399694af0d4b8096c6b2e210bf701c6fc813d4c42e3f39b4f4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef35f25bc609f90086d73231892ad355ded618459092d90f3dae7043102841c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbf702ef52094727dd531a8889050cc340fc0cf738585af6d7b59c0430c7876f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e163ef05de240456ca1739e1146a6f378e6b34f44539995bf2ed3a2fc9e4665d)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientId]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c409be1868ad931cf72345926fc6513180a072a1766144a46b09a8b4a4b926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2Fp",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2Fp:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2Fp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93366d9bf6839da46bb1a2539b423175ef3bf82d5f5162c7e01a51e408ec9680)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12375e7541326f3f14bb5268b63879016833fab0f70e02eeb2ea6928ecb15da4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe5fe665bbe6a079fa9d679ada380a705375dfe99a2f6ffa2fc52c87e964ee4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2388b35909529cac8ae63803013f69d52429960d931217aec2e1ba74e89c2f27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39fa37c99ba363b5b6f32ecce10ba4165a551a99e8319f674439e48c0395e190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14695397c1791ba04a09394d5493fef7ca9bf1e8a93224e6d50e2869c08c28b1)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2Fp]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2Fp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2Fp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f7b5abc4b77d16a1e94b79d470d714ce150c3931ecad4a562349498a4b919d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFp",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFp:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a04a009f70a8993834b17df8ff95227122bae38c952c720b0035571d3ef3a028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edf36274ce6aded0d24723f89b7ff66ba17c85818a9abafb0630492580e0aa3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ef2bafc0fe86b1dd98af7cbf5b311725c7bb010b616a7e098dbbf99c62b28b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d93d77945f6dbeb697b01b480e31ccaa21fd336059019cc2bb2bdcdc75c9cc57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__622da69bebd8472c03e34976ce94f5c3b0c49ded9916c1acf501fbf760a43e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc79434c4a19f891bb6ef51132a4504c3e59790f1d3589a829984dcaa5488079)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFp]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9643a1b8628b29f8f53faf0955d3b93db4ba66150d796e8d82fa05237dff4a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientType",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c80cbf042a53730fe24f48ea4e8f86366f519901307d6b02693e1ff993ab9060)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3bddc632af41611aabcfa69ba4a842cd09cd7782761678920115b53f79a8ae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7651c6be0c27cc1901b09047f964bc14746dd860f400eca0fe7fcb4c0b4ba920)
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
            type_hints = typing.get_type_hints(_typecheckingstub__baa45c2793b17efd6ce7517e9916fe29fa7b7f8d8c20105ec935c25625227137)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebdfac215feabb5a00440d4e299075517c3b8f609e087df1b660f25c14877e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__540d417afa230e4b03345a4d94682a7eb5c40bd4efd623e94d785bd058687a16)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientType]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c937780dd6f0b268ebf5644ce582b1851dca0174b427dd5a92e1474cdf99a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkce",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkce:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2d93902f79a0597cfdb10fc5a0a1885a7fbaaa4277e0b2983983b6012bc94b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d65ac9fcd43089b95f094efc223d8b547649c8c6d33492361869f07592c8847)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f5deb43e8f5a4c26477c428742fb6e6b3f6b1171166ec089635fcf77d47438)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c9014dc2bffd945982fccf4aeace5bbe91345b6e0ef0cf429d90723ce63de0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba26270b685b7cdaee340dfa9276eccb1fd1b169c17df9993e0aefdfb22bd07b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__222aabe17d36cf0dd65ce05b5953efb5b73f8f77c8693b749adb4c7eadceb986)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkce]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d3d5ccc6310df688a739089c7cc71c44ac2a11a17cf1de90a681da79930b1e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokens",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokens:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokens(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71cbd9205f28e8b23e839ce1214b22a30bc9f32cc579cb4966948c978aabed2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0df67c9f0f9de8da1791e2ee0adf358a4de3b1570a285e6c79a897287713c11)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be370989e65ff2e99a2aea6a5b58d2b68a58f37b9235d6c7df394e09fcd3c887)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d76a29518b6d4bc40de32c9bd2aed85e2da06d0c5006b294da2eba312080b85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c1aca72da713eab334915656cf137d7f9e46e9cfd3fca27b5069af73d158a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a639a9aa6402f0ae1d099f466121a53d390409f18a3a641008f89be3264346a1)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokens]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokens], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokens],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae084406d74ed8705eebbc4452ed356404bf31cd369501a65be2da56fc2a14e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUri",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUri:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cbe4c1db849fb012779238142260dfd55bd420527c4ea44cf76a56d15a83873)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd075ae12d6fde7302f5767b41f09516ded0c47268d657921c702ec0f3e7eaf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e265b003b36a641c226225d91523f0ba64d7ec1e9b8acd6e3bc019067554e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee8fea16df6ddd9ef1f3f895a826240c95756a86922802f2a11f9042cf67f151)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcc7e51bbfad450b69fb830c059977340a0f7d30afa639cc5d92ca31c15def86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3b2a876dddbcd260bba64f5e933b18389efb2d621bce2a4cb6b324a977e5ff6)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUri]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUri], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUri],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b08cea5795421848e05a9d49e641ca3b89763f4472d7969d2014cb46081b7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a45b5f95bff0eec41f78bc660a2548979e0c2471ef7970b674efe28d1889d656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397d705c88073fb46d1e9e63bd6907569ae77aa934add24fee96f0b403e04f92)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61a8bbb448c3aec501cdba23061ad0de6bbd30e0df589b1a9d6dca4be639a29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aa0067d040178f15e5491f0241373114963ac3bcaae9962deb143206abe3517)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1a3359c436a301b3e09de40df3e5f730dca4b81759f762184c9d0a1a49b1214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35e2a2438da3c4aa38d6e6b10baf14e4395729081502fe4666802deb7ea1467c)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidity]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f47d573b67dcd0eb0542bf884c4c390d0154f22af095cae409eb96d846550fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d20c91c8eb0b9f51ddd8054199459449554a15f4f8cac20ad03472cc0fd60866)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a978acb076c99054f18630147ac06c0478248ce6f03c4572d7de89ad1fc2eb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759d7a6f6db0bc7968b8fb0b43df678d311844ff2a3087620315e17ed861102e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c8757c283d172ebfb92314edee06daca61e0d7db0d981eb780e7374b3e953ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2feed339254174fd9b4426f307f9cd23f3f44bec166e3becdaf14298ced54214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9ddb50b558cecea0f75a28503c76201f1ee43448722da4b961baeecebcd77a7)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpoint]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3cb7e95fd4620ba2c68f9b66c4e56020bfa06178fb9ffcfefece48fd10b89fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRoles",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRoles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__793595b19a458f42b61ceefdbe40e68e7d558bb266c960f3b2a39c1a3d1e2932)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaeecf2a4e6dfd961a23843445d587d8424d15320c89341e0857574b7489fa99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2eeef2bf8708a6f01663ef0145541bb63b04222ce84b2339123801e1df01b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c3f34ab34a81b1866e048ad628791d150322bd33580a13215dba52ec6b6ff5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64283a28a20048905b830f2c3ccb6a9130e6c9b9db74aa2d024baf071c5aebf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__552908269fd6a7209c13e505b2597df4d6efd2bb2c998eb126a6f4fbea1589d2)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRoles]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRoles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRoles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b886377e926f8d07b086ca45ee5565281cac3f5ba7359749cc2add92b4218e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b43bfa5850a5e77bc0cefae64c86b0c46d50444668ccb19a0b27a4a0110a7d07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="blockedRolesList")
    def blocked_roles_list(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructList, jsii.get(self, "blockedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputCommentList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputCommentList, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputEnabledList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputEnabledList, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyList, jsii.get(self, "networkPolicy"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedAuthorizationEndpoints")
    def oauth_allowed_authorization_endpoints(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsList, jsii.get(self, "oauthAllowedAuthorizationEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedTokenEndpoints")
    def oauth_allowed_token_endpoints(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsList, jsii.get(self, "oauthAllowedTokenEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowNonTlsRedirectUri")
    def oauth_allow_non_tls_redirect_uri(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriList, jsii.get(self, "oauthAllowNonTlsRedirectUri"))

    @builtins.property
    @jsii.member(jsii_name="oauthAuthorizationEndpoint")
    def oauth_authorization_endpoint(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointList, jsii.get(self, "oauthAuthorizationEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdList, jsii.get(self, "oauthClientId"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKey2Fp")
    def oauth_client_rsa_public_key2_fp(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpList, jsii.get(self, "oauthClientRsaPublicKey2Fp"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKeyFp")
    def oauth_client_rsa_public_key_fp(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpList, jsii.get(self, "oauthClientRsaPublicKeyFp"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientType")
    def oauth_client_type(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeList, jsii.get(self, "oauthClientType"))

    @builtins.property
    @jsii.member(jsii_name="oauthEnforcePkce")
    def oauth_enforce_pkce(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceList, jsii.get(self, "oauthEnforcePkce"))

    @builtins.property
    @jsii.member(jsii_name="oauthIssueRefreshTokens")
    def oauth_issue_refresh_tokens(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensList, jsii.get(self, "oauthIssueRefreshTokens"))

    @builtins.property
    @jsii.member(jsii_name="oauthRedirectUri")
    def oauth_redirect_uri(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriList, jsii.get(self, "oauthRedirectUri"))

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityList, jsii.get(self, "oauthRefreshTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpoint")
    def oauth_token_endpoint(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointList, jsii.get(self, "oauthTokenEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="oauthUseSecondaryRoles")
    def oauth_use_secondary_roles(
        self,
    ) -> OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesList:
        return typing.cast(OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesList, jsii.get(self, "oauthUseSecondaryRoles"))

    @builtins.property
    @jsii.member(jsii_name="preAuthorizedRolesList")
    def pre_authorized_roles_list(
        self,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructList":
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructList", jsii.get(self, "preAuthorizedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutput]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a465be6f60e31691e983af4458edf2c3336cd384a614c5b93899ac3b3e1c8b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f28e14795e75fcf76d00ad5d2dcebd1f18919bc3b9fa5dcb405151853bd482e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c497d700b360342a6330ce96a4ee348a018dd839b5ff374fadaf488c08bfea32)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae72580885b8998f0a8394b3535dccecb5b18436e0e7a71e5b15a1cadc39bca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5af98e5a5fc8d5fd8390d5a04ea60d5ba63d189907bd0da89fed8c17a1555386)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fdce346e096058f06800a8e37e5804c86600b1b7b50d9b4e40529746e9c5557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__264bcd54db9561ab692f8c1ce6068d3afc9557a5716dd1ca35edb4c3811dd949)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStruct]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b339f9f531ea840bc0eb178c9be31b263d2439f23cddfc4d25e9aaf1b94804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsRelatedParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsRelatedParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsRelatedParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsRelatedParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsRelatedParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3637b4ed54eeb5b62be7a5dd56ea02ad4da9c91bc30258ec2c1c2a2de533a9f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsRelatedParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0443da98141373cf703e8ebb1fc2bc82ef801341f2cd047c0404e6764a5bf1a0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsRelatedParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec5e1d092b7dfbe32beeb810c04a65cc48ea5a5e62ed1688139f05ae63ea681)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9657012d93e36393610d22649170ebcd0452a675e5422a3ab6d1282ca743d97e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a062b7f8f731acadcec1d93e398aeda50a13e580eec3ee6c4ba186d7d46b9fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad5aa9452c122d91b1ab62c161b2cae7e2eb20cc98d4c7f37aa2203755a605b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34df356420bfa44d66d642adc6c34220956d88f1d1cf8f564911d8e1c354bbab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01f8b08f23449d86d4b96bb853dbe61b1d32bd6f6a04b1f28e0f116e145f675)
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
            type_hints = typing.get_type_hints(_typecheckingstub__160b32c523f0eab00e18251015c6ceb7755696ce9d5c3a70fd209bbb369391ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87d81f944ee7e5e898c2ed62daba55d025bdf10b78dfb517d73d3b4d69ffad23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4c4586decdc04e4d82e5e8008036610704fb2d9fe76c8142c7a41eaadab24c0)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7ab9b2d5bc865955d0dd160fde5d3ba25dbc88395c4683e799edbf5c95bdce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsRelatedParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsRelatedParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7385b102c3659d61f99377eadb1b18e524df3b481534413356323742acef44c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="oauthAddPrivilegedRolesToBlockedList")
    def oauth_add_privileged_roles_to_blocked_list(
        self,
    ) -> OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList:
        return typing.cast(OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList, jsii.get(self, "oauthAddPrivilegedRolesToBlockedList"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsRelatedParameters]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsRelatedParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsRelatedParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0656f32cccd21ac4318948fa922e335e892874fcb94de9bb6a73db0b77d125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class OauthIntegrationForPartnerApplicationsShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthIntegrationForPartnerApplicationsShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthIntegrationForPartnerApplicationsShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af1c1a0aa27aa284497350fa758fb306fc49d69775ccae44af93ac054b41ad46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OauthIntegrationForPartnerApplicationsShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606eb4dcb412e50a196e032eded98756eb9a5909104af9bd037f2a08f1f7c21c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthIntegrationForPartnerApplicationsShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec5ad23dc68c414696ec706aaa4811ef1ca2fe6054cb357bc96dbfd6b908f01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12342c73ba60a9cf9b9381ebea7440df2a0aa7b1262a0b8b75c318b7ecd098f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9f913241e990515ccd814039ec14055ca0a8fa9bf0a360f873b529cbd437132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OauthIntegrationForPartnerApplicationsShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.oauthIntegrationForPartnerApplications.OauthIntegrationForPartnerApplicationsShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__100c8005f8f27137746da6f933ce91fb39492c18b9a5b8e23900821c48e12cbc)
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
    ) -> typing.Optional[OauthIntegrationForPartnerApplicationsShowOutput]:
        return typing.cast(typing.Optional[OauthIntegrationForPartnerApplicationsShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OauthIntegrationForPartnerApplicationsShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad67b4880ab227be3649e46e90ee95ff0b0d1408ae9bb8666be8f7569a3f9b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OauthIntegrationForPartnerApplications",
    "OauthIntegrationForPartnerApplicationsConfig",
    "OauthIntegrationForPartnerApplicationsDescribeOutput",
    "OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStruct",
    "OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStructOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputComment",
    "OauthIntegrationForPartnerApplicationsDescribeOutputCommentList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputCommentOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputEnabled",
    "OauthIntegrationForPartnerApplicationsDescribeOutputEnabledList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputEnabledOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicy",
    "OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicyOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUri",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpoints",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpoints",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpointsOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpoint",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpointOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientId",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientIdOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2Fp",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFp",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientType",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientTypeOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkce",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkceOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokens",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokensOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUri",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUriOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidity",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidityOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpoint",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpointOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRoles",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRolesOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputOutputReference",
    "OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStruct",
    "OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructList",
    "OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStructOutputReference",
    "OauthIntegrationForPartnerApplicationsRelatedParameters",
    "OauthIntegrationForPartnerApplicationsRelatedParametersList",
    "OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct",
    "OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructList",
    "OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStructOutputReference",
    "OauthIntegrationForPartnerApplicationsRelatedParametersOutputReference",
    "OauthIntegrationForPartnerApplicationsShowOutput",
    "OauthIntegrationForPartnerApplicationsShowOutputList",
    "OauthIntegrationForPartnerApplicationsShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__90df3a7593055b3842f7b95a64f325944cea311964db1611991b757d07b480ff(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    oauth_client: builtins.str,
    blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oauth_issue_refresh_tokens: typing.Optional[builtins.str] = None,
    oauth_redirect_uri: typing.Optional[builtins.str] = None,
    oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
    oauth_use_secondary_roles: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__e81af47a2500d658202bd9c9404a232456360e71adc146e5112b549b16105b51(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13fa251d973e7827d404e72ce4a8cef5663634c8c0f85e20d3e7e430730f46c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef751e18850b5e5d06f566c2951a7c9c6484cd9ec51229cf6ec037f8f56c66d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67876a938d4da45a828c401b79a825ccd4e6f96ae767b6c66ff650bfbf151216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9074eb2914c5efd8ff67e54e90a735df0a7a943465849d1eb77ad77d9bd232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9526a658fc6af9bec629030f9a668c92b6a3f6bf596bacd94e7cc342c2a4bf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866b9ad82ff1d1eeec2cfcfa4965351873fa0f52ed490f008827c9297e9219a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e0d69086f272ad18015009dbfd02cf706b92f1ba67180da6dd16d0858e79f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce6284fe41768761f1a6b83d5afea64e1e153a46802a842e37981b57f425a8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec047033cc11605405f34f834568974fc5ad265036c4990bb086f474da9594a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a43067957980df671cf37ff72cd273e4e992039e765ffe24c9ca855a4d0f0dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af96a8af16bdee37916ca1cc8a5b1aa4655ebee55f4ca4ac854bd690e858da8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    oauth_client: builtins.str,
    blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oauth_issue_refresh_tokens: typing.Optional[builtins.str] = None,
    oauth_redirect_uri: typing.Optional[builtins.str] = None,
    oauth_refresh_token_validity: typing.Optional[jsii.Number] = None,
    oauth_use_secondary_roles: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc34e2dcd082c1624fede08616fa2b60e2b1c34ebb7caffa38ccb68b8cff88c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7c000bde434e29f6f317e2d878363bb96d94dde731b00064c47e868185f958(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce47f629fa5f181ef8dd46a49c3cec99089b0ae60e0fda46e54031bff340e0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55cba9f536d88e5a1c8cd4a1246eac6f3f2036bc963ac8f5aa2f691ab2dc2a33(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c7737b6c669d22a3e7cf2c1235eece0ead4873b312a10a0fad7df835255e7d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da382a5771427eab5c85210c445c6bddec0c8e64430a20570614201dc9dbf910(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0eae5cead7b147a64a096d20eb3d4ffc8cfb589ea917509798bad4c1d4032e(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputBlockedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2cc5b49c0bd31d0a52398df633b7c6ceec0c09b8c6358ab53917cf96054339(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3456fdfae4dd3b7401f9cc926124bbfab83f466d9a97d4e5a3a5c355d017f6aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510ddf8896234b200860da95be214157274c28135284891c5ec622e39a8ed00c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e6ce3369bbb918de84a6d174657b3f0c3d1b1ab28308b1910e753866b909e2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a731aadeded676d1ebf8ae92e9a3adee831a839129ef93aeaece4fa6fdb344a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72c47a738068666e26dd508ecbfe67adc026fbab9b94c392692a240e68e159e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0269e330b87c89391bfaff134bd0e4fa3ef07e532a5d1da590bb7e4e7aee3f5(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputComment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63127af1433a93b032e37575f260947c8a1fbc48b305ae9a964f3ca125ff49b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0d154c62d572b20127322f602fea7f6339933f2be3512f953e792d59de4f52(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388f816943d408e174accc5cb1a4ad1e137557acc098bcf3702ad5a972a079da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2afea0986b39df5148927219e4cbe33a9d7dcc839d53eff76091003e8c5faa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895cb96d687686f3eceec1864dce5b4366fc55ff2933aa9263fc8b8824706a38(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981ad79556f593d1e0ec4b5b8668a83835d63e30a0d92d56746f98b485fa20df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c77818d43ae5ab684a652356514f47412081a2d760edc133a954e0d1afa97d4(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputEnabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a5d5259f92c92750c863a9b562819717df165838138616822972f753d6cc07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e15a6e530c16d64dffdeded063fda30ea6963fe49c3cb3dfff25560d162f60(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10682f295e12f2b278675f968cc9167662342ae6d7532689aa3f6dcf2df2c9fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be96d0f9bc27dbd54fc2f9721b203d6e39a3aba326e8326abf981051a98b83d6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2ea50a5a0e76a298ee329416c071e4ffaeb9a34817e63ebe9417324a86f7fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05ca8d5b53dc06c5557794338b853389e2a5fe1d456788d4a69196a7134605d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868791f97ac9c96d7b70f0e57850a398850df18eaba43520dbc72523400b877c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbeecb08419f7054483d05c457938b5ab987f0728b23f1477e25854ad06d0883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62dd9ad6a5e94046aa8f897813b5fd29a8ebf9daba77e22d2c063fc8890b9aa5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f88047ad549ec30f68fe71e507f348d5f27bebea9b9635991714f3ad75f04f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98703969320cef59a37021950c76ae8d96cbc49e951bfda451be310b55f146da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021e4a6aac1e9f1d5389f6aec5dc374ebec75c4da78120daf00397d4bb12448d(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputNetworkPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53517dcf659178b4bba788d507d5ec9ae16a042567c2720122c679ed8761f1a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442245935e31fec7e4875b035d8a2491d7050784d170b4abba002dc37ee1b9ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782c3450607a3294abd82c229a2f04c838f1f3c310e000baa3a5ec793ce8bde8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102495806f05d1975dacdcbfebd070f645ef22064f5f38916aab00f5376b3249(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7076452d321410d4c06df41425d3e8ba4db86aeeb0b50dbe33a903a1c2e73867(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c01e0058481376503d75a0626391bcfec8577f752e14b05d5ba6b8beb35665(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7044283225091acd8fb1dcdd34d3f4971d12a05aa543f88b1b7f388fd44a59(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowNonTlsRedirectUri],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f168897b6c85d4cac83697cc1e162f2a9292dc1be46449b9f40f5531fda2cb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060b6f81d6eed7364e35cc030fe0fa3549096f04c250c253cad0bd4616c134d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28deb51719454c5e64c4a49de6d8f871f54e48852abb6e07b2fa78dbe666e2fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb85123349b69ec3bd6795c457c80d33a2eb3c893662c5cc9a20efc96729a25(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f41bda9f6dff345afbd928182a6b5df7ac1e18dcc71f099e1bdf28444319648(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5a548e9868a476bacfa1ad45cbb6c3b123e236bfdba39939970a0b7587df16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097f1d3abfa1a75e09739ff6dd0c81046c843b7c2fb9b45720258648df600851(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedAuthorizationEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5ca0a0ec0bb6586db577999152e3ecccf539b1f114dbc4cf20554d956ff165(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6dbbb726e6d2ad4c701a4827ce152e32d938fe849fe315eb763d0eb9fa387b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b4c820c18ddaa584bea8d37514c46fb211a2ca8d8de092977934fd0b15d3e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f52f065543c2fa39929c1d2bdb0aa59b2cfe1d53cfeb9ec2f4c91d2d3104011(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699428f5ade72d8b11da4843ab080b8b9c399748e595bfac3f502eec86ed5005(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ae8369ea829352e4accc3ed27f5e715ae3f0d1a20d24d215c03d5a8ac9f33b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c39e1d490955313f0d45fd1a83bbcc250167157cd3d9fe6dd7d7b74fedd7cf(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAllowedTokenEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcb55e99dc741a6d4ad02630dd4eef77508a7e372ace6ccd59f1ef6fbe70382(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecf226ca2ccf85644d06e1d147b5ea11364ada396845a49a5bd0898a19c6045(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8854e2848f0f21ec489be31b77e6bc805ac715e2304243850817ae70ba8bb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0aec8530cce5c5ac95395d1cbb86e9e67a0fe37e372ef4af279a0d9f89f3f2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cca241ea10da1c4014e36a998423582e170afd0f6f245009254ed2be501eb47(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6f7959d4742f2a5aba2f5d2a57f056d9f140f716103725a144637b07dc3b19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce4f0a1d253ed04b9964656e00e27e0a1eae2d47e68e30c87d6b0c5eaca0a14(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthAuthorizationEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a48425f29098596015346677962cd553df701ca9d4b8db217fcba6fe12f651(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1747f18d66cd8dd87ac17011ccb040f51b2da441316c0604f587eb0284912304(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721fb50ac413a399694af0d4b8096c6b2e210bf701c6fc813d4c42e3f39b4f4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef35f25bc609f90086d73231892ad355ded618459092d90f3dae7043102841c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf702ef52094727dd531a8889050cc340fc0cf738585af6d7b59c0430c7876f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e163ef05de240456ca1739e1146a6f378e6b34f44539995bf2ed3a2fc9e4665d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c409be1868ad931cf72345926fc6513180a072a1766144a46b09a8b4a4b926(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93366d9bf6839da46bb1a2539b423175ef3bf82d5f5162c7e01a51e408ec9680(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12375e7541326f3f14bb5268b63879016833fab0f70e02eeb2ea6928ecb15da4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe5fe665bbe6a079fa9d679ada380a705375dfe99a2f6ffa2fc52c87e964ee4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2388b35909529cac8ae63803013f69d52429960d931217aec2e1ba74e89c2f27(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fa37c99ba363b5b6f32ecce10ba4165a551a99e8319f674439e48c0395e190(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14695397c1791ba04a09394d5493fef7ca9bf1e8a93224e6d50e2869c08c28b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f7b5abc4b77d16a1e94b79d470d714ce150c3931ecad4a562349498a4b919d(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKey2Fp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04a009f70a8993834b17df8ff95227122bae38c952c720b0035571d3ef3a028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edf36274ce6aded0d24723f89b7ff66ba17c85818a9abafb0630492580e0aa3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ef2bafc0fe86b1dd98af7cbf5b311725c7bb010b616a7e098dbbf99c62b28b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93d77945f6dbeb697b01b480e31ccaa21fd336059019cc2bb2bdcdc75c9cc57(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622da69bebd8472c03e34976ce94f5c3b0c49ded9916c1acf501fbf760a43e12(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc79434c4a19f891bb6ef51132a4504c3e59790f1d3589a829984dcaa5488079(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9643a1b8628b29f8f53faf0955d3b93db4ba66150d796e8d82fa05237dff4a0a(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientRsaPublicKeyFp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80cbf042a53730fe24f48ea4e8f86366f519901307d6b02693e1ff993ab9060(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3bddc632af41611aabcfa69ba4a842cd09cd7782761678920115b53f79a8ae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7651c6be0c27cc1901b09047f964bc14746dd860f400eca0fe7fcb4c0b4ba920(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa45c2793b17efd6ce7517e9916fe29fa7b7f8d8c20105ec935c25625227137(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdfac215feabb5a00440d4e299075517c3b8f609e087df1b660f25c14877e50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540d417afa230e4b03345a4d94682a7eb5c40bd4efd623e94d785bd058687a16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c937780dd6f0b268ebf5644ce582b1851dca0174b427dd5a92e1474cdf99a5(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthClientType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d93902f79a0597cfdb10fc5a0a1885a7fbaaa4277e0b2983983b6012bc94b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d65ac9fcd43089b95f094efc223d8b547649c8c6d33492361869f07592c8847(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f5deb43e8f5a4c26477c428742fb6e6b3f6b1171166ec089635fcf77d47438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9014dc2bffd945982fccf4aeace5bbe91345b6e0ef0cf429d90723ce63de0c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba26270b685b7cdaee340dfa9276eccb1fd1b169c17df9993e0aefdfb22bd07b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222aabe17d36cf0dd65ce05b5953efb5b73f8f77c8693b749adb4c7eadceb986(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3d5ccc6310df688a739089c7cc71c44ac2a11a17cf1de90a681da79930b1e7(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthEnforcePkce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cbd9205f28e8b23e839ce1214b22a30bc9f32cc579cb4966948c978aabed2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0df67c9f0f9de8da1791e2ee0adf358a4de3b1570a285e6c79a897287713c11(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be370989e65ff2e99a2aea6a5b58d2b68a58f37b9235d6c7df394e09fcd3c887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d76a29518b6d4bc40de32c9bd2aed85e2da06d0c5006b294da2eba312080b85(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1aca72da713eab334915656cf137d7f9e46e9cfd3fca27b5069af73d158a02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a639a9aa6402f0ae1d099f466121a53d390409f18a3a641008f89be3264346a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae084406d74ed8705eebbc4452ed356404bf31cd369501a65be2da56fc2a14e(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthIssueRefreshTokens],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbe4c1db849fb012779238142260dfd55bd420527c4ea44cf76a56d15a83873(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd075ae12d6fde7302f5767b41f09516ded0c47268d657921c702ec0f3e7eaf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e265b003b36a641c226225d91523f0ba64d7ec1e9b8acd6e3bc019067554e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8fea16df6ddd9ef1f3f895a826240c95756a86922802f2a11f9042cf67f151(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc7e51bbfad450b69fb830c059977340a0f7d30afa639cc5d92ca31c15def86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b2a876dddbcd260bba64f5e933b18389efb2d621bce2a4cb6b324a977e5ff6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b08cea5795421848e05a9d49e641ca3b89763f4472d7969d2014cb46081b7e(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthRedirectUri],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45b5f95bff0eec41f78bc660a2548979e0c2471ef7970b674efe28d1889d656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397d705c88073fb46d1e9e63bd6907569ae77aa934add24fee96f0b403e04f92(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61a8bbb448c3aec501cdba23061ad0de6bbd30e0df589b1a9d6dca4be639a29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa0067d040178f15e5491f0241373114963ac3bcaae9962deb143206abe3517(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a3359c436a301b3e09de40df3e5f730dca4b81759f762184c9d0a1a49b1214(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e2a2438da3c4aa38d6e6b10baf14e4395729081502fe4666802deb7ea1467c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f47d573b67dcd0eb0542bf884c4c390d0154f22af095cae409eb96d846550fe(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthRefreshTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20c91c8eb0b9f51ddd8054199459449554a15f4f8cac20ad03472cc0fd60866(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a978acb076c99054f18630147ac06c0478248ce6f03c4572d7de89ad1fc2eb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759d7a6f6db0bc7968b8fb0b43df678d311844ff2a3087620315e17ed861102e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8757c283d172ebfb92314edee06daca61e0d7db0d981eb780e7374b3e953ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2feed339254174fd9b4426f307f9cd23f3f44bec166e3becdaf14298ced54214(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ddb50b558cecea0f75a28503c76201f1ee43448722da4b961baeecebcd77a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3cb7e95fd4620ba2c68f9b66c4e56020bfa06178fb9ffcfefece48fd10b89fb(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthTokenEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793595b19a458f42b61ceefdbe40e68e7d558bb266c960f3b2a39c1a3d1e2932(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaeecf2a4e6dfd961a23843445d587d8424d15320c89341e0857574b7489fa99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2eeef2bf8708a6f01663ef0145541bb63b04222ce84b2339123801e1df01b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3f34ab34a81b1866e048ad628791d150322bd33580a13215dba52ec6b6ff5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64283a28a20048905b830f2c3ccb6a9130e6c9b9db74aa2d024baf071c5aebf7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552908269fd6a7209c13e505b2597df4d6efd2bb2c998eb126a6f4fbea1589d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b886377e926f8d07b086ca45ee5565281cac3f5ba7359749cc2add92b4218e(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputOauthUseSecondaryRoles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43bfa5850a5e77bc0cefae64c86b0c46d50444668ccb19a0b27a4a0110a7d07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a465be6f60e31691e983af4458edf2c3336cd384a614c5b93899ac3b3e1c8b6(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28e14795e75fcf76d00ad5d2dcebd1f18919bc3b9fa5dcb405151853bd482e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c497d700b360342a6330ce96a4ee348a018dd839b5ff374fadaf488c08bfea32(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae72580885b8998f0a8394b3535dccecb5b18436e0e7a71e5b15a1cadc39bca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af98e5a5fc8d5fd8390d5a04ea60d5ba63d189907bd0da89fed8c17a1555386(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdce346e096058f06800a8e37e5804c86600b1b7b50d9b4e40529746e9c5557(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264bcd54db9561ab692f8c1ce6068d3afc9557a5716dd1ca35edb4c3811dd949(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b339f9f531ea840bc0eb178c9be31b263d2439f23cddfc4d25e9aaf1b94804(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsDescribeOutputPreAuthorizedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3637b4ed54eeb5b62be7a5dd56ea02ad4da9c91bc30258ec2c1c2a2de533a9f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0443da98141373cf703e8ebb1fc2bc82ef801341f2cd047c0404e6764a5bf1a0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec5e1d092b7dfbe32beeb810c04a65cc48ea5a5e62ed1688139f05ae63ea681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9657012d93e36393610d22649170ebcd0452a675e5422a3ab6d1282ca743d97e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a062b7f8f731acadcec1d93e398aeda50a13e580eec3ee6c4ba186d7d46b9fe3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5aa9452c122d91b1ab62c161b2cae7e2eb20cc98d4c7f37aa2203755a605b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34df356420bfa44d66d642adc6c34220956d88f1d1cf8f564911d8e1c354bbab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01f8b08f23449d86d4b96bb853dbe61b1d32bd6f6a04b1f28e0f116e145f675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160b32c523f0eab00e18251015c6ceb7755696ce9d5c3a70fd209bbb369391ef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d81f944ee7e5e898c2ed62daba55d025bdf10b78dfb517d73d3b4d69ffad23(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c4586decdc04e4d82e5e8008036610704fb2d9fe76c8142c7a41eaadab24c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7ab9b2d5bc865955d0dd160fde5d3ba25dbc88395c4683e799edbf5c95bdce(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsRelatedParametersOauthAddPrivilegedRolesToBlockedListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7385b102c3659d61f99377eadb1b18e524df3b481534413356323742acef44c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0656f32cccd21ac4318948fa922e335e892874fcb94de9bb6a73db0b77d125(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsRelatedParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1c1a0aa27aa284497350fa758fb306fc49d69775ccae44af93ac054b41ad46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606eb4dcb412e50a196e032eded98756eb9a5909104af9bd037f2a08f1f7c21c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec5ad23dc68c414696ec706aaa4811ef1ca2fe6054cb357bc96dbfd6b908f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12342c73ba60a9cf9b9381ebea7440df2a0aa7b1262a0b8b75c318b7ecd098f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f913241e990515ccd814039ec14055ca0a8fa9bf0a360f873b529cbd437132(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100c8005f8f27137746da6f933ce91fb39492c18b9a5b8e23900821c48e12cbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad67b4880ab227be3649e46e90ee95ff0b0d1408ae9bb8666be8f7569a3f9b0(
    value: typing.Optional[OauthIntegrationForPartnerApplicationsShowOutput],
) -> None:
    """Type checking stubs"""
    pass
