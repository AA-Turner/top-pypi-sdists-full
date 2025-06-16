r'''
# `google_certificate_manager_certificate_issuance_config`

Refer to the Terraform Registry for docs: [`google_certificate_manager_certificate_issuance_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config).
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


class GoogleCertificateManagerCertificateIssuanceConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificateIssuanceConfig.GoogleCertificateManagerCertificateIssuanceConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config google_certificate_manager_certificate_issuance_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        certificate_authority_config: typing.Union["GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig", typing.Dict[builtins.str, typing.Any]],
        key_algorithm: builtins.str,
        lifetime: builtins.str,
        name: builtins.str,
        rotation_window_percentage: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCertificateManagerCertificateIssuanceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config google_certificate_manager_certificate_issuance_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param certificate_authority_config: certificate_authority_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#certificate_authority_config GoogleCertificateManagerCertificateIssuanceConfig#certificate_authority_config}
        :param key_algorithm: Key algorithm to use when generating the private key. Possible values: ["RSA_2048", "ECDSA_P256"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#key_algorithm GoogleCertificateManagerCertificateIssuanceConfig#key_algorithm}
        :param lifetime: Lifetime of issued certificates. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "1814400s". Valid values are from 21 days (1814400s) to 30 days (2592000s) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#lifetime GoogleCertificateManagerCertificateIssuanceConfig#lifetime}
        :param name: A user-defined name of the certificate issuance config. CertificateIssuanceConfig names must be unique globally. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#name GoogleCertificateManagerCertificateIssuanceConfig#name}
        :param rotation_window_percentage: It specifies the percentage of elapsed time of the certificate lifetime to wait before renewing the certificate. Must be a number between 1-99, inclusive. You must set the rotation window percentage in relation to the certificate lifetime so that certificate renewal occurs at least 7 days after the certificate has been issued and at least 7 days before it expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#rotation_window_percentage GoogleCertificateManagerCertificateIssuanceConfig#rotation_window_percentage}
        :param description: One or more paragraphs of text description of a CertificateIssuanceConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#description GoogleCertificateManagerCertificateIssuanceConfig#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#id GoogleCertificateManagerCertificateIssuanceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: 'Set of label tags associated with the CertificateIssuanceConfig resource. An object containing a list of "key": value pairs. Example: { "name": "wrench", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#labels GoogleCertificateManagerCertificateIssuanceConfig#labels}
        :param location: The Certificate Manager location. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#location GoogleCertificateManagerCertificateIssuanceConfig#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#project GoogleCertificateManagerCertificateIssuanceConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#timeouts GoogleCertificateManagerCertificateIssuanceConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e10b31e755bc0fa428720dfbdc6ec551ba8fbdba83ad95d4308f3981e038abb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCertificateManagerCertificateIssuanceConfigConfig(
            certificate_authority_config=certificate_authority_config,
            key_algorithm=key_algorithm,
            lifetime=lifetime,
            name=name,
            rotation_window_percentage=rotation_window_percentage,
            description=description,
            id=id,
            labels=labels,
            location=location,
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
        '''Generates CDKTF code for importing a GoogleCertificateManagerCertificateIssuanceConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCertificateManagerCertificateIssuanceConfig to import.
        :param import_from_id: The id of the existing GoogleCertificateManagerCertificateIssuanceConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCertificateManagerCertificateIssuanceConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c61cf3e173ac4adb856834e068f562d40beb5d291cbe842fdd0a98766fd3e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCertificateAuthorityConfig")
    def put_certificate_authority_config(
        self,
        *,
        certificate_authority_service_config: typing.Optional[typing.Union["GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_authority_service_config: certificate_authority_service_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#certificate_authority_service_config GoogleCertificateManagerCertificateIssuanceConfig#certificate_authority_service_config}
        '''
        value = GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig(
            certificate_authority_service_config=certificate_authority_service_config
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateAuthorityConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#create GoogleCertificateManagerCertificateIssuanceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#delete GoogleCertificateManagerCertificateIssuanceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#update GoogleCertificateManagerCertificateIssuanceConfig#update}.
        '''
        value = GoogleCertificateManagerCertificateIssuanceConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

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
    @jsii.member(jsii_name="certificateAuthorityConfig")
    def certificate_authority_config(
        self,
    ) -> "GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigOutputReference":
        return typing.cast("GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigOutputReference", jsii.get(self, "certificateAuthorityConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleCertificateManagerCertificateIssuanceConfigTimeoutsOutputReference":
        return typing.cast("GoogleCertificateManagerCertificateIssuanceConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityConfigInput")
    def certificate_authority_config_input(
        self,
    ) -> typing.Optional["GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig"]:
        return typing.cast(typing.Optional["GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig"], jsii.get(self, "certificateAuthorityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithmInput")
    def key_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifetimeInput")
    def lifetime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationWindowPercentageInput")
    def rotation_window_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rotationWindowPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCertificateManagerCertificateIssuanceConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCertificateManagerCertificateIssuanceConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fea8fb3b0343c04e84ff9856d6e6853be9d660da02a2b3a5458c974fcb2881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9360ff932df3a61e5804eb1a6eebd39f05fd7f5364c719248d8bca3e7dba5177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithm")
    def key_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlgorithm"))

    @key_algorithm.setter
    def key_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e140f13cbe4043df11343170b65d4e865ccd5a85c4a64d4f2730c4d55825f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3e37b086904c4e95de4b56dc50ba5ef87db1590a4ce2a1a434ba8500bf3742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lifetime")
    def lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifetime"))

    @lifetime.setter
    def lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420a5b941cfa7749045f421ba038aff24e907e9fa4aca1d1d9c0feb54f0cd6fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f26c9cb6a34a0b4d025fe1d452892c4f9d3b05dffeaacdf55c8fc56e0cc95b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2234600dfab3a69b2547410b9425e684820bc112ae233609023c1ca8678eed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b93b1635b122c1d32f598754667bd9adb7ec1499f171d93f2989d84da93145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationWindowPercentage")
    def rotation_window_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rotationWindowPercentage"))

    @rotation_window_percentage.setter
    def rotation_window_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2749ba7198a50e1ecf4359eba831ee783b9704f0c9911cece8659cccb90f670b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationWindowPercentage", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificateIssuanceConfig.GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority_service_config": "certificateAuthorityServiceConfig",
    },
)
class GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig:
    def __init__(
        self,
        *,
        certificate_authority_service_config: typing.Optional[typing.Union["GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_authority_service_config: certificate_authority_service_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#certificate_authority_service_config GoogleCertificateManagerCertificateIssuanceConfig#certificate_authority_service_config}
        '''
        if isinstance(certificate_authority_service_config, dict):
            certificate_authority_service_config = GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig(**certificate_authority_service_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3d35eceb1f554c78c64a007ab4acbbdeb263592da82badf3ca8bc55373b5ec)
            check_type(argname="argument certificate_authority_service_config", value=certificate_authority_service_config, expected_type=type_hints["certificate_authority_service_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_authority_service_config is not None:
            self._values["certificate_authority_service_config"] = certificate_authority_service_config

    @builtins.property
    def certificate_authority_service_config(
        self,
    ) -> typing.Optional["GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig"]:
        '''certificate_authority_service_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#certificate_authority_service_config GoogleCertificateManagerCertificateIssuanceConfig#certificate_authority_service_config}
        '''
        result = self._values.get("certificate_authority_service_config")
        return typing.cast(typing.Optional["GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificateIssuanceConfig.GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig",
    jsii_struct_bases=[],
    name_mapping={"ca_pool": "caPool"},
)
class GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig:
    def __init__(self, *, ca_pool: builtins.str) -> None:
        '''
        :param ca_pool: A CA pool resource used to issue a certificate. The CA pool string has a relative resource path following the form "projects/{project}/locations/{location}/caPools/{caPool}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#ca_pool GoogleCertificateManagerCertificateIssuanceConfig#ca_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b163af01c352524af994856123faf111f0fc63aefa6eaf1b2ce8db0366ac455)
            check_type(argname="argument ca_pool", value=ca_pool, expected_type=type_hints["ca_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ca_pool": ca_pool,
        }

    @builtins.property
    def ca_pool(self) -> builtins.str:
        '''A CA pool resource used to issue a certificate.

        The CA pool string has a relative resource path following the form
        "projects/{project}/locations/{location}/caPools/{caPool}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#ca_pool GoogleCertificateManagerCertificateIssuanceConfig#ca_pool}
        '''
        result = self._values.get("ca_pool")
        assert result is not None, "Required property 'ca_pool' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificateIssuanceConfig.GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d68b22e8a6cc7ea56ca451f828e982ca2832c6740080bd0666f3bc5d1e62003)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="caPoolInput")
    def ca_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="caPool")
    def ca_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caPool"))

    @ca_pool.setter
    def ca_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb33cf195d020ca83bcc6adf12fde097399ace0ae524d246488804758d072623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig]:
        return typing.cast(typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09108283ae5a5e074a02ee2ed8bba79940ee2506a9cb57168e498f8b77b1d88c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificateIssuanceConfig.GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9dac3d897f43229507b14006f6a39101de2b0b09f388b4a0dcade36594fc6d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCertificateAuthorityServiceConfig")
    def put_certificate_authority_service_config(
        self,
        *,
        ca_pool: builtins.str,
    ) -> None:
        '''
        :param ca_pool: A CA pool resource used to issue a certificate. The CA pool string has a relative resource path following the form "projects/{project}/locations/{location}/caPools/{caPool}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#ca_pool GoogleCertificateManagerCertificateIssuanceConfig#ca_pool}
        '''
        value = GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig(
            ca_pool=ca_pool
        )

        return typing.cast(None, jsii.invoke(self, "putCertificateAuthorityServiceConfig", [value]))

    @jsii.member(jsii_name="resetCertificateAuthorityServiceConfig")
    def reset_certificate_authority_service_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateAuthorityServiceConfig", []))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityServiceConfig")
    def certificate_authority_service_config(
        self,
    ) -> GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigOutputReference:
        return typing.cast(GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigOutputReference, jsii.get(self, "certificateAuthorityServiceConfig"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityServiceConfigInput")
    def certificate_authority_service_config_input(
        self,
    ) -> typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig]:
        return typing.cast(typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig], jsii.get(self, "certificateAuthorityServiceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig]:
        return typing.cast(typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a8c65d3992284be6f993acc9bee12eb6651f8075e83dad1c93a130afc8d1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificateIssuanceConfig.GoogleCertificateManagerCertificateIssuanceConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "certificate_authority_config": "certificateAuthorityConfig",
        "key_algorithm": "keyAlgorithm",
        "lifetime": "lifetime",
        "name": "name",
        "rotation_window_percentage": "rotationWindowPercentage",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleCertificateManagerCertificateIssuanceConfigConfig(
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
        certificate_authority_config: typing.Union[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig, typing.Dict[builtins.str, typing.Any]],
        key_algorithm: builtins.str,
        lifetime: builtins.str,
        name: builtins.str,
        rotation_window_percentage: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCertificateManagerCertificateIssuanceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param certificate_authority_config: certificate_authority_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#certificate_authority_config GoogleCertificateManagerCertificateIssuanceConfig#certificate_authority_config}
        :param key_algorithm: Key algorithm to use when generating the private key. Possible values: ["RSA_2048", "ECDSA_P256"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#key_algorithm GoogleCertificateManagerCertificateIssuanceConfig#key_algorithm}
        :param lifetime: Lifetime of issued certificates. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "1814400s". Valid values are from 21 days (1814400s) to 30 days (2592000s) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#lifetime GoogleCertificateManagerCertificateIssuanceConfig#lifetime}
        :param name: A user-defined name of the certificate issuance config. CertificateIssuanceConfig names must be unique globally. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#name GoogleCertificateManagerCertificateIssuanceConfig#name}
        :param rotation_window_percentage: It specifies the percentage of elapsed time of the certificate lifetime to wait before renewing the certificate. Must be a number between 1-99, inclusive. You must set the rotation window percentage in relation to the certificate lifetime so that certificate renewal occurs at least 7 days after the certificate has been issued and at least 7 days before it expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#rotation_window_percentage GoogleCertificateManagerCertificateIssuanceConfig#rotation_window_percentage}
        :param description: One or more paragraphs of text description of a CertificateIssuanceConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#description GoogleCertificateManagerCertificateIssuanceConfig#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#id GoogleCertificateManagerCertificateIssuanceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: 'Set of label tags associated with the CertificateIssuanceConfig resource. An object containing a list of "key": value pairs. Example: { "name": "wrench", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#labels GoogleCertificateManagerCertificateIssuanceConfig#labels}
        :param location: The Certificate Manager location. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#location GoogleCertificateManagerCertificateIssuanceConfig#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#project GoogleCertificateManagerCertificateIssuanceConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#timeouts GoogleCertificateManagerCertificateIssuanceConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(certificate_authority_config, dict):
            certificate_authority_config = GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig(**certificate_authority_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleCertificateManagerCertificateIssuanceConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d64db8b0ded640072656127968c67cc73e7909aa89938aa2a07905b4cee49fe)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument certificate_authority_config", value=certificate_authority_config, expected_type=type_hints["certificate_authority_config"])
            check_type(argname="argument key_algorithm", value=key_algorithm, expected_type=type_hints["key_algorithm"])
            check_type(argname="argument lifetime", value=lifetime, expected_type=type_hints["lifetime"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rotation_window_percentage", value=rotation_window_percentage, expected_type=type_hints["rotation_window_percentage"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_authority_config": certificate_authority_config,
            "key_algorithm": key_algorithm,
            "lifetime": lifetime,
            "name": name,
            "rotation_window_percentage": rotation_window_percentage,
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
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
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
    def certificate_authority_config(
        self,
    ) -> GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig:
        '''certificate_authority_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#certificate_authority_config GoogleCertificateManagerCertificateIssuanceConfig#certificate_authority_config}
        '''
        result = self._values.get("certificate_authority_config")
        assert result is not None, "Required property 'certificate_authority_config' is missing"
        return typing.cast(GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig, result)

    @builtins.property
    def key_algorithm(self) -> builtins.str:
        '''Key algorithm to use when generating the private key. Possible values: ["RSA_2048", "ECDSA_P256"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#key_algorithm GoogleCertificateManagerCertificateIssuanceConfig#key_algorithm}
        '''
        result = self._values.get("key_algorithm")
        assert result is not None, "Required property 'key_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lifetime(self) -> builtins.str:
        '''Lifetime of issued certificates.

        A duration in seconds with up to nine fractional digits, ending with 's'.
        Example: "1814400s". Valid values are from 21 days (1814400s) to 30 days (2592000s)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#lifetime GoogleCertificateManagerCertificateIssuanceConfig#lifetime}
        '''
        result = self._values.get("lifetime")
        assert result is not None, "Required property 'lifetime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A user-defined name of the certificate issuance config. CertificateIssuanceConfig names must be unique globally.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#name GoogleCertificateManagerCertificateIssuanceConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rotation_window_percentage(self) -> jsii.Number:
        '''It specifies the percentage of elapsed time of the certificate lifetime to wait before renewing the certificate.

        Must be a number between 1-99, inclusive.
        You must set the rotation window percentage in relation to the certificate lifetime so that certificate renewal occurs at least 7 days after
        the certificate has been issued and at least 7 days before it expires.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#rotation_window_percentage GoogleCertificateManagerCertificateIssuanceConfig#rotation_window_percentage}
        '''
        result = self._values.get("rotation_window_percentage")
        assert result is not None, "Required property 'rotation_window_percentage' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''One or more paragraphs of text description of a CertificateIssuanceConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#description GoogleCertificateManagerCertificateIssuanceConfig#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#id GoogleCertificateManagerCertificateIssuanceConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ''''Set of label tags associated with the CertificateIssuanceConfig resource.

        An object containing a list of "key": value pairs. Example: { "name": "wrench", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#labels GoogleCertificateManagerCertificateIssuanceConfig#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The Certificate Manager location. If not specified, "global" is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#location GoogleCertificateManagerCertificateIssuanceConfig#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#project GoogleCertificateManagerCertificateIssuanceConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleCertificateManagerCertificateIssuanceConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#timeouts GoogleCertificateManagerCertificateIssuanceConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCertificateManagerCertificateIssuanceConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateIssuanceConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificateIssuanceConfig.GoogleCertificateManagerCertificateIssuanceConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCertificateManagerCertificateIssuanceConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#create GoogleCertificateManagerCertificateIssuanceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#delete GoogleCertificateManagerCertificateIssuanceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#update GoogleCertificateManagerCertificateIssuanceConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5619aefc682776745bfeb53f7863f28c1494b50ff31a093ddf483ee632542531)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#create GoogleCertificateManagerCertificateIssuanceConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#delete GoogleCertificateManagerCertificateIssuanceConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate_issuance_config#update GoogleCertificateManagerCertificateIssuanceConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateIssuanceConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCertificateManagerCertificateIssuanceConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificateIssuanceConfig.GoogleCertificateManagerCertificateIssuanceConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f1e17359a298f35620f7cc8d1807da52a2af0d2433bea86c602b52bcd11b74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__937c1a3eee29e71763e1dd8c869a79039b6a9bd09fa41ed421e23a293f072e42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4644b91065f1ec85a6f5817d9f2eecf4df561aec02b91999f535d80d379065fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1caa6429e26d20a9ac2cc067f90e89ed289cf09d74f4bc58c18fa6cf5ffc0876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCertificateManagerCertificateIssuanceConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCertificateManagerCertificateIssuanceConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCertificateManagerCertificateIssuanceConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b9e35a204b6c24c0e97d5cf7f5c80ec2e7c35b274eca6d6ff699dd557fe50d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCertificateManagerCertificateIssuanceConfig",
    "GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig",
    "GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig",
    "GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigOutputReference",
    "GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigOutputReference",
    "GoogleCertificateManagerCertificateIssuanceConfigConfig",
    "GoogleCertificateManagerCertificateIssuanceConfigTimeouts",
    "GoogleCertificateManagerCertificateIssuanceConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0e10b31e755bc0fa428720dfbdc6ec551ba8fbdba83ad95d4308f3981e038abb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    certificate_authority_config: typing.Union[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig, typing.Dict[builtins.str, typing.Any]],
    key_algorithm: builtins.str,
    lifetime: builtins.str,
    name: builtins.str,
    rotation_window_percentage: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCertificateManagerCertificateIssuanceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__63c61cf3e173ac4adb856834e068f562d40beb5d291cbe842fdd0a98766fd3e3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fea8fb3b0343c04e84ff9856d6e6853be9d660da02a2b3a5458c974fcb2881(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9360ff932df3a61e5804eb1a6eebd39f05fd7f5364c719248d8bca3e7dba5177(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e140f13cbe4043df11343170b65d4e865ccd5a85c4a64d4f2730c4d55825f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3e37b086904c4e95de4b56dc50ba5ef87db1590a4ce2a1a434ba8500bf3742(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420a5b941cfa7749045f421ba038aff24e907e9fa4aca1d1d9c0feb54f0cd6fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f26c9cb6a34a0b4d025fe1d452892c4f9d3b05dffeaacdf55c8fc56e0cc95b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2234600dfab3a69b2547410b9425e684820bc112ae233609023c1ca8678eed2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b93b1635b122c1d32f598754667bd9adb7ec1499f171d93f2989d84da93145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2749ba7198a50e1ecf4359eba831ee783b9704f0c9911cece8659cccb90f670b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3d35eceb1f554c78c64a007ab4acbbdeb263592da82badf3ca8bc55373b5ec(
    *,
    certificate_authority_service_config: typing.Optional[typing.Union[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b163af01c352524af994856123faf111f0fc63aefa6eaf1b2ce8db0366ac455(
    *,
    ca_pool: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d68b22e8a6cc7ea56ca451f828e982ca2832c6740080bd0666f3bc5d1e62003(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb33cf195d020ca83bcc6adf12fde097399ace0ae524d246488804758d072623(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09108283ae5a5e074a02ee2ed8bba79940ee2506a9cb57168e498f8b77b1d88c(
    value: typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dac3d897f43229507b14006f6a39101de2b0b09f388b4a0dcade36594fc6d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a8c65d3992284be6f993acc9bee12eb6651f8075e83dad1c93a130afc8d1be(
    value: typing.Optional[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d64db8b0ded640072656127968c67cc73e7909aa89938aa2a07905b4cee49fe(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    certificate_authority_config: typing.Union[GoogleCertificateManagerCertificateIssuanceConfigCertificateAuthorityConfig, typing.Dict[builtins.str, typing.Any]],
    key_algorithm: builtins.str,
    lifetime: builtins.str,
    name: builtins.str,
    rotation_window_percentage: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCertificateManagerCertificateIssuanceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5619aefc682776745bfeb53f7863f28c1494b50ff31a093ddf483ee632542531(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f1e17359a298f35620f7cc8d1807da52a2af0d2433bea86c602b52bcd11b74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937c1a3eee29e71763e1dd8c869a79039b6a9bd09fa41ed421e23a293f072e42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4644b91065f1ec85a6f5817d9f2eecf4df561aec02b91999f535d80d379065fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1caa6429e26d20a9ac2cc067f90e89ed289cf09d74f4bc58c18fa6cf5ffc0876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b9e35a204b6c24c0e97d5cf7f5c80ec2e7c35b274eca6d6ff699dd557fe50d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCertificateManagerCertificateIssuanceConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
