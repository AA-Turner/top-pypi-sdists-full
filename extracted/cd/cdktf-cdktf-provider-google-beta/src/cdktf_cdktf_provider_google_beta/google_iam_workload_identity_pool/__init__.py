r'''
# `google_iam_workload_identity_pool`

Refer to the Terraform Registry for docs: [`google_iam_workload_identity_pool`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool).
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


class GoogleIamWorkloadIdentityPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool google_iam_workload_identity_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        workload_identity_pool_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inline_certificate_issuance_config: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inline_trust_config: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolInlineTrustConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool google_iam_workload_identity_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param workload_identity_pool_id: The ID to use for the pool, which becomes the final component of the resource name. This value should be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#workload_identity_pool_id GoogleIamWorkloadIdentityPool#workload_identity_pool_id}
        :param description: A description of the pool. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#description GoogleIamWorkloadIdentityPool#description}
        :param disabled: Whether the pool is disabled. You cannot use a disabled pool to exchange tokens, or use existing tokens to access resources. If the pool is re-enabled, existing tokens grant access again. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#disabled GoogleIamWorkloadIdentityPool#disabled}
        :param display_name: A display name for the pool. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#display_name GoogleIamWorkloadIdentityPool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#id GoogleIamWorkloadIdentityPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inline_certificate_issuance_config: inline_certificate_issuance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#inline_certificate_issuance_config GoogleIamWorkloadIdentityPool#inline_certificate_issuance_config}
        :param inline_trust_config: inline_trust_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#inline_trust_config GoogleIamWorkloadIdentityPool#inline_trust_config}
        :param mode: The mode for the pool is operating in. Pools with an unspecified mode will operate as if they are in 'FEDERATION_ONLY' mode. ~> **Note** This field cannot be changed after the Workload Identity Pool is created. While 'terraform plan' may show an update if you change this field's value, 'terraform apply' **will fail with an API error** (such as 'Error 400: Attempted to update an immutable field.'). To specify a different 'mode', please create a new Workload Identity Pool resource. - 'FEDERATION_ONLY': Pools can only be used for federating external workload identities into Google Cloud. Unless otherwise noted, no structure or format constraints are applied to workload identities in a 'FEDERATION_ONLY' mode pool, and you may not create any resources within the pool besides providers. - 'TRUST_DOMAIN': Pools can be used to assign identities to Google Cloud workloads. All identities within a 'TRUST_DOMAIN' mode pool must consist of a single namespace and individual workload identifier. The subject identifier for all identities must conform to the following format: 'ns//sa/<workload_identifier>'. 'google_iam_workload_identity_pool_provider's cannot be created within 'TRUST_DOMAIN' mode pools. Possible values: ["FEDERATION_ONLY", "TRUST_DOMAIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#mode GoogleIamWorkloadIdentityPool#mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#project GoogleIamWorkloadIdentityPool#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#timeouts GoogleIamWorkloadIdentityPool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55028bac2eaa1ac69f18598fea073d82f39175d1f38dda252dda9ba6a3598746)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIamWorkloadIdentityPoolConfig(
            workload_identity_pool_id=workload_identity_pool_id,
            description=description,
            disabled=disabled,
            display_name=display_name,
            id=id,
            inline_certificate_issuance_config=inline_certificate_issuance_config,
            inline_trust_config=inline_trust_config,
            mode=mode,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleIamWorkloadIdentityPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleIamWorkloadIdentityPool to import.
        :param import_from_id: The id of the existing GoogleIamWorkloadIdentityPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleIamWorkloadIdentityPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd9f99453b5599dda3e3696d4559aaefbeb624ed16061962a34dfc3ec7b3435)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInlineCertificateIssuanceConfig")
    def put_inline_certificate_issuance_config(
        self,
        *,
        ca_pools: typing.Mapping[builtins.str, builtins.str],
        key_algorithm: typing.Optional[builtins.str] = None,
        lifetime: typing.Optional[builtins.str] = None,
        rotation_window_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param ca_pools: A required mapping of a cloud region to the CA pool resource located in that region used for certificate issuance, adhering to these constraints: * **Key format:** A supported cloud region name equivalent to the location identifier in the corresponding map entry's value. - **Value format:** A valid CA pool resource path format like: 'projects/{project}/locations/{location}/caPools/{ca_pool}' - **Region Matching:** Workloads are ONLY issued certificates from CA pools within the same region. Also the CA pool region (in value) must match the workload's region (key). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#ca_pools GoogleIamWorkloadIdentityPool#ca_pools}
        :param key_algorithm: Key algorithm to use when generating the key pair. This key pair will be used to create the certificate. If unspecified, this will default to 'ECDSA_P256'. - 'RSA_2048': Specifies RSA with a 2048-bit modulus. - 'RSA_3072': Specifies RSA with a 3072-bit modulus. - 'RSA_4096': Specifies RSA with a 4096-bit modulus. - 'ECDSA_P256': Specifies ECDSA with curve P256. - 'ECDSA_P384': Specifies ECDSA with curve P384. Possible values: ["RSA_2048", "RSA_3072", "RSA_4096", "ECDSA_P256", "ECDSA_P384"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#key_algorithm GoogleIamWorkloadIdentityPool#key_algorithm}
        :param lifetime: Lifetime of the workload certificates issued by the CA pool in seconds. Must be between '86400s' (24 hours) to '2592000s' (30 days), ends in the suffix "'s'" (indicating seconds) and is preceded by the number of seconds. If unspecified, this will be defaulted to '86400s' (24 hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#lifetime GoogleIamWorkloadIdentityPool#lifetime}
        :param rotation_window_percentage: Rotation window percentage indicating when certificate rotation should be initiated based on remaining lifetime. Must be between '50' - '80'. If unspecified, this will be defaulted to '50'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#rotation_window_percentage GoogleIamWorkloadIdentityPool#rotation_window_percentage}
        '''
        value = GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig(
            ca_pools=ca_pools,
            key_algorithm=key_algorithm,
            lifetime=lifetime,
            rotation_window_percentage=rotation_window_percentage,
        )

        return typing.cast(None, jsii.invoke(self, "putInlineCertificateIssuanceConfig", [value]))

    @jsii.member(jsii_name="putInlineTrustConfig")
    def put_inline_trust_config(
        self,
        *,
        additional_trust_bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param additional_trust_bundles: additional_trust_bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#additional_trust_bundles GoogleIamWorkloadIdentityPool#additional_trust_bundles}
        '''
        value = GoogleIamWorkloadIdentityPoolInlineTrustConfig(
            additional_trust_bundles=additional_trust_bundles
        )

        return typing.cast(None, jsii.invoke(self, "putInlineTrustConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#create GoogleIamWorkloadIdentityPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#delete GoogleIamWorkloadIdentityPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#update GoogleIamWorkloadIdentityPool#update}.
        '''
        value = GoogleIamWorkloadIdentityPoolTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

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

    @jsii.member(jsii_name="resetInlineCertificateIssuanceConfig")
    def reset_inline_certificate_issuance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineCertificateIssuanceConfig", []))

    @jsii.member(jsii_name="resetInlineTrustConfig")
    def reset_inline_trust_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineTrustConfig", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="inlineCertificateIssuanceConfig")
    def inline_certificate_issuance_config(
        self,
    ) -> "GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfigOutputReference":
        return typing.cast("GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfigOutputReference", jsii.get(self, "inlineCertificateIssuanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="inlineTrustConfig")
    def inline_trust_config(
        self,
    ) -> "GoogleIamWorkloadIdentityPoolInlineTrustConfigOutputReference":
        return typing.cast("GoogleIamWorkloadIdentityPoolInlineTrustConfigOutputReference", jsii.get(self, "inlineTrustConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleIamWorkloadIdentityPoolTimeoutsOutputReference":
        return typing.cast("GoogleIamWorkloadIdentityPoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="inlineCertificateIssuanceConfigInput")
    def inline_certificate_issuance_config_input(
        self,
    ) -> typing.Optional["GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig"]:
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig"], jsii.get(self, "inlineCertificateIssuanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="inlineTrustConfigInput")
    def inline_trust_config_input(
        self,
    ) -> typing.Optional["GoogleIamWorkloadIdentityPoolInlineTrustConfig"]:
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolInlineTrustConfig"], jsii.get(self, "inlineTrustConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIamWorkloadIdentityPoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIamWorkloadIdentityPoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityPoolIdInput")
    def workload_identity_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadIdentityPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c180a54bec5c2a0abf33dd302bbed2fdbec4661c3bcf73a59cb4a89a41153e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b0287fd61c0b7a11fdd7333722a08534af7270fe22f96a46468189009e743c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28cf04ef905d8d126af0a21d3b6a971af86bd3cb8223410be6bbdbb637c7e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54291f5c28bbc984b97715fa144937ab29b180570530632f551e3321c3a9581f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4984fc855f84364f1bb9f6435ee17af8c85b875d81515451843cef6f934230c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de119945357ed61ef6598d006a1a8cbc21348108bd9065d5f7e6b0b98c85395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityPoolId")
    def workload_identity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadIdentityPoolId"))

    @workload_identity_pool_id.setter
    def workload_identity_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928714b72b77ec5acab275d8ec4ce5252585997e1f0a965e161d7cd046346cf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadIdentityPoolId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolConfig",
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
        "description": "description",
        "disabled": "disabled",
        "display_name": "displayName",
        "id": "id",
        "inline_certificate_issuance_config": "inlineCertificateIssuanceConfig",
        "inline_trust_config": "inlineTrustConfig",
        "mode": "mode",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleIamWorkloadIdentityPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inline_certificate_issuance_config: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inline_trust_config: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolInlineTrustConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIamWorkloadIdentityPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param workload_identity_pool_id: The ID to use for the pool, which becomes the final component of the resource name. This value should be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#workload_identity_pool_id GoogleIamWorkloadIdentityPool#workload_identity_pool_id}
        :param description: A description of the pool. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#description GoogleIamWorkloadIdentityPool#description}
        :param disabled: Whether the pool is disabled. You cannot use a disabled pool to exchange tokens, or use existing tokens to access resources. If the pool is re-enabled, existing tokens grant access again. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#disabled GoogleIamWorkloadIdentityPool#disabled}
        :param display_name: A display name for the pool. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#display_name GoogleIamWorkloadIdentityPool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#id GoogleIamWorkloadIdentityPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inline_certificate_issuance_config: inline_certificate_issuance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#inline_certificate_issuance_config GoogleIamWorkloadIdentityPool#inline_certificate_issuance_config}
        :param inline_trust_config: inline_trust_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#inline_trust_config GoogleIamWorkloadIdentityPool#inline_trust_config}
        :param mode: The mode for the pool is operating in. Pools with an unspecified mode will operate as if they are in 'FEDERATION_ONLY' mode. ~> **Note** This field cannot be changed after the Workload Identity Pool is created. While 'terraform plan' may show an update if you change this field's value, 'terraform apply' **will fail with an API error** (such as 'Error 400: Attempted to update an immutable field.'). To specify a different 'mode', please create a new Workload Identity Pool resource. - 'FEDERATION_ONLY': Pools can only be used for federating external workload identities into Google Cloud. Unless otherwise noted, no structure or format constraints are applied to workload identities in a 'FEDERATION_ONLY' mode pool, and you may not create any resources within the pool besides providers. - 'TRUST_DOMAIN': Pools can be used to assign identities to Google Cloud workloads. All identities within a 'TRUST_DOMAIN' mode pool must consist of a single namespace and individual workload identifier. The subject identifier for all identities must conform to the following format: 'ns//sa/<workload_identifier>'. 'google_iam_workload_identity_pool_provider's cannot be created within 'TRUST_DOMAIN' mode pools. Possible values: ["FEDERATION_ONLY", "TRUST_DOMAIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#mode GoogleIamWorkloadIdentityPool#mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#project GoogleIamWorkloadIdentityPool#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#timeouts GoogleIamWorkloadIdentityPool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(inline_certificate_issuance_config, dict):
            inline_certificate_issuance_config = GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig(**inline_certificate_issuance_config)
        if isinstance(inline_trust_config, dict):
            inline_trust_config = GoogleIamWorkloadIdentityPoolInlineTrustConfig(**inline_trust_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleIamWorkloadIdentityPoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b477e3c83d9b24d62c9dd23b368dd8ab0e5421779866a76c16180040a1cbe92)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument workload_identity_pool_id", value=workload_identity_pool_id, expected_type=type_hints["workload_identity_pool_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inline_certificate_issuance_config", value=inline_certificate_issuance_config, expected_type=type_hints["inline_certificate_issuance_config"])
            check_type(argname="argument inline_trust_config", value=inline_trust_config, expected_type=type_hints["inline_trust_config"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "workload_identity_pool_id": workload_identity_pool_id,
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
        if disabled is not None:
            self._values["disabled"] = disabled
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if inline_certificate_issuance_config is not None:
            self._values["inline_certificate_issuance_config"] = inline_certificate_issuance_config
        if inline_trust_config is not None:
            self._values["inline_trust_config"] = inline_trust_config
        if mode is not None:
            self._values["mode"] = mode
        if project is not None:
            self._values["project"] = project
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
    def workload_identity_pool_id(self) -> builtins.str:
        '''The ID to use for the pool, which becomes the final component of the resource name.

        This
        value should be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix
        'gcp-' is reserved for use by Google, and may not be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#workload_identity_pool_id GoogleIamWorkloadIdentityPool#workload_identity_pool_id}
        '''
        result = self._values.get("workload_identity_pool_id")
        assert result is not None, "Required property 'workload_identity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the pool. Cannot exceed 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#description GoogleIamWorkloadIdentityPool#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the pool is disabled.

        You cannot use a disabled pool to exchange tokens, or use
        existing tokens to access resources. If the pool is re-enabled, existing tokens grant
        access again.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#disabled GoogleIamWorkloadIdentityPool#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A display name for the pool. Cannot exceed 32 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#display_name GoogleIamWorkloadIdentityPool#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#id GoogleIamWorkloadIdentityPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_certificate_issuance_config(
        self,
    ) -> typing.Optional["GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig"]:
        '''inline_certificate_issuance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#inline_certificate_issuance_config GoogleIamWorkloadIdentityPool#inline_certificate_issuance_config}
        '''
        result = self._values.get("inline_certificate_issuance_config")
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig"], result)

    @builtins.property
    def inline_trust_config(
        self,
    ) -> typing.Optional["GoogleIamWorkloadIdentityPoolInlineTrustConfig"]:
        '''inline_trust_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#inline_trust_config GoogleIamWorkloadIdentityPool#inline_trust_config}
        '''
        result = self._values.get("inline_trust_config")
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolInlineTrustConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode for the pool is operating in.

        Pools with an unspecified mode will operate as if they
        are in 'FEDERATION_ONLY' mode.

        ~> **Note** This field cannot be changed after the Workload Identity Pool is created. While
        'terraform plan' may show an update if you change this field's value, 'terraform apply'
        **will fail with an API error** (such as 'Error 400: Attempted to update an immutable field.').
        To specify a different 'mode', please create a new Workload Identity Pool resource.

        - 'FEDERATION_ONLY': Pools can only be used for federating external workload identities into
          Google Cloud. Unless otherwise noted, no structure or format constraints are applied to
          workload identities in a 'FEDERATION_ONLY' mode pool, and you may not create any resources
          within the pool besides providers.
        - 'TRUST_DOMAIN': Pools can be used to assign identities to Google Cloud workloads. All
          identities within a 'TRUST_DOMAIN' mode pool must consist of a single namespace and individual
          workload identifier. The subject identifier for all identities must conform to the following
          format: 'ns//sa/<workload_identifier>'.
          'google_iam_workload_identity_pool_provider's cannot be created within 'TRUST_DOMAIN'
          mode pools. Possible values: ["FEDERATION_ONLY", "TRUST_DOMAIN"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#mode GoogleIamWorkloadIdentityPool#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#project GoogleIamWorkloadIdentityPool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleIamWorkloadIdentityPoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#timeouts GoogleIamWorkloadIdentityPool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIamWorkloadIdentityPoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "ca_pools": "caPools",
        "key_algorithm": "keyAlgorithm",
        "lifetime": "lifetime",
        "rotation_window_percentage": "rotationWindowPercentage",
    },
)
class GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig:
    def __init__(
        self,
        *,
        ca_pools: typing.Mapping[builtins.str, builtins.str],
        key_algorithm: typing.Optional[builtins.str] = None,
        lifetime: typing.Optional[builtins.str] = None,
        rotation_window_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param ca_pools: A required mapping of a cloud region to the CA pool resource located in that region used for certificate issuance, adhering to these constraints: * **Key format:** A supported cloud region name equivalent to the location identifier in the corresponding map entry's value. - **Value format:** A valid CA pool resource path format like: 'projects/{project}/locations/{location}/caPools/{ca_pool}' - **Region Matching:** Workloads are ONLY issued certificates from CA pools within the same region. Also the CA pool region (in value) must match the workload's region (key). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#ca_pools GoogleIamWorkloadIdentityPool#ca_pools}
        :param key_algorithm: Key algorithm to use when generating the key pair. This key pair will be used to create the certificate. If unspecified, this will default to 'ECDSA_P256'. - 'RSA_2048': Specifies RSA with a 2048-bit modulus. - 'RSA_3072': Specifies RSA with a 3072-bit modulus. - 'RSA_4096': Specifies RSA with a 4096-bit modulus. - 'ECDSA_P256': Specifies ECDSA with curve P256. - 'ECDSA_P384': Specifies ECDSA with curve P384. Possible values: ["RSA_2048", "RSA_3072", "RSA_4096", "ECDSA_P256", "ECDSA_P384"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#key_algorithm GoogleIamWorkloadIdentityPool#key_algorithm}
        :param lifetime: Lifetime of the workload certificates issued by the CA pool in seconds. Must be between '86400s' (24 hours) to '2592000s' (30 days), ends in the suffix "'s'" (indicating seconds) and is preceded by the number of seconds. If unspecified, this will be defaulted to '86400s' (24 hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#lifetime GoogleIamWorkloadIdentityPool#lifetime}
        :param rotation_window_percentage: Rotation window percentage indicating when certificate rotation should be initiated based on remaining lifetime. Must be between '50' - '80'. If unspecified, this will be defaulted to '50'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#rotation_window_percentage GoogleIamWorkloadIdentityPool#rotation_window_percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b4317f5a615969fff2860f547cfe7191e9875f13bf46e648c445d24eea9a7c)
            check_type(argname="argument ca_pools", value=ca_pools, expected_type=type_hints["ca_pools"])
            check_type(argname="argument key_algorithm", value=key_algorithm, expected_type=type_hints["key_algorithm"])
            check_type(argname="argument lifetime", value=lifetime, expected_type=type_hints["lifetime"])
            check_type(argname="argument rotation_window_percentage", value=rotation_window_percentage, expected_type=type_hints["rotation_window_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ca_pools": ca_pools,
        }
        if key_algorithm is not None:
            self._values["key_algorithm"] = key_algorithm
        if lifetime is not None:
            self._values["lifetime"] = lifetime
        if rotation_window_percentage is not None:
            self._values["rotation_window_percentage"] = rotation_window_percentage

    @builtins.property
    def ca_pools(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''A required mapping of a cloud region to the CA pool resource located in that region used for certificate issuance, adhering to these constraints:  * **Key format:** A supported cloud region name equivalent to the location identifier in the corresponding map entry's value.

        - **Value format:** A valid CA pool resource path format like:
          'projects/{project}/locations/{location}/caPools/{ca_pool}'
        - **Region Matching:** Workloads are ONLY issued certificates from CA pools within the
          same region. Also the CA pool region (in value) must match the workload's region (key).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#ca_pools GoogleIamWorkloadIdentityPool#ca_pools}
        '''
        result = self._values.get("ca_pools")
        assert result is not None, "Required property 'ca_pools' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def key_algorithm(self) -> typing.Optional[builtins.str]:
        '''Key algorithm to use when generating the key pair.

        This key pair will be used to create
        the certificate. If unspecified, this will default to 'ECDSA_P256'.

        - 'RSA_2048': Specifies RSA with a 2048-bit modulus.
        - 'RSA_3072': Specifies RSA with a 3072-bit modulus.
        - 'RSA_4096': Specifies RSA with a 4096-bit modulus.
        - 'ECDSA_P256': Specifies ECDSA with curve P256.
        - 'ECDSA_P384': Specifies ECDSA with curve P384. Possible values: ["RSA_2048", "RSA_3072", "RSA_4096", "ECDSA_P256", "ECDSA_P384"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#key_algorithm GoogleIamWorkloadIdentityPool#key_algorithm}
        '''
        result = self._values.get("key_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifetime(self) -> typing.Optional[builtins.str]:
        '''Lifetime of the workload certificates issued by the CA pool in seconds.

        Must be between
        '86400s' (24 hours) to '2592000s' (30 days), ends in the suffix "'s'" (indicating seconds)
        and is preceded by the number of seconds. If unspecified, this will be defaulted to
        '86400s' (24 hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#lifetime GoogleIamWorkloadIdentityPool#lifetime}
        '''
        result = self._values.get("lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_window_percentage(self) -> typing.Optional[jsii.Number]:
        '''Rotation window percentage indicating when certificate rotation should be initiated based on remaining lifetime.

        Must be between '50' - '80'. If unspecified, this will be defaulted
        to '50'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#rotation_window_percentage GoogleIamWorkloadIdentityPool#rotation_window_percentage}
        '''
        result = self._values.get("rotation_window_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__441676dde809b26d781a85d0b3d6e0b12bcf77011870e729e9b77ecb7e6168cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyAlgorithm")
    def reset_key_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyAlgorithm", []))

    @jsii.member(jsii_name="resetLifetime")
    def reset_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifetime", []))

    @jsii.member(jsii_name="resetRotationWindowPercentage")
    def reset_rotation_window_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationWindowPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="caPoolsInput")
    def ca_pools_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "caPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithmInput")
    def key_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="lifetimeInput")
    def lifetime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationWindowPercentageInput")
    def rotation_window_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rotationWindowPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="caPools")
    def ca_pools(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "caPools"))

    @ca_pools.setter
    def ca_pools(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d05fc7cea6075a52cac34398bd2f376ac00d447f95fff1871bd29698b94f4f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caPools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithm")
    def key_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlgorithm"))

    @key_algorithm.setter
    def key_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef23c7cd04b2d7e51a6526cb7d913cb2fb1321f5682c68acf5bb69cad6909b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lifetime")
    def lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifetime"))

    @lifetime.setter
    def lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b3c82985da5632f8a8f72f19d26e79c8671923c18994247d580604c26ba2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationWindowPercentage")
    def rotation_window_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rotationWindowPercentage"))

    @rotation_window_percentage.setter
    def rotation_window_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9595c5d73d97fd933fa2be5bfc9c930b4bb031f4ad0eec6668210f5c1ff0e03b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationWindowPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig]:
        return typing.cast(typing.Optional[GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db4b64d161a1938c973ee39d49b83bde1b8d960cfd473a762670bfdf240a05ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineTrustConfig",
    jsii_struct_bases=[],
    name_mapping={"additional_trust_bundles": "additionalTrustBundles"},
)
class GoogleIamWorkloadIdentityPoolInlineTrustConfig:
    def __init__(
        self,
        *,
        additional_trust_bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param additional_trust_bundles: additional_trust_bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#additional_trust_bundles GoogleIamWorkloadIdentityPool#additional_trust_bundles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b4f1e8617acf42f5f1245966af1f0dfa2bfb2d75cbfc5a2bc817744144cd32)
            check_type(argname="argument additional_trust_bundles", value=additional_trust_bundles, expected_type=type_hints["additional_trust_bundles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_trust_bundles is not None:
            self._values["additional_trust_bundles"] = additional_trust_bundles

    @builtins.property
    def additional_trust_bundles(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles"]]]:
        '''additional_trust_bundles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#additional_trust_bundles GoogleIamWorkloadIdentityPool#additional_trust_bundles}
        '''
        result = self._values.get("additional_trust_bundles")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolInlineTrustConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles",
    jsii_struct_bases=[],
    name_mapping={"trust_anchors": "trustAnchors", "trust_domain": "trustDomain"},
)
class GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles:
    def __init__(
        self,
        *,
        trust_anchors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors", typing.Dict[builtins.str, typing.Any]]]],
        trust_domain: builtins.str,
    ) -> None:
        '''
        :param trust_anchors: trust_anchors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#trust_anchors GoogleIamWorkloadIdentityPool#trust_anchors}
        :param trust_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#trust_domain GoogleIamWorkloadIdentityPool#trust_domain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e79c9f0dff7b69e3e6a2206da732e6630326a285c1ea5c7b2b68d86206268d)
            check_type(argname="argument trust_anchors", value=trust_anchors, expected_type=type_hints["trust_anchors"])
            check_type(argname="argument trust_domain", value=trust_domain, expected_type=type_hints["trust_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trust_anchors": trust_anchors,
            "trust_domain": trust_domain,
        }

    @builtins.property
    def trust_anchors(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors"]]:
        '''trust_anchors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#trust_anchors GoogleIamWorkloadIdentityPool#trust_anchors}
        '''
        result = self._values.get("trust_anchors")
        assert result is not None, "Required property 'trust_anchors' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors"]], result)

    @builtins.property
    def trust_domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#trust_domain GoogleIamWorkloadIdentityPool#trust_domain}.'''
        result = self._values.get("trust_domain")
        assert result is not None, "Required property 'trust_domain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5c54c1e361aef56138e36556634bea5e7971c7fa929da42f623cf6a58234357)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771864814fca2cf677151c91c162cb92b444a20541d7d11fdfa96d1ab539a6de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9c9d7fedf82ef177874ab90f91ab04c85378228e9b8c0b570afe301e880acb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7112a8bad66a99cfecbbf98049152629082a5cbe508ab11740aa7206fd854751)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8c2bf2101444cd3b80ae461131aeab61f491e86274b481b7561204fcd6be7f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600486caf7afcd447ff270d00913d6a963aa9a021b6953afd10e6a57b350ae2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ca0c85ab4472f332c61806711c65d01117ad2c1c0931466a50a6ca6708fa99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTrustAnchors")
    def put_trust_anchors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ed2dfdcafbdd7f3fd2063fcedad6d7e90fac46345c1399e5973fe6b2b3d54d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrustAnchors", [value]))

    @builtins.property
    @jsii.member(jsii_name="trustAnchors")
    def trust_anchors(
        self,
    ) -> "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsList":
        return typing.cast("GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsList", jsii.get(self, "trustAnchors"))

    @builtins.property
    @jsii.member(jsii_name="trustAnchorsInput")
    def trust_anchors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors"]]], jsii.get(self, "trustAnchorsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustDomainInput")
    def trust_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="trustDomain")
    def trust_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustDomain"))

    @trust_domain.setter
    def trust_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b87c4e185c1902a7373abe3b6a8decea9e6b0aab88b88c7a844e2a206c0f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cbc904ced9bce7397690b3eb9fab8f1650d8e385d2674dd2dabc1000c8f477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors",
    jsii_struct_bases=[],
    name_mapping={"pem_certificate": "pemCertificate"},
)
class GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors:
    def __init__(self, *, pem_certificate: builtins.str) -> None:
        '''
        :param pem_certificate: PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#pem_certificate GoogleIamWorkloadIdentityPool#pem_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcfaf3a5778cf2a324a5815aef6beacdd31246ce5509d1669bef4ceb94555b80)
            check_type(argname="argument pem_certificate", value=pem_certificate, expected_type=type_hints["pem_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pem_certificate": pem_certificate,
        }

    @builtins.property
    def pem_certificate(self) -> builtins.str:
        '''PEM certificate of the PKI used for validation. Must only contain one ca certificate(either root or intermediate cert).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#pem_certificate GoogleIamWorkloadIdentityPool#pem_certificate}
        '''
        result = self._values.get("pem_certificate")
        assert result is not None, "Required property 'pem_certificate' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__159000674414f885356d7d1152fb799df0098c46aea8f5cafe0c7206f7489cc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556cf8e67562e5fcba1908e32dbfd02f4f8fd693ad5883099da5724c560429dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5046c2455c523c210e74ac1bb94d43f08b297bdd867517ca25b28ed68d40f5ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1dd737e448ac94e19c2f534d36488f0faedae7c2925b296de2af3352f6cfade)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cf9deb87a50d7a13c281652a780329435702e14f92211302ed35b70bdb7598c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3b92ae8f4694e33e72d041ce48ede5b188d82cbed7cff87ca7f4ba4d1d301b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ccfa9ae06d7022e8dac8cfc381474dae6adfe7902322ae513b7d6e53c80121d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__a01fbb96e514911ab9369cdc8d883dc8b687c008279ea239d832d6e9e5d9fe2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc346b97c6eb185df927906164595b621ca1fa35710306021f035a16f53bfc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIamWorkloadIdentityPoolInlineTrustConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolInlineTrustConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de3b36501d2d5196f9d380288e42fd1063da7f330da4a28f816df5fbdbc6adde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalTrustBundles")
    def put_additional_trust_bundles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d1522a6cc92bb968a6757076530af546a87c3bb050bf1db81df92b11ff4695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalTrustBundles", [value]))

    @jsii.member(jsii_name="resetAdditionalTrustBundles")
    def reset_additional_trust_bundles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalTrustBundles", []))

    @builtins.property
    @jsii.member(jsii_name="additionalTrustBundles")
    def additional_trust_bundles(
        self,
    ) -> GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesList:
        return typing.cast(GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesList, jsii.get(self, "additionalTrustBundles"))

    @builtins.property
    @jsii.member(jsii_name="additionalTrustBundlesInput")
    def additional_trust_bundles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]]], jsii.get(self, "additionalTrustBundlesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIamWorkloadIdentityPoolInlineTrustConfig]:
        return typing.cast(typing.Optional[GoogleIamWorkloadIdentityPoolInlineTrustConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIamWorkloadIdentityPoolInlineTrustConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a047221f1ece485fc2c2c22a6e3980c28e0a8da6907a9fa385097e507452bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleIamWorkloadIdentityPoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#create GoogleIamWorkloadIdentityPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#delete GoogleIamWorkloadIdentityPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#update GoogleIamWorkloadIdentityPool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06827431041d2e983e2e94b4374c77de0d7a2b2ea3a7316a76ba33458f09529c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#create GoogleIamWorkloadIdentityPool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#delete GoogleIamWorkloadIdentityPool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iam_workload_identity_pool#update GoogleIamWorkloadIdentityPool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIamWorkloadIdentityPoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIamWorkloadIdentityPoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIamWorkloadIdentityPool.GoogleIamWorkloadIdentityPoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a65c588483e78c41976a451db9b762dc6f2793fd371f66f5ae1c267e5b22b8ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a34b00689f3cecb6b283b6363878bc9d44177bacc791c70d9a22085c49f2aaf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b6c68cfdb4891278d052da10d2d6f4c99b08c8a6c0b411dd7afe0fac2673de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31e33990dceb124fb2806f68c60437f923a49ed5332c22f4dce08efc1e53f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3719b211468cd3c95740088a7ae741d4abcdd3d2b4fb6a11b64dac86e35b9def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleIamWorkloadIdentityPool",
    "GoogleIamWorkloadIdentityPoolConfig",
    "GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig",
    "GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfigOutputReference",
    "GoogleIamWorkloadIdentityPoolInlineTrustConfig",
    "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles",
    "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesList",
    "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesOutputReference",
    "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors",
    "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsList",
    "GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchorsOutputReference",
    "GoogleIamWorkloadIdentityPoolInlineTrustConfigOutputReference",
    "GoogleIamWorkloadIdentityPoolTimeouts",
    "GoogleIamWorkloadIdentityPoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__55028bac2eaa1ac69f18598fea073d82f39175d1f38dda252dda9ba6a3598746(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    workload_identity_pool_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inline_certificate_issuance_config: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inline_trust_config: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolInlineTrustConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2fd9f99453b5599dda3e3696d4559aaefbeb624ed16061962a34dfc3ec7b3435(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c180a54bec5c2a0abf33dd302bbed2fdbec4661c3bcf73a59cb4a89a41153e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0287fd61c0b7a11fdd7333722a08534af7270fe22f96a46468189009e743c4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28cf04ef905d8d126af0a21d3b6a971af86bd3cb8223410be6bbdbb637c7e4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54291f5c28bbc984b97715fa144937ab29b180570530632f551e3321c3a9581f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4984fc855f84364f1bb9f6435ee17af8c85b875d81515451843cef6f934230c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de119945357ed61ef6598d006a1a8cbc21348108bd9065d5f7e6b0b98c85395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928714b72b77ec5acab275d8ec4ce5252585997e1f0a965e161d7cd046346cf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b477e3c83d9b24d62c9dd23b368dd8ab0e5421779866a76c16180040a1cbe92(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    workload_identity_pool_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inline_certificate_issuance_config: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inline_trust_config: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolInlineTrustConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIamWorkloadIdentityPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b4317f5a615969fff2860f547cfe7191e9875f13bf46e648c445d24eea9a7c(
    *,
    ca_pools: typing.Mapping[builtins.str, builtins.str],
    key_algorithm: typing.Optional[builtins.str] = None,
    lifetime: typing.Optional[builtins.str] = None,
    rotation_window_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441676dde809b26d781a85d0b3d6e0b12bcf77011870e729e9b77ecb7e6168cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d05fc7cea6075a52cac34398bd2f376ac00d447f95fff1871bd29698b94f4f9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef23c7cd04b2d7e51a6526cb7d913cb2fb1321f5682c68acf5bb69cad6909b97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b3c82985da5632f8a8f72f19d26e79c8671923c18994247d580604c26ba2c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9595c5d73d97fd933fa2be5bfc9c930b4bb031f4ad0eec6668210f5c1ff0e03b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4b64d161a1938c973ee39d49b83bde1b8d960cfd473a762670bfdf240a05ce(
    value: typing.Optional[GoogleIamWorkloadIdentityPoolInlineCertificateIssuanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b4f1e8617acf42f5f1245966af1f0dfa2bfb2d75cbfc5a2bc817744144cd32(
    *,
    additional_trust_bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e79c9f0dff7b69e3e6a2206da732e6630326a285c1ea5c7b2b68d86206268d(
    *,
    trust_anchors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors, typing.Dict[builtins.str, typing.Any]]]],
    trust_domain: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c54c1e361aef56138e36556634bea5e7971c7fa929da42f623cf6a58234357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771864814fca2cf677151c91c162cb92b444a20541d7d11fdfa96d1ab539a6de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9c9d7fedf82ef177874ab90f91ab04c85378228e9b8c0b570afe301e880acb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7112a8bad66a99cfecbbf98049152629082a5cbe508ab11740aa7206fd854751(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c2bf2101444cd3b80ae461131aeab61f491e86274b481b7561204fcd6be7f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600486caf7afcd447ff270d00913d6a963aa9a021b6953afd10e6a57b350ae2a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ca0c85ab4472f332c61806711c65d01117ad2c1c0931466a50a6ca6708fa99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ed2dfdcafbdd7f3fd2063fcedad6d7e90fac46345c1399e5973fe6b2b3d54d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b87c4e185c1902a7373abe3b6a8decea9e6b0aab88b88c7a844e2a206c0f77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cbc904ced9bce7397690b3eb9fab8f1650d8e385d2674dd2dabc1000c8f477(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfaf3a5778cf2a324a5815aef6beacdd31246ce5509d1669bef4ceb94555b80(
    *,
    pem_certificate: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159000674414f885356d7d1152fb799df0098c46aea8f5cafe0c7206f7489cc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556cf8e67562e5fcba1908e32dbfd02f4f8fd693ad5883099da5724c560429dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5046c2455c523c210e74ac1bb94d43f08b297bdd867517ca25b28ed68d40f5ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1dd737e448ac94e19c2f534d36488f0faedae7c2925b296de2af3352f6cfade(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf9deb87a50d7a13c281652a780329435702e14f92211302ed35b70bdb7598c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3b92ae8f4694e33e72d041ce48ede5b188d82cbed7cff87ca7f4ba4d1d301b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccfa9ae06d7022e8dac8cfc381474dae6adfe7902322ae513b7d6e53c80121d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01fbb96e514911ab9369cdc8d883dc8b687c008279ea239d832d6e9e5d9fe2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc346b97c6eb185df927906164595b621ca1fa35710306021f035a16f53bfc4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundlesTrustAnchors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3b36501d2d5196f9d380288e42fd1063da7f330da4a28f816df5fbdbc6adde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d1522a6cc92bb968a6757076530af546a87c3bb050bf1db81df92b11ff4695(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIamWorkloadIdentityPoolInlineTrustConfigAdditionalTrustBundles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a047221f1ece485fc2c2c22a6e3980c28e0a8da6907a9fa385097e507452bd(
    value: typing.Optional[GoogleIamWorkloadIdentityPoolInlineTrustConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06827431041d2e983e2e94b4374c77de0d7a2b2ea3a7316a76ba33458f09529c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65c588483e78c41976a451db9b762dc6f2793fd371f66f5ae1c267e5b22b8ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34b00689f3cecb6b283b6363878bc9d44177bacc791c70d9a22085c49f2aaf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b6c68cfdb4891278d052da10d2d6f4c99b08c8a6c0b411dd7afe0fac2673de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31e33990dceb124fb2806f68c60437f923a49ed5332c22f4dce08efc1e53f95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3719b211468cd3c95740088a7ae741d4abcdd3d2b4fb6a11b64dac86e35b9def(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIamWorkloadIdentityPoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
