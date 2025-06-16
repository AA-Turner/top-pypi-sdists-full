r'''
# `google_iam_workload_identity_pool_provider`

Refer to the Terraform Registry for docs: [`google_iam_workload_identity_pool_provider`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider).
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


class GoogleIamWorkloadIdentityPoolProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider google_iam_workload_identity_pool_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        workload_identity_pool_id: builtins.str,
        workload_identity_pool_provider_id: builtins.str,
        attribute_condition: typing.Optional[builtins.str] = None,
        attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        aws: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolProviderAws", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        saml: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        x509: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolProviderX509", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider google_iam_workload_identity_pool_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param workload_identity_pool_id: The ID used for the pool, which is the final component of the pool resource name. This value should be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#workload_identity_pool_id GoogleIamWorkloadIdentityPoolProvider#workload_identity_pool_id}
        :param workload_identity_pool_provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#workload_identity_pool_provider_id GoogleIamWorkloadIdentityPoolProvider#workload_identity_pool_provider_id}
        :param attribute_condition: `A Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: - 'assertion': JSON representing the authentication credential issued by the provider. - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credential are accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#attribute_condition GoogleIamWorkloadIdentityPoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: - 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. Cannot exceed 127 characters. - 'google.groups': Groups the external identity belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where '{custom_attribute}' is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workload to Google Cloud resources. For example: - 'google.subject': 'principal://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/subject/{value}' - 'google.groups': 'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/group/{value}' - 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For AWS providers, the following rules apply: - If no attribute mapping is defined, the following default mapping applies:: { "google.subject":"assertion.arn", "attribute.aws_role": "assertion.arn.contains('assumed-role')" " ? assertion.arn.extract('{account_arn}assumed-role/')" " + 'assumed-role/'" " + assertion.arn.extract('assumed-role/{role_name}/')" " : assertion.arn", } - If any custom attribute mappings are defined, they must include a mapping to the 'google.subject' attribute. For OIDC providers, the following rules apply: - Custom attribute mappings must be defined, and must include a mapping to the 'google.subject' attribute. For example, the following maps the 'sub' claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#attribute_mapping GoogleIamWorkloadIdentityPoolProvider#attribute_mapping}
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#aws GoogleIamWorkloadIdentityPoolProvider#aws}
        :param description: A description for the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#description GoogleIamWorkloadIdentityPoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#disabled GoogleIamWorkloadIdentityPoolProvider#disabled}
        :param display_name: A display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#display_name GoogleIamWorkloadIdentityPoolProvider#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#id GoogleIamWorkloadIdentityPoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#oidc GoogleIamWorkloadIdentityPoolProvider#oidc}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#project GoogleIamWorkloadIdentityPoolProvider#project}.
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#saml GoogleIamWorkloadIdentityPoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#timeouts GoogleIamWorkloadIdentityPoolProvider#timeouts}
        :param x509: x509 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#x509 GoogleIamWorkloadIdentityPoolProvider#x509}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fe01d243fcdbdc314942b687214c438ce8f21ccdaa8c6d3e439540629d6ca4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIamWorkloadIdentityPoolProviderConfig(
            workload_identity_pool_id=workload_identity_pool_id,
            workload_identity_pool_provider_id=workload_identity_pool_provider_id,
            attribute_condition=attribute_condition,
            attribute_mapping=attribute_mapping,
            aws=aws,
            description=description,
            disabled=disabled,
            display_name=display_name,
            id=id,
            oidc=oidc,
            project=project,
            saml=saml,
            timeouts=timeouts,
            x509=x509,
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
        '''Generates CDKTF code for importing a GoogleIamWorkloadIdentityPoolProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleIamWorkloadIdentityPoolProvider to import.
        :param import_from_id: The id of the existing GoogleIamWorkloadIdentityPoolProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleIamWorkloadIdentityPoolProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00356f08092ffc07223a332edd74dfab63a450384dd66dfaa241254312bb7a5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAws")
    def put_aws(self, *, account_id: builtins.str) -> None:
        '''
        :param account_id: The AWS account ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#account_id GoogleIamWorkloadIdentityPoolProvider#account_id}
        '''
        value = GoogleIamWorkloadIdentityPoolProviderAws(account_id=account_id)

        return typing.cast(None, jsii.invoke(self, "putAws", [value]))

    @jsii.member(jsii_name="putOidc")
    def put_oidc(
        self,
        *,
        issuer_uri: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        jwks_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param issuer_uri: The OIDC issuer URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#issuer_uri GoogleIamWorkloadIdentityPoolProvider#issuer_uri}
        :param allowed_audiences: Acceptable values for the 'aud' field (audience) in the OIDC token. Token exchange requests are rejected if the token audience does not match one of the configured values. Each audience may be at most 256 characters. A maximum of 10 audiences may be configured. If this list is empty, the OIDC token audience must be equal to the full canonical resource name of the WorkloadIdentityPoolProvider, with or without the HTTPS prefix. For example:: //iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id> https://iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#allowed_audiences GoogleIamWorkloadIdentityPoolProvider#allowed_audiences}
        :param jwks_json: OIDC JWKs in JSON String format. For details on definition of a JWK, see https:tools.ietf.org/html/rfc7517. If not set, then we use the 'jwks_uri' from the discovery document fetched from the .well-known path for the 'issuer_uri'. Currently, RSA and EC asymmetric keys are supported. The JWK must use following format and include only the following fields:: { "keys": [ { "kty": "RSA/EC", "alg": "<algorithm>", "use": "sig", "kid": "<key-id>", "n": "", "e": "", "x": "", "y": "", "crv": "" } ] } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#jwks_json GoogleIamWorkloadIdentityPoolProvider#jwks_json}
        '''
        value = GoogleIamWorkloadIdentityPoolProviderOidc(
            issuer_uri=issuer_uri,
            allowed_audiences=allowed_audiences,
            jwks_json=jwks_json,
        )

        return typing.cast(None, jsii.invoke(self, "putOidc", [value]))

    @jsii.member(jsii_name="putSaml")
    def put_saml(self, *, idp_metadata_xml: builtins.str) -> None:
        '''
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#idp_metadata_xml GoogleIamWorkloadIdentityPoolProvider#idp_metadata_xml}
        '''
        value = GoogleIamWorkloadIdentityPoolProviderSaml(
            idp_metadata_xml=idp_metadata_xml
        )

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#create GoogleIamWorkloadIdentityPoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#delete GoogleIamWorkloadIdentityPoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#update GoogleIamWorkloadIdentityPoolProvider#update}.
        '''
        value = GoogleIamWorkloadIdentityPoolProviderTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putX509")
    def put_x509(
        self,
        *,
        trust_store: typing.Union["GoogleIamWorkloadIdentityPoolProviderX509TrustStore", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param trust_store: trust_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#trust_store GoogleIamWorkloadIdentityPoolProvider#trust_store}
        '''
        value = GoogleIamWorkloadIdentityPoolProviderX509(trust_store=trust_store)

        return typing.cast(None, jsii.invoke(self, "putX509", [value]))

    @jsii.member(jsii_name="resetAttributeCondition")
    def reset_attribute_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeCondition", []))

    @jsii.member(jsii_name="resetAttributeMapping")
    def reset_attribute_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeMapping", []))

    @jsii.member(jsii_name="resetAws")
    def reset_aws(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAws", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOidc")
    def reset_oidc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidc", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSaml")
    def reset_saml(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetX509")
    def reset_x509(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetX509", []))

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
    @jsii.member(jsii_name="aws")
    def aws(self) -> "GoogleIamWorkloadIdentityPoolProviderAwsOutputReference":
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderAwsOutputReference", jsii.get(self, "aws"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oidc")
    def oidc(self) -> "GoogleIamWorkloadIdentityPoolProviderOidcOutputReference":
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderOidcOutputReference", jsii.get(self, "oidc"))

    @builtins.property
    @jsii.member(jsii_name="saml")
    def saml(self) -> "GoogleIamWorkloadIdentityPoolProviderSamlOutputReference":
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderSamlOutputReference", jsii.get(self, "saml"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleIamWorkloadIdentityPoolProviderTimeoutsOutputReference":
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="x509")
    def x509(self) -> "GoogleIamWorkloadIdentityPoolProviderX509OutputReference":
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderX509OutputReference", jsii.get(self, "x509"))

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
    @jsii.member(jsii_name="awsInput")
    def aws_input(self) -> typing.Optional["GoogleIamWorkloadIdentityPoolProviderAws"]:
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolProviderAws"], jsii.get(self, "awsInput"))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcInput")
    def oidc_input(
        self,
    ) -> typing.Optional["GoogleIamWorkloadIdentityPoolProviderOidc"]:
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolProviderOidc"], jsii.get(self, "oidcInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="samlInput")
    def saml_input(
        self,
    ) -> typing.Optional["GoogleIamWorkloadIdentityPoolProviderSaml"]:
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolProviderSaml"], jsii.get(self, "samlInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIamWorkloadIdentityPoolProviderTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIamWorkloadIdentityPoolProviderTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityPoolIdInput")
    def workload_identity_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadIdentityPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityPoolProviderIdInput")
    def workload_identity_pool_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadIdentityPoolProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="x509Input")
    def x509_input(
        self,
    ) -> typing.Optional["GoogleIamWorkloadIdentityPoolProviderX509"]:
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolProviderX509"], jsii.get(self, "x509Input"))

    @builtins.property
    @jsii.member(jsii_name="attributeCondition")
    def attribute_condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeCondition"))

    @attribute_condition.setter
    def attribute_condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1254da48a50ca5797e8df1f050d6bd56e310a8fbcad94b4eb7325399cf58c2af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18f1e8232b141948cf183adad7397bf2a878d9496af127ccc4831c81adf91e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e706f521bbaff0a045d33cd62504acf70a3672cf46d627adc7043b656865c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb5943777508043ebdc7e5418b0379d2c8ce8f5def189f13b8f3b8ef38b0a280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f0d0ca4ff8926970d4d7526d536131dc6053b69e1457f96a4b756c0fa8a1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18cec7dc81490e2f5a1febf6868621315825c41ffb4fc13d7c4114ce1825264f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a9f39e964c3ff1f0455dd345db4da9e62324fd4c57133e9965d4f95d00cee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityPoolId")
    def workload_identity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadIdentityPoolId"))

    @workload_identity_pool_id.setter
    def workload_identity_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0f9a981e5f6593303b2eac42754870b91627567595574afcf32aacbd712b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadIdentityPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityPoolProviderId")
    def workload_identity_pool_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadIdentityPoolProviderId"))

    @workload_identity_pool_provider_id.setter
    def workload_identity_pool_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45eb3756d751420a64d666d621df3ad70bf250512cb75c00b65979fd02eca290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadIdentityPoolProviderId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderAws",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId"},
)
class GoogleIamWorkloadIdentityPoolProviderAws:
    def __init__(self, *, account_id: builtins.str) -> None:
        '''
        :param account_id: The AWS account ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#account_id GoogleIamWorkloadIdentityPoolProvider#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b75021fe30f2868ea32199bcfcef55f7d578cbb2586879d87e947c4f745fd4a)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The AWS account ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#account_id GoogleIamWorkloadIdentityPoolProvider#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolProviderAws(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolProviderAwsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderAwsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b509cd3ea8aefeba6a4f8d6b60fb39bd3180af365af1a8bdfb464c3ff4b0184)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047a19646ce6e832c214b4f585bb27ecfb00584ef3a0fec7cfe6b57d6565fdbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkloadIdentityPoolProviderAws]:
        return typing.cast(typing.Optional[GoogleIamWorkloadIdentityPoolProviderAws], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderAws],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5fba30310928a560a5821e841269312b45a1126ccd34dd6b5814cbb17b42ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "workload_identity_pool_id": "workloadIdentityPoolId",
        "workload_identity_pool_provider_id": "workloadIdentityPoolProviderId",
        "attribute_condition": "attributeCondition",
        "attribute_mapping": "attributeMapping",
        "aws": "aws",
        "description": "description",
        "disabled": "disabled",
        "display_name": "displayName",
        "id": "id",
        "oidc": "oidc",
        "project": "project",
        "saml": "saml",
        "timeouts": "timeouts",
        "x509": "x509",
    },
)
class GoogleIamWorkloadIdentityPoolProviderConfig(
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
        workload_identity_pool_id: builtins.str,
        workload_identity_pool_provider_id: builtins.str,
        attribute_condition: typing.Optional[builtins.str] = None,
        attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        aws: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderAws, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        saml: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        x509: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolProviderX509", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param workload_identity_pool_id: The ID used for the pool, which is the final component of the pool resource name. This value should be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#workload_identity_pool_id GoogleIamWorkloadIdentityPoolProvider#workload_identity_pool_id}
        :param workload_identity_pool_provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#workload_identity_pool_provider_id GoogleIamWorkloadIdentityPoolProvider#workload_identity_pool_provider_id}
        :param attribute_condition: `A Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: - 'assertion': JSON representing the authentication credential issued by the provider. - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credential are accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#attribute_condition GoogleIamWorkloadIdentityPoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: - 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. Cannot exceed 127 characters. - 'google.groups': Groups the external identity belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where '{custom_attribute}' is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workload to Google Cloud resources. For example: - 'google.subject': 'principal://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/subject/{value}' - 'google.groups': 'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/group/{value}' - 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For AWS providers, the following rules apply: - If no attribute mapping is defined, the following default mapping applies:: { "google.subject":"assertion.arn", "attribute.aws_role": "assertion.arn.contains('assumed-role')" " ? assertion.arn.extract('{account_arn}assumed-role/')" " + 'assumed-role/'" " + assertion.arn.extract('assumed-role/{role_name}/')" " : assertion.arn", } - If any custom attribute mappings are defined, they must include a mapping to the 'google.subject' attribute. For OIDC providers, the following rules apply: - Custom attribute mappings must be defined, and must include a mapping to the 'google.subject' attribute. For example, the following maps the 'sub' claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#attribute_mapping GoogleIamWorkloadIdentityPoolProvider#attribute_mapping}
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#aws GoogleIamWorkloadIdentityPoolProvider#aws}
        :param description: A description for the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#description GoogleIamWorkloadIdentityPoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#disabled GoogleIamWorkloadIdentityPoolProvider#disabled}
        :param display_name: A display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#display_name GoogleIamWorkloadIdentityPoolProvider#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#id GoogleIamWorkloadIdentityPoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#oidc GoogleIamWorkloadIdentityPoolProvider#oidc}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#project GoogleIamWorkloadIdentityPoolProvider#project}.
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#saml GoogleIamWorkloadIdentityPoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#timeouts GoogleIamWorkloadIdentityPoolProvider#timeouts}
        :param x509: x509 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#x509 GoogleIamWorkloadIdentityPoolProvider#x509}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws, dict):
            aws = GoogleIamWorkloadIdentityPoolProviderAws(**aws)
        if isinstance(oidc, dict):
            oidc = GoogleIamWorkloadIdentityPoolProviderOidc(**oidc)
        if isinstance(saml, dict):
            saml = GoogleIamWorkloadIdentityPoolProviderSaml(**saml)
        if isinstance(timeouts, dict):
            timeouts = GoogleIamWorkloadIdentityPoolProviderTimeouts(**timeouts)
        if isinstance(x509, dict):
            x509 = GoogleIamWorkloadIdentityPoolProviderX509(**x509)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac48cd5d2a8884d3757c7fbaa14ca696659c4d9a95296078b85fb842f287ef9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument workload_identity_pool_id", value=workload_identity_pool_id, expected_type=type_hints["workload_identity_pool_id"])
            check_type(argname="argument workload_identity_pool_provider_id", value=workload_identity_pool_provider_id, expected_type=type_hints["workload_identity_pool_provider_id"])
            check_type(argname="argument attribute_condition", value=attribute_condition, expected_type=type_hints["attribute_condition"])
            check_type(argname="argument attribute_mapping", value=attribute_mapping, expected_type=type_hints["attribute_mapping"])
            check_type(argname="argument aws", value=aws, expected_type=type_hints["aws"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument oidc", value=oidc, expected_type=type_hints["oidc"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument saml", value=saml, expected_type=type_hints["saml"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument x509", value=x509, expected_type=type_hints["x509"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "workload_identity_pool_id": workload_identity_pool_id,
            "workload_identity_pool_provider_id": workload_identity_pool_provider_id,
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
        if aws is not None:
            self._values["aws"] = aws
        if description is not None:
            self._values["description"] = description
        if disabled is not None:
            self._values["disabled"] = disabled
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if oidc is not None:
            self._values["oidc"] = oidc
        if project is not None:
            self._values["project"] = project
        if saml is not None:
            self._values["saml"] = saml
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if x509 is not None:
            self._values["x509"] = x509

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
    def workload_identity_pool_id(self) -> builtins.str:
        '''The ID used for the pool, which is the final component of the pool resource name.

        This
        value should be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix
        'gcp-' is reserved for use by Google, and may not be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#workload_identity_pool_id GoogleIamWorkloadIdentityPoolProvider#workload_identity_pool_id}
        '''
        result = self._values.get("workload_identity_pool_id")
        assert result is not None, "Required property 'workload_identity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workload_identity_pool_provider_id(self) -> builtins.str:
        '''The ID for the provider, which becomes the final component of the resource name.

        This
        value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix
        'gcp-' is reserved for use by Google, and may not be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#workload_identity_pool_provider_id GoogleIamWorkloadIdentityPoolProvider#workload_identity_pool_provider_id}
        '''
        result = self._values.get("workload_identity_pool_provider_id")
        assert result is not None, "Required property 'workload_identity_pool_provider_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attribute_condition(self) -> typing.Optional[builtins.str]:
        '''`A Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted.

        The expression must output a boolean representing whether to allow the federation.

        The following keywords may be referenced in the expressions:

        - 'assertion': JSON representing the authentication credential issued by the provider.
        - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'.
        - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'.

        The maximum length of the attribute condition expression is 4096 characters. If
        unspecified, all valid authentication credential are accepted.

        The following example shows how to only allow credentials with a mapped 'google.groups'
        value of 'admins'::

           "'admins' in google.groups"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#attribute_condition GoogleIamWorkloadIdentityPoolProvider#attribute_condition}
        '''
        result = self._values.get("attribute_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attribute_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Maps attributes from authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'.

        Each key must be a string specifying the Google Cloud IAM attribute to map to.

        The following keys are supported:

        - 'google.subject': The principal IAM is authenticating. You can reference this value
          in IAM bindings. This is also the subject that appears in Cloud Logging logs.
          Cannot exceed 127 characters.
        - 'google.groups': Groups the external identity belongs to. You can grant groups
          access to resources using an IAM 'principalSet' binding; access applies to all
          members of the group.

        You can also provide custom attributes by specifying 'attribute.{custom_attribute}',
        where '{custom_attribute}' is the name of the custom attribute to be mapped. You can
        define a maximum of 50 custom attributes. The maximum length of a mapped attribute key
        is 100 characters, and the key may only contain the characters [a-z0-9_].

        You can reference these attributes in IAM policies to define fine-grained access for a
        workload to Google Cloud resources. For example:

        - 'google.subject':
          'principal://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/subject/{value}'
        - 'google.groups':
          'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/group/{value}'
        - 'attribute.{custom_attribute}':
          'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/attribute.{custom_attribute}/{value}'

        Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_
        function that maps an identity provider credential to the normalized attribute specified
        by the corresponding map key.

        You can use the 'assertion' keyword in the expression to access a JSON representation of
        the authentication credential issued by the provider.

        The maximum length of an attribute mapping expression is 2048 characters. When evaluated,
        the total size of all mapped attributes must not exceed 8KB.

        For AWS providers, the following rules apply:

        - If no attribute mapping is defined, the following default mapping applies::

             {
               "google.subject":"assertion.arn",
               "attribute.aws_role":
                 "assertion.arn.contains('assumed-role')"
                 " ? assertion.arn.extract('{account_arn}assumed-role/')"
                 "   + 'assumed-role/'"
                 "   + assertion.arn.extract('assumed-role/{role_name}/')"
                 " : assertion.arn",
             }
        - If any custom attribute mappings are defined, they must include a mapping to the
          'google.subject' attribute.

        For OIDC providers, the following rules apply:

        - Custom attribute mappings must be defined, and must include a mapping to the
          'google.subject' attribute. For example, the following maps the 'sub' claim of the
          incoming credential to the 'subject' attribute on a Google token::

             {"google.subject": "assertion.sub"}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#attribute_mapping GoogleIamWorkloadIdentityPoolProvider#attribute_mapping}
        '''
        result = self._values.get("attribute_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def aws(self) -> typing.Optional[GoogleIamWorkloadIdentityPoolProviderAws]:
        '''aws block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#aws GoogleIamWorkloadIdentityPoolProvider#aws}
        '''
        result = self._values.get("aws")
        return typing.cast(typing.Optional[GoogleIamWorkloadIdentityPoolProviderAws], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the provider. Cannot exceed 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#description GoogleIamWorkloadIdentityPoolProvider#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#disabled GoogleIamWorkloadIdentityPoolProvider#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A display name for the provider. Cannot exceed 32 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#display_name GoogleIamWorkloadIdentityPoolProvider#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#id GoogleIamWorkloadIdentityPoolProvider#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc(self) -> typing.Optional["GoogleIamWorkloadIdentityPoolProviderOidc"]:
        '''oidc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#oidc GoogleIamWorkloadIdentityPoolProvider#oidc}
        '''
        result = self._values.get("oidc")
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolProviderOidc"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#project GoogleIamWorkloadIdentityPoolProvider#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml(self) -> typing.Optional["GoogleIamWorkloadIdentityPoolProviderSaml"]:
        '''saml block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#saml GoogleIamWorkloadIdentityPoolProvider#saml}
        '''
        result = self._values.get("saml")
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolProviderSaml"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleIamWorkloadIdentityPoolProviderTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#timeouts GoogleIamWorkloadIdentityPoolProvider#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolProviderTimeouts"], result)

    @builtins.property
    def x509(self) -> typing.Optional["GoogleIamWorkloadIdentityPoolProviderX509"]:
        '''x509 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#x509 GoogleIamWorkloadIdentityPoolProvider#x509}
        '''
        result = self._values.get("x509")
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolProviderX509"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderOidc",
    jsii_struct_bases=[],
    name_mapping={
        "issuer_uri": "issuerUri",
        "allowed_audiences": "allowedAudiences",
        "jwks_json": "jwksJson",
    },
)
class GoogleIamWorkloadIdentityPoolProviderOidc:
    def __init__(
        self,
        *,
        issuer_uri: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        jwks_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param issuer_uri: The OIDC issuer URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#issuer_uri GoogleIamWorkloadIdentityPoolProvider#issuer_uri}
        :param allowed_audiences: Acceptable values for the 'aud' field (audience) in the OIDC token. Token exchange requests are rejected if the token audience does not match one of the configured values. Each audience may be at most 256 characters. A maximum of 10 audiences may be configured. If this list is empty, the OIDC token audience must be equal to the full canonical resource name of the WorkloadIdentityPoolProvider, with or without the HTTPS prefix. For example:: //iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id> https://iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#allowed_audiences GoogleIamWorkloadIdentityPoolProvider#allowed_audiences}
        :param jwks_json: OIDC JWKs in JSON String format. For details on definition of a JWK, see https:tools.ietf.org/html/rfc7517. If not set, then we use the 'jwks_uri' from the discovery document fetched from the .well-known path for the 'issuer_uri'. Currently, RSA and EC asymmetric keys are supported. The JWK must use following format and include only the following fields:: { "keys": [ { "kty": "RSA/EC", "alg": "<algorithm>", "use": "sig", "kid": "<key-id>", "n": "", "e": "", "x": "", "y": "", "crv": "" } ] } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#jwks_json GoogleIamWorkloadIdentityPoolProvider#jwks_json}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f718b45507175380bf1753e6563358bc69ec348300586295dc87511d5a814ed6)
            check_type(argname="argument issuer_uri", value=issuer_uri, expected_type=type_hints["issuer_uri"])
            check_type(argname="argument allowed_audiences", value=allowed_audiences, expected_type=type_hints["allowed_audiences"])
            check_type(argname="argument jwks_json", value=jwks_json, expected_type=type_hints["jwks_json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer_uri": issuer_uri,
        }
        if allowed_audiences is not None:
            self._values["allowed_audiences"] = allowed_audiences
        if jwks_json is not None:
            self._values["jwks_json"] = jwks_json

    @builtins.property
    def issuer_uri(self) -> builtins.str:
        '''The OIDC issuer URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#issuer_uri GoogleIamWorkloadIdentityPoolProvider#issuer_uri}
        '''
        result = self._values.get("issuer_uri")
        assert result is not None, "Required property 'issuer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Acceptable values for the 'aud' field (audience) in the OIDC token.

        Token exchange
        requests are rejected if the token audience does not match one of the configured
        values. Each audience may be at most 256 characters. A maximum of 10 audiences may
        be configured.

        If this list is empty, the OIDC token audience must be equal to the full canonical
        resource name of the WorkloadIdentityPoolProvider, with or without the HTTPS prefix.
        For example::

           //iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id>
           https://iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id>

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#allowed_audiences GoogleIamWorkloadIdentityPoolProvider#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#jwks_json GoogleIamWorkloadIdentityPoolProvider#jwks_json}
        '''
        result = self._values.get("jwks_json")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolProviderOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolProviderOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bb18f7f585ab968d5365b737ff3a9af17a5beecaae0e9fde92c6f3b0cf73a51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedAudiences")
    def reset_allowed_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAudiences", []))

    @jsii.member(jsii_name="resetJwksJson")
    def reset_jwks_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwksJson", []))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiencesInput")
    def allowed_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAudiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUriInput")
    def issuer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="jwksJsonInput")
    def jwks_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwksJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @allowed_audiences.setter
    def allowed_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a84b033a0a2c096040c67bcb34c707f7ad8f633f41a3171ecff45302d7bd26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc57c8e5493d9e1a2b50065f6bd893b77d6657a866c51b79cce7c8b28f2536d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwksJson")
    def jwks_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwksJson"))

    @jwks_json.setter
    def jwks_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9f7b598f5063beb903cbb3391c859cd0e9b6064bf9684dfc96827f5bc9b44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwksJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkloadIdentityPoolProviderOidc]:
        return typing.cast(typing.Optional[GoogleIamWorkloadIdentityPoolProviderOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderOidc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39809f4a1421ce7e2fbd8663a0e258c768ebdc0069a10389626eb468d295ab95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderSaml",
    jsii_struct_bases=[],
    name_mapping={"idp_metadata_xml": "idpMetadataXml"},
)
class GoogleIamWorkloadIdentityPoolProviderSaml:
    def __init__(self, *, idp_metadata_xml: builtins.str) -> None:
        '''
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#idp_metadata_xml GoogleIamWorkloadIdentityPoolProvider#idp_metadata_xml}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac603480cae0cca8936c5b19b5f8fd6011309198b21516280c79465378f6c24)
            check_type(argname="argument idp_metadata_xml", value=idp_metadata_xml, expected_type=type_hints["idp_metadata_xml"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "idp_metadata_xml": idp_metadata_xml,
        }

    @builtins.property
    def idp_metadata_xml(self) -> builtins.str:
        '''SAML Identity provider configuration metadata xml doc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#idp_metadata_xml GoogleIamWorkloadIdentityPoolProvider#idp_metadata_xml}
        '''
        result = self._values.get("idp_metadata_xml")
        assert result is not None, "Required property 'idp_metadata_xml' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolProviderSaml(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolProviderSamlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderSamlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b97af1278301cf3afb040cca014b47ee741d479fa03795b39df6cfa67393ffa0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f65627f84bc453bec6d7a55c0a33dc9e237d21b09ed2e7147f0c01f25045f7b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpMetadataXml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkloadIdentityPoolProviderSaml]:
        return typing.cast(typing.Optional[GoogleIamWorkloadIdentityPoolProviderSaml], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderSaml],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbd79c3c7c31c452910ff23a2f30051099a7953a9a11e27d3abbe8bfdc85181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleIamWorkloadIdentityPoolProviderTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#create GoogleIamWorkloadIdentityPoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#delete GoogleIamWorkloadIdentityPoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#update GoogleIamWorkloadIdentityPoolProvider#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3bd370c3daf5b9bac042827be7dc86ec1f445c2583a155622794d78f9224af)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#create GoogleIamWorkloadIdentityPoolProvider#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#delete GoogleIamWorkloadIdentityPoolProvider#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#update GoogleIamWorkloadIdentityPoolProvider#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolProviderTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolProviderTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97219de153f315b0adef24fd7ed1553e6fa2d2e703774e8f97a096eb1cae7830)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db1ae8f0858d3fc03048913b71b82df8599f16682b1a656cdab91af87b6de7b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6b4c6ae95c19c8bdd04843bbe820f2f00ea141e254678ee3ead4b8408e8a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee2366c05aae8d96df99cf1bb05d9690c15bf4f7fd74eb729d7d733cd6b8bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a7f4c21b5aacf0df70737c6a61dd30f97177fc11f55fa40ffda51343dee46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509",
    jsii_struct_bases=[],
    name_mapping={"trust_store": "trustStore"},
)
class GoogleIamWorkloadIdentityPoolProviderX509:
    def __init__(
        self,
        *,
        trust_store: typing.Union["GoogleIamWorkloadIdentityPoolProviderX509TrustStore", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param trust_store: trust_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#trust_store GoogleIamWorkloadIdentityPoolProvider#trust_store}
        '''
        if isinstance(trust_store, dict):
            trust_store = GoogleIamWorkloadIdentityPoolProviderX509TrustStore(**trust_store)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9da1c8ee3cec5c84728e280cce9fb90238f44be0c7a3a6eeaa1e74142e0053)
            check_type(argname="argument trust_store", value=trust_store, expected_type=type_hints["trust_store"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trust_store": trust_store,
        }

    @builtins.property
    def trust_store(self) -> "GoogleIamWorkloadIdentityPoolProviderX509TrustStore":
        '''trust_store block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#trust_store GoogleIamWorkloadIdentityPoolProvider#trust_store}
        '''
        result = self._values.get("trust_store")
        assert result is not None, "Required property 'trust_store' is missing"
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderX509TrustStore", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolProviderX509(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolProviderX509OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f12a14dd79862fbcb946b1bb24b2a379dba1157a7dab69ea91a6d3be6d2e999)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTrustStore")
    def put_trust_store(
        self,
        *,
        trust_anchors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors", typing.Dict[builtins.str, typing.Any]]]],
        intermediate_cas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param trust_anchors: trust_anchors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#trust_anchors GoogleIamWorkloadIdentityPoolProvider#trust_anchors}
        :param intermediate_cas: intermediate_cas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#intermediate_cas GoogleIamWorkloadIdentityPoolProvider#intermediate_cas}
        '''
        value = GoogleIamWorkloadIdentityPoolProviderX509TrustStore(
            trust_anchors=trust_anchors, intermediate_cas=intermediate_cas
        )

        return typing.cast(None, jsii.invoke(self, "putTrustStore", [value]))

    @builtins.property
    @jsii.member(jsii_name="trustStore")
    def trust_store(
        self,
    ) -> "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreOutputReference":
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderX509TrustStoreOutputReference", jsii.get(self, "trustStore"))

    @builtins.property
    @jsii.member(jsii_name="trustStoreInput")
    def trust_store_input(
        self,
    ) -> typing.Optional["GoogleIamWorkloadIdentityPoolProviderX509TrustStore"]:
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolProviderX509TrustStore"], jsii.get(self, "trustStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkloadIdentityPoolProviderX509]:
        return typing.cast(typing.Optional[GoogleIamWorkloadIdentityPoolProviderX509], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderX509],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea40f4525ecc457adf61a446c010a07c2b0786882ab1ca51ac2e5a3983a1c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509TrustStore",
    jsii_struct_bases=[],
    name_mapping={
        "trust_anchors": "trustAnchors",
        "intermediate_cas": "intermediateCas",
    },
)
class GoogleIamWorkloadIdentityPoolProviderX509TrustStore:
    def __init__(
        self,
        *,
        trust_anchors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors", typing.Dict[builtins.str, typing.Any]]]],
        intermediate_cas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param trust_anchors: trust_anchors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#trust_anchors GoogleIamWorkloadIdentityPoolProvider#trust_anchors}
        :param intermediate_cas: intermediate_cas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#intermediate_cas GoogleIamWorkloadIdentityPoolProvider#intermediate_cas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018602c5c2583d364fadf5af324c4d75f52be56463c29f614b6fe7b131b33a44)
            check_type(argname="argument trust_anchors", value=trust_anchors, expected_type=type_hints["trust_anchors"])
            check_type(argname="argument intermediate_cas", value=intermediate_cas, expected_type=type_hints["intermediate_cas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trust_anchors": trust_anchors,
        }
        if intermediate_cas is not None:
            self._values["intermediate_cas"] = intermediate_cas

    @builtins.property
    def trust_anchors(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors"]]:
        '''trust_anchors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#trust_anchors GoogleIamWorkloadIdentityPoolProvider#trust_anchors}
        '''
        result = self._values.get("trust_anchors")
        assert result is not None, "Required property 'trust_anchors' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors"]], result)

    @builtins.property
    def intermediate_cas(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas"]]]:
        '''intermediate_cas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#intermediate_cas GoogleIamWorkloadIdentityPoolProvider#intermediate_cas}
        '''
        result = self._values.get("intermediate_cas")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolProviderX509TrustStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas",
    jsii_struct_bases=[],
    name_mapping={"pem_certificate": "pemCertificate"},
)
class GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas:
    def __init__(
        self,
        *,
        pem_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pem_certificate: PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#pem_certificate GoogleIamWorkloadIdentityPoolProvider#pem_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ccf43e3561e02332782e451d982b78a04a8cf7c1b2c6548fb7ce71232cdef53)
            check_type(argname="argument pem_certificate", value=pem_certificate, expected_type=type_hints["pem_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pem_certificate is not None:
            self._values["pem_certificate"] = pem_certificate

    @builtins.property
    def pem_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#pem_certificate GoogleIamWorkloadIdentityPoolProvider#pem_certificate}
        '''
        result = self._values.get("pem_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ee917055f5e3441bbf2a7512e90fdb948846d7784aa345d12c93336d479bfde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad4d60cc0d65adbe69c539ef79e64ba3fe035e86b410f7bca23e577377071f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a740ef99474513069924b09a6d86b2eecd71eb30bde4972e89cbdff3c862fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee57b54f1addc538cf270c6c0819a1a71574e89f1b9e68acf81da2b7393a5ae8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__931ac65b860ced77e3df73a6d8fe6d1d7b0226a4ee2fd4beeb1417822a09986d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85010cbe5e9ae4302ceaafbb3f6b3e1f4ffc9c350da2d9b8b8a399de911d6ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__118a91cc41304404db8783132fe3c47ba9c83563b0343600f462db9b2503dca4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPemCertificate")
    def reset_pem_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemCertificate", []))

    @builtins.property
    @jsii.member(jsii_name="pemCertificateInput")
    def pem_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="pemCertificate")
    def pem_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemCertificate"))

    @pem_certificate.setter
    def pem_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be249261576c9c06ff6a689cfb396a222e7355c941540dc843e55dfda6133739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01fb4edba237664499cf38564142ea44f1599002334cd51553e9160ed1c8c0e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIamWorkloadIdentityPoolProviderX509TrustStoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509TrustStoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c3ad945eaa7f46033f9b3fd25c89763da369cdb809da9571cb866dd89d8d66b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIntermediateCas")
    def put_intermediate_cas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6033a7c93ac447a6ef9054def0d876f111febf45ce6426ae6fa6bc3bd834d385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIntermediateCas", [value]))

    @jsii.member(jsii_name="putTrustAnchors")
    def put_trust_anchors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d9dbbc95aa223a07abaf724b88ec6a2a9fa189e2e1b77254350e722f39c723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrustAnchors", [value]))

    @jsii.member(jsii_name="resetIntermediateCas")
    def reset_intermediate_cas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntermediateCas", []))

    @builtins.property
    @jsii.member(jsii_name="intermediateCas")
    def intermediate_cas(
        self,
    ) -> GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList:
        return typing.cast(GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList, jsii.get(self, "intermediateCas"))

    @builtins.property
    @jsii.member(jsii_name="trustAnchors")
    def trust_anchors(
        self,
    ) -> "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList":
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList", jsii.get(self, "trustAnchors"))

    @builtins.property
    @jsii.member(jsii_name="intermediateCasInput")
    def intermediate_cas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]], jsii.get(self, "intermediateCasInput"))

    @builtins.property
    @jsii.member(jsii_name="trustAnchorsInput")
    def trust_anchors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors"]]], jsii.get(self, "trustAnchorsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkloadIdentityPoolProviderX509TrustStore]:
        return typing.cast(typing.Optional[GoogleIamWorkloadIdentityPoolProviderX509TrustStore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderX509TrustStore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d475ac0c1e0e7d5ef7204a45e263d82ab9a8b1b3ac603b6616823d28521369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors",
    jsii_struct_bases=[],
    name_mapping={"pem_certificate": "pemCertificate"},
)
class GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors:
    def __init__(
        self,
        *,
        pem_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pem_certificate: PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#pem_certificate GoogleIamWorkloadIdentityPoolProvider#pem_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b6d66216f7cc959e62abb7521c5ae5bdcce16e534a34e43b26a508c2571b89)
            check_type(argname="argument pem_certificate", value=pem_certificate, expected_type=type_hints["pem_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pem_certificate is not None:
            self._values["pem_certificate"] = pem_certificate

    @builtins.property
    def pem_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool_provider#pem_certificate GoogleIamWorkloadIdentityPoolProvider#pem_certificate}
        '''
        result = self._values.get("pem_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91952c7cc95fc84d389bc7c349bd6a87d11e81a0a2dbf8257c7b5bf1305f7206)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04747aa79617d31e78060563892a72dfd81a778bea73455f7acfceff60d46d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3d41e77912d75288823b6faf030bf94452289619f8f090f8def1f5eed93c8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cb0cc68aafb126457a9920faeadfeab4823d2747c137648e143609843f3117d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad56c4b127665fdf443dbc7cb4e36e420cdca4692c833f6d611eb56ee1720648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f81096c1a1a94ff28613ddcbfcf3c6f7dd0f8d45fb5dc3f03fb1a0abf597c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPoolProvider.GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37ac08aec719cfdc2fd1f96df429dcaba87d84cb5d040d25c8909e8ce78a738f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPemCertificate")
    def reset_pem_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemCertificate", []))

    @builtins.property
    @jsii.member(jsii_name="pemCertificateInput")
    def pem_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="pemCertificate")
    def pem_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemCertificate"))

    @pem_certificate.setter
    def pem_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e066ba22636556b4c899e5a2e5c0a2f6d551c44277d5270fec2c8eadef401534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dcbfda9842916cf03dade5a9abff476ebbbd385221b077adaea6b19d2901f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleIamWorkloadIdentityPoolProvider",
    "GoogleIamWorkloadIdentityPoolProviderAws",
    "GoogleIamWorkloadIdentityPoolProviderAwsOutputReference",
    "GoogleIamWorkloadIdentityPoolProviderConfig",
    "GoogleIamWorkloadIdentityPoolProviderOidc",
    "GoogleIamWorkloadIdentityPoolProviderOidcOutputReference",
    "GoogleIamWorkloadIdentityPoolProviderSaml",
    "GoogleIamWorkloadIdentityPoolProviderSamlOutputReference",
    "GoogleIamWorkloadIdentityPoolProviderTimeouts",
    "GoogleIamWorkloadIdentityPoolProviderTimeoutsOutputReference",
    "GoogleIamWorkloadIdentityPoolProviderX509",
    "GoogleIamWorkloadIdentityPoolProviderX509OutputReference",
    "GoogleIamWorkloadIdentityPoolProviderX509TrustStore",
    "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas",
    "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList",
    "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference",
    "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreOutputReference",
    "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors",
    "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList",
    "GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference",
]

publication.publish()

def _typecheckingstub__b3fe01d243fcdbdc314942b687214c438ce8f21ccdaa8c6d3e439540629d6ca4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    workload_identity_pool_id: builtins.str,
    workload_identity_pool_provider_id: builtins.str,
    attribute_condition: typing.Optional[builtins.str] = None,
    attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    aws: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderAws, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    saml: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    x509: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderX509, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__00356f08092ffc07223a332edd74dfab63a450384dd66dfaa241254312bb7a5c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1254da48a50ca5797e8df1f050d6bd56e310a8fbcad94b4eb7325399cf58c2af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f1e8232b141948cf183adad7397bf2a878d9496af127ccc4831c81adf91e8d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e706f521bbaff0a045d33cd62504acf70a3672cf46d627adc7043b656865c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5943777508043ebdc7e5418b0379d2c8ce8f5def189f13b8f3b8ef38b0a280(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f0d0ca4ff8926970d4d7526d536131dc6053b69e1457f96a4b756c0fa8a1b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cec7dc81490e2f5a1febf6868621315825c41ffb4fc13d7c4114ce1825264f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a9f39e964c3ff1f0455dd345db4da9e62324fd4c57133e9965d4f95d00cee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0f9a981e5f6593303b2eac42754870b91627567595574afcf32aacbd712b74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45eb3756d751420a64d666d621df3ad70bf250512cb75c00b65979fd02eca290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b75021fe30f2868ea32199bcfcef55f7d578cbb2586879d87e947c4f745fd4a(
    *,
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b509cd3ea8aefeba6a4f8d6b60fb39bd3180af365af1a8bdfb464c3ff4b0184(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047a19646ce6e832c214b4f585bb27ecfb00584ef3a0fec7cfe6b57d6565fdbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5fba30310928a560a5821e841269312b45a1126ccd34dd6b5814cbb17b42ef(
    value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderAws],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac48cd5d2a8884d3757c7fbaa14ca696659c4d9a95296078b85fb842f287ef9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    workload_identity_pool_id: builtins.str,
    workload_identity_pool_provider_id: builtins.str,
    attribute_condition: typing.Optional[builtins.str] = None,
    attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    aws: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderAws, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    saml: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    x509: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolProviderX509, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f718b45507175380bf1753e6563358bc69ec348300586295dc87511d5a814ed6(
    *,
    issuer_uri: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    jwks_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb18f7f585ab968d5365b737ff3a9af17a5beecaae0e9fde92c6f3b0cf73a51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a84b033a0a2c096040c67bcb34c707f7ad8f633f41a3171ecff45302d7bd26(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc57c8e5493d9e1a2b50065f6bd893b77d6657a866c51b79cce7c8b28f2536d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9f7b598f5063beb903cbb3391c859cd0e9b6064bf9684dfc96827f5bc9b44a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39809f4a1421ce7e2fbd8663a0e258c768ebdc0069a10389626eb468d295ab95(
    value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac603480cae0cca8936c5b19b5f8fd6011309198b21516280c79465378f6c24(
    *,
    idp_metadata_xml: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97af1278301cf3afb040cca014b47ee741d479fa03795b39df6cfa67393ffa0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65627f84bc453bec6d7a55c0a33dc9e237d21b09ed2e7147f0c01f25045f7b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbd79c3c7c31c452910ff23a2f30051099a7953a9a11e27d3abbe8bfdc85181(
    value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderSaml],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3bd370c3daf5b9bac042827be7dc86ec1f445c2583a155622794d78f9224af(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97219de153f315b0adef24fd7ed1553e6fa2d2e703774e8f97a096eb1cae7830(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1ae8f0858d3fc03048913b71b82df8599f16682b1a656cdab91af87b6de7b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6b4c6ae95c19c8bdd04843bbe820f2f00ea141e254678ee3ead4b8408e8a20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee2366c05aae8d96df99cf1bb05d9690c15bf4f7fd74eb729d7d733cd6b8bd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a7f4c21b5aacf0df70737c6a61dd30f97177fc11f55fa40ffda51343dee46c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9da1c8ee3cec5c84728e280cce9fb90238f44be0c7a3a6eeaa1e74142e0053(
    *,
    trust_store: typing.Union[GoogleIamWorkloadIdentityPoolProviderX509TrustStore, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f12a14dd79862fbcb946b1bb24b2a379dba1157a7dab69ea91a6d3be6d2e999(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea40f4525ecc457adf61a446c010a07c2b0786882ab1ca51ac2e5a3983a1c9d(
    value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderX509],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018602c5c2583d364fadf5af324c4d75f52be56463c29f614b6fe7b131b33a44(
    *,
    trust_anchors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors, typing.Dict[builtins.str, typing.Any]]]],
    intermediate_cas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ccf43e3561e02332782e451d982b78a04a8cf7c1b2c6548fb7ce71232cdef53(
    *,
    pem_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee917055f5e3441bbf2a7512e90fdb948846d7784aa345d12c93336d479bfde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad4d60cc0d65adbe69c539ef79e64ba3fe035e86b410f7bca23e577377071f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a740ef99474513069924b09a6d86b2eecd71eb30bde4972e89cbdff3c862fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee57b54f1addc538cf270c6c0819a1a71574e89f1b9e68acf81da2b7393a5ae8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931ac65b860ced77e3df73a6d8fe6d1d7b0226a4ee2fd4beeb1417822a09986d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85010cbe5e9ae4302ceaafbb3f6b3e1f4ffc9c350da2d9b8b8a399de911d6ef5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118a91cc41304404db8783132fe3c47ba9c83563b0343600f462db9b2503dca4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be249261576c9c06ff6a689cfb396a222e7355c941540dc843e55dfda6133739(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01fb4edba237664499cf38564142ea44f1599002334cd51553e9160ed1c8c0e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3ad945eaa7f46033f9b3fd25c89763da369cdb809da9571cb866dd89d8d66b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6033a7c93ac447a6ef9054def0d876f111febf45ce6426ae6fa6bc3bd834d385(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d9dbbc95aa223a07abaf724b88ec6a2a9fa189e2e1b77254350e722f39c723(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d475ac0c1e0e7d5ef7204a45e263d82ab9a8b1b3ac603b6616823d28521369(
    value: typing.Optional[GoogleIamWorkloadIdentityPoolProviderX509TrustStore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b6d66216f7cc959e62abb7521c5ae5bdcce16e534a34e43b26a508c2571b89(
    *,
    pem_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91952c7cc95fc84d389bc7c349bd6a87d11e81a0a2dbf8257c7b5bf1305f7206(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04747aa79617d31e78060563892a72dfd81a778bea73455f7acfceff60d46d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3d41e77912d75288823b6faf030bf94452289619f8f090f8def1f5eed93c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb0cc68aafb126457a9920faeadfeab4823d2747c137648e143609843f3117d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad56c4b127665fdf443dbc7cb4e36e420cdca4692c833f6d611eb56ee1720648(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f81096c1a1a94ff28613ddcbfcf3c6f7dd0f8d45fb5dc3f03fb1a0abf597c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ac08aec719cfdc2fd1f96df429dcaba87d84cb5d040d25c8909e8ce78a738f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e066ba22636556b4c899e5a2e5c0a2f6d551c44277d5270fec2c8eadef401534(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dcbfda9842916cf03dade5a9abff476ebbbd385221b077adaea6b19d2901f09(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]],
) -> None:
    """Type checking stubs"""
    pass
