r'''
# `azuread_application_registration`

Refer to the Terraform Registry for docs: [`azuread_application_registration`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration).
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


class ApplicationRegistration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.applicationRegistration.ApplicationRegistration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration azuread_application_registration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group_membership_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
        homepage_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        implicit_access_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        implicit_id_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logout_url: typing.Optional[builtins.str] = None,
        marketing_url: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        privacy_statement_url: typing.Optional[builtins.str] = None,
        requested_access_token_version: typing.Optional[jsii.Number] = None,
        service_management_reference: typing.Optional[builtins.str] = None,
        sign_in_audience: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
        terms_of_service_url: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApplicationRegistrationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration azuread_application_registration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The display name for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#display_name ApplicationRegistration#display_name}
        :param description: Description of the application as shown to end users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#description ApplicationRegistration#description}
        :param group_membership_claims: Configures the ``groups`` claim that the app expects issued in a user or OAuth access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#group_membership_claims ApplicationRegistration#group_membership_claims}
        :param homepage_url: URL of the home page for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#homepage_url ApplicationRegistration#homepage_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#id ApplicationRegistration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param implicit_access_token_issuance_enabled: Whether this application can request an access token using OAuth implicit flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#implicit_access_token_issuance_enabled ApplicationRegistration#implicit_access_token_issuance_enabled}
        :param implicit_id_token_issuance_enabled: Whether this application can request an ID token using OAuth implicit flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#implicit_id_token_issuance_enabled ApplicationRegistration#implicit_id_token_issuance_enabled}
        :param logout_url: URL of the logout page for the application, where the session is cleared for single sign-out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#logout_url ApplicationRegistration#logout_url}
        :param marketing_url: URL of the marketing page for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#marketing_url ApplicationRegistration#marketing_url}
        :param notes: User-specified notes relevant for the management of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#notes ApplicationRegistration#notes}
        :param privacy_statement_url: URL of the privacy statement for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#privacy_statement_url ApplicationRegistration#privacy_statement_url}
        :param requested_access_token_version: The access token version expected by this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#requested_access_token_version ApplicationRegistration#requested_access_token_version}
        :param service_management_reference: References application or contact information from a service or asset management database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#service_management_reference ApplicationRegistration#service_management_reference}
        :param sign_in_audience: The Microsoft account types that are supported for the current application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#sign_in_audience ApplicationRegistration#sign_in_audience}
        :param support_url: URL of the support page for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#support_url ApplicationRegistration#support_url}
        :param terms_of_service_url: URL of the terms of service statement for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#terms_of_service_url ApplicationRegistration#terms_of_service_url}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#timeouts ApplicationRegistration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1db9b7f2a5837c009b78584dd9b8f700b92552db9538da2509e7f0374483cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApplicationRegistrationConfig(
            display_name=display_name,
            description=description,
            group_membership_claims=group_membership_claims,
            homepage_url=homepage_url,
            id=id,
            implicit_access_token_issuance_enabled=implicit_access_token_issuance_enabled,
            implicit_id_token_issuance_enabled=implicit_id_token_issuance_enabled,
            logout_url=logout_url,
            marketing_url=marketing_url,
            notes=notes,
            privacy_statement_url=privacy_statement_url,
            requested_access_token_version=requested_access_token_version,
            service_management_reference=service_management_reference,
            sign_in_audience=sign_in_audience,
            support_url=support_url,
            terms_of_service_url=terms_of_service_url,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a ApplicationRegistration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApplicationRegistration to import.
        :param import_from_id: The id of the existing ApplicationRegistration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApplicationRegistration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2da838b6194e6b79e4a285331b0b704f30b9236ccb1d47a19fd4eaa56bb8e48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#create ApplicationRegistration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#delete ApplicationRegistration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#read ApplicationRegistration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#update ApplicationRegistration#update}.
        '''
        value = ApplicationRegistrationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGroupMembershipClaims")
    def reset_group_membership_claims(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupMembershipClaims", []))

    @jsii.member(jsii_name="resetHomepageUrl")
    def reset_homepage_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHomepageUrl", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImplicitAccessTokenIssuanceEnabled")
    def reset_implicit_access_token_issuance_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImplicitAccessTokenIssuanceEnabled", []))

    @jsii.member(jsii_name="resetImplicitIdTokenIssuanceEnabled")
    def reset_implicit_id_token_issuance_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImplicitIdTokenIssuanceEnabled", []))

    @jsii.member(jsii_name="resetLogoutUrl")
    def reset_logout_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogoutUrl", []))

    @jsii.member(jsii_name="resetMarketingUrl")
    def reset_marketing_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketingUrl", []))

    @jsii.member(jsii_name="resetNotes")
    def reset_notes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotes", []))

    @jsii.member(jsii_name="resetPrivacyStatementUrl")
    def reset_privacy_statement_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivacyStatementUrl", []))

    @jsii.member(jsii_name="resetRequestedAccessTokenVersion")
    def reset_requested_access_token_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestedAccessTokenVersion", []))

    @jsii.member(jsii_name="resetServiceManagementReference")
    def reset_service_management_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceManagementReference", []))

    @jsii.member(jsii_name="resetSignInAudience")
    def reset_sign_in_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignInAudience", []))

    @jsii.member(jsii_name="resetSupportUrl")
    def reset_support_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportUrl", []))

    @jsii.member(jsii_name="resetTermsOfServiceUrl")
    def reset_terms_of_service_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTermsOfServiceUrl", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="disabledByMicrosoft")
    def disabled_by_microsoft(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disabledByMicrosoft"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="publisherDomain")
    def publisher_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisherDomain"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApplicationRegistrationTimeoutsOutputReference":
        return typing.cast("ApplicationRegistrationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="groupMembershipClaimsInput")
    def group_membership_claims_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupMembershipClaimsInput"))

    @builtins.property
    @jsii.member(jsii_name="homepageUrlInput")
    def homepage_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homepageUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="implicitAccessTokenIssuanceEnabledInput")
    def implicit_access_token_issuance_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "implicitAccessTokenIssuanceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="implicitIdTokenIssuanceEnabledInput")
    def implicit_id_token_issuance_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "implicitIdTokenIssuanceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logoutUrlInput")
    def logout_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoutUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="marketingUrlInput")
    def marketing_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "marketingUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="notesInput")
    def notes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notesInput"))

    @builtins.property
    @jsii.member(jsii_name="privacyStatementUrlInput")
    def privacy_statement_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privacyStatementUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="requestedAccessTokenVersionInput")
    def requested_access_token_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestedAccessTokenVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceManagementReferenceInput")
    def service_management_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceManagementReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="signInAudienceInput")
    def sign_in_audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signInAudienceInput"))

    @builtins.property
    @jsii.member(jsii_name="supportUrlInput")
    def support_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="termsOfServiceUrlInput")
    def terms_of_service_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "termsOfServiceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApplicationRegistrationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApplicationRegistrationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4268bd4c2ed586a2771c304f22feee376205f2238302ce7b4fe64b83dab0b7c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c46fe9f5c639f7cfa16902cd2e0511f90e9af86898576ec3bbd46d61e3c5ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupMembershipClaims")
    def group_membership_claims(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupMembershipClaims"))

    @group_membership_claims.setter
    def group_membership_claims(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4602bc33d6018e4edb7861b31c735d15cf1335915d261e501cfbc5c6cb53c4e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupMembershipClaims", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="homepageUrl")
    def homepage_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homepageUrl"))

    @homepage_url.setter
    def homepage_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2bde4ea6d6fa942d8f7f27592191bbb129423b6d70431e5aca1ac70990ff5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homepageUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03a9c491b87faa604e67956f6359324bf078bf26fbb5bdf4159f4fc84c81269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="implicitAccessTokenIssuanceEnabled")
    def implicit_access_token_issuance_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "implicitAccessTokenIssuanceEnabled"))

    @implicit_access_token_issuance_enabled.setter
    def implicit_access_token_issuance_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba1cfc3905d31700f69c04cffc2194b3d307b36617e5d422962ec1e27025795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "implicitAccessTokenIssuanceEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="implicitIdTokenIssuanceEnabled")
    def implicit_id_token_issuance_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "implicitIdTokenIssuanceEnabled"))

    @implicit_id_token_issuance_enabled.setter
    def implicit_id_token_issuance_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692c1bc47774db3c86dd1150da6a8c14c9b61df8fe5648f1e8e48d2c00f91ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "implicitIdTokenIssuanceEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logoutUrl")
    def logout_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoutUrl"))

    @logout_url.setter
    def logout_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e14ae7c294f895ff032225d67d78cfa62ea49e7722e3bd990caa5c623b0593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoutUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="marketingUrl")
    def marketing_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketingUrl"))

    @marketing_url.setter
    def marketing_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d4671e4ba6f2ce3a97bc678b6fca0aef809178d907d321675867a98ba4e97d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "marketingUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notes"))

    @notes.setter
    def notes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e0a7a079496f9de547120d8dd098e06722bbbf46ad6bc43c6c87084eeb07e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privacyStatementUrl")
    def privacy_statement_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacyStatementUrl"))

    @privacy_statement_url.setter
    def privacy_statement_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee07259967e5a1449512adaf4f0f6329c3250d542556111becf3f5845c4a02ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privacyStatementUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestedAccessTokenVersion")
    def requested_access_token_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requestedAccessTokenVersion"))

    @requested_access_token_version.setter
    def requested_access_token_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008904af6bcc154409536eceaefa61c672b3bb7db3200ddebea6799382ce71d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedAccessTokenVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceManagementReference")
    def service_management_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceManagementReference"))

    @service_management_reference.setter
    def service_management_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34ad71bfff28bc49d523ce837e65a1de69ea70f4a0084fa441c465717462a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceManagementReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signInAudience")
    def sign_in_audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signInAudience"))

    @sign_in_audience.setter
    def sign_in_audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b05c436290372c3844e71bd41d5fd66de1a7314e94dbd0393a2cf8b619403ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signInAudience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportUrl")
    def support_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportUrl"))

    @support_url.setter
    def support_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f71a065061a07eeec6dc7b0faeaed3a78cd28a55cd1876f5a78f244786b5fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="termsOfServiceUrl")
    def terms_of_service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "termsOfServiceUrl"))

    @terms_of_service_url.setter
    def terms_of_service_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad11d8a47617c6c08b348ce466448bf366bdabdc1c7542587c3a0a842e95421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "termsOfServiceUrl", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.applicationRegistration.ApplicationRegistrationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "description": "description",
        "group_membership_claims": "groupMembershipClaims",
        "homepage_url": "homepageUrl",
        "id": "id",
        "implicit_access_token_issuance_enabled": "implicitAccessTokenIssuanceEnabled",
        "implicit_id_token_issuance_enabled": "implicitIdTokenIssuanceEnabled",
        "logout_url": "logoutUrl",
        "marketing_url": "marketingUrl",
        "notes": "notes",
        "privacy_statement_url": "privacyStatementUrl",
        "requested_access_token_version": "requestedAccessTokenVersion",
        "service_management_reference": "serviceManagementReference",
        "sign_in_audience": "signInAudience",
        "support_url": "supportUrl",
        "terms_of_service_url": "termsOfServiceUrl",
        "timeouts": "timeouts",
    },
)
class ApplicationRegistrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group_membership_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
        homepage_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        implicit_access_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        implicit_id_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logout_url: typing.Optional[builtins.str] = None,
        marketing_url: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        privacy_statement_url: typing.Optional[builtins.str] = None,
        requested_access_token_version: typing.Optional[jsii.Number] = None,
        service_management_reference: typing.Optional[builtins.str] = None,
        sign_in_audience: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
        terms_of_service_url: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApplicationRegistrationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The display name for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#display_name ApplicationRegistration#display_name}
        :param description: Description of the application as shown to end users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#description ApplicationRegistration#description}
        :param group_membership_claims: Configures the ``groups`` claim that the app expects issued in a user or OAuth access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#group_membership_claims ApplicationRegistration#group_membership_claims}
        :param homepage_url: URL of the home page for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#homepage_url ApplicationRegistration#homepage_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#id ApplicationRegistration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param implicit_access_token_issuance_enabled: Whether this application can request an access token using OAuth implicit flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#implicit_access_token_issuance_enabled ApplicationRegistration#implicit_access_token_issuance_enabled}
        :param implicit_id_token_issuance_enabled: Whether this application can request an ID token using OAuth implicit flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#implicit_id_token_issuance_enabled ApplicationRegistration#implicit_id_token_issuance_enabled}
        :param logout_url: URL of the logout page for the application, where the session is cleared for single sign-out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#logout_url ApplicationRegistration#logout_url}
        :param marketing_url: URL of the marketing page for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#marketing_url ApplicationRegistration#marketing_url}
        :param notes: User-specified notes relevant for the management of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#notes ApplicationRegistration#notes}
        :param privacy_statement_url: URL of the privacy statement for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#privacy_statement_url ApplicationRegistration#privacy_statement_url}
        :param requested_access_token_version: The access token version expected by this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#requested_access_token_version ApplicationRegistration#requested_access_token_version}
        :param service_management_reference: References application or contact information from a service or asset management database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#service_management_reference ApplicationRegistration#service_management_reference}
        :param sign_in_audience: The Microsoft account types that are supported for the current application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#sign_in_audience ApplicationRegistration#sign_in_audience}
        :param support_url: URL of the support page for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#support_url ApplicationRegistration#support_url}
        :param terms_of_service_url: URL of the terms of service statement for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#terms_of_service_url ApplicationRegistration#terms_of_service_url}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#timeouts ApplicationRegistration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ApplicationRegistrationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2bd1c3cad6b422605cbbe5662b40833138b845a7e7d092637caad82ec44bb2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument group_membership_claims", value=group_membership_claims, expected_type=type_hints["group_membership_claims"])
            check_type(argname="argument homepage_url", value=homepage_url, expected_type=type_hints["homepage_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument implicit_access_token_issuance_enabled", value=implicit_access_token_issuance_enabled, expected_type=type_hints["implicit_access_token_issuance_enabled"])
            check_type(argname="argument implicit_id_token_issuance_enabled", value=implicit_id_token_issuance_enabled, expected_type=type_hints["implicit_id_token_issuance_enabled"])
            check_type(argname="argument logout_url", value=logout_url, expected_type=type_hints["logout_url"])
            check_type(argname="argument marketing_url", value=marketing_url, expected_type=type_hints["marketing_url"])
            check_type(argname="argument notes", value=notes, expected_type=type_hints["notes"])
            check_type(argname="argument privacy_statement_url", value=privacy_statement_url, expected_type=type_hints["privacy_statement_url"])
            check_type(argname="argument requested_access_token_version", value=requested_access_token_version, expected_type=type_hints["requested_access_token_version"])
            check_type(argname="argument service_management_reference", value=service_management_reference, expected_type=type_hints["service_management_reference"])
            check_type(argname="argument sign_in_audience", value=sign_in_audience, expected_type=type_hints["sign_in_audience"])
            check_type(argname="argument support_url", value=support_url, expected_type=type_hints["support_url"])
            check_type(argname="argument terms_of_service_url", value=terms_of_service_url, expected_type=type_hints["terms_of_service_url"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
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
        if description is not None:
            self._values["description"] = description
        if group_membership_claims is not None:
            self._values["group_membership_claims"] = group_membership_claims
        if homepage_url is not None:
            self._values["homepage_url"] = homepage_url
        if id is not None:
            self._values["id"] = id
        if implicit_access_token_issuance_enabled is not None:
            self._values["implicit_access_token_issuance_enabled"] = implicit_access_token_issuance_enabled
        if implicit_id_token_issuance_enabled is not None:
            self._values["implicit_id_token_issuance_enabled"] = implicit_id_token_issuance_enabled
        if logout_url is not None:
            self._values["logout_url"] = logout_url
        if marketing_url is not None:
            self._values["marketing_url"] = marketing_url
        if notes is not None:
            self._values["notes"] = notes
        if privacy_statement_url is not None:
            self._values["privacy_statement_url"] = privacy_statement_url
        if requested_access_token_version is not None:
            self._values["requested_access_token_version"] = requested_access_token_version
        if service_management_reference is not None:
            self._values["service_management_reference"] = service_management_reference
        if sign_in_audience is not None:
            self._values["sign_in_audience"] = sign_in_audience
        if support_url is not None:
            self._values["support_url"] = support_url
        if terms_of_service_url is not None:
            self._values["terms_of_service_url"] = terms_of_service_url
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def display_name(self) -> builtins.str:
        '''The display name for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#display_name ApplicationRegistration#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the application as shown to end users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#description ApplicationRegistration#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_membership_claims(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Configures the ``groups`` claim that the app expects issued in a user or OAuth access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#group_membership_claims ApplicationRegistration#group_membership_claims}
        '''
        result = self._values.get("group_membership_claims")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def homepage_url(self) -> typing.Optional[builtins.str]:
        '''URL of the home page for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#homepage_url ApplicationRegistration#homepage_url}
        '''
        result = self._values.get("homepage_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#id ApplicationRegistration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def implicit_access_token_issuance_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this application can request an access token using OAuth implicit flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#implicit_access_token_issuance_enabled ApplicationRegistration#implicit_access_token_issuance_enabled}
        '''
        result = self._values.get("implicit_access_token_issuance_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def implicit_id_token_issuance_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this application can request an ID token using OAuth implicit flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#implicit_id_token_issuance_enabled ApplicationRegistration#implicit_id_token_issuance_enabled}
        '''
        result = self._values.get("implicit_id_token_issuance_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def logout_url(self) -> typing.Optional[builtins.str]:
        '''URL of the logout page for the application, where the session is cleared for single sign-out.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#logout_url ApplicationRegistration#logout_url}
        '''
        result = self._values.get("logout_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketing_url(self) -> typing.Optional[builtins.str]:
        '''URL of the marketing page for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#marketing_url ApplicationRegistration#marketing_url}
        '''
        result = self._values.get("marketing_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        '''User-specified notes relevant for the management of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#notes ApplicationRegistration#notes}
        '''
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privacy_statement_url(self) -> typing.Optional[builtins.str]:
        '''URL of the privacy statement for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#privacy_statement_url ApplicationRegistration#privacy_statement_url}
        '''
        result = self._values.get("privacy_statement_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requested_access_token_version(self) -> typing.Optional[jsii.Number]:
        '''The access token version expected by this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#requested_access_token_version ApplicationRegistration#requested_access_token_version}
        '''
        result = self._values.get("requested_access_token_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_management_reference(self) -> typing.Optional[builtins.str]:
        '''References application or contact information from a service or asset management database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#service_management_reference ApplicationRegistration#service_management_reference}
        '''
        result = self._values.get("service_management_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_in_audience(self) -> typing.Optional[builtins.str]:
        '''The Microsoft account types that are supported for the current application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#sign_in_audience ApplicationRegistration#sign_in_audience}
        '''
        result = self._values.get("sign_in_audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''URL of the support page for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#support_url ApplicationRegistration#support_url}
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terms_of_service_url(self) -> typing.Optional[builtins.str]:
        '''URL of the terms of service statement for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#terms_of_service_url ApplicationRegistration#terms_of_service_url}
        '''
        result = self._values.get("terms_of_service_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApplicationRegistrationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#timeouts ApplicationRegistration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApplicationRegistrationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationRegistrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.applicationRegistration.ApplicationRegistrationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApplicationRegistrationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#create ApplicationRegistration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#delete ApplicationRegistration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#read ApplicationRegistration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#update ApplicationRegistration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3e516d10ebbf5f742405801c317d5210fe9c42ce56113284ce31f102b2a702)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#create ApplicationRegistration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#delete ApplicationRegistration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#read ApplicationRegistration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application_registration#update ApplicationRegistration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationRegistrationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationRegistrationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.applicationRegistration.ApplicationRegistrationTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e7ef53cfee6f1fb8aae49733eb6c8565b7a9ef5d416727f9ca6d18566806b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42105c71c293d55ecbfde67f1ce39d1a6d193678dd9b81d8db8d40beb96d988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6f05046ae2dc298327d1f38e3f4b6140202255dfcad5449cb163925330ed3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68e37bb9a763239c148b81b921e4148216c9719c1c871d865f3e6449346bebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b850d7929120f483b4963fadd00c03d272dabeb8c2ac02e8d5a68cfb61fd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRegistrationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRegistrationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRegistrationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74f4c5c71ece566ec4ff9fb72a3b4b5d2338e75d4486e25262a1c6a03bc700b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApplicationRegistration",
    "ApplicationRegistrationConfig",
    "ApplicationRegistrationTimeouts",
    "ApplicationRegistrationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__eb1db9b7f2a5837c009b78584dd9b8f700b92552db9538da2509e7f0374483cc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    group_membership_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    homepage_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    implicit_access_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    implicit_id_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logout_url: typing.Optional[builtins.str] = None,
    marketing_url: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    privacy_statement_url: typing.Optional[builtins.str] = None,
    requested_access_token_version: typing.Optional[jsii.Number] = None,
    service_management_reference: typing.Optional[builtins.str] = None,
    sign_in_audience: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
    terms_of_service_url: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApplicationRegistrationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f2da838b6194e6b79e4a285331b0b704f30b9236ccb1d47a19fd4eaa56bb8e48(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4268bd4c2ed586a2771c304f22feee376205f2238302ce7b4fe64b83dab0b7c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c46fe9f5c639f7cfa16902cd2e0511f90e9af86898576ec3bbd46d61e3c5ba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4602bc33d6018e4edb7861b31c735d15cf1335915d261e501cfbc5c6cb53c4e2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2bde4ea6d6fa942d8f7f27592191bbb129423b6d70431e5aca1ac70990ff5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03a9c491b87faa604e67956f6359324bf078bf26fbb5bdf4159f4fc84c81269(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba1cfc3905d31700f69c04cffc2194b3d307b36617e5d422962ec1e27025795(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692c1bc47774db3c86dd1150da6a8c14c9b61df8fe5648f1e8e48d2c00f91ba0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e14ae7c294f895ff032225d67d78cfa62ea49e7722e3bd990caa5c623b0593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d4671e4ba6f2ce3a97bc678b6fca0aef809178d907d321675867a98ba4e97d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0a7a079496f9de547120d8dd098e06722bbbf46ad6bc43c6c87084eeb07e10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee07259967e5a1449512adaf4f0f6329c3250d542556111becf3f5845c4a02ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008904af6bcc154409536eceaefa61c672b3bb7db3200ddebea6799382ce71d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34ad71bfff28bc49d523ce837e65a1de69ea70f4a0084fa441c465717462a7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b05c436290372c3844e71bd41d5fd66de1a7314e94dbd0393a2cf8b619403ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f71a065061a07eeec6dc7b0faeaed3a78cd28a55cd1876f5a78f244786b5fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad11d8a47617c6c08b348ce466448bf366bdabdc1c7542587c3a0a842e95421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2bd1c3cad6b422605cbbe5662b40833138b845a7e7d092637caad82ec44bb2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    group_membership_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    homepage_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    implicit_access_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    implicit_id_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logout_url: typing.Optional[builtins.str] = None,
    marketing_url: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    privacy_statement_url: typing.Optional[builtins.str] = None,
    requested_access_token_version: typing.Optional[jsii.Number] = None,
    service_management_reference: typing.Optional[builtins.str] = None,
    sign_in_audience: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
    terms_of_service_url: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApplicationRegistrationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3e516d10ebbf5f742405801c317d5210fe9c42ce56113284ce31f102b2a702(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e7ef53cfee6f1fb8aae49733eb6c8565b7a9ef5d416727f9ca6d18566806b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42105c71c293d55ecbfde67f1ce39d1a6d193678dd9b81d8db8d40beb96d988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6f05046ae2dc298327d1f38e3f4b6140202255dfcad5449cb163925330ed3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68e37bb9a763239c148b81b921e4148216c9719c1c871d865f3e6449346bebd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b850d7929120f483b4963fadd00c03d272dabeb8c2ac02e8d5a68cfb61fd0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74f4c5c71ece566ec4ff9fb72a3b4b5d2338e75d4486e25262a1c6a03bc700b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRegistrationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
