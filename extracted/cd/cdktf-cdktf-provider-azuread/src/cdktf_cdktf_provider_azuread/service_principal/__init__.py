r'''
# `azuread_service_principal`

Refer to the Terraform Registry for docs: [`azuread_service_principal`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal).
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


class ServicePrincipal(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipal",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal azuread_service_principal}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        client_id: builtins.str,
        account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        app_role_assignment_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServicePrincipalFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        feature_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServicePrincipalFeatureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        login_url: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        notification_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_single_sign_on_mode: typing.Optional[builtins.str] = None,
        saml_single_sign_on: typing.Optional[typing.Union["ServicePrincipalSamlSingleSignOn", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ServicePrincipalTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_existing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal azuread_service_principal} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param client_id: The client ID of the application for which to create a service principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#client_id ServicePrincipal#client_id}
        :param account_enabled: Whether or not the service principal account is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#account_enabled ServicePrincipal#account_enabled}
        :param alternative_names: A list of alternative names, used to retrieve service principals by subscription, identify resource group and full resource ids for managed identities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#alternative_names ServicePrincipal#alternative_names}
        :param app_role_assignment_required: Whether this service principal requires an app role assignment to a user or group before Azure AD will issue a user or access token to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#app_role_assignment_required ServicePrincipal#app_role_assignment_required}
        :param description: Description of the service principal provided for internal end-users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#description ServicePrincipal#description}
        :param features: features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#features ServicePrincipal#features}
        :param feature_tags: feature_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#feature_tags ServicePrincipal#feature_tags}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#id ServicePrincipal#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param login_url: The URL where the service provider redirects the user to Azure AD to authenticate. Azure AD uses the URL to launch the application from Microsoft 365 or the Azure AD My Apps. When blank, Azure AD performs IdP-initiated sign-on for applications configured with SAML-based single sign-on Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#login_url ServicePrincipal#login_url}
        :param notes: Free text field to capture information about the service principal, typically used for operational purposes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#notes ServicePrincipal#notes}
        :param notification_email_addresses: List of email addresses where Azure AD sends a notification when the active certificate is near the expiration date. This is only for the certificates used to sign the SAML token issued for Azure AD Gallery applications Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#notification_email_addresses ServicePrincipal#notification_email_addresses}
        :param owners: A list of object IDs of principals that will be granted ownership of the service principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#owners ServicePrincipal#owners}
        :param preferred_single_sign_on_mode: The single sign-on mode configured for this application. Azure AD uses the preferred single sign-on mode to launch the application from Microsoft 365 or the Azure AD My Apps Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#preferred_single_sign_on_mode ServicePrincipal#preferred_single_sign_on_mode}
        :param saml_single_sign_on: saml_single_sign_on block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#saml_single_sign_on ServicePrincipal#saml_single_sign_on}
        :param tags: A set of tags to apply to the service principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#tags ServicePrincipal#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#timeouts ServicePrincipal#timeouts}
        :param use_existing: When true, the resource will return an existing service principal instead of failing with an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#use_existing ServicePrincipal#use_existing}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274f8fc4f064d72d41fce04f6659ee4ef1986f78ff3f6aa47dd0fcfd20abad5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServicePrincipalConfig(
            client_id=client_id,
            account_enabled=account_enabled,
            alternative_names=alternative_names,
            app_role_assignment_required=app_role_assignment_required,
            description=description,
            features=features,
            feature_tags=feature_tags,
            id=id,
            login_url=login_url,
            notes=notes,
            notification_email_addresses=notification_email_addresses,
            owners=owners,
            preferred_single_sign_on_mode=preferred_single_sign_on_mode,
            saml_single_sign_on=saml_single_sign_on,
            tags=tags,
            timeouts=timeouts,
            use_existing=use_existing,
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
        '''Generates CDKTF code for importing a ServicePrincipal resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServicePrincipal to import.
        :param import_from_id: The id of the existing ServicePrincipal that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServicePrincipal to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39536cddd93408bacdd298f3eab07c2cde811144c80fcf892c4e114f9b25e3b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFeatures")
    def put_features(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServicePrincipalFeatures", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aed6d814f22146e031571c469ddbd21bb42b38d93db8915d4cd5ae2e3a8dbc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatures", [value]))

    @jsii.member(jsii_name="putFeatureTags")
    def put_feature_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServicePrincipalFeatureTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40a2f85d8abcbdc2fab1796027a8cdcc3f9b1e2e45aeb8a1f8d8dff4ee70a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatureTags", [value]))

    @jsii.member(jsii_name="putSamlSingleSignOn")
    def put_saml_single_sign_on(
        self,
        *,
        relay_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param relay_state: The relative URI the service provider would redirect to after completion of the single sign-on flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#relay_state ServicePrincipal#relay_state}
        '''
        value = ServicePrincipalSamlSingleSignOn(relay_state=relay_state)

        return typing.cast(None, jsii.invoke(self, "putSamlSingleSignOn", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#create ServicePrincipal#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#delete ServicePrincipal#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#read ServicePrincipal#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#update ServicePrincipal#update}.
        '''
        value = ServicePrincipalTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccountEnabled")
    def reset_account_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountEnabled", []))

    @jsii.member(jsii_name="resetAlternativeNames")
    def reset_alternative_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlternativeNames", []))

    @jsii.member(jsii_name="resetAppRoleAssignmentRequired")
    def reset_app_role_assignment_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppRoleAssignmentRequired", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFeatures")
    def reset_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatures", []))

    @jsii.member(jsii_name="resetFeatureTags")
    def reset_feature_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureTags", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoginUrl")
    def reset_login_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginUrl", []))

    @jsii.member(jsii_name="resetNotes")
    def reset_notes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotes", []))

    @jsii.member(jsii_name="resetNotificationEmailAddresses")
    def reset_notification_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationEmailAddresses", []))

    @jsii.member(jsii_name="resetOwners")
    def reset_owners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwners", []))

    @jsii.member(jsii_name="resetPreferredSingleSignOnMode")
    def reset_preferred_single_sign_on_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredSingleSignOnMode", []))

    @jsii.member(jsii_name="resetSamlSingleSignOn")
    def reset_saml_single_sign_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamlSingleSignOn", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUseExisting")
    def reset_use_existing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseExisting", []))

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
    @jsii.member(jsii_name="applicationTenantId")
    def application_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationTenantId"))

    @builtins.property
    @jsii.member(jsii_name="appRoleIds")
    def app_role_ids(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "appRoleIds"))

    @builtins.property
    @jsii.member(jsii_name="appRoles")
    def app_roles(self) -> "ServicePrincipalAppRolesList":
        return typing.cast("ServicePrincipalAppRolesList", jsii.get(self, "appRoles"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="features")
    def features(self) -> "ServicePrincipalFeaturesList":
        return typing.cast("ServicePrincipalFeaturesList", jsii.get(self, "features"))

    @builtins.property
    @jsii.member(jsii_name="featureTags")
    def feature_tags(self) -> "ServicePrincipalFeatureTagsList":
        return typing.cast("ServicePrincipalFeatureTagsList", jsii.get(self, "featureTags"))

    @builtins.property
    @jsii.member(jsii_name="homepageUrl")
    def homepage_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homepageUrl"))

    @builtins.property
    @jsii.member(jsii_name="logoutUrl")
    def logout_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoutUrl"))

    @builtins.property
    @jsii.member(jsii_name="oauth2PermissionScopeIds")
    def oauth2_permission_scope_ids(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "oauth2PermissionScopeIds"))

    @builtins.property
    @jsii.member(jsii_name="oauth2PermissionScopes")
    def oauth2_permission_scopes(self) -> "ServicePrincipalOauth2PermissionScopesList":
        return typing.cast("ServicePrincipalOauth2PermissionScopesList", jsii.get(self, "oauth2PermissionScopes"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="redirectUris")
    def redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "redirectUris"))

    @builtins.property
    @jsii.member(jsii_name="samlMetadataUrl")
    def saml_metadata_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "samlMetadataUrl"))

    @builtins.property
    @jsii.member(jsii_name="samlSingleSignOn")
    def saml_single_sign_on(self) -> "ServicePrincipalSamlSingleSignOnOutputReference":
        return typing.cast("ServicePrincipalSamlSingleSignOnOutputReference", jsii.get(self, "samlSingleSignOn"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalNames")
    def service_principal_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "servicePrincipalNames"))

    @builtins.property
    @jsii.member(jsii_name="signInAudience")
    def sign_in_audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signInAudience"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ServicePrincipalTimeoutsOutputReference":
        return typing.cast("ServicePrincipalTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="accountEnabledInput")
    def account_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accountEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="alternativeNamesInput")
    def alternative_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "alternativeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="appRoleAssignmentRequiredInput")
    def app_role_assignment_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "appRoleAssignmentRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="featuresInput")
    def features_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicePrincipalFeatures"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicePrincipalFeatures"]]], jsii.get(self, "featuresInput"))

    @builtins.property
    @jsii.member(jsii_name="featureTagsInput")
    def feature_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicePrincipalFeatureTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicePrincipalFeatureTags"]]], jsii.get(self, "featureTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loginUrlInput")
    def login_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="notesInput")
    def notes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notesInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationEmailAddressesInput")
    def notification_email_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationEmailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="ownersInput")
    def owners_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ownersInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredSingleSignOnModeInput")
    def preferred_single_sign_on_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredSingleSignOnModeInput"))

    @builtins.property
    @jsii.member(jsii_name="samlSingleSignOnInput")
    def saml_single_sign_on_input(
        self,
    ) -> typing.Optional["ServicePrincipalSamlSingleSignOn"]:
        return typing.cast(typing.Optional["ServicePrincipalSamlSingleSignOn"], jsii.get(self, "samlSingleSignOnInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServicePrincipalTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServicePrincipalTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="useExistingInput")
    def use_existing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useExistingInput"))

    @builtins.property
    @jsii.member(jsii_name="accountEnabled")
    def account_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accountEnabled"))

    @account_enabled.setter
    def account_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749dada87d0affa006dfd2132479eb016eaa8e23517dcce094616ec924f14c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alternativeNames")
    def alternative_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "alternativeNames"))

    @alternative_names.setter
    def alternative_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8c1e903f659584ece5f1957e52ffc47a92c67f854e14de4ac9c4b0e1a1fa86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alternativeNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appRoleAssignmentRequired")
    def app_role_assignment_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "appRoleAssignmentRequired"))

    @app_role_assignment_required.setter
    def app_role_assignment_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__923fac015c80c70fa3c07ba199bb88b0cac551ab4dbd096a60cafaee33dd731e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appRoleAssignmentRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00e7b06514ff70102bb49c21ff217f1bc574e649fea59ab5738c47562b84578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66e6b08670d138a1351f1aff245b1ba806cc37d8b076471f4cfe3730b265409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42273f6aa461e9f828d873e13ef1aa2f81bd3fd276162692e12db23ab53c276a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginUrl")
    def login_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginUrl"))

    @login_url.setter
    def login_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61c32cf05141d28d20ae7353e5108fd3a9c804a2fa1141a6e8cc033749e6c0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notes"))

    @notes.setter
    def notes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9741200ed9808aff7d90ad617cdf680f317359cc9db89f7eb6fe8224322367d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationEmailAddresses")
    def notification_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notificationEmailAddresses"))

    @notification_email_addresses.setter
    def notification_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9255e3f25c07018a4ef144b2403045622716d6f85c3605f8aa7220b3312c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owners")
    def owners(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "owners"))

    @owners.setter
    def owners(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c75997ad0e8c33142488fc98aaa304c9ed8001ee5810d45416a6b6a9bdf082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owners", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredSingleSignOnMode")
    def preferred_single_sign_on_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredSingleSignOnMode"))

    @preferred_single_sign_on_mode.setter
    def preferred_single_sign_on_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c982a8007aa915361f6cc33c8679e892c7da035b60bfe38112829fa55334029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredSingleSignOnMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866567d15831790b6d0168597eb597bb7d7cc7a3f961a2c2799753ca57da4b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useExisting")
    def use_existing(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useExisting"))

    @use_existing.setter
    def use_existing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573e8bb2797b1147f97be0bc6d2ec438b8b2e96b82b8d36425c265e650d5e5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useExisting", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalAppRoles",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServicePrincipalAppRoles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicePrincipalAppRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicePrincipalAppRolesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalAppRolesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__988a5add5c74f4b653100bc4c796574a7a09d2cae98f2b2b3dd5d2a44248c39f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServicePrincipalAppRolesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14fe13d372dfdc136c6d6022acd85839761aea8e479e721adf2be891f778d6a2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServicePrincipalAppRolesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0366222b03c5554e69c56cfea773df9782ef6cc8e0b72b8c2219ce4ede8015dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a9a64497a593693d0326e3a3b76f6fb091f4d7853fe51435c4570fe370616d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02e4c54464edea322f0505c735b445cad8379233d545360cdfe97c3ad8eaab67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServicePrincipalAppRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalAppRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dddb8b720f08984bf25d4b1d950a5df4a8c7216cbf47b959e5443384e2c1876)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedMemberTypes")
    def allowed_member_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMemberTypes"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServicePrincipalAppRoles]:
        return typing.cast(typing.Optional[ServicePrincipalAppRoles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServicePrincipalAppRoles]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e09ace7eee80f506a2aa8d6724b692e9dddb515567521cba6e54bf0a3f2987a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "client_id": "clientId",
        "account_enabled": "accountEnabled",
        "alternative_names": "alternativeNames",
        "app_role_assignment_required": "appRoleAssignmentRequired",
        "description": "description",
        "features": "features",
        "feature_tags": "featureTags",
        "id": "id",
        "login_url": "loginUrl",
        "notes": "notes",
        "notification_email_addresses": "notificationEmailAddresses",
        "owners": "owners",
        "preferred_single_sign_on_mode": "preferredSingleSignOnMode",
        "saml_single_sign_on": "samlSingleSignOn",
        "tags": "tags",
        "timeouts": "timeouts",
        "use_existing": "useExisting",
    },
)
class ServicePrincipalConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_id: builtins.str,
        account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        app_role_assignment_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServicePrincipalFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        feature_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServicePrincipalFeatureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        login_url: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        notification_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_single_sign_on_mode: typing.Optional[builtins.str] = None,
        saml_single_sign_on: typing.Optional[typing.Union["ServicePrincipalSamlSingleSignOn", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ServicePrincipalTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_existing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param client_id: The client ID of the application for which to create a service principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#client_id ServicePrincipal#client_id}
        :param account_enabled: Whether or not the service principal account is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#account_enabled ServicePrincipal#account_enabled}
        :param alternative_names: A list of alternative names, used to retrieve service principals by subscription, identify resource group and full resource ids for managed identities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#alternative_names ServicePrincipal#alternative_names}
        :param app_role_assignment_required: Whether this service principal requires an app role assignment to a user or group before Azure AD will issue a user or access token to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#app_role_assignment_required ServicePrincipal#app_role_assignment_required}
        :param description: Description of the service principal provided for internal end-users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#description ServicePrincipal#description}
        :param features: features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#features ServicePrincipal#features}
        :param feature_tags: feature_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#feature_tags ServicePrincipal#feature_tags}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#id ServicePrincipal#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param login_url: The URL where the service provider redirects the user to Azure AD to authenticate. Azure AD uses the URL to launch the application from Microsoft 365 or the Azure AD My Apps. When blank, Azure AD performs IdP-initiated sign-on for applications configured with SAML-based single sign-on Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#login_url ServicePrincipal#login_url}
        :param notes: Free text field to capture information about the service principal, typically used for operational purposes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#notes ServicePrincipal#notes}
        :param notification_email_addresses: List of email addresses where Azure AD sends a notification when the active certificate is near the expiration date. This is only for the certificates used to sign the SAML token issued for Azure AD Gallery applications Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#notification_email_addresses ServicePrincipal#notification_email_addresses}
        :param owners: A list of object IDs of principals that will be granted ownership of the service principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#owners ServicePrincipal#owners}
        :param preferred_single_sign_on_mode: The single sign-on mode configured for this application. Azure AD uses the preferred single sign-on mode to launch the application from Microsoft 365 or the Azure AD My Apps Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#preferred_single_sign_on_mode ServicePrincipal#preferred_single_sign_on_mode}
        :param saml_single_sign_on: saml_single_sign_on block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#saml_single_sign_on ServicePrincipal#saml_single_sign_on}
        :param tags: A set of tags to apply to the service principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#tags ServicePrincipal#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#timeouts ServicePrincipal#timeouts}
        :param use_existing: When true, the resource will return an existing service principal instead of failing with an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#use_existing ServicePrincipal#use_existing}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(saml_single_sign_on, dict):
            saml_single_sign_on = ServicePrincipalSamlSingleSignOn(**saml_single_sign_on)
        if isinstance(timeouts, dict):
            timeouts = ServicePrincipalTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d990a645589140ab9a7b3a68ab4efe8ecb5fe876ec94a17d38b23a8f52fb073)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument account_enabled", value=account_enabled, expected_type=type_hints["account_enabled"])
            check_type(argname="argument alternative_names", value=alternative_names, expected_type=type_hints["alternative_names"])
            check_type(argname="argument app_role_assignment_required", value=app_role_assignment_required, expected_type=type_hints["app_role_assignment_required"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument features", value=features, expected_type=type_hints["features"])
            check_type(argname="argument feature_tags", value=feature_tags, expected_type=type_hints["feature_tags"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument login_url", value=login_url, expected_type=type_hints["login_url"])
            check_type(argname="argument notes", value=notes, expected_type=type_hints["notes"])
            check_type(argname="argument notification_email_addresses", value=notification_email_addresses, expected_type=type_hints["notification_email_addresses"])
            check_type(argname="argument owners", value=owners, expected_type=type_hints["owners"])
            check_type(argname="argument preferred_single_sign_on_mode", value=preferred_single_sign_on_mode, expected_type=type_hints["preferred_single_sign_on_mode"])
            check_type(argname="argument saml_single_sign_on", value=saml_single_sign_on, expected_type=type_hints["saml_single_sign_on"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument use_existing", value=use_existing, expected_type=type_hints["use_existing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
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
        if account_enabled is not None:
            self._values["account_enabled"] = account_enabled
        if alternative_names is not None:
            self._values["alternative_names"] = alternative_names
        if app_role_assignment_required is not None:
            self._values["app_role_assignment_required"] = app_role_assignment_required
        if description is not None:
            self._values["description"] = description
        if features is not None:
            self._values["features"] = features
        if feature_tags is not None:
            self._values["feature_tags"] = feature_tags
        if id is not None:
            self._values["id"] = id
        if login_url is not None:
            self._values["login_url"] = login_url
        if notes is not None:
            self._values["notes"] = notes
        if notification_email_addresses is not None:
            self._values["notification_email_addresses"] = notification_email_addresses
        if owners is not None:
            self._values["owners"] = owners
        if preferred_single_sign_on_mode is not None:
            self._values["preferred_single_sign_on_mode"] = preferred_single_sign_on_mode
        if saml_single_sign_on is not None:
            self._values["saml_single_sign_on"] = saml_single_sign_on
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if use_existing is not None:
            self._values["use_existing"] = use_existing

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
    def client_id(self) -> builtins.str:
        '''The client ID of the application for which to create a service principal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#client_id ServicePrincipal#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the service principal account is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#account_enabled ServicePrincipal#account_enabled}
        '''
        result = self._values.get("account_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of alternative names, used to retrieve service principals by subscription, identify resource group and full resource ids for managed identities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#alternative_names ServicePrincipal#alternative_names}
        '''
        result = self._values.get("alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def app_role_assignment_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this service principal requires an app role assignment to a user or group before Azure AD will issue a user or access token to the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#app_role_assignment_required ServicePrincipal#app_role_assignment_required}
        '''
        result = self._values.get("app_role_assignment_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the service principal provided for internal end-users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#description ServicePrincipal#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def features(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicePrincipalFeatures"]]]:
        '''features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#features ServicePrincipal#features}
        '''
        result = self._values.get("features")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicePrincipalFeatures"]]], result)

    @builtins.property
    def feature_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicePrincipalFeatureTags"]]]:
        '''feature_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#feature_tags ServicePrincipal#feature_tags}
        '''
        result = self._values.get("feature_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicePrincipalFeatureTags"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#id ServicePrincipal#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login_url(self) -> typing.Optional[builtins.str]:
        '''The URL where the service provider redirects the user to Azure AD to authenticate.

        Azure AD uses the URL to launch the application from Microsoft 365 or the Azure AD My Apps. When blank, Azure AD performs IdP-initiated sign-on for applications configured with SAML-based single sign-on

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#login_url ServicePrincipal#login_url}
        '''
        result = self._values.get("login_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        '''Free text field to capture information about the service principal, typically used for operational purposes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#notes ServicePrincipal#notes}
        '''
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_email_addresses(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''List of email addresses where Azure AD sends a notification when the active certificate is near the expiration date.

        This is only for the certificates used to sign the SAML token issued for Azure AD Gallery applications

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#notification_email_addresses ServicePrincipal#notification_email_addresses}
        '''
        result = self._values.get("notification_email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def owners(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of object IDs of principals that will be granted ownership of the service principal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#owners ServicePrincipal#owners}
        '''
        result = self._values.get("owners")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preferred_single_sign_on_mode(self) -> typing.Optional[builtins.str]:
        '''The single sign-on mode configured for this application.

        Azure AD uses the preferred single sign-on mode to launch the application from Microsoft 365 or the Azure AD My Apps

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#preferred_single_sign_on_mode ServicePrincipal#preferred_single_sign_on_mode}
        '''
        result = self._values.get("preferred_single_sign_on_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_single_sign_on(
        self,
    ) -> typing.Optional["ServicePrincipalSamlSingleSignOn"]:
        '''saml_single_sign_on block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#saml_single_sign_on ServicePrincipal#saml_single_sign_on}
        '''
        result = self._values.get("saml_single_sign_on")
        return typing.cast(typing.Optional["ServicePrincipalSamlSingleSignOn"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of tags to apply to the service principal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#tags ServicePrincipal#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ServicePrincipalTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#timeouts ServicePrincipal#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ServicePrincipalTimeouts"], result)

    @builtins.property
    def use_existing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the resource will return an existing service principal instead of failing with an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#use_existing ServicePrincipal#use_existing}
        '''
        result = self._values.get("use_existing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicePrincipalConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalFeatureTags",
    jsii_struct_bases=[],
    name_mapping={
        "custom_single_sign_on": "customSingleSignOn",
        "enterprise": "enterprise",
        "gallery": "gallery",
        "hide": "hide",
    },
)
class ServicePrincipalFeatureTags:
    def __init__(
        self,
        *,
        custom_single_sign_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enterprise: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gallery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param custom_single_sign_on: Whether this service principal represents a custom SAML application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#custom_single_sign_on ServicePrincipal#custom_single_sign_on}
        :param enterprise: Whether this service principal represents an Enterprise Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#enterprise ServicePrincipal#enterprise}
        :param gallery: Whether this service principal represents a gallery application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#gallery ServicePrincipal#gallery}
        :param hide: Whether this app is invisible to users in My Apps and Office 365 Launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#hide ServicePrincipal#hide}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbc5be6055b5c5bfad7c31be3d527324351e88934b8ca3192f5b542b183c8b6)
            check_type(argname="argument custom_single_sign_on", value=custom_single_sign_on, expected_type=type_hints["custom_single_sign_on"])
            check_type(argname="argument enterprise", value=enterprise, expected_type=type_hints["enterprise"])
            check_type(argname="argument gallery", value=gallery, expected_type=type_hints["gallery"])
            check_type(argname="argument hide", value=hide, expected_type=type_hints["hide"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_single_sign_on is not None:
            self._values["custom_single_sign_on"] = custom_single_sign_on
        if enterprise is not None:
            self._values["enterprise"] = enterprise
        if gallery is not None:
            self._values["gallery"] = gallery
        if hide is not None:
            self._values["hide"] = hide

    @builtins.property
    def custom_single_sign_on(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this service principal represents a custom SAML application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#custom_single_sign_on ServicePrincipal#custom_single_sign_on}
        '''
        result = self._values.get("custom_single_sign_on")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enterprise(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this service principal represents an Enterprise Application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#enterprise ServicePrincipal#enterprise}
        '''
        result = self._values.get("enterprise")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gallery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this service principal represents a gallery application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#gallery ServicePrincipal#gallery}
        '''
        result = self._values.get("gallery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this app is invisible to users in My Apps and Office 365 Launcher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#hide ServicePrincipal#hide}
        '''
        result = self._values.get("hide")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicePrincipalFeatureTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicePrincipalFeatureTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalFeatureTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c4a74f6829faaff86161f138318b8ed54dba88f2413c4ed50c90e7df48b63bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServicePrincipalFeatureTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ef8319e64c5248d8978fb239830bcc408ef8430854a7e3d2b546f9e303df1b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServicePrincipalFeatureTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02aa7ab331498d0afefc47e46d2b48e0ee8e6a0cc219deb4bb92a1316529281)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85547ae145cce1cfb776df24f4addc93e9e112469ba27fa4f297335bf3c9fab8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__775ddf2286dade4ce3d1f62b31d6a873ae936ca59c56c5aef3ac611656aabd2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicePrincipalFeatureTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicePrincipalFeatureTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicePrincipalFeatureTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82188b1ede6010f30914e73a96877dcd9001607d93bee52edd1d91a6616de4aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServicePrincipalFeatureTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalFeatureTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6df7bd2bfc04e46ae37e0f4b72586253c8f5c6affc7028cdb803d2214659491)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCustomSingleSignOn")
    def reset_custom_single_sign_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSingleSignOn", []))

    @jsii.member(jsii_name="resetEnterprise")
    def reset_enterprise(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnterprise", []))

    @jsii.member(jsii_name="resetGallery")
    def reset_gallery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGallery", []))

    @jsii.member(jsii_name="resetHide")
    def reset_hide(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHide", []))

    @builtins.property
    @jsii.member(jsii_name="customSingleSignOnInput")
    def custom_single_sign_on_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customSingleSignOnInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseInput")
    def enterprise_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enterpriseInput"))

    @builtins.property
    @jsii.member(jsii_name="galleryInput")
    def gallery_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "galleryInput"))

    @builtins.property
    @jsii.member(jsii_name="hideInput")
    def hide_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hideInput"))

    @builtins.property
    @jsii.member(jsii_name="customSingleSignOn")
    def custom_single_sign_on(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customSingleSignOn"))

    @custom_single_sign_on.setter
    def custom_single_sign_on(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c97d2c8fe0455447846003c3c918126b90d4168741bbc2e52ee85e4d206904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customSingleSignOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enterprise")
    def enterprise(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enterprise"))

    @enterprise.setter
    def enterprise(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d672a531068198d71cba06e50c8e8006c68f26227dddb9443a597de30306c23c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterprise", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gallery")
    def gallery(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "gallery"))

    @gallery.setter
    def gallery(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10429aafe87d2556e8455f5d61b55d42b3150b9e65113ffc8b14b97c9df93835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gallery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hide")
    def hide(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hide"))

    @hide.setter
    def hide(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe88cfe41adbcf2847c822eb4852603ba518aae0b401448e58936f89198b91f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hide", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalFeatureTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalFeatureTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalFeatureTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec7deadae6daa59f66f38d56eea3e9d9e8777b8302961a14b2239402c3903d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalFeatures",
    jsii_struct_bases=[],
    name_mapping={
        "custom_single_sign_on_app": "customSingleSignOnApp",
        "enterprise_application": "enterpriseApplication",
        "gallery_application": "galleryApplication",
        "visible_to_users": "visibleToUsers",
    },
)
class ServicePrincipalFeatures:
    def __init__(
        self,
        *,
        custom_single_sign_on_app: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enterprise_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gallery_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        visible_to_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param custom_single_sign_on_app: Whether this service principal represents a custom SAML application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#custom_single_sign_on_app ServicePrincipal#custom_single_sign_on_app}
        :param enterprise_application: Whether this service principal represents an Enterprise Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#enterprise_application ServicePrincipal#enterprise_application}
        :param gallery_application: Whether this service principal represents a gallery application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#gallery_application ServicePrincipal#gallery_application}
        :param visible_to_users: Whether this app is visible to users in My Apps and Office 365 Launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#visible_to_users ServicePrincipal#visible_to_users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a93b37cf3d7e63d449701af5c680069d45e62d0df07f681496556660f3aff0)
            check_type(argname="argument custom_single_sign_on_app", value=custom_single_sign_on_app, expected_type=type_hints["custom_single_sign_on_app"])
            check_type(argname="argument enterprise_application", value=enterprise_application, expected_type=type_hints["enterprise_application"])
            check_type(argname="argument gallery_application", value=gallery_application, expected_type=type_hints["gallery_application"])
            check_type(argname="argument visible_to_users", value=visible_to_users, expected_type=type_hints["visible_to_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_single_sign_on_app is not None:
            self._values["custom_single_sign_on_app"] = custom_single_sign_on_app
        if enterprise_application is not None:
            self._values["enterprise_application"] = enterprise_application
        if gallery_application is not None:
            self._values["gallery_application"] = gallery_application
        if visible_to_users is not None:
            self._values["visible_to_users"] = visible_to_users

    @builtins.property
    def custom_single_sign_on_app(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this service principal represents a custom SAML application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#custom_single_sign_on_app ServicePrincipal#custom_single_sign_on_app}
        '''
        result = self._values.get("custom_single_sign_on_app")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enterprise_application(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this service principal represents an Enterprise Application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#enterprise_application ServicePrincipal#enterprise_application}
        '''
        result = self._values.get("enterprise_application")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gallery_application(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this service principal represents a gallery application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#gallery_application ServicePrincipal#gallery_application}
        '''
        result = self._values.get("gallery_application")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def visible_to_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this app is visible to users in My Apps and Office 365 Launcher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#visible_to_users ServicePrincipal#visible_to_users}
        '''
        result = self._values.get("visible_to_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicePrincipalFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicePrincipalFeaturesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalFeaturesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4469a6d3f8e8632bf903d2175b7e355ea52e7a3658b100c931fbe9abc94d2dce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServicePrincipalFeaturesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61eda1df6c745dc57e2cbedc3d7304beacab663836d5d6d360c905ea3453bd5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServicePrincipalFeaturesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2644b206218fcfe52b7dd759db78ccc8caec4c45fc1306ac173cf2027df991f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60927ad3fa3572572b378c29ba3d3278e2a6ce306de69e0a0f1babadfa88145f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc82b5987028a6b788fdee14578b379399f3fdc91027cf0b28384e21377dec8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicePrincipalFeatures]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicePrincipalFeatures]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicePrincipalFeatures]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3afb2aa143ece4b558d28ccc540db7178a54a5e5ac9b6dc645b75bdbf4b7e76e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServicePrincipalFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df184a4f8f57ae5c1705368fb64bd38bb7f0d824e4d61e40c7d909361109703b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCustomSingleSignOnApp")
    def reset_custom_single_sign_on_app(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSingleSignOnApp", []))

    @jsii.member(jsii_name="resetEnterpriseApplication")
    def reset_enterprise_application(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnterpriseApplication", []))

    @jsii.member(jsii_name="resetGalleryApplication")
    def reset_gallery_application(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGalleryApplication", []))

    @jsii.member(jsii_name="resetVisibleToUsers")
    def reset_visible_to_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibleToUsers", []))

    @builtins.property
    @jsii.member(jsii_name="customSingleSignOnAppInput")
    def custom_single_sign_on_app_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customSingleSignOnAppInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseApplicationInput")
    def enterprise_application_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enterpriseApplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="galleryApplicationInput")
    def gallery_application_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "galleryApplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="visibleToUsersInput")
    def visible_to_users_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "visibleToUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="customSingleSignOnApp")
    def custom_single_sign_on_app(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customSingleSignOnApp"))

    @custom_single_sign_on_app.setter
    def custom_single_sign_on_app(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161c6db8e3a1cb74a187967c1a64c670c2dc06d724f6bbda311e9ddd5d3c4851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customSingleSignOnApp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enterpriseApplication")
    def enterprise_application(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enterpriseApplication"))

    @enterprise_application.setter
    def enterprise_application(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53127cf87e6d943909939b0b91b0bdd6c9401e80af23535dcb3e0005d63d0289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseApplication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="galleryApplication")
    def gallery_application(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "galleryApplication"))

    @gallery_application.setter
    def gallery_application(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c1c8dcb263f2de25203119d6ef21d22e948d60d5ee8f5111ced608f3724fd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "galleryApplication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibleToUsers")
    def visible_to_users(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "visibleToUsers"))

    @visible_to_users.setter
    def visible_to_users(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa48ebf1c2ed9df7f7b668e9ba4ceacb8fa916f5a8323b4159809061075d2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibleToUsers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalFeatures]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalFeatures]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalFeatures]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f8c9e4b7cfc703ff55387e3b24ae19e916a66f5c3591081299542165504d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalOauth2PermissionScopes",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServicePrincipalOauth2PermissionScopes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicePrincipalOauth2PermissionScopes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicePrincipalOauth2PermissionScopesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalOauth2PermissionScopesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9483ec88400b5af3c478b20377a35b51b1c89c35753b1f0d140227aca18564f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServicePrincipalOauth2PermissionScopesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31687566a89df8e3d1a7462f3ba75264feb354a496f3cd680d4ec83af304137)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServicePrincipalOauth2PermissionScopesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b81d48d3c9e1aed34a0ecadc82a11edacdcc2cc1a35b1e2e5b18a3cf3f415ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff848b6abb24a8d082c131e1e2b41447ffd4dead18665882006db09676a3b094)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3fcabc9491383ae0d91001f7dec0cf547520be6493d02f0213e1393cfe9c049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServicePrincipalOauth2PermissionScopesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalOauth2PermissionScopesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1296986a1d095d4152cd01610789559fa7e714c99e4384a6634641bf1d5f26c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="adminConsentDescription")
    def admin_consent_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminConsentDescription"))

    @builtins.property
    @jsii.member(jsii_name="adminConsentDisplayName")
    def admin_consent_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminConsentDisplayName"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="userConsentDescription")
    def user_consent_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userConsentDescription"))

    @builtins.property
    @jsii.member(jsii_name="userConsentDisplayName")
    def user_consent_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userConsentDisplayName"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServicePrincipalOauth2PermissionScopes]:
        return typing.cast(typing.Optional[ServicePrincipalOauth2PermissionScopes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServicePrincipalOauth2PermissionScopes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ce4ee9b496541494918664f072c5b4c489f59b563aeb406b841acf2718b91b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalSamlSingleSignOn",
    jsii_struct_bases=[],
    name_mapping={"relay_state": "relayState"},
)
class ServicePrincipalSamlSingleSignOn:
    def __init__(self, *, relay_state: typing.Optional[builtins.str] = None) -> None:
        '''
        :param relay_state: The relative URI the service provider would redirect to after completion of the single sign-on flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#relay_state ServicePrincipal#relay_state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd71a55a7b8d5aede6b5712fbd5840983319f7e0d184edb651260aacd7797b20)
            check_type(argname="argument relay_state", value=relay_state, expected_type=type_hints["relay_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if relay_state is not None:
            self._values["relay_state"] = relay_state

    @builtins.property
    def relay_state(self) -> typing.Optional[builtins.str]:
        '''The relative URI the service provider would redirect to after completion of the single sign-on flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#relay_state ServicePrincipal#relay_state}
        '''
        result = self._values.get("relay_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicePrincipalSamlSingleSignOn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicePrincipalSamlSingleSignOnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalSamlSingleSignOnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63ba956e48eb7591fb993a0966230a895c2b2f1ae55adb93709b35b3b9eb825f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRelayState")
    def reset_relay_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelayState", []))

    @builtins.property
    @jsii.member(jsii_name="relayStateInput")
    def relay_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relayStateInput"))

    @builtins.property
    @jsii.member(jsii_name="relayState")
    def relay_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relayState"))

    @relay_state.setter
    def relay_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a53a9cc1942af68f69e18ba49e0fde380ca85ae4c6ef770565a7504956c372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relayState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServicePrincipalSamlSingleSignOn]:
        return typing.cast(typing.Optional[ServicePrincipalSamlSingleSignOn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServicePrincipalSamlSingleSignOn],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab65712a4d5b0b4c76c75e8e685c4984d16d2f1931996465b1e97554d51278c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ServicePrincipalTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#create ServicePrincipal#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#delete ServicePrincipal#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#read ServicePrincipal#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#update ServicePrincipal#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54852d59e37982061c864b849bc369b03ea714cf65135c6d6d6c2ba629dbe949)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#create ServicePrincipal#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#delete ServicePrincipal#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#read ServicePrincipal#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/service_principal#update ServicePrincipal#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicePrincipalTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicePrincipalTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.servicePrincipal.ServicePrincipalTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5b0c180c785f242447cc27e1fa7dce6aa100950c5b68af0341751de41537262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04d03690874b3c8eb5ca5766370386f55d0109e2c2c603fe6898f5a880fdec07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904988df0b56df7d5a717fb343c65d7ed086af7e24eb551c476c4f6943be6258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62c901fe3c50490b72d138dcaebad1317a19acde04a6cedc2c980feae426cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ec0e58f302bc7e290f78271c126c5657e14b98b12fd946eaec71081540b026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7986b8f4619cb93aba144b4094d1079302b159e7b61a144fc3ccf65e51d04af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServicePrincipal",
    "ServicePrincipalAppRoles",
    "ServicePrincipalAppRolesList",
    "ServicePrincipalAppRolesOutputReference",
    "ServicePrincipalConfig",
    "ServicePrincipalFeatureTags",
    "ServicePrincipalFeatureTagsList",
    "ServicePrincipalFeatureTagsOutputReference",
    "ServicePrincipalFeatures",
    "ServicePrincipalFeaturesList",
    "ServicePrincipalFeaturesOutputReference",
    "ServicePrincipalOauth2PermissionScopes",
    "ServicePrincipalOauth2PermissionScopesList",
    "ServicePrincipalOauth2PermissionScopesOutputReference",
    "ServicePrincipalSamlSingleSignOn",
    "ServicePrincipalSamlSingleSignOnOutputReference",
    "ServicePrincipalTimeouts",
    "ServicePrincipalTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__274f8fc4f064d72d41fce04f6659ee4ef1986f78ff3f6aa47dd0fcfd20abad5d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    client_id: builtins.str,
    account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    app_role_assignment_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServicePrincipalFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    feature_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServicePrincipalFeatureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    login_url: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    notification_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_single_sign_on_mode: typing.Optional[builtins.str] = None,
    saml_single_sign_on: typing.Optional[typing.Union[ServicePrincipalSamlSingleSignOn, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ServicePrincipalTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_existing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__39536cddd93408bacdd298f3eab07c2cde811144c80fcf892c4e114f9b25e3b8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aed6d814f22146e031571c469ddbd21bb42b38d93db8915d4cd5ae2e3a8dbc1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServicePrincipalFeatures, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40a2f85d8abcbdc2fab1796027a8cdcc3f9b1e2e45aeb8a1f8d8dff4ee70a63(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServicePrincipalFeatureTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749dada87d0affa006dfd2132479eb016eaa8e23517dcce094616ec924f14c76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8c1e903f659584ece5f1957e52ffc47a92c67f854e14de4ac9c4b0e1a1fa86(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923fac015c80c70fa3c07ba199bb88b0cac551ab4dbd096a60cafaee33dd731e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00e7b06514ff70102bb49c21ff217f1bc574e649fea59ab5738c47562b84578(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66e6b08670d138a1351f1aff245b1ba806cc37d8b076471f4cfe3730b265409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42273f6aa461e9f828d873e13ef1aa2f81bd3fd276162692e12db23ab53c276a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61c32cf05141d28d20ae7353e5108fd3a9c804a2fa1141a6e8cc033749e6c0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9741200ed9808aff7d90ad617cdf680f317359cc9db89f7eb6fe8224322367d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9255e3f25c07018a4ef144b2403045622716d6f85c3605f8aa7220b3312c36(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c75997ad0e8c33142488fc98aaa304c9ed8001ee5810d45416a6b6a9bdf082(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c982a8007aa915361f6cc33c8679e892c7da035b60bfe38112829fa55334029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866567d15831790b6d0168597eb597bb7d7cc7a3f961a2c2799753ca57da4b44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573e8bb2797b1147f97be0bc6d2ec438b8b2e96b82b8d36425c265e650d5e5aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988a5add5c74f4b653100bc4c796574a7a09d2cae98f2b2b3dd5d2a44248c39f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14fe13d372dfdc136c6d6022acd85839761aea8e479e721adf2be891f778d6a2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0366222b03c5554e69c56cfea773df9782ef6cc8e0b72b8c2219ce4ede8015dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9a64497a593693d0326e3a3b76f6fb091f4d7853fe51435c4570fe370616d9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e4c54464edea322f0505c735b445cad8379233d545360cdfe97c3ad8eaab67(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dddb8b720f08984bf25d4b1d950a5df4a8c7216cbf47b959e5443384e2c1876(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e09ace7eee80f506a2aa8d6724b692e9dddb515567521cba6e54bf0a3f2987a(
    value: typing.Optional[ServicePrincipalAppRoles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d990a645589140ab9a7b3a68ab4efe8ecb5fe876ec94a17d38b23a8f52fb073(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_id: builtins.str,
    account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    app_role_assignment_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServicePrincipalFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    feature_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServicePrincipalFeatureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    login_url: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    notification_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_single_sign_on_mode: typing.Optional[builtins.str] = None,
    saml_single_sign_on: typing.Optional[typing.Union[ServicePrincipalSamlSingleSignOn, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ServicePrincipalTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_existing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbc5be6055b5c5bfad7c31be3d527324351e88934b8ca3192f5b542b183c8b6(
    *,
    custom_single_sign_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enterprise: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gallery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4a74f6829faaff86161f138318b8ed54dba88f2413c4ed50c90e7df48b63bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ef8319e64c5248d8978fb239830bcc408ef8430854a7e3d2b546f9e303df1b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02aa7ab331498d0afefc47e46d2b48e0ee8e6a0cc219deb4bb92a1316529281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85547ae145cce1cfb776df24f4addc93e9e112469ba27fa4f297335bf3c9fab8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775ddf2286dade4ce3d1f62b31d6a873ae936ca59c56c5aef3ac611656aabd2b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82188b1ede6010f30914e73a96877dcd9001607d93bee52edd1d91a6616de4aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicePrincipalFeatureTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6df7bd2bfc04e46ae37e0f4b72586253c8f5c6affc7028cdb803d2214659491(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c97d2c8fe0455447846003c3c918126b90d4168741bbc2e52ee85e4d206904(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d672a531068198d71cba06e50c8e8006c68f26227dddb9443a597de30306c23c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10429aafe87d2556e8455f5d61b55d42b3150b9e65113ffc8b14b97c9df93835(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe88cfe41adbcf2847c822eb4852603ba518aae0b401448e58936f89198b91f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec7deadae6daa59f66f38d56eea3e9d9e8777b8302961a14b2239402c3903d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalFeatureTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a93b37cf3d7e63d449701af5c680069d45e62d0df07f681496556660f3aff0(
    *,
    custom_single_sign_on_app: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enterprise_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gallery_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    visible_to_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4469a6d3f8e8632bf903d2175b7e355ea52e7a3658b100c931fbe9abc94d2dce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61eda1df6c745dc57e2cbedc3d7304beacab663836d5d6d360c905ea3453bd5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2644b206218fcfe52b7dd759db78ccc8caec4c45fc1306ac173cf2027df991f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60927ad3fa3572572b378c29ba3d3278e2a6ce306de69e0a0f1babadfa88145f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc82b5987028a6b788fdee14578b379399f3fdc91027cf0b28384e21377dec8d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afb2aa143ece4b558d28ccc540db7178a54a5e5ac9b6dc645b75bdbf4b7e76e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicePrincipalFeatures]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df184a4f8f57ae5c1705368fb64bd38bb7f0d824e4d61e40c7d909361109703b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161c6db8e3a1cb74a187967c1a64c670c2dc06d724f6bbda311e9ddd5d3c4851(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53127cf87e6d943909939b0b91b0bdd6c9401e80af23535dcb3e0005d63d0289(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c1c8dcb263f2de25203119d6ef21d22e948d60d5ee8f5111ced608f3724fd8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa48ebf1c2ed9df7f7b668e9ba4ceacb8fa916f5a8323b4159809061075d2ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f8c9e4b7cfc703ff55387e3b24ae19e916a66f5c3591081299542165504d46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalFeatures]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9483ec88400b5af3c478b20377a35b51b1c89c35753b1f0d140227aca18564f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31687566a89df8e3d1a7462f3ba75264feb354a496f3cd680d4ec83af304137(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b81d48d3c9e1aed34a0ecadc82a11edacdcc2cc1a35b1e2e5b18a3cf3f415ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff848b6abb24a8d082c131e1e2b41447ffd4dead18665882006db09676a3b094(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fcabc9491383ae0d91001f7dec0cf547520be6493d02f0213e1393cfe9c049(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1296986a1d095d4152cd01610789559fa7e714c99e4384a6634641bf1d5f26c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ce4ee9b496541494918664f072c5b4c489f59b563aeb406b841acf2718b91b(
    value: typing.Optional[ServicePrincipalOauth2PermissionScopes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd71a55a7b8d5aede6b5712fbd5840983319f7e0d184edb651260aacd7797b20(
    *,
    relay_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ba956e48eb7591fb993a0966230a895c2b2f1ae55adb93709b35b3b9eb825f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a53a9cc1942af68f69e18ba49e0fde380ca85ae4c6ef770565a7504956c372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab65712a4d5b0b4c76c75e8e685c4984d16d2f1931996465b1e97554d51278c(
    value: typing.Optional[ServicePrincipalSamlSingleSignOn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54852d59e37982061c864b849bc369b03ea714cf65135c6d6d6c2ba629dbe949(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b0c180c785f242447cc27e1fa7dce6aa100950c5b68af0341751de41537262(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d03690874b3c8eb5ca5766370386f55d0109e2c2c603fe6898f5a880fdec07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904988df0b56df7d5a717fb343c65d7ed086af7e24eb551c476c4f6943be6258(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62c901fe3c50490b72d138dcaebad1317a19acde04a6cedc2c980feae426cb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ec0e58f302bc7e290f78271c126c5657e14b98b12fd946eaec71081540b026(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7986b8f4619cb93aba144b4094d1079302b159e7b61a144fc3ccf65e51d04af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServicePrincipalTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
