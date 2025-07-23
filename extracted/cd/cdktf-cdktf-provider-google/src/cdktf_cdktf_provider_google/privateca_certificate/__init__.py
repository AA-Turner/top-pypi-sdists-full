r'''
# `google_privateca_certificate`

Refer to the Terraform Registry for docs: [`google_privateca_certificate`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate).
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


class PrivatecaCertificate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate google_privateca_certificate}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        pool: builtins.str,
        certificate_authority: typing.Optional[builtins.str] = None,
        certificate_template: typing.Optional[builtins.str] = None,
        config: typing.Optional[typing.Union["PrivatecaCertificateConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lifetime: typing.Optional[builtins.str] = None,
        pem_csr: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["PrivatecaCertificateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate google_privateca_certificate} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location of the Certificate. A full list of valid locations can be found by running 'gcloud privateca locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#location PrivatecaCertificate#location}
        :param name: The name for this Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#name PrivatecaCertificate#name}
        :param pool: The name of the CaPool this Certificate belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#pool PrivatecaCertificate#pool}
        :param certificate_authority: The Certificate Authority ID that should issue the certificate. For example, to issue a Certificate from a Certificate Authority with resource name 'projects/my-project/locations/us-central1/caPools/my-pool/certificateAuthorities/my-ca', argument 'pool' should be set to 'projects/my-project/locations/us-central1/caPools/my-pool', argument 'certificate_authority' should be set to 'my-ca'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#certificate_authority PrivatecaCertificate#certificate_authority}
        :param certificate_template: The resource name for a CertificateTemplate used to issue this certificate, in the format 'projects/* /locations/* /certificateTemplates/*'. If this is specified, the caller must have the necessary permission to use this template. If this is omitted, no template will be used. This template must be in the same location as the Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#certificate_template PrivatecaCertificate#certificate_template} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#config PrivatecaCertificate#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#id PrivatecaCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels with user-defined metadata to apply to this resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#labels PrivatecaCertificate#labels}
        :param lifetime: The desired lifetime of the CA certificate. Used to create the "notBeforeTime" and "notAfterTime" fields inside an X.509 certificate. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#lifetime PrivatecaCertificate#lifetime}
        :param pem_csr: Immutable. A pem-encoded X.509 certificate signing request (CSR). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#pem_csr PrivatecaCertificate#pem_csr}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#project PrivatecaCertificate#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#timeouts PrivatecaCertificate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6513ea971e7ba56821e154da8b680e3c480a8c1f3d3cddcbddbce439f2d585)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = PrivatecaCertificateConfig(
            location=location,
            name=name,
            pool=pool,
            certificate_authority=certificate_authority,
            certificate_template=certificate_template,
            config=config,
            id=id,
            labels=labels,
            lifetime=lifetime,
            pem_csr=pem_csr,
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

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a PrivatecaCertificate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PrivatecaCertificate to import.
        :param import_from_id: The id of the existing PrivatecaCertificate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PrivatecaCertificate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90ccb9d67dbd012cf5b4ddcf487a5be7ce38cf1583bb8a3a8b50b9095c30eb9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        public_key: typing.Union["PrivatecaCertificateConfigPublicKey", typing.Dict[builtins.str, typing.Any]],
        subject_config: typing.Union["PrivatecaCertificateConfigSubjectConfig", typing.Dict[builtins.str, typing.Any]],
        x509_config: typing.Union["PrivatecaCertificateConfigX509Config", typing.Dict[builtins.str, typing.Any]],
        subject_key_id: typing.Optional[typing.Union["PrivatecaCertificateConfigSubjectKeyId", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_key: public_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#public_key PrivatecaCertificate#public_key}
        :param subject_config: subject_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject_config PrivatecaCertificate#subject_config}
        :param x509_config: x509_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#x509_config PrivatecaCertificate#x509_config}
        :param subject_key_id: subject_key_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject_key_id PrivatecaCertificate#subject_key_id}
        '''
        value = PrivatecaCertificateConfigA(
            public_key=public_key,
            subject_config=subject_config,
            x509_config=x509_config,
            subject_key_id=subject_key_id,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#create PrivatecaCertificate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#delete PrivatecaCertificate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#update PrivatecaCertificate#update}.
        '''
        value = PrivatecaCertificateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCertificateAuthority")
    def reset_certificate_authority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateAuthority", []))

    @jsii.member(jsii_name="resetCertificateTemplate")
    def reset_certificate_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateTemplate", []))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLifetime")
    def reset_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifetime", []))

    @jsii.member(jsii_name="resetPemCsr")
    def reset_pem_csr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemCsr", []))

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
    @jsii.member(jsii_name="certificateDescription")
    def certificate_description(
        self,
    ) -> "PrivatecaCertificateCertificateDescriptionList":
        return typing.cast("PrivatecaCertificateCertificateDescriptionList", jsii.get(self, "certificateDescription"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "PrivatecaCertificateConfigAOutputReference":
        return typing.cast("PrivatecaCertificateConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="issuerCertificateAuthority")
    def issuer_certificate_authority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerCertificateAuthority"))

    @builtins.property
    @jsii.member(jsii_name="pemCertificate")
    def pem_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemCertificate"))

    @builtins.property
    @jsii.member(jsii_name="pemCertificateChain")
    def pem_certificate_chain(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pemCertificateChain"))

    @builtins.property
    @jsii.member(jsii_name="revocationDetails")
    def revocation_details(self) -> "PrivatecaCertificateRevocationDetailsList":
        return typing.cast("PrivatecaCertificateRevocationDetailsList", jsii.get(self, "revocationDetails"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PrivatecaCertificateTimeoutsOutputReference":
        return typing.cast("PrivatecaCertificateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityInput")
    def certificate_authority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateAuthorityInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateTemplateInput")
    def certificate_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["PrivatecaCertificateConfigA"]:
        return typing.cast(typing.Optional["PrivatecaCertificateConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="pemCsrInput")
    def pem_csr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemCsrInput"))

    @builtins.property
    @jsii.member(jsii_name="poolInput")
    def pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivatecaCertificateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivatecaCertificateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthority")
    def certificate_authority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthority"))

    @certificate_authority.setter
    def certificate_authority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fc6daeb86b12bdd42916a28eb5730764b9e882b2a9c0a39945077d9a47cbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateTemplate")
    def certificate_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateTemplate"))

    @certificate_template.setter
    def certificate_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e236580ce68e3511f183efb60cb72406dc5babf08164c5ad429e36f46f0f815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31740c1f995ddc63f991207f16e771b857fda8b89b9c7b060952affe7fd38aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e66dd75b3ae78bce0a10a7f6c624450bd3483b08c68f3fbb4de5b3f58af018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lifetime")
    def lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifetime"))

    @lifetime.setter
    def lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa1339c31614fa4467a06538cc08ce8494befce858c0fff1683c2cefb9759ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514d4176de01c0f9a9fab787391e3a14f42428c6d1e736310122d800ec758fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1ecf0edb5a9e332362da62c41befa7424d478fe1d62dc6aa9f379c880b13f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pemCsr")
    def pem_csr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemCsr"))

    @pem_csr.setter
    def pem_csr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e53c36654e726768ac8f4fef86cbb1ac704fc7ebab0494bef561e6d1578b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCsr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pool")
    def pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pool"))

    @pool.setter
    def pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff9d9061e8b0e8b17bea4bd11885497546616899e9f9196931f8c47741d0e81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183a1572c9d9fb9ce36439328e8514ff53e4411c0d22529d71e772edfadfa048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescription",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescription:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionAuthorityKeyId",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionAuthorityKeyId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionAuthorityKeyId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionAuthorityKeyIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionAuthorityKeyIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e33ce72de1ea6d5c226af8e2afac76ffa7a38ee99eab97eec29f2f8c02d052a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionAuthorityKeyIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b384285e18c7c74825182ab2a6fd550351f94058c397cdb16025d27cb6c6c4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionAuthorityKeyIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d0e5694a0e380bdf864ee12577542e93023e082b039970b75a8461ee76d595)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f209bacc27a361d1913bb72ecf3c5d3f65ab7c70ebfe3d6ca0d707325130fce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4242eea56eb76a0eaceddc65c4aa144d52517374a869fd051accae1d496e4d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionAuthorityKeyIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionAuthorityKeyIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aa4b14bece8bfde142a301c8467dfbcfd8dc13015bf898d7a9cf72ff3cb8f9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionAuthorityKeyId]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionAuthorityKeyId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionAuthorityKeyId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967f9fa263df211764e64bc273214eaa8e3733caf287017bc6af5b8b7d281653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionCertFingerprint",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionCertFingerprint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionCertFingerprint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionCertFingerprintList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionCertFingerprintList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aee2f950cf0cd35b0bf6ade6583c55994841dac4ad30b8e104f8ddce12ab3d3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionCertFingerprintOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd09e5302d558df825bec4fa7e258cc38d6b33013ad216e9b67cefe430066ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionCertFingerprintOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c618a55c97387b9379e7c8653264af1862d57ee0db15c0bb5174a973ddb22bd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14a25347b09fcbfef9bed95197cd1297eeab26fccb3e5a0dad62a884d9bb6af4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2a6ebd4e1f9f2be1d08e3199aef5f4ddc249f19957f73d536f09d1c1b06eef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionCertFingerprintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionCertFingerprintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e1cb2477054eb590e013271df42f90e340af1a750e5e64e03f86a2c8cb33c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="sha256Hash")
    def sha256_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256Hash"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionCertFingerprint]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionCertFingerprint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionCertFingerprint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f712459cb2baf3fbef357f66e91cf64eec5733c0d3754c5d8d336f209dab91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e85131830e68754f5c3555f77346e8f2ab4246e1a1a559c210daa9ccc1af5e58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0deb1900a13d89bee1df637af0388e52473c53114ec3956d460cbd3801cc0989)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56a012f4bc377158f3a4e29e3d3310d3647ffd4894753d906710ffb2fe0ee17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8884df39f5ba0299179569157d0b15105327c0b400141bd9d1d6e41c6ee24ebd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a9807310602ce40b0df19da43d2cfbfc20552443cea327b6dd6e551376a17c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c32ac2508e3fdacc12ef2c434074367281b0fb5ed4768dc8bcd02cb9420760e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="aiaIssuingCertificateUrls")
    def aia_issuing_certificate_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aiaIssuingCertificateUrls"))

    @builtins.property
    @jsii.member(jsii_name="authorityKeyId")
    def authority_key_id(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionAuthorityKeyIdList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionAuthorityKeyIdList, jsii.get(self, "authorityKeyId"))

    @builtins.property
    @jsii.member(jsii_name="certFingerprint")
    def cert_fingerprint(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionCertFingerprintList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionCertFingerprintList, jsii.get(self, "certFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="crlDistributionPoints")
    def crl_distribution_points(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "crlDistributionPoints"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> "PrivatecaCertificateCertificateDescriptionPublicKeyList":
        return typing.cast("PrivatecaCertificateCertificateDescriptionPublicKeyList", jsii.get(self, "publicKey"))

    @builtins.property
    @jsii.member(jsii_name="subjectDescription")
    def subject_description(
        self,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectDescriptionList":
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectDescriptionList", jsii.get(self, "subjectDescription"))

    @builtins.property
    @jsii.member(jsii_name="subjectKeyId")
    def subject_key_id(
        self,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectKeyIdList":
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectKeyIdList", jsii.get(self, "subjectKeyId"))

    @builtins.property
    @jsii.member(jsii_name="x509Description")
    def x509_description(
        self,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionList":
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionList", jsii.get(self, "x509Description"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescription]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescription], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a369cd5ea2430cc7f3c1997fbceb3bbe7eaf42ec7639370ddb43c22c20f71e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionPublicKey",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionPublicKey:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionPublicKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionPublicKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionPublicKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__405cf4d373b8e0ddd5ca37868f29013e091cf838b215bb1e84ffe85786d512c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionPublicKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997f469bc30aa31d889c8d8c9f81440e5ba67c1e8fb444dff8072738c15d9576)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionPublicKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cece82e0339cb1f423970a2151cf45c19c5fa03d2cb31950b349b4efbebde71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a398e28387c9731b5adf188960d7affb8c192ac956a508b74dffcd57e2e2fb85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__311a30bd371df14e197c204c601df8458757852540099b4b0172d12e0498402a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionPublicKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionPublicKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e73c74bee3086e7fe06e91fd7da1d21287b17a73198fcd7a8fedf303edcd01dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionPublicKey]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionPublicKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionPublicKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9edcb33c32206129bbe063b116f47f5b795b624c6c96d88075d3f4b67ce440f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescription",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionSubjectDescription:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionSubjectDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80241badcb143841aeb856e7f1cfa72a7b6cde69f05582e4f6cf49bb7386abbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectDescriptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aaf3da7a69537458f9c2ab5e87250fcc981be5769fb68054bbd3893e0b6b104)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectDescriptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b1a002801ab2ca043eb7f1ce96d456366bfac05af0db172ce932f1786e3d55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df567132a48b276f027ba69215ca68e972cbe637c3edadb15bc71371248ef008)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b16cd5ee4bb62055af3a7037b832e47a7494ff56d6f4e459a37c14230fa00bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0ce3d8384db581cf924ca418beaeb729002d7b11a5dc17d8843ec0e96b0b43e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hexSerialNumber")
    def hex_serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hexSerialNumber"))

    @builtins.property
    @jsii.member(jsii_name="lifetime")
    def lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifetime"))

    @builtins.property
    @jsii.member(jsii_name="notAfterTime")
    def not_after_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notAfterTime"))

    @builtins.property
    @jsii.member(jsii_name="notBeforeTime")
    def not_before_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notBeforeTime"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(
        self,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectList":
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectList", jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="subjectAltName")
    def subject_alt_name(
        self,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameList":
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameList", jsii.get(self, "subjectAltName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescription]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescription], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913756b766680703ccc8f53deef2549c4586d6d988b409621e754453440d199b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubject",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubject:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltName",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltName:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSans",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSans:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSans(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db3d101fc48b584117da7cf3b129224ddc30f6a1e4ec57935ddb39387a2dc170)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2edc23e3dd29f9e57f50fcbd8c7403c335db6862da67e7aac08156a475d6b806)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fc7b3f7750a34d379d0a01676cacef85388e4211d2a39f5ef6c580982382dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cac94372ba1fad22b16dd2041f4c219ea69c3f69aa42b361764f88d84c3129b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72ed8a91a97a5be3f9cb1df794bd3cdb1d83bb88bcd5c4ecb978a78a135fd2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectId",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27a0372b5641ef7157b83eee10e80e2e2ea108c1bde1a8fa6e35de5b588a4deb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5902fcb7b00b6eeaf0bb47d5c915cdd9045ac9ec91201e398cfc308042578916)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10420fc9d6d542e958888615aa4181172bfbcf56102617c3945ead77e9447a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__296c998648ce51517e1d2f3a03d2123f5bb0b9e377c1f94aa0a2f557bc4d8786)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a08f55b5a17639a74295239bd14eb38254a10cb3a30687b0093900b7b5b9d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da691fa28b109f65205e9cee71f9312a6beb9aa01fbfcabb94456e137dd201ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectId]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a16316c08a21b98dd9b0a22a88973a1ee9ace0b64acc9840c73a4e5f112b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1315273ac99476871c7ff74b373b5b6b36f40c3ab23772351ac6c4aad8624e97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "critical"))

    @builtins.property
    @jsii.member(jsii_name="obectId")
    def obect_id(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdList, jsii.get(self, "obectId"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSans]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSans], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSans],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6d474de734b998d119a6d69336215bbabc54a067a152d31ca230d344ed081f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8492c3c3e6d71db021d16e58b1280afd26cde9c264923d80160e2288ab19e7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cfe62a4ca17ad221707b93e36bcb2d53eb63c5f9a92dc713913f5e531a26b6e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07023a89b1577cff28163a5c44322a20bcd5eb56321938bb09fd7a0172daa41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89875adf1020f6db224703bc095de89590a903bd94dba381e86a9067ac9a2139)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aacf5626506617371e1efb73bb3d0806fb4d74734a04ecb4a7da73d11761fd79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d83c5904855150a292b2800af539032dddf0c184f0d48f13e67c7a351da0acf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="customSans")
    def custom_sans(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansList, jsii.get(self, "customSans"))

    @builtins.property
    @jsii.member(jsii_name="dnsNames")
    def dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsNames"))

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @builtins.property
    @jsii.member(jsii_name="uris")
    def uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "uris"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltName]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e332b287c51791df28ef3b1f808b3bfd4e51fcc89454ab4d55f4ecf31ecdcbdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b031160cd10e48713964cc32a8ac7bf8c21980bd9164f393a2a80d05faa0205)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf3939260c5b791b4b78ff3619869939d530323fadbd7a5c4f02ed07c11b35a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21b4b01bb887231ea17727f17c7d2f0d027b7e468359476662cec35abccff6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9537ca3eac15f8679dd077cd24d91d34523433282e7f7bc6590bf41a08c44148)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e8214fa2a6b1da8d276b9ea64df6781c18ad456adac26b92ae19c4a84056e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a83311aa11d5f72ae5e9fa610614fd3e5a87d04b9585cc632a339712a09d85b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnit")
    def organizational_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationalUnit"))

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @builtins.property
    @jsii.member(jsii_name="streetAddress")
    def street_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streetAddress"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubject]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f1a3625f30964adc09f36f262c86dbaa061d57abdc8a706f13b36071f17245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectKeyId",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionSubjectKeyId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionSubjectKeyId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionSubjectKeyIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectKeyIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a32a4ffeb742ff8d924863c93392d85b5af7306280831005068274de41489041)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionSubjectKeyIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6daa8a9a891ff0ecfb5076ac88870c9e4f626f4c18230d15b7d9384858787750)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionSubjectKeyIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42392e896e17f03b0d8f8991f1cbce6ff5af4048fab5f8f8d1c7c12126467c5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cce932e347f7721b52c6b70ec18ad63d93595b1e5e7c22c7a8416393a0404d1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e1fe94521df1149d71dbebcaa82fd54dc1452d8e22cf2c71c15285048106aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionSubjectKeyIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionSubjectKeyIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1f8c2c41bb19534db873756aed18bb64a5b381e13fb2b79eccc7ce87d8baf0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectKeyId]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectKeyId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectKeyId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff111290a545e50288a2e2ff4bb2bc0b6b7665ca14a0d16e8777f41c0755522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509Description",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509Description:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509Description(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e1f50e24de7daa5f2ab327cb08fae80fc86945fe3868b03efd2a4b765caee56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf07f85048d072656d34c5ccdff0f26a0c5b39550d1f2d7a8e54c07bae2d0622)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a8acbe6993c99a6ea54e635dfbc183e0d4766ec8f84b5a0c31a3d8aa2fe2e71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7d91352fe027de289d0cf40abc99a2c0542ab358eada953b02cf68dd07b29cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e2dbd6118a7c842164c0b3b959f3dbe478521c1e57d727c68e594593421c186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectId",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c60cadf3e51c004f9a3ba30b54898dac4f8c0564410242e69fba3691ae0ecc4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588d094bcea78edf285df7f5a87115ded49db923760e0cbd03fe301741cbf741)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42eb4c5a90ba9052924491e1f67c95e2e340969336e1b2eb8d2a9e0ea8076a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca2b2bd45259d25baf2589b2c30812e39f0be5c6594206dbff84e3d263f3e0d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf32807d505a2224a9afbab1bc469f8b4ba503b9d5fa3837921cb10240d6fd44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f68100cba2f8a5fc17d24688e9c7d5d1941dfe835ce1fb6f5dc82cd543e875ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff6e8caebdb4890b22fe8f893cd6da60fa60cedd09263f43b6c05be9375a9ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff30f13284b82221e9de649d475fe2cea874d4d14f452fd0a667cfc4125dffb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "critical"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdList, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensions]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c814c69ac05d67298e69e1932b3de75f5e4c24dd3a7050e71c368de4238dfd6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f10d9554da98b476c5a8056ebce306ea05b427052b4130b4bd358bc327a07482)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9a74f91b2f2b7d35ab620d990c8b0c699079120ae7efd550115a555effa2d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc734613eab09b4e23a7e63bf8dcfe89b2415d4250b880447b223b0384e31232)
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
            type_hints = typing.get_type_hints(_typecheckingstub__708a01ed3e3c30d05793ebc7b36930211eb1dbce7bc5917790d5a77513c73060)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91eb7625769619cc979c3feb95599318897a970974dd0d525791a505096138a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__347fe064cd581612eac19b606bcd5349db5d0fab407a9770ed9e462fc02c4df3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="isCa")
    def is_ca(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isCa"))

    @builtins.property
    @jsii.member(jsii_name="maxIssuerPathLength")
    def max_issuer_path_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIssuerPathLength"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptions]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d23b61dfe5c23757d8a075f7b7c208ee7d5eaa3fc72e832ebf933682c66368b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsage",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsage:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsage",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsage:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d36f63a01d7c4356fec3a1b353ff4c743ccaa81bc5f9dbe6b95584b870a064f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a5e546d7f3fef96448c12b10720e93dc14f9f4d34021aab0a4f12872c9eff4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63208d4a7d7e32afd9945d32dcfaaff859553aeb1ff68a3328438060b6bb89c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e58f9831a7619a08f6fb03e3438afc9201250128e660f6fe129ee766de04c5db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60b6837846a41470f47475260023f4b66946e70f6f775af8ba5e0cf4de5f10dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2e0feec76b03568ab76584d766f4e096253c16c1f86149db5a764b2b72ee4bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="certSign")
    def cert_sign(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "certSign"))

    @builtins.property
    @jsii.member(jsii_name="contentCommitment")
    def content_commitment(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "contentCommitment"))

    @builtins.property
    @jsii.member(jsii_name="crlSign")
    def crl_sign(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "crlSign"))

    @builtins.property
    @jsii.member(jsii_name="dataEncipherment")
    def data_encipherment(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "dataEncipherment"))

    @builtins.property
    @jsii.member(jsii_name="decipherOnly")
    def decipher_only(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "decipherOnly"))

    @builtins.property
    @jsii.member(jsii_name="digitalSignature")
    def digital_signature(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "digitalSignature"))

    @builtins.property
    @jsii.member(jsii_name="encipherOnly")
    def encipher_only(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "encipherOnly"))

    @builtins.property
    @jsii.member(jsii_name="keyAgreement")
    def key_agreement(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "keyAgreement"))

    @builtins.property
    @jsii.member(jsii_name="keyEncipherment")
    def key_encipherment(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "keyEncipherment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7509d54d3ef68638bcec361b3ed91124bdbc353189cd6f6e24810d0c1be6fea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsage",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsage:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cef95b4be0db5e80a0ea498218594edc83de886473b655e573558422b283e709)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ac318cc71a500ffe8234541ef94d100e9a0e139f694ff5eddc233f2537bdae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865922c9ae31d4294d5bc45a7f9ad5c6533ab482ce06d8ee751526eaa28681d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c5e2304f8e251fd6d108345086d4720a10b72153c9a8bd38f502cac52e692b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__329eb9776fba55e5d2e65c31ee27842b30aed30909b856e8a6bb17687adf2ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fef7966773259a8f9f5e3efd28bd5be8046a13471d0aa8f23f89fb2c403dffe9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientAuth")
    def client_auth(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "clientAuth"))

    @builtins.property
    @jsii.member(jsii_name="codeSigning")
    def code_signing(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "codeSigning"))

    @builtins.property
    @jsii.member(jsii_name="emailProtection")
    def email_protection(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "emailProtection"))

    @builtins.property
    @jsii.member(jsii_name="ocspSigning")
    def ocsp_signing(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "ocspSigning"))

    @builtins.property
    @jsii.member(jsii_name="serverAuth")
    def server_auth(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "serverAuth"))

    @builtins.property
    @jsii.member(jsii_name="timeStamping")
    def time_stamping(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "timeStamping"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52468f296aa91810eef73a27666f0ee7d416c786533deb8d0eb52c077056ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66282787a14d7375e575c081d0a64c2e50d4b93b228ac3d0e1ae4787d5dfc4e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9844c7b907b1f3353903fb71fb080273e856f584c1817503a76fdc865f12068)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e8ce9f624a01c24e861394c8d8c2de3c7ebe271836138a851a710cc3020d5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46f3a1ee55f7de109922a70a5846dfa88ca9db7903cd6eb5e87df6410fbb87dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__578f664d2a7f62b8457c3e58c372594dd54ddf5f2b563d7c1030ff1dbb338f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67853b72575fe2bdba8a9ef9159c863f3d04d92ee9631346b1ada7f97c071ab3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsage")
    def base_key_usage(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageList, jsii.get(self, "baseKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsage")
    def extended_key_usage(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageList, jsii.get(self, "extendedKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsages")
    def unknown_extended_key_usages(
        self,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesList":
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesList", jsii.get(self, "unknownExtendedKeyUsages"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a073e5c3728ece392c8a67a4db245b0e783d1b0857c93e68d046f3f74b02ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsages",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsages:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20905163787241738aafb730bd16f1fc5deb866128be3b45ab12fa32c03441c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9a8f1f9564b90ddab9805025ba38fa16ed54669d88f9814abd0d2f70a92b1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3580a4b700df3cfb19051277e1659898b0645be1f929472bf96d059146ed9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a5f4aab494d1181f8ba2211a675eccee8aa044961a5444428745d64ad54616c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ad956384c7c736f1e2ca162bed1873013e00673599fb8d885a38e82b184fd7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__621390cd363ca2dd5054068e80c79ac2acef621edea6f45a6d6f816a5c93f430)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsages]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsages], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsages],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ffe3be0fb8e925f0ade6abcf75db870eaeb96c4acf7280721034767b28b555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9619cac07c1dc283c031b80f307541088c86716b42f75de18ae3014c6340e86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a3d7e4c9aeff27ad4b388f7d406b4d6fcad2d25950bad045d2b1a5becdd7e1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d08a6300698f7a70576dbfc30748a3d26149a79c9b1d8d75bd6c2400e934409)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b0eaeac987f0a60be029d7dde606e1ff3ba111a8a02c66e647d79b950dec0cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a34cb2c29e04b7fcc8a1679a9a6c0fcea71bc11a516aa167fa9a431f127342bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraints",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc68246556f26bae7090ad646c74e2153a8930073477a35b60b531679ee0e72f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3177e7ae616e33a96ea0eaffbd92f469beac17f24f8e3aa8e0d89e76193302c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ca7ab726dda9bfdbb890a2d530c5a2f768fd615dab66acb5f74fbc87d2a40d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2b632363498d1a319223cfdefe12aed33406f5c83298a623322dfe5e76b9392)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1688fdd03af00870bfd8d876ef5b9b9930aa9c4142e217530695df90a311389c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09241f6ac299db2e93a7eec899e778e012305c4b4b7cbe2c77abbef86994ee82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "critical"))

    @builtins.property
    @jsii.member(jsii_name="excludedDnsNames")
    def excluded_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedDnsNames"))

    @builtins.property
    @jsii.member(jsii_name="excludedEmailAddresses")
    def excluded_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedEmailAddresses"))

    @builtins.property
    @jsii.member(jsii_name="excludedIpRanges")
    def excluded_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="excludedUris")
    def excluded_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedUris"))

    @builtins.property
    @jsii.member(jsii_name="permittedDnsNames")
    def permitted_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedDnsNames"))

    @builtins.property
    @jsii.member(jsii_name="permittedEmailAddresses")
    def permitted_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedEmailAddresses"))

    @builtins.property
    @jsii.member(jsii_name="permittedIpRanges")
    def permitted_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="permittedUris")
    def permitted_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedUris"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraints]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351a643895706b644b5c9595f423ec265bc4d9ac9adb15cc8615dd5df05fa665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43579265900f8670f1c9fbf3022678eb1644504cc686ff21bf6fd70228ff4411)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="additionalExtensions")
    def additional_extensions(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsList, jsii.get(self, "additionalExtensions"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServers")
    def aia_ocsp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aiaOcspServers"))

    @builtins.property
    @jsii.member(jsii_name="caOptions")
    def ca_options(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsList, jsii.get(self, "caOptions"))

    @builtins.property
    @jsii.member(jsii_name="keyUsage")
    def key_usage(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageList, jsii.get(self, "keyUsage"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraints")
    def name_constraints(
        self,
    ) -> PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsList:
        return typing.cast(PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsList, jsii.get(self, "nameConstraints"))

    @builtins.property
    @jsii.member(jsii_name="policyIds")
    def policy_ids(
        self,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsList":
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsList", jsii.get(self, "policyIds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509Description]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509Description], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509Description],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a355289774eb455594b3d8cfe4beb2a7707099d1d8d6e31a9cce6954336167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIds",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8757bb09d517e222650535f6484778be277fceb67475ac8fdd7782d87466951)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0b3f43bd1f352856c56abe725a23391e78e09ad26989f6f4b82277f1bc87e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe86b065a1abd39bf027ea6f801b65677219a412ab76d806cad37455feffb766)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3698c94830de597e2f289ad8fca448a7454825e079c61046e50125dda6301b00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__005bfbbf9cfca1b1fbbd136fbb6dc8da6f8048b77a2f93a1a13685a90d1c2a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9708eb4aaf2d1472d03ff2da076f3b6c239330ded348e88fd23ea57c02e6f024)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIds]:
        return typing.cast(typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44bf46fa42dcf31e49c7e8c891a1a23c59f4b190e9b7ff06d7004a09776f666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfig",
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
        "name": "name",
        "pool": "pool",
        "certificate_authority": "certificateAuthority",
        "certificate_template": "certificateTemplate",
        "config": "config",
        "id": "id",
        "labels": "labels",
        "lifetime": "lifetime",
        "pem_csr": "pemCsr",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class PrivatecaCertificateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        pool: builtins.str,
        certificate_authority: typing.Optional[builtins.str] = None,
        certificate_template: typing.Optional[builtins.str] = None,
        config: typing.Optional[typing.Union["PrivatecaCertificateConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lifetime: typing.Optional[builtins.str] = None,
        pem_csr: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["PrivatecaCertificateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location of the Certificate. A full list of valid locations can be found by running 'gcloud privateca locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#location PrivatecaCertificate#location}
        :param name: The name for this Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#name PrivatecaCertificate#name}
        :param pool: The name of the CaPool this Certificate belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#pool PrivatecaCertificate#pool}
        :param certificate_authority: The Certificate Authority ID that should issue the certificate. For example, to issue a Certificate from a Certificate Authority with resource name 'projects/my-project/locations/us-central1/caPools/my-pool/certificateAuthorities/my-ca', argument 'pool' should be set to 'projects/my-project/locations/us-central1/caPools/my-pool', argument 'certificate_authority' should be set to 'my-ca'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#certificate_authority PrivatecaCertificate#certificate_authority}
        :param certificate_template: The resource name for a CertificateTemplate used to issue this certificate, in the format 'projects/* /locations/* /certificateTemplates/*'. If this is specified, the caller must have the necessary permission to use this template. If this is omitted, no template will be used. This template must be in the same location as the Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#certificate_template PrivatecaCertificate#certificate_template} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#config PrivatecaCertificate#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#id PrivatecaCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels with user-defined metadata to apply to this resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#labels PrivatecaCertificate#labels}
        :param lifetime: The desired lifetime of the CA certificate. Used to create the "notBeforeTime" and "notAfterTime" fields inside an X.509 certificate. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#lifetime PrivatecaCertificate#lifetime}
        :param pem_csr: Immutable. A pem-encoded X.509 certificate signing request (CSR). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#pem_csr PrivatecaCertificate#pem_csr}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#project PrivatecaCertificate#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#timeouts PrivatecaCertificate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = PrivatecaCertificateConfigA(**config)
        if isinstance(timeouts, dict):
            timeouts = PrivatecaCertificateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e9d6a07d20f0fbca56bcde458a9577c49ce47e709406d351f3a17c80239975)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pool", value=pool, expected_type=type_hints["pool"])
            check_type(argname="argument certificate_authority", value=certificate_authority, expected_type=type_hints["certificate_authority"])
            check_type(argname="argument certificate_template", value=certificate_template, expected_type=type_hints["certificate_template"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument lifetime", value=lifetime, expected_type=type_hints["lifetime"])
            check_type(argname="argument pem_csr", value=pem_csr, expected_type=type_hints["pem_csr"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "pool": pool,
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
        if certificate_authority is not None:
            self._values["certificate_authority"] = certificate_authority
        if certificate_template is not None:
            self._values["certificate_template"] = certificate_template
        if config is not None:
            self._values["config"] = config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if lifetime is not None:
            self._values["lifetime"] = lifetime
        if pem_csr is not None:
            self._values["pem_csr"] = pem_csr
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
    def location(self) -> builtins.str:
        '''Location of the Certificate. A full list of valid locations can be found by running 'gcloud privateca locations list'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#location PrivatecaCertificate#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this Certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#name PrivatecaCertificate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool(self) -> builtins.str:
        '''The name of the CaPool this Certificate belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#pool PrivatecaCertificate#pool}
        '''
        result = self._values.get("pool")
        assert result is not None, "Required property 'pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_authority(self) -> typing.Optional[builtins.str]:
        '''The Certificate Authority ID that should issue the certificate.

        For example, to issue a Certificate from
        a Certificate Authority with resource name 'projects/my-project/locations/us-central1/caPools/my-pool/certificateAuthorities/my-ca',
        argument 'pool' should be set to 'projects/my-project/locations/us-central1/caPools/my-pool', argument 'certificate_authority'
        should be set to 'my-ca'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#certificate_authority PrivatecaCertificate#certificate_authority}
        '''
        result = self._values.get("certificate_authority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_template(self) -> typing.Optional[builtins.str]:
        '''The resource name for a CertificateTemplate used to issue this certificate, in the format 'projects/* /locations/* /certificateTemplates/*'.

        If this is specified,
        the caller must have the necessary permission to use this template. If this is
        omitted, no template will be used. This template must be in the same location
        as the Certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#certificate_template PrivatecaCertificate#certificate_template}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("certificate_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config(self) -> typing.Optional["PrivatecaCertificateConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#config PrivatecaCertificate#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["PrivatecaCertificateConfigA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#id PrivatecaCertificate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels with user-defined metadata to apply to this resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#labels PrivatecaCertificate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lifetime(self) -> typing.Optional[builtins.str]:
        '''The desired lifetime of the CA certificate.

        Used to create the "notBeforeTime" and
        "notAfterTime" fields inside an X.509 certificate. A duration in seconds with up to nine
        fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#lifetime PrivatecaCertificate#lifetime}
        '''
        result = self._values.get("lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_csr(self) -> typing.Optional[builtins.str]:
        '''Immutable. A pem-encoded X.509 certificate signing request (CSR).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#pem_csr PrivatecaCertificate#pem_csr}
        '''
        result = self._values.get("pem_csr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#project PrivatecaCertificate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PrivatecaCertificateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#timeouts PrivatecaCertificate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PrivatecaCertificateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "public_key": "publicKey",
        "subject_config": "subjectConfig",
        "x509_config": "x509Config",
        "subject_key_id": "subjectKeyId",
    },
)
class PrivatecaCertificateConfigA:
    def __init__(
        self,
        *,
        public_key: typing.Union["PrivatecaCertificateConfigPublicKey", typing.Dict[builtins.str, typing.Any]],
        subject_config: typing.Union["PrivatecaCertificateConfigSubjectConfig", typing.Dict[builtins.str, typing.Any]],
        x509_config: typing.Union["PrivatecaCertificateConfigX509Config", typing.Dict[builtins.str, typing.Any]],
        subject_key_id: typing.Optional[typing.Union["PrivatecaCertificateConfigSubjectKeyId", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_key: public_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#public_key PrivatecaCertificate#public_key}
        :param subject_config: subject_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject_config PrivatecaCertificate#subject_config}
        :param x509_config: x509_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#x509_config PrivatecaCertificate#x509_config}
        :param subject_key_id: subject_key_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject_key_id PrivatecaCertificate#subject_key_id}
        '''
        if isinstance(public_key, dict):
            public_key = PrivatecaCertificateConfigPublicKey(**public_key)
        if isinstance(subject_config, dict):
            subject_config = PrivatecaCertificateConfigSubjectConfig(**subject_config)
        if isinstance(x509_config, dict):
            x509_config = PrivatecaCertificateConfigX509Config(**x509_config)
        if isinstance(subject_key_id, dict):
            subject_key_id = PrivatecaCertificateConfigSubjectKeyId(**subject_key_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953fde99b9a0a976d4a7201a446e1b04a5e464f2e566254fe094c6fe0b621cab)
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument subject_config", value=subject_config, expected_type=type_hints["subject_config"])
            check_type(argname="argument x509_config", value=x509_config, expected_type=type_hints["x509_config"])
            check_type(argname="argument subject_key_id", value=subject_key_id, expected_type=type_hints["subject_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_key": public_key,
            "subject_config": subject_config,
            "x509_config": x509_config,
        }
        if subject_key_id is not None:
            self._values["subject_key_id"] = subject_key_id

    @builtins.property
    def public_key(self) -> "PrivatecaCertificateConfigPublicKey":
        '''public_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#public_key PrivatecaCertificate#public_key}
        '''
        result = self._values.get("public_key")
        assert result is not None, "Required property 'public_key' is missing"
        return typing.cast("PrivatecaCertificateConfigPublicKey", result)

    @builtins.property
    def subject_config(self) -> "PrivatecaCertificateConfigSubjectConfig":
        '''subject_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject_config PrivatecaCertificate#subject_config}
        '''
        result = self._values.get("subject_config")
        assert result is not None, "Required property 'subject_config' is missing"
        return typing.cast("PrivatecaCertificateConfigSubjectConfig", result)

    @builtins.property
    def x509_config(self) -> "PrivatecaCertificateConfigX509Config":
        '''x509_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#x509_config PrivatecaCertificate#x509_config}
        '''
        result = self._values.get("x509_config")
        assert result is not None, "Required property 'x509_config' is missing"
        return typing.cast("PrivatecaCertificateConfigX509Config", result)

    @builtins.property
    def subject_key_id(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigSubjectKeyId"]:
        '''subject_key_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject_key_id PrivatecaCertificate#subject_key_id}
        '''
        result = self._values.get("subject_key_id")
        return typing.cast(typing.Optional["PrivatecaCertificateConfigSubjectKeyId"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abd5804b9aa2258e0d4f3290b734747fd6164512f5debfbdaee45cc544b68580)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPublicKey")
    def put_public_key(
        self,
        *,
        format: builtins.str,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param format: The format of the public key. Currently, only PEM format is supported. Possible values: ["KEY_TYPE_UNSPECIFIED", "PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#format PrivatecaCertificate#format}
        :param key: Required. A public key. When this is specified in a request, the padding and encoding can be any of the options described by the respective 'KeyType' value. When this is generated by the service, it will always be an RFC 5280 SubjectPublicKeyInfo structure containing an algorithm identifier and a key. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key PrivatecaCertificate#key}
        '''
        value = PrivatecaCertificateConfigPublicKey(format=format, key=key)

        return typing.cast(None, jsii.invoke(self, "putPublicKey", [value]))

    @jsii.member(jsii_name="putSubjectConfig")
    def put_subject_config(
        self,
        *,
        subject: typing.Union["PrivatecaCertificateConfigSubjectConfigSubject", typing.Dict[builtins.str, typing.Any]],
        subject_alt_name: typing.Optional[typing.Union["PrivatecaCertificateConfigSubjectConfigSubjectAltName", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject PrivatecaCertificate#subject}
        :param subject_alt_name: subject_alt_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject_alt_name PrivatecaCertificate#subject_alt_name}
        '''
        value = PrivatecaCertificateConfigSubjectConfig(
            subject=subject, subject_alt_name=subject_alt_name
        )

        return typing.cast(None, jsii.invoke(self, "putSubjectConfig", [value]))

    @jsii.member(jsii_name="putSubjectKeyId")
    def put_subject_key_id(
        self,
        *,
        key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_id: The value of the KeyId in lowercase hexadecimal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_id PrivatecaCertificate#key_id}
        '''
        value = PrivatecaCertificateConfigSubjectKeyId(key_id=key_id)

        return typing.cast(None, jsii.invoke(self, "putSubjectKeyId", [value]))

    @jsii.member(jsii_name="putX509Config")
    def put_x509_config(
        self,
        *,
        key_usage: typing.Union["PrivatecaCertificateConfigX509ConfigKeyUsage", typing.Dict[builtins.str, typing.Any]],
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateConfigX509ConfigAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ca_options: typing.Optional[typing.Union["PrivatecaCertificateConfigX509ConfigCaOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name_constraints: typing.Optional[typing.Union["PrivatecaCertificateConfigX509ConfigNameConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateConfigX509ConfigPolicyIds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_usage PrivatecaCertificate#key_usage}
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#additional_extensions PrivatecaCertificate#additional_extensions}
        :param aia_ocsp_servers: Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#aia_ocsp_servers PrivatecaCertificate#aia_ocsp_servers}
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#ca_options PrivatecaCertificate#ca_options}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#name_constraints PrivatecaCertificate#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#policy_ids PrivatecaCertificate#policy_ids}
        '''
        value = PrivatecaCertificateConfigX509Config(
            key_usage=key_usage,
            additional_extensions=additional_extensions,
            aia_ocsp_servers=aia_ocsp_servers,
            ca_options=ca_options,
            name_constraints=name_constraints,
            policy_ids=policy_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putX509Config", [value]))

    @jsii.member(jsii_name="resetSubjectKeyId")
    def reset_subject_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> "PrivatecaCertificateConfigPublicKeyOutputReference":
        return typing.cast("PrivatecaCertificateConfigPublicKeyOutputReference", jsii.get(self, "publicKey"))

    @builtins.property
    @jsii.member(jsii_name="subjectConfig")
    def subject_config(
        self,
    ) -> "PrivatecaCertificateConfigSubjectConfigOutputReference":
        return typing.cast("PrivatecaCertificateConfigSubjectConfigOutputReference", jsii.get(self, "subjectConfig"))

    @builtins.property
    @jsii.member(jsii_name="subjectKeyId")
    def subject_key_id(self) -> "PrivatecaCertificateConfigSubjectKeyIdOutputReference":
        return typing.cast("PrivatecaCertificateConfigSubjectKeyIdOutputReference", jsii.get(self, "subjectKeyId"))

    @builtins.property
    @jsii.member(jsii_name="x509Config")
    def x509_config(self) -> "PrivatecaCertificateConfigX509ConfigOutputReference":
        return typing.cast("PrivatecaCertificateConfigX509ConfigOutputReference", jsii.get(self, "x509Config"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigPublicKey"]:
        return typing.cast(typing.Optional["PrivatecaCertificateConfigPublicKey"], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectConfigInput")
    def subject_config_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigSubjectConfig"]:
        return typing.cast(typing.Optional["PrivatecaCertificateConfigSubjectConfig"], jsii.get(self, "subjectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectKeyIdInput")
    def subject_key_id_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigSubjectKeyId"]:
        return typing.cast(typing.Optional["PrivatecaCertificateConfigSubjectKeyId"], jsii.get(self, "subjectKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="x509ConfigInput")
    def x509_config_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigX509Config"]:
        return typing.cast(typing.Optional["PrivatecaCertificateConfigX509Config"], jsii.get(self, "x509ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PrivatecaCertificateConfigA]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494e7b44d9cbdc0d58986feca972004caca9e0be6bf1c8fba866c51ddb352e6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigPublicKey",
    jsii_struct_bases=[],
    name_mapping={"format": "format", "key": "key"},
)
class PrivatecaCertificateConfigPublicKey:
    def __init__(
        self,
        *,
        format: builtins.str,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param format: The format of the public key. Currently, only PEM format is supported. Possible values: ["KEY_TYPE_UNSPECIFIED", "PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#format PrivatecaCertificate#format}
        :param key: Required. A public key. When this is specified in a request, the padding and encoding can be any of the options described by the respective 'KeyType' value. When this is generated by the service, it will always be an RFC 5280 SubjectPublicKeyInfo structure containing an algorithm identifier and a key. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key PrivatecaCertificate#key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4caf4b80a5bed45807cc09d2a6070c941d631ace51bc518597ae51e9db5bfd)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "format": format,
        }
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def format(self) -> builtins.str:
        '''The format of the public key. Currently, only PEM format is supported. Possible values: ["KEY_TYPE_UNSPECIFIED", "PEM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#format PrivatecaCertificate#format}
        '''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Required.

        A public key. When this is specified in a request, the padding and encoding can be any of the options described by the respective 'KeyType' value. When this is generated by the service, it will always be an RFC 5280 SubjectPublicKeyInfo structure containing an algorithm identifier and a key. A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key PrivatecaCertificate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigPublicKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigPublicKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigPublicKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__861d7d13e0a51f2f0d3b1af9e52167c5dd551d9142156201bfa3ba158bef9275)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d6591f5d1edff155d9949af9babb067b2f8231f7b724266f6f988c68f30e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400ceb1de25ef5cd8a213cf783481f40216733cf57eeb3bbe1288153a38cbb96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PrivatecaCertificateConfigPublicKey]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigPublicKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigPublicKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77a39af7cc29207421028bead0272bbf27ac41e6a163d12ee7fca28d70403fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigSubjectConfig",
    jsii_struct_bases=[],
    name_mapping={"subject": "subject", "subject_alt_name": "subjectAltName"},
)
class PrivatecaCertificateConfigSubjectConfig:
    def __init__(
        self,
        *,
        subject: typing.Union["PrivatecaCertificateConfigSubjectConfigSubject", typing.Dict[builtins.str, typing.Any]],
        subject_alt_name: typing.Optional[typing.Union["PrivatecaCertificateConfigSubjectConfigSubjectAltName", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject PrivatecaCertificate#subject}
        :param subject_alt_name: subject_alt_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject_alt_name PrivatecaCertificate#subject_alt_name}
        '''
        if isinstance(subject, dict):
            subject = PrivatecaCertificateConfigSubjectConfigSubject(**subject)
        if isinstance(subject_alt_name, dict):
            subject_alt_name = PrivatecaCertificateConfigSubjectConfigSubjectAltName(**subject_alt_name)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5cfe4b2a4533722d1af76bf24f9e3e2dd27268b8b7567279afb8b32a688d5b3)
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument subject_alt_name", value=subject_alt_name, expected_type=type_hints["subject_alt_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject": subject,
        }
        if subject_alt_name is not None:
            self._values["subject_alt_name"] = subject_alt_name

    @builtins.property
    def subject(self) -> "PrivatecaCertificateConfigSubjectConfigSubject":
        '''subject block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject PrivatecaCertificate#subject}
        '''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast("PrivatecaCertificateConfigSubjectConfigSubject", result)

    @builtins.property
    def subject_alt_name(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigSubjectConfigSubjectAltName"]:
        '''subject_alt_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#subject_alt_name PrivatecaCertificate#subject_alt_name}
        '''
        result = self._values.get("subject_alt_name")
        return typing.cast(typing.Optional["PrivatecaCertificateConfigSubjectConfigSubjectAltName"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigSubjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigSubjectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigSubjectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a71244f3552ac2783b731a3a195fff7a31770f40be74f7468cbcd16dc6974c01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubject")
    def put_subject(
        self,
        *,
        common_name: builtins.str,
        organization: builtins.str,
        country_code: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        street_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_name: The common name of the distinguished name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#common_name PrivatecaCertificate#common_name}
        :param organization: The organization of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#organization PrivatecaCertificate#organization}
        :param country_code: The country code of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#country_code PrivatecaCertificate#country_code}
        :param locality: The locality or city of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#locality PrivatecaCertificate#locality}
        :param organizational_unit: The organizational unit of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#organizational_unit PrivatecaCertificate#organizational_unit}
        :param postal_code: The postal code of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#postal_code PrivatecaCertificate#postal_code}
        :param province: The province, territory, or regional state of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#province PrivatecaCertificate#province}
        :param street_address: The street address of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#street_address PrivatecaCertificate#street_address}
        '''
        value = PrivatecaCertificateConfigSubjectConfigSubject(
            common_name=common_name,
            organization=organization,
            country_code=country_code,
            locality=locality,
            organizational_unit=organizational_unit,
            postal_code=postal_code,
            province=province,
            street_address=street_address,
        )

        return typing.cast(None, jsii.invoke(self, "putSubject", [value]))

    @jsii.member(jsii_name="putSubjectAltName")
    def put_subject_alt_name(
        self,
        *,
        dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_names: Contains only valid, fully-qualified host names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#dns_names PrivatecaCertificate#dns_names}
        :param email_addresses: Contains only valid RFC 2822 E-mail addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#email_addresses PrivatecaCertificate#email_addresses}
        :param ip_addresses: Contains only valid 32-bit IPv4 addresses or RFC 4291 IPv6 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#ip_addresses PrivatecaCertificate#ip_addresses}
        :param uris: Contains only valid RFC 3986 URIs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#uris PrivatecaCertificate#uris}
        '''
        value = PrivatecaCertificateConfigSubjectConfigSubjectAltName(
            dns_names=dns_names,
            email_addresses=email_addresses,
            ip_addresses=ip_addresses,
            uris=uris,
        )

        return typing.cast(None, jsii.invoke(self, "putSubjectAltName", [value]))

    @jsii.member(jsii_name="resetSubjectAltName")
    def reset_subject_alt_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAltName", []))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(
        self,
    ) -> "PrivatecaCertificateConfigSubjectConfigSubjectOutputReference":
        return typing.cast("PrivatecaCertificateConfigSubjectConfigSubjectOutputReference", jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="subjectAltName")
    def subject_alt_name(
        self,
    ) -> "PrivatecaCertificateConfigSubjectConfigSubjectAltNameOutputReference":
        return typing.cast("PrivatecaCertificateConfigSubjectConfigSubjectAltNameOutputReference", jsii.get(self, "subjectAltName"))

    @builtins.property
    @jsii.member(jsii_name="subjectAltNameInput")
    def subject_alt_name_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigSubjectConfigSubjectAltName"]:
        return typing.cast(typing.Optional["PrivatecaCertificateConfigSubjectConfigSubjectAltName"], jsii.get(self, "subjectAltNameInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigSubjectConfigSubject"]:
        return typing.cast(typing.Optional["PrivatecaCertificateConfigSubjectConfigSubject"], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigSubjectConfig]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigSubjectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigSubjectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d277848deeeac3f4a3d4e94f96621e20fac1ae587d14d058e2d08893d9e436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigSubjectConfigSubject",
    jsii_struct_bases=[],
    name_mapping={
        "common_name": "commonName",
        "organization": "organization",
        "country_code": "countryCode",
        "locality": "locality",
        "organizational_unit": "organizationalUnit",
        "postal_code": "postalCode",
        "province": "province",
        "street_address": "streetAddress",
    },
)
class PrivatecaCertificateConfigSubjectConfigSubject:
    def __init__(
        self,
        *,
        common_name: builtins.str,
        organization: builtins.str,
        country_code: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        street_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_name: The common name of the distinguished name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#common_name PrivatecaCertificate#common_name}
        :param organization: The organization of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#organization PrivatecaCertificate#organization}
        :param country_code: The country code of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#country_code PrivatecaCertificate#country_code}
        :param locality: The locality or city of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#locality PrivatecaCertificate#locality}
        :param organizational_unit: The organizational unit of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#organizational_unit PrivatecaCertificate#organizational_unit}
        :param postal_code: The postal code of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#postal_code PrivatecaCertificate#postal_code}
        :param province: The province, territory, or regional state of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#province PrivatecaCertificate#province}
        :param street_address: The street address of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#street_address PrivatecaCertificate#street_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1146dc160df4fa704efae1608f6a1f0af69ff7441277d2ccc6035429e3c1bc2f)
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
            check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument street_address", value=street_address, expected_type=type_hints["street_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "common_name": common_name,
            "organization": organization,
        }
        if country_code is not None:
            self._values["country_code"] = country_code
        if locality is not None:
            self._values["locality"] = locality
        if organizational_unit is not None:
            self._values["organizational_unit"] = organizational_unit
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if street_address is not None:
            self._values["street_address"] = street_address

    @builtins.property
    def common_name(self) -> builtins.str:
        '''The common name of the distinguished name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#common_name PrivatecaCertificate#common_name}
        '''
        result = self._values.get("common_name")
        assert result is not None, "Required property 'common_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''The organization of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#organization PrivatecaCertificate#organization}
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def country_code(self) -> typing.Optional[builtins.str]:
        '''The country code of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#country_code PrivatecaCertificate#country_code}
        '''
        result = self._values.get("country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''The locality or city of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#locality PrivatecaCertificate#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizational_unit(self) -> typing.Optional[builtins.str]:
        '''The organizational unit of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#organizational_unit PrivatecaCertificate#organizational_unit}
        '''
        result = self._values.get("organizational_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''The postal code of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#postal_code PrivatecaCertificate#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''The province, territory, or regional state of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#province PrivatecaCertificate#province}
        '''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def street_address(self) -> typing.Optional[builtins.str]:
        '''The street address of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#street_address PrivatecaCertificate#street_address}
        '''
        result = self._values.get("street_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigSubjectConfigSubject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigSubjectConfigSubjectAltName",
    jsii_struct_bases=[],
    name_mapping={
        "dns_names": "dnsNames",
        "email_addresses": "emailAddresses",
        "ip_addresses": "ipAddresses",
        "uris": "uris",
    },
)
class PrivatecaCertificateConfigSubjectConfigSubjectAltName:
    def __init__(
        self,
        *,
        dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_names: Contains only valid, fully-qualified host names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#dns_names PrivatecaCertificate#dns_names}
        :param email_addresses: Contains only valid RFC 2822 E-mail addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#email_addresses PrivatecaCertificate#email_addresses}
        :param ip_addresses: Contains only valid 32-bit IPv4 addresses or RFC 4291 IPv6 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#ip_addresses PrivatecaCertificate#ip_addresses}
        :param uris: Contains only valid RFC 3986 URIs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#uris PrivatecaCertificate#uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e238f5dc5e909170b7ac581060b5bc6775365790900be061e706fe63c3d8f069)
            check_type(argname="argument dns_names", value=dns_names, expected_type=type_hints["dns_names"])
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument uris", value=uris, expected_type=type_hints["uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_names is not None:
            self._values["dns_names"] = dns_names
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if uris is not None:
            self._values["uris"] = uris

    @builtins.property
    def dns_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains only valid, fully-qualified host names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#dns_names PrivatecaCertificate#dns_names}
        '''
        result = self._values.get("dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains only valid RFC 2822 E-mail addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#email_addresses PrivatecaCertificate#email_addresses}
        '''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains only valid 32-bit IPv4 addresses or RFC 4291 IPv6 addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#ip_addresses PrivatecaCertificate#ip_addresses}
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains only valid RFC 3986 URIs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#uris PrivatecaCertificate#uris}
        '''
        result = self._values.get("uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigSubjectConfigSubjectAltName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigSubjectConfigSubjectAltNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigSubjectConfigSubjectAltNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0c0d57cb7b84b43ffda753facec61d06a2e90c462cc1d4cd92f4784a0b47763)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDnsNames")
    def reset_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsNames", []))

    @jsii.member(jsii_name="resetEmailAddresses")
    def reset_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddresses", []))

    @jsii.member(jsii_name="resetIpAddresses")
    def reset_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddresses", []))

    @jsii.member(jsii_name="resetUris")
    def reset_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUris", []))

    @builtins.property
    @jsii.member(jsii_name="dnsNamesInput")
    def dns_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressesInput")
    def email_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressesInput")
    def ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="urisInput")
    def uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urisInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsNames")
    def dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsNames"))

    @dns_names.setter
    def dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b135ae74c5634e3c1c68a20c86ca2517d8c25fd228d5e28e0bda86648635536c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca9951913cf5b1441a0070b4d62461c0bba4841541edf345e4672d8bdcd651a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bec014041987995562450456ea9d918ca801932bd3343073757e4a2a8ae163a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uris")
    def uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "uris"))

    @uris.setter
    def uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c8856d253c5c48ba5bb39a9b6bb889433e20f7fc145f73d42c6cb119fb85fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigSubjectConfigSubjectAltName]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigSubjectConfigSubjectAltName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigSubjectConfigSubjectAltName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a758f71b74bd93e0ccd79ac93a4d2722173d85df9209edeb572f844ff45fdfd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateConfigSubjectConfigSubjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigSubjectConfigSubjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__974eb752a70ba66f2c36636e0aac31c3ad61ae118a96775d2e852dddfeeb7a0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCountryCode")
    def reset_country_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountryCode", []))

    @jsii.member(jsii_name="resetLocality")
    def reset_locality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocality", []))

    @jsii.member(jsii_name="resetOrganizationalUnit")
    def reset_organizational_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnit", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetStreetAddress")
    def reset_street_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreetAddress", []))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="localityInput")
    def locality_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitInput")
    def organizational_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="streetAddressInput")
    def street_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streetAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @common_name.setter
    def common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c2e46144737497f0312811ad0e9532501e790577b647596c48de4908a2759a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa04f51c2f1c1411461baee4aa3f6fe78f4cf701a855e7a08405266c690d90f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf76a3d919829fd470c5229b2da6a68d4bf6ea9cbceff6f5c8689dfdbe74094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02107fb315cb252c87192a502b7f380a144814a996a8fe5d47297eaa5eb0d72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationalUnit")
    def organizational_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationalUnit"))

    @organizational_unit.setter
    def organizational_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62baa92df9c700c83cecd0c1ad0d2aa7e6086fc6886eef4ef9f2d190965ea7e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18c11b389c722526a984e117e65c707775ebf0f8b0ae14d25e14d6733074569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686c75e2bc3b191d071bd84a4bd37b36f86f656b5957361a3486ca0ca9b1f9a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streetAddress")
    def street_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streetAddress"))

    @street_address.setter
    def street_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0664135227d7fde55e5204d749ae313e15c4d98f3bf6ce7992f3b8e0a7ab53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streetAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigSubjectConfigSubject]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigSubjectConfigSubject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigSubjectConfigSubject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912142e5f04bae4881bb6c624ac6b9d65091d869f22205465a38932e13443307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigSubjectKeyId",
    jsii_struct_bases=[],
    name_mapping={"key_id": "keyId"},
)
class PrivatecaCertificateConfigSubjectKeyId:
    def __init__(self, *, key_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param key_id: The value of the KeyId in lowercase hexadecimal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_id PrivatecaCertificate#key_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d1dca07e1da962949ca73b6135bdfd66b7891c1ea58fcf60bebc6f620aff96)
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key_id is not None:
            self._values["key_id"] = key_id

    @builtins.property
    def key_id(self) -> typing.Optional[builtins.str]:
        '''The value of the KeyId in lowercase hexadecimal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_id PrivatecaCertificate#key_id}
        '''
        result = self._values.get("key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigSubjectKeyId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigSubjectKeyIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigSubjectKeyIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31bd110b96a67dde735b359ba6c403fe79388272241b321d7bc216120e90433d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyId")
    def reset_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="keyIdInput")
    def key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @key_id.setter
    def key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8bbf5d0a53b1a530a5a3ea91cde75b9f58563c4ea17f9cf61157c565050c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PrivatecaCertificateConfigSubjectKeyId]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigSubjectKeyId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigSubjectKeyId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a7432d2394b91fe5aa6ba0d00b9a2345258e03e1332653e795147f9637d57c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509Config",
    jsii_struct_bases=[],
    name_mapping={
        "key_usage": "keyUsage",
        "additional_extensions": "additionalExtensions",
        "aia_ocsp_servers": "aiaOcspServers",
        "ca_options": "caOptions",
        "name_constraints": "nameConstraints",
        "policy_ids": "policyIds",
    },
)
class PrivatecaCertificateConfigX509Config:
    def __init__(
        self,
        *,
        key_usage: typing.Union["PrivatecaCertificateConfigX509ConfigKeyUsage", typing.Dict[builtins.str, typing.Any]],
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateConfigX509ConfigAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ca_options: typing.Optional[typing.Union["PrivatecaCertificateConfigX509ConfigCaOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name_constraints: typing.Optional[typing.Union["PrivatecaCertificateConfigX509ConfigNameConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateConfigX509ConfigPolicyIds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_usage PrivatecaCertificate#key_usage}
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#additional_extensions PrivatecaCertificate#additional_extensions}
        :param aia_ocsp_servers: Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#aia_ocsp_servers PrivatecaCertificate#aia_ocsp_servers}
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#ca_options PrivatecaCertificate#ca_options}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#name_constraints PrivatecaCertificate#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#policy_ids PrivatecaCertificate#policy_ids}
        '''
        if isinstance(key_usage, dict):
            key_usage = PrivatecaCertificateConfigX509ConfigKeyUsage(**key_usage)
        if isinstance(ca_options, dict):
            ca_options = PrivatecaCertificateConfigX509ConfigCaOptions(**ca_options)
        if isinstance(name_constraints, dict):
            name_constraints = PrivatecaCertificateConfigX509ConfigNameConstraints(**name_constraints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdd1af9b9cc6781f859611551af670e10d55926bf2345d50aa50e31b52d95f9)
            check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            check_type(argname="argument additional_extensions", value=additional_extensions, expected_type=type_hints["additional_extensions"])
            check_type(argname="argument aia_ocsp_servers", value=aia_ocsp_servers, expected_type=type_hints["aia_ocsp_servers"])
            check_type(argname="argument ca_options", value=ca_options, expected_type=type_hints["ca_options"])
            check_type(argname="argument name_constraints", value=name_constraints, expected_type=type_hints["name_constraints"])
            check_type(argname="argument policy_ids", value=policy_ids, expected_type=type_hints["policy_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_usage": key_usage,
        }
        if additional_extensions is not None:
            self._values["additional_extensions"] = additional_extensions
        if aia_ocsp_servers is not None:
            self._values["aia_ocsp_servers"] = aia_ocsp_servers
        if ca_options is not None:
            self._values["ca_options"] = ca_options
        if name_constraints is not None:
            self._values["name_constraints"] = name_constraints
        if policy_ids is not None:
            self._values["policy_ids"] = policy_ids

    @builtins.property
    def key_usage(self) -> "PrivatecaCertificateConfigX509ConfigKeyUsage":
        '''key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_usage PrivatecaCertificate#key_usage}
        '''
        result = self._values.get("key_usage")
        assert result is not None, "Required property 'key_usage' is missing"
        return typing.cast("PrivatecaCertificateConfigX509ConfigKeyUsage", result)

    @builtins.property
    def additional_extensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigAdditionalExtensions"]]]:
        '''additional_extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#additional_extensions PrivatecaCertificate#additional_extensions}
        '''
        result = self._values.get("additional_extensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigAdditionalExtensions"]]], result)

    @builtins.property
    def aia_ocsp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#aia_ocsp_servers PrivatecaCertificate#aia_ocsp_servers}
        '''
        result = self._values.get("aia_ocsp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ca_options(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigX509ConfigCaOptions"]:
        '''ca_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#ca_options PrivatecaCertificate#ca_options}
        '''
        result = self._values.get("ca_options")
        return typing.cast(typing.Optional["PrivatecaCertificateConfigX509ConfigCaOptions"], result)

    @builtins.property
    def name_constraints(
        self,
    ) -> typing.Optional["PrivatecaCertificateConfigX509ConfigNameConstraints"]:
        '''name_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#name_constraints PrivatecaCertificate#name_constraints}
        '''
        result = self._values.get("name_constraints")
        return typing.cast(typing.Optional["PrivatecaCertificateConfigX509ConfigNameConstraints"], result)

    @builtins.property
    def policy_ids(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigPolicyIds"]]]:
        '''policy_ids block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#policy_ids PrivatecaCertificate#policy_ids}
        '''
        result = self._values.get("policy_ids")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigPolicyIds"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigAdditionalExtensions",
    jsii_struct_bases=[],
    name_mapping={"critical": "critical", "object_id": "objectId", "value": "value"},
)
class PrivatecaCertificateConfigX509ConfigAdditionalExtensions:
    def __init__(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        object_id: typing.Union["PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId", typing.Dict[builtins.str, typing.Any]],
        value: builtins.str,
    ) -> None:
        '''
        :param critical: Indicates whether or not this extension is critical (i.e., if the client does not know how to handle this extension, the client should consider this to be an error). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#critical PrivatecaCertificate#critical}
        :param object_id: object_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#object_id PrivatecaCertificate#object_id}
        :param value: The value of this X.509 extension. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#value PrivatecaCertificate#value}
        '''
        if isinstance(object_id, dict):
            object_id = PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId(**object_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00edc685aa572900ec9ecc2c0249e868c8cedbd6f05b89b3e13b12b79b90e5fe)
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "critical": critical,
            "object_id": object_id,
            "value": value,
        }

    @builtins.property
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether or not this extension is critical (i.e., if the client does not know how to handle this extension, the client should consider this to be an error).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#critical PrivatecaCertificate#critical}
        '''
        result = self._values.get("critical")
        assert result is not None, "Required property 'critical' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def object_id(
        self,
    ) -> "PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId":
        '''object_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#object_id PrivatecaCertificate#object_id}
        '''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast("PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId", result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of this X.509 extension. A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#value PrivatecaCertificate#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509ConfigAdditionalExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigX509ConfigAdditionalExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigAdditionalExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe1d42e1e02095119fb4245f42b2bfc8627901462d9d09cce98ea9dfa72aac8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateConfigX509ConfigAdditionalExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a6fb704624d308cdb7139d9c2c07656018718b4df3e3b02044833246d745c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateConfigX509ConfigAdditionalExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fb1e4c3506cfbcbe333bf2e9b7990d5915f02be6e8ac9b033d14b642ef045d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7ad8be0a73298a6214ca2e505ed96c3d37a3394b0e497e38751a775511ea2f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a0c0e35847ac07d18de5b1b5c64f8b0f2337263f047748218e2b39b8f1a63a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigAdditionalExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigAdditionalExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf248c7fc9252307c28b77107fda32e737aec32f303190a3947675f6973c9ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#object_id_path PrivatecaCertificate#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ce2af4863dc02f855cd089b81d95ba42b65ce2edec94e4c013fceaad3a9f12)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#object_id_path PrivatecaCertificate#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c9377a1969b32d1c8d5f464f81a28c077c632c610ecc973e7392deb8d6082a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e020c527c64d54022d809103d0a543c357eefa57d6459cd07faf4b8eb40be4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a63c085b0028b64c6e3d77f886643019df70a429fbe6ad8e08394e61cf7922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateConfigX509ConfigAdditionalExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigAdditionalExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da3d0b94f4d84379eee9828750307852914e4fe899e3e3907bf1c6daea9dc852)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putObjectId")
    def put_object_id(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#object_id_path PrivatecaCertificate#object_id_path}
        '''
        value = PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId(
            object_id_path=object_id_path
        )

        return typing.cast(None, jsii.invoke(self, "putObjectId", [value]))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(
        self,
    ) -> PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectIdOutputReference:
        return typing.cast(PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectIdOutputReference, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "critical"))

    @critical.setter
    def critical(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1bc8f0b7adde3c9e9fa234173eb0c4aaec29074b1d9786967497b2d94d8874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9281944d1fbe2d6db12ec4d4a5cf873c5f606aa62ebd0eb4fc904d150009e4bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigAdditionalExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigAdditionalExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigAdditionalExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62af555f24d4b07715f9f960fc06e5effdb6311cb676228bbd506dba5c9b60bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigCaOptions",
    jsii_struct_bases=[],
    name_mapping={
        "is_ca": "isCa",
        "max_issuer_path_length": "maxIssuerPathLength",
        "non_ca": "nonCa",
        "zero_max_issuer_path_length": "zeroMaxIssuerPathLength",
    },
)
class PrivatecaCertificateConfigX509ConfigCaOptions:
    def __init__(
        self,
        *,
        is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_issuer_path_length: typing.Optional[jsii.Number] = None,
        non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_ca: When true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#is_ca PrivatecaCertificate#is_ca}
        :param max_issuer_path_length: Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#max_issuer_path_length PrivatecaCertificate#max_issuer_path_length}
        :param non_ca: When true, the "CA" in Basic Constraints extension will be set to false. If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#non_ca PrivatecaCertificate#non_ca}
        :param zero_max_issuer_path_length: When true, the "path length constraint" in Basic Constraints extension will be set to 0. if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#zero_max_issuer_path_length PrivatecaCertificate#zero_max_issuer_path_length}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41866f32f1948c30dc6918086533494f4410212df678c55a547a2a4bd564a216)
            check_type(argname="argument is_ca", value=is_ca, expected_type=type_hints["is_ca"])
            check_type(argname="argument max_issuer_path_length", value=max_issuer_path_length, expected_type=type_hints["max_issuer_path_length"])
            check_type(argname="argument non_ca", value=non_ca, expected_type=type_hints["non_ca"])
            check_type(argname="argument zero_max_issuer_path_length", value=zero_max_issuer_path_length, expected_type=type_hints["zero_max_issuer_path_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_ca is not None:
            self._values["is_ca"] = is_ca
        if max_issuer_path_length is not None:
            self._values["max_issuer_path_length"] = max_issuer_path_length
        if non_ca is not None:
            self._values["non_ca"] = non_ca
        if zero_max_issuer_path_length is not None:
            self._values["zero_max_issuer_path_length"] = zero_max_issuer_path_length

    @builtins.property
    def is_ca(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the "CA" in Basic Constraints extension will be set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#is_ca PrivatecaCertificate#is_ca}
        '''
        result = self._values.get("is_ca")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_issuer_path_length(self) -> typing.Optional[jsii.Number]:
        '''Refers to the "path length constraint" in Basic Constraints extension.

        For a CA certificate, this value describes the depth of
        subordinate CA certificates that are allowed. If this value is less than 0, the request will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#max_issuer_path_length PrivatecaCertificate#max_issuer_path_length}
        '''
        result = self._values.get("max_issuer_path_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def non_ca(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the "CA" in Basic Constraints extension will be set to false.

        If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#non_ca PrivatecaCertificate#non_ca}
        '''
        result = self._values.get("non_ca")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def zero_max_issuer_path_length(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the "path length constraint" in Basic Constraints extension will be set to 0.

        if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset,
        the max path length will be omitted from the CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#zero_max_issuer_path_length PrivatecaCertificate#zero_max_issuer_path_length}
        '''
        result = self._values.get("zero_max_issuer_path_length")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509ConfigCaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigX509ConfigCaOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigCaOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__135ee246545026938289493de42593a78f6bda304a3da1b81159732c0b03b2e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsCa")
    def reset_is_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCa", []))

    @jsii.member(jsii_name="resetMaxIssuerPathLength")
    def reset_max_issuer_path_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIssuerPathLength", []))

    @jsii.member(jsii_name="resetNonCa")
    def reset_non_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonCa", []))

    @jsii.member(jsii_name="resetZeroMaxIssuerPathLength")
    def reset_zero_max_issuer_path_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZeroMaxIssuerPathLength", []))

    @builtins.property
    @jsii.member(jsii_name="isCaInput")
    def is_ca_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCaInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIssuerPathLengthInput")
    def max_issuer_path_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIssuerPathLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="nonCaInput")
    def non_ca_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nonCaInput"))

    @builtins.property
    @jsii.member(jsii_name="zeroMaxIssuerPathLengthInput")
    def zero_max_issuer_path_length_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zeroMaxIssuerPathLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="isCa")
    def is_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCa"))

    @is_ca.setter
    def is_ca(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3ad9b889c47f3e816c8c11780793208576231ee5a5adfef71979959848345d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIssuerPathLength")
    def max_issuer_path_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIssuerPathLength"))

    @max_issuer_path_length.setter
    def max_issuer_path_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8e251b5e53e0a93cacf077bb733d88bc239dfa9d4452719a11daa8521d4f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIssuerPathLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonCa")
    def non_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nonCa"))

    @non_ca.setter
    def non_ca(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1995ff5d9bcb07b401e9f300e86d399ecf0e03243cd7127aefbcd418ccae89c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zeroMaxIssuerPathLength")
    def zero_max_issuer_path_length(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zeroMaxIssuerPathLength"))

    @zero_max_issuer_path_length.setter
    def zero_max_issuer_path_length(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca5311dbfec19ba52fc9bf9b39748d18da122c2b4f6029af5c8181a137dbaf4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zeroMaxIssuerPathLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigCaOptions]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigCaOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigX509ConfigCaOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71263875d268a47f93716a2d01b945d1a24474e2131da7a9bd5201c8a98f2ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "base_key_usage": "baseKeyUsage",
        "extended_key_usage": "extendedKeyUsage",
        "unknown_extended_key_usages": "unknownExtendedKeyUsages",
    },
)
class PrivatecaCertificateConfigX509ConfigKeyUsage:
    def __init__(
        self,
        *,
        base_key_usage: typing.Union["PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage", typing.Dict[builtins.str, typing.Any]],
        extended_key_usage: typing.Union["PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage", typing.Dict[builtins.str, typing.Any]],
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#base_key_usage PrivatecaCertificate#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#extended_key_usage PrivatecaCertificate#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#unknown_extended_key_usages PrivatecaCertificate#unknown_extended_key_usages}
        '''
        if isinstance(base_key_usage, dict):
            base_key_usage = PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage(**base_key_usage)
        if isinstance(extended_key_usage, dict):
            extended_key_usage = PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage(**extended_key_usage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32df3578eac79cebfcbdda93ce0104a936a5c6da13cbc932b9c93e42b6d4bc8)
            check_type(argname="argument base_key_usage", value=base_key_usage, expected_type=type_hints["base_key_usage"])
            check_type(argname="argument extended_key_usage", value=extended_key_usage, expected_type=type_hints["extended_key_usage"])
            check_type(argname="argument unknown_extended_key_usages", value=unknown_extended_key_usages, expected_type=type_hints["unknown_extended_key_usages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_key_usage": base_key_usage,
            "extended_key_usage": extended_key_usage,
        }
        if unknown_extended_key_usages is not None:
            self._values["unknown_extended_key_usages"] = unknown_extended_key_usages

    @builtins.property
    def base_key_usage(
        self,
    ) -> "PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage":
        '''base_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#base_key_usage PrivatecaCertificate#base_key_usage}
        '''
        result = self._values.get("base_key_usage")
        assert result is not None, "Required property 'base_key_usage' is missing"
        return typing.cast("PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage", result)

    @builtins.property
    def extended_key_usage(
        self,
    ) -> "PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage":
        '''extended_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#extended_key_usage PrivatecaCertificate#extended_key_usage}
        '''
        result = self._values.get("extended_key_usage")
        assert result is not None, "Required property 'extended_key_usage' is missing"
        return typing.cast("PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage", result)

    @builtins.property
    def unknown_extended_key_usages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages"]]]:
        '''unknown_extended_key_usages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#unknown_extended_key_usages PrivatecaCertificate#unknown_extended_key_usages}
        '''
        result = self._values.get("unknown_extended_key_usages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509ConfigKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "cert_sign": "certSign",
        "content_commitment": "contentCommitment",
        "crl_sign": "crlSign",
        "data_encipherment": "dataEncipherment",
        "decipher_only": "decipherOnly",
        "digital_signature": "digitalSignature",
        "encipher_only": "encipherOnly",
        "key_agreement": "keyAgreement",
        "key_encipherment": "keyEncipherment",
    },
)
class PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage:
    def __init__(
        self,
        *,
        cert_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        content_commitment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crl_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        decipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        digital_signature: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_agreement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#cert_sign PrivatecaCertificate#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#content_commitment PrivatecaCertificate#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#crl_sign PrivatecaCertificate#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#data_encipherment PrivatecaCertificate#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#decipher_only PrivatecaCertificate#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#digital_signature PrivatecaCertificate#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#encipher_only PrivatecaCertificate#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_agreement PrivatecaCertificate#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_encipherment PrivatecaCertificate#key_encipherment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46802d488ce422c9d186e5cd05a8a4b56a8a5aa4753140b11ff1def61688c10d)
            check_type(argname="argument cert_sign", value=cert_sign, expected_type=type_hints["cert_sign"])
            check_type(argname="argument content_commitment", value=content_commitment, expected_type=type_hints["content_commitment"])
            check_type(argname="argument crl_sign", value=crl_sign, expected_type=type_hints["crl_sign"])
            check_type(argname="argument data_encipherment", value=data_encipherment, expected_type=type_hints["data_encipherment"])
            check_type(argname="argument decipher_only", value=decipher_only, expected_type=type_hints["decipher_only"])
            check_type(argname="argument digital_signature", value=digital_signature, expected_type=type_hints["digital_signature"])
            check_type(argname="argument encipher_only", value=encipher_only, expected_type=type_hints["encipher_only"])
            check_type(argname="argument key_agreement", value=key_agreement, expected_type=type_hints["key_agreement"])
            check_type(argname="argument key_encipherment", value=key_encipherment, expected_type=type_hints["key_encipherment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cert_sign is not None:
            self._values["cert_sign"] = cert_sign
        if content_commitment is not None:
            self._values["content_commitment"] = content_commitment
        if crl_sign is not None:
            self._values["crl_sign"] = crl_sign
        if data_encipherment is not None:
            self._values["data_encipherment"] = data_encipherment
        if decipher_only is not None:
            self._values["decipher_only"] = decipher_only
        if digital_signature is not None:
            self._values["digital_signature"] = digital_signature
        if encipher_only is not None:
            self._values["encipher_only"] = encipher_only
        if key_agreement is not None:
            self._values["key_agreement"] = key_agreement
        if key_encipherment is not None:
            self._values["key_encipherment"] = key_encipherment

    @builtins.property
    def cert_sign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to sign certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#cert_sign PrivatecaCertificate#cert_sign}
        '''
        result = self._values.get("cert_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def content_commitment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#content_commitment PrivatecaCertificate#content_commitment}
        '''
        result = self._values.get("content_commitment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crl_sign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used sign certificate revocation lists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#crl_sign PrivatecaCertificate#crl_sign}
        '''
        result = self._values.get("crl_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def data_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#data_encipherment PrivatecaCertificate#data_encipherment}
        '''
        result = self._values.get("data_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def decipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to decipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#decipher_only PrivatecaCertificate#decipher_only}
        '''
        result = self._values.get("decipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def digital_signature(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for digital signatures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#digital_signature PrivatecaCertificate#digital_signature}
        '''
        result = self._values.get("digital_signature")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#encipher_only PrivatecaCertificate#encipher_only}
        '''
        result = self._values.get("encipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_agreement(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used in a key agreement protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_agreement PrivatecaCertificate#key_agreement}
        '''
        result = self._values.get("key_agreement")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher other keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_encipherment PrivatecaCertificate#key_encipherment}
        '''
        result = self._values.get("key_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__631f23e196be8f541e2b1e1743c7892b14434fb91dd7e9709e0327ab944e76aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCertSign")
    def reset_cert_sign(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertSign", []))

    @jsii.member(jsii_name="resetContentCommitment")
    def reset_content_commitment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentCommitment", []))

    @jsii.member(jsii_name="resetCrlSign")
    def reset_crl_sign(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrlSign", []))

    @jsii.member(jsii_name="resetDataEncipherment")
    def reset_data_encipherment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataEncipherment", []))

    @jsii.member(jsii_name="resetDecipherOnly")
    def reset_decipher_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecipherOnly", []))

    @jsii.member(jsii_name="resetDigitalSignature")
    def reset_digital_signature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigitalSignature", []))

    @jsii.member(jsii_name="resetEncipherOnly")
    def reset_encipher_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncipherOnly", []))

    @jsii.member(jsii_name="resetKeyAgreement")
    def reset_key_agreement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyAgreement", []))

    @jsii.member(jsii_name="resetKeyEncipherment")
    def reset_key_encipherment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyEncipherment", []))

    @builtins.property
    @jsii.member(jsii_name="certSignInput")
    def cert_sign_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "certSignInput"))

    @builtins.property
    @jsii.member(jsii_name="contentCommitmentInput")
    def content_commitment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "contentCommitmentInput"))

    @builtins.property
    @jsii.member(jsii_name="crlSignInput")
    def crl_sign_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crlSignInput"))

    @builtins.property
    @jsii.member(jsii_name="dataEnciphermentInput")
    def data_encipherment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dataEnciphermentInput"))

    @builtins.property
    @jsii.member(jsii_name="decipherOnlyInput")
    def decipher_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "decipherOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="digitalSignatureInput")
    def digital_signature_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "digitalSignatureInput"))

    @builtins.property
    @jsii.member(jsii_name="encipherOnlyInput")
    def encipher_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encipherOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAgreementInput")
    def key_agreement_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keyAgreementInput"))

    @builtins.property
    @jsii.member(jsii_name="keyEnciphermentInput")
    def key_encipherment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keyEnciphermentInput"))

    @builtins.property
    @jsii.member(jsii_name="certSign")
    def cert_sign(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "certSign"))

    @cert_sign.setter
    def cert_sign(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd7e354b0659de08d43ee62b0f115e043ad1503a31c37fcb4a713306b457fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certSign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentCommitment")
    def content_commitment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "contentCommitment"))

    @content_commitment.setter
    def content_commitment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84164b51db87552ee72e72c68696674da7d153ee143d726d9163b9e5c94cfa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentCommitment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crlSign")
    def crl_sign(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crlSign"))

    @crl_sign.setter
    def crl_sign(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a5c526696df082c2a121681900b1a7e0f32a81e3e19870a018974510539e113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crlSign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataEncipherment")
    def data_encipherment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dataEncipherment"))

    @data_encipherment.setter
    def data_encipherment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ffcf589a72cd7e7ad06eacb6989456b88a56274502e52e98fe65ca8bfcecee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataEncipherment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="decipherOnly")
    def decipher_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "decipherOnly"))

    @decipher_only.setter
    def decipher_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffc8f1a42a0e90dcc2b2fe84b526c0654569116cac2d3ad09cff2fd460cb7b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "decipherOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="digitalSignature")
    def digital_signature(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "digitalSignature"))

    @digital_signature.setter
    def digital_signature(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b5a03fb882ac60ea2005eca4f59b0cf59daedb84fcccc1c8ad8b3de1ec423e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digitalSignature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encipherOnly")
    def encipher_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encipherOnly"))

    @encipher_only.setter
    def encipher_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67b2f98674141ed7078d1f0f476e263e9157b91576007107ce404b04a129d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encipherOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAgreement")
    def key_agreement(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keyAgreement"))

    @key_agreement.setter
    def key_agreement(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d4d6b4230785243e788697c62b028ee76e7b2510d63fd4dddb49a400be2f17a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAgreement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyEncipherment")
    def key_encipherment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keyEncipherment"))

    @key_encipherment.setter
    def key_encipherment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf631343ca4a813160c277a865dff37fa236ff7833c3ca8184f534ed8bb0147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyEncipherment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07df6d07572dc8b493d9b954046a875c0f8e02d70e21798108f4f1076c7dd0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "client_auth": "clientAuth",
        "code_signing": "codeSigning",
        "email_protection": "emailProtection",
        "ocsp_signing": "ocspSigning",
        "server_auth": "serverAuth",
        "time_stamping": "timeStamping",
    },
)
class PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage:
    def __init__(
        self,
        *,
        client_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ocsp_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_stamping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#client_auth PrivatecaCertificate#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#code_signing PrivatecaCertificate#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#email_protection PrivatecaCertificate#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#ocsp_signing PrivatecaCertificate#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#server_auth PrivatecaCertificate#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#time_stamping PrivatecaCertificate#time_stamping}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ae6f808cf2572bcf3bdb84a11a2dafcba0a76844bc3ab312a7c375565a27b5)
            check_type(argname="argument client_auth", value=client_auth, expected_type=type_hints["client_auth"])
            check_type(argname="argument code_signing", value=code_signing, expected_type=type_hints["code_signing"])
            check_type(argname="argument email_protection", value=email_protection, expected_type=type_hints["email_protection"])
            check_type(argname="argument ocsp_signing", value=ocsp_signing, expected_type=type_hints["ocsp_signing"])
            check_type(argname="argument server_auth", value=server_auth, expected_type=type_hints["server_auth"])
            check_type(argname="argument time_stamping", value=time_stamping, expected_type=type_hints["time_stamping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_auth is not None:
            self._values["client_auth"] = client_auth
        if code_signing is not None:
            self._values["code_signing"] = code_signing
        if email_protection is not None:
            self._values["email_protection"] = email_protection
        if ocsp_signing is not None:
            self._values["ocsp_signing"] = ocsp_signing
        if server_auth is not None:
            self._values["server_auth"] = server_auth
        if time_stamping is not None:
            self._values["time_stamping"] = time_stamping

    @builtins.property
    def client_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#client_auth PrivatecaCertificate#client_auth}
        '''
        result = self._values.get("client_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def code_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#code_signing PrivatecaCertificate#code_signing}
        '''
        result = self._values.get("code_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def email_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#email_protection PrivatecaCertificate#email_protection}
        '''
        result = self._values.get("email_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ocsp_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#ocsp_signing PrivatecaCertificate#ocsp_signing}
        '''
        result = self._values.get("ocsp_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def server_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#server_auth PrivatecaCertificate#server_auth}
        '''
        result = self._values.get("server_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_stamping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#time_stamping PrivatecaCertificate#time_stamping}
        '''
        result = self._values.get("time_stamping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6ab4655095e3d8736579d1f9d2131a53ce73184823014899710618b01a8e15f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientAuth")
    def reset_client_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientAuth", []))

    @jsii.member(jsii_name="resetCodeSigning")
    def reset_code_signing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeSigning", []))

    @jsii.member(jsii_name="resetEmailProtection")
    def reset_email_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailProtection", []))

    @jsii.member(jsii_name="resetOcspSigning")
    def reset_ocsp_signing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcspSigning", []))

    @jsii.member(jsii_name="resetServerAuth")
    def reset_server_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerAuth", []))

    @jsii.member(jsii_name="resetTimeStamping")
    def reset_time_stamping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeStamping", []))

    @builtins.property
    @jsii.member(jsii_name="clientAuthInput")
    def client_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="codeSigningInput")
    def code_signing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "codeSigningInput"))

    @builtins.property
    @jsii.member(jsii_name="emailProtectionInput")
    def email_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "emailProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="ocspSigningInput")
    def ocsp_signing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ocspSigningInput"))

    @builtins.property
    @jsii.member(jsii_name="serverAuthInput")
    def server_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "serverAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="timeStampingInput")
    def time_stamping_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeStampingInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAuth")
    def client_auth(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientAuth"))

    @client_auth.setter
    def client_auth(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79727a60056c0fdb14fe73da18f54d29afdf3c9b96cacd24c42b1c0c1e713aa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeSigning")
    def code_signing(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "codeSigning"))

    @code_signing.setter
    def code_signing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b288de985187488184d8c9db71397532162f9adf5146006d70a3a513f216aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeSigning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailProtection")
    def email_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "emailProtection"))

    @email_protection.setter
    def email_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722772725ae6753e3b38d28e4902856d82e3cc4abe8e5a9f47487924c63eee80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ocspSigning")
    def ocsp_signing(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ocspSigning"))

    @ocsp_signing.setter
    def ocsp_signing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562f9422916cd0af75d798426487a49d22c69e224eb1a727aab754b6ace2af43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ocspSigning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverAuth")
    def server_auth(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "serverAuth"))

    @server_auth.setter
    def server_auth(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eeefbb4175f8e1f7e03ce9df8a4aeed010d294e5f1cde01dbd867fc14b29e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeStamping")
    def time_stamping(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "timeStamping"))

    @time_stamping.setter
    def time_stamping(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9121de694afa1ceaf3fe4ebe83e4b02d24e95a9e542093ec24e9aad2cdeedf04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeStamping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae09f9433cd5eec6901c37dd6a1e8fd36643b326cdde27f977863e6351b7fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateConfigX509ConfigKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e682020ec0d765b963fc16f2313001c125557753c5903379bd6d053fd7a4ca0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBaseKeyUsage")
    def put_base_key_usage(
        self,
        *,
        cert_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        content_commitment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crl_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        decipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        digital_signature: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_agreement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#cert_sign PrivatecaCertificate#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#content_commitment PrivatecaCertificate#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#crl_sign PrivatecaCertificate#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#data_encipherment PrivatecaCertificate#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#decipher_only PrivatecaCertificate#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#digital_signature PrivatecaCertificate#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#encipher_only PrivatecaCertificate#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_agreement PrivatecaCertificate#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#key_encipherment PrivatecaCertificate#key_encipherment}
        '''
        value = PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage(
            cert_sign=cert_sign,
            content_commitment=content_commitment,
            crl_sign=crl_sign,
            data_encipherment=data_encipherment,
            decipher_only=decipher_only,
            digital_signature=digital_signature,
            encipher_only=encipher_only,
            key_agreement=key_agreement,
            key_encipherment=key_encipherment,
        )

        return typing.cast(None, jsii.invoke(self, "putBaseKeyUsage", [value]))

    @jsii.member(jsii_name="putExtendedKeyUsage")
    def put_extended_key_usage(
        self,
        *,
        client_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ocsp_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_stamping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#client_auth PrivatecaCertificate#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#code_signing PrivatecaCertificate#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#email_protection PrivatecaCertificate#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#ocsp_signing PrivatecaCertificate#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#server_auth PrivatecaCertificate#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#time_stamping PrivatecaCertificate#time_stamping}
        '''
        value = PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage(
            client_auth=client_auth,
            code_signing=code_signing,
            email_protection=email_protection,
            ocsp_signing=ocsp_signing,
            server_auth=server_auth,
            time_stamping=time_stamping,
        )

        return typing.cast(None, jsii.invoke(self, "putExtendedKeyUsage", [value]))

    @jsii.member(jsii_name="putUnknownExtendedKeyUsages")
    def put_unknown_extended_key_usages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afec427c694c7649c6efd2d63e5270ede0cecd247e057122967614d41d68118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUnknownExtendedKeyUsages", [value]))

    @jsii.member(jsii_name="resetUnknownExtendedKeyUsages")
    def reset_unknown_extended_key_usages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnknownExtendedKeyUsages", []))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsage")
    def base_key_usage(
        self,
    ) -> PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsageOutputReference:
        return typing.cast(PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsageOutputReference, jsii.get(self, "baseKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsage")
    def extended_key_usage(
        self,
    ) -> PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference:
        return typing.cast(PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference, jsii.get(self, "extendedKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsages")
    def unknown_extended_key_usages(
        self,
    ) -> "PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList":
        return typing.cast("PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList", jsii.get(self, "unknownExtendedKeyUsages"))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsageInput")
    def base_key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage], jsii.get(self, "baseKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsageInput")
    def extended_key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage], jsii.get(self, "extendedKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsagesInput")
    def unknown_extended_key_usages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages"]]], jsii.get(self, "unknownExtendedKeyUsagesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a528ce33de37353f7f80eb3879b5826ba8b39fbf0bd0f65c1387330811e93a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#object_id_path PrivatecaCertificate#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56d9a388d7964d34008b3a99fd51f56897534a07261f37431b4cd43ba002de2)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#object_id_path PrivatecaCertificate#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fdd202136669ef50ee38a2220a33103727f2d2cbf445cc6bc21b4f83ab8a4d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d1adf946af559b8243f8f67cdb3b4e529c7753acb2cb0e82e2a98c59d82108)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4395cb32a3483789a735cc9b9c6a6fc3db6bec8c44b60d5748a2aef650a7c4f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82846c2dc4f0007cd77750dea0e24a52eb0a7986aec1d2c5d2a82fbc11b8fd5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34a7c085a0caae397f36ce0ea92dac910ed2dcf85470c028af53a02e39c7329f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0782c82fb9647dcbf3c184bbda2d0b6141c3528148ad53a3fafb48cacfdc4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73c4685c2b5dee96d067aaeecef968e886513bd7ba879e910b4b1f5ea10c6225)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40a9bd5c86304c607203a20c25c0d4b7e97c53c2c2a7cf97f929e12eb2b5196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c75eec05739719eeecfc2a9ff928d1e18c68eeb3f14c98ff56dc1d02df54660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigNameConstraints",
    jsii_struct_bases=[],
    name_mapping={
        "critical": "critical",
        "excluded_dns_names": "excludedDnsNames",
        "excluded_email_addresses": "excludedEmailAddresses",
        "excluded_ip_ranges": "excludedIpRanges",
        "excluded_uris": "excludedUris",
        "permitted_dns_names": "permittedDnsNames",
        "permitted_email_addresses": "permittedEmailAddresses",
        "permitted_ip_ranges": "permittedIpRanges",
        "permitted_uris": "permittedUris",
    },
)
class PrivatecaCertificateConfigX509ConfigNameConstraints:
    def __init__(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        excluded_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#critical PrivatecaCertificate#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_dns_names PrivatecaCertificate#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_email_addresses PrivatecaCertificate#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_ip_ranges PrivatecaCertificate#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_uris PrivatecaCertificate#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_dns_names PrivatecaCertificate#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_email_addresses PrivatecaCertificate#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_ip_ranges PrivatecaCertificate#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_uris PrivatecaCertificate#permitted_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a699b1366899f8a4e198ceea47619367826c66cb9ce29d1e38858661587fd96)
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument excluded_dns_names", value=excluded_dns_names, expected_type=type_hints["excluded_dns_names"])
            check_type(argname="argument excluded_email_addresses", value=excluded_email_addresses, expected_type=type_hints["excluded_email_addresses"])
            check_type(argname="argument excluded_ip_ranges", value=excluded_ip_ranges, expected_type=type_hints["excluded_ip_ranges"])
            check_type(argname="argument excluded_uris", value=excluded_uris, expected_type=type_hints["excluded_uris"])
            check_type(argname="argument permitted_dns_names", value=permitted_dns_names, expected_type=type_hints["permitted_dns_names"])
            check_type(argname="argument permitted_email_addresses", value=permitted_email_addresses, expected_type=type_hints["permitted_email_addresses"])
            check_type(argname="argument permitted_ip_ranges", value=permitted_ip_ranges, expected_type=type_hints["permitted_ip_ranges"])
            check_type(argname="argument permitted_uris", value=permitted_uris, expected_type=type_hints["permitted_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "critical": critical,
        }
        if excluded_dns_names is not None:
            self._values["excluded_dns_names"] = excluded_dns_names
        if excluded_email_addresses is not None:
            self._values["excluded_email_addresses"] = excluded_email_addresses
        if excluded_ip_ranges is not None:
            self._values["excluded_ip_ranges"] = excluded_ip_ranges
        if excluded_uris is not None:
            self._values["excluded_uris"] = excluded_uris
        if permitted_dns_names is not None:
            self._values["permitted_dns_names"] = permitted_dns_names
        if permitted_email_addresses is not None:
            self._values["permitted_email_addresses"] = permitted_email_addresses
        if permitted_ip_ranges is not None:
            self._values["permitted_ip_ranges"] = permitted_ip_ranges
        if permitted_uris is not None:
            self._values["permitted_uris"] = permitted_uris

    @builtins.property
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether or not the name constraints are marked critical.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#critical PrivatecaCertificate#critical}
        '''
        result = self._values.get("critical")
        assert result is not None, "Required property 'critical' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def excluded_dns_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains excluded DNS names.

        Any DNS name that can be
        constructed by simply adding zero or more labels to
        the left-hand side of the name satisfies the name constraint.
        For example, 'example.com', 'www.example.com', 'www.sub.example.com'
        would satisfy 'example.com' while 'example1.com' does not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_dns_names PrivatecaCertificate#excluded_dns_names}
        '''
        result = self._values.get("excluded_dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded email addresses.

        The value can be a particular
        email address, a hostname to indicate all email addresses on that host or
        a domain with a leading period (e.g. '.example.com') to indicate
        all email addresses in that domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_email_addresses PrivatecaCertificate#excluded_email_addresses}
        '''
        result = self._values.get("excluded_email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded IP ranges.

        For IPv4 addresses, the ranges
        are expressed using CIDR notation as specified in RFC 4632.
        For IPv6 addresses, the ranges are expressed in similar encoding as IPv4
        addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_ip_ranges PrivatecaCertificate#excluded_ip_ranges}
        '''
        result = self._values.get("excluded_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_uris PrivatecaCertificate#excluded_uris}
        '''
        result = self._values.get("excluded_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_dns_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains permitted DNS names.

        Any DNS name that can be
        constructed by simply adding zero or more labels to
        the left-hand side of the name satisfies the name constraint.
        For example, 'example.com', 'www.example.com', 'www.sub.example.com'
        would satisfy 'example.com' while 'example1.com' does not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_dns_names PrivatecaCertificate#permitted_dns_names}
        '''
        result = self._values.get("permitted_dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted email addresses.

        The value can be a particular
        email address, a hostname to indicate all email addresses on that host or
        a domain with a leading period (e.g. '.example.com') to indicate
        all email addresses in that domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_email_addresses PrivatecaCertificate#permitted_email_addresses}
        '''
        result = self._values.get("permitted_email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted IP ranges.

        For IPv4 addresses, the ranges
        are expressed using CIDR notation as specified in RFC 4632.
        For IPv6 addresses, the ranges are expressed in similar encoding as IPv4
        addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_ip_ranges PrivatecaCertificate#permitted_ip_ranges}
        '''
        result = self._values.get("permitted_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_uris PrivatecaCertificate#permitted_uris}
        '''
        result = self._values.get("permitted_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509ConfigNameConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigX509ConfigNameConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigNameConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e665309a521d025c0d26a6f6e6233f332ab2293e3738dede33a64bfe40f0d59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedDnsNames")
    def reset_excluded_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedDnsNames", []))

    @jsii.member(jsii_name="resetExcludedEmailAddresses")
    def reset_excluded_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedEmailAddresses", []))

    @jsii.member(jsii_name="resetExcludedIpRanges")
    def reset_excluded_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedIpRanges", []))

    @jsii.member(jsii_name="resetExcludedUris")
    def reset_excluded_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedUris", []))

    @jsii.member(jsii_name="resetPermittedDnsNames")
    def reset_permitted_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedDnsNames", []))

    @jsii.member(jsii_name="resetPermittedEmailAddresses")
    def reset_permitted_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedEmailAddresses", []))

    @jsii.member(jsii_name="resetPermittedIpRanges")
    def reset_permitted_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedIpRanges", []))

    @jsii.member(jsii_name="resetPermittedUris")
    def reset_permitted_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedUris", []))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedDnsNamesInput")
    def excluded_dns_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedDnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedEmailAddressesInput")
    def excluded_email_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedEmailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedIpRangesInput")
    def excluded_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedUrisInput")
    def excluded_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedDnsNamesInput")
    def permitted_dns_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedDnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedEmailAddressesInput")
    def permitted_email_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedEmailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedIpRangesInput")
    def permitted_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedUrisInput")
    def permitted_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "critical"))

    @critical.setter
    def critical(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5c1d8061cdafa67ce59f03295a8071355eb678df9079bf0fe8cf862e2d4279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedDnsNames")
    def excluded_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedDnsNames"))

    @excluded_dns_names.setter
    def excluded_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a56e1661afdfa6264c412358fe74f87a1ae3f8ec197c6fbb5efb479e03e1f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedEmailAddresses")
    def excluded_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedEmailAddresses"))

    @excluded_email_addresses.setter
    def excluded_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1560dd20ca3d46c3b48ea664544605628ac8e4d4541db9c9d0236d9f5af4dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedIpRanges")
    def excluded_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedIpRanges"))

    @excluded_ip_ranges.setter
    def excluded_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653d875147013a12e10d3dcf0396bba6d978fb2cfeb0fce17e80870668697eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedUris")
    def excluded_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedUris"))

    @excluded_uris.setter
    def excluded_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b40a40197dca2ce72fd6c366098af40ab3313127161b3b80d0017ecb425a4624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedDnsNames")
    def permitted_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedDnsNames"))

    @permitted_dns_names.setter
    def permitted_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d61666d7d09a58a295e4bfbad8c644b5f715bbe87d61f779f1327570d48b49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedEmailAddresses")
    def permitted_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedEmailAddresses"))

    @permitted_email_addresses.setter
    def permitted_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2ed9ffdb7b46cfa0ea0e105c1267fc002d96d8f2f06bb5952db316428c3120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedIpRanges")
    def permitted_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedIpRanges"))

    @permitted_ip_ranges.setter
    def permitted_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742ed012c374d90d4895c67264361a5ffa2f48982afd00fec95079e3ff1e991e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedUris")
    def permitted_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedUris"))

    @permitted_uris.setter
    def permitted_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ba5fccfc0d64ec531617cda602ca3131e83c17e8b82d3483bd999950df3a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigNameConstraints]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigNameConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigX509ConfigNameConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a8b57b9beb218b25cb0b93cf621fe3489770374954d23c05de61bbeca5b0cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateConfigX509ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98d3d34badad54f73ed784964e76a5a677feaa9c09c2246ac74e8ccaaa70749d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalExtensions")
    def put_additional_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateConfigX509ConfigAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9b08ac8a734c15e89cc3bb367c51046a42f3dbfd7381ad86dd53c618780b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalExtensions", [value]))

    @jsii.member(jsii_name="putCaOptions")
    def put_ca_options(
        self,
        *,
        is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_issuer_path_length: typing.Optional[jsii.Number] = None,
        non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_ca: When true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#is_ca PrivatecaCertificate#is_ca}
        :param max_issuer_path_length: Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#max_issuer_path_length PrivatecaCertificate#max_issuer_path_length}
        :param non_ca: When true, the "CA" in Basic Constraints extension will be set to false. If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#non_ca PrivatecaCertificate#non_ca}
        :param zero_max_issuer_path_length: When true, the "path length constraint" in Basic Constraints extension will be set to 0. if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#zero_max_issuer_path_length PrivatecaCertificate#zero_max_issuer_path_length}
        '''
        value = PrivatecaCertificateConfigX509ConfigCaOptions(
            is_ca=is_ca,
            max_issuer_path_length=max_issuer_path_length,
            non_ca=non_ca,
            zero_max_issuer_path_length=zero_max_issuer_path_length,
        )

        return typing.cast(None, jsii.invoke(self, "putCaOptions", [value]))

    @jsii.member(jsii_name="putKeyUsage")
    def put_key_usage(
        self,
        *,
        base_key_usage: typing.Union[PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]],
        extended_key_usage: typing.Union[PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]],
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#base_key_usage PrivatecaCertificate#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#extended_key_usage PrivatecaCertificate#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#unknown_extended_key_usages PrivatecaCertificate#unknown_extended_key_usages}
        '''
        value = PrivatecaCertificateConfigX509ConfigKeyUsage(
            base_key_usage=base_key_usage,
            extended_key_usage=extended_key_usage,
            unknown_extended_key_usages=unknown_extended_key_usages,
        )

        return typing.cast(None, jsii.invoke(self, "putKeyUsage", [value]))

    @jsii.member(jsii_name="putNameConstraints")
    def put_name_constraints(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        excluded_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#critical PrivatecaCertificate#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_dns_names PrivatecaCertificate#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_email_addresses PrivatecaCertificate#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_ip_ranges PrivatecaCertificate#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#excluded_uris PrivatecaCertificate#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_dns_names PrivatecaCertificate#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_email_addresses PrivatecaCertificate#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_ip_ranges PrivatecaCertificate#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#permitted_uris PrivatecaCertificate#permitted_uris}
        '''
        value = PrivatecaCertificateConfigX509ConfigNameConstraints(
            critical=critical,
            excluded_dns_names=excluded_dns_names,
            excluded_email_addresses=excluded_email_addresses,
            excluded_ip_ranges=excluded_ip_ranges,
            excluded_uris=excluded_uris,
            permitted_dns_names=permitted_dns_names,
            permitted_email_addresses=permitted_email_addresses,
            permitted_ip_ranges=permitted_ip_ranges,
            permitted_uris=permitted_uris,
        )

        return typing.cast(None, jsii.invoke(self, "putNameConstraints", [value]))

    @jsii.member(jsii_name="putPolicyIds")
    def put_policy_ids(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateConfigX509ConfigPolicyIds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d536f55db18101d9180883a55a90d0cfbe42869aff1030961d6ec52dc31fee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyIds", [value]))

    @jsii.member(jsii_name="resetAdditionalExtensions")
    def reset_additional_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalExtensions", []))

    @jsii.member(jsii_name="resetAiaOcspServers")
    def reset_aia_ocsp_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAiaOcspServers", []))

    @jsii.member(jsii_name="resetCaOptions")
    def reset_ca_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaOptions", []))

    @jsii.member(jsii_name="resetNameConstraints")
    def reset_name_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameConstraints", []))

    @jsii.member(jsii_name="resetPolicyIds")
    def reset_policy_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyIds", []))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensions")
    def additional_extensions(
        self,
    ) -> PrivatecaCertificateConfigX509ConfigAdditionalExtensionsList:
        return typing.cast(PrivatecaCertificateConfigX509ConfigAdditionalExtensionsList, jsii.get(self, "additionalExtensions"))

    @builtins.property
    @jsii.member(jsii_name="caOptions")
    def ca_options(
        self,
    ) -> PrivatecaCertificateConfigX509ConfigCaOptionsOutputReference:
        return typing.cast(PrivatecaCertificateConfigX509ConfigCaOptionsOutputReference, jsii.get(self, "caOptions"))

    @builtins.property
    @jsii.member(jsii_name="keyUsage")
    def key_usage(self) -> PrivatecaCertificateConfigX509ConfigKeyUsageOutputReference:
        return typing.cast(PrivatecaCertificateConfigX509ConfigKeyUsageOutputReference, jsii.get(self, "keyUsage"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraints")
    def name_constraints(
        self,
    ) -> PrivatecaCertificateConfigX509ConfigNameConstraintsOutputReference:
        return typing.cast(PrivatecaCertificateConfigX509ConfigNameConstraintsOutputReference, jsii.get(self, "nameConstraints"))

    @builtins.property
    @jsii.member(jsii_name="policyIds")
    def policy_ids(self) -> "PrivatecaCertificateConfigX509ConfigPolicyIdsList":
        return typing.cast("PrivatecaCertificateConfigX509ConfigPolicyIdsList", jsii.get(self, "policyIds"))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensionsInput")
    def additional_extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigAdditionalExtensions]]], jsii.get(self, "additionalExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServersInput")
    def aia_ocsp_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aiaOcspServersInput"))

    @builtins.property
    @jsii.member(jsii_name="caOptionsInput")
    def ca_options_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigCaOptions]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigCaOptions], jsii.get(self, "caOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyUsageInput")
    def key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsage], jsii.get(self, "keyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraintsInput")
    def name_constraints_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateConfigX509ConfigNameConstraints]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509ConfigNameConstraints], jsii.get(self, "nameConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdsInput")
    def policy_ids_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigPolicyIds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateConfigX509ConfigPolicyIds"]]], jsii.get(self, "policyIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServers")
    def aia_ocsp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aiaOcspServers"))

    @aia_ocsp_servers.setter
    def aia_ocsp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7fe8793ef853ac3ccbaad34f01ae7ef4c769a144778b6be211504a4e90111f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aiaOcspServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PrivatecaCertificateConfigX509Config]:
        return typing.cast(typing.Optional[PrivatecaCertificateConfigX509Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateConfigX509Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8b4fbf4367c793c741da3c35a4c01a02658f123f2e584dc3838a990acfaf2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigPolicyIds",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateConfigX509ConfigPolicyIds:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#object_id_path PrivatecaCertificate#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e2609527fa27d81792c16eaa200d4cbad45a097313bdc37101c6ef83c9808a)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#object_id_path PrivatecaCertificate#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateConfigX509ConfigPolicyIds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateConfigX509ConfigPolicyIdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigPolicyIdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8fc76ecc403163d39b6257569b60e982ec6af9a565b1158aae18dd687190068)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateConfigX509ConfigPolicyIdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e322d2754a67fcaf215e632c6a9cd3b97e2b4d87b01e6d098d13129d63720edd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateConfigX509ConfigPolicyIdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479cbce77195deac6746d512ed73fde92654187d14539b470f06d09085a5808e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81cf0f905cbafff2694469e75c87f8b032c3ab521c1bdd9f1f3b25f5612e3196)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7c10238b1338123ba106b6f98bc099d92a8d0de1f97c39ca8b9e847d2e7f00c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigPolicyIds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigPolicyIds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigPolicyIds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d60385208493d3c4b12db07facc27833f123b6113a87f4eff775072ac6f0965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateConfigX509ConfigPolicyIdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateConfigX509ConfigPolicyIdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f88752150dcada2d73f00b2a0a20d30f18905025b03c7a19dd6798baf3e7b2e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfa72f634af028fbb0a38bb510960f4af65b77cc10a3148386f96d807de453c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigPolicyIds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigPolicyIds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigPolicyIds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c921d23052f20991a65b815f4e83f34b3458cde162dc9f50d5cadf09c62cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateRevocationDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateRevocationDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateRevocationDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateRevocationDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateRevocationDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1aa236e1c0a003401df7b039649e4dff8efe40f160b08896f5effe26c02ee0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateRevocationDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308a8bf44a67e19a61af3aea28471b3e2064d9a6af919046f0be56de64b15c60)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateRevocationDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b250ff69808acf272b31c6424ecb1bdfe70c66dc674176d08b4ae0bb58d9a5fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c159c828ac5cd7dbbfc74f58ccb680b9de03622cfd6572fc1d4eba6ca9788656)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8aa4f97bfcceea7ce3d8142ae94b7c41fbf31615ca6bffec2a151d9ea1cf29c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateRevocationDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateRevocationDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd4b0303d3b430e6a99ecd3af652e41fbb74521ebb8f13ce5d16e3012f0c4493)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="revocationState")
    def revocation_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revocationState"))

    @builtins.property
    @jsii.member(jsii_name="revocationTime")
    def revocation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revocationTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PrivatecaCertificateRevocationDetails]:
        return typing.cast(typing.Optional[PrivatecaCertificateRevocationDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateRevocationDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d44dd4d6c003308ccd11a828dba6ea60248fee22effa4f5936f6ebad18a4f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PrivatecaCertificateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#create PrivatecaCertificate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#delete PrivatecaCertificate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#update PrivatecaCertificate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7ef8b440b93769a669866adf09785bb03b8ebd56862f3ebf234bab74912c5f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#create PrivatecaCertificate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#delete PrivatecaCertificate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate#update PrivatecaCertificate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificate.PrivatecaCertificateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f42db0f588cbdd2eaec56dfd253344076acc96ff17184a2217ffb19e9d1172bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bbff2b5c582104ed381e8446a420c70359a24bd59a7db9b9212949dbde3141e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88dde5f2c0ec29a5b2d925b2f41bd77e7c68ddf434f6427e832aabd340964a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d76ca036851326a725390d61dfe1ac272ed91706af9c1878732ee80b9e4da5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9385a7139af82555c77a0883a2b37d4af5086553efc20dc893fb7a353fc7940d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PrivatecaCertificate",
    "PrivatecaCertificateCertificateDescription",
    "PrivatecaCertificateCertificateDescriptionAuthorityKeyId",
    "PrivatecaCertificateCertificateDescriptionAuthorityKeyIdList",
    "PrivatecaCertificateCertificateDescriptionAuthorityKeyIdOutputReference",
    "PrivatecaCertificateCertificateDescriptionCertFingerprint",
    "PrivatecaCertificateCertificateDescriptionCertFingerprintList",
    "PrivatecaCertificateCertificateDescriptionCertFingerprintOutputReference",
    "PrivatecaCertificateCertificateDescriptionList",
    "PrivatecaCertificateCertificateDescriptionOutputReference",
    "PrivatecaCertificateCertificateDescriptionPublicKey",
    "PrivatecaCertificateCertificateDescriptionPublicKeyList",
    "PrivatecaCertificateCertificateDescriptionPublicKeyOutputReference",
    "PrivatecaCertificateCertificateDescriptionSubjectDescription",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionList",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionOutputReference",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubject",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltName",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSans",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansList",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectId",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdList",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectIdOutputReference",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansOutputReference",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameList",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameOutputReference",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectList",
    "PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectOutputReference",
    "PrivatecaCertificateCertificateDescriptionSubjectKeyId",
    "PrivatecaCertificateCertificateDescriptionSubjectKeyIdList",
    "PrivatecaCertificateCertificateDescriptionSubjectKeyIdOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509Description",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensions",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectId",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectIdOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptions",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptionsOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsage",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsage",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsageOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsage",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsageOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsages",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsagesOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraints",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraintsOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionOutputReference",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIds",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsList",
    "PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIdsOutputReference",
    "PrivatecaCertificateConfig",
    "PrivatecaCertificateConfigA",
    "PrivatecaCertificateConfigAOutputReference",
    "PrivatecaCertificateConfigPublicKey",
    "PrivatecaCertificateConfigPublicKeyOutputReference",
    "PrivatecaCertificateConfigSubjectConfig",
    "PrivatecaCertificateConfigSubjectConfigOutputReference",
    "PrivatecaCertificateConfigSubjectConfigSubject",
    "PrivatecaCertificateConfigSubjectConfigSubjectAltName",
    "PrivatecaCertificateConfigSubjectConfigSubjectAltNameOutputReference",
    "PrivatecaCertificateConfigSubjectConfigSubjectOutputReference",
    "PrivatecaCertificateConfigSubjectKeyId",
    "PrivatecaCertificateConfigSubjectKeyIdOutputReference",
    "PrivatecaCertificateConfigX509Config",
    "PrivatecaCertificateConfigX509ConfigAdditionalExtensions",
    "PrivatecaCertificateConfigX509ConfigAdditionalExtensionsList",
    "PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId",
    "PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectIdOutputReference",
    "PrivatecaCertificateConfigX509ConfigAdditionalExtensionsOutputReference",
    "PrivatecaCertificateConfigX509ConfigCaOptions",
    "PrivatecaCertificateConfigX509ConfigCaOptionsOutputReference",
    "PrivatecaCertificateConfigX509ConfigKeyUsage",
    "PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage",
    "PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsageOutputReference",
    "PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage",
    "PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference",
    "PrivatecaCertificateConfigX509ConfigKeyUsageOutputReference",
    "PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages",
    "PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList",
    "PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference",
    "PrivatecaCertificateConfigX509ConfigNameConstraints",
    "PrivatecaCertificateConfigX509ConfigNameConstraintsOutputReference",
    "PrivatecaCertificateConfigX509ConfigOutputReference",
    "PrivatecaCertificateConfigX509ConfigPolicyIds",
    "PrivatecaCertificateConfigX509ConfigPolicyIdsList",
    "PrivatecaCertificateConfigX509ConfigPolicyIdsOutputReference",
    "PrivatecaCertificateRevocationDetails",
    "PrivatecaCertificateRevocationDetailsList",
    "PrivatecaCertificateRevocationDetailsOutputReference",
    "PrivatecaCertificateTimeouts",
    "PrivatecaCertificateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4e6513ea971e7ba56821e154da8b680e3c480a8c1f3d3cddcbddbce439f2d585(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    pool: builtins.str,
    certificate_authority: typing.Optional[builtins.str] = None,
    certificate_template: typing.Optional[builtins.str] = None,
    config: typing.Optional[typing.Union[PrivatecaCertificateConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lifetime: typing.Optional[builtins.str] = None,
    pem_csr: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[PrivatecaCertificateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f90ccb9d67dbd012cf5b4ddcf487a5be7ce38cf1583bb8a3a8b50b9095c30eb9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fc6daeb86b12bdd42916a28eb5730764b9e882b2a9c0a39945077d9a47cbee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e236580ce68e3511f183efb60cb72406dc5babf08164c5ad429e36f46f0f815(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31740c1f995ddc63f991207f16e771b857fda8b89b9c7b060952affe7fd38aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e66dd75b3ae78bce0a10a7f6c624450bd3483b08c68f3fbb4de5b3f58af018(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa1339c31614fa4467a06538cc08ce8494befce858c0fff1683c2cefb9759ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514d4176de01c0f9a9fab787391e3a14f42428c6d1e736310122d800ec758fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1ecf0edb5a9e332362da62c41befa7424d478fe1d62dc6aa9f379c880b13f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e53c36654e726768ac8f4fef86cbb1ac704fc7ebab0494bef561e6d1578b02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff9d9061e8b0e8b17bea4bd11885497546616899e9f9196931f8c47741d0e81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183a1572c9d9fb9ce36439328e8514ff53e4411c0d22529d71e772edfadfa048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33ce72de1ea6d5c226af8e2afac76ffa7a38ee99eab97eec29f2f8c02d052a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b384285e18c7c74825182ab2a6fd550351f94058c397cdb16025d27cb6c6c4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d0e5694a0e380bdf864ee12577542e93023e082b039970b75a8461ee76d595(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f209bacc27a361d1913bb72ecf3c5d3f65ab7c70ebfe3d6ca0d707325130fce(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4242eea56eb76a0eaceddc65c4aa144d52517374a869fd051accae1d496e4d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa4b14bece8bfde142a301c8467dfbcfd8dc13015bf898d7a9cf72ff3cb8f9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967f9fa263df211764e64bc273214eaa8e3733caf287017bc6af5b8b7d281653(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionAuthorityKeyId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee2f950cf0cd35b0bf6ade6583c55994841dac4ad30b8e104f8ddce12ab3d3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd09e5302d558df825bec4fa7e258cc38d6b33013ad216e9b67cefe430066ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c618a55c97387b9379e7c8653264af1862d57ee0db15c0bb5174a973ddb22bd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a25347b09fcbfef9bed95197cd1297eeab26fccb3e5a0dad62a884d9bb6af4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a6ebd4e1f9f2be1d08e3199aef5f4ddc249f19957f73d536f09d1c1b06eef7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e1cb2477054eb590e013271df42f90e340af1a750e5e64e03f86a2c8cb33c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f712459cb2baf3fbef357f66e91cf64eec5733c0d3754c5d8d336f209dab91(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionCertFingerprint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85131830e68754f5c3555f77346e8f2ab4246e1a1a559c210daa9ccc1af5e58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0deb1900a13d89bee1df637af0388e52473c53114ec3956d460cbd3801cc0989(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56a012f4bc377158f3a4e29e3d3310d3647ffd4894753d906710ffb2fe0ee17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8884df39f5ba0299179569157d0b15105327c0b400141bd9d1d6e41c6ee24ebd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9807310602ce40b0df19da43d2cfbfc20552443cea327b6dd6e551376a17c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c32ac2508e3fdacc12ef2c434074367281b0fb5ed4768dc8bcd02cb9420760e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a369cd5ea2430cc7f3c1997fbceb3bbe7eaf42ec7639370ddb43c22c20f71e4d(
    value: typing.Optional[PrivatecaCertificateCertificateDescription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405cf4d373b8e0ddd5ca37868f29013e091cf838b215bb1e84ffe85786d512c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997f469bc30aa31d889c8d8c9f81440e5ba67c1e8fb444dff8072738c15d9576(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cece82e0339cb1f423970a2151cf45c19c5fa03d2cb31950b349b4efbebde71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a398e28387c9731b5adf188960d7affb8c192ac956a508b74dffcd57e2e2fb85(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311a30bd371df14e197c204c601df8458757852540099b4b0172d12e0498402a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73c74bee3086e7fe06e91fd7da1d21287b17a73198fcd7a8fedf303edcd01dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9edcb33c32206129bbe063b116f47f5b795b624c6c96d88075d3f4b67ce440f(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionPublicKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80241badcb143841aeb856e7f1cfa72a7b6cde69f05582e4f6cf49bb7386abbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaf3da7a69537458f9c2ab5e87250fcc981be5769fb68054bbd3893e0b6b104(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b1a002801ab2ca043eb7f1ce96d456366bfac05af0db172ce932f1786e3d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df567132a48b276f027ba69215ca68e972cbe637c3edadb15bc71371248ef008(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b16cd5ee4bb62055af3a7037b832e47a7494ff56d6f4e459a37c14230fa00bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ce3d8384db581cf924ca418beaeb729002d7b11a5dc17d8843ec0e96b0b43e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913756b766680703ccc8f53deef2549c4586d6d988b409621e754453440d199b(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3d101fc48b584117da7cf3b129224ddc30f6a1e4ec57935ddb39387a2dc170(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edc23e3dd29f9e57f50fcbd8c7403c335db6862da67e7aac08156a475d6b806(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fc7b3f7750a34d379d0a01676cacef85388e4211d2a39f5ef6c580982382dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac94372ba1fad22b16dd2041f4c219ea69c3f69aa42b361764f88d84c3129b8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ed8a91a97a5be3f9cb1df794bd3cdb1d83bb88bcd5c4ecb978a78a135fd2d1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a0372b5641ef7157b83eee10e80e2e2ea108c1bde1a8fa6e35de5b588a4deb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5902fcb7b00b6eeaf0bb47d5c915cdd9045ac9ec91201e398cfc308042578916(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10420fc9d6d542e958888615aa4181172bfbcf56102617c3945ead77e9447a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296c998648ce51517e1d2f3a03d2123f5bb0b9e377c1f94aa0a2f557bc4d8786(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a08f55b5a17639a74295239bd14eb38254a10cb3a30687b0093900b7b5b9d11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da691fa28b109f65205e9cee71f9312a6beb9aa01fbfcabb94456e137dd201ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a16316c08a21b98dd9b0a22a88973a1ee9ace0b64acc9840c73a4e5f112b82(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSansObectId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1315273ac99476871c7ff74b373b5b6b36f40c3ab23772351ac6c4aad8624e97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6d474de734b998d119a6d69336215bbabc54a067a152d31ca230d344ed081f(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltNameCustomSans],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8492c3c3e6d71db021d16e58b1280afd26cde9c264923d80160e2288ab19e7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfe62a4ca17ad221707b93e36bcb2d53eb63c5f9a92dc713913f5e531a26b6e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07023a89b1577cff28163a5c44322a20bcd5eb56321938bb09fd7a0172daa41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89875adf1020f6db224703bc095de89590a903bd94dba381e86a9067ac9a2139(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacf5626506617371e1efb73bb3d0806fb4d74734a04ecb4a7da73d11761fd79(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83c5904855150a292b2800af539032dddf0c184f0d48f13e67c7a351da0acf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e332b287c51791df28ef3b1f808b3bfd4e51fcc89454ab4d55f4ecf31ecdcbdc(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubjectAltName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b031160cd10e48713964cc32a8ac7bf8c21980bd9164f393a2a80d05faa0205(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf3939260c5b791b4b78ff3619869939d530323fadbd7a5c4f02ed07c11b35a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21b4b01bb887231ea17727f17c7d2f0d027b7e468359476662cec35abccff6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9537ca3eac15f8679dd077cd24d91d34523433282e7f7bc6590bf41a08c44148(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e8214fa2a6b1da8d276b9ea64df6781c18ad456adac26b92ae19c4a84056e2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a83311aa11d5f72ae5e9fa610614fd3e5a87d04b9585cc632a339712a09d85b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f1a3625f30964adc09f36f262c86dbaa061d57abdc8a706f13b36071f17245(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectDescriptionSubject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32a4ffeb742ff8d924863c93392d85b5af7306280831005068274de41489041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6daa8a9a891ff0ecfb5076ac88870c9e4f626f4c18230d15b7d9384858787750(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42392e896e17f03b0d8f8991f1cbce6ff5af4048fab5f8f8d1c7c12126467c5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce932e347f7721b52c6b70ec18ad63d93595b1e5e7c22c7a8416393a0404d1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e1fe94521df1149d71dbebcaa82fd54dc1452d8e22cf2c71c15285048106aa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f8c2c41bb19534db873756aed18bb64a5b381e13fb2b79eccc7ce87d8baf0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff111290a545e50288a2e2ff4bb2bc0b6b7665ca14a0d16e8777f41c0755522(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionSubjectKeyId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1f50e24de7daa5f2ab327cb08fae80fc86945fe3868b03efd2a4b765caee56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf07f85048d072656d34c5ccdff0f26a0c5b39550d1f2d7a8e54c07bae2d0622(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8acbe6993c99a6ea54e635dfbc183e0d4766ec8f84b5a0c31a3d8aa2fe2e71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d91352fe027de289d0cf40abc99a2c0542ab358eada953b02cf68dd07b29cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2dbd6118a7c842164c0b3b959f3dbe478521c1e57d727c68e594593421c186(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60cadf3e51c004f9a3ba30b54898dac4f8c0564410242e69fba3691ae0ecc4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588d094bcea78edf285df7f5a87115ded49db923760e0cbd03fe301741cbf741(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42eb4c5a90ba9052924491e1f67c95e2e340969336e1b2eb8d2a9e0ea8076a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2b2bd45259d25baf2589b2c30812e39f0be5c6594206dbff84e3d263f3e0d3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf32807d505a2224a9afbab1bc469f8b4ba503b9d5fa3837921cb10240d6fd44(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68100cba2f8a5fc17d24688e9c7d5d1941dfe835ce1fb6f5dc82cd543e875ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff6e8caebdb4890b22fe8f893cd6da60fa60cedd09263f43b6c05be9375a9ae(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensionsObjectId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff30f13284b82221e9de649d475fe2cea874d4d14f452fd0a667cfc4125dffb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c814c69ac05d67298e69e1932b3de75f5e4c24dd3a7050e71c368de4238dfd6e(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionAdditionalExtensions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10d9554da98b476c5a8056ebce306ea05b427052b4130b4bd358bc327a07482(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9a74f91b2f2b7d35ab620d990c8b0c699079120ae7efd550115a555effa2d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc734613eab09b4e23a7e63bf8dcfe89b2415d4250b880447b223b0384e31232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708a01ed3e3c30d05793ebc7b36930211eb1dbce7bc5917790d5a77513c73060(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91eb7625769619cc979c3feb95599318897a970974dd0d525791a505096138a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347fe064cd581612eac19b606bcd5349db5d0fab407a9770ed9e462fc02c4df3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d23b61dfe5c23757d8a075f7b7c208ee7d5eaa3fc72e832ebf933682c66368b(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionCaOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36f63a01d7c4356fec3a1b353ff4c743ccaa81bc5f9dbe6b95584b870a064f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a5e546d7f3fef96448c12b10720e93dc14f9f4d34021aab0a4f12872c9eff4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63208d4a7d7e32afd9945d32dcfaaff859553aeb1ff68a3328438060b6bb89c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58f9831a7619a08f6fb03e3438afc9201250128e660f6fe129ee766de04c5db(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b6837846a41470f47475260023f4b66946e70f6f775af8ba5e0cf4de5f10dd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e0feec76b03568ab76584d766f4e096253c16c1f86149db5a764b2b72ee4bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7509d54d3ef68638bcec361b3ed91124bdbc353189cd6f6e24810d0c1be6fea8(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageBaseKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef95b4be0db5e80a0ea498218594edc83de886473b655e573558422b283e709(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ac318cc71a500ffe8234541ef94d100e9a0e139f694ff5eddc233f2537bdae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865922c9ae31d4294d5bc45a7f9ad5c6533ab482ce06d8ee751526eaa28681d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c5e2304f8e251fd6d108345086d4720a10b72153c9a8bd38f502cac52e692b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329eb9776fba55e5d2e65c31ee27842b30aed30909b856e8a6bb17687adf2ebb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef7966773259a8f9f5e3efd28bd5be8046a13471d0aa8f23f89fb2c403dffe9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52468f296aa91810eef73a27666f0ee7d416c786533deb8d0eb52c077056ac3(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageExtendedKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66282787a14d7375e575c081d0a64c2e50d4b93b228ac3d0e1ae4787d5dfc4e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9844c7b907b1f3353903fb71fb080273e856f584c1817503a76fdc865f12068(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e8ce9f624a01c24e861394c8d8c2de3c7ebe271836138a851a710cc3020d5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f3a1ee55f7de109922a70a5846dfa88ca9db7903cd6eb5e87df6410fbb87dc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578f664d2a7f62b8457c3e58c372594dd54ddf5f2b563d7c1030ff1dbb338f2c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67853b72575fe2bdba8a9ef9159c863f3d04d92ee9631346b1ada7f97c071ab3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a073e5c3728ece392c8a67a4db245b0e783d1b0857c93e68d046f3f74b02ee7(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20905163787241738aafb730bd16f1fc5deb866128be3b45ab12fa32c03441c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9a8f1f9564b90ddab9805025ba38fa16ed54669d88f9814abd0d2f70a92b1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3580a4b700df3cfb19051277e1659898b0645be1f929472bf96d059146ed9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5f4aab494d1181f8ba2211a675eccee8aa044961a5444428745d64ad54616c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad956384c7c736f1e2ca162bed1873013e00673599fb8d885a38e82b184fd7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621390cd363ca2dd5054068e80c79ac2acef621edea6f45a6d6f816a5c93f430(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ffe3be0fb8e925f0ade6abcf75db870eaeb96c4acf7280721034767b28b555(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionKeyUsageUnknownExtendedKeyUsages],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9619cac07c1dc283c031b80f307541088c86716b42f75de18ae3014c6340e86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a3d7e4c9aeff27ad4b388f7d406b4d6fcad2d25950bad045d2b1a5becdd7e1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d08a6300698f7a70576dbfc30748a3d26149a79c9b1d8d75bd6c2400e934409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0eaeac987f0a60be029d7dde606e1ff3ba111a8a02c66e647d79b950dec0cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34cb2c29e04b7fcc8a1679a9a6c0fcea71bc11a516aa167fa9a431f127342bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc68246556f26bae7090ad646c74e2153a8930073477a35b60b531679ee0e72f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3177e7ae616e33a96ea0eaffbd92f469beac17f24f8e3aa8e0d89e76193302c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ca7ab726dda9bfdbb890a2d530c5a2f768fd615dab66acb5f74fbc87d2a40d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b632363498d1a319223cfdefe12aed33406f5c83298a623322dfe5e76b9392(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1688fdd03af00870bfd8d876ef5b9b9930aa9c4142e217530695df90a311389c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09241f6ac299db2e93a7eec899e778e012305c4b4b7cbe2c77abbef86994ee82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351a643895706b644b5c9595f423ec265bc4d9ac9adb15cc8615dd5df05fa665(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionNameConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43579265900f8670f1c9fbf3022678eb1644504cc686ff21bf6fd70228ff4411(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a355289774eb455594b3d8cfe4beb2a7707099d1d8d6e31a9cce6954336167(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509Description],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8757bb09d517e222650535f6484778be277fceb67475ac8fdd7782d87466951(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0b3f43bd1f352856c56abe725a23391e78e09ad26989f6f4b82277f1bc87e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe86b065a1abd39bf027ea6f801b65677219a412ab76d806cad37455feffb766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3698c94830de597e2f289ad8fca448a7454825e079c61046e50125dda6301b00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005bfbbf9cfca1b1fbbd136fbb6dc8da6f8048b77a2f93a1a13685a90d1c2a85(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9708eb4aaf2d1472d03ff2da076f3b6c239330ded348e88fd23ea57c02e6f024(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44bf46fa42dcf31e49c7e8c891a1a23c59f4b190e9b7ff06d7004a09776f666(
    value: typing.Optional[PrivatecaCertificateCertificateDescriptionX509DescriptionPolicyIds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e9d6a07d20f0fbca56bcde458a9577c49ce47e709406d351f3a17c80239975(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    pool: builtins.str,
    certificate_authority: typing.Optional[builtins.str] = None,
    certificate_template: typing.Optional[builtins.str] = None,
    config: typing.Optional[typing.Union[PrivatecaCertificateConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lifetime: typing.Optional[builtins.str] = None,
    pem_csr: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[PrivatecaCertificateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953fde99b9a0a976d4a7201a446e1b04a5e464f2e566254fe094c6fe0b621cab(
    *,
    public_key: typing.Union[PrivatecaCertificateConfigPublicKey, typing.Dict[builtins.str, typing.Any]],
    subject_config: typing.Union[PrivatecaCertificateConfigSubjectConfig, typing.Dict[builtins.str, typing.Any]],
    x509_config: typing.Union[PrivatecaCertificateConfigX509Config, typing.Dict[builtins.str, typing.Any]],
    subject_key_id: typing.Optional[typing.Union[PrivatecaCertificateConfigSubjectKeyId, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd5804b9aa2258e0d4f3290b734747fd6164512f5debfbdaee45cc544b68580(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494e7b44d9cbdc0d58986feca972004caca9e0be6bf1c8fba866c51ddb352e6c(
    value: typing.Optional[PrivatecaCertificateConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4caf4b80a5bed45807cc09d2a6070c941d631ace51bc518597ae51e9db5bfd(
    *,
    format: builtins.str,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861d7d13e0a51f2f0d3b1af9e52167c5dd551d9142156201bfa3ba158bef9275(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d6591f5d1edff155d9949af9babb067b2f8231f7b724266f6f988c68f30e63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400ceb1de25ef5cd8a213cf783481f40216733cf57eeb3bbe1288153a38cbb96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77a39af7cc29207421028bead0272bbf27ac41e6a163d12ee7fca28d70403fe(
    value: typing.Optional[PrivatecaCertificateConfigPublicKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cfe4b2a4533722d1af76bf24f9e3e2dd27268b8b7567279afb8b32a688d5b3(
    *,
    subject: typing.Union[PrivatecaCertificateConfigSubjectConfigSubject, typing.Dict[builtins.str, typing.Any]],
    subject_alt_name: typing.Optional[typing.Union[PrivatecaCertificateConfigSubjectConfigSubjectAltName, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71244f3552ac2783b731a3a195fff7a31770f40be74f7468cbcd16dc6974c01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d277848deeeac3f4a3d4e94f96621e20fac1ae587d14d058e2d08893d9e436(
    value: typing.Optional[PrivatecaCertificateConfigSubjectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1146dc160df4fa704efae1608f6a1f0af69ff7441277d2ccc6035429e3c1bc2f(
    *,
    common_name: builtins.str,
    organization: builtins.str,
    country_code: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    street_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e238f5dc5e909170b7ac581060b5bc6775365790900be061e706fe63c3d8f069(
    *,
    dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c0d57cb7b84b43ffda753facec61d06a2e90c462cc1d4cd92f4784a0b47763(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b135ae74c5634e3c1c68a20c86ca2517d8c25fd228d5e28e0bda86648635536c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca9951913cf5b1441a0070b4d62461c0bba4841541edf345e4672d8bdcd651a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bec014041987995562450456ea9d918ca801932bd3343073757e4a2a8ae163a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c8856d253c5c48ba5bb39a9b6bb889433e20f7fc145f73d42c6cb119fb85fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a758f71b74bd93e0ccd79ac93a4d2722173d85df9209edeb572f844ff45fdfd9(
    value: typing.Optional[PrivatecaCertificateConfigSubjectConfigSubjectAltName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974eb752a70ba66f2c36636e0aac31c3ad61ae118a96775d2e852dddfeeb7a0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c2e46144737497f0312811ad0e9532501e790577b647596c48de4908a2759a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa04f51c2f1c1411461baee4aa3f6fe78f4cf701a855e7a08405266c690d90f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf76a3d919829fd470c5229b2da6a68d4bf6ea9cbceff6f5c8689dfdbe74094(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02107fb315cb252c87192a502b7f380a144814a996a8fe5d47297eaa5eb0d72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62baa92df9c700c83cecd0c1ad0d2aa7e6086fc6886eef4ef9f2d190965ea7e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18c11b389c722526a984e117e65c707775ebf0f8b0ae14d25e14d6733074569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686c75e2bc3b191d071bd84a4bd37b36f86f656b5957361a3486ca0ca9b1f9a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0664135227d7fde55e5204d749ae313e15c4d98f3bf6ce7992f3b8e0a7ab53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912142e5f04bae4881bb6c624ac6b9d65091d869f22205465a38932e13443307(
    value: typing.Optional[PrivatecaCertificateConfigSubjectConfigSubject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d1dca07e1da962949ca73b6135bdfd66b7891c1ea58fcf60bebc6f620aff96(
    *,
    key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bd110b96a67dde735b359ba6c403fe79388272241b321d7bc216120e90433d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8bbf5d0a53b1a530a5a3ea91cde75b9f58563c4ea17f9cf61157c565050c83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a7432d2394b91fe5aa6ba0d00b9a2345258e03e1332653e795147f9637d57c(
    value: typing.Optional[PrivatecaCertificateConfigSubjectKeyId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdd1af9b9cc6781f859611551af670e10d55926bf2345d50aa50e31b52d95f9(
    *,
    key_usage: typing.Union[PrivatecaCertificateConfigX509ConfigKeyUsage, typing.Dict[builtins.str, typing.Any]],
    additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateConfigX509ConfigAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ca_options: typing.Optional[typing.Union[PrivatecaCertificateConfigX509ConfigCaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    name_constraints: typing.Optional[typing.Union[PrivatecaCertificateConfigX509ConfigNameConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateConfigX509ConfigPolicyIds, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00edc685aa572900ec9ecc2c0249e868c8cedbd6f05b89b3e13b12b79b90e5fe(
    *,
    critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    object_id: typing.Union[PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId, typing.Dict[builtins.str, typing.Any]],
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1d42e1e02095119fb4245f42b2bfc8627901462d9d09cce98ea9dfa72aac8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a6fb704624d308cdb7139d9c2c07656018718b4df3e3b02044833246d745c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fb1e4c3506cfbcbe333bf2e9b7990d5915f02be6e8ac9b033d14b642ef045d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ad8be0a73298a6214ca2e505ed96c3d37a3394b0e497e38751a775511ea2f3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0c0e35847ac07d18de5b1b5c64f8b0f2337263f047748218e2b39b8f1a63a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf248c7fc9252307c28b77107fda32e737aec32f303190a3947675f6973c9ec5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigAdditionalExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ce2af4863dc02f855cd089b81d95ba42b65ce2edec94e4c013fceaad3a9f12(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9377a1969b32d1c8d5f464f81a28c077c632c610ecc973e7392deb8d6082a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e020c527c64d54022d809103d0a543c357eefa57d6459cd07faf4b8eb40be4(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a63c085b0028b64c6e3d77f886643019df70a429fbe6ad8e08394e61cf7922(
    value: typing.Optional[PrivatecaCertificateConfigX509ConfigAdditionalExtensionsObjectId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3d0b94f4d84379eee9828750307852914e4fe899e3e3907bf1c6daea9dc852(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1bc8f0b7adde3c9e9fa234173eb0c4aaec29074b1d9786967497b2d94d8874(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9281944d1fbe2d6db12ec4d4a5cf873c5f606aa62ebd0eb4fc904d150009e4bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62af555f24d4b07715f9f960fc06e5effdb6311cb676228bbd506dba5c9b60bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigAdditionalExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41866f32f1948c30dc6918086533494f4410212df678c55a547a2a4bd564a216(
    *,
    is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_issuer_path_length: typing.Optional[jsii.Number] = None,
    non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135ee246545026938289493de42593a78f6bda304a3da1b81159732c0b03b2e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3ad9b889c47f3e816c8c11780793208576231ee5a5adfef71979959848345d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8e251b5e53e0a93cacf077bb733d88bc239dfa9d4452719a11daa8521d4f8b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1995ff5d9bcb07b401e9f300e86d399ecf0e03243cd7127aefbcd418ccae89c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5311dbfec19ba52fc9bf9b39748d18da122c2b4f6029af5c8181a137dbaf4a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71263875d268a47f93716a2d01b945d1a24474e2131da7a9bd5201c8a98f2ada(
    value: typing.Optional[PrivatecaCertificateConfigX509ConfigCaOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32df3578eac79cebfcbdda93ce0104a936a5c6da13cbc932b9c93e42b6d4bc8(
    *,
    base_key_usage: typing.Union[PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]],
    extended_key_usage: typing.Union[PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]],
    unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46802d488ce422c9d186e5cd05a8a4b56a8a5aa4753140b11ff1def61688c10d(
    *,
    cert_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    content_commitment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crl_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    data_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    decipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    digital_signature: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_agreement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631f23e196be8f541e2b1e1743c7892b14434fb91dd7e9709e0327ab944e76aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd7e354b0659de08d43ee62b0f115e043ad1503a31c37fcb4a713306b457fda(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84164b51db87552ee72e72c68696674da7d153ee143d726d9163b9e5c94cfa7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5c526696df082c2a121681900b1a7e0f32a81e3e19870a018974510539e113(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffcf589a72cd7e7ad06eacb6989456b88a56274502e52e98fe65ca8bfcecee6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffc8f1a42a0e90dcc2b2fe84b526c0654569116cac2d3ad09cff2fd460cb7b9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b5a03fb882ac60ea2005eca4f59b0cf59daedb84fcccc1c8ad8b3de1ec423e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67b2f98674141ed7078d1f0f476e263e9157b91576007107ce404b04a129d76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4d6b4230785243e788697c62b028ee76e7b2510d63fd4dddb49a400be2f17a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf631343ca4a813160c277a865dff37fa236ff7833c3ca8184f534ed8bb0147(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07df6d07572dc8b493d9b954046a875c0f8e02d70e21798108f4f1076c7dd0a(
    value: typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageBaseKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ae6f808cf2572bcf3bdb84a11a2dafcba0a76844bc3ab312a7c375565a27b5(
    *,
    client_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    code_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    email_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ocsp_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    server_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    time_stamping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ab4655095e3d8736579d1f9d2131a53ce73184823014899710618b01a8e15f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79727a60056c0fdb14fe73da18f54d29afdf3c9b96cacd24c42b1c0c1e713aa3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b288de985187488184d8c9db71397532162f9adf5146006d70a3a513f216aa2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722772725ae6753e3b38d28e4902856d82e3cc4abe8e5a9f47487924c63eee80(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562f9422916cd0af75d798426487a49d22c69e224eb1a727aab754b6ace2af43(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eeefbb4175f8e1f7e03ce9df8a4aeed010d294e5f1cde01dbd867fc14b29e75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9121de694afa1ceaf3fe4ebe83e4b02d24e95a9e542093ec24e9aad2cdeedf04(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae09f9433cd5eec6901c37dd6a1e8fd36643b326cdde27f977863e6351b7fe3(
    value: typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsageExtendedKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e682020ec0d765b963fc16f2313001c125557753c5903379bd6d053fd7a4ca0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afec427c694c7649c6efd2d63e5270ede0cecd247e057122967614d41d68118(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a528ce33de37353f7f80eb3879b5826ba8b39fbf0bd0f65c1387330811e93a(
    value: typing.Optional[PrivatecaCertificateConfigX509ConfigKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56d9a388d7964d34008b3a99fd51f56897534a07261f37431b4cd43ba002de2(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdd202136669ef50ee38a2220a33103727f2d2cbf445cc6bc21b4f83ab8a4d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d1adf946af559b8243f8f67cdb3b4e529c7753acb2cb0e82e2a98c59d82108(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4395cb32a3483789a735cc9b9c6a6fc3db6bec8c44b60d5748a2aef650a7c4f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82846c2dc4f0007cd77750dea0e24a52eb0a7986aec1d2c5d2a82fbc11b8fd5e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a7c085a0caae397f36ce0ea92dac910ed2dcf85470c028af53a02e39c7329f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0782c82fb9647dcbf3c184bbda2d0b6141c3528148ad53a3fafb48cacfdc4e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c4685c2b5dee96d067aaeecef968e886513bd7ba879e910b4b1f5ea10c6225(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40a9bd5c86304c607203a20c25c0d4b7e97c53c2c2a7cf97f929e12eb2b5196(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c75eec05739719eeecfc2a9ff928d1e18c68eeb3f14c98ff56dc1d02df54660(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a699b1366899f8a4e198ceea47619367826c66cb9ce29d1e38858661587fd96(
    *,
    critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    excluded_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e665309a521d025c0d26a6f6e6233f332ab2293e3738dede33a64bfe40f0d59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5c1d8061cdafa67ce59f03295a8071355eb678df9079bf0fe8cf862e2d4279(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a56e1661afdfa6264c412358fe74f87a1ae3f8ec197c6fbb5efb479e03e1f1a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1560dd20ca3d46c3b48ea664544605628ac8e4d4541db9c9d0236d9f5af4dd1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653d875147013a12e10d3dcf0396bba6d978fb2cfeb0fce17e80870668697eb0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40a40197dca2ce72fd6c366098af40ab3313127161b3b80d0017ecb425a4624(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d61666d7d09a58a295e4bfbad8c644b5f715bbe87d61f779f1327570d48b49(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2ed9ffdb7b46cfa0ea0e105c1267fc002d96d8f2f06bb5952db316428c3120(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742ed012c374d90d4895c67264361a5ffa2f48982afd00fec95079e3ff1e991e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ba5fccfc0d64ec531617cda602ca3131e83c17e8b82d3483bd999950df3a29(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a8b57b9beb218b25cb0b93cf621fe3489770374954d23c05de61bbeca5b0cf(
    value: typing.Optional[PrivatecaCertificateConfigX509ConfigNameConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d3d34badad54f73ed784964e76a5a677feaa9c09c2246ac74e8ccaaa70749d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9b08ac8a734c15e89cc3bb367c51046a42f3dbfd7381ad86dd53c618780b58(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateConfigX509ConfigAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d536f55db18101d9180883a55a90d0cfbe42869aff1030961d6ec52dc31fee(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateConfigX509ConfigPolicyIds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7fe8793ef853ac3ccbaad34f01ae7ef4c769a144778b6be211504a4e90111f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8b4fbf4367c793c741da3c35a4c01a02658f123f2e584dc3838a990acfaf2d(
    value: typing.Optional[PrivatecaCertificateConfigX509Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e2609527fa27d81792c16eaa200d4cbad45a097313bdc37101c6ef83c9808a(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fc76ecc403163d39b6257569b60e982ec6af9a565b1158aae18dd687190068(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e322d2754a67fcaf215e632c6a9cd3b97e2b4d87b01e6d098d13129d63720edd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479cbce77195deac6746d512ed73fde92654187d14539b470f06d09085a5808e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81cf0f905cbafff2694469e75c87f8b032c3ab521c1bdd9f1f3b25f5612e3196(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c10238b1338123ba106b6f98bc099d92a8d0de1f97c39ca8b9e847d2e7f00c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d60385208493d3c4b12db07facc27833f123b6113a87f4eff775072ac6f0965(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateConfigX509ConfigPolicyIds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88752150dcada2d73f00b2a0a20d30f18905025b03c7a19dd6798baf3e7b2e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfa72f634af028fbb0a38bb510960f4af65b77cc10a3148386f96d807de453c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c921d23052f20991a65b815f4e83f34b3458cde162dc9f50d5cadf09c62cd5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateConfigX509ConfigPolicyIds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1aa236e1c0a003401df7b039649e4dff8efe40f160b08896f5effe26c02ee0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308a8bf44a67e19a61af3aea28471b3e2064d9a6af919046f0be56de64b15c60(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b250ff69808acf272b31c6424ecb1bdfe70c66dc674176d08b4ae0bb58d9a5fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c159c828ac5cd7dbbfc74f58ccb680b9de03622cfd6572fc1d4eba6ca9788656(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8aa4f97bfcceea7ce3d8142ae94b7c41fbf31615ca6bffec2a151d9ea1cf29c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4b0303d3b430e6a99ecd3af652e41fbb74521ebb8f13ce5d16e3012f0c4493(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d44dd4d6c003308ccd11a828dba6ea60248fee22effa4f5936f6ebad18a4f2(
    value: typing.Optional[PrivatecaCertificateRevocationDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7ef8b440b93769a669866adf09785bb03b8ebd56862f3ebf234bab74912c5f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42db0f588cbdd2eaec56dfd253344076acc96ff17184a2217ffb19e9d1172bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbff2b5c582104ed381e8446a420c70359a24bd59a7db9b9212949dbde3141e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88dde5f2c0ec29a5b2d925b2f41bd77e7c68ddf434f6427e832aabd340964a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d76ca036851326a725390d61dfe1ac272ed91706af9c1878732ee80b9e4da5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9385a7139af82555c77a0883a2b37d4af5086553efc20dc893fb7a353fc7940d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
