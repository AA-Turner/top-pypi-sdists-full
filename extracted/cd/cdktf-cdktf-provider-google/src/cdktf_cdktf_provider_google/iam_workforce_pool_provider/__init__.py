r'''
# `google_iam_workforce_pool_provider`

Refer to the Terraform Registry for docs: [`google_iam_workforce_pool_provider`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider).
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


class IamWorkforcePoolProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider google_iam_workforce_pool_provider}.'''

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
        extra_attributes_oauth2_client: typing.Optional[typing.Union["IamWorkforcePoolProviderExtraAttributesOauth2Client", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["IamWorkforcePoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        saml: typing.Optional[typing.Union["IamWorkforcePoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["IamWorkforcePoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider google_iam_workforce_pool_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#location IamWorkforcePoolProvider#location}
        :param provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#provider_id IamWorkforcePoolProvider#provider_id}
        :param workforce_pool_id: The ID to use for the pool, which becomes the final component of the resource name. The IDs must be a globally unique string of 6 to 63 lowercase letters, digits, or hyphens. It must start with a letter, and cannot have a trailing hyphen. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#workforce_pool_id IamWorkforcePoolProvider#workforce_pool_id}
        :param attribute_condition: A `Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: - 'assertion': JSON representing the authentication credential issued by the provider. - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. 'google.profile_photo' and 'google.display_name' are not supported. - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credentials will be accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#attribute_condition IamWorkforcePoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from the authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: - 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. This is a required field and the mapped subject cannot exceed 127 bytes. - 'google.groups': Groups the authenticating user belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. - 'google.display_name': The name of the authenticated user. This is an optional field and the mapped display name cannot exceed 100 bytes. If not set, 'google.subject' will be displayed instead. This attribute cannot be referenced in IAM bindings. - 'google.profile_photo': The URL that specifies the authenticated user's thumbnail photo. This is an optional field. When set, the image will be visible as the user's profile picture. If not set, a generic user icon will be displayed instead. This attribute cannot be referenced in IAM bindings. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where {custom_attribute} is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workforce pool to Google Cloud resources. For example: - 'google.subject': 'principal://iam.googleapis.com/locations/{location}/workforcePools/{pool}/subject/{value}' - 'google.groups': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/group/{value}' - 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For OIDC providers, you must supply a custom mapping that includes the 'google.subject' attribute. For example, the following maps the sub claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} An object containing a list of '"key": value' pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#attribute_mapping IamWorkforcePoolProvider#attribute_mapping}
        :param description: A user-specified description of the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#description IamWorkforcePoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#disabled IamWorkforcePoolProvider#disabled}
        :param display_name: A user-specified display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#display_name IamWorkforcePoolProvider#display_name}
        :param extra_attributes_oauth2_client: extra_attributes_oauth2_client block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#extra_attributes_oauth2_client IamWorkforcePoolProvider#extra_attributes_oauth2_client}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#id IamWorkforcePoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#oidc IamWorkforcePoolProvider#oidc}
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#saml IamWorkforcePoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#timeouts IamWorkforcePoolProvider#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a47478adbd3ec68f1330af2d6ff9e243c88aefadc8c47839af58a905b566e88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IamWorkforcePoolProviderConfig(
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
        '''Generates CDKTF code for importing a IamWorkforcePoolProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IamWorkforcePoolProvider to import.
        :param import_from_id: The id of the existing IamWorkforcePoolProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IamWorkforcePoolProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6899dfe1ba34b9d94adeee1ca4b4bc51491f29ff2222907e4e61785e8f960fb)
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
        client_secret: typing.Union["IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret", typing.Dict[builtins.str, typing.Any]],
        issuer_uri: builtins.str,
        query_parameters: typing.Optional[typing.Union["IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param attributes_type: Represents the IdP and type of claims that should be fetched. - AZURE_AD_GROUPS_MAIL: Used to get the user's group claims from the Azure AD identity provider using configuration provided in ExtraAttributesOAuth2Client and 'mail' property of the 'microsoft.graph.group' object is used for claim mapping. See https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties for more details on 'microsoft.graph.group' properties. The attributes obtained from idntity provider are mapped to 'assertion.groups'. - AZURE_AD_GROUPS_ID: Used to get the user's group claims from the Azure AD identity provider using configuration provided in ExtraAttributesOAuth2Client and 'id' property of the 'microsoft.graph.group' object is used for claim mapping. See https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties for more details on 'microsoft.graph.group' properties. The group IDs obtained from Azure AD are present in 'assertion.groups' for OIDC providers and 'assertion.attributes.groups' for SAML providers for attribute mapping. Possible values: ["AZURE_AD_GROUPS_MAIL", "AZURE_AD_GROUPS_ID"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#attributes_type IamWorkforcePoolProvider#attributes_type}
        :param client_id: The OAuth 2.0 client ID for retrieving extra attributes from the identity provider. Required to get the Access Token using client credentials grant flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_id IamWorkforcePoolProvider#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_secret IamWorkforcePoolProvider#client_secret}
        :param issuer_uri: The OIDC identity provider's issuer URI. Must be a valid URI using the 'https' scheme. Required to get the OIDC discovery document. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#issuer_uri IamWorkforcePoolProvider#issuer_uri}
        :param query_parameters: query_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#query_parameters IamWorkforcePoolProvider#query_parameters}
        '''
        value = IamWorkforcePoolProviderExtraAttributesOauth2Client(
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
        client_secret: typing.Optional[typing.Union["IamWorkforcePoolProviderOidcClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        jwks_json: typing.Optional[builtins.str] = None,
        web_sso_config: typing.Optional[typing.Union["IamWorkforcePoolProviderOidcWebSsoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: The client ID. Must match the audience claim of the JWT issued by the identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_id IamWorkforcePoolProvider#client_id}
        :param issuer_uri: The OIDC issuer URI. Must be a valid URI using the 'https' scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#issuer_uri IamWorkforcePoolProvider#issuer_uri}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_secret IamWorkforcePoolProvider#client_secret}
        :param jwks_json: OIDC JWKs in JSON String format. For details on definition of a JWK, see https:tools.ietf.org/html/rfc7517. If not set, then we use the 'jwks_uri' from the discovery document fetched from the .well-known path for the 'issuer_uri'. Currently, RSA and EC asymmetric keys are supported. The JWK must use following format and include only the following fields:: { "keys": [ { "kty": "RSA/EC", "alg": "<algorithm>", "use": "sig", "kid": "<key-id>", "n": "", "e": "", "x": "", "y": "", "crv": "" } ] } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#jwks_json IamWorkforcePoolProvider#jwks_json}
        :param web_sso_config: web_sso_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#web_sso_config IamWorkforcePoolProvider#web_sso_config}
        '''
        value = IamWorkforcePoolProviderOidc(
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
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. The xml document should comply with `SAML 2.0 specification <https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf>`_. The max size of the acceptable xml document will be bounded to 128k characters. The metadata xml document should satisfy the following constraints: 1. Must contain an Identity Provider Entity ID. 2. Must contain at least one non-expired signing key certificate. 3. For each signing key: a) Valid from should be no more than 7 days from now. b) Valid to should be no more than 10 years in the future. 4. Up to 3 IdP signing keys are allowed in the metadata xml. When updating the provider's metadata xml, at least one non-expired signing key must overlap with the existing metadata. This requirement is skipped if there are no non-expired signing keys present in the existing metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#idp_metadata_xml IamWorkforcePoolProvider#idp_metadata_xml}
        '''
        value = IamWorkforcePoolProviderSaml(idp_metadata_xml=idp_metadata_xml)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#create IamWorkforcePoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#delete IamWorkforcePoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#update IamWorkforcePoolProvider#update}.
        '''
        value = IamWorkforcePoolProviderTimeouts(
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
    ) -> "IamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference":
        return typing.cast("IamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference", jsii.get(self, "extraAttributesOauth2Client"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oidc")
    def oidc(self) -> "IamWorkforcePoolProviderOidcOutputReference":
        return typing.cast("IamWorkforcePoolProviderOidcOutputReference", jsii.get(self, "oidc"))

    @builtins.property
    @jsii.member(jsii_name="saml")
    def saml(self) -> "IamWorkforcePoolProviderSamlOutputReference":
        return typing.cast("IamWorkforcePoolProviderSamlOutputReference", jsii.get(self, "saml"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IamWorkforcePoolProviderTimeoutsOutputReference":
        return typing.cast("IamWorkforcePoolProviderTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2Client"]:
        return typing.cast(typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2Client"], jsii.get(self, "extraAttributesOauth2ClientInput"))

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
    def oidc_input(self) -> typing.Optional["IamWorkforcePoolProviderOidc"]:
        return typing.cast(typing.Optional["IamWorkforcePoolProviderOidc"], jsii.get(self, "oidcInput"))

    @builtins.property
    @jsii.member(jsii_name="providerIdInput")
    def provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="samlInput")
    def saml_input(self) -> typing.Optional["IamWorkforcePoolProviderSaml"]:
        return typing.cast(typing.Optional["IamWorkforcePoolProviderSaml"], jsii.get(self, "samlInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamWorkforcePoolProviderTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamWorkforcePoolProviderTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d4e1b0db9ca7a173514277f73861e3dfd873c59964ee6338ad0a4906a6cebbce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__032d5f57919a0dfc9718cafb55f934de9c55c82469fb80402ecbf369459802f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a6014637e2e44c92d7b6cbc9ffbad3f777798c19b66112dc44bbcb3b7a7be6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8b6ded60fec5aaedbb912b33165d57e36531fab776a60c2e22fe9bb0d994e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__386113e0e07c0c0a537d8b22ff22d768e34c68e7b50816f571c2d60d92252c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d9c6b2ce89f1ce316a2c5ad15c5390711e96396764ca8e4d9477d74ad1476e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d72abca926c4f1ca51e47a654f1463d0e21f4cb93c7ffe12f2099650fdcc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerId")
    def provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerId"))

    @provider_id.setter
    def provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388af3eaa352f6297a8884a49ae9dfce1f413b0e9a2599cc3f14c5e1fda2b334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workforcePoolId")
    def workforce_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workforcePoolId"))

    @workforce_pool_id.setter
    def workforce_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d27e9ab4e8f7fbbbf2f10fe70a3b72cc78729aa9dfa6ea785e194ccc3eba4fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workforcePoolId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderConfig",
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
class IamWorkforcePoolProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        extra_attributes_oauth2_client: typing.Optional[typing.Union["IamWorkforcePoolProviderExtraAttributesOauth2Client", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["IamWorkforcePoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        saml: typing.Optional[typing.Union["IamWorkforcePoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["IamWorkforcePoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#location IamWorkforcePoolProvider#location}
        :param provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#provider_id IamWorkforcePoolProvider#provider_id}
        :param workforce_pool_id: The ID to use for the pool, which becomes the final component of the resource name. The IDs must be a globally unique string of 6 to 63 lowercase letters, digits, or hyphens. It must start with a letter, and cannot have a trailing hyphen. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#workforce_pool_id IamWorkforcePoolProvider#workforce_pool_id}
        :param attribute_condition: A `Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: - 'assertion': JSON representing the authentication credential issued by the provider. - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. 'google.profile_photo' and 'google.display_name' are not supported. - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credentials will be accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#attribute_condition IamWorkforcePoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from the authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: - 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. This is a required field and the mapped subject cannot exceed 127 bytes. - 'google.groups': Groups the authenticating user belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. - 'google.display_name': The name of the authenticated user. This is an optional field and the mapped display name cannot exceed 100 bytes. If not set, 'google.subject' will be displayed instead. This attribute cannot be referenced in IAM bindings. - 'google.profile_photo': The URL that specifies the authenticated user's thumbnail photo. This is an optional field. When set, the image will be visible as the user's profile picture. If not set, a generic user icon will be displayed instead. This attribute cannot be referenced in IAM bindings. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where {custom_attribute} is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workforce pool to Google Cloud resources. For example: - 'google.subject': 'principal://iam.googleapis.com/locations/{location}/workforcePools/{pool}/subject/{value}' - 'google.groups': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/group/{value}' - 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For OIDC providers, you must supply a custom mapping that includes the 'google.subject' attribute. For example, the following maps the sub claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} An object containing a list of '"key": value' pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#attribute_mapping IamWorkforcePoolProvider#attribute_mapping}
        :param description: A user-specified description of the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#description IamWorkforcePoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#disabled IamWorkforcePoolProvider#disabled}
        :param display_name: A user-specified display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#display_name IamWorkforcePoolProvider#display_name}
        :param extra_attributes_oauth2_client: extra_attributes_oauth2_client block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#extra_attributes_oauth2_client IamWorkforcePoolProvider#extra_attributes_oauth2_client}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#id IamWorkforcePoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#oidc IamWorkforcePoolProvider#oidc}
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#saml IamWorkforcePoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#timeouts IamWorkforcePoolProvider#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(extra_attributes_oauth2_client, dict):
            extra_attributes_oauth2_client = IamWorkforcePoolProviderExtraAttributesOauth2Client(**extra_attributes_oauth2_client)
        if isinstance(oidc, dict):
            oidc = IamWorkforcePoolProviderOidc(**oidc)
        if isinstance(saml, dict):
            saml = IamWorkforcePoolProviderSaml(**saml)
        if isinstance(timeouts, dict):
            timeouts = IamWorkforcePoolProviderTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f319fe9e23ad84ae4ef94ab842d5a90db41a5bf6b0d42dd96ab49e0f574fb2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#location IamWorkforcePoolProvider#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_id(self) -> builtins.str:
        '''The ID for the provider, which becomes the final component of the resource name.

        This value must be 4-32 characters, and may contain the characters [a-z0-9-].
        The prefix 'gcp-' is reserved for use by Google, and may not be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#provider_id IamWorkforcePoolProvider#provider_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#workforce_pool_id IamWorkforcePoolProvider#workforce_pool_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#attribute_condition IamWorkforcePoolProvider#attribute_condition}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#attribute_mapping IamWorkforcePoolProvider#attribute_mapping}
        '''
        result = self._values.get("attribute_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A user-specified description of the provider. Cannot exceed 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#description IamWorkforcePoolProvider#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#disabled IamWorkforcePoolProvider#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-specified display name for the provider. Cannot exceed 32 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#display_name IamWorkforcePoolProvider#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_attributes_oauth2_client(
        self,
    ) -> typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2Client"]:
        '''extra_attributes_oauth2_client block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#extra_attributes_oauth2_client IamWorkforcePoolProvider#extra_attributes_oauth2_client}
        '''
        result = self._values.get("extra_attributes_oauth2_client")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2Client"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#id IamWorkforcePoolProvider#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc(self) -> typing.Optional["IamWorkforcePoolProviderOidc"]:
        '''oidc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#oidc IamWorkforcePoolProvider#oidc}
        '''
        result = self._values.get("oidc")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderOidc"], result)

    @builtins.property
    def saml(self) -> typing.Optional["IamWorkforcePoolProviderSaml"]:
        '''saml block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#saml IamWorkforcePoolProvider#saml}
        '''
        result = self._values.get("saml")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderSaml"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IamWorkforcePoolProviderTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#timeouts IamWorkforcePoolProvider#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderExtraAttributesOauth2Client",
    jsii_struct_bases=[],
    name_mapping={
        "attributes_type": "attributesType",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "issuer_uri": "issuerUri",
        "query_parameters": "queryParameters",
    },
)
class IamWorkforcePoolProviderExtraAttributesOauth2Client:
    def __init__(
        self,
        *,
        attributes_type: builtins.str,
        client_id: builtins.str,
        client_secret: typing.Union["IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret", typing.Dict[builtins.str, typing.Any]],
        issuer_uri: builtins.str,
        query_parameters: typing.Optional[typing.Union["IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param attributes_type: Represents the IdP and type of claims that should be fetched. - AZURE_AD_GROUPS_MAIL: Used to get the user's group claims from the Azure AD identity provider using configuration provided in ExtraAttributesOAuth2Client and 'mail' property of the 'microsoft.graph.group' object is used for claim mapping. See https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties for more details on 'microsoft.graph.group' properties. The attributes obtained from idntity provider are mapped to 'assertion.groups'. - AZURE_AD_GROUPS_ID: Used to get the user's group claims from the Azure AD identity provider using configuration provided in ExtraAttributesOAuth2Client and 'id' property of the 'microsoft.graph.group' object is used for claim mapping. See https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0#properties for more details on 'microsoft.graph.group' properties. The group IDs obtained from Azure AD are present in 'assertion.groups' for OIDC providers and 'assertion.attributes.groups' for SAML providers for attribute mapping. Possible values: ["AZURE_AD_GROUPS_MAIL", "AZURE_AD_GROUPS_ID"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#attributes_type IamWorkforcePoolProvider#attributes_type}
        :param client_id: The OAuth 2.0 client ID for retrieving extra attributes from the identity provider. Required to get the Access Token using client credentials grant flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_id IamWorkforcePoolProvider#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_secret IamWorkforcePoolProvider#client_secret}
        :param issuer_uri: The OIDC identity provider's issuer URI. Must be a valid URI using the 'https' scheme. Required to get the OIDC discovery document. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#issuer_uri IamWorkforcePoolProvider#issuer_uri}
        :param query_parameters: query_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#query_parameters IamWorkforcePoolProvider#query_parameters}
        '''
        if isinstance(client_secret, dict):
            client_secret = IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret(**client_secret)
        if isinstance(query_parameters, dict):
            query_parameters = IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters(**query_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c93fa178322e7f85812986b14768434eb9a725d018ec3c8504e5b4598ec5cec5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#attributes_type IamWorkforcePoolProvider#attributes_type}
        '''
        result = self._values.get("attributes_type")
        assert result is not None, "Required property 'attributes_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OAuth 2.0 client ID for retrieving extra attributes from the identity provider. Required to get the Access Token using client credentials grant flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_id IamWorkforcePoolProvider#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(
        self,
    ) -> "IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret":
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_secret IamWorkforcePoolProvider#client_secret}
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast("IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret", result)

    @builtins.property
    def issuer_uri(self) -> builtins.str:
        '''The OIDC identity provider's issuer URI.

        Must be a valid URI using the 'https' scheme. Required to get the OIDC discovery document.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#issuer_uri IamWorkforcePoolProvider#issuer_uri}
        '''
        result = self._values.get("issuer_uri")
        assert result is not None, "Required property 'issuer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_parameters(
        self,
    ) -> typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters"]:
        '''query_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#query_parameters IamWorkforcePoolProvider#query_parameters}
        '''
        result = self._values.get("query_parameters")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderExtraAttributesOauth2Client(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret:
    def __init__(
        self,
        *,
        value: typing.Optional[typing.Union["IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#value IamWorkforcePoolProvider#value}
        '''
        if isinstance(value, dict):
            value = IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbcb29c2cdc15a250c2503daeba7f2578c1ae58cb79d6668a744430123caed71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#value IamWorkforcePoolProvider#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8ffb063d1340a48965d1e016c048f3dcef80116dab615096e8cb34c96a9244b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putValue")
    def put_value(self, *, plain_text: builtins.str) -> None:
        '''
        :param plain_text: The plain text of the client secret value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#plain_text IamWorkforcePoolProvider#plain_text}
        '''
        value = IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue(
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
    ) -> "IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference":
        return typing.cast("IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue"]:
        return typing.cast(typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d70249e511596ad2bee1d0c3b8ea59e1438ab07b24ad2362ed5d5906dd58777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue",
    jsii_struct_bases=[],
    name_mapping={"plain_text": "plainText"},
)
class IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue:
    def __init__(self, *, plain_text: builtins.str) -> None:
        '''
        :param plain_text: The plain text of the client secret value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#plain_text IamWorkforcePoolProvider#plain_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc24744da2f44f30a980947b715de76630793e81445f734f05e839c382c2200f)
            check_type(argname="argument plain_text", value=plain_text, expected_type=type_hints["plain_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plain_text": plain_text,
        }

    @builtins.property
    def plain_text(self) -> builtins.str:
        '''The plain text of the client secret value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#plain_text IamWorkforcePoolProvider#plain_text}
        '''
        result = self._values.get("plain_text")
        assert result is not None, "Required property 'plain_text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__204b5d1da889b729c09b565a47754b8729ed144e1781ed4b6f14c76e165b4c60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3326dcdf7cbcc576a876079c651773f3eaafb4e45db9baf5176c7aa0c5e5a52f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plainText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50298e0f837148caffcf9abdc084f04c9d5b204cf1cf2a083c60e76b121f2b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea988aa3e9573338b53ad0fbd6bddfbffbc8aeaf3fdd178a550a57896f7590f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(
        self,
        *,
        value: typing.Optional[typing.Union[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#value IamWorkforcePoolProvider#value}
        '''
        value_ = IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret(
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
        :param filter: The filter used to request specific records from IdP. In case of attributes type as AZURE_AD_GROUPS_MAIL and AZURE_AD_GROUPS_ID, it represents the filter used to request specific groups for users from IdP. By default, all of the groups associated with the user are fetched. The groups should be security enabled. See https://learn.microsoft.com/en-us/graph/search-query-parameter for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#filter IamWorkforcePoolProvider#filter}
        '''
        value = IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters(
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
    ) -> IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference:
        return typing.cast(IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="queryParameters")
    def query_parameters(
        self,
    ) -> "IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference":
        return typing.cast("IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference", jsii.get(self, "queryParameters"))

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
    ) -> typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUriInput")
    def issuer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParametersInput")
    def query_parameters_input(
        self,
    ) -> typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters"]:
        return typing.cast(typing.Optional["IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters"], jsii.get(self, "queryParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesType")
    def attributes_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributesType"))

    @attributes_type.setter
    def attributes_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2817b942359bb776d1d22606ee064d4bf79e2f523720ca1bc06173904810b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributesType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275050d04ec0e66f63dbad3f7d676b8e2bdbd593c10fa27f4097ef61cb6b1baf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8508206ba8c3695f18e0ace9ecdfe1228e6247ed84e32f085d889de1ccd35d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2Client]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2Client], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2Client],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca90ba4d43b14c4e97e1214c68c69fdea36a147da302a84050722191398ed41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters:
    def __init__(self, *, filter: typing.Optional[builtins.str] = None) -> None:
        '''
        :param filter: The filter used to request specific records from IdP. In case of attributes type as AZURE_AD_GROUPS_MAIL and AZURE_AD_GROUPS_ID, it represents the filter used to request specific groups for users from IdP. By default, all of the groups associated with the user are fetched. The groups should be security enabled. See https://learn.microsoft.com/en-us/graph/search-query-parameter for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#filter IamWorkforcePoolProvider#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4442ce30c8698e05d3a39225908c5cd0025ed585ad81a9f53cb31035f91d41f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#filter IamWorkforcePoolProvider#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37235d8eda9c21d5aed1c1ab2511357851b8cc420ec4fabff6a66e1f5bbbbd50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ab27db3ae8bc0534ba3ffbb0889526b1df9158be1d7e45aad0b27234f9b850b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b10038db5a0110fc54b3519939f8e12d6522d471a21edf72946b9623dc1ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidc",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "issuer_uri": "issuerUri",
        "client_secret": "clientSecret",
        "jwks_json": "jwksJson",
        "web_sso_config": "webSsoConfig",
    },
)
class IamWorkforcePoolProviderOidc:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        issuer_uri: builtins.str,
        client_secret: typing.Optional[typing.Union["IamWorkforcePoolProviderOidcClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        jwks_json: typing.Optional[builtins.str] = None,
        web_sso_config: typing.Optional[typing.Union["IamWorkforcePoolProviderOidcWebSsoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: The client ID. Must match the audience claim of the JWT issued by the identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_id IamWorkforcePoolProvider#client_id}
        :param issuer_uri: The OIDC issuer URI. Must be a valid URI using the 'https' scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#issuer_uri IamWorkforcePoolProvider#issuer_uri}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_secret IamWorkforcePoolProvider#client_secret}
        :param jwks_json: OIDC JWKs in JSON String format. For details on definition of a JWK, see https:tools.ietf.org/html/rfc7517. If not set, then we use the 'jwks_uri' from the discovery document fetched from the .well-known path for the 'issuer_uri'. Currently, RSA and EC asymmetric keys are supported. The JWK must use following format and include only the following fields:: { "keys": [ { "kty": "RSA/EC", "alg": "<algorithm>", "use": "sig", "kid": "<key-id>", "n": "", "e": "", "x": "", "y": "", "crv": "" } ] } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#jwks_json IamWorkforcePoolProvider#jwks_json}
        :param web_sso_config: web_sso_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#web_sso_config IamWorkforcePoolProvider#web_sso_config}
        '''
        if isinstance(client_secret, dict):
            client_secret = IamWorkforcePoolProviderOidcClientSecret(**client_secret)
        if isinstance(web_sso_config, dict):
            web_sso_config = IamWorkforcePoolProviderOidcWebSsoConfig(**web_sso_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b57aaa92d517f373514b558e9cc6f1654c111ed189ba3e7dab7de33a273b8d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_id IamWorkforcePoolProvider#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer_uri(self) -> builtins.str:
        '''The OIDC issuer URI. Must be a valid URI using the 'https' scheme.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#issuer_uri IamWorkforcePoolProvider#issuer_uri}
        '''
        result = self._values.get("issuer_uri")
        assert result is not None, "Required property 'issuer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(
        self,
    ) -> typing.Optional["IamWorkforcePoolProviderOidcClientSecret"]:
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#client_secret IamWorkforcePoolProvider#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderOidcClientSecret"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#jwks_json IamWorkforcePoolProvider#jwks_json}
        '''
        result = self._values.get("jwks_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_sso_config(
        self,
    ) -> typing.Optional["IamWorkforcePoolProviderOidcWebSsoConfig"]:
        '''web_sso_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#web_sso_config IamWorkforcePoolProvider#web_sso_config}
        '''
        result = self._values.get("web_sso_config")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderOidcWebSsoConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidcClientSecret",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class IamWorkforcePoolProviderOidcClientSecret:
    def __init__(
        self,
        *,
        value: typing.Optional[typing.Union["IamWorkforcePoolProviderOidcClientSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#value IamWorkforcePoolProvider#value}
        '''
        if isinstance(value, dict):
            value = IamWorkforcePoolProviderOidcClientSecretValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cee2fb88ccaedaa1f7262f8a62f7f5d2f67ce8d3c94baea6aa2683ba176191a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional["IamWorkforcePoolProviderOidcClientSecretValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#value IamWorkforcePoolProvider#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderOidcClientSecretValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderOidcClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderOidcClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidcClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd04ded514dc0fdac474b6fba0f24004b9b48920bec820dd0834efeac2517fc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putValue")
    def put_value(self, *, plain_text: builtins.str) -> None:
        '''
        :param plain_text: The plain text of the client secret value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#plain_text IamWorkforcePoolProvider#plain_text}
        '''
        value = IamWorkforcePoolProviderOidcClientSecretValue(plain_text=plain_text)

        return typing.cast(None, jsii.invoke(self, "putValue", [value]))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> "IamWorkforcePoolProviderOidcClientSecretValueOutputReference":
        return typing.cast("IamWorkforcePoolProviderOidcClientSecretValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["IamWorkforcePoolProviderOidcClientSecretValue"]:
        return typing.cast(typing.Optional["IamWorkforcePoolProviderOidcClientSecretValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IamWorkforcePoolProviderOidcClientSecret]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderOidcClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderOidcClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f8dbbbf07abe4313e6e9b6d69b6cce8dbd1b9fafc36ad9fddb10703fd02ada6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidcClientSecretValue",
    jsii_struct_bases=[],
    name_mapping={"plain_text": "plainText"},
)
class IamWorkforcePoolProviderOidcClientSecretValue:
    def __init__(self, *, plain_text: builtins.str) -> None:
        '''
        :param plain_text: The plain text of the client secret value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#plain_text IamWorkforcePoolProvider#plain_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736be669988d4bdc5058b512a88e8508c27889393d353c046b395addd85eba3c)
            check_type(argname="argument plain_text", value=plain_text, expected_type=type_hints["plain_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plain_text": plain_text,
        }

    @builtins.property
    def plain_text(self) -> builtins.str:
        '''The plain text of the client secret value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#plain_text IamWorkforcePoolProvider#plain_text}
        '''
        result = self._values.get("plain_text")
        assert result is not None, "Required property 'plain_text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderOidcClientSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderOidcClientSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidcClientSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51e32a873e319be95ec9d6bf23369f2c3f5bf62d30d4511e4a12ae4d09aa0097)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57a2c6e6a40ab407660f70bf230c0be750e4c039d8189c07e2cc8be59edd7591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plainText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IamWorkforcePoolProviderOidcClientSecretValue]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderOidcClientSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderOidcClientSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b09e3d9174639490aa3d12f1fe5807e1e0c940cc2a500e0be74e1e7062e518b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IamWorkforcePoolProviderOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b42d3b7aeea5ee572f6030330e1f1b5cf62fb08283c8a9f700ba570d3e8690e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(
        self,
        *,
        value: typing.Optional[typing.Union[IamWorkforcePoolProviderOidcClientSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#value IamWorkforcePoolProvider#value}
        '''
        value_ = IamWorkforcePoolProviderOidcClientSecret(value=value)

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
        :param assertion_claims_behavior: The behavior for how OIDC Claims are included in the 'assertion' object used for attribute mapping and attribute condition. - MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS: Merge the UserInfo Endpoint Claims with ID Token Claims, preferring UserInfo Claim Values for the same Claim Name. This option is available only for the Authorization Code Flow. - ONLY_ID_TOKEN_CLAIMS: Only include ID Token Claims. Possible values: ["MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS", "ONLY_ID_TOKEN_CLAIMS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#assertion_claims_behavior IamWorkforcePoolProvider#assertion_claims_behavior}
        :param response_type: The Response Type to request for in the OIDC Authorization Request for web sign-in. The 'CODE' Response Type is recommended to avoid the Implicit Flow, for security reasons. - CODE: The 'response_type=code' selection uses the Authorization Code Flow for web sign-in. Requires a configured client secret. - ID_TOKEN: The 'response_type=id_token' selection uses the Implicit Flow for web sign-in. Possible values: ["CODE", "ID_TOKEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#response_type IamWorkforcePoolProvider#response_type}
        :param additional_scopes: Additional scopes to request for in the OIDC authentication request on top of scopes requested by default. By default, the 'openid', 'profile' and 'email' scopes that are supported by the identity provider are requested. Each additional scope may be at most 256 characters. A maximum of 10 additional scopes may be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#additional_scopes IamWorkforcePoolProvider#additional_scopes}
        '''
        value = IamWorkforcePoolProviderOidcWebSsoConfig(
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
    def client_secret(self) -> IamWorkforcePoolProviderOidcClientSecretOutputReference:
        return typing.cast(IamWorkforcePoolProviderOidcClientSecretOutputReference, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="webSsoConfig")
    def web_sso_config(
        self,
    ) -> "IamWorkforcePoolProviderOidcWebSsoConfigOutputReference":
        return typing.cast("IamWorkforcePoolProviderOidcWebSsoConfigOutputReference", jsii.get(self, "webSsoConfig"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(
        self,
    ) -> typing.Optional[IamWorkforcePoolProviderOidcClientSecret]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderOidcClientSecret], jsii.get(self, "clientSecretInput"))

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
    ) -> typing.Optional["IamWorkforcePoolProviderOidcWebSsoConfig"]:
        return typing.cast(typing.Optional["IamWorkforcePoolProviderOidcWebSsoConfig"], jsii.get(self, "webSsoConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb2f7a9636131c9602f6edcefb4503f80cc41c3770aea14294b34a71e5683cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b8eb23291f94e3d0869295e320512d58f2bbcee379c85fb251420eea5139cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwksJson")
    def jwks_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwksJson"))

    @jwks_json.setter
    def jwks_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2dde012d297e525b117b11412cd9bcda976c50503a7e99f1d6173f5be6c9fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwksJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamWorkforcePoolProviderOidc]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderOidc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c991c2e18daaa9dc1507ebc0880ee0507856a86918241dd36c3d4048a6e9f853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidcWebSsoConfig",
    jsii_struct_bases=[],
    name_mapping={
        "assertion_claims_behavior": "assertionClaimsBehavior",
        "response_type": "responseType",
        "additional_scopes": "additionalScopes",
    },
)
class IamWorkforcePoolProviderOidcWebSsoConfig:
    def __init__(
        self,
        *,
        assertion_claims_behavior: builtins.str,
        response_type: builtins.str,
        additional_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param assertion_claims_behavior: The behavior for how OIDC Claims are included in the 'assertion' object used for attribute mapping and attribute condition. - MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS: Merge the UserInfo Endpoint Claims with ID Token Claims, preferring UserInfo Claim Values for the same Claim Name. This option is available only for the Authorization Code Flow. - ONLY_ID_TOKEN_CLAIMS: Only include ID Token Claims. Possible values: ["MERGE_USER_INFO_OVER_ID_TOKEN_CLAIMS", "ONLY_ID_TOKEN_CLAIMS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#assertion_claims_behavior IamWorkforcePoolProvider#assertion_claims_behavior}
        :param response_type: The Response Type to request for in the OIDC Authorization Request for web sign-in. The 'CODE' Response Type is recommended to avoid the Implicit Flow, for security reasons. - CODE: The 'response_type=code' selection uses the Authorization Code Flow for web sign-in. Requires a configured client secret. - ID_TOKEN: The 'response_type=id_token' selection uses the Implicit Flow for web sign-in. Possible values: ["CODE", "ID_TOKEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#response_type IamWorkforcePoolProvider#response_type}
        :param additional_scopes: Additional scopes to request for in the OIDC authentication request on top of scopes requested by default. By default, the 'openid', 'profile' and 'email' scopes that are supported by the identity provider are requested. Each additional scope may be at most 256 characters. A maximum of 10 additional scopes may be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#additional_scopes IamWorkforcePoolProvider#additional_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a6cc56e59db8de28e1f2a5e6ca4df7d71beab2bb0d9cf3efe858222b402433)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#assertion_claims_behavior IamWorkforcePoolProvider#assertion_claims_behavior}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#response_type IamWorkforcePoolProvider#response_type}
        '''
        result = self._values.get("response_type")
        assert result is not None, "Required property 'response_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional scopes to request for in the OIDC authentication request on top of scopes requested by default.

        By default, the 'openid', 'profile' and 'email' scopes that are supported by the identity provider are requested.
        Each additional scope may be at most 256 characters. A maximum of 10 additional scopes may be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#additional_scopes IamWorkforcePoolProvider#additional_scopes}
        '''
        result = self._values.get("additional_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderOidcWebSsoConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderOidcWebSsoConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidcWebSsoConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c4fd4b5c66c570e42577b66529b6ca724889c8fa213d3590faa86b9ccc23da8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90b64539e0844a1bbb77d0e63aaf465da82d92dc0eb6f66d4bb624628f26af0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assertionClaimsBehavior")
    def assertion_claims_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assertionClaimsBehavior"))

    @assertion_claims_behavior.setter
    def assertion_claims_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a33e62e9712a896df3c4beb7abfa4c2780af50d41ed964f41a328a67bbac9d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assertionClaimsBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseType")
    def response_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseType"))

    @response_type.setter
    def response_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e082db2578cdcd879231da8c624d99cdc16bb1cf49cc47c0c4f2c3fe5bcdbf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IamWorkforcePoolProviderOidcWebSsoConfig]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderOidcWebSsoConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderOidcWebSsoConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71df41946348a9c05294e44382ca9842dc8e13bbf45b4325025c9139176c6ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderSaml",
    jsii_struct_bases=[],
    name_mapping={"idp_metadata_xml": "idpMetadataXml"},
)
class IamWorkforcePoolProviderSaml:
    def __init__(self, *, idp_metadata_xml: builtins.str) -> None:
        '''
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. The xml document should comply with `SAML 2.0 specification <https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf>`_. The max size of the acceptable xml document will be bounded to 128k characters. The metadata xml document should satisfy the following constraints: 1. Must contain an Identity Provider Entity ID. 2. Must contain at least one non-expired signing key certificate. 3. For each signing key: a) Valid from should be no more than 7 days from now. b) Valid to should be no more than 10 years in the future. 4. Up to 3 IdP signing keys are allowed in the metadata xml. When updating the provider's metadata xml, at least one non-expired signing key must overlap with the existing metadata. This requirement is skipped if there are no non-expired signing keys present in the existing metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#idp_metadata_xml IamWorkforcePoolProvider#idp_metadata_xml}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e519f57d11a4b738970c9ad61882e8e98eda02415eff90e33ef126224f0fbc03)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#idp_metadata_xml IamWorkforcePoolProvider#idp_metadata_xml}
        '''
        result = self._values.get("idp_metadata_xml")
        assert result is not None, "Required property 'idp_metadata_xml' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderSaml(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderSamlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderSamlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7539fa8677369208017df4ee32617076ab14d63f1a94112b870c85b746b9667e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__682d1793fc37e9d105e567cf00e866d526e59a47edb95f1f76d87f9d95d0024b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpMetadataXml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamWorkforcePoolProviderSaml]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderSaml], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderSaml],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5b4f74df985063879999e1db387d034115cbe0cf7e0c9dd46e58cd1c41fa4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IamWorkforcePoolProviderTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#create IamWorkforcePoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#delete IamWorkforcePoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#update IamWorkforcePoolProvider#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ed77d8e497aa0090daaeaaa1378646a510614ac6d6fdd4362c17821bb1e520)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#create IamWorkforcePoolProvider#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#delete IamWorkforcePoolProvider#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workforce_pool_provider#update IamWorkforcePoolProvider#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed20058fa6d8611ae68b3eec817a674e1ab095e83d87345f8dac066e8a6ce14f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e866f1d559c40b98a0344726da1871af6395716a180a333cc191b0e51f03698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25f4a6410396b49bf9b66778c0be592eefe71d92c73f6225207cb64a31c0bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c181453d31a5f272ea17b3b08bec20a68f76651cc143eb627abcb3e650d3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkforcePoolProviderTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkforcePoolProviderTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkforcePoolProviderTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6522b6ce950dc2403c9c5c75f226a0a547af862cdfe02d026a7d443d3c7b97e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IamWorkforcePoolProvider",
    "IamWorkforcePoolProviderConfig",
    "IamWorkforcePoolProviderExtraAttributesOauth2Client",
    "IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret",
    "IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretOutputReference",
    "IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue",
    "IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValueOutputReference",
    "IamWorkforcePoolProviderExtraAttributesOauth2ClientOutputReference",
    "IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters",
    "IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParametersOutputReference",
    "IamWorkforcePoolProviderOidc",
    "IamWorkforcePoolProviderOidcClientSecret",
    "IamWorkforcePoolProviderOidcClientSecretOutputReference",
    "IamWorkforcePoolProviderOidcClientSecretValue",
    "IamWorkforcePoolProviderOidcClientSecretValueOutputReference",
    "IamWorkforcePoolProviderOidcOutputReference",
    "IamWorkforcePoolProviderOidcWebSsoConfig",
    "IamWorkforcePoolProviderOidcWebSsoConfigOutputReference",
    "IamWorkforcePoolProviderSaml",
    "IamWorkforcePoolProviderSamlOutputReference",
    "IamWorkforcePoolProviderTimeouts",
    "IamWorkforcePoolProviderTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9a47478adbd3ec68f1330af2d6ff9e243c88aefadc8c47839af58a905b566e88(
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
    extra_attributes_oauth2_client: typing.Optional[typing.Union[IamWorkforcePoolProviderExtraAttributesOauth2Client, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[IamWorkforcePoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    saml: typing.Optional[typing.Union[IamWorkforcePoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[IamWorkforcePoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b6899dfe1ba34b9d94adeee1ca4b4bc51491f29ff2222907e4e61785e8f960fb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e1b0db9ca7a173514277f73861e3dfd873c59964ee6338ad0a4906a6cebbce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032d5f57919a0dfc9718cafb55f934de9c55c82469fb80402ecbf369459802f2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a6014637e2e44c92d7b6cbc9ffbad3f777798c19b66112dc44bbcb3b7a7be6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b6ded60fec5aaedbb912b33165d57e36531fab776a60c2e22fe9bb0d994e72(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386113e0e07c0c0a537d8b22ff22d768e34c68e7b50816f571c2d60d92252c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d9c6b2ce89f1ce316a2c5ad15c5390711e96396764ca8e4d9477d74ad1476e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d72abca926c4f1ca51e47a654f1463d0e21f4cb93c7ffe12f2099650fdcc8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388af3eaa352f6297a8884a49ae9dfce1f413b0e9a2599cc3f14c5e1fda2b334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d27e9ab4e8f7fbbbf2f10fe70a3b72cc78729aa9dfa6ea785e194ccc3eba4fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f319fe9e23ad84ae4ef94ab842d5a90db41a5bf6b0d42dd96ab49e0f574fb2(
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
    extra_attributes_oauth2_client: typing.Optional[typing.Union[IamWorkforcePoolProviderExtraAttributesOauth2Client, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[IamWorkforcePoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    saml: typing.Optional[typing.Union[IamWorkforcePoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[IamWorkforcePoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93fa178322e7f85812986b14768434eb9a725d018ec3c8504e5b4598ec5cec5(
    *,
    attributes_type: builtins.str,
    client_id: builtins.str,
    client_secret: typing.Union[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret, typing.Dict[builtins.str, typing.Any]],
    issuer_uri: builtins.str,
    query_parameters: typing.Optional[typing.Union[IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbcb29c2cdc15a250c2503daeba7f2578c1ae58cb79d6668a744430123caed71(
    *,
    value: typing.Optional[typing.Union[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ffb063d1340a48965d1e016c048f3dcef80116dab615096e8cb34c96a9244b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d70249e511596ad2bee1d0c3b8ea59e1438ab07b24ad2362ed5d5906dd58777(
    value: typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc24744da2f44f30a980947b715de76630793e81445f734f05e839c382c2200f(
    *,
    plain_text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204b5d1da889b729c09b565a47754b8729ed144e1781ed4b6f14c76e165b4c60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3326dcdf7cbcc576a876079c651773f3eaafb4e45db9baf5176c7aa0c5e5a52f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50298e0f837148caffcf9abdc084f04c9d5b204cf1cf2a083c60e76b121f2b0(
    value: typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientClientSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea988aa3e9573338b53ad0fbd6bddfbffbc8aeaf3fdd178a550a57896f7590f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2817b942359bb776d1d22606ee064d4bf79e2f523720ca1bc06173904810b33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275050d04ec0e66f63dbad3f7d676b8e2bdbd593c10fa27f4097ef61cb6b1baf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8508206ba8c3695f18e0ace9ecdfe1228e6247ed84e32f085d889de1ccd35d69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca90ba4d43b14c4e97e1214c68c69fdea36a147da302a84050722191398ed41d(
    value: typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2Client],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4442ce30c8698e05d3a39225908c5cd0025ed585ad81a9f53cb31035f91d41f(
    *,
    filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37235d8eda9c21d5aed1c1ab2511357851b8cc420ec4fabff6a66e1f5bbbbd50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab27db3ae8bc0534ba3ffbb0889526b1df9158be1d7e45aad0b27234f9b850b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b10038db5a0110fc54b3519939f8e12d6522d471a21edf72946b9623dc1ec9(
    value: typing.Optional[IamWorkforcePoolProviderExtraAttributesOauth2ClientQueryParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b57aaa92d517f373514b558e9cc6f1654c111ed189ba3e7dab7de33a273b8d(
    *,
    client_id: builtins.str,
    issuer_uri: builtins.str,
    client_secret: typing.Optional[typing.Union[IamWorkforcePoolProviderOidcClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    jwks_json: typing.Optional[builtins.str] = None,
    web_sso_config: typing.Optional[typing.Union[IamWorkforcePoolProviderOidcWebSsoConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cee2fb88ccaedaa1f7262f8a62f7f5d2f67ce8d3c94baea6aa2683ba176191a(
    *,
    value: typing.Optional[typing.Union[IamWorkforcePoolProviderOidcClientSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd04ded514dc0fdac474b6fba0f24004b9b48920bec820dd0834efeac2517fc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8dbbbf07abe4313e6e9b6d69b6cce8dbd1b9fafc36ad9fddb10703fd02ada6(
    value: typing.Optional[IamWorkforcePoolProviderOidcClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736be669988d4bdc5058b512a88e8508c27889393d353c046b395addd85eba3c(
    *,
    plain_text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e32a873e319be95ec9d6bf23369f2c3f5bf62d30d4511e4a12ae4d09aa0097(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a2c6e6a40ab407660f70bf230c0be750e4c039d8189c07e2cc8be59edd7591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b09e3d9174639490aa3d12f1fe5807e1e0c940cc2a500e0be74e1e7062e518b(
    value: typing.Optional[IamWorkforcePoolProviderOidcClientSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b42d3b7aeea5ee572f6030330e1f1b5cf62fb08283c8a9f700ba570d3e8690e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb2f7a9636131c9602f6edcefb4503f80cc41c3770aea14294b34a71e5683cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b8eb23291f94e3d0869295e320512d58f2bbcee379c85fb251420eea5139cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2dde012d297e525b117b11412cd9bcda976c50503a7e99f1d6173f5be6c9fbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c991c2e18daaa9dc1507ebc0880ee0507856a86918241dd36c3d4048a6e9f853(
    value: typing.Optional[IamWorkforcePoolProviderOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a6cc56e59db8de28e1f2a5e6ca4df7d71beab2bb0d9cf3efe858222b402433(
    *,
    assertion_claims_behavior: builtins.str,
    response_type: builtins.str,
    additional_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4fd4b5c66c570e42577b66529b6ca724889c8fa213d3590faa86b9ccc23da8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b64539e0844a1bbb77d0e63aaf465da82d92dc0eb6f66d4bb624628f26af0d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33e62e9712a896df3c4beb7abfa4c2780af50d41ed964f41a328a67bbac9d2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e082db2578cdcd879231da8c624d99cdc16bb1cf49cc47c0c4f2c3fe5bcdbf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71df41946348a9c05294e44382ca9842dc8e13bbf45b4325025c9139176c6ab0(
    value: typing.Optional[IamWorkforcePoolProviderOidcWebSsoConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e519f57d11a4b738970c9ad61882e8e98eda02415eff90e33ef126224f0fbc03(
    *,
    idp_metadata_xml: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7539fa8677369208017df4ee32617076ab14d63f1a94112b870c85b746b9667e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682d1793fc37e9d105e567cf00e866d526e59a47edb95f1f76d87f9d95d0024b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5b4f74df985063879999e1db387d034115cbe0cf7e0c9dd46e58cd1c41fa4d(
    value: typing.Optional[IamWorkforcePoolProviderSaml],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ed77d8e497aa0090daaeaaa1378646a510614ac6d6fdd4362c17821bb1e520(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed20058fa6d8611ae68b3eec817a674e1ab095e83d87345f8dac066e8a6ce14f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e866f1d559c40b98a0344726da1871af6395716a180a333cc191b0e51f03698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25f4a6410396b49bf9b66778c0be592eefe71d92c73f6225207cb64a31c0bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c181453d31a5f272ea17b3b08bec20a68f76651cc143eb627abcb3e650d3ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6522b6ce950dc2403c9c5c75f226a0a547af862cdfe02d026a7d443d3c7b97e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkforcePoolProviderTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
