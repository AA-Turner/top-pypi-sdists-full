r'''
# `google_iam_workforce_pool_provider`

Refer to the Terraform Registry for docs: [`google_iam_workforce_pool_provider`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider).
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


class GoogleIamWorkforcePoolProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider google_iam_workforce_pool_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        provider_id: builtins.str,
        workforce_pool_id: builtins.str,
        attribute_condition: typing.Optional[builtins.str] = None,
        attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        extra_attributes_oauth2_client: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        saml: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider google_iam_workforce_pool_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#location GoogleIamWorkforcePoolProvider#location}
        :param provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#provider_id GoogleIamWorkforcePoolProvider#provider_id}
        :param workforce_pool_id: The ID to use for the pool, which becomes the final component of the resource name. The IDs must be a globally unique string of 6 to 63 lowercase letters, digits, or hyphens. It must start with a letter, and cannot have a trailing hyphen. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#workforce_pool_id GoogleIamWorkforcePoolProvider#workforce_pool_id}
        :param attribute_condition: A `Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: - 'assertion': JSON representing the authentication credential issued by the provider. - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. 'google.profile_photo' and 'google.display_name' are not supported. - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credentials will be accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#attribute_condition GoogleIamWorkforcePoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from the authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: - 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. This is a required field and the mapped subject cannot exceed 127 bytes. - 'google.groups': Groups the authenticating user belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. - 'google.display_name': The name of the authenticated user. This is an optional field and the mapped display name cannot exceed 100 bytes. If not set, 'google.subject' will be displayed instead. This attribute cannot be referenced in IAM bindings. - 'google.profile_photo': The URL that specifies the authenticated user's thumbnail photo. This is an optional field. When set, the image will be visible as the user's profile picture. If not set, a generic user icon will be displayed instead. This attribute cannot be referenced in IAM bindings. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where {custom_attribute} is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workforce pool to Google Cloud resources. For example: - 'google.subject': 'principal://iam.googleapis.com/locations/{location}/workforcePools/{pool}/subject/{value}' - 'google.groups': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/group/{value}' - 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For OIDC providers, you must supply a custom mapping that includes the 'google.subject' attribute. For example, the following maps the sub claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} An object containing a list of '"key": value' pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#attribute_mapping GoogleIamWorkforcePoolProvider#attribute_mapping}
        :param description: A user-specified description of the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#description GoogleIamWorkforcePoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#disabled GoogleIamWorkforcePoolProvider#disabled}
        :param display_name: A user-specified display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#display_name GoogleIamWorkforcePoolProvider#display_name}
        :param extra_attributes_oauth2_client: extra_attributes_oauth2_client block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#extra_attributes_oauth2_client GoogleIamWorkforcePoolProvider#extra_attributes_oauth2_client}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#id GoogleIamWorkforcePoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#oidc GoogleIamWorkforcePoolProvider#oidc}
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#saml GoogleIamWorkforcePoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#timeouts GoogleIamWorkforcePoolProvider#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd955dc1b04496da86a773d0ed15b00dcca2f3cd25d1006083788a394927196e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIamWorkforcePoolProviderConfig(
            location=location,
            provider_id=provider_id,
            workforce_pool_id=workforce_pool_id,
            attribute_condition=attribute_condition,
            attribute_mapping=attribute_mapping,
            description=description,
            disabled=disabled,
            display_name=display_name,
            extra_attributes_oauth2_client=extra_attributes_oauth2_client,
            id=id,
            oidc=oidc,
            saml=saml,
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
        '''Generates CDKTF code for importing a GoogleIamWorkforcePoolProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleIamWorkforcePoolProvider to import.
        :param import_from_id: The id of the existing GoogleIamWorkforcePoolProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleIamWorkforcePoolProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5669dd4dd914225e63afaa85430e2d7a6592a36876aeef54adf7a297e64d7fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExtraAttributesOauth2Client")
    def put_extra_attributes_oauth2_client(
        self,
        *,
        attributes_type: builtins.str,
        client_id: builtins.str,
        client_secret: typing.Union["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret", typing.Dict[builtins.str, typing.Any]],
        issuer_uri: builtins.str,
        query_parameters: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param attributes_type: Represents the IdP and type of claims that should be fetched. - AZURE_AD_GROUPS_MAIL: Used to get the user's group claims from the Azure AD identity provider using configuration provided in ExtraAttributesOAuth2Client and 'mail' property of the 'microsoft.graph.group' object is used for claim mapping. See https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties for more details on 'microsoft.graph.group' properties. The attributes obtained from idntity provider are mapped to 'assertion.groups'. - AZURE_AD_GROUPS_ID: Used to get the user's group claims from the Azure AD identity provider using configuration provided in ExtraAttributesOAuth2Client and 'id' property of the 'microsoft.graph.group' object is used for claim mapping. See https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties for more details on 'microsoft.graph.group' properties. The group IDs obtained from Azure AD are present in 'assertion.groups' for OIDC providers and 'assertion.attributes.groups' for SAML providers for attribute mapping. Possible values: ["AZURE_AD_GROUPS_MAIL", "AZURE_AD_GROUPS_ID"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#attributes_type GoogleIamWorkforcePoolProvider#attributes_type}
        :param client_id: The OAuth 2.0 client ID for retrieving extra attributes from the identity provider. Required to get the Access Token using client credentials grant flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_id GoogleIamWorkforcePoolProvider#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_secret GoogleIamWorkforcePoolProvider#client_secret}
        :param issuer_uri: The OIDC identity provider's issuer URI. Must be a valid URI using the 'https' scheme. Required to get the OIDC discovery document. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#issuer_uri GoogleIamWorkforcePoolProvider#issuer_uri}
        :param query_parameters: query_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#query_parameters GoogleIamWorkforcePoolProvider#query_parameters}
        '''
        value = GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client(
            attributes_type=attributes_type,
            client_id=client_id,
            client_secret=client_secret,
            issuer_uri=issuer_uri,
            query_parameters=query_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putExtraAttributesOauth2Client", [value]))

    @jsii.member(jsii_name="putOidc")
    def put_oidc(
        self,
        *,
        client_id: builtins.str,
        issuer_uri: builtins.str,
        client_secret: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderOidcClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        jwks_json: typing.Optional[builtins.str] = None,
        web_sso_config: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderOidcWebSsoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: The client ID. Must match the audience claim of the JWT issued by the identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_id GoogleIamWorkforcePoolProvider#client_id}
        :param issuer_uri: The OIDC issuer URI. Must be a valid URI using the 'https' scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#issuer_uri GoogleIamWorkforcePoolProvider#issuer_uri}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_secret GoogleIamWorkforcePoolProvider#client_secret}
        :param jwks_json: OIDC JWKs in JSON String format. For details on definition of a JWK, see https:tools.ietf.org/html/rfc7517. If not set, then we use the 'jwks_uri' from the discovery document fetched from the .well-known path for the 'issuer_uri'. Currently, RSA and EC asymmetric keys are supported. The JWK must use following format and include only the following fields:: { "keys": [ { "kty": "RSA/EC", "alg": "<algorithm>", "use": "sig", "kid": "<key-id>", "n": "", "e": "", "x": "", "y": "", "crv": "" } ] } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#jwks_json GoogleIamWorkforcePoolProvider#jwks_json}
        :param web_sso_config: web_sso_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#web_sso_config GoogleIamWorkforcePoolProvider#web_sso_config}
        '''
        value = GoogleIamWorkforcePoolProviderOidc(
            client_id=client_id,
            issuer_uri=issuer_uri,
            client_secret=client_secret,
            jwks_json=jwks_json,
            web_sso_config=web_sso_config,
        )

        return typing.cast(None, jsii.invoke(self, "putOidc", [value]))

    @jsii.member(jsii_name="putSaml")
    def put_saml(self, *, idp_metadata_xml: builtins.str) -> None:
        '''
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. The xml document should comply with `SAML 2.0 specification <https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf>`_. The max size of the acceptable xml document will be bounded to 128k characters. The metadata xml document should satisfy the following constraints: 1. Must contain an Identity Provider Entity ID. 2. Must contain at least one non-expired signing key certificate. 3. For each signing key: a) Valid from should be no more than 7 days from now. b) Valid to should be no more than 10 years in the future. 4. Up to 3 IdP signing keys are allowed in the metadata xml. When updating the provider's metadata xml, at least one non-expired signing key must overlap with the existing metadata. This requirement is skipped if there are no non-expired signing keys present in the existing metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#idp_metadata_xml GoogleIamWorkforcePoolProvider#idp_metadata_xml}
        '''
        value = GoogleIamWorkforcePoolProviderSaml(idp_metadata_xml=idp_metadata_xml)

        return typing.cast(None, jsii.invoke(self, "putSaml", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#create GoogleIamWorkforcePoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#delete GoogleIamWorkforcePoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#update GoogleIamWorkforcePoolProvider#update}.
        '''
        value = GoogleIamWorkforcePoolProviderTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAttributeCondition")
    def reset_attribute_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeCondition", []))

    @jsii.member(jsii_name="resetAttributeMapping")
    def reset_attribute_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeMapping", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetExtraAttributesOauth2Client")
    def reset_extra_attributes_oauth2_client(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraAttributesOauth2Client", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOidc")
    def reset_oidc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidc", []))

    @jsii.member(jsii_name="resetSaml")
    def reset_saml(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml", []))

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
    @jsii.member(jsii_name="extraAttributesOauth2Client")
    def extra_attributes_oauth2_client(
        self,
    ) -> "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference":
        return typing.cast("GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference", jsii.get(self, "extraAttributesOauth2Client"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oidc")
    def oidc(self) -> "GoogleIamWorkforcePoolProviderOidcOutputReference":
        return typing.cast("GoogleIamWorkforcePoolProviderOidcOutputReference", jsii.get(self, "oidc"))

    @builtins.property
    @jsii.member(jsii_name="saml")
    def saml(self) -> "GoogleIamWorkforcePoolProviderSamlOutputReference":
        return typing.cast("GoogleIamWorkforcePoolProviderSamlOutputReference", jsii.get(self, "saml"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleIamWorkforcePoolProviderTimeoutsOutputReference":
        return typing.cast("GoogleIamWorkforcePoolProviderTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="attributeConditionInput")
    def attribute_condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeMappingInput")
    def attribute_mapping_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "attributeMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="extraAttributesOauth2ClientInput")
    def extra_attributes_oauth2_client_input(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client"]:
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client"], jsii.get(self, "extraAttributesOauth2ClientInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcInput")
    def oidc_input(self) -> typing.Optional["GoogleIamWorkforcePoolProviderOidc"]:
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderOidc"], jsii.get(self, "oidcInput"))

    @builtins.property
    @jsii.member(jsii_name="providerIdInput")
    def provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="samlInput")
    def saml_input(self) -> typing.Optional["GoogleIamWorkforcePoolProviderSaml"]:
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderSaml"], jsii.get(self, "samlInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIamWorkforcePoolProviderTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIamWorkforcePoolProviderTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workforcePoolIdInput")
    def workforce_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workforcePoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeCondition")
    def attribute_condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeCondition"))

    @attribute_condition.setter
    def attribute_condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7af2300067617555e0bdee5c327dc178c3939403c07c86a5fb75462f42b70b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attributeMapping")
    def attribute_mapping(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "attributeMapping"))

    @attribute_mapping.setter
    def attribute_mapping(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bae040d091cf3161a863ae995490649ed9db58f7ecadef242d57b0d8a324f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ffcd3d30584702058ce249af860d8fe3cd4d96726002973d82ff247b7dce0eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe628da377271369ec659af7a2fd9043bc02eac65440e603565e436bd90d0f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8b82c0ab8e3ffa7da263600a154dc07dc9593d095e4d9a4a81758461e23a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adafeb2cc3de48dcf9b3f8fa2270b129e375fae52250b72d026263d5de2d4d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45eb01dc38753b2c4f3be6c79b9220e9a72618410ea99c6fdbb63261cb07078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerId")
    def provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerId"))

    @provider_id.setter
    def provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98ce78c3c1ff0769da788f3c55e276bf62a21286c414844030e286849868c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workforcePoolId")
    def workforce_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workforcePoolId"))

    @workforce_pool_id.setter
    def workforce_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553aa19d81b16963eca7cb6f4aa47369bf87f1b1be795fb45ed6107b33339ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workforcePoolId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "provider_id": "providerId",
        "workforce_pool_id": "workforcePoolId",
        "attribute_condition": "attributeCondition",
        "attribute_mapping": "attributeMapping",
        "description": "description",
        "disabled": "disabled",
        "display_name": "displayName",
        "extra_attributes_oauth2_client": "extraAttributesOauth2Client",
        "id": "id",
        "oidc": "oidc",
        "saml": "saml",
        "timeouts": "timeouts",
    },
)
class GoogleIamWorkforcePoolProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        provider_id: builtins.str,
        workforce_pool_id: builtins.str,
        attribute_condition: typing.Optional[builtins.str] = None,
        attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        extra_attributes_oauth2_client: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        saml: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#location GoogleIamWorkforcePoolProvider#location}
        :param provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#provider_id GoogleIamWorkforcePoolProvider#provider_id}
        :param workforce_pool_id: The ID to use for the pool, which becomes the final component of the resource name. The IDs must be a globally unique string of 6 to 63 lowercase letters, digits, or hyphens. It must start with a letter, and cannot have a trailing hyphen. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#workforce_pool_id GoogleIamWorkforcePoolProvider#workforce_pool_id}
        :param attribute_condition: A `Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: - 'assertion': JSON representing the authentication credential issued by the provider. - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. 'google.profile_photo' and 'google.display_name' are not supported. - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credentials will be accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#attribute_condition GoogleIamWorkforcePoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from the authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: - 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. This is a required field and the mapped subject cannot exceed 127 bytes. - 'google.groups': Groups the authenticating user belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. - 'google.display_name': The name of the authenticated user. This is an optional field and the mapped display name cannot exceed 100 bytes. If not set, 'google.subject' will be displayed instead. This attribute cannot be referenced in IAM bindings. - 'google.profile_photo': The URL that specifies the authenticated user's thumbnail photo. This is an optional field. When set, the image will be visible as the user's profile picture. If not set, a generic user icon will be displayed instead. This attribute cannot be referenced in IAM bindings. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where {custom_attribute} is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workforce pool to Google Cloud resources. For example: - 'google.subject': 'principal://iam.googleapis.com/locations/{location}/workforcePools/{pool}/subject/{value}' - 'google.groups': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/group/{value}' - 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For OIDC providers, you must supply a custom mapping that includes the 'google.subject' attribute. For example, the following maps the sub claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} An object containing a list of '"key": value' pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#attribute_mapping GoogleIamWorkforcePoolProvider#attribute_mapping}
        :param description: A user-specified description of the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#description GoogleIamWorkforcePoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#disabled GoogleIamWorkforcePoolProvider#disabled}
        :param display_name: A user-specified display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#display_name GoogleIamWorkforcePoolProvider#display_name}
        :param extra_attributes_oauth2_client: extra_attributes_oauth2_client block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#extra_attributes_oauth2_client GoogleIamWorkforcePoolProvider#extra_attributes_oauth2_client}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#id GoogleIamWorkforcePoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#oidc GoogleIamWorkforcePoolProvider#oidc}
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#saml GoogleIamWorkforcePoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#timeouts GoogleIamWorkforcePoolProvider#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(extra_attributes_oauth2_client, dict):
            extra_attributes_oauth2_client = GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client(**extra_attributes_oauth2_client)
        if isinstance(oidc, dict):
            oidc = GoogleIamWorkforcePoolProviderOidc(**oidc)
        if isinstance(saml, dict):
            saml = GoogleIamWorkforcePoolProviderSaml(**saml)
        if isinstance(timeouts, dict):
            timeouts = GoogleIamWorkforcePoolProviderTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40246723df2937e5d6eb80758bf84fe80d137020704a3172a5be320602f4b893)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument provider_id", value=provider_id, expected_type=type_hints["provider_id"])
            check_type(argname="argument workforce_pool_id", value=workforce_pool_id, expected_type=type_hints["workforce_pool_id"])
            check_type(argname="argument attribute_condition", value=attribute_condition, expected_type=type_hints["attribute_condition"])
            check_type(argname="argument attribute_mapping", value=attribute_mapping, expected_type=type_hints["attribute_mapping"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument extra_attributes_oauth2_client", value=extra_attributes_oauth2_client, expected_type=type_hints["extra_attributes_oauth2_client"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument oidc", value=oidc, expected_type=type_hints["oidc"])
            check_type(argname="argument saml", value=saml, expected_type=type_hints["saml"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "provider_id": provider_id,
            "workforce_pool_id": workforce_pool_id,
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
        if attribute_condition is not None:
            self._values["attribute_condition"] = attribute_condition
        if attribute_mapping is not None:
            self._values["attribute_mapping"] = attribute_mapping
        if description is not None:
            self._values["description"] = description
        if disabled is not None:
            self._values["disabled"] = disabled
        if display_name is not None:
            self._values["display_name"] = display_name
        if extra_attributes_oauth2_client is not None:
            self._values["extra_attributes_oauth2_client"] = extra_attributes_oauth2_client
        if id is not None:
            self._values["id"] = id
        if oidc is not None:
            self._values["oidc"] = oidc
        if saml is not None:
            self._values["saml"] = saml
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
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#location GoogleIamWorkforcePoolProvider#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_id(self) -> builtins.str:
        '''The ID for the provider, which becomes the final component of the resource name.

        This value must be 4-32 characters, and may contain the characters [a-z0-9-].
        The prefix 'gcp-' is reserved for use by Google, and may not be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#provider_id GoogleIamWorkforcePoolProvider#provider_id}
        '''
        result = self._values.get("provider_id")
        assert result is not None, "Required property 'provider_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workforce_pool_id(self) -> builtins.str:
        '''The ID to use for the pool, which becomes the final component of the resource name.

        The IDs must be a globally unique string of 6 to 63 lowercase letters, digits, or hyphens.
        It must start with a letter, and cannot have a trailing hyphen.
        The prefix 'gcp-' is reserved for use by Google, and may not be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#workforce_pool_id GoogleIamWorkforcePoolProvider#workforce_pool_id}
        '''
        result = self._values.get("workforce_pool_id")
        assert result is not None, "Required property 'workforce_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attribute_condition(self) -> typing.Optional[builtins.str]:
        '''A `Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted.

        The expression must output a boolean representing whether to allow the federation.

        The following keywords may be referenced in the expressions:

        - 'assertion': JSON representing the authentication credential issued by the provider.
        - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'.
          'google.profile_photo' and 'google.display_name' are not supported.
        - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'.

        The maximum length of the attribute condition expression is 4096 characters.
        If unspecified, all valid authentication credentials will be accepted.

        The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins'::

           "'admins' in google.groups"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#attribute_condition GoogleIamWorkforcePoolProvider#attribute_condition}
        '''
        result = self._values.get("attribute_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attribute_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Maps attributes from the authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'.

        Each key must be a string specifying the Google Cloud IAM attribute to map to.

        The following keys are supported:

        - 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings.
          This is also the subject that appears in Cloud Logging logs. This is a required field and
          the mapped subject cannot exceed 127 bytes.
        - 'google.groups': Groups the authenticating user belongs to. You can grant groups access to
          resources using an IAM 'principalSet' binding; access applies to all members of the group.
        - 'google.display_name': The name of the authenticated user. This is an optional field and
          the mapped display name cannot exceed 100 bytes. If not set, 'google.subject' will be displayed instead.
          This attribute cannot be referenced in IAM bindings.
        - 'google.profile_photo': The URL that specifies the authenticated user's thumbnail photo.
          This is an optional field. When set, the image will be visible as the user's profile picture.
          If not set, a generic user icon will be displayed instead.
          This attribute cannot be referenced in IAM bindings.

        You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where {custom_attribute}
        is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes.
        The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_].

        You can reference these attributes in IAM policies to define fine-grained access for a workforce pool
        to Google Cloud resources. For example:

        - 'google.subject':
          'principal://iam.googleapis.com/locations/{location}/workforcePools/{pool}/subject/{value}'
        - 'google.groups':
          'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/group/{value}'
        - 'attribute.{custom_attribute}':
          'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/attribute.{custom_attribute}/{value}'

        Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_
        function that maps an identity provider credential to the normalized attribute specified
        by the corresponding map key.

        You can use the 'assertion' keyword in the expression to access a JSON representation of
        the authentication credential issued by the provider.

        The maximum length of an attribute mapping expression is 2048 characters. When evaluated,
        the total size of all mapped attributes must not exceed 8KB.

        For OIDC providers, you must supply a custom mapping that includes the 'google.subject' attribute.
        For example, the following maps the sub claim of the incoming credential to the 'subject' attribute
        on a Google token::

           {"google.subject": "assertion.sub"}

        An object containing a list of '"key": value' pairs.
        Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#attribute_mapping GoogleIamWorkforcePoolProvider#attribute_mapping}
        '''
        result = self._values.get("attribute_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A user-specified description of the provider. Cannot exceed 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#description GoogleIamWorkforcePoolProvider#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#disabled GoogleIamWorkforcePoolProvider#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-specified display name for the provider. Cannot exceed 32 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#display_name GoogleIamWorkforcePoolProvider#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_attributes_oauth2_client(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client"]:
        '''extra_attributes_oauth2_client block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#extra_attributes_oauth2_client GoogleIamWorkforcePoolProvider#extra_attributes_oauth2_client}
        '''
        result = self._values.get("extra_attributes_oauth2_client")
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#id GoogleIamWorkforcePoolProvider#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc(self) -> typing.Optional["GoogleIamWorkforcePoolProviderOidc"]:
        '''oidc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#oidc GoogleIamWorkforcePoolProvider#oidc}
        '''
        result = self._values.get("oidc")
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderOidc"], result)

    @builtins.property
    def saml(self) -> typing.Optional["GoogleIamWorkforcePoolProviderSaml"]:
        '''saml block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#saml GoogleIamWorkforcePoolProvider#saml}
        '''
        result = self._values.get("saml")
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderSaml"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleIamWorkforcePoolProviderTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#timeouts GoogleIamWorkforcePoolProvider#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client",
    jsii_struct_bases=[],
    name_mapping={
        "attributes_type": "attributesType",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "issuer_uri": "issuerUri",
        "query_parameters": "queryParameters",
    },
)
class GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client:
    def __init__(
        self,
        *,
        attributes_type: builtins.str,
        client_id: builtins.str,
        client_secret: typing.Union["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret", typing.Dict[builtins.str, typing.Any]],
        issuer_uri: builtins.str,
        query_parameters: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param attributes_type: Represents the IdP and type of claims that should be fetched. - AZURE_AD_GROUPS_MAIL: Used to get the user's group claims from the Azure AD identity provider using configuration provided in ExtraAttributesOAuth2Client and 'mail' property of the 'microsoft.graph.group' object is used for claim mapping. See https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties for more details on 'microsoft.graph.group' properties. The attributes obtained from idntity provider are mapped to 'assertion.groups'. - AZURE_AD_GROUPS_ID: Used to get the user's group claims from the Azure AD identity provider using configuration provided in ExtraAttributesOAuth2Client and 'id' property of the 'microsoft.graph.group' object is used for claim mapping. See https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties for more details on 'microsoft.graph.group' properties. The group IDs obtained from Azure AD are present in 'assertion.groups' for OIDC providers and 'assertion.attributes.groups' for SAML providers for attribute mapping. Possible values: ["AZURE_AD_GROUPS_MAIL", "AZURE_AD_GROUPS_ID"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#attributes_type GoogleIamWorkforcePoolProvider#attributes_type}
        :param client_id: The OAuth 2.0 client ID for retrieving extra attributes from the identity provider. Required to get the Access Token using client credentials grant flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_id GoogleIamWorkforcePoolProvider#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_secret GoogleIamWorkforcePoolProvider#client_secret}
        :param issuer_uri: The OIDC identity provider's issuer URI. Must be a valid URI using the 'https' scheme. Required to get the OIDC discovery document. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#issuer_uri GoogleIamWorkforcePoolProvider#issuer_uri}
        :param query_parameters: query_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#query_parameters GoogleIamWorkforcePoolProvider#query_parameters}
        '''
        if isinstance(client_secret, dict):
            client_secret = GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret(**client_secret)
        if isinstance(query_parameters, dict):
            query_parameters = GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters(**query_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09bdee81b6ed8c968647fe6aed6e7b5f3db220e53adf55093b7c3069fd811695)
            check_type(argname="argument attributes_type", value=attributes_type, expected_type=type_hints["attributes_type"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument issuer_uri", value=issuer_uri, expected_type=type_hints["issuer_uri"])
            check_type(argname="argument query_parameters", value=query_parameters, expected_type=type_hints["query_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attributes_type": attributes_type,
            "client_id": client_id,
            "client_secret": client_secret,
            "issuer_uri": issuer_uri,
        }
        if query_parameters is not None:
            self._values["query_parameters"] = query_parameters

    @builtins.property
    def attributes_type(self) -> builtins.str:
        '''Represents the IdP and type of claims that should be fetched.

        - AZURE_AD_GROUPS_MAIL: Used to get the user's group claims from the Azure AD identity provider using configuration provided
          in ExtraAttributesOAuth2Client and 'mail' property of the 'microsoft.graph.group' object is used for claim mapping.
          See https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties for more details on
          'microsoft.graph.group' properties. The attributes obtained from idntity provider are mapped to 'assertion.groups'.
        - AZURE_AD_GROUPS_ID:  Used to get the user's group claims from the Azure AD identity provider
          using configuration provided in ExtraAttributesOAuth2Client and 'id'
          property of the 'microsoft.graph.group' object is used for claim mapping. See
          https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties
          for more details on 'microsoft.graph.group' properties. The
          group IDs obtained from Azure AD are present in 'assertion.groups' for
          OIDC providers and 'assertion.attributes.groups' for SAML providers for
          attribute mapping. Possible values: ["AZURE_AD_GROUPS_MAIL", "AZURE_AD_GROUPS_ID"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#attributes_type GoogleIamWorkforcePoolProvider#attributes_type}
        '''
        result = self._values.get("attributes_type")
        assert result is not None, "Required property 'attributes_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OAuth 2.0 client ID for retrieving extra attributes from the identity provider. Required to get the Access Token using client credentials grant flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_id GoogleIamWorkforcePoolProvider#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(
        self,
    ) -> "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret":
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_secret GoogleIamWorkforcePoolProvider#client_secret}
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast("GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret", result)

    @builtins.property
    def issuer_uri(self) -> builtins.str:
        '''The OIDC identity provider's issuer URI.

        Must be a valid URI using the 'https' scheme. Required to get the OIDC discovery document.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#issuer_uri GoogleIamWorkforcePoolProvider#issuer_uri}
        '''
        result = self._values.get("issuer_uri")
        assert result is not None, "Required property 'issuer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_parameters(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters"]:
        '''query_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#query_parameters GoogleIamWorkforcePoolProvider#query_parameters}
        '''
        result = self._values.get("query_parameters")
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret:
    def __init__(
        self,
        *,
        value: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#value GoogleIamWorkforcePoolProvider#value}
        '''
        if isinstance(value, dict):
            value = GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a268749c3d028e23b2506e80731d41e43b142f48f2ce3afdd6b37b8734abdb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#value GoogleIamWorkforcePoolProvider#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77b2798c118b6550bcd67b5a33f33d9baf983db6999850bea7ae4e524e917b6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putValue")
    def put_value(self, *, plain_text: builtins.str) -> None:
        '''
        :param plain_text: The plain text of the client secret value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#plain_text GoogleIamWorkforcePoolProvider#plain_text}
        '''
        value = GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue(
            plain_text=plain_text
        )

        return typing.cast(None, jsii.invoke(self, "putValue", [value]))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference":
        return typing.cast("GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue"]:
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b29af157b9bdd8eb3edf2f27ce9157b1c7cfa691cf55e339ddb632325e5130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue",
    jsii_struct_bases=[],
    name_mapping={"plain_text": "plainText"},
)
class GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue:
    def __init__(self, *, plain_text: builtins.str) -> None:
        '''
        :param plain_text: The plain text of the client secret value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#plain_text GoogleIamWorkforcePoolProvider#plain_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5df51a87c7f575fa05c1d221519c6d9f59a38bd60b91ecffa6f9e4b3e4fdc81)
            check_type(argname="argument plain_text", value=plain_text, expected_type=type_hints["plain_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plain_text": plain_text,
        }

    @builtins.property
    def plain_text(self) -> builtins.str:
        '''The plain text of the client secret value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#plain_text GoogleIamWorkforcePoolProvider#plain_text}
        '''
        result = self._values.get("plain_text")
        assert result is not None, "Required property 'plain_text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cde047f9bbdd9726bceb5ba5e54ed9c05ab9b3ac4e197c72c0e1908f7e01be87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="plainTextInput")
    def plain_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "plainTextInput"))

    @builtins.property
    @jsii.member(jsii_name="plainText")
    def plain_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "plainText"))

    @plain_text.setter
    def plain_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682178f467349303bc3adb3130988bb8d7c7e4643f72448feb5d3d9872d0b987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plainText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e12b199e4b8f7588b886bdc58c9ad4c8d4cede605891c6b513e9a1b95e7291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f7f7826a86864db233f4e7f25e94ce69d7cf9c0fe9ca7a36ea994b7aa2b9afa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(
        self,
        *,
        value: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#value GoogleIamWorkforcePoolProvider#value}
        '''
        value_ = GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret(
            value=value
        )

        return typing.cast(None, jsii.invoke(self, "putClientSecret", [value_]))

    @jsii.member(jsii_name="putQueryParameters")
    def put_query_parameters(
        self,
        *,
        filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter: The filter used to request specific records from IdP. In case of attributes type as AZURE_AD_GROUPS_MAIL and AZURE_AD_GROUPS_ID, it represents the filter used to request specific groups for users from IdP. By default, all of the groups associated with the user are fetched. The groups should be security enabled. See https://learn.microsoft.com/en-us/graph/search-query-parameter for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#filter GoogleIamWorkforcePoolProvider#filter}
        '''
        value = GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters(
            filter=filter
        )

        return typing.cast(None, jsii.invoke(self, "putQueryParameters", [value]))

    @jsii.member(jsii_name="resetQueryParameters")
    def reset_query_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParameters", []))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(
        self,
    ) -> GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference:
        return typing.cast(GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="queryParameters")
    def query_parameters(
        self,
    ) -> "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference":
        return typing.cast("GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference", jsii.get(self, "queryParameters"))

    @builtins.property
    @jsii.member(jsii_name="attributesTypeInput")
    def attributes_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributesTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(
        self,
    ) -> typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUriInput")
    def issuer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParametersInput")
    def query_parameters_input(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters"]:
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters"], jsii.get(self, "queryParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesType")
    def attributes_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributesType"))

    @attributes_type.setter
    def attributes_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c657fc93d0bdf1e481fd7571bbb59aad0895d2fbcf8094e1dab4c916f82d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributesType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa68a1b558228a5d4c10cad32cdbf4dd6c305f8161c585c79df4f917d4a2ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa1b062a82c8ffe09c5aad2a33c2cf94f9da9893785867c884fd13bb5177ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f0adcf1514f7c0034eeb38ee844df125920a0a070a985767aa760cc7efec61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters:
    def __init__(self, *, filter: typing.Optional[builtins.str] = None) -> None:
        '''
        :param filter: The filter used to request specific records from IdP. In case of attributes type as AZURE_AD_GROUPS_MAIL and AZURE_AD_GROUPS_ID, it represents the filter used to request specific groups for users from IdP. By default, all of the groups associated with the user are fetched. The groups should be security enabled. See https://learn.microsoft.com/en-us/graph/search-query-parameter for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#filter GoogleIamWorkforcePoolProvider#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1649f2574e75ae079c092c1a3ef43a49e1f44a911ac5b70cdf4cd42e5d7716d8)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''The filter used to request specific records from IdP.

        In case of attributes type as AZURE_AD_GROUPS_MAIL and AZURE_AD_GROUPS_ID, it represents the
        filter used to request specific groups for users from IdP. By default, all of the groups associated with the user are fetched. The
        groups should be security enabled. See https://learn.microsoft.com/en-us/graph/search-query-parameter for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#filter GoogleIamWorkforcePoolProvider#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6dc21617bc0ee3a85e021d6b84369bcd3389a09f2673620bcb2f7f8d2929103)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a125436394b2acb3804556d0314a0ed8f22654ad1ed64c67c59da254042d67c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323f9e398a1ea0b3ff13d14fba0da17bab1ed52da15b3d4b97b8eef9bd233843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderOidc",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "issuer_uri": "issuerUri",
        "client_secret": "clientSecret",
        "jwks_json": "jwksJson",
        "web_sso_config": "webSsoConfig",
    },
)
class GoogleIamWorkforcePoolProviderOidc:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        issuer_uri: builtins.str,
        client_secret: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderOidcClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        jwks_json: typing.Optional[builtins.str] = None,
        web_sso_config: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderOidcWebSsoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: The client ID. Must match the audience claim of the JWT issued by the identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_id GoogleIamWorkforcePoolProvider#client_id}
        :param issuer_uri: The OIDC issuer URI. Must be a valid URI using the 'https' scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#issuer_uri GoogleIamWorkforcePoolProvider#issuer_uri}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_secret GoogleIamWorkforcePoolProvider#client_secret}
        :param jwks_json: OIDC JWKs in JSON String format. For details on definition of a JWK, see https:tools.ietf.org/html/rfc7517. If not set, then we use the 'jwks_uri' from the discovery document fetched from the .well-known path for the 'issuer_uri'. Currently, RSA and EC asymmetric keys are supported. The JWK must use following format and include only the following fields:: { "keys": [ { "kty": "RSA/EC", "alg": "<algorithm>", "use": "sig", "kid": "<key-id>", "n": "", "e": "", "x": "", "y": "", "crv": "" } ] } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#jwks_json GoogleIamWorkforcePoolProvider#jwks_json}
        :param web_sso_config: web_sso_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#web_sso_config GoogleIamWorkforcePoolProvider#web_sso_config}
        '''
        if isinstance(client_secret, dict):
            client_secret = GoogleIamWorkforcePoolProviderOidcClientSecret(**client_secret)
        if isinstance(web_sso_config, dict):
            web_sso_config = GoogleIamWorkforcePoolProviderOidcWebSsoConfig(**web_sso_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2eaa733147e60b682318c6347036312ae597108ac13f9922af518b83204aa6)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument issuer_uri", value=issuer_uri, expected_type=type_hints["issuer_uri"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument jwks_json", value=jwks_json, expected_type=type_hints["jwks_json"])
            check_type(argname="argument web_sso_config", value=web_sso_config, expected_type=type_hints["web_sso_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "issuer_uri": issuer_uri,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if jwks_json is not None:
            self._values["jwks_json"] = jwks_json
        if web_sso_config is not None:
            self._values["web_sso_config"] = web_sso_config

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client ID. Must match the audience claim of the JWT issued by the identity provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_id GoogleIamWorkforcePoolProvider#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer_uri(self) -> builtins.str:
        '''The OIDC issuer URI. Must be a valid URI using the 'https' scheme.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#issuer_uri GoogleIamWorkforcePoolProvider#issuer_uri}
        '''
        result = self._values.get("issuer_uri")
        assert result is not None, "Required property 'issuer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderOidcClientSecret"]:
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#client_secret GoogleIamWorkforcePoolProvider#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderOidcClientSecret"], result)

    @builtins.property
    def jwks_json(self) -> typing.Optional[builtins.str]:
        '''OIDC JWKs in JSON String format.

        For details on definition of a
        JWK, see https:tools.ietf.org/html/rfc7517. If not set, then we
        use the 'jwks_uri' from the discovery document fetched from the
        .well-known path for the 'issuer_uri'. Currently, RSA and EC asymmetric
        keys are supported. The JWK must use following format and include only
        the following fields::

           {
             "keys": [
               {
                     "kty": "RSA/EC",
                     "alg": "<algorithm>",
                     "use": "sig",
                     "kid": "<key-id>",
                     "n": "",
                     "e": "",
                     "x": "",
                     "y": "",
                     "crv": ""
               }
             ]
           }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#jwks_json GoogleIamWorkforcePoolProvider#jwks_json}
        '''
        result = self._values.get("jwks_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_sso_config(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderOidcWebSsoConfig"]:
        '''web_sso_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#web_sso_config GoogleIamWorkforcePoolProvider#web_sso_config}
        '''
        result = self._values.get("web_sso_config")
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderOidcWebSsoConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderOidcClientSecret",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class GoogleIamWorkforcePoolProviderOidcClientSecret:
    def __init__(
        self,
        *,
        value: typing.Optional[typing.Union["GoogleIamWorkforcePoolProviderOidcClientSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#value GoogleIamWorkforcePoolProvider#value}
        '''
        if isinstance(value, dict):
            value = GoogleIamWorkforcePoolProviderOidcClientSecretValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9dd6543f37bfe8c7392c038aa43e88fecba5ed4e8f093b61cd5564c91ea393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderOidcClientSecretValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#value GoogleIamWorkforcePoolProvider#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderOidcClientSecretValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderOidcClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkforcePoolProviderOidcClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderOidcClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f53f254d001e1c425e854a04ed7645ab930fe8b6879351030df76314c11d85d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putValue")
    def put_value(self, *, plain_text: builtins.str) -> None:
        '''
        :param plain_text: The plain text of the client secret value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#plain_text GoogleIamWorkforcePoolProvider#plain_text}
        '''
        value = GoogleIamWorkforcePoolProviderOidcClientSecretValue(
            plain_text=plain_text
        )

        return typing.cast(None, jsii.invoke(self, "putValue", [value]))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> "GoogleIamWorkforcePoolProviderOidcClientSecretValueOutputReference":
        return typing.cast("GoogleIamWorkforcePoolProviderOidcClientSecretValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderOidcClientSecretValue"]:
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderOidcClientSecretValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecret]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97c84946ecdbea5018a8af616caf098f6c51ee13000f9fd631871a28740656f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderOidcClientSecretValue",
    jsii_struct_bases=[],
    name_mapping={"plain_text": "plainText"},
)
class GoogleIamWorkforcePoolProviderOidcClientSecretValue:
    def __init__(self, *, plain_text: builtins.str) -> None:
        '''
        :param plain_text: The plain text of the client secret value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#plain_text GoogleIamWorkforcePoolProvider#plain_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e369ac7094fe0a3a6a9c91e217553a93379c75d88801bc22c7cc2d2e1760fed2)
            check_type(argname="argument plain_text", value=plain_text, expected_type=type_hints["plain_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plain_text": plain_text,
        }

    @builtins.property
    def plain_text(self) -> builtins.str:
        '''The plain text of the client secret value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#plain_text GoogleIamWorkforcePoolProvider#plain_text}
        '''
        result = self._values.get("plain_text")
        assert result is not None, "Required property 'plain_text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderOidcClientSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkforcePoolProviderOidcClientSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderOidcClientSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed0c4f0e375ab7fd006a12722374bb54891ffaaae3fd294d6c35865f7e7b0fba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @builtins.property
    @jsii.member(jsii_name="plainTextInput")
    def plain_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "plainTextInput"))

    @builtins.property
    @jsii.member(jsii_name="plainText")
    def plain_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "plainText"))

    @plain_text.setter
    def plain_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eefccbac3e176f0678507b87388da68cd4f860c12631a1b05abcfbd276dd033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plainText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecretValue]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4774f33f22019945336d1522ba9f993ceab8116e8b085f1faf8a4c1abd77e7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIamWorkforcePoolProviderOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3406116e0f7fb0d68899846e363f4c3799cd3e4cfe45afa4e6829fd8d092112a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(
        self,
        *,
        value: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderOidcClientSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#value GoogleIamWorkforcePoolProvider#value}
        '''
        value_ = GoogleIamWorkforcePoolProviderOidcClientSecret(value=value)

        return typing.cast(None, jsii.invoke(self, "putClientSecret", [value_]))

    @jsii.member(jsii_name="putWebSsoConfig")
    def put_web_sso_config(
        self,
        *,
        assertion_claims_behavior: builtins.str,
        response_type: builtins.str,
        additional_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param assertion_claims_behavior: The behavior for how OIDC Claims are included in the 'assertion' object used for attribute mapping and attribute condition. - MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS: Merge the UserInfo Endpoint Claims with ID Token Claims, preferring UserInfo Claim Values for the same Claim Name. This option is available only for the Authorization Code Flow. - ONLY_ID_TOKEN_CLAIMS: Only include ID Token Claims. Possible values: ["MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS", "ONLY_ID_TOKEN_CLAIMS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#assertion_claims_behavior GoogleIamWorkforcePoolProvider#assertion_claims_behavior}
        :param response_type: The Response Type to request for in the OIDC Authorization Request for web sign-in. The 'CODE' Response Type is recommended to avoid the Implicit Flow, for security reasons. - CODE: The 'response_type=code' selection uses the Authorization Code Flow for web sign-in. Requires a configured client secret. - ID_TOKEN: The 'response_type=id_token' selection uses the Implicit Flow for web sign-in. Possible values: ["CODE", "ID_TOKEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#response_type GoogleIamWorkforcePoolProvider#response_type}
        :param additional_scopes: Additional scopes to request for in the OIDC authentication request on top of scopes requested by default. By default, the 'openid', 'profile' and 'email' scopes that are supported by the identity provider are requested. Each additional scope may be at most 256 characters. A maximum of 10 additional scopes may be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#additional_scopes GoogleIamWorkforcePoolProvider#additional_scopes}
        '''
        value = GoogleIamWorkforcePoolProviderOidcWebSsoConfig(
            assertion_claims_behavior=assertion_claims_behavior,
            response_type=response_type,
            additional_scopes=additional_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putWebSsoConfig", [value]))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetJwksJson")
    def reset_jwks_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwksJson", []))

    @jsii.member(jsii_name="resetWebSsoConfig")
    def reset_web_sso_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebSsoConfig", []))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(
        self,
    ) -> GoogleIamWorkforcePoolProviderOidcClientSecretOutputReference:
        return typing.cast(GoogleIamWorkforcePoolProviderOidcClientSecretOutputReference, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="webSsoConfig")
    def web_sso_config(
        self,
    ) -> "GoogleIamWorkforcePoolProviderOidcWebSsoConfigOutputReference":
        return typing.cast("GoogleIamWorkforcePoolProviderOidcWebSsoConfigOutputReference", jsii.get(self, "webSsoConfig"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(
        self,
    ) -> typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecret]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecret], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUriInput")
    def issuer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="jwksJsonInput")
    def jwks_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwksJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="webSsoConfigInput")
    def web_sso_config_input(
        self,
    ) -> typing.Optional["GoogleIamWorkforcePoolProviderOidcWebSsoConfig"]:
        return typing.cast(typing.Optional["GoogleIamWorkforcePoolProviderOidcWebSsoConfig"], jsii.get(self, "webSsoConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c908224c51bff347e2791220f31300325649fa8122f2fb095c97dce550ed7a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ab77a030dde76e9cba83445f973a60246a044359a725b6b7f32abfd885bb45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwksJson")
    def jwks_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwksJson"))

    @jwks_json.setter
    def jwks_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faab493ce397271c85cd854dda89ae636176d8352005ded7665154bb217b1d58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwksJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIamWorkforcePoolProviderOidc]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkforcePoolProviderOidc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ead7c73e9d8e722528729ef9a2bf7adc5867a4090a6ecd901da3ec7c5eb0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderOidcWebSsoConfig",
    jsii_struct_bases=[],
    name_mapping={
        "assertion_claims_behavior": "assertionClaimsBehavior",
        "response_type": "responseType",
        "additional_scopes": "additionalScopes",
    },
)
class GoogleIamWorkforcePoolProviderOidcWebSsoConfig:
    def __init__(
        self,
        *,
        assertion_claims_behavior: builtins.str,
        response_type: builtins.str,
        additional_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param assertion_claims_behavior: The behavior for how OIDC Claims are included in the 'assertion' object used for attribute mapping and attribute condition. - MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS: Merge the UserInfo Endpoint Claims with ID Token Claims, preferring UserInfo Claim Values for the same Claim Name. This option is available only for the Authorization Code Flow. - ONLY_ID_TOKEN_CLAIMS: Only include ID Token Claims. Possible values: ["MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS", "ONLY_ID_TOKEN_CLAIMS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#assertion_claims_behavior GoogleIamWorkforcePoolProvider#assertion_claims_behavior}
        :param response_type: The Response Type to request for in the OIDC Authorization Request for web sign-in. The 'CODE' Response Type is recommended to avoid the Implicit Flow, for security reasons. - CODE: The 'response_type=code' selection uses the Authorization Code Flow for web sign-in. Requires a configured client secret. - ID_TOKEN: The 'response_type=id_token' selection uses the Implicit Flow for web sign-in. Possible values: ["CODE", "ID_TOKEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#response_type GoogleIamWorkforcePoolProvider#response_type}
        :param additional_scopes: Additional scopes to request for in the OIDC authentication request on top of scopes requested by default. By default, the 'openid', 'profile' and 'email' scopes that are supported by the identity provider are requested. Each additional scope may be at most 256 characters. A maximum of 10 additional scopes may be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#additional_scopes GoogleIamWorkforcePoolProvider#additional_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70a911a30575d21717c76b25ed9111cbf5f9461ff8469e91919c694f9802ec6)
            check_type(argname="argument assertion_claims_behavior", value=assertion_claims_behavior, expected_type=type_hints["assertion_claims_behavior"])
            check_type(argname="argument response_type", value=response_type, expected_type=type_hints["response_type"])
            check_type(argname="argument additional_scopes", value=additional_scopes, expected_type=type_hints["additional_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assertion_claims_behavior": assertion_claims_behavior,
            "response_type": response_type,
        }
        if additional_scopes is not None:
            self._values["additional_scopes"] = additional_scopes

    @builtins.property
    def assertion_claims_behavior(self) -> builtins.str:
        '''The behavior for how OIDC Claims are included in the 'assertion' object used for attribute mapping and attribute condition.

        - MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS: Merge the UserInfo Endpoint Claims with ID Token Claims, preferring UserInfo Claim Values for the same Claim Name. This option is available only for the Authorization Code Flow.
        - ONLY_ID_TOKEN_CLAIMS: Only include ID Token Claims. Possible values: ["MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS", "ONLY_ID_TOKEN_CLAIMS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#assertion_claims_behavior GoogleIamWorkforcePoolProvider#assertion_claims_behavior}
        '''
        result = self._values.get("assertion_claims_behavior")
        assert result is not None, "Required property 'assertion_claims_behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def response_type(self) -> builtins.str:
        '''The Response Type to request for in the OIDC Authorization Request for web sign-in.

        The 'CODE' Response Type is recommended to avoid the Implicit Flow, for security reasons.

        - CODE: The 'response_type=code' selection uses the Authorization Code Flow for web sign-in. Requires a configured client secret.
        - ID_TOKEN: The 'response_type=id_token' selection uses the Implicit Flow for web sign-in. Possible values: ["CODE", "ID_TOKEN"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#response_type GoogleIamWorkforcePoolProvider#response_type}
        '''
        result = self._values.get("response_type")
        assert result is not None, "Required property 'response_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional scopes to request for in the OIDC authentication request on top of scopes requested by default.

        By default, the 'openid', 'profile' and 'email' scopes that are supported by the identity provider are requested.
        Each additional scope may be at most 256 characters. A maximum of 10 additional scopes may be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#additional_scopes GoogleIamWorkforcePoolProvider#additional_scopes}
        '''
        result = self._values.get("additional_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderOidcWebSsoConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkforcePoolProviderOidcWebSsoConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderOidcWebSsoConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45056b9d866acbfe2bca4546d060624ddc635b2d20f6c20b45ad3a6078123f9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalScopes")
    def reset_additional_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalScopes", []))

    @builtins.property
    @jsii.member(jsii_name="additionalScopesInput")
    def additional_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="assertionClaimsBehaviorInput")
    def assertion_claims_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assertionClaimsBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="responseTypeInput")
    def response_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalScopes")
    def additional_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalScopes"))

    @additional_scopes.setter
    def additional_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf499eb1209fc9d5d08322c4b5b766c33cdc011cf333272a74b7df34c5af54e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assertionClaimsBehavior")
    def assertion_claims_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assertionClaimsBehavior"))

    @assertion_claims_behavior.setter
    def assertion_claims_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77275b8c56d5613314c558db10a4986760753e3084e3bfbb1885ef3fc1b6f5c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assertionClaimsBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseType")
    def response_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseType"))

    @response_type.setter
    def response_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538f2fed1aa77aef00fbf7ce7a8087099df2964ea4bdae24aadf8e70b63dbec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkforcePoolProviderOidcWebSsoConfig]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderOidcWebSsoConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkforcePoolProviderOidcWebSsoConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb9a115f8180b4721cd94743a7b38c134dcbe3a985802d6b69fade755c380ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderSaml",
    jsii_struct_bases=[],
    name_mapping={"idp_metadata_xml": "idpMetadataXml"},
)
class GoogleIamWorkforcePoolProviderSaml:
    def __init__(self, *, idp_metadata_xml: builtins.str) -> None:
        '''
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. The xml document should comply with `SAML 2.0 specification <https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf>`_. The max size of the acceptable xml document will be bounded to 128k characters. The metadata xml document should satisfy the following constraints: 1. Must contain an Identity Provider Entity ID. 2. Must contain at least one non-expired signing key certificate. 3. For each signing key: a) Valid from should be no more than 7 days from now. b) Valid to should be no more than 10 years in the future. 4. Up to 3 IdP signing keys are allowed in the metadata xml. When updating the provider's metadata xml, at least one non-expired signing key must overlap with the existing metadata. This requirement is skipped if there are no non-expired signing keys present in the existing metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#idp_metadata_xml GoogleIamWorkforcePoolProvider#idp_metadata_xml}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3325494a4c6cf016e6aeb58edb55aa04925c84d3a344be039ec12c84d20be606)
            check_type(argname="argument idp_metadata_xml", value=idp_metadata_xml, expected_type=type_hints["idp_metadata_xml"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "idp_metadata_xml": idp_metadata_xml,
        }

    @builtins.property
    def idp_metadata_xml(self) -> builtins.str:
        '''SAML Identity provider configuration metadata xml doc.

        The xml document should comply with `SAML 2.0 specification <https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf>`_.
        The max size of the acceptable xml document will be bounded to 128k characters.

        The metadata xml document should satisfy the following constraints:

        1. Must contain an Identity Provider Entity ID.
        2. Must contain at least one non-expired signing key certificate.
        3. For each signing key:
           a) Valid from should be no more than 7 days from now.
           b) Valid to should be no more than 10 years in the future.
        4. Up to 3 IdP signing keys are allowed in the metadata xml.

        When updating the provider's metadata xml, at least one non-expired signing key
        must overlap with the existing metadata. This requirement is skipped if there are
        no non-expired signing keys present in the existing metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#idp_metadata_xml GoogleIamWorkforcePoolProvider#idp_metadata_xml}
        '''
        result = self._values.get("idp_metadata_xml")
        assert result is not None, "Required property 'idp_metadata_xml' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderSaml(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkforcePoolProviderSamlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderSamlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf9292733df99bb5001a597175d73d1919bec4ebd74120e96f3dc0789c8008f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idpMetadataXmlInput")
    def idp_metadata_xml_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idpMetadataXmlInput"))

    @builtins.property
    @jsii.member(jsii_name="idpMetadataXml")
    def idp_metadata_xml(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpMetadataXml"))

    @idp_metadata_xml.setter
    def idp_metadata_xml(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39bcf503b1589030fd80d79cb7b7261193382269e3bb3335d9d76c14603bf639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpMetadataXml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIamWorkforcePoolProviderSaml]:
        return typing.cast(typing.Optional[GoogleIamWorkforcePoolProviderSaml], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkforcePoolProviderSaml],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98266b606d40ae0d5141a96b4ec686e96aff4176e9990b8ac44a6775cc4cd928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleIamWorkforcePoolProviderTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#create GoogleIamWorkforcePoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#delete GoogleIamWorkforcePoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#update GoogleIamWorkforcePoolProvider#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0feb5bd0a304da349ad8a54436cdbe11e1f1450a99878b5b01d8eeecd4cdbed)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#create GoogleIamWorkforcePoolProvider#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#delete GoogleIamWorkforcePoolProvider#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workforce_pool_provider#update GoogleIamWorkforcePoolProvider#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkforcePoolProviderTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkforcePoolProviderTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkforcePoolProvider.GoogleIamWorkforcePoolProviderTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__786c61ff768c60b23a83fba5bc60537bcf93a7129d54d301d23fcad29f35254a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3ab18a09063231319b967add0880a0ab64471bdaa01cac502265c82c7f162f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e254357771b955a30e2394b39d565d5f5a7a354008a3356a88bd99e5ac7e3d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b63e880d01f70db6f16d17d867568aaf06299f8d1a7a93d36d4690f652bfef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkforcePoolProviderTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkforcePoolProviderTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkforcePoolProviderTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe0dbba5f143dcc5e1b8fc70b9fdcae770028e163e504baaa50eae21bc2e790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleIamWorkforcePoolProvider",
    "GoogleIamWorkforcePoolProviderConfig",
    "GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client",
    "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret",
    "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference",
    "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue",
    "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference",
    "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference",
    "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters",
    "GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference",
    "GoogleIamWorkforcePoolProviderOidc",
    "GoogleIamWorkforcePoolProviderOidcClientSecret",
    "GoogleIamWorkforcePoolProviderOidcClientSecretOutputReference",
    "GoogleIamWorkforcePoolProviderOidcClientSecretValue",
    "GoogleIamWorkforcePoolProviderOidcClientSecretValueOutputReference",
    "GoogleIamWorkforcePoolProviderOidcOutputReference",
    "GoogleIamWorkforcePoolProviderOidcWebSsoConfig",
    "GoogleIamWorkforcePoolProviderOidcWebSsoConfigOutputReference",
    "GoogleIamWorkforcePoolProviderSaml",
    "GoogleIamWorkforcePoolProviderSamlOutputReference",
    "GoogleIamWorkforcePoolProviderTimeouts",
    "GoogleIamWorkforcePoolProviderTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fd955dc1b04496da86a773d0ed15b00dcca2f3cd25d1006083788a394927196e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    provider_id: builtins.str,
    workforce_pool_id: builtins.str,
    attribute_condition: typing.Optional[builtins.str] = None,
    attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    extra_attributes_oauth2_client: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    saml: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f5669dd4dd914225e63afaa85430e2d7a6592a36876aeef54adf7a297e64d7fa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7af2300067617555e0bdee5c327dc178c3939403c07c86a5fb75462f42b70b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bae040d091cf3161a863ae995490649ed9db58f7ecadef242d57b0d8a324f8c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ffcd3d30584702058ce249af860d8fe3cd4d96726002973d82ff247b7dce0eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe628da377271369ec659af7a2fd9043bc02eac65440e603565e436bd90d0f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8b82c0ab8e3ffa7da263600a154dc07dc9593d095e4d9a4a81758461e23a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adafeb2cc3de48dcf9b3f8fa2270b129e375fae52250b72d026263d5de2d4d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45eb01dc38753b2c4f3be6c79b9220e9a72618410ea99c6fdbb63261cb07078(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98ce78c3c1ff0769da788f3c55e276bf62a21286c414844030e286849868c40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553aa19d81b16963eca7cb6f4aa47369bf87f1b1be795fb45ed6107b33339ccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40246723df2937e5d6eb80758bf84fe80d137020704a3172a5be320602f4b893(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    provider_id: builtins.str,
    workforce_pool_id: builtins.str,
    attribute_condition: typing.Optional[builtins.str] = None,
    attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    extra_attributes_oauth2_client: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    saml: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bdee81b6ed8c968647fe6aed6e7b5f3db220e53adf55093b7c3069fd811695(
    *,
    attributes_type: builtins.str,
    client_id: builtins.str,
    client_secret: typing.Union[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret, typing.Dict[builtins.str, typing.Any]],
    issuer_uri: builtins.str,
    query_parameters: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a268749c3d028e23b2506e80731d41e43b142f48f2ce3afdd6b37b8734abdb1(
    *,
    value: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b2798c118b6550bcd67b5a33f33d9baf983db6999850bea7ae4e524e917b6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b29af157b9bdd8eb3edf2f27ce9157b1c7cfa691cf55e339ddb632325e5130(
    value: typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5df51a87c7f575fa05c1d221519c6d9f59a38bd60b91ecffa6f9e4b3e4fdc81(
    *,
    plain_text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde047f9bbdd9726bceb5ba5e54ed9c05ab9b3ac4e197c72c0e1908f7e01be87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682178f467349303bc3adb3130988bb8d7c7e4643f72448feb5d3d9872d0b987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e12b199e4b8f7588b886bdc58c9ad4c8d4cede605891c6b513e9a1b95e7291(
    value: typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7f7826a86864db233f4e7f25e94ce69d7cf9c0fe9ca7a36ea994b7aa2b9afa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c657fc93d0bdf1e481fd7571bbb59aad0895d2fbcf8094e1dab4c916f82d4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa68a1b558228a5d4c10cad32cdbf4dd6c305f8161c585c79df4f917d4a2ca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa1b062a82c8ffe09c5aad2a33c2cf94f9da9893785867c884fd13bb5177ca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f0adcf1514f7c0034eeb38ee844df125920a0a070a985767aa760cc7efec61(
    value: typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2Client],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1649f2574e75ae079c092c1a3ef43a49e1f44a911ac5b70cdf4cd42e5d7716d8(
    *,
    filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6dc21617bc0ee3a85e021d6b84369bcd3389a09f2673620bcb2f7f8d2929103(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a125436394b2acb3804556d0314a0ed8f22654ad1ed64c67c59da254042d67c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323f9e398a1ea0b3ff13d14fba0da17bab1ed52da15b3d4b97b8eef9bd233843(
    value: typing.Optional[GoogleIamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2eaa733147e60b682318c6347036312ae597108ac13f9922af518b83204aa6(
    *,
    client_id: builtins.str,
    issuer_uri: builtins.str,
    client_secret: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderOidcClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    jwks_json: typing.Optional[builtins.str] = None,
    web_sso_config: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderOidcWebSsoConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9dd6543f37bfe8c7392c038aa43e88fecba5ed4e8f093b61cd5564c91ea393(
    *,
    value: typing.Optional[typing.Union[GoogleIamWorkforcePoolProviderOidcClientSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53f254d001e1c425e854a04ed7645ab930fe8b6879351030df76314c11d85d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97c84946ecdbea5018a8af616caf098f6c51ee13000f9fd631871a28740656f(
    value: typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e369ac7094fe0a3a6a9c91e217553a93379c75d88801bc22c7cc2d2e1760fed2(
    *,
    plain_text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0c4f0e375ab7fd006a12722374bb54891ffaaae3fd294d6c35865f7e7b0fba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eefccbac3e176f0678507b87388da68cd4f860c12631a1b05abcfbd276dd033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4774f33f22019945336d1522ba9f993ceab8116e8b085f1faf8a4c1abd77e7e8(
    value: typing.Optional[GoogleIamWorkforcePoolProviderOidcClientSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3406116e0f7fb0d68899846e363f4c3799cd3e4cfe45afa4e6829fd8d092112a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c908224c51bff347e2791220f31300325649fa8122f2fb095c97dce550ed7a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ab77a030dde76e9cba83445f973a60246a044359a725b6b7f32abfd885bb45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faab493ce397271c85cd854dda89ae636176d8352005ded7665154bb217b1d58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ead7c73e9d8e722528729ef9a2bf7adc5867a4090a6ecd901da3ec7c5eb0ff(
    value: typing.Optional[GoogleIamWorkforcePoolProviderOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70a911a30575d21717c76b25ed9111cbf5f9461ff8469e91919c694f9802ec6(
    *,
    assertion_claims_behavior: builtins.str,
    response_type: builtins.str,
    additional_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45056b9d866acbfe2bca4546d060624ddc635b2d20f6c20b45ad3a6078123f9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf499eb1209fc9d5d08322c4b5b766c33cdc011cf333272a74b7df34c5af54e2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77275b8c56d5613314c558db10a4986760753e3084e3bfbb1885ef3fc1b6f5c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538f2fed1aa77aef00fbf7ce7a8087099df2964ea4bdae24aadf8e70b63dbec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb9a115f8180b4721cd94743a7b38c134dcbe3a985802d6b69fade755c380ae(
    value: typing.Optional[GoogleIamWorkforcePoolProviderOidcWebSsoConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3325494a4c6cf016e6aeb58edb55aa04925c84d3a344be039ec12c84d20be606(
    *,
    idp_metadata_xml: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9292733df99bb5001a597175d73d1919bec4ebd74120e96f3dc0789c8008f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39bcf503b1589030fd80d79cb7b7261193382269e3bb3335d9d76c14603bf639(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98266b606d40ae0d5141a96b4ec686e96aff4176e9990b8ac44a6775cc4cd928(
    value: typing.Optional[GoogleIamWorkforcePoolProviderSaml],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0feb5bd0a304da349ad8a54436cdbe11e1f1450a99878b5b01d8eeecd4cdbed(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786c61ff768c60b23a83fba5bc60537bcf93a7129d54d301d23fcad29f35254a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab18a09063231319b967add0880a0ab64471bdaa01cac502265c82c7f162f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e254357771b955a30e2394b39d565d5f5a7a354008a3356a88bd99e5ac7e3d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b63e880d01f70db6f16d17d867568aaf06299f8d1a7a93d36d4690f652bfef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe0dbba5f143dcc5e1b8fc70b9fdcae770028e163e504baaa50eae21bc2e790(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkforcePoolProviderTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
