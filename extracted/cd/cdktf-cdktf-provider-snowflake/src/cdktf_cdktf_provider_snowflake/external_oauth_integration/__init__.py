r'''
# `snowflake_external_oauth_integration`

Refer to the Terraform Registry for docs: [`snowflake_external_oauth_integration`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration).
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


class ExternalOauthIntegration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegration",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration snowflake_external_oauth_integration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        external_oauth_issuer: builtins.str,
        external_oauth_snowflake_user_mapping_attribute: builtins.str,
        external_oauth_token_user_mapping_claim: typing.Sequence[builtins.str],
        external_oauth_type: builtins.str,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        external_oauth_allowed_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_oauth_any_role_mode: typing.Optional[builtins.str] = None,
        external_oauth_audience_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_oauth_blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_oauth_jws_keys_url: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_oauth_rsa_public_key: typing.Optional[builtins.str] = None,
        external_oauth_rsa_public_key2: typing.Optional[builtins.str] = None,
        external_oauth_scope_delimiter: typing.Optional[builtins.str] = None,
        external_oauth_scope_mapping_attribute: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration snowflake_external_oauth_integration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled: Specifies whether to initiate operation of the integration or suspend it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#enabled ExternalOauthIntegration#enabled}
        :param external_oauth_issuer: Specifies the URL to define the OAuth 2.0 authorization server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_issuer ExternalOauthIntegration#external_oauth_issuer}
        :param external_oauth_snowflake_user_mapping_attribute: Indicates which Snowflake user record attribute should be used to map the access token to a Snowflake user record. Valid values are (case-insensitive): ``LOGIN_NAME`` | ``EMAIL_ADDRESS``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_snowflake_user_mapping_attribute ExternalOauthIntegration#external_oauth_snowflake_user_mapping_attribute}
        :param external_oauth_token_user_mapping_claim: Specifies the access token claim or claims that can be used to map the access token to a Snowflake user record. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_token_user_mapping_claim ExternalOauthIntegration#external_oauth_token_user_mapping_claim}
        :param external_oauth_type: Specifies the OAuth 2.0 authorization server to be Okta, Microsoft Azure AD, Ping Identity PingFederate, or a Custom OAuth 2.0 authorization server. Valid values are (case-insensitive): ``OKTA`` | ``AZURE`` | ``PING_FEDERATE`` | ``CUSTOM``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_type ExternalOauthIntegration#external_oauth_type}
        :param name: Specifies the name of the External Oath integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#name ExternalOauthIntegration#name}
        :param comment: Specifies a comment for the OAuth integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#comment ExternalOauthIntegration#comment}
        :param external_oauth_allowed_roles_list: Specifies the list of roles that the client can set as the primary role. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_allowed_roles_list ExternalOauthIntegration#external_oauth_allowed_roles_list}
        :param external_oauth_any_role_mode: Specifies whether the OAuth client or user can use a role that is not defined in the OAuth access token. Valid values are (case-insensitive): ``DISABLE`` | ``ENABLE`` | ``ENABLE_FOR_PRIVILEGE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_any_role_mode ExternalOauthIntegration#external_oauth_any_role_mode}
        :param external_oauth_audience_list: Specifies additional values that can be used for the access token's audience validation on top of using the Customer's Snowflake Account URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_audience_list ExternalOauthIntegration#external_oauth_audience_list}
        :param external_oauth_blocked_roles_list: Specifies the list of roles that a client cannot set as the primary role. By default, this list includes the ACCOUNTADMIN, ORGADMIN and SECURITYADMIN roles. To remove these privileged roles from the list, use the ALTER ACCOUNT command to set the EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST account parameter to FALSE. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_blocked_roles_list ExternalOauthIntegration#external_oauth_blocked_roles_list}
        :param external_oauth_jws_keys_url: Specifies the endpoint or a list of endpoints from which to download public keys or certificates to validate an External OAuth access token. The maximum number of URLs that can be specified in the list is 3. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_jws_keys_url ExternalOauthIntegration#external_oauth_jws_keys_url}
        :param external_oauth_rsa_public_key: Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_rsa_public_key ExternalOauthIntegration#external_oauth_rsa_public_key}
        :param external_oauth_rsa_public_key2: Specifies a second RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. Used for key rotation. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_rsa_public_key_2 ExternalOauthIntegration#external_oauth_rsa_public_key_2}
        :param external_oauth_scope_delimiter: Specifies the scope delimiter in the authorization token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_scope_delimiter ExternalOauthIntegration#external_oauth_scope_delimiter}
        :param external_oauth_scope_mapping_attribute: Specifies the access token claim to map the access token to an account role. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_scope_mapping_attribute ExternalOauthIntegration#external_oauth_scope_mapping_attribute}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#id ExternalOauthIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35dfabda2663a4d9bee41d19b6803bf06a1bf44ff04ed45d617bdefca8249594)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ExternalOauthIntegrationConfig(
            enabled=enabled,
            external_oauth_issuer=external_oauth_issuer,
            external_oauth_snowflake_user_mapping_attribute=external_oauth_snowflake_user_mapping_attribute,
            external_oauth_token_user_mapping_claim=external_oauth_token_user_mapping_claim,
            external_oauth_type=external_oauth_type,
            name=name,
            comment=comment,
            external_oauth_allowed_roles_list=external_oauth_allowed_roles_list,
            external_oauth_any_role_mode=external_oauth_any_role_mode,
            external_oauth_audience_list=external_oauth_audience_list,
            external_oauth_blocked_roles_list=external_oauth_blocked_roles_list,
            external_oauth_jws_keys_url=external_oauth_jws_keys_url,
            external_oauth_rsa_public_key=external_oauth_rsa_public_key,
            external_oauth_rsa_public_key2=external_oauth_rsa_public_key2,
            external_oauth_scope_delimiter=external_oauth_scope_delimiter,
            external_oauth_scope_mapping_attribute=external_oauth_scope_mapping_attribute,
            id=id,
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
        '''Generates CDKTF code for importing a ExternalOauthIntegration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ExternalOauthIntegration to import.
        :param import_from_id: The id of the existing ExternalOauthIntegration that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ExternalOauthIntegration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba49d5af8dd32aa32671a62f79d536bad66c4da7099ba0845b821025745ddb7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetExternalOauthAllowedRolesList")
    def reset_external_oauth_allowed_roles_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthAllowedRolesList", []))

    @jsii.member(jsii_name="resetExternalOauthAnyRoleMode")
    def reset_external_oauth_any_role_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthAnyRoleMode", []))

    @jsii.member(jsii_name="resetExternalOauthAudienceList")
    def reset_external_oauth_audience_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthAudienceList", []))

    @jsii.member(jsii_name="resetExternalOauthBlockedRolesList")
    def reset_external_oauth_blocked_roles_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthBlockedRolesList", []))

    @jsii.member(jsii_name="resetExternalOauthJwsKeysUrl")
    def reset_external_oauth_jws_keys_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthJwsKeysUrl", []))

    @jsii.member(jsii_name="resetExternalOauthRsaPublicKey")
    def reset_external_oauth_rsa_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthRsaPublicKey", []))

    @jsii.member(jsii_name="resetExternalOauthRsaPublicKey2")
    def reset_external_oauth_rsa_public_key2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthRsaPublicKey2", []))

    @jsii.member(jsii_name="resetExternalOauthScopeDelimiter")
    def reset_external_oauth_scope_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthScopeDelimiter", []))

    @jsii.member(jsii_name="resetExternalOauthScopeMappingAttribute")
    def reset_external_oauth_scope_mapping_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthScopeMappingAttribute", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    def describe_output(self) -> "ExternalOauthIntegrationDescribeOutputList":
        return typing.cast("ExternalOauthIntegrationDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="relatedParameters")
    def related_parameters(self) -> "ExternalOauthIntegrationRelatedParametersList":
        return typing.cast("ExternalOauthIntegrationRelatedParametersList", jsii.get(self, "relatedParameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "ExternalOauthIntegrationShowOutputList":
        return typing.cast("ExternalOauthIntegrationShowOutputList", jsii.get(self, "showOutput"))

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
    @jsii.member(jsii_name="externalOauthAllowedRolesListInput")
    def external_oauth_allowed_roles_list_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalOauthAllowedRolesListInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthAnyRoleModeInput")
    def external_oauth_any_role_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalOauthAnyRoleModeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthAudienceListInput")
    def external_oauth_audience_list_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalOauthAudienceListInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthBlockedRolesListInput")
    def external_oauth_blocked_roles_list_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalOauthBlockedRolesListInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthIssuerInput")
    def external_oauth_issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalOauthIssuerInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthJwsKeysUrlInput")
    def external_oauth_jws_keys_url_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalOauthJwsKeysUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthRsaPublicKey2Input")
    def external_oauth_rsa_public_key2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalOauthRsaPublicKey2Input"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthRsaPublicKeyInput")
    def external_oauth_rsa_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalOauthRsaPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthScopeDelimiterInput")
    def external_oauth_scope_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalOauthScopeDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthScopeMappingAttributeInput")
    def external_oauth_scope_mapping_attribute_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalOauthScopeMappingAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthSnowflakeUserMappingAttributeInput")
    def external_oauth_snowflake_user_mapping_attribute_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalOauthSnowflakeUserMappingAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthTokenUserMappingClaimInput")
    def external_oauth_token_user_mapping_claim_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalOauthTokenUserMappingClaimInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthTypeInput")
    def external_oauth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalOauthTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac030933dd792662e17628398b3465cb3b686a90faffd2d872c76b9626c1f18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de0fdf1abb35924f96b3e2e06ce9f694730e4ac6ceff1cb9d305511acb5af576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthAllowedRolesList")
    def external_oauth_allowed_roles_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalOauthAllowedRolesList"))

    @external_oauth_allowed_roles_list.setter
    def external_oauth_allowed_roles_list(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e406d246d8a808516861e02fca6fd3ee0411b34cf5ba278b6ff42b6c642934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthAllowedRolesList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthAnyRoleMode")
    def external_oauth_any_role_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalOauthAnyRoleMode"))

    @external_oauth_any_role_mode.setter
    def external_oauth_any_role_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc91b850d1c88bf2576c219c79bc388426afc5128c0c36c7beb40d1fd5d61a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthAnyRoleMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthAudienceList")
    def external_oauth_audience_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalOauthAudienceList"))

    @external_oauth_audience_list.setter
    def external_oauth_audience_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9ccd124663370c0abe76d9443fceb34d4c5bca657965a07d7b213d5a710c2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthAudienceList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthBlockedRolesList")
    def external_oauth_blocked_roles_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalOauthBlockedRolesList"))

    @external_oauth_blocked_roles_list.setter
    def external_oauth_blocked_roles_list(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1683e8f055b2384f31039ae60a649287f3b0b93e6c3650b8e596d6ab76f00d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthBlockedRolesList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthIssuer")
    def external_oauth_issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalOauthIssuer"))

    @external_oauth_issuer.setter
    def external_oauth_issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5c6b9df1c8e4dcbc6710ba3427a6fd5686d84492118211345f150554b42f02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthIssuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthJwsKeysUrl")
    def external_oauth_jws_keys_url(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalOauthJwsKeysUrl"))

    @external_oauth_jws_keys_url.setter
    def external_oauth_jws_keys_url(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8356de93e2811cbff76f080d066e6ade944f15cc8c84e5d0938ecda33a846b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthJwsKeysUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthRsaPublicKey")
    def external_oauth_rsa_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalOauthRsaPublicKey"))

    @external_oauth_rsa_public_key.setter
    def external_oauth_rsa_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a031be7d3c472f16017762f777adcb8854104aaebfdf2410e8817d125f6a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthRsaPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthRsaPublicKey2")
    def external_oauth_rsa_public_key2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalOauthRsaPublicKey2"))

    @external_oauth_rsa_public_key2.setter
    def external_oauth_rsa_public_key2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd72c4d51b5846d37f9d3cfcfc7d51bd4d73ed4df55e5299c6ee2d0224e9dc19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthRsaPublicKey2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthScopeDelimiter")
    def external_oauth_scope_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalOauthScopeDelimiter"))

    @external_oauth_scope_delimiter.setter
    def external_oauth_scope_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac958fb64fd155600720fcf04e8ec92fe957d988c1aa5d48687ddf533a162f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthScopeDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthScopeMappingAttribute")
    def external_oauth_scope_mapping_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalOauthScopeMappingAttribute"))

    @external_oauth_scope_mapping_attribute.setter
    def external_oauth_scope_mapping_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce86aa42efb12c7b9176d213dc7d9907038cad34c134daaca4eca85e05cfa55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthScopeMappingAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthSnowflakeUserMappingAttribute")
    def external_oauth_snowflake_user_mapping_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalOauthSnowflakeUserMappingAttribute"))

    @external_oauth_snowflake_user_mapping_attribute.setter
    def external_oauth_snowflake_user_mapping_attribute(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b38cb6e29bf0ced54672acca1052ddbb7ee1a3bb915126d50cf7021f321891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthSnowflakeUserMappingAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthTokenUserMappingClaim")
    def external_oauth_token_user_mapping_claim(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalOauthTokenUserMappingClaim"))

    @external_oauth_token_user_mapping_claim.setter
    def external_oauth_token_user_mapping_claim(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd598442b95f12e2a5ea0250bbe0072dce1b0a592ef9ceeaae4f73f436072d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthTokenUserMappingClaim", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthType")
    def external_oauth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalOauthType"))

    @external_oauth_type.setter
    def external_oauth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1df96291435c387207c764d99b3268ea200ecac5ed2fd9b6b075a9c64b8a212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808cdddc1a5523ee6b86977e8d07f33273cadd92c00a1bf54d1f79e7647aa75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5915b3b17c1324f7c13b61f21ddc02c9045e2845be02dcebbae2631b6b34dc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationConfig",
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
        "external_oauth_issuer": "externalOauthIssuer",
        "external_oauth_snowflake_user_mapping_attribute": "externalOauthSnowflakeUserMappingAttribute",
        "external_oauth_token_user_mapping_claim": "externalOauthTokenUserMappingClaim",
        "external_oauth_type": "externalOauthType",
        "name": "name",
        "comment": "comment",
        "external_oauth_allowed_roles_list": "externalOauthAllowedRolesList",
        "external_oauth_any_role_mode": "externalOauthAnyRoleMode",
        "external_oauth_audience_list": "externalOauthAudienceList",
        "external_oauth_blocked_roles_list": "externalOauthBlockedRolesList",
        "external_oauth_jws_keys_url": "externalOauthJwsKeysUrl",
        "external_oauth_rsa_public_key": "externalOauthRsaPublicKey",
        "external_oauth_rsa_public_key2": "externalOauthRsaPublicKey2",
        "external_oauth_scope_delimiter": "externalOauthScopeDelimiter",
        "external_oauth_scope_mapping_attribute": "externalOauthScopeMappingAttribute",
        "id": "id",
    },
)
class ExternalOauthIntegrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        external_oauth_issuer: builtins.str,
        external_oauth_snowflake_user_mapping_attribute: builtins.str,
        external_oauth_token_user_mapping_claim: typing.Sequence[builtins.str],
        external_oauth_type: builtins.str,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        external_oauth_allowed_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_oauth_any_role_mode: typing.Optional[builtins.str] = None,
        external_oauth_audience_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_oauth_blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_oauth_jws_keys_url: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_oauth_rsa_public_key: typing.Optional[builtins.str] = None,
        external_oauth_rsa_public_key2: typing.Optional[builtins.str] = None,
        external_oauth_scope_delimiter: typing.Optional[builtins.str] = None,
        external_oauth_scope_mapping_attribute: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enabled: Specifies whether to initiate operation of the integration or suspend it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#enabled ExternalOauthIntegration#enabled}
        :param external_oauth_issuer: Specifies the URL to define the OAuth 2.0 authorization server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_issuer ExternalOauthIntegration#external_oauth_issuer}
        :param external_oauth_snowflake_user_mapping_attribute: Indicates which Snowflake user record attribute should be used to map the access token to a Snowflake user record. Valid values are (case-insensitive): ``LOGIN_NAME`` | ``EMAIL_ADDRESS``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_snowflake_user_mapping_attribute ExternalOauthIntegration#external_oauth_snowflake_user_mapping_attribute}
        :param external_oauth_token_user_mapping_claim: Specifies the access token claim or claims that can be used to map the access token to a Snowflake user record. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_token_user_mapping_claim ExternalOauthIntegration#external_oauth_token_user_mapping_claim}
        :param external_oauth_type: Specifies the OAuth 2.0 authorization server to be Okta, Microsoft Azure AD, Ping Identity PingFederate, or a Custom OAuth 2.0 authorization server. Valid values are (case-insensitive): ``OKTA`` | ``AZURE`` | ``PING_FEDERATE`` | ``CUSTOM``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_type ExternalOauthIntegration#external_oauth_type}
        :param name: Specifies the name of the External Oath integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#name ExternalOauthIntegration#name}
        :param comment: Specifies a comment for the OAuth integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#comment ExternalOauthIntegration#comment}
        :param external_oauth_allowed_roles_list: Specifies the list of roles that the client can set as the primary role. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_allowed_roles_list ExternalOauthIntegration#external_oauth_allowed_roles_list}
        :param external_oauth_any_role_mode: Specifies whether the OAuth client or user can use a role that is not defined in the OAuth access token. Valid values are (case-insensitive): ``DISABLE`` | ``ENABLE`` | ``ENABLE_FOR_PRIVILEGE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_any_role_mode ExternalOauthIntegration#external_oauth_any_role_mode}
        :param external_oauth_audience_list: Specifies additional values that can be used for the access token's audience validation on top of using the Customer's Snowflake Account URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_audience_list ExternalOauthIntegration#external_oauth_audience_list}
        :param external_oauth_blocked_roles_list: Specifies the list of roles that a client cannot set as the primary role. By default, this list includes the ACCOUNTADMIN, ORGADMIN and SECURITYADMIN roles. To remove these privileged roles from the list, use the ALTER ACCOUNT command to set the EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST account parameter to FALSE. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_blocked_roles_list ExternalOauthIntegration#external_oauth_blocked_roles_list}
        :param external_oauth_jws_keys_url: Specifies the endpoint or a list of endpoints from which to download public keys or certificates to validate an External OAuth access token. The maximum number of URLs that can be specified in the list is 3. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_jws_keys_url ExternalOauthIntegration#external_oauth_jws_keys_url}
        :param external_oauth_rsa_public_key: Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_rsa_public_key ExternalOauthIntegration#external_oauth_rsa_public_key}
        :param external_oauth_rsa_public_key2: Specifies a second RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. Used for key rotation. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_rsa_public_key_2 ExternalOauthIntegration#external_oauth_rsa_public_key_2}
        :param external_oauth_scope_delimiter: Specifies the scope delimiter in the authorization token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_scope_delimiter ExternalOauthIntegration#external_oauth_scope_delimiter}
        :param external_oauth_scope_mapping_attribute: Specifies the access token claim to map the access token to an account role. If removed from the config, the resource is recreated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_scope_mapping_attribute ExternalOauthIntegration#external_oauth_scope_mapping_attribute}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#id ExternalOauthIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d8c8358b1d7c296499d2bdb87669d5b64e700e489739d3e0a5355e56d66b45)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument external_oauth_issuer", value=external_oauth_issuer, expected_type=type_hints["external_oauth_issuer"])
            check_type(argname="argument external_oauth_snowflake_user_mapping_attribute", value=external_oauth_snowflake_user_mapping_attribute, expected_type=type_hints["external_oauth_snowflake_user_mapping_attribute"])
            check_type(argname="argument external_oauth_token_user_mapping_claim", value=external_oauth_token_user_mapping_claim, expected_type=type_hints["external_oauth_token_user_mapping_claim"])
            check_type(argname="argument external_oauth_type", value=external_oauth_type, expected_type=type_hints["external_oauth_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument external_oauth_allowed_roles_list", value=external_oauth_allowed_roles_list, expected_type=type_hints["external_oauth_allowed_roles_list"])
            check_type(argname="argument external_oauth_any_role_mode", value=external_oauth_any_role_mode, expected_type=type_hints["external_oauth_any_role_mode"])
            check_type(argname="argument external_oauth_audience_list", value=external_oauth_audience_list, expected_type=type_hints["external_oauth_audience_list"])
            check_type(argname="argument external_oauth_blocked_roles_list", value=external_oauth_blocked_roles_list, expected_type=type_hints["external_oauth_blocked_roles_list"])
            check_type(argname="argument external_oauth_jws_keys_url", value=external_oauth_jws_keys_url, expected_type=type_hints["external_oauth_jws_keys_url"])
            check_type(argname="argument external_oauth_rsa_public_key", value=external_oauth_rsa_public_key, expected_type=type_hints["external_oauth_rsa_public_key"])
            check_type(argname="argument external_oauth_rsa_public_key2", value=external_oauth_rsa_public_key2, expected_type=type_hints["external_oauth_rsa_public_key2"])
            check_type(argname="argument external_oauth_scope_delimiter", value=external_oauth_scope_delimiter, expected_type=type_hints["external_oauth_scope_delimiter"])
            check_type(argname="argument external_oauth_scope_mapping_attribute", value=external_oauth_scope_mapping_attribute, expected_type=type_hints["external_oauth_scope_mapping_attribute"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "external_oauth_issuer": external_oauth_issuer,
            "external_oauth_snowflake_user_mapping_attribute": external_oauth_snowflake_user_mapping_attribute,
            "external_oauth_token_user_mapping_claim": external_oauth_token_user_mapping_claim,
            "external_oauth_type": external_oauth_type,
            "name": name,
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
        if external_oauth_allowed_roles_list is not None:
            self._values["external_oauth_allowed_roles_list"] = external_oauth_allowed_roles_list
        if external_oauth_any_role_mode is not None:
            self._values["external_oauth_any_role_mode"] = external_oauth_any_role_mode
        if external_oauth_audience_list is not None:
            self._values["external_oauth_audience_list"] = external_oauth_audience_list
        if external_oauth_blocked_roles_list is not None:
            self._values["external_oauth_blocked_roles_list"] = external_oauth_blocked_roles_list
        if external_oauth_jws_keys_url is not None:
            self._values["external_oauth_jws_keys_url"] = external_oauth_jws_keys_url
        if external_oauth_rsa_public_key is not None:
            self._values["external_oauth_rsa_public_key"] = external_oauth_rsa_public_key
        if external_oauth_rsa_public_key2 is not None:
            self._values["external_oauth_rsa_public_key2"] = external_oauth_rsa_public_key2
        if external_oauth_scope_delimiter is not None:
            self._values["external_oauth_scope_delimiter"] = external_oauth_scope_delimiter
        if external_oauth_scope_mapping_attribute is not None:
            self._values["external_oauth_scope_mapping_attribute"] = external_oauth_scope_mapping_attribute
        if id is not None:
            self._values["id"] = id

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
        '''Specifies whether to initiate operation of the integration or suspend it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#enabled ExternalOauthIntegration#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def external_oauth_issuer(self) -> builtins.str:
        '''Specifies the URL to define the OAuth 2.0 authorization server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_issuer ExternalOauthIntegration#external_oauth_issuer}
        '''
        result = self._values.get("external_oauth_issuer")
        assert result is not None, "Required property 'external_oauth_issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_oauth_snowflake_user_mapping_attribute(self) -> builtins.str:
        '''Indicates which Snowflake user record attribute should be used to map the access token to a Snowflake user record.

        Valid values are (case-insensitive): ``LOGIN_NAME`` | ``EMAIL_ADDRESS``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_snowflake_user_mapping_attribute ExternalOauthIntegration#external_oauth_snowflake_user_mapping_attribute}
        '''
        result = self._values.get("external_oauth_snowflake_user_mapping_attribute")
        assert result is not None, "Required property 'external_oauth_snowflake_user_mapping_attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_oauth_token_user_mapping_claim(self) -> typing.List[builtins.str]:
        '''Specifies the access token claim or claims that can be used to map the access token to a Snowflake user record.

        If removed from the config, the resource is recreated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_token_user_mapping_claim ExternalOauthIntegration#external_oauth_token_user_mapping_claim}
        '''
        result = self._values.get("external_oauth_token_user_mapping_claim")
        assert result is not None, "Required property 'external_oauth_token_user_mapping_claim' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def external_oauth_type(self) -> builtins.str:
        '''Specifies the OAuth 2.0 authorization server to be Okta, Microsoft Azure AD, Ping Identity PingFederate, or a Custom OAuth 2.0 authorization server. Valid values are (case-insensitive): ``OKTA`` | ``AZURE`` | ``PING_FEDERATE`` | ``CUSTOM``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_type ExternalOauthIntegration#external_oauth_type}
        '''
        result = self._values.get("external_oauth_type")
        assert result is not None, "Required property 'external_oauth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the External Oath integration.

        This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#name ExternalOauthIntegration#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the OAuth integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#comment ExternalOauthIntegration#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_oauth_allowed_roles_list(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of roles that the client can set as the primary role.

        For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_allowed_roles_list ExternalOauthIntegration#external_oauth_allowed_roles_list}
        '''
        result = self._values.get("external_oauth_allowed_roles_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_oauth_any_role_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the OAuth client or user can use a role that is not defined in the OAuth access token.

        Valid values are (case-insensitive): ``DISABLE`` | ``ENABLE`` | ``ENABLE_FOR_PRIVILEGE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_any_role_mode ExternalOauthIntegration#external_oauth_any_role_mode}
        '''
        result = self._values.get("external_oauth_any_role_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_oauth_audience_list(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies additional values that can be used for the access token's audience validation on top of using the Customer's Snowflake Account URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_audience_list ExternalOauthIntegration#external_oauth_audience_list}
        '''
        result = self._values.get("external_oauth_audience_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_oauth_blocked_roles_list(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of roles that a client cannot set as the primary role.

        By default, this list includes the ACCOUNTADMIN, ORGADMIN and SECURITYADMIN roles. To remove these privileged roles from the list, use the ALTER ACCOUNT command to set the EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST account parameter to FALSE. For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_blocked_roles_list ExternalOauthIntegration#external_oauth_blocked_roles_list}
        '''
        result = self._values.get("external_oauth_blocked_roles_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_oauth_jws_keys_url(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the endpoint or a list of endpoints from which to download public keys or certificates to validate an External OAuth access token.

        The maximum number of URLs that can be specified in the list is 3. If removed from the config, the resource is recreated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_jws_keys_url ExternalOauthIntegration#external_oauth_jws_keys_url}
        '''
        result = self._values.get("external_oauth_jws_keys_url")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_oauth_rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers.

        If removed from the config, the resource is recreated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_rsa_public_key ExternalOauthIntegration#external_oauth_rsa_public_key}
        '''
        result = self._values.get("external_oauth_rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_oauth_rsa_public_key2(self) -> typing.Optional[builtins.str]:
        '''Specifies a second RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers.

        Used for key rotation. If removed from the config, the resource is recreated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_rsa_public_key_2 ExternalOauthIntegration#external_oauth_rsa_public_key_2}
        '''
        result = self._values.get("external_oauth_rsa_public_key2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_oauth_scope_delimiter(self) -> typing.Optional[builtins.str]:
        '''Specifies the scope delimiter in the authorization token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_scope_delimiter ExternalOauthIntegration#external_oauth_scope_delimiter}
        '''
        result = self._values.get("external_oauth_scope_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_oauth_scope_mapping_attribute(self) -> typing.Optional[builtins.str]:
        '''Specifies the access token claim to map the access token to an account role.

        If removed from the config, the resource is recreated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#external_oauth_scope_mapping_attribute ExternalOauthIntegration#external_oauth_scope_mapping_attribute}
        '''
        result = self._values.get("external_oauth_scope_mapping_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_oauth_integration#id ExternalOauthIntegration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputComment",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputComment:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputComment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputCommentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputCommentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f05c2a1d2559b562092d8c8070b0b47da81f32ac672f1bd6dba302c7c102c2e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputCommentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951e606f8889d5cf1fbe8af7ddc0f74d15ea0bcfd1c69981215b704ebe26f4da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputCommentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ffde6087278c1648711f977a76e1676140dff2421f609b7e86782cce3ca916)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a8564c944ef547be51dbde36d71e651a9ccabaf5fabebc1dc08c41d2ab4c1c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c7845923be8c420b146bfa47a0636e8e63f3bef11efd9b496cef1669cacc5f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputCommentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputCommentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba6aa35c1906bca1570f4e16824efac6f7b79f5e9faaebb3dd9908d888c69a22)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputComment]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputComment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputComment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6961b84cff08ef69964049c3850c3a5b66069b8f03e2298a2f3dcb65c950b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputEnabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputEnabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputEnabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputEnabledList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputEnabledList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18dcff3cc2fcd266e23b08ddacddc9e5578ddb92f393fda1e98b7d6fa6bc9c6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputEnabledOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead2494c7aaa7d4de223b330f44d9da4b25ec34ebd333c134577b92e6170f010)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputEnabledOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b7a30dc45e793d1fcf727e433d28178651ae36dabd56a862f57d0e65624f8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f506042e7d2815824cc4ddd12d9ab106f17d890609a5b678d918549c989db80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d01b33b9432519b09c05123264c62c39fad5e12e1e9d91426c1f6985ed4f9a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputEnabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputEnabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cffc02298fb35cbf4cba99e60c6fb7ffb71c57f4f646c777a45aa574e8373d00)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputEnabled]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputEnabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputEnabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3004e99c23ebac29e5361440bd3b93399a7973f80c01b89ec8aebb99fd123f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__194752679719ddb2edf9cfec8df866d2cbfc8bc95b41c5c66e55eff821d127c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38031c1ec6dae0ac422976edf8a696d9ff770222c6d0b170354bd36361af552)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05948a277bfdc4347838736b31d28caa807bde6026f564e8083bb9ed047f3863)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bdab36afd82a5e940e9fa1b8c8157cce745525e68ab85f40cae513703e17f89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__319422fc14801f14664fa55d1ce79aaa18fb300337a7cc8f677751f7f0a8686f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3502a8eaadbcda75936eb980bc0f282491aa846aa4c5bbe4951bf0465311131c)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStruct]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b120b964bdfae2d98aba9f6599e271a8db2203a83bd26de4f914f2afdd4e61af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleMode",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleMode:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0be01a5733f5ace8c6c62e6525a33388c20674d3f46c1cfdd6e0d68ee2ff858)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4fadd2790a0b283c311db1af512fefead626f47c905b3b58283a8e30bf19b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f0f7b04b1c2b393c60b0af262e257b54fb552878016741eb84e9b83b6254bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17bbeec715b68bf8ace499bcf1e965608b20148950dfdddedc5e8c69897936e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99bb7d1bbc38d4048d8b1a215a4f8336ded2d4462208f8beb854c0713e692497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0781fbc52089fbef03c648d657160ba446ccf9cf0803d267f9be46676df28aa2)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleMode]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleMode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleMode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d596e91ffa64ec73156498c15699087406cba36bb7a988e87d7f909176193b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2def37604997391dc1c21e57133fdabc5c65ccbffe71099ece9f2db123a8b79b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9386e2efd02a2b7d5a1e127d2545a037c591a7b8dfce7597edd9e004dca81272)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e24a49910c3f98f6d91f337fcb8725730dab7cbffc4108875236230e04e9568)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f1918ce731d818d8dea69d2935c4c340749be8d8c8ae0364f52c5e835ab2cfc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__488596ee2fe08322c9576d09e4533334d06394b2ecc91a1339111731ed31ad1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__613e9daf6e29729b8ecfb51d36bcf29ca6c8498f3076d05a111a53f0c9573b67)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStruct]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7ac569bc57332be0bac3a9cf7fb9cda311e063e958cca871e0a84c4ad0a05a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6bcee608055f43bec64389c90483fc0de095b29d5b559d7707bfcd69011f310)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ab9e2ead93b82b94330070e9b72b03ec7bedcba7e328d95d2062f9d761dd32)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f53ac71f3dbfc1d77a92296628e3a0ea1002b9bcc09d9aab91124f75cb6f3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__244c63c03a957e7198d86343746749ad6fcb09fce5e354e4a975a2f4bbf3ff06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71e8e4b07b671b3fe59dd40ef5aa890fae10978ce060f6263608fbc439e2ca20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fa7fc64638980b96f9058c04b102a43d86b64ffe4116ca32e6357ba684ecd9f)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStruct]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f75dc59b42743c97d310315ab9c8d3b9bf470827c8d61d274507bf49983e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthIssuer",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthIssuer:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthIssuer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthIssuerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthIssuerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3891053d829bc26df1c252956c708258053520c0be66e3643bd080361bc94362)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthIssuerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ab3dba852943a64f154b8f17a91497d86f34548d85447b2b80b499765981a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthIssuerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa15a0245d16670b75ece83c867f0b763955c445fa0f9b63efea6fc7afba1d09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8aa0a9a71b9c7e2a8fb1bed88b661b853188d2474ec94252267098c1b0552a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fdaf3b93b86bf263016e779606fe933ca1239497d8be9fcd9ab5d2cea5c26a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthIssuerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthIssuerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ccfef55d120e1c538553d0010de02191718bdeca6ae0ad9438a03524c809f7c)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthIssuer]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthIssuer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthIssuer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ccde13ce89a15a99517fc2f808abf49d765562f6154ef93b76ef4a5a6b9d3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b915bd9905bc92d87dc750a29b553a30a778dde3b6c68ae24584d9af44f01dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc1089a4c5f0a073cd0583f534602afb842b059a90697369d35bfa90078fcee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d3836542074ba78e4e3fb2e4a906774ac9093327404d776d28b2f2378e3e23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__429c82c949d1f17a919abaa7d31adc99b2e139cd8e6898c3756b8288193e6b7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4b1669e08cc4f4ea2df0592d099574daac58e64eb1678f63422d31ed9476b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1268149ecb2db3dfe4cad92e3d458836942965f6f5e98ae5e666c15516d1f9db)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrl]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2568268077d2eadbedeb12f12cb550a35118dd2a6d36eb6817e7bebfc9c92b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdf310b675b2bb165f0fe24d1b11094b9c243ae0d19bc73f293250bc95cc1ad7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5885e06f00dd855e7daa1392a82077dde72bfff8d448abea14bab502872824bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2956550f911af53a6c86189ec6f4a96439e320c1bcd537d2cb312cc2b0047801)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cc0076c4e99fc964ed791a9fd4d25fbd3f37d81cbcec7f086c863d85952b7f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d507a31c1d093c02fef0a5dd630db8fbd6d07f561da90276f48169f7160a9ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__520171eac47ddb3f16a7df7c94fa2b324045cc5245ce0ee847a16e9e64d1ce2d)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9943c9fe1c8c7f7f1f4f0130ac348cc24e73e06780da5a1d1f237243f179a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23e02321ee0184e322a9dca807c9b187313e29415e8af4bd61d586540a072adb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0922cafd62630d848371b9ccfc60007afaa40d22df70c2d113b5aaa9dbba94)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b84f27ea88e543fe7386cbf3311faa480676a89f5478ce783c3861c84b282e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14b8a3035b11118c878ef831e05d922e968b54d099cf3f14480bb4d0175fc81f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3ee5fac6e831dfc2a89e98c814305df950080a1606a53f400ba9c84f065783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__240e1d640d467fe326b55266545d2162ca48b6151aa617357a395b58477da277)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7080d8e6801d4c7e15d13bf3c3a24144efb12dd8a3ada933ddf9f6d7218e74b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiter",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiter:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__240349e4be6ca9736e7672f3baaf3ee2ce8494546173d0fbb99e023f16c93514)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf7b712f333bdc8b770190880a6ff229a9ed362158b92d73a9cf527c747e219)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe21e38e2301161e0767efe672e2fb39ee8ad38aed723667517230ad2e1d925d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__526ad344e0760793e53df669d67278cc862a462808da5f9ecd04f5788ffb4cd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f02269599cd524f7775af45e522d118365d8a834ecaba0661d40f8c1f6684682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03c2ea75a1744b4db50fcb6801e0dfb73acadbc4db97811081393531056b14e2)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiter]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__952747ea1b2b898846ae60c9f9fb49b4ba4f69d3373144df12fce86831d4d1f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttribute",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttribute:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttribute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__559c08f5605c49bc7bf129302145c589e09bcfcfeaa7dfd3dcecdaa92c2ae945)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe97a8a6b344cdc8662ffc9d58aefed0f7cf9c3fc05fc0e2937e8c08907f8ff8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140293f794dd31a3e1b0f16daa2f0f5026fee691658b800f68e45eb57efb4ed9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__745d49e62983e66602bb82729912921a3d3913d55bc1be29ef71076d55c98add)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a6ebc85057b360150812a23e8abf76a7ae97950f7560e89a3eaa0850d299422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41f8370ef13ccd7eb42dd0048e68b3b481bee0cc00fbf00d3b6e03de9e48d67a)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttribute]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttribute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttribute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63569d1e79633d45fefc552db3d28adb04a8c95681d5c8fb189bc91e3e6b8560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaim",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaim:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0dc0ad97ecf7bac2d2b02067251fcdee5030766ec718032b41f1f5ff0d26ce2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11bec8745cf278fdfa7aeaa5581f93e98bb2397d741ca4fb331633dce20f9dbc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74cc7f1a405fac2549929dcf54ce631b5e41e39b7f31528be2f7b2ba39129fda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bd9c3bf9427fbde3fc6fc6f279141ab094b549bf2da0e025e3342a8cd8eac91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da1e6683068c32947b5a7b52e1982e37726398450a5a0270af834b2c377a53ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66a470487578b942cb2d78bacf1420c6bbe72b100a44510113efa6c7326f7f11)
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
    ) -> typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaim]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaim], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaim],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a681c53f934f98d215e98ed9ebd86f982c49c54ccb63ea960e500f17c9d116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd27ea6dc3589e2b5f5248038b3605f4720be917f5ef141377343c2903797d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90b3f5606798ce76e77504726fbd259ae746cefd1366cf1a683d199b3f406858)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5dff239cdd859aa74bfdbfff66d93a606a1790e7ab1a4cf18396c6955ae5dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56cf1b5f4c35a0fef42188e6186115a5e4388fc8992a8f74b048918917e6ce44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a060d816c926eb5ea934f759673e319d899aabe6e232420b7efade2b08b1b4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88b81b2b1acffad50329bff4f51fae6e18ea0ef3c08ac84bf81eb4d7dc368592)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> ExternalOauthIntegrationDescribeOutputCommentList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputCommentList, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> ExternalOauthIntegrationDescribeOutputEnabledList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputEnabledList, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthAllowedRolesList")
    def external_oauth_allowed_roles_list(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructList, jsii.get(self, "externalOauthAllowedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthAnyRoleMode")
    def external_oauth_any_role_mode(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeList, jsii.get(self, "externalOauthAnyRoleMode"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthAudienceList")
    def external_oauth_audience_list(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructList, jsii.get(self, "externalOauthAudienceList"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthBlockedRolesList")
    def external_oauth_blocked_roles_list(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructList, jsii.get(self, "externalOauthBlockedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthIssuer")
    def external_oauth_issuer(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthIssuerList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthIssuerList, jsii.get(self, "externalOauthIssuer"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthJwsKeysUrl")
    def external_oauth_jws_keys_url(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlList, jsii.get(self, "externalOauthJwsKeysUrl"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthRsaPublicKey")
    def external_oauth_rsa_public_key(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyList, jsii.get(self, "externalOauthRsaPublicKey"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthRsaPublicKey2")
    def external_oauth_rsa_public_key2(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2List:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2List, jsii.get(self, "externalOauthRsaPublicKey2"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthScopeDelimiter")
    def external_oauth_scope_delimiter(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterList, jsii.get(self, "externalOauthScopeDelimiter"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthSnowflakeUserMappingAttribute")
    def external_oauth_snowflake_user_mapping_attribute(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeList, jsii.get(self, "externalOauthSnowflakeUserMappingAttribute"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthTokenUserMappingClaim")
    def external_oauth_token_user_mapping_claim(
        self,
    ) -> ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimList:
        return typing.cast(ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimList, jsii.get(self, "externalOauthTokenUserMappingClaim"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExternalOauthIntegrationDescribeOutput]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc275f07b7622a0442ff30714419900491eca64612439612c8a68f8e8a9c59d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationRelatedParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationRelatedParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationRelatedParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dd151e5a32cedabe5d19f11fe8d3f196c39e03068f139031b491be862b45c3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325b41e59e2e03b7ec28e3669b25bb5d61a74a3956a11080c4a849d01f2bb57a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ef87ec763c40b20c7b5249d55cfc9f2f72a2ab7db02107ce551b8ab8493754)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a0ce47cc97eb70a4e4255f312282fa1103dbf57d741ef0a08214d6bdec96a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e893df928da7fe18f4e619ba07ec7bd3d0f9455c7b11f9f4d6112a379e661401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__589b485db250c4fb40610561693ef09459083fff1d927031d8a4c85f5f8e2044)
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
    ) -> typing.Optional[ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStruct]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e33563108322342bc8957faf07cb143701b46337d02871d74cfe176a97cf291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationRelatedParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationRelatedParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0520d6b15c53e794bfa4b3c1bfc7b201e9cc91bfc1011f014c2e207a80326016)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationRelatedParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740f4a1b39774306a935bc4e3c4949f936bb4c9823c5a6a1cb8d089c53b99615)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationRelatedParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f52de0d6e0a50e0429dd55c5c508bb6c284f8ec300b21f161cc9a9428197e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edf3a2a7c88338280499f34cc85ea2140a48dfed86adb3903b87e6cecdd1bca2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40256565044c8a8733ab88554159fe197ceabd9057aa5da143aec81ca01621b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationRelatedParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationRelatedParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc435324885e343117f49127fc39b1f719b21756c4ace474fd93a14462d437ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="externalOauthAddPrivilegedRolesToBlockedList")
    def external_oauth_add_privileged_roles_to_blocked_list(
        self,
    ) -> ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructList:
        return typing.cast(ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructList, jsii.get(self, "externalOauthAddPrivilegedRolesToBlockedList"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ExternalOauthIntegrationRelatedParameters]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationRelatedParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationRelatedParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761a35c33bdb01c0f756cd61e055d318f41f340a25110f2c32fce1d1e8afbfb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ExternalOauthIntegrationShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalOauthIntegrationShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2fe76d320736217afcea88e2a7c5c289f321522bf102b9a11548d374707c6c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ExternalOauthIntegrationShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ab28c865f02b025bf7873e240e4f7416394ac435843c99d4d9d2afc9cb01e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalOauthIntegrationShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b13616b37529cfb262d10221fa60218ef5a04822f45e39fc2a4b0e1db98a4a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f686ce12e8c59ddb1381a1be24d6139376a0398a7c101165f0ed31ad4560e9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__540b3bd4a202c3b905c8c38327941dbea395707dcd0ddcee147a6f2ae8bf6d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ExternalOauthIntegrationShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1be0ed180b370e557b95ec7fe20ab408ba5b5925ec49d471cd153ac9b1cecea)
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
    def internal_value(self) -> typing.Optional[ExternalOauthIntegrationShowOutput]:
        return typing.cast(typing.Optional[ExternalOauthIntegrationShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExternalOauthIntegrationShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838bbab76ef1b76a84660c358a77cbb269df7cf85fbb0170589ddf83ca9c076d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ExternalOauthIntegration",
    "ExternalOauthIntegrationConfig",
    "ExternalOauthIntegrationDescribeOutput",
    "ExternalOauthIntegrationDescribeOutputComment",
    "ExternalOauthIntegrationDescribeOutputCommentList",
    "ExternalOauthIntegrationDescribeOutputCommentOutputReference",
    "ExternalOauthIntegrationDescribeOutputEnabled",
    "ExternalOauthIntegrationDescribeOutputEnabledList",
    "ExternalOauthIntegrationDescribeOutputEnabledOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStruct",
    "ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStructOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleMode",
    "ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleModeOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStruct",
    "ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStructOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStruct",
    "ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStructOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthIssuer",
    "ExternalOauthIntegrationDescribeOutputExternalOauthIssuerList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthIssuerOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrl",
    "ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrlOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey",
    "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2",
    "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2List",
    "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2OutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKeyOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiter",
    "ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiterOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttribute",
    "ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference",
    "ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaim",
    "ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimList",
    "ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaimOutputReference",
    "ExternalOauthIntegrationDescribeOutputList",
    "ExternalOauthIntegrationDescribeOutputOutputReference",
    "ExternalOauthIntegrationRelatedParameters",
    "ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStruct",
    "ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructList",
    "ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStructOutputReference",
    "ExternalOauthIntegrationRelatedParametersList",
    "ExternalOauthIntegrationRelatedParametersOutputReference",
    "ExternalOauthIntegrationShowOutput",
    "ExternalOauthIntegrationShowOutputList",
    "ExternalOauthIntegrationShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__35dfabda2663a4d9bee41d19b6803bf06a1bf44ff04ed45d617bdefca8249594(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    external_oauth_issuer: builtins.str,
    external_oauth_snowflake_user_mapping_attribute: builtins.str,
    external_oauth_token_user_mapping_claim: typing.Sequence[builtins.str],
    external_oauth_type: builtins.str,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    external_oauth_allowed_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_oauth_any_role_mode: typing.Optional[builtins.str] = None,
    external_oauth_audience_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_oauth_blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_oauth_jws_keys_url: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_oauth_rsa_public_key: typing.Optional[builtins.str] = None,
    external_oauth_rsa_public_key2: typing.Optional[builtins.str] = None,
    external_oauth_scope_delimiter: typing.Optional[builtins.str] = None,
    external_oauth_scope_mapping_attribute: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__0ba49d5af8dd32aa32671a62f79d536bad66c4da7099ba0845b821025745ddb7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac030933dd792662e17628398b3465cb3b686a90faffd2d872c76b9626c1f18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0fdf1abb35924f96b3e2e06ce9f694730e4ac6ceff1cb9d305511acb5af576(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e406d246d8a808516861e02fca6fd3ee0411b34cf5ba278b6ff42b6c642934(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc91b850d1c88bf2576c219c79bc388426afc5128c0c36c7beb40d1fd5d61a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9ccd124663370c0abe76d9443fceb34d4c5bca657965a07d7b213d5a710c2e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1683e8f055b2384f31039ae60a649287f3b0b93e6c3650b8e596d6ab76f00d0f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5c6b9df1c8e4dcbc6710ba3427a6fd5686d84492118211345f150554b42f02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8356de93e2811cbff76f080d066e6ade944f15cc8c84e5d0938ecda33a846b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a031be7d3c472f16017762f777adcb8854104aaebfdf2410e8817d125f6a5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd72c4d51b5846d37f9d3cfcfc7d51bd4d73ed4df55e5299c6ee2d0224e9dc19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac958fb64fd155600720fcf04e8ec92fe957d988c1aa5d48687ddf533a162f0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce86aa42efb12c7b9176d213dc7d9907038cad34c134daaca4eca85e05cfa55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b38cb6e29bf0ced54672acca1052ddbb7ee1a3bb915126d50cf7021f321891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd598442b95f12e2a5ea0250bbe0072dce1b0a592ef9ceeaae4f73f436072d8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1df96291435c387207c764d99b3268ea200ecac5ed2fd9b6b075a9c64b8a212(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808cdddc1a5523ee6b86977e8d07f33273cadd92c00a1bf54d1f79e7647aa75b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5915b3b17c1324f7c13b61f21ddc02c9045e2845be02dcebbae2631b6b34dc47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d8c8358b1d7c296499d2bdb87669d5b64e700e489739d3e0a5355e56d66b45(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    external_oauth_issuer: builtins.str,
    external_oauth_snowflake_user_mapping_attribute: builtins.str,
    external_oauth_token_user_mapping_claim: typing.Sequence[builtins.str],
    external_oauth_type: builtins.str,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    external_oauth_allowed_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_oauth_any_role_mode: typing.Optional[builtins.str] = None,
    external_oauth_audience_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_oauth_blocked_roles_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_oauth_jws_keys_url: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_oauth_rsa_public_key: typing.Optional[builtins.str] = None,
    external_oauth_rsa_public_key2: typing.Optional[builtins.str] = None,
    external_oauth_scope_delimiter: typing.Optional[builtins.str] = None,
    external_oauth_scope_mapping_attribute: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05c2a1d2559b562092d8c8070b0b47da81f32ac672f1bd6dba302c7c102c2e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951e606f8889d5cf1fbe8af7ddc0f74d15ea0bcfd1c69981215b704ebe26f4da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ffde6087278c1648711f977a76e1676140dff2421f609b7e86782cce3ca916(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8564c944ef547be51dbde36d71e651a9ccabaf5fabebc1dc08c41d2ab4c1c3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7845923be8c420b146bfa47a0636e8e63f3bef11efd9b496cef1669cacc5f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6aa35c1906bca1570f4e16824efac6f7b79f5e9faaebb3dd9908d888c69a22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6961b84cff08ef69964049c3850c3a5b66069b8f03e2298a2f3dcb65c950b94(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputComment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dcff3cc2fcd266e23b08ddacddc9e5578ddb92f393fda1e98b7d6fa6bc9c6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead2494c7aaa7d4de223b330f44d9da4b25ec34ebd333c134577b92e6170f010(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b7a30dc45e793d1fcf727e433d28178651ae36dabd56a862f57d0e65624f8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f506042e7d2815824cc4ddd12d9ab106f17d890609a5b678d918549c989db80(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d01b33b9432519b09c05123264c62c39fad5e12e1e9d91426c1f6985ed4f9a4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffc02298fb35cbf4cba99e60c6fb7ffb71c57f4f646c777a45aa574e8373d00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3004e99c23ebac29e5361440bd3b93399a7973f80c01b89ec8aebb99fd123f(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputEnabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194752679719ddb2edf9cfec8df866d2cbfc8bc95b41c5c66e55eff821d127c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38031c1ec6dae0ac422976edf8a696d9ff770222c6d0b170354bd36361af552(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05948a277bfdc4347838736b31d28caa807bde6026f564e8083bb9ed047f3863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdab36afd82a5e940e9fa1b8c8157cce745525e68ab85f40cae513703e17f89(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319422fc14801f14664fa55d1ce79aaa18fb300337a7cc8f677751f7f0a8686f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3502a8eaadbcda75936eb980bc0f282491aa846aa4c5bbe4951bf0465311131c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b120b964bdfae2d98aba9f6599e271a8db2203a83bd26de4f914f2afdd4e61af(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAllowedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0be01a5733f5ace8c6c62e6525a33388c20674d3f46c1cfdd6e0d68ee2ff858(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4fadd2790a0b283c311db1af512fefead626f47c905b3b58283a8e30bf19b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f0f7b04b1c2b393c60b0af262e257b54fb552878016741eb84e9b83b6254bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17bbeec715b68bf8ace499bcf1e965608b20148950dfdddedc5e8c69897936e4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bb7d1bbc38d4048d8b1a215a4f8336ded2d4462208f8beb854c0713e692497(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0781fbc52089fbef03c648d657160ba446ccf9cf0803d267f9be46676df28aa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d596e91ffa64ec73156498c15699087406cba36bb7a988e87d7f909176193b11(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAnyRoleMode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2def37604997391dc1c21e57133fdabc5c65ccbffe71099ece9f2db123a8b79b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9386e2efd02a2b7d5a1e127d2545a037c591a7b8dfce7597edd9e004dca81272(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e24a49910c3f98f6d91f337fcb8725730dab7cbffc4108875236230e04e9568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1918ce731d818d8dea69d2935c4c340749be8d8c8ae0364f52c5e835ab2cfc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488596ee2fe08322c9576d09e4533334d06394b2ecc91a1339111731ed31ad1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613e9daf6e29729b8ecfb51d36bcf29ca6c8498f3076d05a111a53f0c9573b67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7ac569bc57332be0bac3a9cf7fb9cda311e063e958cca871e0a84c4ad0a05a(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthAudienceListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bcee608055f43bec64389c90483fc0de095b29d5b559d7707bfcd69011f310(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ab9e2ead93b82b94330070e9b72b03ec7bedcba7e328d95d2062f9d761dd32(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f53ac71f3dbfc1d77a92296628e3a0ea1002b9bcc09d9aab91124f75cb6f3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244c63c03a957e7198d86343746749ad6fcb09fce5e354e4a975a2f4bbf3ff06(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e8e4b07b671b3fe59dd40ef5aa890fae10978ce060f6263608fbc439e2ca20(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa7fc64638980b96f9058c04b102a43d86b64ffe4116ca32e6357ba684ecd9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f75dc59b42743c97d310315ab9c8d3b9bf470827c8d61d274507bf49983e11(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthBlockedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3891053d829bc26df1c252956c708258053520c0be66e3643bd080361bc94362(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ab3dba852943a64f154b8f17a91497d86f34548d85447b2b80b499765981a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa15a0245d16670b75ece83c867f0b763955c445fa0f9b63efea6fc7afba1d09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8aa0a9a71b9c7e2a8fb1bed88b661b853188d2474ec94252267098c1b0552a6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdaf3b93b86bf263016e779606fe933ca1239497d8be9fcd9ab5d2cea5c26a9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccfef55d120e1c538553d0010de02191718bdeca6ae0ad9438a03524c809f7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccde13ce89a15a99517fc2f808abf49d765562f6154ef93b76ef4a5a6b9d3ea(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthIssuer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b915bd9905bc92d87dc750a29b553a30a778dde3b6c68ae24584d9af44f01dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc1089a4c5f0a073cd0583f534602afb842b059a90697369d35bfa90078fcee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d3836542074ba78e4e3fb2e4a906774ac9093327404d776d28b2f2378e3e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429c82c949d1f17a919abaa7d31adc99b2e139cd8e6898c3756b8288193e6b7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b1669e08cc4f4ea2df0592d099574daac58e64eb1678f63422d31ed9476b90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1268149ecb2db3dfe4cad92e3d458836942965f6f5e98ae5e666c15516d1f9db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2568268077d2eadbedeb12f12cb550a35118dd2a6d36eb6817e7bebfc9c92b8(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthJwsKeysUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf310b675b2bb165f0fe24d1b11094b9c243ae0d19bc73f293250bc95cc1ad7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5885e06f00dd855e7daa1392a82077dde72bfff8d448abea14bab502872824bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2956550f911af53a6c86189ec6f4a96439e320c1bcd537d2cb312cc2b0047801(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc0076c4e99fc964ed791a9fd4d25fbd3f37d81cbcec7f086c863d85952b7f3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d507a31c1d093c02fef0a5dd630db8fbd6d07f561da90276f48169f7160a9ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520171eac47ddb3f16a7df7c94fa2b324045cc5245ce0ee847a16e9e64d1ce2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9943c9fe1c8c7f7f1f4f0130ac348cc24e73e06780da5a1d1f237243f179a47(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e02321ee0184e322a9dca807c9b187313e29415e8af4bd61d586540a072adb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0922cafd62630d848371b9ccfc60007afaa40d22df70c2d113b5aaa9dbba94(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b84f27ea88e543fe7386cbf3311faa480676a89f5478ce783c3861c84b282e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b8a3035b11118c878ef831e05d922e968b54d099cf3f14480bb4d0175fc81f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3ee5fac6e831dfc2a89e98c814305df950080a1606a53f400ba9c84f065783(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240e1d640d467fe326b55266545d2162ca48b6151aa617357a395b58477da277(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7080d8e6801d4c7e15d13bf3c3a24144efb12dd8a3ada933ddf9f6d7218e74b(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthRsaPublicKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240349e4be6ca9736e7672f3baaf3ee2ce8494546173d0fbb99e023f16c93514(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf7b712f333bdc8b770190880a6ff229a9ed362158b92d73a9cf527c747e219(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe21e38e2301161e0767efe672e2fb39ee8ad38aed723667517230ad2e1d925d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__526ad344e0760793e53df669d67278cc862a462808da5f9ecd04f5788ffb4cd1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02269599cd524f7775af45e522d118365d8a834ecaba0661d40f8c1f6684682(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c2ea75a1744b4db50fcb6801e0dfb73acadbc4db97811081393531056b14e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952747ea1b2b898846ae60c9f9fb49b4ba4f69d3373144df12fce86831d4d1f7(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthScopeDelimiter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559c08f5605c49bc7bf129302145c589e09bcfcfeaa7dfd3dcecdaa92c2ae945(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe97a8a6b344cdc8662ffc9d58aefed0f7cf9c3fc05fc0e2937e8c08907f8ff8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140293f794dd31a3e1b0f16daa2f0f5026fee691658b800f68e45eb57efb4ed9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745d49e62983e66602bb82729912921a3d3913d55bc1be29ef71076d55c98add(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6ebc85057b360150812a23e8abf76a7ae97950f7560e89a3eaa0850d299422(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f8370ef13ccd7eb42dd0048e68b3b481bee0cc00fbf00d3b6e03de9e48d67a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63569d1e79633d45fefc552db3d28adb04a8c95681d5c8fb189bc91e3e6b8560(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthSnowflakeUserMappingAttribute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0dc0ad97ecf7bac2d2b02067251fcdee5030766ec718032b41f1f5ff0d26ce2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11bec8745cf278fdfa7aeaa5581f93e98bb2397d741ca4fb331633dce20f9dbc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74cc7f1a405fac2549929dcf54ce631b5e41e39b7f31528be2f7b2ba39129fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd9c3bf9427fbde3fc6fc6f279141ab094b549bf2da0e025e3342a8cd8eac91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1e6683068c32947b5a7b52e1982e37726398450a5a0270af834b2c377a53ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a470487578b942cb2d78bacf1420c6bbe72b100a44510113efa6c7326f7f11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a681c53f934f98d215e98ed9ebd86f982c49c54ccb63ea960e500f17c9d116(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutputExternalOauthTokenUserMappingClaim],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd27ea6dc3589e2b5f5248038b3605f4720be917f5ef141377343c2903797d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b3f5606798ce76e77504726fbd259ae746cefd1366cf1a683d199b3f406858(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5dff239cdd859aa74bfdbfff66d93a606a1790e7ab1a4cf18396c6955ae5dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56cf1b5f4c35a0fef42188e6186115a5e4388fc8992a8f74b048918917e6ce44(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a060d816c926eb5ea934f759673e319d899aabe6e232420b7efade2b08b1b4d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b81b2b1acffad50329bff4f51fae6e18ea0ef3c08ac84bf81eb4d7dc368592(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc275f07b7622a0442ff30714419900491eca64612439612c8a68f8e8a9c59d8(
    value: typing.Optional[ExternalOauthIntegrationDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd151e5a32cedabe5d19f11fe8d3f196c39e03068f139031b491be862b45c3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325b41e59e2e03b7ec28e3669b25bb5d61a74a3956a11080c4a849d01f2bb57a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ef87ec763c40b20c7b5249d55cfc9f2f72a2ab7db02107ce551b8ab8493754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a0ce47cc97eb70a4e4255f312282fa1103dbf57d741ef0a08214d6bdec96a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e893df928da7fe18f4e619ba07ec7bd3d0f9455c7b11f9f4d6112a379e661401(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589b485db250c4fb40610561693ef09459083fff1d927031d8a4c85f5f8e2044(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e33563108322342bc8957faf07cb143701b46337d02871d74cfe176a97cf291(
    value: typing.Optional[ExternalOauthIntegrationRelatedParametersExternalOauthAddPrivilegedRolesToBlockedListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0520d6b15c53e794bfa4b3c1bfc7b201e9cc91bfc1011f014c2e207a80326016(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740f4a1b39774306a935bc4e3c4949f936bb4c9823c5a6a1cb8d089c53b99615(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f52de0d6e0a50e0429dd55c5c508bb6c284f8ec300b21f161cc9a9428197e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf3a2a7c88338280499f34cc85ea2140a48dfed86adb3903b87e6cecdd1bca2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40256565044c8a8733ab88554159fe197ceabd9057aa5da143aec81ca01621b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc435324885e343117f49127fc39b1f719b21756c4ace474fd93a14462d437ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761a35c33bdb01c0f756cd61e055d318f41f340a25110f2c32fce1d1e8afbfb6(
    value: typing.Optional[ExternalOauthIntegrationRelatedParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2fe76d320736217afcea88e2a7c5c289f321522bf102b9a11548d374707c6c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ab28c865f02b025bf7873e240e4f7416394ac435843c99d4d9d2afc9cb01e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b13616b37529cfb262d10221fa60218ef5a04822f45e39fc2a4b0e1db98a4a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f686ce12e8c59ddb1381a1be24d6139376a0398a7c101165f0ed31ad4560e9d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540b3bd4a202c3b905c8c38327941dbea395707dcd0ddcee147a6f2ae8bf6d7d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1be0ed180b370e557b95ec7fe20ab408ba5b5925ec49d471cd153ac9b1cecea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838bbab76ef1b76a84660c358a77cbb269df7cf85fbb0170589ddf83ca9c076d(
    value: typing.Optional[ExternalOauthIntegrationShowOutput],
) -> None:
    """Type checking stubs"""
    pass
