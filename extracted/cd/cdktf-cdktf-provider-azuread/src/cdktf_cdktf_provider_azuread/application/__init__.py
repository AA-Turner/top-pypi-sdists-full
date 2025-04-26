r'''
# `azuread_application`

Refer to the Terraform Registry for docs: [`azuread_application`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application).
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


class Application(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.Application",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application azuread_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        api: typing.Optional[typing.Union["ApplicationApi", typing.Dict[builtins.str, typing.Any]]] = None,
        app_role: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationAppRole", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        device_only_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fallback_public_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        feature_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationFeatureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        group_membership_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        identifier_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logo_image: typing.Optional[builtins.str] = None,
        marketing_url: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        oauth2_post_response_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optional_claims: typing.Optional[typing.Union["ApplicationOptionalClaims", typing.Dict[builtins.str, typing.Any]]] = None,
        owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        password: typing.Optional[typing.Union["ApplicationPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_duplicate_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        privacy_statement_url: typing.Optional[builtins.str] = None,
        public_client: typing.Optional[typing.Union["ApplicationPublicClient", typing.Dict[builtins.str, typing.Any]]] = None,
        required_resource_access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationRequiredResourceAccess", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_management_reference: typing.Optional[builtins.str] = None,
        sign_in_audience: typing.Optional[builtins.str] = None,
        single_page_application: typing.Optional[typing.Union["ApplicationSinglePageApplication", typing.Dict[builtins.str, typing.Any]]] = None,
        support_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        template_id: typing.Optional[builtins.str] = None,
        terms_of_service_url: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        web: typing.Optional[typing.Union["ApplicationWeb", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application azuread_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The display name for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#display_name Application#display_name}
        :param api: api block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#api Application#api}
        :param app_role: app_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#app_role Application#app_role}
        :param description: Description of the application as shown to end users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#description Application#description}
        :param device_only_auth_enabled: Specifies whether this application supports device authentication without a user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#device_only_auth_enabled Application#device_only_auth_enabled}
        :param fallback_public_client_enabled: Specifies whether the application is a public client. Appropriate for apps using token grant flows that don't use a redirect URI Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#fallback_public_client_enabled Application#fallback_public_client_enabled}
        :param feature_tags: feature_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#feature_tags Application#feature_tags}
        :param group_membership_claims: Configures the ``groups`` claim issued in a user or OAuth 2.0 access token that the app expects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#group_membership_claims Application#group_membership_claims}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id Application#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identifier_uris: The user-defined URI(s) that uniquely identify an application within its Azure AD tenant, or within a verified custom domain if the application is multi-tenant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#identifier_uris Application#identifier_uris}
        :param logo_image: Base64 encoded logo image in gif, png or jpeg format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#logo_image Application#logo_image}
        :param marketing_url: URL of the application's marketing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#marketing_url Application#marketing_url}
        :param notes: User-specified notes relevant for the management of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#notes Application#notes}
        :param oauth2_post_response_required: Specifies whether, as part of OAuth 2.0 token requests, Azure AD allows POST requests, as opposed to GET requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#oauth2_post_response_required Application#oauth2_post_response_required}
        :param optional_claims: optional_claims block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#optional_claims Application#optional_claims}
        :param owners: A list of object IDs of principals that will be granted ownership of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#owners Application#owners}
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#password Application#password}
        :param prevent_duplicate_names: If ``true``, will return an error if an existing application is found with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#prevent_duplicate_names Application#prevent_duplicate_names}
        :param privacy_statement_url: URL of the application's privacy statement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#privacy_statement_url Application#privacy_statement_url}
        :param public_client: public_client block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#public_client Application#public_client}
        :param required_resource_access: required_resource_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#required_resource_access Application#required_resource_access}
        :param service_management_reference: References application or service contact information from a Service or Asset Management database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#service_management_reference Application#service_management_reference}
        :param sign_in_audience: The Microsoft account types that are supported for the current application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#sign_in_audience Application#sign_in_audience}
        :param single_page_application: single_page_application block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#single_page_application Application#single_page_application}
        :param support_url: URL of the application's support page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#support_url Application#support_url}
        :param tags: A set of tags to apply to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#tags Application#tags}
        :param template_id: Unique ID of the application template from which this application is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#template_id Application#template_id}
        :param terms_of_service_url: URL of the application's terms of service statement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#terms_of_service_url Application#terms_of_service_url}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#timeouts Application#timeouts}
        :param web: web block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#web Application#web}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598797ffd1c1da722948df1ca1dc3b8215b03ddbf0fe97b2a57729b95394ccfa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApplicationConfig(
            display_name=display_name,
            api=api,
            app_role=app_role,
            description=description,
            device_only_auth_enabled=device_only_auth_enabled,
            fallback_public_client_enabled=fallback_public_client_enabled,
            feature_tags=feature_tags,
            group_membership_claims=group_membership_claims,
            id=id,
            identifier_uris=identifier_uris,
            logo_image=logo_image,
            marketing_url=marketing_url,
            notes=notes,
            oauth2_post_response_required=oauth2_post_response_required,
            optional_claims=optional_claims,
            owners=owners,
            password=password,
            prevent_duplicate_names=prevent_duplicate_names,
            privacy_statement_url=privacy_statement_url,
            public_client=public_client,
            required_resource_access=required_resource_access,
            service_management_reference=service_management_reference,
            sign_in_audience=sign_in_audience,
            single_page_application=single_page_application,
            support_url=support_url,
            tags=tags,
            template_id=template_id,
            terms_of_service_url=terms_of_service_url,
            timeouts=timeouts,
            web=web,
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
        '''Generates CDKTF code for importing a Application resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Application to import.
        :param import_from_id: The id of the existing Application that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Application to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5429ed8a97b3f6264afd5e685eb2c5c1b29b06522ca4d48461060a6f297afcdc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApi")
    def put_api(
        self,
        *,
        known_client_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        mapped_claims_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oauth2_permission_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationApiOauth2PermissionScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
        requested_access_token_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param known_client_applications: Used for bundling consent if you have a solution that contains two parts: a client app and a custom web API app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#known_client_applications Application#known_client_applications}
        :param mapped_claims_enabled: Allows an application to use claims mapping without specifying a custom signing key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#mapped_claims_enabled Application#mapped_claims_enabled}
        :param oauth2_permission_scope: oauth2_permission_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#oauth2_permission_scope Application#oauth2_permission_scope}
        :param requested_access_token_version: The access token version expected by this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#requested_access_token_version Application#requested_access_token_version}
        '''
        value = ApplicationApi(
            known_client_applications=known_client_applications,
            mapped_claims_enabled=mapped_claims_enabled,
            oauth2_permission_scope=oauth2_permission_scope,
            requested_access_token_version=requested_access_token_version,
        )

        return typing.cast(None, jsii.invoke(self, "putApi", [value]))

    @jsii.member(jsii_name="putAppRole")
    def put_app_role(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationAppRole", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f79eaaab621d89c408e6bb27118292445556e36738325b6f7241217958e1e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAppRole", [value]))

    @jsii.member(jsii_name="putFeatureTags")
    def put_feature_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationFeatureTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502f85d7583c461ebe66f09b22aa9d4d395bf6519afa246264da95f213ba7fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatureTags", [value]))

    @jsii.member(jsii_name="putOptionalClaims")
    def put_optional_claims(
        self,
        *,
        access_token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationOptionalClaimsAccessToken", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id_token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationOptionalClaimsIdToken", typing.Dict[builtins.str, typing.Any]]]]] = None,
        saml2_token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationOptionalClaimsSaml2Token", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_token: access_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#access_token Application#access_token}
        :param id_token: id_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id_token Application#id_token}
        :param saml2_token: saml2_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#saml2_token Application#saml2_token}
        '''
        value = ApplicationOptionalClaims(
            access_token=access_token, id_token=id_token, saml2_token=saml2_token
        )

        return typing.cast(None, jsii.invoke(self, "putOptionalClaims", [value]))

    @jsii.member(jsii_name="putPassword")
    def put_password(
        self,
        *,
        display_name: builtins.str,
        end_date: typing.Optional[builtins.str] = None,
        start_date: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: A display name for the password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#display_name Application#display_name}
        :param end_date: The end date until which the password is valid, formatted as an RFC3339 date string (e.g. ``2018-01-01T01:02:03Z``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#end_date Application#end_date}
        :param start_date: The start date from which the password is valid, formatted as an RFC3339 date string (e.g. ``2018-01-01T01:02:03Z``). If this isn't specified, the current date is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#start_date Application#start_date}
        '''
        value = ApplicationPassword(
            display_name=display_name, end_date=end_date, start_date=start_date
        )

        return typing.cast(None, jsii.invoke(self, "putPassword", [value]))

    @jsii.member(jsii_name="putPublicClient")
    def put_public_client(
        self,
        *,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param redirect_uris: The URLs where user tokens are sent for sign-in, or the redirect URIs where OAuth 2.0 authorization codes and access tokens are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#redirect_uris Application#redirect_uris}
        '''
        value = ApplicationPublicClient(redirect_uris=redirect_uris)

        return typing.cast(None, jsii.invoke(self, "putPublicClient", [value]))

    @jsii.member(jsii_name="putRequiredResourceAccess")
    def put_required_resource_access(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationRequiredResourceAccess", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd13071039aa750678fe8748b949bf633bcd3142a86ecdf930ddab86da763a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequiredResourceAccess", [value]))

    @jsii.member(jsii_name="putSinglePageApplication")
    def put_single_page_application(
        self,
        *,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param redirect_uris: The URLs where user tokens are sent for sign-in, or the redirect URIs where OAuth 2.0 authorization codes and access tokens are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#redirect_uris Application#redirect_uris}
        '''
        value = ApplicationSinglePageApplication(redirect_uris=redirect_uris)

        return typing.cast(None, jsii.invoke(self, "putSinglePageApplication", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#create Application#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#delete Application#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#read Application#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#update Application#update}.
        '''
        value = ApplicationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWeb")
    def put_web(
        self,
        *,
        homepage_url: typing.Optional[builtins.str] = None,
        implicit_grant: typing.Optional[typing.Union["ApplicationWebImplicitGrant", typing.Dict[builtins.str, typing.Any]]] = None,
        logout_url: typing.Optional[builtins.str] = None,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param homepage_url: Home page or landing page of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#homepage_url Application#homepage_url}
        :param implicit_grant: implicit_grant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#implicit_grant Application#implicit_grant}
        :param logout_url: The URL that will be used by Microsoft's authorization service to sign out a user using front-channel, back-channel or SAML logout protocols. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#logout_url Application#logout_url}
        :param redirect_uris: The URLs where user tokens are sent for sign-in, or the redirect URIs where OAuth 2.0 authorization codes and access tokens are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#redirect_uris Application#redirect_uris}
        '''
        value = ApplicationWeb(
            homepage_url=homepage_url,
            implicit_grant=implicit_grant,
            logout_url=logout_url,
            redirect_uris=redirect_uris,
        )

        return typing.cast(None, jsii.invoke(self, "putWeb", [value]))

    @jsii.member(jsii_name="resetApi")
    def reset_api(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApi", []))

    @jsii.member(jsii_name="resetAppRole")
    def reset_app_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppRole", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDeviceOnlyAuthEnabled")
    def reset_device_only_auth_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceOnlyAuthEnabled", []))

    @jsii.member(jsii_name="resetFallbackPublicClientEnabled")
    def reset_fallback_public_client_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFallbackPublicClientEnabled", []))

    @jsii.member(jsii_name="resetFeatureTags")
    def reset_feature_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureTags", []))

    @jsii.member(jsii_name="resetGroupMembershipClaims")
    def reset_group_membership_claims(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupMembershipClaims", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentifierUris")
    def reset_identifier_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentifierUris", []))

    @jsii.member(jsii_name="resetLogoImage")
    def reset_logo_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogoImage", []))

    @jsii.member(jsii_name="resetMarketingUrl")
    def reset_marketing_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketingUrl", []))

    @jsii.member(jsii_name="resetNotes")
    def reset_notes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotes", []))

    @jsii.member(jsii_name="resetOauth2PostResponseRequired")
    def reset_oauth2_post_response_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2PostResponseRequired", []))

    @jsii.member(jsii_name="resetOptionalClaims")
    def reset_optional_claims(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptionalClaims", []))

    @jsii.member(jsii_name="resetOwners")
    def reset_owners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwners", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPreventDuplicateNames")
    def reset_prevent_duplicate_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventDuplicateNames", []))

    @jsii.member(jsii_name="resetPrivacyStatementUrl")
    def reset_privacy_statement_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivacyStatementUrl", []))

    @jsii.member(jsii_name="resetPublicClient")
    def reset_public_client(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicClient", []))

    @jsii.member(jsii_name="resetRequiredResourceAccess")
    def reset_required_resource_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredResourceAccess", []))

    @jsii.member(jsii_name="resetServiceManagementReference")
    def reset_service_management_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceManagementReference", []))

    @jsii.member(jsii_name="resetSignInAudience")
    def reset_sign_in_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignInAudience", []))

    @jsii.member(jsii_name="resetSinglePageApplication")
    def reset_single_page_application(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSinglePageApplication", []))

    @jsii.member(jsii_name="resetSupportUrl")
    def reset_support_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportUrl", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTemplateId")
    def reset_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateId", []))

    @jsii.member(jsii_name="resetTermsOfServiceUrl")
    def reset_terms_of_service_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTermsOfServiceUrl", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWeb")
    def reset_web(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeb", []))

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
    @jsii.member(jsii_name="api")
    def api(self) -> "ApplicationApiOutputReference":
        return typing.cast("ApplicationApiOutputReference", jsii.get(self, "api"))

    @builtins.property
    @jsii.member(jsii_name="appRole")
    def app_role(self) -> "ApplicationAppRoleList":
        return typing.cast("ApplicationAppRoleList", jsii.get(self, "appRole"))

    @builtins.property
    @jsii.member(jsii_name="appRoleIds")
    def app_role_ids(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "appRoleIds"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="disabledByMicrosoft")
    def disabled_by_microsoft(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disabledByMicrosoft"))

    @builtins.property
    @jsii.member(jsii_name="featureTags")
    def feature_tags(self) -> "ApplicationFeatureTagsList":
        return typing.cast("ApplicationFeatureTagsList", jsii.get(self, "featureTags"))

    @builtins.property
    @jsii.member(jsii_name="logoUrl")
    def logo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoUrl"))

    @builtins.property
    @jsii.member(jsii_name="oauth2PermissionScopeIds")
    def oauth2_permission_scope_ids(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "oauth2PermissionScopeIds"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="optionalClaims")
    def optional_claims(self) -> "ApplicationOptionalClaimsOutputReference":
        return typing.cast("ApplicationOptionalClaimsOutputReference", jsii.get(self, "optionalClaims"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> "ApplicationPasswordOutputReference":
        return typing.cast("ApplicationPasswordOutputReference", jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="publicClient")
    def public_client(self) -> "ApplicationPublicClientOutputReference":
        return typing.cast("ApplicationPublicClientOutputReference", jsii.get(self, "publicClient"))

    @builtins.property
    @jsii.member(jsii_name="publisherDomain")
    def publisher_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisherDomain"))

    @builtins.property
    @jsii.member(jsii_name="requiredResourceAccess")
    def required_resource_access(self) -> "ApplicationRequiredResourceAccessList":
        return typing.cast("ApplicationRequiredResourceAccessList", jsii.get(self, "requiredResourceAccess"))

    @builtins.property
    @jsii.member(jsii_name="singlePageApplication")
    def single_page_application(
        self,
    ) -> "ApplicationSinglePageApplicationOutputReference":
        return typing.cast("ApplicationSinglePageApplicationOutputReference", jsii.get(self, "singlePageApplication"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApplicationTimeoutsOutputReference":
        return typing.cast("ApplicationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="web")
    def web(self) -> "ApplicationWebOutputReference":
        return typing.cast("ApplicationWebOutputReference", jsii.get(self, "web"))

    @builtins.property
    @jsii.member(jsii_name="apiInput")
    def api_input(self) -> typing.Optional["ApplicationApi"]:
        return typing.cast(typing.Optional["ApplicationApi"], jsii.get(self, "apiInput"))

    @builtins.property
    @jsii.member(jsii_name="appRoleInput")
    def app_role_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationAppRole"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationAppRole"]]], jsii.get(self, "appRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceOnlyAuthEnabledInput")
    def device_only_auth_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deviceOnlyAuthEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fallbackPublicClientEnabledInput")
    def fallback_public_client_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fallbackPublicClientEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="featureTagsInput")
    def feature_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationFeatureTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationFeatureTags"]]], jsii.get(self, "featureTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupMembershipClaimsInput")
    def group_membership_claims_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupMembershipClaimsInput"))

    @builtins.property
    @jsii.member(jsii_name="identifierUrisInput")
    def identifier_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identifierUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logoImageInput")
    def logo_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoImageInput"))

    @builtins.property
    @jsii.member(jsii_name="marketingUrlInput")
    def marketing_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "marketingUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="notesInput")
    def notes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notesInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2PostResponseRequiredInput")
    def oauth2_post_response_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "oauth2PostResponseRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalClaimsInput")
    def optional_claims_input(self) -> typing.Optional["ApplicationOptionalClaims"]:
        return typing.cast(typing.Optional["ApplicationOptionalClaims"], jsii.get(self, "optionalClaimsInput"))

    @builtins.property
    @jsii.member(jsii_name="ownersInput")
    def owners_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ownersInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional["ApplicationPassword"]:
        return typing.cast(typing.Optional["ApplicationPassword"], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="preventDuplicateNamesInput")
    def prevent_duplicate_names_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventDuplicateNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="privacyStatementUrlInput")
    def privacy_statement_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privacyStatementUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="publicClientInput")
    def public_client_input(self) -> typing.Optional["ApplicationPublicClient"]:
        return typing.cast(typing.Optional["ApplicationPublicClient"], jsii.get(self, "publicClientInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredResourceAccessInput")
    def required_resource_access_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationRequiredResourceAccess"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationRequiredResourceAccess"]]], jsii.get(self, "requiredResourceAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceManagementReferenceInput")
    def service_management_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceManagementReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="signInAudienceInput")
    def sign_in_audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signInAudienceInput"))

    @builtins.property
    @jsii.member(jsii_name="singlePageApplicationInput")
    def single_page_application_input(
        self,
    ) -> typing.Optional["ApplicationSinglePageApplication"]:
        return typing.cast(typing.Optional["ApplicationSinglePageApplication"], jsii.get(self, "singlePageApplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="supportUrlInput")
    def support_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="templateIdInput")
    def template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="termsOfServiceUrlInput")
    def terms_of_service_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "termsOfServiceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApplicationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApplicationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="webInput")
    def web_input(self) -> typing.Optional["ApplicationWeb"]:
        return typing.cast(typing.Optional["ApplicationWeb"], jsii.get(self, "webInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c795272e61ef9ce89935d4fc838f774b855aacde02acefa7d59f02524add22d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceOnlyAuthEnabled")
    def device_only_auth_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deviceOnlyAuthEnabled"))

    @device_only_auth_enabled.setter
    def device_only_auth_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c87aeca713f24baed1508cd10f366ce3ca94900e89b60dc7a5858d8812bf5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceOnlyAuthEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd7509b000b9ecb129eba618849abc0005887c4c1e2fb8f5fa4e4fe723433c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fallbackPublicClientEnabled")
    def fallback_public_client_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fallbackPublicClientEnabled"))

    @fallback_public_client_enabled.setter
    def fallback_public_client_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c08ce8edc55f00d9b52244d03a54e7561027a481b695fbed14ac5062387a08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fallbackPublicClientEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupMembershipClaims")
    def group_membership_claims(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupMembershipClaims"))

    @group_membership_claims.setter
    def group_membership_claims(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__065bc0280592fe47a24a360cef92e406e0f5c3c08a56a7780832fd5d634706cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupMembershipClaims", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921b4bb8935a9944638df928163c59b0bab5c4cc9b95a5877fe1d61d2a415e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identifierUris")
    def identifier_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identifierUris"))

    @identifier_uris.setter
    def identifier_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86baa584f1edbdbc002485f50971e4a52d0ae1d80ca7599af1471ada4d428bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identifierUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logoImage")
    def logo_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoImage"))

    @logo_image.setter
    def logo_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2e657cf61c46092375cd2f65f1566fe3c3c1e58b76398ae2ff62784c842d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="marketingUrl")
    def marketing_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketingUrl"))

    @marketing_url.setter
    def marketing_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b404e4e2b161a2c22c614f6fa9597156db0eec6e38d2d91639bedddda6353ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "marketingUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notes"))

    @notes.setter
    def notes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e54250879c450e1f3920437e79a82ad57daa4c8b8af2c7e422d7518d1809a94f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2PostResponseRequired")
    def oauth2_post_response_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "oauth2PostResponseRequired"))

    @oauth2_post_response_required.setter
    def oauth2_post_response_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e77ff5e726620b62a8192c8f66834e2884dfcd788940dfdb175ed6617a8fb78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2PostResponseRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owners")
    def owners(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "owners"))

    @owners.setter
    def owners(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49bfe04e31875031895be1752580f00012a8265540b3363d7c79df64e1e21622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owners", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventDuplicateNames")
    def prevent_duplicate_names(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventDuplicateNames"))

    @prevent_duplicate_names.setter
    def prevent_duplicate_names(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe5b8d15a8736b8d334b391348cdde2c64c015de022ac0486580b07887c12a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventDuplicateNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privacyStatementUrl")
    def privacy_statement_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacyStatementUrl"))

    @privacy_statement_url.setter
    def privacy_statement_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2abe2527a40053f36c39edc05474ae1ecd773193611946ac0e2567b524be8def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privacyStatementUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceManagementReference")
    def service_management_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceManagementReference"))

    @service_management_reference.setter
    def service_management_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3379a935de6279c322ac6bad07850eb5afa2c82d99a279ad07a616dc069a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceManagementReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signInAudience")
    def sign_in_audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signInAudience"))

    @sign_in_audience.setter
    def sign_in_audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9aa5403d0d67c71116c7dda47a66970883add862c75c0e4179b4df2d3d42d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signInAudience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportUrl")
    def support_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportUrl"))

    @support_url.setter
    def support_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88c7e24fa536fe013f7a05ae1a9a969a285cf3629f02713c1de7c0a7303caf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805bba6ff5ddea670883d37c1d2594c8b2e6ebb43c926832532965585e2d4e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateId"))

    @template_id.setter
    def template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f385de9a4eb108e00cbd887a3f8a3fb0cd0ea9c95e0e59ae01ab3ce124d0c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="termsOfServiceUrl")
    def terms_of_service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "termsOfServiceUrl"))

    @terms_of_service_url.setter
    def terms_of_service_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5692c6383c3f765867d3dfa2baae310f6790b402e8b47a25a170dcefacda5129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "termsOfServiceUrl", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationApi",
    jsii_struct_bases=[],
    name_mapping={
        "known_client_applications": "knownClientApplications",
        "mapped_claims_enabled": "mappedClaimsEnabled",
        "oauth2_permission_scope": "oauth2PermissionScope",
        "requested_access_token_version": "requestedAccessTokenVersion",
    },
)
class ApplicationApi:
    def __init__(
        self,
        *,
        known_client_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        mapped_claims_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oauth2_permission_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationApiOauth2PermissionScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
        requested_access_token_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param known_client_applications: Used for bundling consent if you have a solution that contains two parts: a client app and a custom web API app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#known_client_applications Application#known_client_applications}
        :param mapped_claims_enabled: Allows an application to use claims mapping without specifying a custom signing key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#mapped_claims_enabled Application#mapped_claims_enabled}
        :param oauth2_permission_scope: oauth2_permission_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#oauth2_permission_scope Application#oauth2_permission_scope}
        :param requested_access_token_version: The access token version expected by this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#requested_access_token_version Application#requested_access_token_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13883a3dbb678cb13a448982c307eebad77973ede01c78c63668b37438c4693d)
            check_type(argname="argument known_client_applications", value=known_client_applications, expected_type=type_hints["known_client_applications"])
            check_type(argname="argument mapped_claims_enabled", value=mapped_claims_enabled, expected_type=type_hints["mapped_claims_enabled"])
            check_type(argname="argument oauth2_permission_scope", value=oauth2_permission_scope, expected_type=type_hints["oauth2_permission_scope"])
            check_type(argname="argument requested_access_token_version", value=requested_access_token_version, expected_type=type_hints["requested_access_token_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if known_client_applications is not None:
            self._values["known_client_applications"] = known_client_applications
        if mapped_claims_enabled is not None:
            self._values["mapped_claims_enabled"] = mapped_claims_enabled
        if oauth2_permission_scope is not None:
            self._values["oauth2_permission_scope"] = oauth2_permission_scope
        if requested_access_token_version is not None:
            self._values["requested_access_token_version"] = requested_access_token_version

    @builtins.property
    def known_client_applications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Used for bundling consent if you have a solution that contains two parts: a client app and a custom web API app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#known_client_applications Application#known_client_applications}
        '''
        result = self._values.get("known_client_applications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mapped_claims_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows an application to use claims mapping without specifying a custom signing key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#mapped_claims_enabled Application#mapped_claims_enabled}
        '''
        result = self._values.get("mapped_claims_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def oauth2_permission_scope(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationApiOauth2PermissionScope"]]]:
        '''oauth2_permission_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#oauth2_permission_scope Application#oauth2_permission_scope}
        '''
        result = self._values.get("oauth2_permission_scope")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationApiOauth2PermissionScope"]]], result)

    @builtins.property
    def requested_access_token_version(self) -> typing.Optional[jsii.Number]:
        '''The access token version expected by this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#requested_access_token_version Application#requested_access_token_version}
        '''
        result = self._values.get("requested_access_token_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationApi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationApiOauth2PermissionScope",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "admin_consent_description": "adminConsentDescription",
        "admin_consent_display_name": "adminConsentDisplayName",
        "enabled": "enabled",
        "type": "type",
        "user_consent_description": "userConsentDescription",
        "user_consent_display_name": "userConsentDisplayName",
        "value": "value",
    },
)
class ApplicationApiOauth2PermissionScope:
    def __init__(
        self,
        *,
        id: builtins.str,
        admin_consent_description: typing.Optional[builtins.str] = None,
        admin_consent_display_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
        user_consent_description: typing.Optional[builtins.str] = None,
        user_consent_display_name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The unique identifier of the delegated permission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id Application#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param admin_consent_description: Delegated permission description that appears in all tenant-wide admin consent experiences, intended to be read by an administrator granting the permission on behalf of all users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#admin_consent_description Application#admin_consent_description}
        :param admin_consent_display_name: Display name for the delegated permission, intended to be read by an administrator granting the permission on behalf of all users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#admin_consent_display_name Application#admin_consent_display_name}
        :param enabled: Determines if the permission scope is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#enabled Application#enabled}
        :param type: Whether this delegated permission should be considered safe for non-admin users to consent to on behalf of themselves, or whether an administrator should be required for consent to the permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#type Application#type}
        :param user_consent_description: Delegated permission description that appears in the end user consent experience, intended to be read by a user consenting on their own behalf. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#user_consent_description Application#user_consent_description}
        :param user_consent_display_name: Display name for the delegated permission that appears in the end user consent experience. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#user_consent_display_name Application#user_consent_display_name}
        :param value: The value that is used for the ``scp`` claim in OAuth 2.0 access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#value Application#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a603d452291f77fe2144e3455e1196b20930aec54de441eb643ed4ada53e53d4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument admin_consent_description", value=admin_consent_description, expected_type=type_hints["admin_consent_description"])
            check_type(argname="argument admin_consent_display_name", value=admin_consent_display_name, expected_type=type_hints["admin_consent_display_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_consent_description", value=user_consent_description, expected_type=type_hints["user_consent_description"])
            check_type(argname="argument user_consent_display_name", value=user_consent_display_name, expected_type=type_hints["user_consent_display_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if admin_consent_description is not None:
            self._values["admin_consent_description"] = admin_consent_description
        if admin_consent_display_name is not None:
            self._values["admin_consent_display_name"] = admin_consent_display_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if type is not None:
            self._values["type"] = type
        if user_consent_description is not None:
            self._values["user_consent_description"] = user_consent_description
        if user_consent_display_name is not None:
            self._values["user_consent_display_name"] = user_consent_display_name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique identifier of the delegated permission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id Application#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_consent_description(self) -> typing.Optional[builtins.str]:
        '''Delegated permission description that appears in all tenant-wide admin consent experiences, intended to be read by an administrator granting the permission on behalf of all users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#admin_consent_description Application#admin_consent_description}
        '''
        result = self._values.get("admin_consent_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_consent_display_name(self) -> typing.Optional[builtins.str]:
        '''Display name for the delegated permission, intended to be read by an administrator granting the permission on behalf of all users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#admin_consent_display_name Application#admin_consent_display_name}
        '''
        result = self._values.get("admin_consent_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if the permission scope is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#enabled Application#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Whether this delegated permission should be considered safe for non-admin users to consent to on behalf of themselves, or whether an administrator should be required for consent to the permissions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#type Application#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_consent_description(self) -> typing.Optional[builtins.str]:
        '''Delegated permission description that appears in the end user consent experience, intended to be read by a user consenting on their own behalf.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#user_consent_description Application#user_consent_description}
        '''
        result = self._values.get("user_consent_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_consent_display_name(self) -> typing.Optional[builtins.str]:
        '''Display name for the delegated permission that appears in the end user consent experience.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#user_consent_display_name Application#user_consent_display_name}
        '''
        result = self._values.get("user_consent_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value that is used for the ``scp`` claim in OAuth 2.0 access tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#value Application#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationApiOauth2PermissionScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationApiOauth2PermissionScopeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationApiOauth2PermissionScopeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5682218f782ad0ae47b0b5f3f3195cb65606ae5561f52f04c528638e4cad97b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationApiOauth2PermissionScopeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7071e3819a91667a16a37f4b0675373cf6b6cf67348864c3abd2d0ceef0d922)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationApiOauth2PermissionScopeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b844d8b153f24bd1ebc682feb66e6f61af0a08a4666723c6bb33ade6d7b11859)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60207eb7c7b7266872304bbac5f3af835a78a2e30d192d3eeed304a95006fb43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f19f70e828453d079001701a5394e067f7662b4a63865d98fe6e6eb6a892449e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationApiOauth2PermissionScope]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationApiOauth2PermissionScope]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationApiOauth2PermissionScope]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a5a6695f9b26b0f3cfb51da5e473d90aeeca537a4289561e68d98232da993e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationApiOauth2PermissionScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationApiOauth2PermissionScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61773a508b1a73bc2c3fa2dee48b2ccf89b6af1e4d34e41d100ee42e5b8a4c39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAdminConsentDescription")
    def reset_admin_consent_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminConsentDescription", []))

    @jsii.member(jsii_name="resetAdminConsentDisplayName")
    def reset_admin_consent_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminConsentDisplayName", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserConsentDescription")
    def reset_user_consent_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserConsentDescription", []))

    @jsii.member(jsii_name="resetUserConsentDisplayName")
    def reset_user_consent_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserConsentDisplayName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="adminConsentDescriptionInput")
    def admin_consent_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminConsentDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="adminConsentDisplayNameInput")
    def admin_consent_display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminConsentDisplayNameInput"))

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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userConsentDescriptionInput")
    def user_consent_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userConsentDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="userConsentDisplayNameInput")
    def user_consent_display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userConsentDisplayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="adminConsentDescription")
    def admin_consent_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminConsentDescription"))

    @admin_consent_description.setter
    def admin_consent_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce16180340c880c8741908b718ad35ad826737cf83d2a151a1777ed1eda4844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminConsentDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminConsentDisplayName")
    def admin_consent_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminConsentDisplayName"))

    @admin_consent_display_name.setter
    def admin_consent_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53cc4f9a487eb78842b8f08ba495727cea491d3fbbac10b54e9706d8535dc585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminConsentDisplayName", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__421422ba08df9b201ddecb12f00b70c1910c087bfb5a9df7ae9a42997615ec09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5eb6b8efe2cc94517fe18d7a2a1e774ca5e468c94ed87a1b8cdf27ae55d3323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a47957fe34487cea6e99097ccb608c758c173dc35b94845694191ec8422e49c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userConsentDescription")
    def user_consent_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userConsentDescription"))

    @user_consent_description.setter
    def user_consent_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff092f3ff204e0aac4df71f7f64b275f51e2acc1b4d2a29698b76b481d1d3758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userConsentDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userConsentDisplayName")
    def user_consent_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userConsentDisplayName"))

    @user_consent_display_name.setter
    def user_consent_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472c5f0ebfbbfab86ec7c9a09b2b92e02bcc9fb077b2760ba7079e48b3a3a770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userConsentDisplayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ae28abba6b3bf8089e955f196620b3171934bc0d9aa6d45f51403044f93918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationApiOauth2PermissionScope]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationApiOauth2PermissionScope]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationApiOauth2PermissionScope]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694c90b4f425c4bb9d040997494d575c4e216d0c2005adea33cdeaa1d95e60e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationApiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationApiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__118ca585b01d2e4b9ec76d3b684c8c3963aa14174fe54c9875e81cb4f6deba90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauth2PermissionScope")
    def put_oauth2_permission_scope(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationApiOauth2PermissionScope, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122d11e79a59c401e0b62e70ebf407c6180b6ca1e6b81cfa711d3ca24e15c39a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOauth2PermissionScope", [value]))

    @jsii.member(jsii_name="resetKnownClientApplications")
    def reset_known_client_applications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKnownClientApplications", []))

    @jsii.member(jsii_name="resetMappedClaimsEnabled")
    def reset_mapped_claims_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappedClaimsEnabled", []))

    @jsii.member(jsii_name="resetOauth2PermissionScope")
    def reset_oauth2_permission_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2PermissionScope", []))

    @jsii.member(jsii_name="resetRequestedAccessTokenVersion")
    def reset_requested_access_token_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestedAccessTokenVersion", []))

    @builtins.property
    @jsii.member(jsii_name="oauth2PermissionScope")
    def oauth2_permission_scope(self) -> ApplicationApiOauth2PermissionScopeList:
        return typing.cast(ApplicationApiOauth2PermissionScopeList, jsii.get(self, "oauth2PermissionScope"))

    @builtins.property
    @jsii.member(jsii_name="knownClientApplicationsInput")
    def known_client_applications_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "knownClientApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="mappedClaimsEnabledInput")
    def mapped_claims_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mappedClaimsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2PermissionScopeInput")
    def oauth2_permission_scope_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationApiOauth2PermissionScope]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationApiOauth2PermissionScope]]], jsii.get(self, "oauth2PermissionScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="requestedAccessTokenVersionInput")
    def requested_access_token_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestedAccessTokenVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="knownClientApplications")
    def known_client_applications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "knownClientApplications"))

    @known_client_applications.setter
    def known_client_applications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b367cf1e266543bca7532b6241cf131aef3e96d75a0f0e77825aa93ecc021f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knownClientApplications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mappedClaimsEnabled")
    def mapped_claims_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mappedClaimsEnabled"))

    @mapped_claims_enabled.setter
    def mapped_claims_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a48995f8733aa9c7e1cd582dcc53c2978aead083e4d8f6b8a8847c81e5f630e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mappedClaimsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestedAccessTokenVersion")
    def requested_access_token_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requestedAccessTokenVersion"))

    @requested_access_token_version.setter
    def requested_access_token_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c72923a2036b203e78c55ad37e556d3e19271370ac20007ee189ee98765979c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedAccessTokenVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationApi]:
        return typing.cast(typing.Optional[ApplicationApi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApplicationApi]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdea627c6e47781bec316d5729bc0beeee25bb7f55760695603067781868d56a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationAppRole",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_member_types": "allowedMemberTypes",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "enabled": "enabled",
        "value": "value",
    },
)
class ApplicationAppRole:
    def __init__(
        self,
        *,
        allowed_member_types: typing.Sequence[builtins.str],
        description: builtins.str,
        display_name: builtins.str,
        id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_member_types: Specifies whether this app role definition can be assigned to users and groups by setting to ``User``, or to other applications (that are accessing this application in a standalone scenario) by setting to ``Application``, or to both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#allowed_member_types Application#allowed_member_types}
        :param description: Description of the app role that appears when the role is being assigned and, if the role functions as an application permissions, during the consent experiences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#description Application#description}
        :param display_name: Display name for the app role that appears during app role assignment and in consent experiences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#display_name Application#display_name}
        :param id: The unique identifier of the app role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id Application#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param enabled: Determines if the app role is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#enabled Application#enabled}
        :param value: The value that is used for the ``roles`` claim in ID tokens and OAuth 2.0 access tokens that are authenticating an assigned service or user principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#value Application#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ccca5bc8f625f30cff92d61a362220c2f97b661191a2a450fb8894050fde134)
            check_type(argname="argument allowed_member_types", value=allowed_member_types, expected_type=type_hints["allowed_member_types"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_member_types": allowed_member_types,
            "description": description,
            "display_name": display_name,
            "id": id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def allowed_member_types(self) -> typing.List[builtins.str]:
        '''Specifies whether this app role definition can be assigned to users and groups by setting to ``User``, or to other applications (that are accessing this application in a standalone scenario) by setting to ``Application``, or to both.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#allowed_member_types Application#allowed_member_types}
        '''
        result = self._values.get("allowed_member_types")
        assert result is not None, "Required property 'allowed_member_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> builtins.str:
        '''Description of the app role that appears when the role is being assigned and, if the role functions as an application permissions, during the consent experiences.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#description Application#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Display name for the app role that appears during app role assignment and in consent experiences.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#display_name Application#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique identifier of the app role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id Application#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if the app role is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#enabled Application#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value that is used for the ``roles`` claim in ID tokens and OAuth 2.0 access tokens that are authenticating an assigned service or user principal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#value Application#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationAppRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationAppRoleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationAppRoleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0d7628988b8cdea4e806f31b1153109a6af7eadadc74f120f55ac939a898457)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApplicationAppRoleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007db1ce0a8a39992539a75476190f0cc72032de76dea4952bb2863afbc2cf93)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationAppRoleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855d3113d5b2a626d42e73e6e0aef8e15329ab542154dd30927a97e474bfe9ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09938e6d78f49f4897efd0a1818cd0de0c03eb32598a41711099d00bf5f0cffc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f448b36699a8c9d7d12f17ba5949a07ce0a87ba2c3aa0a81cbd4ccc540b0a053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationAppRole]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationAppRole]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationAppRole]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52ac41c5bc654a3ef432a9bacec380637e301b5c059b5051d3b7d15ec3a9e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationAppRoleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationAppRoleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e14c6acc338dfb0d90744c970ff66c34aa2d1e27ff5af88ba3741293aa8e34a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="allowedMemberTypesInput")
    def allowed_member_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMemberTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMemberTypes")
    def allowed_member_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMemberTypes"))

    @allowed_member_types.setter
    def allowed_member_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf10705a2d8af459c7de18888c953111f86d8cabebc803eb91f08b9db106c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMemberTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8aaa95519081c38f403b2f7aba8f1b8af267da44ac5c6e04666c9f578853299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74101af84480ad5151535400a569c1c88398c16f7be883f035e6abd0c1817e27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__cfe7ba9475a532e21ec7548f6ac6b76e299c98db4657cfcfc8927c32845a2e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb57519440756516a4e8e8a004df579d29aa437b3c29be7715cd105c8dd765e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2a16208f5e6f0553df4172badf956d8807f96afd0e3cdf907383497cf8ac29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationAppRole]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationAppRole]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationAppRole]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddbbc700c2c203ed71ca095bf52e5cf31f7346ca268ad73a0fa939d24e2e488f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationConfig",
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
        "api": "api",
        "app_role": "appRole",
        "description": "description",
        "device_only_auth_enabled": "deviceOnlyAuthEnabled",
        "fallback_public_client_enabled": "fallbackPublicClientEnabled",
        "feature_tags": "featureTags",
        "group_membership_claims": "groupMembershipClaims",
        "id": "id",
        "identifier_uris": "identifierUris",
        "logo_image": "logoImage",
        "marketing_url": "marketingUrl",
        "notes": "notes",
        "oauth2_post_response_required": "oauth2PostResponseRequired",
        "optional_claims": "optionalClaims",
        "owners": "owners",
        "password": "password",
        "prevent_duplicate_names": "preventDuplicateNames",
        "privacy_statement_url": "privacyStatementUrl",
        "public_client": "publicClient",
        "required_resource_access": "requiredResourceAccess",
        "service_management_reference": "serviceManagementReference",
        "sign_in_audience": "signInAudience",
        "single_page_application": "singlePageApplication",
        "support_url": "supportUrl",
        "tags": "tags",
        "template_id": "templateId",
        "terms_of_service_url": "termsOfServiceUrl",
        "timeouts": "timeouts",
        "web": "web",
    },
)
class ApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api: typing.Optional[typing.Union[ApplicationApi, typing.Dict[builtins.str, typing.Any]]] = None,
        app_role: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationAppRole, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        device_only_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fallback_public_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        feature_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationFeatureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        group_membership_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        identifier_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logo_image: typing.Optional[builtins.str] = None,
        marketing_url: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        oauth2_post_response_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optional_claims: typing.Optional[typing.Union["ApplicationOptionalClaims", typing.Dict[builtins.str, typing.Any]]] = None,
        owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        password: typing.Optional[typing.Union["ApplicationPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_duplicate_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        privacy_statement_url: typing.Optional[builtins.str] = None,
        public_client: typing.Optional[typing.Union["ApplicationPublicClient", typing.Dict[builtins.str, typing.Any]]] = None,
        required_resource_access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationRequiredResourceAccess", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_management_reference: typing.Optional[builtins.str] = None,
        sign_in_audience: typing.Optional[builtins.str] = None,
        single_page_application: typing.Optional[typing.Union["ApplicationSinglePageApplication", typing.Dict[builtins.str, typing.Any]]] = None,
        support_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        template_id: typing.Optional[builtins.str] = None,
        terms_of_service_url: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        web: typing.Optional[typing.Union["ApplicationWeb", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The display name for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#display_name Application#display_name}
        :param api: api block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#api Application#api}
        :param app_role: app_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#app_role Application#app_role}
        :param description: Description of the application as shown to end users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#description Application#description}
        :param device_only_auth_enabled: Specifies whether this application supports device authentication without a user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#device_only_auth_enabled Application#device_only_auth_enabled}
        :param fallback_public_client_enabled: Specifies whether the application is a public client. Appropriate for apps using token grant flows that don't use a redirect URI Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#fallback_public_client_enabled Application#fallback_public_client_enabled}
        :param feature_tags: feature_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#feature_tags Application#feature_tags}
        :param group_membership_claims: Configures the ``groups`` claim issued in a user or OAuth 2.0 access token that the app expects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#group_membership_claims Application#group_membership_claims}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id Application#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identifier_uris: The user-defined URI(s) that uniquely identify an application within its Azure AD tenant, or within a verified custom domain if the application is multi-tenant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#identifier_uris Application#identifier_uris}
        :param logo_image: Base64 encoded logo image in gif, png or jpeg format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#logo_image Application#logo_image}
        :param marketing_url: URL of the application's marketing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#marketing_url Application#marketing_url}
        :param notes: User-specified notes relevant for the management of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#notes Application#notes}
        :param oauth2_post_response_required: Specifies whether, as part of OAuth 2.0 token requests, Azure AD allows POST requests, as opposed to GET requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#oauth2_post_response_required Application#oauth2_post_response_required}
        :param optional_claims: optional_claims block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#optional_claims Application#optional_claims}
        :param owners: A list of object IDs of principals that will be granted ownership of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#owners Application#owners}
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#password Application#password}
        :param prevent_duplicate_names: If ``true``, will return an error if an existing application is found with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#prevent_duplicate_names Application#prevent_duplicate_names}
        :param privacy_statement_url: URL of the application's privacy statement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#privacy_statement_url Application#privacy_statement_url}
        :param public_client: public_client block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#public_client Application#public_client}
        :param required_resource_access: required_resource_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#required_resource_access Application#required_resource_access}
        :param service_management_reference: References application or service contact information from a Service or Asset Management database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#service_management_reference Application#service_management_reference}
        :param sign_in_audience: The Microsoft account types that are supported for the current application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#sign_in_audience Application#sign_in_audience}
        :param single_page_application: single_page_application block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#single_page_application Application#single_page_application}
        :param support_url: URL of the application's support page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#support_url Application#support_url}
        :param tags: A set of tags to apply to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#tags Application#tags}
        :param template_id: Unique ID of the application template from which this application is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#template_id Application#template_id}
        :param terms_of_service_url: URL of the application's terms of service statement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#terms_of_service_url Application#terms_of_service_url}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#timeouts Application#timeouts}
        :param web: web block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#web Application#web}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(api, dict):
            api = ApplicationApi(**api)
        if isinstance(optional_claims, dict):
            optional_claims = ApplicationOptionalClaims(**optional_claims)
        if isinstance(password, dict):
            password = ApplicationPassword(**password)
        if isinstance(public_client, dict):
            public_client = ApplicationPublicClient(**public_client)
        if isinstance(single_page_application, dict):
            single_page_application = ApplicationSinglePageApplication(**single_page_application)
        if isinstance(timeouts, dict):
            timeouts = ApplicationTimeouts(**timeouts)
        if isinstance(web, dict):
            web = ApplicationWeb(**web)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cb3548d34fbf82155a5cfd99a0a0f1adad50324c72d8840279611c6fc3cd15c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument app_role", value=app_role, expected_type=type_hints["app_role"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument device_only_auth_enabled", value=device_only_auth_enabled, expected_type=type_hints["device_only_auth_enabled"])
            check_type(argname="argument fallback_public_client_enabled", value=fallback_public_client_enabled, expected_type=type_hints["fallback_public_client_enabled"])
            check_type(argname="argument feature_tags", value=feature_tags, expected_type=type_hints["feature_tags"])
            check_type(argname="argument group_membership_claims", value=group_membership_claims, expected_type=type_hints["group_membership_claims"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identifier_uris", value=identifier_uris, expected_type=type_hints["identifier_uris"])
            check_type(argname="argument logo_image", value=logo_image, expected_type=type_hints["logo_image"])
            check_type(argname="argument marketing_url", value=marketing_url, expected_type=type_hints["marketing_url"])
            check_type(argname="argument notes", value=notes, expected_type=type_hints["notes"])
            check_type(argname="argument oauth2_post_response_required", value=oauth2_post_response_required, expected_type=type_hints["oauth2_post_response_required"])
            check_type(argname="argument optional_claims", value=optional_claims, expected_type=type_hints["optional_claims"])
            check_type(argname="argument owners", value=owners, expected_type=type_hints["owners"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument prevent_duplicate_names", value=prevent_duplicate_names, expected_type=type_hints["prevent_duplicate_names"])
            check_type(argname="argument privacy_statement_url", value=privacy_statement_url, expected_type=type_hints["privacy_statement_url"])
            check_type(argname="argument public_client", value=public_client, expected_type=type_hints["public_client"])
            check_type(argname="argument required_resource_access", value=required_resource_access, expected_type=type_hints["required_resource_access"])
            check_type(argname="argument service_management_reference", value=service_management_reference, expected_type=type_hints["service_management_reference"])
            check_type(argname="argument sign_in_audience", value=sign_in_audience, expected_type=type_hints["sign_in_audience"])
            check_type(argname="argument single_page_application", value=single_page_application, expected_type=type_hints["single_page_application"])
            check_type(argname="argument support_url", value=support_url, expected_type=type_hints["support_url"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
            check_type(argname="argument terms_of_service_url", value=terms_of_service_url, expected_type=type_hints["terms_of_service_url"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument web", value=web, expected_type=type_hints["web"])
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
        if api is not None:
            self._values["api"] = api
        if app_role is not None:
            self._values["app_role"] = app_role
        if description is not None:
            self._values["description"] = description
        if device_only_auth_enabled is not None:
            self._values["device_only_auth_enabled"] = device_only_auth_enabled
        if fallback_public_client_enabled is not None:
            self._values["fallback_public_client_enabled"] = fallback_public_client_enabled
        if feature_tags is not None:
            self._values["feature_tags"] = feature_tags
        if group_membership_claims is not None:
            self._values["group_membership_claims"] = group_membership_claims
        if id is not None:
            self._values["id"] = id
        if identifier_uris is not None:
            self._values["identifier_uris"] = identifier_uris
        if logo_image is not None:
            self._values["logo_image"] = logo_image
        if marketing_url is not None:
            self._values["marketing_url"] = marketing_url
        if notes is not None:
            self._values["notes"] = notes
        if oauth2_post_response_required is not None:
            self._values["oauth2_post_response_required"] = oauth2_post_response_required
        if optional_claims is not None:
            self._values["optional_claims"] = optional_claims
        if owners is not None:
            self._values["owners"] = owners
        if password is not None:
            self._values["password"] = password
        if prevent_duplicate_names is not None:
            self._values["prevent_duplicate_names"] = prevent_duplicate_names
        if privacy_statement_url is not None:
            self._values["privacy_statement_url"] = privacy_statement_url
        if public_client is not None:
            self._values["public_client"] = public_client
        if required_resource_access is not None:
            self._values["required_resource_access"] = required_resource_access
        if service_management_reference is not None:
            self._values["service_management_reference"] = service_management_reference
        if sign_in_audience is not None:
            self._values["sign_in_audience"] = sign_in_audience
        if single_page_application is not None:
            self._values["single_page_application"] = single_page_application
        if support_url is not None:
            self._values["support_url"] = support_url
        if tags is not None:
            self._values["tags"] = tags
        if template_id is not None:
            self._values["template_id"] = template_id
        if terms_of_service_url is not None:
            self._values["terms_of_service_url"] = terms_of_service_url
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if web is not None:
            self._values["web"] = web

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#display_name Application#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api(self) -> typing.Optional[ApplicationApi]:
        '''api block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#api Application#api}
        '''
        result = self._values.get("api")
        return typing.cast(typing.Optional[ApplicationApi], result)

    @builtins.property
    def app_role(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationAppRole]]]:
        '''app_role block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#app_role Application#app_role}
        '''
        result = self._values.get("app_role")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationAppRole]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the application as shown to end users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#description Application#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_only_auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether this application supports device authentication without a user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#device_only_auth_enabled Application#device_only_auth_enabled}
        '''
        result = self._values.get("device_only_auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fallback_public_client_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the application is a public client.

        Appropriate for apps using token grant flows that don't use a redirect URI

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#fallback_public_client_enabled Application#fallback_public_client_enabled}
        '''
        result = self._values.get("fallback_public_client_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def feature_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationFeatureTags"]]]:
        '''feature_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#feature_tags Application#feature_tags}
        '''
        result = self._values.get("feature_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationFeatureTags"]]], result)

    @builtins.property
    def group_membership_claims(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Configures the ``groups`` claim issued in a user or OAuth 2.0 access token that the app expects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#group_membership_claims Application#group_membership_claims}
        '''
        result = self._values.get("group_membership_claims")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id Application#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identifier_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The user-defined URI(s) that uniquely identify an application within its Azure AD tenant, or within a verified custom domain if the application is multi-tenant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#identifier_uris Application#identifier_uris}
        '''
        result = self._values.get("identifier_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logo_image(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded logo image in gif, png or jpeg format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#logo_image Application#logo_image}
        '''
        result = self._values.get("logo_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketing_url(self) -> typing.Optional[builtins.str]:
        '''URL of the application's marketing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#marketing_url Application#marketing_url}
        '''
        result = self._values.get("marketing_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        '''User-specified notes relevant for the management of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#notes Application#notes}
        '''
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_post_response_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether, as part of OAuth 2.0 token requests, Azure AD allows POST requests, as opposed to GET requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#oauth2_post_response_required Application#oauth2_post_response_required}
        '''
        result = self._values.get("oauth2_post_response_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def optional_claims(self) -> typing.Optional["ApplicationOptionalClaims"]:
        '''optional_claims block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#optional_claims Application#optional_claims}
        '''
        result = self._values.get("optional_claims")
        return typing.cast(typing.Optional["ApplicationOptionalClaims"], result)

    @builtins.property
    def owners(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of object IDs of principals that will be granted ownership of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#owners Application#owners}
        '''
        result = self._values.get("owners")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def password(self) -> typing.Optional["ApplicationPassword"]:
        '''password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#password Application#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional["ApplicationPassword"], result)

    @builtins.property
    def prevent_duplicate_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, will return an error if an existing application is found with the same name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#prevent_duplicate_names Application#prevent_duplicate_names}
        '''
        result = self._values.get("prevent_duplicate_names")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def privacy_statement_url(self) -> typing.Optional[builtins.str]:
        '''URL of the application's privacy statement.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#privacy_statement_url Application#privacy_statement_url}
        '''
        result = self._values.get("privacy_statement_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_client(self) -> typing.Optional["ApplicationPublicClient"]:
        '''public_client block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#public_client Application#public_client}
        '''
        result = self._values.get("public_client")
        return typing.cast(typing.Optional["ApplicationPublicClient"], result)

    @builtins.property
    def required_resource_access(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationRequiredResourceAccess"]]]:
        '''required_resource_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#required_resource_access Application#required_resource_access}
        '''
        result = self._values.get("required_resource_access")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationRequiredResourceAccess"]]], result)

    @builtins.property
    def service_management_reference(self) -> typing.Optional[builtins.str]:
        '''References application or service contact information from a Service or Asset Management database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#service_management_reference Application#service_management_reference}
        '''
        result = self._values.get("service_management_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_in_audience(self) -> typing.Optional[builtins.str]:
        '''The Microsoft account types that are supported for the current application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#sign_in_audience Application#sign_in_audience}
        '''
        result = self._values.get("sign_in_audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_page_application(
        self,
    ) -> typing.Optional["ApplicationSinglePageApplication"]:
        '''single_page_application block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#single_page_application Application#single_page_application}
        '''
        result = self._values.get("single_page_application")
        return typing.cast(typing.Optional["ApplicationSinglePageApplication"], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''URL of the application's support page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#support_url Application#support_url}
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of tags to apply to the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#tags Application#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def template_id(self) -> typing.Optional[builtins.str]:
        '''Unique ID of the application template from which this application is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#template_id Application#template_id}
        '''
        result = self._values.get("template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terms_of_service_url(self) -> typing.Optional[builtins.str]:
        '''URL of the application's terms of service statement.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#terms_of_service_url Application#terms_of_service_url}
        '''
        result = self._values.get("terms_of_service_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApplicationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#timeouts Application#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApplicationTimeouts"], result)

    @builtins.property
    def web(self) -> typing.Optional["ApplicationWeb"]:
        '''web block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#web Application#web}
        '''
        result = self._values.get("web")
        return typing.cast(typing.Optional["ApplicationWeb"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationFeatureTags",
    jsii_struct_bases=[],
    name_mapping={
        "custom_single_sign_on": "customSingleSignOn",
        "enterprise": "enterprise",
        "gallery": "gallery",
        "hide": "hide",
    },
)
class ApplicationFeatureTags:
    def __init__(
        self,
        *,
        custom_single_sign_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enterprise: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gallery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param custom_single_sign_on: Whether this application represents a custom SAML application for linked service principals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#custom_single_sign_on Application#custom_single_sign_on}
        :param enterprise: Whether this application represents an Enterprise Application for linked service principals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#enterprise Application#enterprise}
        :param gallery: Whether this application represents a gallery application for linked service principals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#gallery Application#gallery}
        :param hide: Whether this application is invisible to users in My Apps and Office 365 Launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#hide Application#hide}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff588c3e621ec6c91c62dad1e6a2a3c18541db56551db3a1a2b1a431bf2d6df8)
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
        '''Whether this application represents a custom SAML application for linked service principals.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#custom_single_sign_on Application#custom_single_sign_on}
        '''
        result = self._values.get("custom_single_sign_on")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enterprise(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this application represents an Enterprise Application for linked service principals.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#enterprise Application#enterprise}
        '''
        result = self._values.get("enterprise")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gallery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this application represents a gallery application for linked service principals.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#gallery Application#gallery}
        '''
        result = self._values.get("gallery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this application is invisible to users in My Apps and Office 365 Launcher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#hide Application#hide}
        '''
        result = self._values.get("hide")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationFeatureTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationFeatureTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationFeatureTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99620609ce11317741307a990ebd41b6ff9b536f98a34cbde8ccda14d6dc67a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApplicationFeatureTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b43788d18733e793521bd132f632b995398e407b18935c9b55dfecc019b889)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationFeatureTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__505c38594545a946a14e30cd589b716cd67850b2becaab691318cccbfb4c7570)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d714c19120a876ca0ef1c7e9d12d7fca3d89df50b18dfd1d106f097dd14a2815)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcd0e3578f169379d613b8ec9e1a85b1a38caac5638ee4de59fd1e5f9e41e407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationFeatureTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationFeatureTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationFeatureTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9041f2249f6c9dab746e9023595af80c9bd26ba8820ef3651fd5485fc6ae1473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationFeatureTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationFeatureTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bb5cb4dec93350758e3d001f181d0aec04a073e14da43c0e5d846f523a4b67b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e16aa31ae8b9ffeb6bdd8bdfcd26814fab81bc1d42ec8edf04bc706bf95ba32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b8a5db64eface58b8fdcc098f0bfb200253d1a0cad5b3893bddedefa95ebaf5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d2f240070924a944f86e340bc150aa735322ee4fe4617f235213d1a295a609f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed390487c06337e25e9b4187e809f1c50347667f19a6bc5ac96ec70ec0c90be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hide", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationFeatureTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationFeatureTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationFeatureTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138c638045b71ed0a80379e164b618338e7ba30eef8b4bb94843793fa5e97c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaims",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "id_token": "idToken",
        "saml2_token": "saml2Token",
    },
)
class ApplicationOptionalClaims:
    def __init__(
        self,
        *,
        access_token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationOptionalClaimsAccessToken", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id_token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationOptionalClaimsIdToken", typing.Dict[builtins.str, typing.Any]]]]] = None,
        saml2_token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationOptionalClaimsSaml2Token", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_token: access_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#access_token Application#access_token}
        :param id_token: id_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id_token Application#id_token}
        :param saml2_token: saml2_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#saml2_token Application#saml2_token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e99ec47e27b5ffab33febea63ed2564366e065156ee96d41be9da2f1e8f80f)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument id_token", value=id_token, expected_type=type_hints["id_token"])
            check_type(argname="argument saml2_token", value=saml2_token, expected_type=type_hints["saml2_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if id_token is not None:
            self._values["id_token"] = id_token
        if saml2_token is not None:
            self._values["saml2_token"] = saml2_token

    @builtins.property
    def access_token(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationOptionalClaimsAccessToken"]]]:
        '''access_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#access_token Application#access_token}
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationOptionalClaimsAccessToken"]]], result)

    @builtins.property
    def id_token(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationOptionalClaimsIdToken"]]]:
        '''id_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id_token Application#id_token}
        '''
        result = self._values.get("id_token")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationOptionalClaimsIdToken"]]], result)

    @builtins.property
    def saml2_token(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationOptionalClaimsSaml2Token"]]]:
        '''saml2_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#saml2_token Application#saml2_token}
        '''
        result = self._values.get("saml2_token")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationOptionalClaimsSaml2Token"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationOptionalClaims(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsAccessToken",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "additional_properties": "additionalProperties",
        "essential": "essential",
        "source": "source",
    },
)
class ApplicationOptionalClaimsAccessToken:
    def __init__(
        self,
        *,
        name: builtins.str,
        additional_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
        essential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the optional claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#name Application#name}
        :param additional_properties: List of additional properties of the claim. If a property exists in this list, it modifies the behaviour of the optional claim Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#additional_properties Application#additional_properties}
        :param essential: Whether the claim specified by the client is necessary to ensure a smooth authorization experience. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#essential Application#essential}
        :param source: The source of the claim. If ``source`` is absent, the claim is a predefined optional claim. If ``source`` is ``user``, the value of ``name`` is the extension property from the user object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#source Application#source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c00648c7aebcc80dca776e505afe28f45367bc8d211d09bcfc5d87bb35a667)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument additional_properties", value=additional_properties, expected_type=type_hints["additional_properties"])
            check_type(argname="argument essential", value=essential, expected_type=type_hints["essential"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if additional_properties is not None:
            self._values["additional_properties"] = additional_properties
        if essential is not None:
            self._values["essential"] = essential
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the optional claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#name Application#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_properties(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of additional properties of the claim.

        If a property exists in this list, it modifies the behaviour of the optional claim

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#additional_properties Application#additional_properties}
        '''
        result = self._values.get("additional_properties")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def essential(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the claim specified by the client is necessary to ensure a smooth authorization experience.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#essential Application#essential}
        '''
        result = self._values.get("essential")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The source of the claim.

        If ``source`` is absent, the claim is a predefined optional claim. If ``source`` is ``user``, the value of ``name`` is the extension property from the user object

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#source Application#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationOptionalClaimsAccessToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationOptionalClaimsAccessTokenList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsAccessTokenList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__464f880ac9d93e216d280e2f6cd1c589d30cf4e9cc765ff5592f90c27f8d50cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationOptionalClaimsAccessTokenOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb870fe6a47bd2d27655c7043c4faaa251b3c53c01dba4752fcad8aa97d68335)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationOptionalClaimsAccessTokenOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749373a6a5ddb79ade38e98ba573d59a7fad288900a467505f714220bbb12290)
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
            type_hints = typing.get_type_hints(_typecheckingstub__203257452e926f7db6eb6265f43723d30c24302676152f19cb3aa769eb1b843a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__688729673ba5903dd8d45bb443c2c347fd421f744e4ae47fbccda7381cec80ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsAccessToken]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsAccessToken]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsAccessToken]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbea00619b564f2242eae628badcc045a32d7744ac10a85b441b01fed22c384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationOptionalClaimsAccessTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsAccessTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f17502990ce7ed0a5488ed35ae0ce1d54e1c72191d808a63f5455dcb07fb1494)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAdditionalProperties")
    def reset_additional_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalProperties", []))

    @jsii.member(jsii_name="resetEssential")
    def reset_essential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEssential", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="additionalPropertiesInput")
    def additional_properties_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="essentialInput")
    def essential_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "essentialInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalProperties")
    def additional_properties(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalProperties"))

    @additional_properties.setter
    def additional_properties(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359c55fdb1812406ce1b449ff5cc4226c1933273276b712ed2350ee7960ec399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="essential")
    def essential(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "essential"))

    @essential.setter
    def essential(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad2d1f75dc8d499dc197845a3918bea1470ec3ec7a6ec67bfb4987b0fedcd1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "essential", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be52b8805f353220664c373d01a8ad5480c0858a84587b85a694b003cd48bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70adf9c0dda55ab10802091738a45e83028e3bf94dc70d7661a0a6cb42f6d7db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsAccessToken]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsAccessToken]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsAccessToken]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03520a46af59363ac8a57c512e61e92ffa4c2e18b4d159628afa5ae694fabc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsIdToken",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "additional_properties": "additionalProperties",
        "essential": "essential",
        "source": "source",
    },
)
class ApplicationOptionalClaimsIdToken:
    def __init__(
        self,
        *,
        name: builtins.str,
        additional_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
        essential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the optional claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#name Application#name}
        :param additional_properties: List of additional properties of the claim. If a property exists in this list, it modifies the behaviour of the optional claim Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#additional_properties Application#additional_properties}
        :param essential: Whether the claim specified by the client is necessary to ensure a smooth authorization experience. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#essential Application#essential}
        :param source: The source of the claim. If ``source`` is absent, the claim is a predefined optional claim. If ``source`` is ``user``, the value of ``name`` is the extension property from the user object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#source Application#source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080e700fd8d306760ba263b35ec2c3114b87a491a3aa92c1d5b592eeb79bc430)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument additional_properties", value=additional_properties, expected_type=type_hints["additional_properties"])
            check_type(argname="argument essential", value=essential, expected_type=type_hints["essential"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if additional_properties is not None:
            self._values["additional_properties"] = additional_properties
        if essential is not None:
            self._values["essential"] = essential
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the optional claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#name Application#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_properties(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of additional properties of the claim.

        If a property exists in this list, it modifies the behaviour of the optional claim

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#additional_properties Application#additional_properties}
        '''
        result = self._values.get("additional_properties")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def essential(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the claim specified by the client is necessary to ensure a smooth authorization experience.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#essential Application#essential}
        '''
        result = self._values.get("essential")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The source of the claim.

        If ``source`` is absent, the claim is a predefined optional claim. If ``source`` is ``user``, the value of ``name`` is the extension property from the user object

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#source Application#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationOptionalClaimsIdToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationOptionalClaimsIdTokenList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsIdTokenList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c82a7f939fe43e0b227d5af1127885284d529dc5067d0af2fad663f970d041f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationOptionalClaimsIdTokenOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e632bc6b0424c500b300a1d86ada9d09699640e493a25f92003f93aeb6261ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationOptionalClaimsIdTokenOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836d89067cd59fcfae54b7bf8a40370d7ba7779a847c39114bc5a3f89b5c0aed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9c2c122a7a120e5c199748ec00bbc992ffe8255ef09378f7cf36cd41e77074f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc05e58a7eaa38de74e46d645d972a476409781fbe66a9bb45821f4c1c8061b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsIdToken]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsIdToken]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsIdToken]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cd70614c5a1c444dc9620026db45665bb03fdcf447ff03f872ffeddda3385d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationOptionalClaimsIdTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsIdTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__134b758519d1c18c463c06d0f3827689d999096787b5328ce7e66705d62e3656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAdditionalProperties")
    def reset_additional_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalProperties", []))

    @jsii.member(jsii_name="resetEssential")
    def reset_essential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEssential", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="additionalPropertiesInput")
    def additional_properties_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="essentialInput")
    def essential_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "essentialInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalProperties")
    def additional_properties(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalProperties"))

    @additional_properties.setter
    def additional_properties(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee61a637b94fd629a85b38aa4ae0c70373a47d11a5f0b9242022937dfc4aedc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="essential")
    def essential(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "essential"))

    @essential.setter
    def essential(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48ab3d21669a11b61fa81af3d2104cca20e3a3f44f07e1b0ab5bb4fdce0ebc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "essential", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d409ded4104d41166feae1ce94ddf3c42d8bff1f9099cf8ac6681a1393523f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e248facb4a592d308b39ff7b3e154380d312e17054c1f538648d868478c5edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsIdToken]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsIdToken]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsIdToken]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19b94224c66dd85193d63de0a4685ee5422c5adea99ced8a316d3107ba4f413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationOptionalClaimsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5741ece50d694df329beaa48eb4e592a86285a059d6bdafb07590d9703b442b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessToken")
    def put_access_token(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationOptionalClaimsAccessToken, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2952dbe01e63190887b9d931ea874e7aaa96e361ff2e825c5e9da67811eba90e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessToken", [value]))

    @jsii.member(jsii_name="putIdToken")
    def put_id_token(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationOptionalClaimsIdToken, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e0e9fe2ab38d57f410ac6488f106097d6024310026b0956e60be9fc701d74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIdToken", [value]))

    @jsii.member(jsii_name="putSaml2Token")
    def put_saml2_token(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationOptionalClaimsSaml2Token", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90930d2c4e2ea11910a599162bda31aa484a293df6e7f4583db3dff7f02c3f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSaml2Token", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetIdToken")
    def reset_id_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdToken", []))

    @jsii.member(jsii_name="resetSaml2Token")
    def reset_saml2_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml2Token", []))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> ApplicationOptionalClaimsAccessTokenList:
        return typing.cast(ApplicationOptionalClaimsAccessTokenList, jsii.get(self, "accessToken"))

    @builtins.property
    @jsii.member(jsii_name="idToken")
    def id_token(self) -> ApplicationOptionalClaimsIdTokenList:
        return typing.cast(ApplicationOptionalClaimsIdTokenList, jsii.get(self, "idToken"))

    @builtins.property
    @jsii.member(jsii_name="saml2Token")
    def saml2_token(self) -> "ApplicationOptionalClaimsSaml2TokenList":
        return typing.cast("ApplicationOptionalClaimsSaml2TokenList", jsii.get(self, "saml2Token"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsAccessToken]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsAccessToken]]], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="idTokenInput")
    def id_token_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsIdToken]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsIdToken]]], jsii.get(self, "idTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="saml2TokenInput")
    def saml2_token_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationOptionalClaimsSaml2Token"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationOptionalClaimsSaml2Token"]]], jsii.get(self, "saml2TokenInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationOptionalClaims]:
        return typing.cast(typing.Optional[ApplicationOptionalClaims], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApplicationOptionalClaims]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ca1cebe1ff07da0825c31e248f973051240164980124ac1033c46fb808a11f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsSaml2Token",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "additional_properties": "additionalProperties",
        "essential": "essential",
        "source": "source",
    },
)
class ApplicationOptionalClaimsSaml2Token:
    def __init__(
        self,
        *,
        name: builtins.str,
        additional_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
        essential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the optional claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#name Application#name}
        :param additional_properties: List of additional properties of the claim. If a property exists in this list, it modifies the behaviour of the optional claim Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#additional_properties Application#additional_properties}
        :param essential: Whether the claim specified by the client is necessary to ensure a smooth authorization experience. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#essential Application#essential}
        :param source: The source of the claim. If ``source`` is absent, the claim is a predefined optional claim. If ``source`` is ``user``, the value of ``name`` is the extension property from the user object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#source Application#source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0368fef266605bbb4c10d37cfe0c5bb7309b73aaf17161afdb67f49b827f50)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument additional_properties", value=additional_properties, expected_type=type_hints["additional_properties"])
            check_type(argname="argument essential", value=essential, expected_type=type_hints["essential"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if additional_properties is not None:
            self._values["additional_properties"] = additional_properties
        if essential is not None:
            self._values["essential"] = essential
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the optional claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#name Application#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_properties(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of additional properties of the claim.

        If a property exists in this list, it modifies the behaviour of the optional claim

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#additional_properties Application#additional_properties}
        '''
        result = self._values.get("additional_properties")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def essential(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the claim specified by the client is necessary to ensure a smooth authorization experience.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#essential Application#essential}
        '''
        result = self._values.get("essential")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The source of the claim.

        If ``source`` is absent, the claim is a predefined optional claim. If ``source`` is ``user``, the value of ``name`` is the extension property from the user object

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#source Application#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationOptionalClaimsSaml2Token(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationOptionalClaimsSaml2TokenList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsSaml2TokenList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1460bb39e81b26a66d36ea864a1a8817dc34e5f9320c0b33817161f5a9c0a0bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationOptionalClaimsSaml2TokenOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664fcd59343012783a86e9dcc0fc0ff608a8db27bba9b2f9153dcbc2f5fca403)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationOptionalClaimsSaml2TokenOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c247a729a7e2f99fc060b5bd17c8e789d7f74c759f8f95ed663895402e2e84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c38a5092257788e1113dbfb10d5a18fdaef65c088333730de048d0aab5d124bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93b8e4674423e9da958609f985932966f5a0cd5ec9278067c9623385af2b679b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsSaml2Token]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsSaml2Token]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsSaml2Token]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d63eb72f0b0a4f6d5ffb8f128e5cccb3a5e3c0e35183c362f48d3ed260dd2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationOptionalClaimsSaml2TokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationOptionalClaimsSaml2TokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7cd189b084223789b83bf6ebfc9c4349e76a4efff700bc7c3c1d5858223a62d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAdditionalProperties")
    def reset_additional_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalProperties", []))

    @jsii.member(jsii_name="resetEssential")
    def reset_essential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEssential", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="additionalPropertiesInput")
    def additional_properties_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="essentialInput")
    def essential_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "essentialInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalProperties")
    def additional_properties(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalProperties"))

    @additional_properties.setter
    def additional_properties(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93151bc6cb4d1d715ae59364cca944dd42409677ba24d711ef056ce4eb50d558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="essential")
    def essential(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "essential"))

    @essential.setter
    def essential(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7cb0e51fbe55486e7b1d3824f3083cc925e602b8c427c5d8025395e3c4d22c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "essential", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f6190aa398e55bd1a3bdccc77c7559082cdb505f96a68b8fb2ebd31048f5ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9ed1021236d9e7165d42cfd901b56552fc7c9a6615dd0fb6343d20bc3bebd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsSaml2Token]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsSaml2Token]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsSaml2Token]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bc445ef3d5c4baad513f84feed8bb92919bbdde1dcbd5f83688ae4072d8f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationPassword",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "end_date": "endDate",
        "start_date": "startDate",
    },
)
class ApplicationPassword:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        end_date: typing.Optional[builtins.str] = None,
        start_date: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: A display name for the password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#display_name Application#display_name}
        :param end_date: The end date until which the password is valid, formatted as an RFC3339 date string (e.g. ``2018-01-01T01:02:03Z``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#end_date Application#end_date}
        :param start_date: The start date from which the password is valid, formatted as an RFC3339 date string (e.g. ``2018-01-01T01:02:03Z``). If this isn't specified, the current date is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#start_date Application#start_date}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43230d131f4fa25800ea9bcd3f0677070e2a1f89f19c3cc317e4e9b4e70c51e)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
        }
        if end_date is not None:
            self._values["end_date"] = end_date
        if start_date is not None:
            self._values["start_date"] = start_date

    @builtins.property
    def display_name(self) -> builtins.str:
        '''A display name for the password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#display_name Application#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_date(self) -> typing.Optional[builtins.str]:
        '''The end date until which the password is valid, formatted as an RFC3339 date string (e.g. ``2018-01-01T01:02:03Z``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#end_date Application#end_date}
        '''
        result = self._values.get("end_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_date(self) -> typing.Optional[builtins.str]:
        '''The start date from which the password is valid, formatted as an RFC3339 date string (e.g. ``2018-01-01T01:02:03Z``). If this isn't specified, the current date is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#start_date Application#start_date}
        '''
        result = self._values.get("start_date")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__deebe9b8f653d5638a8c0a9fe0ba382a5c893bc02701bdcd5c33f8f325289396)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndDate")
    def reset_end_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndDate", []))

    @jsii.member(jsii_name="resetStartDate")
    def reset_start_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartDate", []))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263ec990fefc09266a2e857b5022048bf2aafbe03a9a2a2ac05f77dbac1988e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDate"))

    @end_date.setter
    def end_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd261623c7f54faa336db894836cc2831b2645ca1a3d7bb3e5e74a09341f70a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDate"))

    @start_date.setter
    def start_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894d449fcc24bd66c4bd49a37fac89461623c14fbfcde41c0579aad910105f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationPassword]:
        return typing.cast(typing.Optional[ApplicationPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApplicationPassword]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaccb9eaea01e6873d3a38cbfc1beef59643f4620568568570346e3ec8f40527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationPublicClient",
    jsii_struct_bases=[],
    name_mapping={"redirect_uris": "redirectUris"},
)
class ApplicationPublicClient:
    def __init__(
        self,
        *,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param redirect_uris: The URLs where user tokens are sent for sign-in, or the redirect URIs where OAuth 2.0 authorization codes and access tokens are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#redirect_uris Application#redirect_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3608c82177642aced42d5ced63563fe3ba5192a016f763c4e4059a1a83007d)
            check_type(argname="argument redirect_uris", value=redirect_uris, expected_type=type_hints["redirect_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if redirect_uris is not None:
            self._values["redirect_uris"] = redirect_uris

    @builtins.property
    def redirect_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The URLs where user tokens are sent for sign-in, or the redirect URIs where OAuth 2.0 authorization codes and access tokens are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#redirect_uris Application#redirect_uris}
        '''
        result = self._values.get("redirect_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationPublicClient(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationPublicClientOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationPublicClientOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dacc8604373bf5ac2402d35ca3d4e409492924d267ba342f42d7cc483aa31b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRedirectUris")
    def reset_redirect_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUris", []))

    @builtins.property
    @jsii.member(jsii_name="redirectUrisInput")
    def redirect_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "redirectUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUris")
    def redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "redirectUris"))

    @redirect_uris.setter
    def redirect_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec86fc43c4a7b180ffa196342f72f0289fef1760d2aab370234e87798c447a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationPublicClient]:
        return typing.cast(typing.Optional[ApplicationPublicClient], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApplicationPublicClient]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18c34cc270c93e8b8f113c11a4bc056091017a19ccca32be8c2397b3bd266c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationRequiredResourceAccess",
    jsii_struct_bases=[],
    name_mapping={
        "resource_access": "resourceAccess",
        "resource_app_id": "resourceAppId",
    },
)
class ApplicationRequiredResourceAccess:
    def __init__(
        self,
        *,
        resource_access: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationRequiredResourceAccessResourceAccess", typing.Dict[builtins.str, typing.Any]]]],
        resource_app_id: builtins.str,
    ) -> None:
        '''
        :param resource_access: resource_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#resource_access Application#resource_access}
        :param resource_app_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#resource_app_id Application#resource_app_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802c8bdf03776fc5d34df6a40021d8f82ffc7b7f7a6688ad858fc5d207d7afc0)
            check_type(argname="argument resource_access", value=resource_access, expected_type=type_hints["resource_access"])
            check_type(argname="argument resource_app_id", value=resource_app_id, expected_type=type_hints["resource_app_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_access": resource_access,
            "resource_app_id": resource_app_id,
        }

    @builtins.property
    def resource_access(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationRequiredResourceAccessResourceAccess"]]:
        '''resource_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#resource_access Application#resource_access}
        '''
        result = self._values.get("resource_access")
        assert result is not None, "Required property 'resource_access' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationRequiredResourceAccessResourceAccess"]], result)

    @builtins.property
    def resource_app_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#resource_app_id Application#resource_app_id}.'''
        result = self._values.get("resource_app_id")
        assert result is not None, "Required property 'resource_app_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationRequiredResourceAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationRequiredResourceAccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationRequiredResourceAccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72736e105764c0240893607dc960105c35b9f7f5c3c9d64d855b0365f7c6def6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationRequiredResourceAccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483e1819ff8f99542893856442de423553f8fea18339a5bff7ebcb330ef53057)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationRequiredResourceAccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd549678f3230f0b03b503ffbc47e9587a7ecb349ac1e6aeddce2c1183def49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe56e6e09c0879adf0f204157dd750250e7ab775c0cb749e174a2b4d6d14235)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8949c1b2e8d89209e3da180f076e7a926ee5624ed9eda0af90fe249ee91f836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationRequiredResourceAccess]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationRequiredResourceAccess]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationRequiredResourceAccess]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a96c0d781d96548ec1f8fcc4e00736af0b7e267b4cfbd1b66780b12857ed8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationRequiredResourceAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationRequiredResourceAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f93a5e02fe0ae9494b45af6cf03cb513300892533ae8eda552968abdc83004dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putResourceAccess")
    def put_resource_access(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationRequiredResourceAccessResourceAccess", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b82d9ccaa85ea3d86f4c6a88be130e131a84e043efa3694d8227b972a2641e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceAccess", [value]))

    @builtins.property
    @jsii.member(jsii_name="resourceAccess")
    def resource_access(self) -> "ApplicationRequiredResourceAccessResourceAccessList":
        return typing.cast("ApplicationRequiredResourceAccessResourceAccessList", jsii.get(self, "resourceAccess"))

    @builtins.property
    @jsii.member(jsii_name="resourceAccessInput")
    def resource_access_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationRequiredResourceAccessResourceAccess"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationRequiredResourceAccessResourceAccess"]]], jsii.get(self, "resourceAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceAppIdInput")
    def resource_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceAppId")
    def resource_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceAppId"))

    @resource_app_id.setter
    def resource_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef37b83dfdf6d26ce084f8207945334cdbf5e2eeae3e38a70fbd9f59696d3eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceAppId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRequiredResourceAccess]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRequiredResourceAccess]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRequiredResourceAccess]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69efba654894321816fa6773f716fb70f286ae67dc631b55d74f25f303085813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationRequiredResourceAccessResourceAccess",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "type": "type"},
)
class ApplicationRequiredResourceAccessResourceAccess:
    def __init__(self, *, id: builtins.str, type: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id Application#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#type Application#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd83b1572b072673109bf7854ad76af751f91008d7f05df4d093eba03bcf6e4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "type": type,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id Application#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#type Application#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationRequiredResourceAccessResourceAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationRequiredResourceAccessResourceAccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationRequiredResourceAccessResourceAccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55920dc43b5ab725bd3ffb936cce7e168534a1a334371a0a051be6d6a1f2e3ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationRequiredResourceAccessResourceAccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ae0bba3c3bdf79f9ceec66a4a8068e3f2a12a8f140ac6fb2c2862eb0533857)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationRequiredResourceAccessResourceAccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137a06aba64a6229d8347db8498331bea6ab9eab787fa89909c587bce7038168)
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
            type_hints = typing.get_type_hints(_typecheckingstub__899410dfc39dbb1ed080ee7b9e03ba9ac0168b911a84b67d39d12de5658a94ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc903e285be4ff2e15c763b6e3c01329717f0752c882b5c7fd69c98d7aabb5d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationRequiredResourceAccessResourceAccess]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationRequiredResourceAccessResourceAccess]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationRequiredResourceAccessResourceAccess]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef8faeb834e77aa30b27396a4626db0f21d660c8296e2b8802d41545ec6e532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationRequiredResourceAccessResourceAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationRequiredResourceAccessResourceAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bde0d83fbf257d362280b9acd4a3601147e9098b78847f608d3b8382887fa3c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ec6fe98de6a59f27f21d035031304093eb4afbaf7aec3fa957ced45b7f05eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b6f14931977e9d3ad48c07a50f1d77d31a4ae463f044ac8e32ca1638f46c23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRequiredResourceAccessResourceAccess]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRequiredResourceAccessResourceAccess]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRequiredResourceAccessResourceAccess]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9557fd562197a5c347f2e38eb868665686f16f39266b440ff1b04262e56e35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationSinglePageApplication",
    jsii_struct_bases=[],
    name_mapping={"redirect_uris": "redirectUris"},
)
class ApplicationSinglePageApplication:
    def __init__(
        self,
        *,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param redirect_uris: The URLs where user tokens are sent for sign-in, or the redirect URIs where OAuth 2.0 authorization codes and access tokens are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#redirect_uris Application#redirect_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d33652da506dd1047bc0312e362670bb538645bd49b7ce51fe6b40bfdd3e59)
            check_type(argname="argument redirect_uris", value=redirect_uris, expected_type=type_hints["redirect_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if redirect_uris is not None:
            self._values["redirect_uris"] = redirect_uris

    @builtins.property
    def redirect_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The URLs where user tokens are sent for sign-in, or the redirect URIs where OAuth 2.0 authorization codes and access tokens are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#redirect_uris Application#redirect_uris}
        '''
        result = self._values.get("redirect_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSinglePageApplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationSinglePageApplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationSinglePageApplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__333214dc96b1813122ff60bc582164383ae63eb821b2b91cbbbdc6cadea764ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRedirectUris")
    def reset_redirect_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUris", []))

    @builtins.property
    @jsii.member(jsii_name="redirectUrisInput")
    def redirect_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "redirectUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUris")
    def redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "redirectUris"))

    @redirect_uris.setter
    def redirect_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2476d59ac0987d27422188dd38068ff6036d4ef1a09ed87f97ea61a3ccfba42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationSinglePageApplication]:
        return typing.cast(typing.Optional[ApplicationSinglePageApplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationSinglePageApplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6ca6c0218a3da3816809f51387b54016bdb7cc84b0b60b7b7c5fe0592c379b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApplicationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#create Application#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#delete Application#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#read Application#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#update Application#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d51bd6cfe0dd1c0c65c3f912293ff6cc449648acc268ffd5ed9acb567dba2d0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#create Application#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#delete Application#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#read Application#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#update Application#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4883cc5f94f9294ba67af23f3e5547d108471653d80c41f3635b0fa97bedcada)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75b64c93d75e15af50e3d1f62ff289218a22ad076887f484d909129444c9aa85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4399acb298e6c782d8d32043f62578db96e23d00808737b2ab4d3797f7986144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8185f9c0fff40455649170bc3cab88457e059994c88860bb54d8644565305314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167da2aa91ff99112f067947f01f9584b23bb0b31f6e4409eddd695a4bb97bd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee9c0545747f788a1a5014831a79cec8cdabed846be435bcadc421822984d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationWeb",
    jsii_struct_bases=[],
    name_mapping={
        "homepage_url": "homepageUrl",
        "implicit_grant": "implicitGrant",
        "logout_url": "logoutUrl",
        "redirect_uris": "redirectUris",
    },
)
class ApplicationWeb:
    def __init__(
        self,
        *,
        homepage_url: typing.Optional[builtins.str] = None,
        implicit_grant: typing.Optional[typing.Union["ApplicationWebImplicitGrant", typing.Dict[builtins.str, typing.Any]]] = None,
        logout_url: typing.Optional[builtins.str] = None,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param homepage_url: Home page or landing page of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#homepage_url Application#homepage_url}
        :param implicit_grant: implicit_grant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#implicit_grant Application#implicit_grant}
        :param logout_url: The URL that will be used by Microsoft's authorization service to sign out a user using front-channel, back-channel or SAML logout protocols. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#logout_url Application#logout_url}
        :param redirect_uris: The URLs where user tokens are sent for sign-in, or the redirect URIs where OAuth 2.0 authorization codes and access tokens are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#redirect_uris Application#redirect_uris}
        '''
        if isinstance(implicit_grant, dict):
            implicit_grant = ApplicationWebImplicitGrant(**implicit_grant)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b892ae716b9048b849838b5169ec26105a8f93575e6e8fa89a8208ffd62a13)
            check_type(argname="argument homepage_url", value=homepage_url, expected_type=type_hints["homepage_url"])
            check_type(argname="argument implicit_grant", value=implicit_grant, expected_type=type_hints["implicit_grant"])
            check_type(argname="argument logout_url", value=logout_url, expected_type=type_hints["logout_url"])
            check_type(argname="argument redirect_uris", value=redirect_uris, expected_type=type_hints["redirect_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if homepage_url is not None:
            self._values["homepage_url"] = homepage_url
        if implicit_grant is not None:
            self._values["implicit_grant"] = implicit_grant
        if logout_url is not None:
            self._values["logout_url"] = logout_url
        if redirect_uris is not None:
            self._values["redirect_uris"] = redirect_uris

    @builtins.property
    def homepage_url(self) -> typing.Optional[builtins.str]:
        '''Home page or landing page of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#homepage_url Application#homepage_url}
        '''
        result = self._values.get("homepage_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def implicit_grant(self) -> typing.Optional["ApplicationWebImplicitGrant"]:
        '''implicit_grant block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#implicit_grant Application#implicit_grant}
        '''
        result = self._values.get("implicit_grant")
        return typing.cast(typing.Optional["ApplicationWebImplicitGrant"], result)

    @builtins.property
    def logout_url(self) -> typing.Optional[builtins.str]:
        '''The URL that will be used by Microsoft's authorization service to sign out a user using front-channel, back-channel or SAML logout protocols.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#logout_url Application#logout_url}
        '''
        result = self._values.get("logout_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The URLs where user tokens are sent for sign-in, or the redirect URIs where OAuth 2.0 authorization codes and access tokens are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#redirect_uris Application#redirect_uris}
        '''
        result = self._values.get("redirect_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationWeb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.application.ApplicationWebImplicitGrant",
    jsii_struct_bases=[],
    name_mapping={
        "access_token_issuance_enabled": "accessTokenIssuanceEnabled",
        "id_token_issuance_enabled": "idTokenIssuanceEnabled",
    },
)
class ApplicationWebImplicitGrant:
    def __init__(
        self,
        *,
        access_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_token_issuance_enabled: Whether this web application can request an access token using OAuth 2.0 implicit flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#access_token_issuance_enabled Application#access_token_issuance_enabled}
        :param id_token_issuance_enabled: Whether this web application can request an ID token using OAuth 2.0 implicit flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id_token_issuance_enabled Application#id_token_issuance_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8f87e7407a1e7e81d0f8c8d6659fc51de15e101f9156ff92be316ba6de5000)
            check_type(argname="argument access_token_issuance_enabled", value=access_token_issuance_enabled, expected_type=type_hints["access_token_issuance_enabled"])
            check_type(argname="argument id_token_issuance_enabled", value=id_token_issuance_enabled, expected_type=type_hints["id_token_issuance_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token_issuance_enabled is not None:
            self._values["access_token_issuance_enabled"] = access_token_issuance_enabled
        if id_token_issuance_enabled is not None:
            self._values["id_token_issuance_enabled"] = id_token_issuance_enabled

    @builtins.property
    def access_token_issuance_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this web application can request an access token using OAuth 2.0 implicit flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#access_token_issuance_enabled Application#access_token_issuance_enabled}
        '''
        result = self._values.get("access_token_issuance_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id_token_issuance_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this web application can request an ID token using OAuth 2.0 implicit flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id_token_issuance_enabled Application#id_token_issuance_enabled}
        '''
        result = self._values.get("id_token_issuance_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationWebImplicitGrant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationWebImplicitGrantOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationWebImplicitGrantOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0b5aeb85638137b5f5fdb771405706c2dd84cb1026dd10eea6396183747b420)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessTokenIssuanceEnabled")
    def reset_access_token_issuance_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessTokenIssuanceEnabled", []))

    @jsii.member(jsii_name="resetIdTokenIssuanceEnabled")
    def reset_id_token_issuance_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdTokenIssuanceEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="accessTokenIssuanceEnabledInput")
    def access_token_issuance_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessTokenIssuanceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idTokenIssuanceEnabledInput")
    def id_token_issuance_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "idTokenIssuanceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenIssuanceEnabled")
    def access_token_issuance_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessTokenIssuanceEnabled"))

    @access_token_issuance_enabled.setter
    def access_token_issuance_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d6d48933a6a6a1d1564c3babe8fa0f7fafc83b16efdb597c4ea11c790befae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessTokenIssuanceEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idTokenIssuanceEnabled")
    def id_token_issuance_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "idTokenIssuanceEnabled"))

    @id_token_issuance_enabled.setter
    def id_token_issuance_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46285e1333a7f0be5cba68e3ff2fa91aeab6cdd81c5c3ee91d155773e6f80a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idTokenIssuanceEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationWebImplicitGrant]:
        return typing.cast(typing.Optional[ApplicationWebImplicitGrant], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationWebImplicitGrant],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f17a7c730b1a1c9bf1bd585399df422a3ee5c48517152f28732ba281944d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationWebOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.application.ApplicationWebOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0063e00bda130333a6cb306027786d0053796ce74b00df1750740d8655e2475e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImplicitGrant")
    def put_implicit_grant(
        self,
        *,
        access_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_token_issuance_enabled: Whether this web application can request an access token using OAuth 2.0 implicit flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#access_token_issuance_enabled Application#access_token_issuance_enabled}
        :param id_token_issuance_enabled: Whether this web application can request an ID token using OAuth 2.0 implicit flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/application#id_token_issuance_enabled Application#id_token_issuance_enabled}
        '''
        value = ApplicationWebImplicitGrant(
            access_token_issuance_enabled=access_token_issuance_enabled,
            id_token_issuance_enabled=id_token_issuance_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putImplicitGrant", [value]))

    @jsii.member(jsii_name="resetHomepageUrl")
    def reset_homepage_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHomepageUrl", []))

    @jsii.member(jsii_name="resetImplicitGrant")
    def reset_implicit_grant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImplicitGrant", []))

    @jsii.member(jsii_name="resetLogoutUrl")
    def reset_logout_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogoutUrl", []))

    @jsii.member(jsii_name="resetRedirectUris")
    def reset_redirect_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUris", []))

    @builtins.property
    @jsii.member(jsii_name="implicitGrant")
    def implicit_grant(self) -> ApplicationWebImplicitGrantOutputReference:
        return typing.cast(ApplicationWebImplicitGrantOutputReference, jsii.get(self, "implicitGrant"))

    @builtins.property
    @jsii.member(jsii_name="homepageUrlInput")
    def homepage_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homepageUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="implicitGrantInput")
    def implicit_grant_input(self) -> typing.Optional[ApplicationWebImplicitGrant]:
        return typing.cast(typing.Optional[ApplicationWebImplicitGrant], jsii.get(self, "implicitGrantInput"))

    @builtins.property
    @jsii.member(jsii_name="logoutUrlInput")
    def logout_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoutUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUrisInput")
    def redirect_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "redirectUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="homepageUrl")
    def homepage_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homepageUrl"))

    @homepage_url.setter
    def homepage_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6a708e50c2e042f71160b489e19745d8a159fc3c24f34c96ebc9b4a1dd836f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homepageUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logoutUrl")
    def logout_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoutUrl"))

    @logout_url.setter
    def logout_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3e4fcca613eaf6a6bb1bc70326b3d304501934d3bee56957016403fef4484d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoutUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUris")
    def redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "redirectUris"))

    @redirect_uris.setter
    def redirect_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf691849a7db98cecf9c2df337e8dbbaa97ab1a0a2782d8d5d90ae65a1b824b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationWeb]:
        return typing.cast(typing.Optional[ApplicationWeb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApplicationWeb]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd77c509620d1317b42b8e7c517ebe9e9b1f82a51c9a9eaaf94ebd9af87cb907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Application",
    "ApplicationApi",
    "ApplicationApiOauth2PermissionScope",
    "ApplicationApiOauth2PermissionScopeList",
    "ApplicationApiOauth2PermissionScopeOutputReference",
    "ApplicationApiOutputReference",
    "ApplicationAppRole",
    "ApplicationAppRoleList",
    "ApplicationAppRoleOutputReference",
    "ApplicationConfig",
    "ApplicationFeatureTags",
    "ApplicationFeatureTagsList",
    "ApplicationFeatureTagsOutputReference",
    "ApplicationOptionalClaims",
    "ApplicationOptionalClaimsAccessToken",
    "ApplicationOptionalClaimsAccessTokenList",
    "ApplicationOptionalClaimsAccessTokenOutputReference",
    "ApplicationOptionalClaimsIdToken",
    "ApplicationOptionalClaimsIdTokenList",
    "ApplicationOptionalClaimsIdTokenOutputReference",
    "ApplicationOptionalClaimsOutputReference",
    "ApplicationOptionalClaimsSaml2Token",
    "ApplicationOptionalClaimsSaml2TokenList",
    "ApplicationOptionalClaimsSaml2TokenOutputReference",
    "ApplicationPassword",
    "ApplicationPasswordOutputReference",
    "ApplicationPublicClient",
    "ApplicationPublicClientOutputReference",
    "ApplicationRequiredResourceAccess",
    "ApplicationRequiredResourceAccessList",
    "ApplicationRequiredResourceAccessOutputReference",
    "ApplicationRequiredResourceAccessResourceAccess",
    "ApplicationRequiredResourceAccessResourceAccessList",
    "ApplicationRequiredResourceAccessResourceAccessOutputReference",
    "ApplicationSinglePageApplication",
    "ApplicationSinglePageApplicationOutputReference",
    "ApplicationTimeouts",
    "ApplicationTimeoutsOutputReference",
    "ApplicationWeb",
    "ApplicationWebImplicitGrant",
    "ApplicationWebImplicitGrantOutputReference",
    "ApplicationWebOutputReference",
]

publication.publish()

def _typecheckingstub__598797ffd1c1da722948df1ca1dc3b8215b03ddbf0fe97b2a57729b95394ccfa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    api: typing.Optional[typing.Union[ApplicationApi, typing.Dict[builtins.str, typing.Any]]] = None,
    app_role: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationAppRole, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    device_only_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fallback_public_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    feature_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationFeatureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group_membership_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    identifier_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logo_image: typing.Optional[builtins.str] = None,
    marketing_url: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    oauth2_post_response_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optional_claims: typing.Optional[typing.Union[ApplicationOptionalClaims, typing.Dict[builtins.str, typing.Any]]] = None,
    owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    password: typing.Optional[typing.Union[ApplicationPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    prevent_duplicate_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    privacy_statement_url: typing.Optional[builtins.str] = None,
    public_client: typing.Optional[typing.Union[ApplicationPublicClient, typing.Dict[builtins.str, typing.Any]]] = None,
    required_resource_access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationRequiredResourceAccess, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_management_reference: typing.Optional[builtins.str] = None,
    sign_in_audience: typing.Optional[builtins.str] = None,
    single_page_application: typing.Optional[typing.Union[ApplicationSinglePageApplication, typing.Dict[builtins.str, typing.Any]]] = None,
    support_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    template_id: typing.Optional[builtins.str] = None,
    terms_of_service_url: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    web: typing.Optional[typing.Union[ApplicationWeb, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5429ed8a97b3f6264afd5e685eb2c5c1b29b06522ca4d48461060a6f297afcdc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f79eaaab621d89c408e6bb27118292445556e36738325b6f7241217958e1e39(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationAppRole, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502f85d7583c461ebe66f09b22aa9d4d395bf6519afa246264da95f213ba7fdb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationFeatureTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd13071039aa750678fe8748b949bf633bcd3142a86ecdf930ddab86da763a5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationRequiredResourceAccess, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c795272e61ef9ce89935d4fc838f774b855aacde02acefa7d59f02524add22d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c87aeca713f24baed1508cd10f366ce3ca94900e89b60dc7a5858d8812bf5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd7509b000b9ecb129eba618849abc0005887c4c1e2fb8f5fa4e4fe723433c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c08ce8edc55f00d9b52244d03a54e7561027a481b695fbed14ac5062387a08d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065bc0280592fe47a24a360cef92e406e0f5c3c08a56a7780832fd5d634706cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921b4bb8935a9944638df928163c59b0bab5c4cc9b95a5877fe1d61d2a415e2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86baa584f1edbdbc002485f50971e4a52d0ae1d80ca7599af1471ada4d428bf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2e657cf61c46092375cd2f65f1566fe3c3c1e58b76398ae2ff62784c842d6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b404e4e2b161a2c22c614f6fa9597156db0eec6e38d2d91639bedddda6353ba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54250879c450e1f3920437e79a82ad57daa4c8b8af2c7e422d7518d1809a94f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e77ff5e726620b62a8192c8f66834e2884dfcd788940dfdb175ed6617a8fb78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bfe04e31875031895be1752580f00012a8265540b3363d7c79df64e1e21622(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe5b8d15a8736b8d334b391348cdde2c64c015de022ac0486580b07887c12a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abe2527a40053f36c39edc05474ae1ecd773193611946ac0e2567b524be8def(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3379a935de6279c322ac6bad07850eb5afa2c82d99a279ad07a616dc069a84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9aa5403d0d67c71116c7dda47a66970883add862c75c0e4179b4df2d3d42d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88c7e24fa536fe013f7a05ae1a9a969a285cf3629f02713c1de7c0a7303caf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805bba6ff5ddea670883d37c1d2594c8b2e6ebb43c926832532965585e2d4e5d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f385de9a4eb108e00cbd887a3f8a3fb0cd0ea9c95e0e59ae01ab3ce124d0c7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5692c6383c3f765867d3dfa2baae310f6790b402e8b47a25a170dcefacda5129(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13883a3dbb678cb13a448982c307eebad77973ede01c78c63668b37438c4693d(
    *,
    known_client_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
    mapped_claims_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    oauth2_permission_scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationApiOauth2PermissionScope, typing.Dict[builtins.str, typing.Any]]]]] = None,
    requested_access_token_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a603d452291f77fe2144e3455e1196b20930aec54de441eb643ed4ada53e53d4(
    *,
    id: builtins.str,
    admin_consent_description: typing.Optional[builtins.str] = None,
    admin_consent_display_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
    user_consent_description: typing.Optional[builtins.str] = None,
    user_consent_display_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5682218f782ad0ae47b0b5f3f3195cb65606ae5561f52f04c528638e4cad97b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7071e3819a91667a16a37f4b0675373cf6b6cf67348864c3abd2d0ceef0d922(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b844d8b153f24bd1ebc682feb66e6f61af0a08a4666723c6bb33ade6d7b11859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60207eb7c7b7266872304bbac5f3af835a78a2e30d192d3eeed304a95006fb43(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19f70e828453d079001701a5394e067f7662b4a63865d98fe6e6eb6a892449e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5a6695f9b26b0f3cfb51da5e473d90aeeca537a4289561e68d98232da993e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationApiOauth2PermissionScope]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61773a508b1a73bc2c3fa2dee48b2ccf89b6af1e4d34e41d100ee42e5b8a4c39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce16180340c880c8741908b718ad35ad826737cf83d2a151a1777ed1eda4844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53cc4f9a487eb78842b8f08ba495727cea491d3fbbac10b54e9706d8535dc585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421422ba08df9b201ddecb12f00b70c1910c087bfb5a9df7ae9a42997615ec09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5eb6b8efe2cc94517fe18d7a2a1e774ca5e468c94ed87a1b8cdf27ae55d3323(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47957fe34487cea6e99097ccb608c758c173dc35b94845694191ec8422e49c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff092f3ff204e0aac4df71f7f64b275f51e2acc1b4d2a29698b76b481d1d3758(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472c5f0ebfbbfab86ec7c9a09b2b92e02bcc9fb077b2760ba7079e48b3a3a770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ae28abba6b3bf8089e955f196620b3171934bc0d9aa6d45f51403044f93918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694c90b4f425c4bb9d040997494d575c4e216d0c2005adea33cdeaa1d95e60e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationApiOauth2PermissionScope]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118ca585b01d2e4b9ec76d3b684c8c3963aa14174fe54c9875e81cb4f6deba90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122d11e79a59c401e0b62e70ebf407c6180b6ca1e6b81cfa711d3ca24e15c39a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationApiOauth2PermissionScope, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b367cf1e266543bca7532b6241cf131aef3e96d75a0f0e77825aa93ecc021f13(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a48995f8733aa9c7e1cd582dcc53c2978aead083e4d8f6b8a8847c81e5f630e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c72923a2036b203e78c55ad37e556d3e19271370ac20007ee189ee98765979c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdea627c6e47781bec316d5729bc0beeee25bb7f55760695603067781868d56a(
    value: typing.Optional[ApplicationApi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccca5bc8f625f30cff92d61a362220c2f97b661191a2a450fb8894050fde134(
    *,
    allowed_member_types: typing.Sequence[builtins.str],
    description: builtins.str,
    display_name: builtins.str,
    id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d7628988b8cdea4e806f31b1153109a6af7eadadc74f120f55ac939a898457(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007db1ce0a8a39992539a75476190f0cc72032de76dea4952bb2863afbc2cf93(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855d3113d5b2a626d42e73e6e0aef8e15329ab542154dd30927a97e474bfe9ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09938e6d78f49f4897efd0a1818cd0de0c03eb32598a41711099d00bf5f0cffc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f448b36699a8c9d7d12f17ba5949a07ce0a87ba2c3aa0a81cbd4ccc540b0a053(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52ac41c5bc654a3ef432a9bacec380637e301b5c059b5051d3b7d15ec3a9e3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationAppRole]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14c6acc338dfb0d90744c970ff66c34aa2d1e27ff5af88ba3741293aa8e34a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf10705a2d8af459c7de18888c953111f86d8cabebc803eb91f08b9db106c56(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8aaa95519081c38f403b2f7aba8f1b8af267da44ac5c6e04666c9f578853299(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74101af84480ad5151535400a569c1c88398c16f7be883f035e6abd0c1817e27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe7ba9475a532e21ec7548f6ac6b76e299c98db4657cfcfc8927c32845a2e26(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb57519440756516a4e8e8a004df579d29aa437b3c29be7715cd105c8dd765e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2a16208f5e6f0553df4172badf956d8807f96afd0e3cdf907383497cf8ac29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbbc700c2c203ed71ca095bf52e5cf31f7346ca268ad73a0fa939d24e2e488f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationAppRole]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb3548d34fbf82155a5cfd99a0a0f1adad50324c72d8840279611c6fc3cd15c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    api: typing.Optional[typing.Union[ApplicationApi, typing.Dict[builtins.str, typing.Any]]] = None,
    app_role: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationAppRole, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    device_only_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fallback_public_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    feature_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationFeatureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group_membership_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    identifier_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logo_image: typing.Optional[builtins.str] = None,
    marketing_url: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    oauth2_post_response_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optional_claims: typing.Optional[typing.Union[ApplicationOptionalClaims, typing.Dict[builtins.str, typing.Any]]] = None,
    owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    password: typing.Optional[typing.Union[ApplicationPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    prevent_duplicate_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    privacy_statement_url: typing.Optional[builtins.str] = None,
    public_client: typing.Optional[typing.Union[ApplicationPublicClient, typing.Dict[builtins.str, typing.Any]]] = None,
    required_resource_access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationRequiredResourceAccess, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_management_reference: typing.Optional[builtins.str] = None,
    sign_in_audience: typing.Optional[builtins.str] = None,
    single_page_application: typing.Optional[typing.Union[ApplicationSinglePageApplication, typing.Dict[builtins.str, typing.Any]]] = None,
    support_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    template_id: typing.Optional[builtins.str] = None,
    terms_of_service_url: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    web: typing.Optional[typing.Union[ApplicationWeb, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff588c3e621ec6c91c62dad1e6a2a3c18541db56551db3a1a2b1a431bf2d6df8(
    *,
    custom_single_sign_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enterprise: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gallery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99620609ce11317741307a990ebd41b6ff9b536f98a34cbde8ccda14d6dc67a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b43788d18733e793521bd132f632b995398e407b18935c9b55dfecc019b889(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505c38594545a946a14e30cd589b716cd67850b2becaab691318cccbfb4c7570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d714c19120a876ca0ef1c7e9d12d7fca3d89df50b18dfd1d106f097dd14a2815(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd0e3578f169379d613b8ec9e1a85b1a38caac5638ee4de59fd1e5f9e41e407(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9041f2249f6c9dab746e9023595af80c9bd26ba8820ef3651fd5485fc6ae1473(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationFeatureTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb5cb4dec93350758e3d001f181d0aec04a073e14da43c0e5d846f523a4b67b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e16aa31ae8b9ffeb6bdd8bdfcd26814fab81bc1d42ec8edf04bc706bf95ba32(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8a5db64eface58b8fdcc098f0bfb200253d1a0cad5b3893bddedefa95ebaf5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2f240070924a944f86e340bc150aa735322ee4fe4617f235213d1a295a609f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed390487c06337e25e9b4187e809f1c50347667f19a6bc5ac96ec70ec0c90be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138c638045b71ed0a80379e164b618338e7ba30eef8b4bb94843793fa5e97c45(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationFeatureTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e99ec47e27b5ffab33febea63ed2564366e065156ee96d41be9da2f1e8f80f(
    *,
    access_token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationOptionalClaimsAccessToken, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id_token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationOptionalClaimsIdToken, typing.Dict[builtins.str, typing.Any]]]]] = None,
    saml2_token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationOptionalClaimsSaml2Token, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c00648c7aebcc80dca776e505afe28f45367bc8d211d09bcfc5d87bb35a667(
    *,
    name: builtins.str,
    additional_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    essential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464f880ac9d93e216d280e2f6cd1c589d30cf4e9cc765ff5592f90c27f8d50cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb870fe6a47bd2d27655c7043c4faaa251b3c53c01dba4752fcad8aa97d68335(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749373a6a5ddb79ade38e98ba573d59a7fad288900a467505f714220bbb12290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203257452e926f7db6eb6265f43723d30c24302676152f19cb3aa769eb1b843a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688729673ba5903dd8d45bb443c2c347fd421f744e4ae47fbccda7381cec80ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbea00619b564f2242eae628badcc045a32d7744ac10a85b441b01fed22c384(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsAccessToken]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17502990ce7ed0a5488ed35ae0ce1d54e1c72191d808a63f5455dcb07fb1494(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359c55fdb1812406ce1b449ff5cc4226c1933273276b712ed2350ee7960ec399(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad2d1f75dc8d499dc197845a3918bea1470ec3ec7a6ec67bfb4987b0fedcd1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be52b8805f353220664c373d01a8ad5480c0858a84587b85a694b003cd48bb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70adf9c0dda55ab10802091738a45e83028e3bf94dc70d7661a0a6cb42f6d7db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03520a46af59363ac8a57c512e61e92ffa4c2e18b4d159628afa5ae694fabc8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsAccessToken]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080e700fd8d306760ba263b35ec2c3114b87a491a3aa92c1d5b592eeb79bc430(
    *,
    name: builtins.str,
    additional_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    essential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82a7f939fe43e0b227d5af1127885284d529dc5067d0af2fad663f970d041f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e632bc6b0424c500b300a1d86ada9d09699640e493a25f92003f93aeb6261ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836d89067cd59fcfae54b7bf8a40370d7ba7779a847c39114bc5a3f89b5c0aed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c2c122a7a120e5c199748ec00bbc992ffe8255ef09378f7cf36cd41e77074f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc05e58a7eaa38de74e46d645d972a476409781fbe66a9bb45821f4c1c8061b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cd70614c5a1c444dc9620026db45665bb03fdcf447ff03f872ffeddda3385d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsIdToken]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134b758519d1c18c463c06d0f3827689d999096787b5328ce7e66705d62e3656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee61a637b94fd629a85b38aa4ae0c70373a47d11a5f0b9242022937dfc4aedc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48ab3d21669a11b61fa81af3d2104cca20e3a3f44f07e1b0ab5bb4fdce0ebc1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d409ded4104d41166feae1ce94ddf3c42d8bff1f9099cf8ac6681a1393523f96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e248facb4a592d308b39ff7b3e154380d312e17054c1f538648d868478c5edd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19b94224c66dd85193d63de0a4685ee5422c5adea99ced8a316d3107ba4f413(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsIdToken]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5741ece50d694df329beaa48eb4e592a86285a059d6bdafb07590d9703b442b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2952dbe01e63190887b9d931ea874e7aaa96e361ff2e825c5e9da67811eba90e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationOptionalClaimsAccessToken, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e0e9fe2ab38d57f410ac6488f106097d6024310026b0956e60be9fc701d74c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationOptionalClaimsIdToken, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90930d2c4e2ea11910a599162bda31aa484a293df6e7f4583db3dff7f02c3f41(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationOptionalClaimsSaml2Token, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ca1cebe1ff07da0825c31e248f973051240164980124ac1033c46fb808a11f(
    value: typing.Optional[ApplicationOptionalClaims],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0368fef266605bbb4c10d37cfe0c5bb7309b73aaf17161afdb67f49b827f50(
    *,
    name: builtins.str,
    additional_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    essential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1460bb39e81b26a66d36ea864a1a8817dc34e5f9320c0b33817161f5a9c0a0bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664fcd59343012783a86e9dcc0fc0ff608a8db27bba9b2f9153dcbc2f5fca403(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c247a729a7e2f99fc060b5bd17c8e789d7f74c759f8f95ed663895402e2e84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38a5092257788e1113dbfb10d5a18fdaef65c088333730de048d0aab5d124bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b8e4674423e9da958609f985932966f5a0cd5ec9278067c9623385af2b679b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d63eb72f0b0a4f6d5ffb8f128e5cccb3a5e3c0e35183c362f48d3ed260dd2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationOptionalClaimsSaml2Token]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cd189b084223789b83bf6ebfc9c4349e76a4efff700bc7c3c1d5858223a62d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93151bc6cb4d1d715ae59364cca944dd42409677ba24d711ef056ce4eb50d558(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7cb0e51fbe55486e7b1d3824f3083cc925e602b8c427c5d8025395e3c4d22c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f6190aa398e55bd1a3bdccc77c7559082cdb505f96a68b8fb2ebd31048f5ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9ed1021236d9e7165d42cfd901b56552fc7c9a6615dd0fb6343d20bc3bebd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bc445ef3d5c4baad513f84feed8bb92919bbdde1dcbd5f83688ae4072d8f03(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationOptionalClaimsSaml2Token]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43230d131f4fa25800ea9bcd3f0677070e2a1f89f19c3cc317e4e9b4e70c51e(
    *,
    display_name: builtins.str,
    end_date: typing.Optional[builtins.str] = None,
    start_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deebe9b8f653d5638a8c0a9fe0ba382a5c893bc02701bdcd5c33f8f325289396(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263ec990fefc09266a2e857b5022048bf2aafbe03a9a2a2ac05f77dbac1988e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd261623c7f54faa336db894836cc2831b2645ca1a3d7bb3e5e74a09341f70a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894d449fcc24bd66c4bd49a37fac89461623c14fbfcde41c0579aad910105f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaccb9eaea01e6873d3a38cbfc1beef59643f4620568568570346e3ec8f40527(
    value: typing.Optional[ApplicationPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3608c82177642aced42d5ced63563fe3ba5192a016f763c4e4059a1a83007d(
    *,
    redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dacc8604373bf5ac2402d35ca3d4e409492924d267ba342f42d7cc483aa31b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec86fc43c4a7b180ffa196342f72f0289fef1760d2aab370234e87798c447a6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18c34cc270c93e8b8f113c11a4bc056091017a19ccca32be8c2397b3bd266c6(
    value: typing.Optional[ApplicationPublicClient],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802c8bdf03776fc5d34df6a40021d8f82ffc7b7f7a6688ad858fc5d207d7afc0(
    *,
    resource_access: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationRequiredResourceAccessResourceAccess, typing.Dict[builtins.str, typing.Any]]]],
    resource_app_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72736e105764c0240893607dc960105c35b9f7f5c3c9d64d855b0365f7c6def6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483e1819ff8f99542893856442de423553f8fea18339a5bff7ebcb330ef53057(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd549678f3230f0b03b503ffbc47e9587a7ecb349ac1e6aeddce2c1183def49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe56e6e09c0879adf0f204157dd750250e7ab775c0cb749e174a2b4d6d14235(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8949c1b2e8d89209e3da180f076e7a926ee5624ed9eda0af90fe249ee91f836(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a96c0d781d96548ec1f8fcc4e00736af0b7e267b4cfbd1b66780b12857ed8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationRequiredResourceAccess]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93a5e02fe0ae9494b45af6cf03cb513300892533ae8eda552968abdc83004dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b82d9ccaa85ea3d86f4c6a88be130e131a84e043efa3694d8227b972a2641e0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationRequiredResourceAccessResourceAccess, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef37b83dfdf6d26ce084f8207945334cdbf5e2eeae3e38a70fbd9f59696d3eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69efba654894321816fa6773f716fb70f286ae67dc631b55d74f25f303085813(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRequiredResourceAccess]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd83b1572b072673109bf7854ad76af751f91008d7f05df4d093eba03bcf6e4(
    *,
    id: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55920dc43b5ab725bd3ffb936cce7e168534a1a334371a0a051be6d6a1f2e3ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ae0bba3c3bdf79f9ceec66a4a8068e3f2a12a8f140ac6fb2c2862eb0533857(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137a06aba64a6229d8347db8498331bea6ab9eab787fa89909c587bce7038168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899410dfc39dbb1ed080ee7b9e03ba9ac0168b911a84b67d39d12de5658a94ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc903e285be4ff2e15c763b6e3c01329717f0752c882b5c7fd69c98d7aabb5d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef8faeb834e77aa30b27396a4626db0f21d660c8296e2b8802d41545ec6e532(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationRequiredResourceAccessResourceAccess]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde0d83fbf257d362280b9acd4a3601147e9098b78847f608d3b8382887fa3c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ec6fe98de6a59f27f21d035031304093eb4afbaf7aec3fa957ced45b7f05eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b6f14931977e9d3ad48c07a50f1d77d31a4ae463f044ac8e32ca1638f46c23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9557fd562197a5c347f2e38eb868665686f16f39266b440ff1b04262e56e35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationRequiredResourceAccessResourceAccess]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d33652da506dd1047bc0312e362670bb538645bd49b7ce51fe6b40bfdd3e59(
    *,
    redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333214dc96b1813122ff60bc582164383ae63eb821b2b91cbbbdc6cadea764ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2476d59ac0987d27422188dd38068ff6036d4ef1a09ed87f97ea61a3ccfba42b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6ca6c0218a3da3816809f51387b54016bdb7cc84b0b60b7b7c5fe0592c379b(
    value: typing.Optional[ApplicationSinglePageApplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d51bd6cfe0dd1c0c65c3f912293ff6cc449648acc268ffd5ed9acb567dba2d0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4883cc5f94f9294ba67af23f3e5547d108471653d80c41f3635b0fa97bedcada(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b64c93d75e15af50e3d1f62ff289218a22ad076887f484d909129444c9aa85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4399acb298e6c782d8d32043f62578db96e23d00808737b2ab4d3797f7986144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8185f9c0fff40455649170bc3cab88457e059994c88860bb54d8644565305314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167da2aa91ff99112f067947f01f9584b23bb0b31f6e4409eddd695a4bb97bd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee9c0545747f788a1a5014831a79cec8cdabed846be435bcadc421822984d03(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b892ae716b9048b849838b5169ec26105a8f93575e6e8fa89a8208ffd62a13(
    *,
    homepage_url: typing.Optional[builtins.str] = None,
    implicit_grant: typing.Optional[typing.Union[ApplicationWebImplicitGrant, typing.Dict[builtins.str, typing.Any]]] = None,
    logout_url: typing.Optional[builtins.str] = None,
    redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8f87e7407a1e7e81d0f8c8d6659fc51de15e101f9156ff92be316ba6de5000(
    *,
    access_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id_token_issuance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b5aeb85638137b5f5fdb771405706c2dd84cb1026dd10eea6396183747b420(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d6d48933a6a6a1d1564c3babe8fa0f7fafc83b16efdb597c4ea11c790befae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46285e1333a7f0be5cba68e3ff2fa91aeab6cdd81c5c3ee91d155773e6f80a5f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f17a7c730b1a1c9bf1bd585399df422a3ee5c48517152f28732ba281944d4f(
    value: typing.Optional[ApplicationWebImplicitGrant],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0063e00bda130333a6cb306027786d0053796ce74b00df1750740d8655e2475e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6a708e50c2e042f71160b489e19745d8a159fc3c24f34c96ebc9b4a1dd836f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3e4fcca613eaf6a6bb1bc70326b3d304501934d3bee56957016403fef4484d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf691849a7db98cecf9c2df337e8dbbaa97ab1a0a2782d8d5d90ae65a1b824b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd77c509620d1317b42b8e7c517ebe9e9b1f82a51c9a9eaaf94ebd9af87cb907(
    value: typing.Optional[ApplicationWeb],
) -> None:
    """Type checking stubs"""
    pass
