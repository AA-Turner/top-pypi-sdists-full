r'''
# `google_iam_workload_identity_pool_provider`

Refer to the Terraform Registry for docs: [`google_iam_workload_identity_pool_provider`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider).
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


class IamWorkloadIdentityPoolProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider google_iam_workload_identity_pool_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        workload_identity_pool_id: builtins.str,
        workload_identity_pool_provider_id: builtins.str,
        attribute_condition: typing.Optional[builtins.str] = None,
        attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        aws: typing.Optional[typing.Union["IamWorkloadIdentityPoolProviderAws", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["IamWorkloadIdentityPoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        saml: typing.Optional[typing.Union["IamWorkloadIdentityPoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["IamWorkloadIdentityPoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        x509: typing.Optional[typing.Union["IamWorkloadIdentityPoolProviderX509", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider google_iam_workload_identity_pool_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param workload_identity_pool_id: The ID used for the pool, which is the final component of the pool resource name. This value should be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#workload_identity_pool_id IamWorkloadIdentityPoolProvider#workload_identity_pool_id}
        :param workload_identity_pool_provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#workload_identity_pool_provider_id IamWorkloadIdentityPoolProvider#workload_identity_pool_provider_id}
        :param attribute_condition: `A Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: - 'assertion': JSON representing the authentication credential issued by the provider. - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credential are accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#attribute_condition IamWorkloadIdentityPoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: - 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. Cannot exceed 127 characters. - 'google.groups': Groups the external identity belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where '{custom_attribute}' is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workload to Google Cloud resources. For example: - 'google.subject': 'principal://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/subject/{value}' - 'google.groups': 'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/group/{value}' - 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For AWS providers, the following rules apply: - If no attribute mapping is defined, the following default mapping applies:: { "google.subject":"assertion.arn", "attribute.aws_role": "assertion.arn.contains('assumed-role')" " ? assertion.arn.extract('{account_arn}assumed-role/')" " + 'assumed-role/'" " + assertion.arn.extract('assumed-role/{role_name}/')" " : assertion.arn", } - If any custom attribute mappings are defined, they must include a mapping to the 'google.subject' attribute. For OIDC providers, the following rules apply: - Custom attribute mappings must be defined, and must include a mapping to the 'google.subject' attribute. For example, the following maps the 'sub' claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#attribute_mapping IamWorkloadIdentityPoolProvider#attribute_mapping}
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#aws IamWorkloadIdentityPoolProvider#aws}
        :param description: A description for the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#description IamWorkloadIdentityPoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#disabled IamWorkloadIdentityPoolProvider#disabled}
        :param display_name: A display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#display_name IamWorkloadIdentityPoolProvider#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#id IamWorkloadIdentityPoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#oidc IamWorkloadIdentityPoolProvider#oidc}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#project IamWorkloadIdentityPoolProvider#project}.
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#saml IamWorkloadIdentityPoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#timeouts IamWorkloadIdentityPoolProvider#timeouts}
        :param x509: x509 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#x509 IamWorkloadIdentityPoolProvider#x509}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7db34fdba41bfb946679b6b528f9e7dedcd81f06705360bdced99e89c7d3ddd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IamWorkloadIdentityPoolProviderConfig(
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
        '''Generates CDKTF code for importing a IamWorkloadIdentityPoolProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IamWorkloadIdentityPoolProvider to import.
        :param import_from_id: The id of the existing IamWorkloadIdentityPoolProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IamWorkloadIdentityPoolProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee75e96605d360bd556b51979775e15d1a1c5df1329c391e10c47a7e6acab62)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAws")
    def put_aws(self, *, account_id: builtins.str) -> None:
        '''
        :param account_id: The AWS account ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#account_id IamWorkloadIdentityPoolProvider#account_id}
        '''
        value = IamWorkloadIdentityPoolProviderAws(account_id=account_id)

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
        :param issuer_uri: The OIDC issuer URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#issuer_uri IamWorkloadIdentityPoolProvider#issuer_uri}
        :param allowed_audiences: Acceptable values for the 'aud' field (audience) in the OIDC token. Token exchange requests are rejected if the token audience does not match one of the configured values. Each audience may be at most 256 characters. A maximum of 10 audiences may be configured. If this list is empty, the OIDC token audience must be equal to the full canonical resource name of the WorkloadIdentityPoolProvider, with or without the HTTPS prefix. For example:: //iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id> https://iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#allowed_audiences IamWorkloadIdentityPoolProvider#allowed_audiences}
        :param jwks_json: OIDC JWKs in JSON String format. For details on definition of a JWK, see https:tools.ietf.org/html/rfc7517. If not set, then we use the 'jwks_uri' from the discovery document fetched from the .well-known path for the 'issuer_uri'. Currently, RSA and EC asymmetric keys are supported. The JWK must use following format and include only the following fields:: { "keys": [ { "kty": "RSA/EC", "alg": "<algorithm>", "use": "sig", "kid": "<key-id>", "n": "", "e": "", "x": "", "y": "", "crv": "" } ] } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#jwks_json IamWorkloadIdentityPoolProvider#jwks_json}
        '''
        value = IamWorkloadIdentityPoolProviderOidc(
            issuer_uri=issuer_uri,
            allowed_audiences=allowed_audiences,
            jwks_json=jwks_json,
        )

        return typing.cast(None, jsii.invoke(self, "putOidc", [value]))

    @jsii.member(jsii_name="putSaml")
    def put_saml(self, *, idp_metadata_xml: builtins.str) -> None:
        '''
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#idp_metadata_xml IamWorkloadIdentityPoolProvider#idp_metadata_xml}
        '''
        value = IamWorkloadIdentityPoolProviderSaml(idp_metadata_xml=idp_metadata_xml)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#create IamWorkloadIdentityPoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#delete IamWorkloadIdentityPoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#update IamWorkloadIdentityPoolProvider#update}.
        '''
        value = IamWorkloadIdentityPoolProviderTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putX509")
    def put_x509(
        self,
        *,
        trust_store: typing.Union["IamWorkloadIdentityPoolProviderX509TrustStore", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param trust_store: trust_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#trust_store IamWorkloadIdentityPoolProvider#trust_store}
        '''
        value = IamWorkloadIdentityPoolProviderX509(trust_store=trust_store)

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
    def aws(self) -> "IamWorkloadIdentityPoolProviderAwsOutputReference":
        return typing.cast("IamWorkloadIdentityPoolProviderAwsOutputReference", jsii.get(self, "aws"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oidc")
    def oidc(self) -> "IamWorkloadIdentityPoolProviderOidcOutputReference":
        return typing.cast("IamWorkloadIdentityPoolProviderOidcOutputReference", jsii.get(self, "oidc"))

    @builtins.property
    @jsii.member(jsii_name="saml")
    def saml(self) -> "IamWorkloadIdentityPoolProviderSamlOutputReference":
        return typing.cast("IamWorkloadIdentityPoolProviderSamlOutputReference", jsii.get(self, "saml"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IamWorkloadIdentityPoolProviderTimeoutsOutputReference":
        return typing.cast("IamWorkloadIdentityPoolProviderTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="x509")
    def x509(self) -> "IamWorkloadIdentityPoolProviderX509OutputReference":
        return typing.cast("IamWorkloadIdentityPoolProviderX509OutputReference", jsii.get(self, "x509"))

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
    def aws_input(self) -> typing.Optional["IamWorkloadIdentityPoolProviderAws"]:
        return typing.cast(typing.Optional["IamWorkloadIdentityPoolProviderAws"], jsii.get(self, "awsInput"))

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
    def oidc_input(self) -> typing.Optional["IamWorkloadIdentityPoolProviderOidc"]:
        return typing.cast(typing.Optional["IamWorkloadIdentityPoolProviderOidc"], jsii.get(self, "oidcInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="samlInput")
    def saml_input(self) -> typing.Optional["IamWorkloadIdentityPoolProviderSaml"]:
        return typing.cast(typing.Optional["IamWorkloadIdentityPoolProviderSaml"], jsii.get(self, "samlInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamWorkloadIdentityPoolProviderTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamWorkloadIdentityPoolProviderTimeouts"]], jsii.get(self, "timeoutsInput"))

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
    def x509_input(self) -> typing.Optional["IamWorkloadIdentityPoolProviderX509"]:
        return typing.cast(typing.Optional["IamWorkloadIdentityPoolProviderX509"], jsii.get(self, "x509Input"))

    @builtins.property
    @jsii.member(jsii_name="attributeCondition")
    def attribute_condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeCondition"))

    @attribute_condition.setter
    def attribute_condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d741bc633bcc2c9d48868f10e36271ebc7b7fa34d62a6e3e7822b0d94966a56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48a92d7ea5763422fdf3d83f5930c733c8fd015da5ae7ba86a597893cdd562b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab40ba53b65d1f766331ddd71c9762cd05d7b5169cd88de8c726a912ce80aa8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a831b7f09a08bb32468b25bdf8932342c97ce042fd102a5c60a272a05a53e289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b492c90871a5a34d74f3764a63b5cedf70f2986767bc961989454157e3a31c3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6000066ca5d299d75dd04583eff5c40428b9a41516cc5d15d9d0fd39a538fc09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ac109b1f83aea06b977a3c433bff17e2c058d16cb21e5beefcd7d2fb89b0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityPoolId")
    def workload_identity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadIdentityPoolId"))

    @workload_identity_pool_id.setter
    def workload_identity_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a676309ef3df27dfd5eefb03bcd0d38b00fdf7da87fff97187882e3d92c0383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadIdentityPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityPoolProviderId")
    def workload_identity_pool_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadIdentityPoolProviderId"))

    @workload_identity_pool_provider_id.setter
    def workload_identity_pool_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5712b60279b25e6c69d4244fd428280c947e215a5bb4401c4ff96f67cdd1569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadIdentityPoolProviderId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderAws",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId"},
)
class IamWorkloadIdentityPoolProviderAws:
    def __init__(self, *, account_id: builtins.str) -> None:
        '''
        :param account_id: The AWS account ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#account_id IamWorkloadIdentityPoolProvider#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4979cd4f6091031a81af78a77fa7d32d8bc3c87d7085b330cee08dbee8881bd9)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The AWS account ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#account_id IamWorkloadIdentityPoolProvider#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityPoolProviderAws(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkloadIdentityPoolProviderAwsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderAwsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5eb3fbd4f09af276e03c30eb70db44c049b79e9cf7ed9c87823869b3e2a5ec3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ae3ce77f2a33f24c265dfe8e3a93288aba0a3fc7a60129785d20320111e2634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamWorkloadIdentityPoolProviderAws]:
        return typing.cast(typing.Optional[IamWorkloadIdentityPoolProviderAws], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkloadIdentityPoolProviderAws],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903424ed86c6ebd734735a0507606bec6f7d5dc66fe2ebbcdd294175173d31b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderConfig",
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
class IamWorkloadIdentityPoolProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        aws: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderAws, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["IamWorkloadIdentityPoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        saml: typing.Optional[typing.Union["IamWorkloadIdentityPoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["IamWorkloadIdentityPoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        x509: typing.Optional[typing.Union["IamWorkloadIdentityPoolProviderX509", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param workload_identity_pool_id: The ID used for the pool, which is the final component of the pool resource name. This value should be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#workload_identity_pool_id IamWorkloadIdentityPoolProvider#workload_identity_pool_id}
        :param workload_identity_pool_provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#workload_identity_pool_provider_id IamWorkloadIdentityPoolProvider#workload_identity_pool_provider_id}
        :param attribute_condition: `A Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: - 'assertion': JSON representing the authentication credential issued by the provider. - 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. - 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credential are accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#attribute_condition IamWorkloadIdentityPoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: - 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. Cannot exceed 127 characters. - 'google.groups': Groups the external identity belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where '{custom_attribute}' is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workload to Google Cloud resources. For example: - 'google.subject': 'principal://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/subject/{value}' - 'google.groups': 'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/group/{value}' - 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For AWS providers, the following rules apply: - If no attribute mapping is defined, the following default mapping applies:: { "google.subject":"assertion.arn", "attribute.aws_role": "assertion.arn.contains('assumed-role')" " ? assertion.arn.extract('{account_arn}assumed-role/')" " + 'assumed-role/'" " + assertion.arn.extract('assumed-role/{role_name}/')" " : assertion.arn", } - If any custom attribute mappings are defined, they must include a mapping to the 'google.subject' attribute. For OIDC providers, the following rules apply: - Custom attribute mappings must be defined, and must include a mapping to the 'google.subject' attribute. For example, the following maps the 'sub' claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#attribute_mapping IamWorkloadIdentityPoolProvider#attribute_mapping}
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#aws IamWorkloadIdentityPoolProvider#aws}
        :param description: A description for the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#description IamWorkloadIdentityPoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#disabled IamWorkloadIdentityPoolProvider#disabled}
        :param display_name: A display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#display_name IamWorkloadIdentityPoolProvider#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#id IamWorkloadIdentityPoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#oidc IamWorkloadIdentityPoolProvider#oidc}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#project IamWorkloadIdentityPoolProvider#project}.
        :param saml: saml block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#saml IamWorkloadIdentityPoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#timeouts IamWorkloadIdentityPoolProvider#timeouts}
        :param x509: x509 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#x509 IamWorkloadIdentityPoolProvider#x509}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws, dict):
            aws = IamWorkloadIdentityPoolProviderAws(**aws)
        if isinstance(oidc, dict):
            oidc = IamWorkloadIdentityPoolProviderOidc(**oidc)
        if isinstance(saml, dict):
            saml = IamWorkloadIdentityPoolProviderSaml(**saml)
        if isinstance(timeouts, dict):
            timeouts = IamWorkloadIdentityPoolProviderTimeouts(**timeouts)
        if isinstance(x509, dict):
            x509 = IamWorkloadIdentityPoolProviderX509(**x509)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663020bb00aec0566f5081dbaecbcb4e6a4ec53459b6a8e46c99c8aabc4e65fe)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#workload_identity_pool_id IamWorkloadIdentityPoolProvider#workload_identity_pool_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#workload_identity_pool_provider_id IamWorkloadIdentityPoolProvider#workload_identity_pool_provider_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#attribute_condition IamWorkloadIdentityPoolProvider#attribute_condition}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#attribute_mapping IamWorkloadIdentityPoolProvider#attribute_mapping}
        '''
        result = self._values.get("attribute_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def aws(self) -> typing.Optional[IamWorkloadIdentityPoolProviderAws]:
        '''aws block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#aws IamWorkloadIdentityPoolProvider#aws}
        '''
        result = self._values.get("aws")
        return typing.cast(typing.Optional[IamWorkloadIdentityPoolProviderAws], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the provider. Cannot exceed 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#description IamWorkloadIdentityPoolProvider#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#disabled IamWorkloadIdentityPoolProvider#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A display name for the provider. Cannot exceed 32 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#display_name IamWorkloadIdentityPoolProvider#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#id IamWorkloadIdentityPoolProvider#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc(self) -> typing.Optional["IamWorkloadIdentityPoolProviderOidc"]:
        '''oidc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#oidc IamWorkloadIdentityPoolProvider#oidc}
        '''
        result = self._values.get("oidc")
        return typing.cast(typing.Optional["IamWorkloadIdentityPoolProviderOidc"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#project IamWorkloadIdentityPoolProvider#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml(self) -> typing.Optional["IamWorkloadIdentityPoolProviderSaml"]:
        '''saml block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#saml IamWorkloadIdentityPoolProvider#saml}
        '''
        result = self._values.get("saml")
        return typing.cast(typing.Optional["IamWorkloadIdentityPoolProviderSaml"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IamWorkloadIdentityPoolProviderTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#timeouts IamWorkloadIdentityPoolProvider#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IamWorkloadIdentityPoolProviderTimeouts"], result)

    @builtins.property
    def x509(self) -> typing.Optional["IamWorkloadIdentityPoolProviderX509"]:
        '''x509 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#x509 IamWorkloadIdentityPoolProvider#x509}
        '''
        result = self._values.get("x509")
        return typing.cast(typing.Optional["IamWorkloadIdentityPoolProviderX509"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityPoolProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderOidc",
    jsii_struct_bases=[],
    name_mapping={
        "issuer_uri": "issuerUri",
        "allowed_audiences": "allowedAudiences",
        "jwks_json": "jwksJson",
    },
)
class IamWorkloadIdentityPoolProviderOidc:
    def __init__(
        self,
        *,
        issuer_uri: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        jwks_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param issuer_uri: The OIDC issuer URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#issuer_uri IamWorkloadIdentityPoolProvider#issuer_uri}
        :param allowed_audiences: Acceptable values for the 'aud' field (audience) in the OIDC token. Token exchange requests are rejected if the token audience does not match one of the configured values. Each audience may be at most 256 characters. A maximum of 10 audiences may be configured. If this list is empty, the OIDC token audience must be equal to the full canonical resource name of the WorkloadIdentityPoolProvider, with or without the HTTPS prefix. For example:: //iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id> https://iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#allowed_audiences IamWorkloadIdentityPoolProvider#allowed_audiences}
        :param jwks_json: OIDC JWKs in JSON String format. For details on definition of a JWK, see https:tools.ietf.org/html/rfc7517. If not set, then we use the 'jwks_uri' from the discovery document fetched from the .well-known path for the 'issuer_uri'. Currently, RSA and EC asymmetric keys are supported. The JWK must use following format and include only the following fields:: { "keys": [ { "kty": "RSA/EC", "alg": "<algorithm>", "use": "sig", "kid": "<key-id>", "n": "", "e": "", "x": "", "y": "", "crv": "" } ] } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#jwks_json IamWorkloadIdentityPoolProvider#jwks_json}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75c67e9419210f2a6309ead6be1432198fe043d9a145c3674b7a583ee9b8de6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#issuer_uri IamWorkloadIdentityPoolProvider#issuer_uri}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#allowed_audiences IamWorkloadIdentityPoolProvider#allowed_audiences}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#jwks_json IamWorkloadIdentityPoolProvider#jwks_json}
        '''
        result = self._values.get("jwks_json")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityPoolProviderOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkloadIdentityPoolProviderOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4663e11842eeedc3aa0e0234b0cbc66c52c7929dafc8ff3971518aa7087ab808)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd9527eb23c1e166d35631024f4175601fc1e79d4f83a4dc45c9451de2c223d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa41e10f19b25dfa0f6c136f63f9bf1b55a2e98f0d6c93f3331a3d0aaa3dac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwksJson")
    def jwks_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwksJson"))

    @jwks_json.setter
    def jwks_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37294cd90f47ed047a5cda694fb3a52aac623889562471aa4622091f830389db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwksJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamWorkloadIdentityPoolProviderOidc]:
        return typing.cast(typing.Optional[IamWorkloadIdentityPoolProviderOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkloadIdentityPoolProviderOidc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b2865a663129f2fbafaed0573e2264269ad6577a3d0fd6e0687363323758c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderSaml",
    jsii_struct_bases=[],
    name_mapping={"idp_metadata_xml": "idpMetadataXml"},
)
class IamWorkloadIdentityPoolProviderSaml:
    def __init__(self, *, idp_metadata_xml: builtins.str) -> None:
        '''
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#idp_metadata_xml IamWorkloadIdentityPoolProvider#idp_metadata_xml}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e6063a75e7144229ca0d5d4ebab9fdec5772bb34db3396ad4e4ebba5497827)
            check_type(argname="argument idp_metadata_xml", value=idp_metadata_xml, expected_type=type_hints["idp_metadata_xml"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "idp_metadata_xml": idp_metadata_xml,
        }

    @builtins.property
    def idp_metadata_xml(self) -> builtins.str:
        '''SAML Identity provider configuration metadata xml doc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#idp_metadata_xml IamWorkloadIdentityPoolProvider#idp_metadata_xml}
        '''
        result = self._values.get("idp_metadata_xml")
        assert result is not None, "Required property 'idp_metadata_xml' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityPoolProviderSaml(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkloadIdentityPoolProviderSamlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderSamlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17b85c18fc05a5ea59633cda30558d4d2fb428a8b662a905c9172581674e98ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__403d0affbdb746877451a0ff8fdb80f806ed8701739f0f818091c5fb91bc6a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpMetadataXml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamWorkloadIdentityPoolProviderSaml]:
        return typing.cast(typing.Optional[IamWorkloadIdentityPoolProviderSaml], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkloadIdentityPoolProviderSaml],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5460197ae00ff480d5ac24e590876b379818244bd62cb436baf2bea8eadee0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IamWorkloadIdentityPoolProviderTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#create IamWorkloadIdentityPoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#delete IamWorkloadIdentityPoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#update IamWorkloadIdentityPoolProvider#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcab517ef0655435794da3d2a38265223833f227dd078d5d0f873f197946e2a7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#create IamWorkloadIdentityPoolProvider#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#delete IamWorkloadIdentityPoolProvider#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#update IamWorkloadIdentityPoolProvider#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityPoolProviderTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkloadIdentityPoolProviderTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c3b919303a674b0fdeda64b543921f4f3be8d9bdfd028af5f41157be1e299c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a596ff11514e906d0059c9dd487636e050b2996602521ae7abc69b07a264c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03370407dd498e1a89fddb2871b8961db2840f47ab2565c0cc7bb4daada4e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd9f06eee9d0e2129676da6d79be894d1908f0c07e748818d3501e40a79f2d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ad6956a36563d813398b8a512a1568da097b870be4285b1e2f16f939a990eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509",
    jsii_struct_bases=[],
    name_mapping={"trust_store": "trustStore"},
)
class IamWorkloadIdentityPoolProviderX509:
    def __init__(
        self,
        *,
        trust_store: typing.Union["IamWorkloadIdentityPoolProviderX509TrustStore", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param trust_store: trust_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#trust_store IamWorkloadIdentityPoolProvider#trust_store}
        '''
        if isinstance(trust_store, dict):
            trust_store = IamWorkloadIdentityPoolProviderX509TrustStore(**trust_store)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ed2c77567f57df9da189652803d404ea45dd0536771d069a2e024692fe18b5)
            check_type(argname="argument trust_store", value=trust_store, expected_type=type_hints["trust_store"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trust_store": trust_store,
        }

    @builtins.property
    def trust_store(self) -> "IamWorkloadIdentityPoolProviderX509TrustStore":
        '''trust_store block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#trust_store IamWorkloadIdentityPoolProvider#trust_store}
        '''
        result = self._values.get("trust_store")
        assert result is not None, "Required property 'trust_store' is missing"
        return typing.cast("IamWorkloadIdentityPoolProviderX509TrustStore", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityPoolProviderX509(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkloadIdentityPoolProviderX509OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33d40b3e40b914a8ffd2ae2632aa86b970d01b882d01290da31a466cc549f032)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTrustStore")
    def put_trust_store(
        self,
        *,
        trust_anchors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors", typing.Dict[builtins.str, typing.Any]]]],
        intermediate_cas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param trust_anchors: trust_anchors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#trust_anchors IamWorkloadIdentityPoolProvider#trust_anchors}
        :param intermediate_cas: intermediate_cas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#intermediate_cas IamWorkloadIdentityPoolProvider#intermediate_cas}
        '''
        value = IamWorkloadIdentityPoolProviderX509TrustStore(
            trust_anchors=trust_anchors, intermediate_cas=intermediate_cas
        )

        return typing.cast(None, jsii.invoke(self, "putTrustStore", [value]))

    @builtins.property
    @jsii.member(jsii_name="trustStore")
    def trust_store(
        self,
    ) -> "IamWorkloadIdentityPoolProviderX509TrustStoreOutputReference":
        return typing.cast("IamWorkloadIdentityPoolProviderX509TrustStoreOutputReference", jsii.get(self, "trustStore"))

    @builtins.property
    @jsii.member(jsii_name="trustStoreInput")
    def trust_store_input(
        self,
    ) -> typing.Optional["IamWorkloadIdentityPoolProviderX509TrustStore"]:
        return typing.cast(typing.Optional["IamWorkloadIdentityPoolProviderX509TrustStore"], jsii.get(self, "trustStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamWorkloadIdentityPoolProviderX509]:
        return typing.cast(typing.Optional[IamWorkloadIdentityPoolProviderX509], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkloadIdentityPoolProviderX509],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056ca26155099b08164c3f012866518252e0bd50037831df33cb0d3b53bca872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509TrustStore",
    jsii_struct_bases=[],
    name_mapping={
        "trust_anchors": "trustAnchors",
        "intermediate_cas": "intermediateCas",
    },
)
class IamWorkloadIdentityPoolProviderX509TrustStore:
    def __init__(
        self,
        *,
        trust_anchors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors", typing.Dict[builtins.str, typing.Any]]]],
        intermediate_cas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param trust_anchors: trust_anchors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#trust_anchors IamWorkloadIdentityPoolProvider#trust_anchors}
        :param intermediate_cas: intermediate_cas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#intermediate_cas IamWorkloadIdentityPoolProvider#intermediate_cas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef1a9b8ac6ce0ef610d7cc4e040048cbb0436f446a7d62ddab0ce01875e1e00)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors"]]:
        '''trust_anchors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#trust_anchors IamWorkloadIdentityPoolProvider#trust_anchors}
        '''
        result = self._values.get("trust_anchors")
        assert result is not None, "Required property 'trust_anchors' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors"]], result)

    @builtins.property
    def intermediate_cas(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas"]]]:
        '''intermediate_cas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#intermediate_cas IamWorkloadIdentityPoolProvider#intermediate_cas}
        '''
        result = self._values.get("intermediate_cas")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityPoolProviderX509TrustStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas",
    jsii_struct_bases=[],
    name_mapping={"pem_certificate": "pemCertificate"},
)
class IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas:
    def __init__(
        self,
        *,
        pem_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pem_certificate: PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#pem_certificate IamWorkloadIdentityPoolProvider#pem_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefb06850c0f05459ccbc3d953ffdbe055639106a73df1b48ec3af993ab50ec7)
            check_type(argname="argument pem_certificate", value=pem_certificate, expected_type=type_hints["pem_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pem_certificate is not None:
            self._values["pem_certificate"] = pem_certificate

    @builtins.property
    def pem_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#pem_certificate IamWorkloadIdentityPoolProvider#pem_certificate}
        '''
        result = self._values.get("pem_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2adb3db53f5ab3a3eb952d4752d25dc446251e9874347bbbf58de643ca3a758a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f727b70aa0587df2381459961df5bcfeec3a7324a139b9af6cec189198f153)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf03a37c07bea0a5a99b3fdc7374eb07eef6a4f00f391d50af5b0ede57da533f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__674de377be71efc47c495bd6ed2682830b93150305d39ba4c2b3f0fe513fc661)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a137cf550329be3ad2c454ac1d0c755084a709818b07279329863b6409606f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc850fcd40e92136688c42fcfdc61453b901a5fd30825fa38675c03c2e042272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbc50c6db44d195212dbd86b333e124dbbbfe15a315946d8fec30d23340f465e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8707ba78034ce13972b5075ccb7e6ebfd45fcfed0c1478af34acabd4372ae29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b6b4414f356c4dc72c250fda68ad2b3fb42d1a9789705748a1cb1f8e0be9cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IamWorkloadIdentityPoolProviderX509TrustStoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509TrustStoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd50859c93d13da1648d16adad6fcdb785c2e2eda16b70335962d7a0902a92a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIntermediateCas")
    def put_intermediate_cas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743367f05fd70c4f988696d385bfb50cc9fcfe3f9e178003a57440b6dc768b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIntermediateCas", [value]))

    @jsii.member(jsii_name="putTrustAnchors")
    def put_trust_anchors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab2889428ac2c9ddb6a550a287c50dab83fdd70b954b2d785587680d598c4f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrustAnchors", [value]))

    @jsii.member(jsii_name="resetIntermediateCas")
    def reset_intermediate_cas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntermediateCas", []))

    @builtins.property
    @jsii.member(jsii_name="intermediateCas")
    def intermediate_cas(
        self,
    ) -> IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList:
        return typing.cast(IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList, jsii.get(self, "intermediateCas"))

    @builtins.property
    @jsii.member(jsii_name="trustAnchors")
    def trust_anchors(
        self,
    ) -> "IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList":
        return typing.cast("IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList", jsii.get(self, "trustAnchors"))

    @builtins.property
    @jsii.member(jsii_name="intermediateCasInput")
    def intermediate_cas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]], jsii.get(self, "intermediateCasInput"))

    @builtins.property
    @jsii.member(jsii_name="trustAnchorsInput")
    def trust_anchors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors"]]], jsii.get(self, "trustAnchorsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IamWorkloadIdentityPoolProviderX509TrustStore]:
        return typing.cast(typing.Optional[IamWorkloadIdentityPoolProviderX509TrustStore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkloadIdentityPoolProviderX509TrustStore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f014a626bce9090a93e51c998355a4711d8a81254f977ed8eaea45a378f92299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors",
    jsii_struct_bases=[],
    name_mapping={"pem_certificate": "pemCertificate"},
)
class IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors:
    def __init__(
        self,
        *,
        pem_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pem_certificate: PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#pem_certificate IamWorkloadIdentityPoolProvider#pem_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7d37f542973873401ea42b91a5850ccf3453f25003ace21da354061952f6f2)
            check_type(argname="argument pem_certificate", value=pem_certificate, expected_type=type_hints["pem_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pem_certificate is not None:
            self._values["pem_certificate"] = pem_certificate

    @builtins.property
    def pem_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_workload_identity_pool_provider#pem_certificate IamWorkloadIdentityPoolProvider#pem_certificate}
        '''
        result = self._values.get("pem_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54d9050d02e37e942f8b9d714122557fd85ccea63ffb6a93db10f727da93565c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b2db537f01a0bf57888bebaccae15e2eb3c0c66a99144a1dfb06a2f53b123c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975f55a9e26d685af9471f37f3e3c3e7a3f934e854f524f2792c5ac853ab15ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51e26d429160fc4f409c381084ec604dd01e29d016199ad4345ebf077be07f3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e8cf3ee127b332a49fc04c28eb214d1f72bd460a640cd57edac7b366fb9ac25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb95affa6a9cebafa26a2971ae884574d04c752c58b9ce6944fe7c67e5a98fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkloadIdentityPoolProvider.IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9fbf07c8c814da749f40330a91ae432619f8deaff0254078a9e749e24c565b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f37d965c38eed29b493a3c4ae6b7eb2f5fee0df4e6539e31b63a7efb8bc22a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dcbadefde1a1f00069390a90ce13eb287acd1fb8122463338463ddd0471ca0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IamWorkloadIdentityPoolProvider",
    "IamWorkloadIdentityPoolProviderAws",
    "IamWorkloadIdentityPoolProviderAwsOutputReference",
    "IamWorkloadIdentityPoolProviderConfig",
    "IamWorkloadIdentityPoolProviderOidc",
    "IamWorkloadIdentityPoolProviderOidcOutputReference",
    "IamWorkloadIdentityPoolProviderSaml",
    "IamWorkloadIdentityPoolProviderSamlOutputReference",
    "IamWorkloadIdentityPoolProviderTimeouts",
    "IamWorkloadIdentityPoolProviderTimeoutsOutputReference",
    "IamWorkloadIdentityPoolProviderX509",
    "IamWorkloadIdentityPoolProviderX509OutputReference",
    "IamWorkloadIdentityPoolProviderX509TrustStore",
    "IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas",
    "IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasList",
    "IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCasOutputReference",
    "IamWorkloadIdentityPoolProviderX509TrustStoreOutputReference",
    "IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors",
    "IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsList",
    "IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchorsOutputReference",
]

publication.publish()

def _typecheckingstub__f7db34fdba41bfb946679b6b528f9e7dedcd81f06705360bdced99e89c7d3ddd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    workload_identity_pool_id: builtins.str,
    workload_identity_pool_provider_id: builtins.str,
    attribute_condition: typing.Optional[builtins.str] = None,
    attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    aws: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderAws, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    saml: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    x509: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderX509, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9ee75e96605d360bd556b51979775e15d1a1c5df1329c391e10c47a7e6acab62(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d741bc633bcc2c9d48868f10e36271ebc7b7fa34d62a6e3e7822b0d94966a56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a92d7ea5763422fdf3d83f5930c733c8fd015da5ae7ba86a597893cdd562b4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab40ba53b65d1f766331ddd71c9762cd05d7b5169cd88de8c726a912ce80aa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a831b7f09a08bb32468b25bdf8932342c97ce042fd102a5c60a272a05a53e289(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b492c90871a5a34d74f3764a63b5cedf70f2986767bc961989454157e3a31c3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6000066ca5d299d75dd04583eff5c40428b9a41516cc5d15d9d0fd39a538fc09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ac109b1f83aea06b977a3c433bff17e2c058d16cb21e5beefcd7d2fb89b0d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a676309ef3df27dfd5eefb03bcd0d38b00fdf7da87fff97187882e3d92c0383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5712b60279b25e6c69d4244fd428280c947e215a5bb4401c4ff96f67cdd1569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4979cd4f6091031a81af78a77fa7d32d8bc3c87d7085b330cee08dbee8881bd9(
    *,
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5eb3fbd4f09af276e03c30eb70db44c049b79e9cf7ed9c87823869b3e2a5ec3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae3ce77f2a33f24c265dfe8e3a93288aba0a3fc7a60129785d20320111e2634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903424ed86c6ebd734735a0507606bec6f7d5dc66fe2ebbcdd294175173d31b1(
    value: typing.Optional[IamWorkloadIdentityPoolProviderAws],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663020bb00aec0566f5081dbaecbcb4e6a4ec53459b6a8e46c99c8aabc4e65fe(
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
    aws: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderAws, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    saml: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    x509: typing.Optional[typing.Union[IamWorkloadIdentityPoolProviderX509, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75c67e9419210f2a6309ead6be1432198fe043d9a145c3674b7a583ee9b8de6(
    *,
    issuer_uri: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    jwks_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4663e11842eeedc3aa0e0234b0cbc66c52c7929dafc8ff3971518aa7087ab808(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9527eb23c1e166d35631024f4175601fc1e79d4f83a4dc45c9451de2c223d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa41e10f19b25dfa0f6c136f63f9bf1b55a2e98f0d6c93f3331a3d0aaa3dac7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37294cd90f47ed047a5cda694fb3a52aac623889562471aa4622091f830389db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b2865a663129f2fbafaed0573e2264269ad6577a3d0fd6e0687363323758c0(
    value: typing.Optional[IamWorkloadIdentityPoolProviderOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e6063a75e7144229ca0d5d4ebab9fdec5772bb34db3396ad4e4ebba5497827(
    *,
    idp_metadata_xml: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b85c18fc05a5ea59633cda30558d4d2fb428a8b662a905c9172581674e98ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403d0affbdb746877451a0ff8fdb80f806ed8701739f0f818091c5fb91bc6a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5460197ae00ff480d5ac24e590876b379818244bd62cb436baf2bea8eadee0f(
    value: typing.Optional[IamWorkloadIdentityPoolProviderSaml],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcab517ef0655435794da3d2a38265223833f227dd078d5d0f873f197946e2a7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3b919303a674b0fdeda64b543921f4f3be8d9bdfd028af5f41157be1e299c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a596ff11514e906d0059c9dd487636e050b2996602521ae7abc69b07a264c42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03370407dd498e1a89fddb2871b8961db2840f47ab2565c0cc7bb4daada4e72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd9f06eee9d0e2129676da6d79be894d1908f0c07e748818d3501e40a79f2d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ad6956a36563d813398b8a512a1568da097b870be4285b1e2f16f939a990eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ed2c77567f57df9da189652803d404ea45dd0536771d069a2e024692fe18b5(
    *,
    trust_store: typing.Union[IamWorkloadIdentityPoolProviderX509TrustStore, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d40b3e40b914a8ffd2ae2632aa86b970d01b882d01290da31a466cc549f032(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056ca26155099b08164c3f012866518252e0bd50037831df33cb0d3b53bca872(
    value: typing.Optional[IamWorkloadIdentityPoolProviderX509],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef1a9b8ac6ce0ef610d7cc4e040048cbb0436f446a7d62ddab0ce01875e1e00(
    *,
    trust_anchors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors, typing.Dict[builtins.str, typing.Any]]]],
    intermediate_cas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefb06850c0f05459ccbc3d953ffdbe055639106a73df1b48ec3af993ab50ec7(
    *,
    pem_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2adb3db53f5ab3a3eb952d4752d25dc446251e9874347bbbf58de643ca3a758a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f727b70aa0587df2381459961df5bcfeec3a7324a139b9af6cec189198f153(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf03a37c07bea0a5a99b3fdc7374eb07eef6a4f00f391d50af5b0ede57da533f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674de377be71efc47c495bd6ed2682830b93150305d39ba4c2b3f0fe513fc661(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a137cf550329be3ad2c454ac1d0c755084a709818b07279329863b6409606f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc850fcd40e92136688c42fcfdc61453b901a5fd30825fa38675c03c2e042272(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc50c6db44d195212dbd86b333e124dbbbfe15a315946d8fec30d23340f465e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8707ba78034ce13972b5075ccb7e6ebfd45fcfed0c1478af34acabd4372ae29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b6b4414f356c4dc72c250fda68ad2b3fb42d1a9789705748a1cb1f8e0be9cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd50859c93d13da1648d16adad6fcdb785c2e2eda16b70335962d7a0902a92a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743367f05fd70c4f988696d385bfb50cc9fcfe3f9e178003a57440b6dc768b74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IamWorkloadIdentityPoolProviderX509TrustStoreIntermediateCas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab2889428ac2c9ddb6a550a287c50dab83fdd70b954b2d785587680d598c4f5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f014a626bce9090a93e51c998355a4711d8a81254f977ed8eaea45a378f92299(
    value: typing.Optional[IamWorkloadIdentityPoolProviderX509TrustStore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7d37f542973873401ea42b91a5850ccf3453f25003ace21da354061952f6f2(
    *,
    pem_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d9050d02e37e942f8b9d714122557fd85ccea63ffb6a93db10f727da93565c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b2db537f01a0bf57888bebaccae15e2eb3c0c66a99144a1dfb06a2f53b123c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975f55a9e26d685af9471f37f3e3c3e7a3f934e854f524f2792c5ac853ab15ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e26d429160fc4f409c381084ec604dd01e29d016199ad4345ebf077be07f3b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8cf3ee127b332a49fc04c28eb214d1f72bd460a640cd57edac7b366fb9ac25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb95affa6a9cebafa26a2971ae884574d04c752c58b9ce6944fe7c67e5a98fb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9fbf07c8c814da749f40330a91ae432619f8deaff0254078a9e749e24c565b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f37d965c38eed29b493a3c4ae6b7eb2f5fee0df4e6539e31b63a7efb8bc22a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dcbadefde1a1f00069390a90ce13eb287acd1fb8122463338463ddd0471ca0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamWorkloadIdentityPoolProviderX509TrustStoreTrustAnchors]],
) -> None:
    """Type checking stubs"""
    pass
