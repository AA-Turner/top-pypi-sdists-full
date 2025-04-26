r'''
# `snowflake_saml2_integration`

Refer to the Terraform Registry for docs: [`snowflake_saml2_integration`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration).
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


class Saml2Integration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2Integration",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration snowflake_saml2_integration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        saml2_issuer: builtins.str,
        saml2_provider: builtins.str,
        saml2_sso_url: builtins.str,
        saml2_x509_cert: builtins.str,
        allowed_email_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_user_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        saml2_enable_sp_initiated: typing.Optional[builtins.str] = None,
        saml2_force_authn: typing.Optional[builtins.str] = None,
        saml2_post_logout_redirect_url: typing.Optional[builtins.str] = None,
        saml2_requested_nameid_format: typing.Optional[builtins.str] = None,
        saml2_sign_request: typing.Optional[builtins.str] = None,
        saml2_snowflake_acs_url: typing.Optional[builtins.str] = None,
        saml2_snowflake_issuer_url: typing.Optional[builtins.str] = None,
        saml2_sp_initiated_login_page_label: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration snowflake_saml2_integration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Specifies the name of the SAML2 integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#name Saml2Integration#name}
        :param saml2_issuer: The string containing the IdP EntityID / Issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_issuer Saml2Integration#saml2_issuer}
        :param saml2_provider: The string describing the IdP. Valid options are: ``OKTA`` | ``ADFS`` | ``CUSTOM``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_provider Saml2Integration#saml2_provider}
        :param saml2_sso_url: The string containing the IdP SSO URL, where the user should be redirected by Snowflake (the Service Provider) with a SAML AuthnRequest message. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_sso_url Saml2Integration#saml2_sso_url}
        :param saml2_x509_cert: The Base64 encoded IdP signing certificate on a single line without the leading -----BEGIN CERTIFICATE----- and ending -----END CERTIFICATE----- markers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_x509_cert Saml2Integration#saml2_x509_cert}
        :param allowed_email_patterns: A list of regular expressions that email addresses are matched against to authenticate with a SAML2 security integration. If this field changes value from non-empty to empty, the whole resource is recreated because of Snowflake limitations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#allowed_email_patterns Saml2Integration#allowed_email_patterns}
        :param allowed_user_domains: A list of email domains that can authenticate with a SAML2 security integration. If this field changes value from non-empty to empty, the whole resource is recreated because of Snowflake limitations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#allowed_user_domains Saml2Integration#allowed_user_domains}
        :param comment: Specifies a comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#comment Saml2Integration#comment}
        :param enabled: Specifies whether this security integration is enabled or disabled. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#enabled Saml2Integration#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#id Saml2Integration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param saml2_enable_sp_initiated: The Boolean indicating if the Log In With button will be shown on the login page. TRUE: displays the Log in With button on the login page. FALSE: does not display the Log in With button on the login page. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_enable_sp_initiated Saml2Integration#saml2_enable_sp_initiated}
        :param saml2_force_authn: The Boolean indicating whether users, during the initial authentication flow, are forced to authenticate again to access Snowflake. When set to TRUE, Snowflake sets the ForceAuthn SAML parameter to TRUE in the outgoing request from Snowflake to the identity provider. TRUE: forces users to authenticate again to access Snowflake, even if a valid session with the identity provider exists. FALSE: does not force users to authenticate again to access Snowflake. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_force_authn Saml2Integration#saml2_force_authn}
        :param saml2_post_logout_redirect_url: The endpoint to which Snowflake redirects users after clicking the Log Out button in the classic Snowflake web interface. Snowflake terminates the Snowflake session upon redirecting to the specified endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_post_logout_redirect_url Saml2Integration#saml2_post_logout_redirect_url}
        :param saml2_requested_nameid_format: The SAML NameID format allows Snowflake to set an expectation of the identifying attribute of the user (i.e. SAML Subject) in the SAML assertion from the IdP to ensure a valid authentication to Snowflake. Valid options are: ``urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified`` | ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`` | ``urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName`` | ``urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName`` | ``urn:oasis:names:tc:SAML:2.0:nameid-format:kerberos`` | ``urn:oasis:names:tc:SAML:2.0:nameid-format:persistent`` | ``urn:oasis:names:tc:SAML:2.0:nameid-format:transient``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_requested_nameid_format Saml2Integration#saml2_requested_nameid_format}
        :param saml2_sign_request: The Boolean indicating whether SAML requests are signed. TRUE: allows SAML requests to be signed. FALSE: does not allow SAML requests to be signed. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_sign_request Saml2Integration#saml2_sign_request}
        :param saml2_snowflake_acs_url: The string containing the Snowflake Assertion Consumer Service URL to which the IdP will send its SAML authentication response back to Snowflake. This property will be set in the SAML authentication request generated by Snowflake when initiating a SAML SSO operation with the IdP. If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use. Because Okta does not support underscores in URLs, the underscore in the account name must be converted to a hyphen. See `docs <https://docs.snowflake.com/en/user-guide/organizations-connect#okta-urls>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_snowflake_acs_url Saml2Integration#saml2_snowflake_acs_url}
        :param saml2_snowflake_issuer_url: The string containing the EntityID / Issuer for the Snowflake service provider. If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use. Because Okta does not support underscores in URLs, the underscore in the account name must be converted to a hyphen. See `docs <https://docs.snowflake.com/en/user-guide/organizations-connect#okta-urls>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_snowflake_issuer_url Saml2Integration#saml2_snowflake_issuer_url}
        :param saml2_sp_initiated_login_page_label: The string containing the label to display after the Log In With button on the login page. If this field changes value from non-empty to empty, the whole resource is recreated because of Snowflake limitations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_sp_initiated_login_page_label Saml2Integration#saml2_sp_initiated_login_page_label}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fdc4cab6eadc678f8e01b60c79e1ed28a085f458f6ee3ce536d1e2f73571e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Saml2IntegrationConfig(
            name=name,
            saml2_issuer=saml2_issuer,
            saml2_provider=saml2_provider,
            saml2_sso_url=saml2_sso_url,
            saml2_x509_cert=saml2_x509_cert,
            allowed_email_patterns=allowed_email_patterns,
            allowed_user_domains=allowed_user_domains,
            comment=comment,
            enabled=enabled,
            id=id,
            saml2_enable_sp_initiated=saml2_enable_sp_initiated,
            saml2_force_authn=saml2_force_authn,
            saml2_post_logout_redirect_url=saml2_post_logout_redirect_url,
            saml2_requested_nameid_format=saml2_requested_nameid_format,
            saml2_sign_request=saml2_sign_request,
            saml2_snowflake_acs_url=saml2_snowflake_acs_url,
            saml2_snowflake_issuer_url=saml2_snowflake_issuer_url,
            saml2_sp_initiated_login_page_label=saml2_sp_initiated_login_page_label,
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
        '''Generates CDKTF code for importing a Saml2Integration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Saml2Integration to import.
        :param import_from_id: The id of the existing Saml2Integration that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Saml2Integration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d234d7cc8225f9f79e4111d55484297ce1681132be3d4ccd90c9f55cf4f169)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAllowedEmailPatterns")
    def reset_allowed_email_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedEmailPatterns", []))

    @jsii.member(jsii_name="resetAllowedUserDomains")
    def reset_allowed_user_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedUserDomains", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSaml2EnableSpInitiated")
    def reset_saml2_enable_sp_initiated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml2EnableSpInitiated", []))

    @jsii.member(jsii_name="resetSaml2ForceAuthn")
    def reset_saml2_force_authn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml2ForceAuthn", []))

    @jsii.member(jsii_name="resetSaml2PostLogoutRedirectUrl")
    def reset_saml2_post_logout_redirect_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml2PostLogoutRedirectUrl", []))

    @jsii.member(jsii_name="resetSaml2RequestedNameidFormat")
    def reset_saml2_requested_nameid_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml2RequestedNameidFormat", []))

    @jsii.member(jsii_name="resetSaml2SignRequest")
    def reset_saml2_sign_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml2SignRequest", []))

    @jsii.member(jsii_name="resetSaml2SnowflakeAcsUrl")
    def reset_saml2_snowflake_acs_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml2SnowflakeAcsUrl", []))

    @jsii.member(jsii_name="resetSaml2SnowflakeIssuerUrl")
    def reset_saml2_snowflake_issuer_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml2SnowflakeIssuerUrl", []))

    @jsii.member(jsii_name="resetSaml2SpInitiatedLoginPageLabel")
    def reset_saml2_sp_initiated_login_page_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml2SpInitiatedLoginPageLabel", []))

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
    def describe_output(self) -> "Saml2IntegrationDescribeOutputList":
        return typing.cast("Saml2IntegrationDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "Saml2IntegrationShowOutputList":
        return typing.cast("Saml2IntegrationShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="allowedEmailPatternsInput")
    def allowed_email_patterns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedEmailPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedUserDomainsInput")
    def allowed_user_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedUserDomainsInput"))

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
    @jsii.member(jsii_name="saml2EnableSpInitiatedInput")
    def saml2_enable_sp_initiated_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2EnableSpInitiatedInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2ForceAuthnInput")
    def saml2_force_authn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2ForceAuthnInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2IssuerInput")
    def saml2_issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2IssuerInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2PostLogoutRedirectUrlInput")
    def saml2_post_logout_redirect_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2PostLogoutRedirectUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2ProviderInput")
    def saml2_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2ProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2RequestedNameidFormatInput")
    def saml2_requested_nameid_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2RequestedNameidFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2SignRequestInput")
    def saml2_sign_request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2SignRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeAcsUrlInput")
    def saml2_snowflake_acs_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2SnowflakeAcsUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeIssuerUrlInput")
    def saml2_snowflake_issuer_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2SnowflakeIssuerUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2SpInitiatedLoginPageLabelInput")
    def saml2_sp_initiated_login_page_label_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2SpInitiatedLoginPageLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2SsoUrlInput")
    def saml2_sso_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2SsoUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2X509CertInput")
    def saml2_x509_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saml2X509CertInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedEmailPatterns")
    def allowed_email_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedEmailPatterns"))

    @allowed_email_patterns.setter
    def allowed_email_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ee319e05c03cbe88c77cc5a9d80be94a61396aa401e758aac912f8a96ea16c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedEmailPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedUserDomains")
    def allowed_user_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedUserDomains"))

    @allowed_user_domains.setter
    def allowed_user_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e332e6b254b7372161c524d6aae8bf23243541b5a9cc3d0fb25ebf0ffb5144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedUserDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194ef5fd70bea144ee936fd33f6c34963cf9dc492a47a5922ddc4604b77bc2a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5156a2c534b8a6c179aa9da3922f9516f76503c14cb8d192a0f0cc31caf82013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd2e0ad447f0d9858ea393ff27c5671f4cdecd1632c3d04b825f5c3f739e6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748734633f50e0b07becae59b90e3f231d99edaee9e8efa30015958015e088cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2EnableSpInitiated")
    def saml2_enable_sp_initiated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2EnableSpInitiated"))

    @saml2_enable_sp_initiated.setter
    def saml2_enable_sp_initiated(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd457c5411b9c6b0d1444f3009254628113cf29bc6d7ef2d45b56d4d3b1765ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2EnableSpInitiated", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2ForceAuthn")
    def saml2_force_authn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2ForceAuthn"))

    @saml2_force_authn.setter
    def saml2_force_authn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e7e58fa0f6256789139538eefeb67405c2d8898719221a67a9dab79a8c1424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2ForceAuthn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2Issuer")
    def saml2_issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2Issuer"))

    @saml2_issuer.setter
    def saml2_issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983ae4d1c960d45eb021604b6ec2e2c964688029c79495b63e2c20eb0c28761e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2Issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2PostLogoutRedirectUrl")
    def saml2_post_logout_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2PostLogoutRedirectUrl"))

    @saml2_post_logout_redirect_url.setter
    def saml2_post_logout_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d791527e043b8b8ea6d32d4c132d88d63afbe3ae673bc38b8402503fd57f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2PostLogoutRedirectUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2Provider")
    def saml2_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2Provider"))

    @saml2_provider.setter
    def saml2_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a249a6b5028b91945077ee03a4dd9d6ba7b7155f11d89c04916bcdf0fba603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2Provider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2RequestedNameidFormat")
    def saml2_requested_nameid_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2RequestedNameidFormat"))

    @saml2_requested_nameid_format.setter
    def saml2_requested_nameid_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22a4e162848edc67490ffb02bfe144889491348c6e2a7baa42ae55395ab5f5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2RequestedNameidFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2SignRequest")
    def saml2_sign_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2SignRequest"))

    @saml2_sign_request.setter
    def saml2_sign_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d48137d19b361a9cdaffd6b1e177896e0eca1bbdb33d45a7aecf6ba38e7f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2SignRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeAcsUrl")
    def saml2_snowflake_acs_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2SnowflakeAcsUrl"))

    @saml2_snowflake_acs_url.setter
    def saml2_snowflake_acs_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680c313ab0ac41da03f1b4c361dba3162ab41e21b9dd3ce7d28dfc143d5dc843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2SnowflakeAcsUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeIssuerUrl")
    def saml2_snowflake_issuer_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2SnowflakeIssuerUrl"))

    @saml2_snowflake_issuer_url.setter
    def saml2_snowflake_issuer_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a1917e17c0b0201e753f2b2e26436525123eecd13e12a3e083e81d16e59405c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2SnowflakeIssuerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2SpInitiatedLoginPageLabel")
    def saml2_sp_initiated_login_page_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2SpInitiatedLoginPageLabel"))

    @saml2_sp_initiated_login_page_label.setter
    def saml2_sp_initiated_login_page_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e924546471783e5816cff5fb27639a4c6198a9f62845298214af93ba0294266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2SpInitiatedLoginPageLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2SsoUrl")
    def saml2_sso_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2SsoUrl"))

    @saml2_sso_url.setter
    def saml2_sso_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503e185d5aa9d0329d21ee23a302120fc388c00d9895ea58e3815f4538be9358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2SsoUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saml2X509Cert")
    def saml2_x509_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saml2X509Cert"))

    @saml2_x509_cert.setter
    def saml2_x509_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8399c25fade5c35ca2d66826a86a8dbc2bb430cb4b09d132f0b0a503f1a2f67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saml2X509Cert", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationConfig",
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
        "saml2_issuer": "saml2Issuer",
        "saml2_provider": "saml2Provider",
        "saml2_sso_url": "saml2SsoUrl",
        "saml2_x509_cert": "saml2X509Cert",
        "allowed_email_patterns": "allowedEmailPatterns",
        "allowed_user_domains": "allowedUserDomains",
        "comment": "comment",
        "enabled": "enabled",
        "id": "id",
        "saml2_enable_sp_initiated": "saml2EnableSpInitiated",
        "saml2_force_authn": "saml2ForceAuthn",
        "saml2_post_logout_redirect_url": "saml2PostLogoutRedirectUrl",
        "saml2_requested_nameid_format": "saml2RequestedNameidFormat",
        "saml2_sign_request": "saml2SignRequest",
        "saml2_snowflake_acs_url": "saml2SnowflakeAcsUrl",
        "saml2_snowflake_issuer_url": "saml2SnowflakeIssuerUrl",
        "saml2_sp_initiated_login_page_label": "saml2SpInitiatedLoginPageLabel",
    },
)
class Saml2IntegrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        saml2_issuer: builtins.str,
        saml2_provider: builtins.str,
        saml2_sso_url: builtins.str,
        saml2_x509_cert: builtins.str,
        allowed_email_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_user_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        saml2_enable_sp_initiated: typing.Optional[builtins.str] = None,
        saml2_force_authn: typing.Optional[builtins.str] = None,
        saml2_post_logout_redirect_url: typing.Optional[builtins.str] = None,
        saml2_requested_nameid_format: typing.Optional[builtins.str] = None,
        saml2_sign_request: typing.Optional[builtins.str] = None,
        saml2_snowflake_acs_url: typing.Optional[builtins.str] = None,
        saml2_snowflake_issuer_url: typing.Optional[builtins.str] = None,
        saml2_sp_initiated_login_page_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Specifies the name of the SAML2 integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#name Saml2Integration#name}
        :param saml2_issuer: The string containing the IdP EntityID / Issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_issuer Saml2Integration#saml2_issuer}
        :param saml2_provider: The string describing the IdP. Valid options are: ``OKTA`` | ``ADFS`` | ``CUSTOM``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_provider Saml2Integration#saml2_provider}
        :param saml2_sso_url: The string containing the IdP SSO URL, where the user should be redirected by Snowflake (the Service Provider) with a SAML AuthnRequest message. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_sso_url Saml2Integration#saml2_sso_url}
        :param saml2_x509_cert: The Base64 encoded IdP signing certificate on a single line without the leading -----BEGIN CERTIFICATE----- and ending -----END CERTIFICATE----- markers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_x509_cert Saml2Integration#saml2_x509_cert}
        :param allowed_email_patterns: A list of regular expressions that email addresses are matched against to authenticate with a SAML2 security integration. If this field changes value from non-empty to empty, the whole resource is recreated because of Snowflake limitations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#allowed_email_patterns Saml2Integration#allowed_email_patterns}
        :param allowed_user_domains: A list of email domains that can authenticate with a SAML2 security integration. If this field changes value from non-empty to empty, the whole resource is recreated because of Snowflake limitations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#allowed_user_domains Saml2Integration#allowed_user_domains}
        :param comment: Specifies a comment for the integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#comment Saml2Integration#comment}
        :param enabled: Specifies whether this security integration is enabled or disabled. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#enabled Saml2Integration#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#id Saml2Integration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param saml2_enable_sp_initiated: The Boolean indicating if the Log In With button will be shown on the login page. TRUE: displays the Log in With button on the login page. FALSE: does not display the Log in With button on the login page. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_enable_sp_initiated Saml2Integration#saml2_enable_sp_initiated}
        :param saml2_force_authn: The Boolean indicating whether users, during the initial authentication flow, are forced to authenticate again to access Snowflake. When set to TRUE, Snowflake sets the ForceAuthn SAML parameter to TRUE in the outgoing request from Snowflake to the identity provider. TRUE: forces users to authenticate again to access Snowflake, even if a valid session with the identity provider exists. FALSE: does not force users to authenticate again to access Snowflake. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_force_authn Saml2Integration#saml2_force_authn}
        :param saml2_post_logout_redirect_url: The endpoint to which Snowflake redirects users after clicking the Log Out button in the classic Snowflake web interface. Snowflake terminates the Snowflake session upon redirecting to the specified endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_post_logout_redirect_url Saml2Integration#saml2_post_logout_redirect_url}
        :param saml2_requested_nameid_format: The SAML NameID format allows Snowflake to set an expectation of the identifying attribute of the user (i.e. SAML Subject) in the SAML assertion from the IdP to ensure a valid authentication to Snowflake. Valid options are: ``urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified`` | ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`` | ``urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName`` | ``urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName`` | ``urn:oasis:names:tc:SAML:2.0:nameid-format:kerberos`` | ``urn:oasis:names:tc:SAML:2.0:nameid-format:persistent`` | ``urn:oasis:names:tc:SAML:2.0:nameid-format:transient``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_requested_nameid_format Saml2Integration#saml2_requested_nameid_format}
        :param saml2_sign_request: The Boolean indicating whether SAML requests are signed. TRUE: allows SAML requests to be signed. FALSE: does not allow SAML requests to be signed. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_sign_request Saml2Integration#saml2_sign_request}
        :param saml2_snowflake_acs_url: The string containing the Snowflake Assertion Consumer Service URL to which the IdP will send its SAML authentication response back to Snowflake. This property will be set in the SAML authentication request generated by Snowflake when initiating a SAML SSO operation with the IdP. If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use. Because Okta does not support underscores in URLs, the underscore in the account name must be converted to a hyphen. See `docs <https://docs.snowflake.com/en/user-guide/organizations-connect#okta-urls>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_snowflake_acs_url Saml2Integration#saml2_snowflake_acs_url}
        :param saml2_snowflake_issuer_url: The string containing the EntityID / Issuer for the Snowflake service provider. If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use. Because Okta does not support underscores in URLs, the underscore in the account name must be converted to a hyphen. See `docs <https://docs.snowflake.com/en/user-guide/organizations-connect#okta-urls>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_snowflake_issuer_url Saml2Integration#saml2_snowflake_issuer_url}
        :param saml2_sp_initiated_login_page_label: The string containing the label to display after the Log In With button on the login page. If this field changes value from non-empty to empty, the whole resource is recreated because of Snowflake limitations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_sp_initiated_login_page_label Saml2Integration#saml2_sp_initiated_login_page_label}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c902fdcbbacc332cc7ce8649e6f43e9dc9fa05377cb476e6b64d84133d3df61)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument saml2_issuer", value=saml2_issuer, expected_type=type_hints["saml2_issuer"])
            check_type(argname="argument saml2_provider", value=saml2_provider, expected_type=type_hints["saml2_provider"])
            check_type(argname="argument saml2_sso_url", value=saml2_sso_url, expected_type=type_hints["saml2_sso_url"])
            check_type(argname="argument saml2_x509_cert", value=saml2_x509_cert, expected_type=type_hints["saml2_x509_cert"])
            check_type(argname="argument allowed_email_patterns", value=allowed_email_patterns, expected_type=type_hints["allowed_email_patterns"])
            check_type(argname="argument allowed_user_domains", value=allowed_user_domains, expected_type=type_hints["allowed_user_domains"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument saml2_enable_sp_initiated", value=saml2_enable_sp_initiated, expected_type=type_hints["saml2_enable_sp_initiated"])
            check_type(argname="argument saml2_force_authn", value=saml2_force_authn, expected_type=type_hints["saml2_force_authn"])
            check_type(argname="argument saml2_post_logout_redirect_url", value=saml2_post_logout_redirect_url, expected_type=type_hints["saml2_post_logout_redirect_url"])
            check_type(argname="argument saml2_requested_nameid_format", value=saml2_requested_nameid_format, expected_type=type_hints["saml2_requested_nameid_format"])
            check_type(argname="argument saml2_sign_request", value=saml2_sign_request, expected_type=type_hints["saml2_sign_request"])
            check_type(argname="argument saml2_snowflake_acs_url", value=saml2_snowflake_acs_url, expected_type=type_hints["saml2_snowflake_acs_url"])
            check_type(argname="argument saml2_snowflake_issuer_url", value=saml2_snowflake_issuer_url, expected_type=type_hints["saml2_snowflake_issuer_url"])
            check_type(argname="argument saml2_sp_initiated_login_page_label", value=saml2_sp_initiated_login_page_label, expected_type=type_hints["saml2_sp_initiated_login_page_label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "saml2_issuer": saml2_issuer,
            "saml2_provider": saml2_provider,
            "saml2_sso_url": saml2_sso_url,
            "saml2_x509_cert": saml2_x509_cert,
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
        if allowed_email_patterns is not None:
            self._values["allowed_email_patterns"] = allowed_email_patterns
        if allowed_user_domains is not None:
            self._values["allowed_user_domains"] = allowed_user_domains
        if comment is not None:
            self._values["comment"] = comment
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if saml2_enable_sp_initiated is not None:
            self._values["saml2_enable_sp_initiated"] = saml2_enable_sp_initiated
        if saml2_force_authn is not None:
            self._values["saml2_force_authn"] = saml2_force_authn
        if saml2_post_logout_redirect_url is not None:
            self._values["saml2_post_logout_redirect_url"] = saml2_post_logout_redirect_url
        if saml2_requested_nameid_format is not None:
            self._values["saml2_requested_nameid_format"] = saml2_requested_nameid_format
        if saml2_sign_request is not None:
            self._values["saml2_sign_request"] = saml2_sign_request
        if saml2_snowflake_acs_url is not None:
            self._values["saml2_snowflake_acs_url"] = saml2_snowflake_acs_url
        if saml2_snowflake_issuer_url is not None:
            self._values["saml2_snowflake_issuer_url"] = saml2_snowflake_issuer_url
        if saml2_sp_initiated_login_page_label is not None:
            self._values["saml2_sp_initiated_login_page_label"] = saml2_sp_initiated_login_page_label

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
        '''Specifies the name of the SAML2 integration.

        This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#name Saml2Integration#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def saml2_issuer(self) -> builtins.str:
        '''The string containing the IdP EntityID / Issuer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_issuer Saml2Integration#saml2_issuer}
        '''
        result = self._values.get("saml2_issuer")
        assert result is not None, "Required property 'saml2_issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def saml2_provider(self) -> builtins.str:
        '''The string describing the IdP. Valid options are: ``OKTA`` | ``ADFS`` | ``CUSTOM``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_provider Saml2Integration#saml2_provider}
        '''
        result = self._values.get("saml2_provider")
        assert result is not None, "Required property 'saml2_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def saml2_sso_url(self) -> builtins.str:
        '''The string containing the IdP SSO URL, where the user should be redirected by Snowflake (the Service Provider) with a SAML AuthnRequest message.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_sso_url Saml2Integration#saml2_sso_url}
        '''
        result = self._values.get("saml2_sso_url")
        assert result is not None, "Required property 'saml2_sso_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def saml2_x509_cert(self) -> builtins.str:
        '''The Base64 encoded IdP signing certificate on a single line without the leading -----BEGIN CERTIFICATE----- and ending -----END CERTIFICATE----- markers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_x509_cert Saml2Integration#saml2_x509_cert}
        '''
        result = self._values.get("saml2_x509_cert")
        assert result is not None, "Required property 'saml2_x509_cert' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_email_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of regular expressions that email addresses are matched against to authenticate with a SAML2 security integration.

        If this field changes value from non-empty to empty, the whole resource is recreated because of Snowflake limitations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#allowed_email_patterns Saml2Integration#allowed_email_patterns}
        '''
        result = self._values.get("allowed_email_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_user_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of email domains that can authenticate with a SAML2 security integration.

        If this field changes value from non-empty to empty, the whole resource is recreated because of Snowflake limitations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#allowed_user_domains Saml2Integration#allowed_user_domains}
        '''
        result = self._values.get("allowed_user_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#comment Saml2Integration#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.str]:
        '''Specifies whether this security integration is enabled or disabled.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#enabled Saml2Integration#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#id Saml2Integration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml2_enable_sp_initiated(self) -> typing.Optional[builtins.str]:
        '''The Boolean indicating if the Log In With button will be shown on the login page.

        TRUE: displays the Log in With button on the login page. FALSE: does not display the Log in With button on the login page. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_enable_sp_initiated Saml2Integration#saml2_enable_sp_initiated}
        '''
        result = self._values.get("saml2_enable_sp_initiated")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml2_force_authn(self) -> typing.Optional[builtins.str]:
        '''The Boolean indicating whether users, during the initial authentication flow, are forced to authenticate again to access Snowflake.

        When set to TRUE, Snowflake sets the ForceAuthn SAML parameter to TRUE in the outgoing request from Snowflake to the identity provider. TRUE: forces users to authenticate again to access Snowflake, even if a valid session with the identity provider exists. FALSE: does not force users to authenticate again to access Snowflake. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_force_authn Saml2Integration#saml2_force_authn}
        '''
        result = self._values.get("saml2_force_authn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml2_post_logout_redirect_url(self) -> typing.Optional[builtins.str]:
        '''The endpoint to which Snowflake redirects users after clicking the Log Out button in the classic Snowflake web interface.

        Snowflake terminates the Snowflake session upon redirecting to the specified endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_post_logout_redirect_url Saml2Integration#saml2_post_logout_redirect_url}
        '''
        result = self._values.get("saml2_post_logout_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml2_requested_nameid_format(self) -> typing.Optional[builtins.str]:
        '''The SAML NameID format allows Snowflake to set an expectation of the identifying attribute of the user (i.e. SAML Subject) in the SAML assertion from the IdP to ensure a valid authentication to Snowflake. Valid options are: ``urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified`` | ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`` | ``urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName`` | ``urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName`` | ``urn:oasis:names:tc:SAML:2.0:nameid-format:kerberos`` | ``urn:oasis:names:tc:SAML:2.0:nameid-format:persistent`` | ``urn:oasis:names:tc:SAML:2.0:nameid-format:transient``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_requested_nameid_format Saml2Integration#saml2_requested_nameid_format}
        '''
        result = self._values.get("saml2_requested_nameid_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml2_sign_request(self) -> typing.Optional[builtins.str]:
        '''The Boolean indicating whether SAML requests are signed.

        TRUE: allows SAML requests to be signed. FALSE: does not allow SAML requests to be signed. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_sign_request Saml2Integration#saml2_sign_request}
        '''
        result = self._values.get("saml2_sign_request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml2_snowflake_acs_url(self) -> typing.Optional[builtins.str]:
        '''The string containing the Snowflake Assertion Consumer Service URL to which the IdP will send its SAML authentication response back to Snowflake.

        This property will be set in the SAML authentication request generated by Snowflake when initiating a SAML SSO operation with the IdP. If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use. Because Okta does not support underscores in URLs, the underscore in the account name must be converted to a hyphen. See `docs <https://docs.snowflake.com/en/user-guide/organizations-connect#okta-urls>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_snowflake_acs_url Saml2Integration#saml2_snowflake_acs_url}
        '''
        result = self._values.get("saml2_snowflake_acs_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml2_snowflake_issuer_url(self) -> typing.Optional[builtins.str]:
        '''The string containing the EntityID / Issuer for the Snowflake service provider.

        If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use. Because Okta does not support underscores in URLs, the underscore in the account name must be converted to a hyphen. See `docs <https://docs.snowflake.com/en/user-guide/organizations-connect#okta-urls>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_snowflake_issuer_url Saml2Integration#saml2_snowflake_issuer_url}
        '''
        result = self._values.get("saml2_snowflake_issuer_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml2_sp_initiated_login_page_label(self) -> typing.Optional[builtins.str]:
        '''The string containing the label to display after the Log In With button on the login page.

        If this field changes value from non-empty to empty, the whole resource is recreated because of Snowflake limitations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/saml2_integration#saml2_sp_initiated_login_page_label Saml2Integration#saml2_sp_initiated_login_page_label}
        '''
        result = self._values.get("saml2_sp_initiated_login_page_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputAllowedEmailPatterns",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputAllowedEmailPatterns:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputAllowedEmailPatterns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputAllowedEmailPatternsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputAllowedEmailPatternsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96205f7ab62459d54ec9e1107c6696f26290f668f1d96349130d0e742ba20035)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputAllowedEmailPatternsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266b8bb04829d4c5412617098067776316b246c8757808f32a8ae5e4792b8fef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputAllowedEmailPatternsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9c98e4f93350ad3ea9aa93557ab6931ccf5fcbd130877ace725f657a93321b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a305e20580eac6a5ab073afcf99490beef806eca15f60efc71a24c9355490839)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1784f6acb95be25cac9f1ea6576187ab59526815fe2f21b67c31434f478bbc46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputAllowedEmailPatternsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputAllowedEmailPatternsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb61fb1ab8dd0cad71df6bcba7612e2938b76ccd79074a9e91cc2200c15abc84)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputAllowedEmailPatterns]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputAllowedEmailPatterns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputAllowedEmailPatterns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2857586af6a1d6baed2773a0df1907fa243b24f79f20800a79e341171d87cccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputAllowedUserDomains",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputAllowedUserDomains:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputAllowedUserDomains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputAllowedUserDomainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputAllowedUserDomainsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9cb2c119a35f3853e3c894ffaa24414efeb42103b952fcb9aa4f92606ebe032)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputAllowedUserDomainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ed99c1fad99f74d80cfb226911e41008faee8ebed295b76daa39c8db281ef7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputAllowedUserDomainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63741088000e1805e4e3cb6f36c7edfabc59fd6eabc20a78357e842ea9e3bc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc4db25ada69e8aa312bfdd543630f28b125fbbca72f67c80579d6398e9aab33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7b1d3b09a6d2713587ce8bac332a6c0a573db9a568ac3706601a32ba7614b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputAllowedUserDomainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputAllowedUserDomainsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__715c0d39ac9f47090b06e8e7e313661b4d848e6d305c35fcaa9b3eabe064b0b2)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputAllowedUserDomains]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputAllowedUserDomains], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputAllowedUserDomains],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50696c5eb2d1829056d1cd0c639ab64f1e8bd2de98aa8ce58395aa70c8e357a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputComment",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputComment:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputComment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputCommentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputCommentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b10a83561000bc0487c415b1a63ad2b78de4f19d981f8145d63cb81f2013789f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputCommentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd0fbb4c4823a48b15c9a90971490cea181372d13ab98a348f732f3ed0fb602)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputCommentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24416bb8b0634eaa2a3eb27c28d18d09a9ce06170c8a49489d95c7b271d31ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6b49aceea9199ce3d7961b673864cfdc6efb328aabfbf2db2c83d9964d5ef5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23c49346753d72362407de6a24c1f0b183f36557a086f11ed8591ed6c0795e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputCommentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputCommentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__009bad3dfe0c8633c12ce5431e0eebfd289ce8a15d0e1e2af600874cb0f5fbce)
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
    def internal_value(self) -> typing.Optional[Saml2IntegrationDescribeOutputComment]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputComment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputComment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40ec14bf5486f5d4e454bd27fdd5c212419c8657976c596b9e4e01e5ece299c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b4e18ecf1967640ef66da49a7423bdf495f08db786b006f6aa34ddd6debd3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebed1fb927cbf73be136de8ae40adf658f9f2647f6db26b888108967c72311a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6724e7eccb10c4d5ed44fbe437dc99edc4bd62bbbe8add52cd2b70dab933ef74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fff9532ba25614facac65e3fbf6ea9361ac7fcfb5d68c0ded5622e26dfa6504)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0a439abcadbb404b79c10a8dc06f36b4ca105cf52af5e70b9983e8cfa394144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b53e141bb470b10175a3a926521d05b95359aecd8a20236a48fe8599e7c72e87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedEmailPatterns")
    def allowed_email_patterns(
        self,
    ) -> Saml2IntegrationDescribeOutputAllowedEmailPatternsList:
        return typing.cast(Saml2IntegrationDescribeOutputAllowedEmailPatternsList, jsii.get(self, "allowedEmailPatterns"))

    @builtins.property
    @jsii.member(jsii_name="allowedUserDomains")
    def allowed_user_domains(
        self,
    ) -> Saml2IntegrationDescribeOutputAllowedUserDomainsList:
        return typing.cast(Saml2IntegrationDescribeOutputAllowedUserDomainsList, jsii.get(self, "allowedUserDomains"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> Saml2IntegrationDescribeOutputCommentList:
        return typing.cast(Saml2IntegrationDescribeOutputCommentList, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="saml2DigestMethodsUsed")
    def saml2_digest_methods_used(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedList", jsii.get(self, "saml2DigestMethodsUsed"))

    @builtins.property
    @jsii.member(jsii_name="saml2EnableSpInitiated")
    def saml2_enable_sp_initiated(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedList", jsii.get(self, "saml2EnableSpInitiated"))

    @builtins.property
    @jsii.member(jsii_name="saml2ForceAuthn")
    def saml2_force_authn(self) -> "Saml2IntegrationDescribeOutputSaml2ForceAuthnList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2ForceAuthnList", jsii.get(self, "saml2ForceAuthn"))

    @builtins.property
    @jsii.member(jsii_name="saml2Issuer")
    def saml2_issuer(self) -> "Saml2IntegrationDescribeOutputSaml2IssuerList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2IssuerList", jsii.get(self, "saml2Issuer"))

    @builtins.property
    @jsii.member(jsii_name="saml2PostLogoutRedirectUrl")
    def saml2_post_logout_redirect_url(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlList", jsii.get(self, "saml2PostLogoutRedirectUrl"))

    @builtins.property
    @jsii.member(jsii_name="saml2Provider")
    def saml2_provider(self) -> "Saml2IntegrationDescribeOutputSaml2ProviderList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2ProviderList", jsii.get(self, "saml2Provider"))

    @builtins.property
    @jsii.member(jsii_name="saml2RequestedNameidFormat")
    def saml2_requested_nameid_format(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatList", jsii.get(self, "saml2RequestedNameidFormat"))

    @builtins.property
    @jsii.member(jsii_name="saml2SignatureMethodsUsed")
    def saml2_signature_methods_used(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedList", jsii.get(self, "saml2SignatureMethodsUsed"))

    @builtins.property
    @jsii.member(jsii_name="saml2SignRequest")
    def saml2_sign_request(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2SignRequestList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SignRequestList", jsii.get(self, "saml2SignRequest"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeAcsUrl")
    def saml2_snowflake_acs_url(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlList", jsii.get(self, "saml2SnowflakeAcsUrl"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeIssuerUrl")
    def saml2_snowflake_issuer_url(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlList", jsii.get(self, "saml2SnowflakeIssuerUrl"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeMetadata")
    def saml2_snowflake_metadata(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataList", jsii.get(self, "saml2SnowflakeMetadata"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeX509Cert")
    def saml2_snowflake_x509_cert(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertList", jsii.get(self, "saml2SnowflakeX509Cert"))

    @builtins.property
    @jsii.member(jsii_name="saml2SpInitiatedLoginPageLabel")
    def saml2_sp_initiated_login_page_label(
        self,
    ) -> "Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelList", jsii.get(self, "saml2SpInitiatedLoginPageLabel"))

    @builtins.property
    @jsii.member(jsii_name="saml2SsoUrl")
    def saml2_sso_url(self) -> "Saml2IntegrationDescribeOutputSaml2SsoUrlList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SsoUrlList", jsii.get(self, "saml2SsoUrl"))

    @builtins.property
    @jsii.member(jsii_name="saml2X509Cert")
    def saml2_x509_cert(self) -> "Saml2IntegrationDescribeOutputSaml2X509CertList":
        return typing.cast("Saml2IntegrationDescribeOutputSaml2X509CertList", jsii.get(self, "saml2X509Cert"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Saml2IntegrationDescribeOutput]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0abb25ae1cac5d4d9323a0ff39d2421447a69997fa991f2d6b9977d111d762b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2DigestMethodsUsed",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2DigestMethodsUsed:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2DigestMethodsUsed(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4a4ae1904873a6815aa01ffa99e49ed22efe53a089cb15c94cb087693bad66d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6e05d685197e219d6c62714eca368838d07922d0f792221bf126cf8afebd61)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36ddee1612ecc2a18fe0e79162df530bb6900a86254d4fb32c52815d0b2ea36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dcbd76bd481f75369ef6a13a15a6d08713138ec6535a38ac6c30c72b0eeba4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__390c8fef40db90d6e7d5d3f4ff0443a4ded3f6279e6d64168bff16e8559b17e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__977a71990a4bd4e1e00d402203e75ad5c073e8d9950d8106474093adced2cfe3)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2DigestMethodsUsed]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2DigestMethodsUsed], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2DigestMethodsUsed],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767f3ae4a2aaa940d37b9c98f112629fcc0ea315654e6409e67d08bb2f285bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2EnableSpInitiated",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2EnableSpInitiated:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2EnableSpInitiated(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b02886fcf0d956e3e7ac73f740e7c14367f18f7859f7e416adf95b5e1d1b62d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b067f43c8433d035a7dc8edba743e302e8b8a35feaab49ee9a6d918891d2ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__508784853c6640e90122c42cc64363bbb79e56ac7fc3d11684dbcf09b418b97e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c022aaf64633e49bf9bd21d2472592a3f857733dfa89d3d93d82c073cd07a9f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb3e69c604d5375d20eeb36a7e74fa8a2c87f665852cf94ca07476e1e23c8d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3748d1e99e9ac623740d54b36488b1676b928d9225b56b847128edf9f765bf36)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2EnableSpInitiated]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2EnableSpInitiated], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2EnableSpInitiated],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__952d690a264469f2b94d163952f1d8ecca85f7334757d2855e23827561a332b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2ForceAuthn",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2ForceAuthn:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2ForceAuthn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2ForceAuthnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2ForceAuthnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__969a684d5862c9a37bdf4fe351f8c7d58c658352f7414a3a51ab4a5641150029)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2ForceAuthnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e28e68376c1e5d9d2d294b265d9710ccfac77c1929d103488f668174c25b47b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2ForceAuthnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64433ef4b0d525b4bd6d2b57fa83c7e3893c9890c5881823d12f777048ef92e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00aa86cda1d74c84c01dc8b5f67501f327a55a05a8877451679a74fe03772672)
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
            type_hints = typing.get_type_hints(_typecheckingstub__052c18965b6cf1f0aceff047f1eef481131900f3ecd3c51b6ae87f2c5613cd3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2ForceAuthnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2ForceAuthnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7918c65a157a2a394c12f90acfe439bfd6feb55fa532a4c2a57ad126c2a67a3a)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2ForceAuthn]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2ForceAuthn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2ForceAuthn],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b86fc54a2608c7f0d8b51509867163a7a40e477f58627dffcc55c0040b704f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2Issuer",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2Issuer:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2Issuer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2IssuerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2IssuerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c54eaa975a32948e6dda434053eb70a9d04845378187d1e98f71593381272086)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2IssuerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9dae95f4273cfd6b07d4fa42f189a19b229d4883cb27154ad6ad7e112515b0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2IssuerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa6bc83afa67429ba5a26bef3ce2c7d9600678586347feb6854b72c8d760c00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a243b5daeef28bafbc430330df5fc1b95e1cffefbd79f4aece11bb8320315f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11b76bb1ea9e68ecbba3094fdd6ff7944f9ac2d58632ee1b74660e25517e252f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2IssuerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2IssuerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__accff65f3f02c1bc84e76d54c16df76f2200fed588902025b852ef49f6f8255b)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2Issuer]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2Issuer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2Issuer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eebb53509329a8f780c0f744a150fb011f384bb389f8c8ad5791d8fd0c53ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cc574a66a6ea95b509fb8ca902c847f37447584081ea23abb47d1d9a5ad6344)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7945ec4e14ff764a33ef44cc0d9d804232def3e68e773b2d5cf0f158fe900d1b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b3e5bca5989f93aa1fd2904e2c56f7aa922a6d62770645d3f6be7ee1c139ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fb50b5814cf17bc1dec0e6482bdeb49f32a541d7e21caf4bdc7e2081f5c6457)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d585ec3133844c4d59631206da3beb8fdc90f335b68421639461c952a7ee78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8884d1457c5956d88df07e7818c527abdb036ba84bbf7c01bdc025cbfc84106)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrl]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87057b3d0d36faa16803bbd62d815bf6c7d23a205e8f2f670bac159680674713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2Provider",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2Provider:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2Provider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2ProviderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2ProviderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4617d5352423de045f77b275e0221f258fdb904bce666b76029ad4c8e7459fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2ProviderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c816f950e0fba6fdaa1133665c77e18945a0eb6cd0f0ea25397caa8fd54a08)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2ProviderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009effd4e6bb30b695de6cb601440b9e0a767c322858f7a762e8e1e42e761036)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b727e0b070bb4ca7373b98d3b04c47e85549a0dd009b8df7dcea5254cb7b81f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed32f22ac055d6a457d52140d13e9c112bf3ce978b0af7c8c7fd441d4f4b8a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2ProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2ProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__348857039b17903360b743a110b0a0e128240e58ff24fc3f1bee91eebcbc200b)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2Provider]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2Provider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2Provider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e041fe7ba225bb7bc399d0446801810d778d8f5ff09e53981ffa40616cea41b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2RequestedNameidFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2RequestedNameidFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2RequestedNameidFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__105e53043241a0140609fdea40d5e08873c40761a5c25e7dc1c7a562e57a00c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a97f168e68582ecbf5af3619b63adc0d763fd9cea97da97bf5223b565cded8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2aa06014ec79c69ef0d592c319d62eac83c4b639f6a871b7ff04b1d846bc6b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d785afcdec3262b186a9d5ed79c70c96333bb3f9baacc8943b8a581cf17ee4a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9c66af54091d41dd5b88a92eaff4a2b084022e571654bed219255aad70f2e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba2a9cbe20553df8c42c28a8c1429f8fd15264136101cc4918b0e12e4beb77bc)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2RequestedNameidFormat]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2RequestedNameidFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2RequestedNameidFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e26d1edde15a28b786f8f84e52402dd57d7c0746ec498e0cdf31e3f3772e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SignRequest",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2SignRequest:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2SignRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2SignRequestList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SignRequestList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__031b3bbac5f8ae0f2e94b4d5cf724be041652e7f2f0c1c338bc2500ec3e1c3cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2SignRequestOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3faf07637b4aced6096b8b41e468fddd0583c3efe38ab3e149d20732dd1eccfc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SignRequestOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e2e00fc03c8a00830d615aec805786cc05b0a6210a26cbcacbc3ebe053cd12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95b36d2852a69981bfde0c7a80e0cbe0e8c425900479b36859096850df7dffa1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4a9d3631f1a9a54432dd93cafcdb17a28ee4348bd60e10f8026fc94031ad8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2SignRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SignRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e069e51939dd4228d0c235ecafdf62cfc96efb263fa0d3c5183313aa8297236)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2SignRequest]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2SignRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SignRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9f59782181ccf3467ebf9b3a72a165d9080668e39638b60f9b8ec8037b6e2e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsed",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsed:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsed(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14e8c2c2fe7c1d57009bf53af98cd854fc2556c682c5f31b0123e2b625138479)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1177873757d51c280cb95163082e2ddb59008ab1496aae8853b1fa39e32e312)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41cd3409cf4a7d1156f46f603f1a1dc01394243126eef26c0fbaba32231f2d33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fca3d230f3f6afccd58d2bea48427c7b17542553f3dfa5899902fa9d870c1faf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06568790bc63dd2457a108f94d174611cbc61774b4ac4682c4494f5128192022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f1527c3deafa84fc1b757f993436235b560f98a387ed4ef5ee32ba03a32a013)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsed]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsed], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsed],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494843a7aaca39c4b6703c778eb849a2b17e52425cd5c7ff32ae161f65d43c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d6c33bdd742114627cc41d56c4ecd97a583d81177e729826016f0334345229c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af35d6c1bf29a548e2b9f62e1e2f71f903210aece1e6195206f2011e0113aa2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874cee0bf30d9bdfede4c447a148560a76d84401574ddcd6623f264b417cceb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f222f1de1beb8d649421660cd63356039db8cc202601d1a9bfc0c738ef08325)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3db50c8272887cf1a732b417b06d4b28a8aa43a736420a94300fbff68356bbc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de1ee287b52fb60df95f018ce9006b88b0b493f0867dcfb453393f42b8ce8037)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrl]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6046618571b4ebf840d12a1b9765d2c333378fb41ac5706112e4c7ecfb632c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39c659be8ec982e7058dfc776c143ad5d37f9f8ba03b414f374e386918afc1c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e46259f6439641523f8a724ee07c109b200a142fae0b8fbd2b7124803d8afb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb1b66b42364317245a0202e6aa4741ccb3d1d1f98d4e838a1f1ec1b328499c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e6387cf2f29a41fd4ff52aee2b0f2f5bdeb25915b75d9a6610a1e283730fca2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78f2fae3be460ad89fdafc245ac4d64c5d6d1a20c3cea902fe6be2f29de0fe09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd5e2faf885488db2e225d52641c51c15fd75fb5e3c23399c5e9e19b67d5f703)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrl]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b959469e68115f5ca3f0a86d1cb6e01d1a4765d64851753edf9c2472c5cf3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeMetadata",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2SnowflakeMetadata:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2SnowflakeMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d33f56e9ee8c24da1612418de5cdf7d6bf7dac39c2e3f37e3da1a94c5dc8eb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abcf1c39d2edd41c73f2887d91de6003aaf1278020c310f94ebee81a07d553d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c0cfbd36ae267433603cc6c5f19801ed6cc70c76e6449fb1405b7c3cc7617f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd9f98659ef118b4a423351dae4b43670cedb99138fef60c5b4a5366a574a449)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3b9b8c96b3608489e13caaa379f1a7be66b26553fb75f9afdba2a5ac493769c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42e9d1fdce64b93aee106bb068f9417a1f6fbe22481c91e39c4a12bc34c7e5ff)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeMetadata]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467f4dcfb5dd945b553838820ef459d6966f189678d2089e5b55bbb22476b2a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeX509Cert",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2SnowflakeX509Cert:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2SnowflakeX509Cert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79949d0bf6b2457405a8829405ebaead7f7317f14eaf21814af97d80da581e74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b60bf906104d4f7a9b85eaa3811f9badb8c783662c2e6a54087d39ff7b99ad6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4796bde66b10fa0b123c3b60dd328fb4d8b6f9662177269c4d05aff536120fd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1231fe6e4a2ca3db877e17128ca08571c441f8f39c521284e3930ea3b6af7a64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__542fec1e148a640369edfc38f10141c19fe3395d1797f7209d5c76cc987b6d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63216722a4bb1297b9051e5e06da0ef19784e9d2a997082ad2a81489001b3809)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeX509Cert]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeX509Cert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeX509Cert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3025db470d884be7aa9d7549fcd0cc4e4cfdd04c92c5f856e37f9b773172bc3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabel",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c968913fc13b38e076259d9e2b0c67d6bc304e9e0cf754cd67f448c6677e1ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd401c013501477b2a9c523c0b5100aac1220362810bef4865664a485a2971f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270b2035eeb5bda8d38dcbddbe551dceff2027b4902dabc4fa4c5a4ee1e38ef1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e0bf5525adba9a5099b720b21d0266172c1659e464a0dd5e30242a01b4fde92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeeeca0e527420edd3fe839153eb98d2abab2e6f8ddb9f6ed6d9255a726932ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__246568f2177b4aa14fc64040de61d01d44b99d689f08ef61471791841da44a02)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabel]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7941c68e53a6cea563f84c6133dbe1076c4ca9500732aa906ef8ab8e14a11fee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SsoUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2SsoUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2SsoUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2SsoUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SsoUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94a4467790cd091dd81b35e0a0a87e085bdbe6b97df4713fefdbb6765d7dcbb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2SsoUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f1b75ba1738c89119ea0ff14d3eabf0a63175b3b6c0bc3aaf954c01f2f5132)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2SsoUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d785fea32031494ccc13f60bd43cb4086d3a3784473ec13a6a19cae2497446aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3eb232cfe0518b98ee285e65f2eb19e3ffbebe93cb5019dee1c75f53d8ce53b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9e00b5a02c2c2b8ac4683197f518e4615b9d972855d7298ac40cf110293d66c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2SsoUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2SsoUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c88ac34787c153ae79960562d30587b25def1b771d4083c3825796aeb1116015)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2SsoUrl]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2SsoUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SsoUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ad2070f5a7a3be45b1cf3410bceb910ea429a52361a99cfee0748abaacb00f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2X509Cert",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationDescribeOutputSaml2X509Cert:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationDescribeOutputSaml2X509Cert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationDescribeOutputSaml2X509CertList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2X509CertList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d285dd74bd0190ec137338d7a57776bd27a96d4ebe699813cf2090e9a8be6d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Saml2IntegrationDescribeOutputSaml2X509CertOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8346bffc201b6bc9b3ad6b23886a9cb16d37808cc0ebf9762aa8309c9d093f0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationDescribeOutputSaml2X509CertOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7969d5572e5e3e62560c18f290ec0e54705ab758a0e539152589257cb99bf09b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b7e757a56a138f84abf101aae9031b09f098125dd53ba56562a6b3fc4657b31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af0e24350e35a6739f4919fdf4fc4249f5944c097620f3e3643afd46edaa08ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationDescribeOutputSaml2X509CertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationDescribeOutputSaml2X509CertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cd5a6010102d5b7a1d0c9041c098bcff0ece561b0e249287d03729fe0469ac8)
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
    ) -> typing.Optional[Saml2IntegrationDescribeOutputSaml2X509Cert]:
        return typing.cast(typing.Optional[Saml2IntegrationDescribeOutputSaml2X509Cert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationDescribeOutputSaml2X509Cert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c9d71ed67f13f45a2fd0da26e08b3c376c6f0ba9da0ffbd8b56d1ff0d0087c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class Saml2IntegrationShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Saml2IntegrationShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Saml2IntegrationShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa30480b81964c652aa853b03435cc6e6e9e39b56cde25fc4cbaf190ced4e512)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "Saml2IntegrationShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8215afa490e71b9732aa9046c84ad7a8331a3667f38e79f491693ae2ca20e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Saml2IntegrationShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f00783916ecde791dc6ad6db57d0aecd4659716d8ebdea1e02ff3e42585fed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ace96bbdc40c2ae7e53c7b45fef0a9b3805e006acaf85e1cc093c64f423f5d8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3ba56361469a78a50e1989552e229d1f8d427619a6359cd0c7b07be6217e222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Saml2IntegrationShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.saml2Integration.Saml2IntegrationShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d14eb662653fa0e7c0a802d8b3377f055bf385e637eb870b25ae140c62072b9)
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
    def internal_value(self) -> typing.Optional[Saml2IntegrationShowOutput]:
        return typing.cast(typing.Optional[Saml2IntegrationShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Saml2IntegrationShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663ecd50f3dc127947608afd2b752da96dd62e19311d8702d71242c8bcfbc060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Saml2Integration",
    "Saml2IntegrationConfig",
    "Saml2IntegrationDescribeOutput",
    "Saml2IntegrationDescribeOutputAllowedEmailPatterns",
    "Saml2IntegrationDescribeOutputAllowedEmailPatternsList",
    "Saml2IntegrationDescribeOutputAllowedEmailPatternsOutputReference",
    "Saml2IntegrationDescribeOutputAllowedUserDomains",
    "Saml2IntegrationDescribeOutputAllowedUserDomainsList",
    "Saml2IntegrationDescribeOutputAllowedUserDomainsOutputReference",
    "Saml2IntegrationDescribeOutputComment",
    "Saml2IntegrationDescribeOutputCommentList",
    "Saml2IntegrationDescribeOutputCommentOutputReference",
    "Saml2IntegrationDescribeOutputList",
    "Saml2IntegrationDescribeOutputOutputReference",
    "Saml2IntegrationDescribeOutputSaml2DigestMethodsUsed",
    "Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedList",
    "Saml2IntegrationDescribeOutputSaml2DigestMethodsUsedOutputReference",
    "Saml2IntegrationDescribeOutputSaml2EnableSpInitiated",
    "Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedList",
    "Saml2IntegrationDescribeOutputSaml2EnableSpInitiatedOutputReference",
    "Saml2IntegrationDescribeOutputSaml2ForceAuthn",
    "Saml2IntegrationDescribeOutputSaml2ForceAuthnList",
    "Saml2IntegrationDescribeOutputSaml2ForceAuthnOutputReference",
    "Saml2IntegrationDescribeOutputSaml2Issuer",
    "Saml2IntegrationDescribeOutputSaml2IssuerList",
    "Saml2IntegrationDescribeOutputSaml2IssuerOutputReference",
    "Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrl",
    "Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlList",
    "Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrlOutputReference",
    "Saml2IntegrationDescribeOutputSaml2Provider",
    "Saml2IntegrationDescribeOutputSaml2ProviderList",
    "Saml2IntegrationDescribeOutputSaml2ProviderOutputReference",
    "Saml2IntegrationDescribeOutputSaml2RequestedNameidFormat",
    "Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatList",
    "Saml2IntegrationDescribeOutputSaml2RequestedNameidFormatOutputReference",
    "Saml2IntegrationDescribeOutputSaml2SignRequest",
    "Saml2IntegrationDescribeOutputSaml2SignRequestList",
    "Saml2IntegrationDescribeOutputSaml2SignRequestOutputReference",
    "Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsed",
    "Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedList",
    "Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsedOutputReference",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrl",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlList",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrlOutputReference",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrl",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlList",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrlOutputReference",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeMetadata",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataList",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeMetadataOutputReference",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeX509Cert",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertList",
    "Saml2IntegrationDescribeOutputSaml2SnowflakeX509CertOutputReference",
    "Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabel",
    "Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelList",
    "Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference",
    "Saml2IntegrationDescribeOutputSaml2SsoUrl",
    "Saml2IntegrationDescribeOutputSaml2SsoUrlList",
    "Saml2IntegrationDescribeOutputSaml2SsoUrlOutputReference",
    "Saml2IntegrationDescribeOutputSaml2X509Cert",
    "Saml2IntegrationDescribeOutputSaml2X509CertList",
    "Saml2IntegrationDescribeOutputSaml2X509CertOutputReference",
    "Saml2IntegrationShowOutput",
    "Saml2IntegrationShowOutputList",
    "Saml2IntegrationShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__02fdc4cab6eadc678f8e01b60c79e1ed28a085f458f6ee3ce536d1e2f73571e9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    saml2_issuer: builtins.str,
    saml2_provider: builtins.str,
    saml2_sso_url: builtins.str,
    saml2_x509_cert: builtins.str,
    allowed_email_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_user_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    saml2_enable_sp_initiated: typing.Optional[builtins.str] = None,
    saml2_force_authn: typing.Optional[builtins.str] = None,
    saml2_post_logout_redirect_url: typing.Optional[builtins.str] = None,
    saml2_requested_nameid_format: typing.Optional[builtins.str] = None,
    saml2_sign_request: typing.Optional[builtins.str] = None,
    saml2_snowflake_acs_url: typing.Optional[builtins.str] = None,
    saml2_snowflake_issuer_url: typing.Optional[builtins.str] = None,
    saml2_sp_initiated_login_page_label: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__e6d234d7cc8225f9f79e4111d55484297ce1681132be3d4ccd90c9f55cf4f169(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ee319e05c03cbe88c77cc5a9d80be94a61396aa401e758aac912f8a96ea16c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e332e6b254b7372161c524d6aae8bf23243541b5a9cc3d0fb25ebf0ffb5144(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194ef5fd70bea144ee936fd33f6c34963cf9dc492a47a5922ddc4604b77bc2a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5156a2c534b8a6c179aa9da3922f9516f76503c14cb8d192a0f0cc31caf82013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd2e0ad447f0d9858ea393ff27c5671f4cdecd1632c3d04b825f5c3f739e6b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748734633f50e0b07becae59b90e3f231d99edaee9e8efa30015958015e088cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd457c5411b9c6b0d1444f3009254628113cf29bc6d7ef2d45b56d4d3b1765ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e7e58fa0f6256789139538eefeb67405c2d8898719221a67a9dab79a8c1424(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983ae4d1c960d45eb021604b6ec2e2c964688029c79495b63e2c20eb0c28761e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d791527e043b8b8ea6d32d4c132d88d63afbe3ae673bc38b8402503fd57f2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a249a6b5028b91945077ee03a4dd9d6ba7b7155f11d89c04916bcdf0fba603(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22a4e162848edc67490ffb02bfe144889491348c6e2a7baa42ae55395ab5f5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d48137d19b361a9cdaffd6b1e177896e0eca1bbdb33d45a7aecf6ba38e7f8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680c313ab0ac41da03f1b4c361dba3162ab41e21b9dd3ce7d28dfc143d5dc843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1917e17c0b0201e753f2b2e26436525123eecd13e12a3e083e81d16e59405c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e924546471783e5816cff5fb27639a4c6198a9f62845298214af93ba0294266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503e185d5aa9d0329d21ee23a302120fc388c00d9895ea58e3815f4538be9358(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8399c25fade5c35ca2d66826a86a8dbc2bb430cb4b09d132f0b0a503f1a2f67e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c902fdcbbacc332cc7ce8649e6f43e9dc9fa05377cb476e6b64d84133d3df61(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    saml2_issuer: builtins.str,
    saml2_provider: builtins.str,
    saml2_sso_url: builtins.str,
    saml2_x509_cert: builtins.str,
    allowed_email_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_user_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    saml2_enable_sp_initiated: typing.Optional[builtins.str] = None,
    saml2_force_authn: typing.Optional[builtins.str] = None,
    saml2_post_logout_redirect_url: typing.Optional[builtins.str] = None,
    saml2_requested_nameid_format: typing.Optional[builtins.str] = None,
    saml2_sign_request: typing.Optional[builtins.str] = None,
    saml2_snowflake_acs_url: typing.Optional[builtins.str] = None,
    saml2_snowflake_issuer_url: typing.Optional[builtins.str] = None,
    saml2_sp_initiated_login_page_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96205f7ab62459d54ec9e1107c6696f26290f668f1d96349130d0e742ba20035(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266b8bb04829d4c5412617098067776316b246c8757808f32a8ae5e4792b8fef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9c98e4f93350ad3ea9aa93557ab6931ccf5fcbd130877ace725f657a93321b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a305e20580eac6a5ab073afcf99490beef806eca15f60efc71a24c9355490839(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1784f6acb95be25cac9f1ea6576187ab59526815fe2f21b67c31434f478bbc46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb61fb1ab8dd0cad71df6bcba7612e2938b76ccd79074a9e91cc2200c15abc84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2857586af6a1d6baed2773a0df1907fa243b24f79f20800a79e341171d87cccd(
    value: typing.Optional[Saml2IntegrationDescribeOutputAllowedEmailPatterns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cb2c119a35f3853e3c894ffaa24414efeb42103b952fcb9aa4f92606ebe032(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ed99c1fad99f74d80cfb226911e41008faee8ebed295b76daa39c8db281ef7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63741088000e1805e4e3cb6f36c7edfabc59fd6eabc20a78357e842ea9e3bc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4db25ada69e8aa312bfdd543630f28b125fbbca72f67c80579d6398e9aab33(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b1d3b09a6d2713587ce8bac332a6c0a573db9a568ac3706601a32ba7614b53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715c0d39ac9f47090b06e8e7e313661b4d848e6d305c35fcaa9b3eabe064b0b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50696c5eb2d1829056d1cd0c639ab64f1e8bd2de98aa8ce58395aa70c8e357a4(
    value: typing.Optional[Saml2IntegrationDescribeOutputAllowedUserDomains],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10a83561000bc0487c415b1a63ad2b78de4f19d981f8145d63cb81f2013789f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd0fbb4c4823a48b15c9a90971490cea181372d13ab98a348f732f3ed0fb602(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24416bb8b0634eaa2a3eb27c28d18d09a9ce06170c8a49489d95c7b271d31ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6b49aceea9199ce3d7961b673864cfdc6efb328aabfbf2db2c83d9964d5ef5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c49346753d72362407de6a24c1f0b183f36557a086f11ed8591ed6c0795e90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009bad3dfe0c8633c12ce5431e0eebfd289ce8a15d0e1e2af600874cb0f5fbce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40ec14bf5486f5d4e454bd27fdd5c212419c8657976c596b9e4e01e5ece299c(
    value: typing.Optional[Saml2IntegrationDescribeOutputComment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b4e18ecf1967640ef66da49a7423bdf495f08db786b006f6aa34ddd6debd3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebed1fb927cbf73be136de8ae40adf658f9f2647f6db26b888108967c72311a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6724e7eccb10c4d5ed44fbe437dc99edc4bd62bbbe8add52cd2b70dab933ef74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fff9532ba25614facac65e3fbf6ea9361ac7fcfb5d68c0ded5622e26dfa6504(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a439abcadbb404b79c10a8dc06f36b4ca105cf52af5e70b9983e8cfa394144(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53e141bb470b10175a3a926521d05b95359aecd8a20236a48fe8599e7c72e87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0abb25ae1cac5d4d9323a0ff39d2421447a69997fa991f2d6b9977d111d762b(
    value: typing.Optional[Saml2IntegrationDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a4ae1904873a6815aa01ffa99e49ed22efe53a089cb15c94cb087693bad66d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6e05d685197e219d6c62714eca368838d07922d0f792221bf126cf8afebd61(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36ddee1612ecc2a18fe0e79162df530bb6900a86254d4fb32c52815d0b2ea36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dcbd76bd481f75369ef6a13a15a6d08713138ec6535a38ac6c30c72b0eeba4f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390c8fef40db90d6e7d5d3f4ff0443a4ded3f6279e6d64168bff16e8559b17e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977a71990a4bd4e1e00d402203e75ad5c073e8d9950d8106474093adced2cfe3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767f3ae4a2aaa940d37b9c98f112629fcc0ea315654e6409e67d08bb2f285bad(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2DigestMethodsUsed],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02886fcf0d956e3e7ac73f740e7c14367f18f7859f7e416adf95b5e1d1b62d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b067f43c8433d035a7dc8edba743e302e8b8a35feaab49ee9a6d918891d2ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508784853c6640e90122c42cc64363bbb79e56ac7fc3d11684dbcf09b418b97e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c022aaf64633e49bf9bd21d2472592a3f857733dfa89d3d93d82c073cd07a9f5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb3e69c604d5375d20eeb36a7e74fa8a2c87f665852cf94ca07476e1e23c8d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3748d1e99e9ac623740d54b36488b1676b928d9225b56b847128edf9f765bf36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952d690a264469f2b94d163952f1d8ecca85f7334757d2855e23827561a332b9(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2EnableSpInitiated],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969a684d5862c9a37bdf4fe351f8c7d58c658352f7414a3a51ab4a5641150029(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e28e68376c1e5d9d2d294b265d9710ccfac77c1929d103488f668174c25b47b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64433ef4b0d525b4bd6d2b57fa83c7e3893c9890c5881823d12f777048ef92e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00aa86cda1d74c84c01dc8b5f67501f327a55a05a8877451679a74fe03772672(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052c18965b6cf1f0aceff047f1eef481131900f3ecd3c51b6ae87f2c5613cd3d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7918c65a157a2a394c12f90acfe439bfd6feb55fa532a4c2a57ad126c2a67a3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b86fc54a2608c7f0d8b51509867163a7a40e477f58627dffcc55c0040b704f1(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2ForceAuthn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54eaa975a32948e6dda434053eb70a9d04845378187d1e98f71593381272086(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9dae95f4273cfd6b07d4fa42f189a19b229d4883cb27154ad6ad7e112515b0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa6bc83afa67429ba5a26bef3ce2c7d9600678586347feb6854b72c8d760c00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a243b5daeef28bafbc430330df5fc1b95e1cffefbd79f4aece11bb8320315f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b76bb1ea9e68ecbba3094fdd6ff7944f9ac2d58632ee1b74660e25517e252f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__accff65f3f02c1bc84e76d54c16df76f2200fed588902025b852ef49f6f8255b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eebb53509329a8f780c0f744a150fb011f384bb389f8c8ad5791d8fd0c53ac5(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2Issuer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc574a66a6ea95b509fb8ca902c847f37447584081ea23abb47d1d9a5ad6344(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7945ec4e14ff764a33ef44cc0d9d804232def3e68e773b2d5cf0f158fe900d1b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b3e5bca5989f93aa1fd2904e2c56f7aa922a6d62770645d3f6be7ee1c139ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb50b5814cf17bc1dec0e6482bdeb49f32a541d7e21caf4bdc7e2081f5c6457(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d585ec3133844c4d59631206da3beb8fdc90f335b68421639461c952a7ee78e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8884d1457c5956d88df07e7818c527abdb036ba84bbf7c01bdc025cbfc84106(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87057b3d0d36faa16803bbd62d815bf6c7d23a205e8f2f670bac159680674713(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2PostLogoutRedirectUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4617d5352423de045f77b275e0221f258fdb904bce666b76029ad4c8e7459fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c816f950e0fba6fdaa1133665c77e18945a0eb6cd0f0ea25397caa8fd54a08(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009effd4e6bb30b695de6cb601440b9e0a767c322858f7a762e8e1e42e761036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b727e0b070bb4ca7373b98d3b04c47e85549a0dd009b8df7dcea5254cb7b81f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed32f22ac055d6a457d52140d13e9c112bf3ce978b0af7c8c7fd441d4f4b8a78(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348857039b17903360b743a110b0a0e128240e58ff24fc3f1bee91eebcbc200b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e041fe7ba225bb7bc399d0446801810d778d8f5ff09e53981ffa40616cea41b(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2Provider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105e53043241a0140609fdea40d5e08873c40761a5c25e7dc1c7a562e57a00c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a97f168e68582ecbf5af3619b63adc0d763fd9cea97da97bf5223b565cded8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2aa06014ec79c69ef0d592c319d62eac83c4b639f6a871b7ff04b1d846bc6b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d785afcdec3262b186a9d5ed79c70c96333bb3f9baacc8943b8a581cf17ee4a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c66af54091d41dd5b88a92eaff4a2b084022e571654bed219255aad70f2e7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2a9cbe20553df8c42c28a8c1429f8fd15264136101cc4918b0e12e4beb77bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e26d1edde15a28b786f8f84e52402dd57d7c0746ec498e0cdf31e3f3772e8c(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2RequestedNameidFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031b3bbac5f8ae0f2e94b4d5cf724be041652e7f2f0c1c338bc2500ec3e1c3cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3faf07637b4aced6096b8b41e468fddd0583c3efe38ab3e149d20732dd1eccfc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e2e00fc03c8a00830d615aec805786cc05b0a6210a26cbcacbc3ebe053cd12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b36d2852a69981bfde0c7a80e0cbe0e8c425900479b36859096850df7dffa1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a9d3631f1a9a54432dd93cafcdb17a28ee4348bd60e10f8026fc94031ad8d1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e069e51939dd4228d0c235ecafdf62cfc96efb263fa0d3c5183313aa8297236(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f59782181ccf3467ebf9b3a72a165d9080668e39638b60f9b8ec8037b6e2e7(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SignRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e8c2c2fe7c1d57009bf53af98cd854fc2556c682c5f31b0123e2b625138479(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1177873757d51c280cb95163082e2ddb59008ab1496aae8853b1fa39e32e312(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cd3409cf4a7d1156f46f603f1a1dc01394243126eef26c0fbaba32231f2d33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca3d230f3f6afccd58d2bea48427c7b17542553f3dfa5899902fa9d870c1faf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06568790bc63dd2457a108f94d174611cbc61774b4ac4682c4494f5128192022(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1527c3deafa84fc1b757f993436235b560f98a387ed4ef5ee32ba03a32a013(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494843a7aaca39c4b6703c778eb849a2b17e52425cd5c7ff32ae161f65d43c8b(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SignatureMethodsUsed],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6c33bdd742114627cc41d56c4ecd97a583d81177e729826016f0334345229c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af35d6c1bf29a548e2b9f62e1e2f71f903210aece1e6195206f2011e0113aa2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874cee0bf30d9bdfede4c447a148560a76d84401574ddcd6623f264b417cceb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f222f1de1beb8d649421660cd63356039db8cc202601d1a9bfc0c738ef08325(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db50c8272887cf1a732b417b06d4b28a8aa43a736420a94300fbff68356bbc9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1ee287b52fb60df95f018ce9006b88b0b493f0867dcfb453393f42b8ce8037(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6046618571b4ebf840d12a1b9765d2c333378fb41ac5706112e4c7ecfb632c62(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeAcsUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c659be8ec982e7058dfc776c143ad5d37f9f8ba03b414f374e386918afc1c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e46259f6439641523f8a724ee07c109b200a142fae0b8fbd2b7124803d8afb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb1b66b42364317245a0202e6aa4741ccb3d1d1f98d4e838a1f1ec1b328499c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6387cf2f29a41fd4ff52aee2b0f2f5bdeb25915b75d9a6610a1e283730fca2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f2fae3be460ad89fdafc245ac4d64c5d6d1a20c3cea902fe6be2f29de0fe09(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5e2faf885488db2e225d52641c51c15fd75fb5e3c23399c5e9e19b67d5f703(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b959469e68115f5ca3f0a86d1cb6e01d1a4765d64851753edf9c2472c5cf3b(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeIssuerUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d33f56e9ee8c24da1612418de5cdf7d6bf7dac39c2e3f37e3da1a94c5dc8eb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abcf1c39d2edd41c73f2887d91de6003aaf1278020c310f94ebee81a07d553d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c0cfbd36ae267433603cc6c5f19801ed6cc70c76e6449fb1405b7c3cc7617f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9f98659ef118b4a423351dae4b43670cedb99138fef60c5b4a5366a574a449(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b9b8c96b3608489e13caaa379f1a7be66b26553fb75f9afdba2a5ac493769c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e9d1fdce64b93aee106bb068f9417a1f6fbe22481c91e39c4a12bc34c7e5ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467f4dcfb5dd945b553838820ef459d6966f189678d2089e5b55bbb22476b2a0(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79949d0bf6b2457405a8829405ebaead7f7317f14eaf21814af97d80da581e74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b60bf906104d4f7a9b85eaa3811f9badb8c783662c2e6a54087d39ff7b99ad6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4796bde66b10fa0b123c3b60dd328fb4d8b6f9662177269c4d05aff536120fd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1231fe6e4a2ca3db877e17128ca08571c441f8f39c521284e3930ea3b6af7a64(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542fec1e148a640369edfc38f10141c19fe3395d1797f7209d5c76cc987b6d9c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63216722a4bb1297b9051e5e06da0ef19784e9d2a997082ad2a81489001b3809(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3025db470d884be7aa9d7549fcd0cc4e4cfdd04c92c5f856e37f9b773172bc3f(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SnowflakeX509Cert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c968913fc13b38e076259d9e2b0c67d6bc304e9e0cf754cd67f448c6677e1ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd401c013501477b2a9c523c0b5100aac1220362810bef4865664a485a2971f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270b2035eeb5bda8d38dcbddbe551dceff2027b4902dabc4fa4c5a4ee1e38ef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0bf5525adba9a5099b720b21d0266172c1659e464a0dd5e30242a01b4fde92(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeeeca0e527420edd3fe839153eb98d2abab2e6f8ddb9f6ed6d9255a726932ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246568f2177b4aa14fc64040de61d01d44b99d689f08ef61471791841da44a02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7941c68e53a6cea563f84c6133dbe1076c4ca9500732aa906ef8ab8e14a11fee(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SpInitiatedLoginPageLabel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a4467790cd091dd81b35e0a0a87e085bdbe6b97df4713fefdbb6765d7dcbb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f1b75ba1738c89119ea0ff14d3eabf0a63175b3b6c0bc3aaf954c01f2f5132(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d785fea32031494ccc13f60bd43cb4086d3a3784473ec13a6a19cae2497446aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3eb232cfe0518b98ee285e65f2eb19e3ffbebe93cb5019dee1c75f53d8ce53b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e00b5a02c2c2b8ac4683197f518e4615b9d972855d7298ac40cf110293d66c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88ac34787c153ae79960562d30587b25def1b771d4083c3825796aeb1116015(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ad2070f5a7a3be45b1cf3410bceb910ea429a52361a99cfee0748abaacb00f(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2SsoUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d285dd74bd0190ec137338d7a57776bd27a96d4ebe699813cf2090e9a8be6d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8346bffc201b6bc9b3ad6b23886a9cb16d37808cc0ebf9762aa8309c9d093f0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7969d5572e5e3e62560c18f290ec0e54705ab758a0e539152589257cb99bf09b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7e757a56a138f84abf101aae9031b09f098125dd53ba56562a6b3fc4657b31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0e24350e35a6739f4919fdf4fc4249f5944c097620f3e3643afd46edaa08ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd5a6010102d5b7a1d0c9041c098bcff0ece561b0e249287d03729fe0469ac8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c9d71ed67f13f45a2fd0da26e08b3c376c6f0ba9da0ffbd8b56d1ff0d0087c(
    value: typing.Optional[Saml2IntegrationDescribeOutputSaml2X509Cert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa30480b81964c652aa853b03435cc6e6e9e39b56cde25fc4cbaf190ced4e512(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8215afa490e71b9732aa9046c84ad7a8331a3667f38e79f491693ae2ca20e8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f00783916ecde791dc6ad6db57d0aecd4659716d8ebdea1e02ff3e42585fed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace96bbdc40c2ae7e53c7b45fef0a9b3805e006acaf85e1cc093c64f423f5d8b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ba56361469a78a50e1989552e229d1f8d427619a6359cd0c7b07be6217e222(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d14eb662653fa0e7c0a802d8b3377f055bf385e637eb870b25ae140c62072b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663ecd50f3dc127947608afd2b752da96dd62e19311d8702d71242c8bcfbc060(
    value: typing.Optional[Saml2IntegrationShowOutput],
) -> None:
    """Type checking stubs"""
    pass
