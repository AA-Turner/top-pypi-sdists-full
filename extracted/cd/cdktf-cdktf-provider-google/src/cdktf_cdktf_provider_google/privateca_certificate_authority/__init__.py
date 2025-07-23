r'''
# `google_privateca_certificate_authority`

Refer to the Terraform Registry for docs: [`google_privateca_certificate_authority`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority).
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


class PrivatecaCertificateAuthority(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthority",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority google_privateca_certificate_authority}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        certificate_authority_id: builtins.str,
        config: typing.Union["PrivatecaCertificateAuthorityConfigA", typing.Dict[builtins.str, typing.Any]],
        key_spec: typing.Union["PrivatecaCertificateAuthorityKeySpec", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        pool: builtins.str,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        desired_state: typing.Optional[builtins.str] = None,
        gcs_bucket: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_active_certificates_on_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lifetime: typing.Optional[builtins.str] = None,
        pem_ca_certificate: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        skip_grace_period: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subordinate_config: typing.Optional[typing.Union["PrivatecaCertificateAuthoritySubordinateConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PrivatecaCertificateAuthorityTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        user_defined_access_urls: typing.Optional[typing.Union["PrivatecaCertificateAuthorityUserDefinedAccessUrls", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority google_privateca_certificate_authority} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param certificate_authority_id: The user provided Resource ID for this Certificate Authority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#certificate_authority_id PrivatecaCertificateAuthority#certificate_authority_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#config PrivatecaCertificateAuthority#config}
        :param key_spec: key_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_spec PrivatecaCertificateAuthority#key_spec}
        :param location: Location of the CertificateAuthority. A full list of valid locations can be found by running 'gcloud privateca locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#location PrivatecaCertificateAuthority#location}
        :param pool: The name of the CaPool this Certificate Authority belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pool PrivatecaCertificateAuthority#pool}
        :param deletion_protection: Whether Terraform will be prevented from destroying the CertificateAuthority. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the CertificateAuthority will fail. When the field is set to false, deleting the CertificateAuthority is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#deletion_protection PrivatecaCertificateAuthority#deletion_protection}
        :param desired_state: Desired state of the CertificateAuthority. Set this field to 'STAGED' to create a 'STAGED' root CA. Possible values: ENABLED, DISABLED, STAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#desired_state PrivatecaCertificateAuthority#desired_state}
        :param gcs_bucket: The name of a Cloud Storage bucket where this CertificateAuthority will publish content, such as the CA certificate and CRLs. This must be a bucket name, without any prefixes (such as 'gs://') or suffixes (such as '.googleapis.com'). For example, to use a bucket named my-bucket, you would simply specify 'my-bucket'. If not specified, a managed bucket will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#gcs_bucket PrivatecaCertificateAuthority#gcs_bucket}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#id PrivatecaCertificateAuthority#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_active_certificates_on_deletion: This field allows the CA to be deleted even if the CA has active certs. Active certs include both unrevoked and unexpired certs. Use with care. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ignore_active_certificates_on_deletion PrivatecaCertificateAuthority#ignore_active_certificates_on_deletion}
        :param labels: Labels with user-defined metadata. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#labels PrivatecaCertificateAuthority#labels}
        :param lifetime: The desired lifetime of the CA certificate. Used to create the "notBeforeTime" and "notAfterTime" fields inside an X.509 certificate. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#lifetime PrivatecaCertificateAuthority#lifetime}
        :param pem_ca_certificate: The signed CA certificate issued from the subordinated CA's CSR. This is needed when activating the subordiante CA with a third party issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pem_ca_certificate PrivatecaCertificateAuthority#pem_ca_certificate}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#project PrivatecaCertificateAuthority#project}.
        :param skip_grace_period: If this flag is set, the Certificate Authority will be deleted as soon as possible without a 30-day grace period where undeletion would have been allowed. If you proceed, there will be no way to recover this CA. Use with care. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#skip_grace_period PrivatecaCertificateAuthority#skip_grace_period}
        :param subordinate_config: subordinate_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subordinate_config PrivatecaCertificateAuthority#subordinate_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#timeouts PrivatecaCertificateAuthority#timeouts}
        :param type: The Type of this CertificateAuthority. ~> **Note:** For 'SUBORDINATE' Certificate Authorities, they need to be activated before they can issue certificates. Default value: "SELF_SIGNED" Possible values: ["SELF_SIGNED", "SUBORDINATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#type PrivatecaCertificateAuthority#type}
        :param user_defined_access_urls: user_defined_access_urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#user_defined_access_urls PrivatecaCertificateAuthority#user_defined_access_urls}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e2ded4e1de4193797f923bbb76a625d831255ac97f311bbd90e6b36f1b1652)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = PrivatecaCertificateAuthorityConfig(
            certificate_authority_id=certificate_authority_id,
            config=config,
            key_spec=key_spec,
            location=location,
            pool=pool,
            deletion_protection=deletion_protection,
            desired_state=desired_state,
            gcs_bucket=gcs_bucket,
            id=id,
            ignore_active_certificates_on_deletion=ignore_active_certificates_on_deletion,
            labels=labels,
            lifetime=lifetime,
            pem_ca_certificate=pem_ca_certificate,
            project=project,
            skip_grace_period=skip_grace_period,
            subordinate_config=subordinate_config,
            timeouts=timeouts,
            type=type,
            user_defined_access_urls=user_defined_access_urls,
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
        '''Generates CDKTF code for importing a PrivatecaCertificateAuthority resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PrivatecaCertificateAuthority to import.
        :param import_from_id: The id of the existing PrivatecaCertificateAuthority that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PrivatecaCertificateAuthority to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fcabfe3b4c6ee50c071e220058aed6b8962ed774fb5d0459843e6b3859573a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        subject_config: typing.Union["PrivatecaCertificateAuthorityConfigSubjectConfig", typing.Dict[builtins.str, typing.Any]],
        x509_config: typing.Union["PrivatecaCertificateAuthorityConfigX509Config", typing.Dict[builtins.str, typing.Any]],
        subject_key_id: typing.Optional[typing.Union["PrivatecaCertificateAuthorityConfigSubjectKeyId", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param subject_config: subject_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject_config PrivatecaCertificateAuthority#subject_config}
        :param x509_config: x509_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#x509_config PrivatecaCertificateAuthority#x509_config}
        :param subject_key_id: subject_key_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject_key_id PrivatecaCertificateAuthority#subject_key_id}
        '''
        value = PrivatecaCertificateAuthorityConfigA(
            subject_config=subject_config,
            x509_config=x509_config,
            subject_key_id=subject_key_id,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putKeySpec")
    def put_key_spec(
        self,
        *,
        algorithm: typing.Optional[builtins.str] = None,
        cloud_kms_key_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: The algorithm to use for creating a managed Cloud KMS key for a for a simplified experience. All managed keys will be have their ProtectionLevel as HSM. Possible values: ["SIGN_HASH_ALGORITHM_UNSPECIFIED", "RSA_PSS_2048_SHA256", "RSA_PSS_3072_SHA256", "RSA_PSS_4096_SHA256", "RSA_PKCS1_2048_SHA256", "RSA_PKCS1_3072_SHA256", "RSA_PKCS1_4096_SHA256", "EC_P256_SHA256", "EC_P384_SHA384"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#algorithm PrivatecaCertificateAuthority#algorithm}
        :param cloud_kms_key_version: The resource name for an existing Cloud KMS CryptoKeyVersion in the format 'projects/* /locations/* /keyRings/* /cryptoKeys/* /cryptoKeyVersions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#cloud_kms_key_version PrivatecaCertificateAuthority#cloud_kms_key_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = PrivatecaCertificateAuthorityKeySpec(
            algorithm=algorithm, cloud_kms_key_version=cloud_kms_key_version
        )

        return typing.cast(None, jsii.invoke(self, "putKeySpec", [value]))

    @jsii.member(jsii_name="putSubordinateConfig")
    def put_subordinate_config(
        self,
        *,
        certificate_authority: typing.Optional[builtins.str] = None,
        pem_issuer_chain: typing.Optional[typing.Union["PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_authority: This can refer to a CertificateAuthority that was used to create a subordinate CertificateAuthority. This field is used for information and usability purposes only. The resource name is in the format 'projects/* /locations/* /caPools/* /certificateAuthorities/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#certificate_authority PrivatecaCertificateAuthority#certificate_authority} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param pem_issuer_chain: pem_issuer_chain block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pem_issuer_chain PrivatecaCertificateAuthority#pem_issuer_chain}
        '''
        value = PrivatecaCertificateAuthoritySubordinateConfig(
            certificate_authority=certificate_authority,
            pem_issuer_chain=pem_issuer_chain,
        )

        return typing.cast(None, jsii.invoke(self, "putSubordinateConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#create PrivatecaCertificateAuthority#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#delete PrivatecaCertificateAuthority#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#update PrivatecaCertificateAuthority#update}.
        '''
        value = PrivatecaCertificateAuthorityTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUserDefinedAccessUrls")
    def put_user_defined_access_urls(
        self,
        *,
        aia_issuing_certificate_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        crl_access_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aia_issuing_certificate_urls: A list of URLs where this CertificateAuthority's CA certificate is published that is specified by users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#aia_issuing_certificate_urls PrivatecaCertificateAuthority#aia_issuing_certificate_urls}
        :param crl_access_urls: A list of URLs where this CertificateAuthority's CRLs are published that is specified by users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#crl_access_urls PrivatecaCertificateAuthority#crl_access_urls}
        '''
        value = PrivatecaCertificateAuthorityUserDefinedAccessUrls(
            aia_issuing_certificate_urls=aia_issuing_certificate_urls,
            crl_access_urls=crl_access_urls,
        )

        return typing.cast(None, jsii.invoke(self, "putUserDefinedAccessUrls", [value]))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDesiredState")
    def reset_desired_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredState", []))

    @jsii.member(jsii_name="resetGcsBucket")
    def reset_gcs_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsBucket", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreActiveCertificatesOnDeletion")
    def reset_ignore_active_certificates_on_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreActiveCertificatesOnDeletion", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLifetime")
    def reset_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifetime", []))

    @jsii.member(jsii_name="resetPemCaCertificate")
    def reset_pem_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemCaCertificate", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSkipGracePeriod")
    def reset_skip_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipGracePeriod", []))

    @jsii.member(jsii_name="resetSubordinateConfig")
    def reset_subordinate_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubordinateConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserDefinedAccessUrls")
    def reset_user_defined_access_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefinedAccessUrls", []))

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
    @jsii.member(jsii_name="accessUrls")
    def access_urls(self) -> "PrivatecaCertificateAuthorityAccessUrlsList":
        return typing.cast("PrivatecaCertificateAuthorityAccessUrlsList", jsii.get(self, "accessUrls"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "PrivatecaCertificateAuthorityConfigAOutputReference":
        return typing.cast("PrivatecaCertificateAuthorityConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="keySpec")
    def key_spec(self) -> "PrivatecaCertificateAuthorityKeySpecOutputReference":
        return typing.cast("PrivatecaCertificateAuthorityKeySpecOutputReference", jsii.get(self, "keySpec"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="pemCaCertificates")
    def pem_ca_certificates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pemCaCertificates"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="subordinateConfig")
    def subordinate_config(
        self,
    ) -> "PrivatecaCertificateAuthoritySubordinateConfigOutputReference":
        return typing.cast("PrivatecaCertificateAuthoritySubordinateConfigOutputReference", jsii.get(self, "subordinateConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PrivatecaCertificateAuthorityTimeoutsOutputReference":
        return typing.cast("PrivatecaCertificateAuthorityTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedAccessUrls")
    def user_defined_access_urls(
        self,
    ) -> "PrivatecaCertificateAuthorityUserDefinedAccessUrlsOutputReference":
        return typing.cast("PrivatecaCertificateAuthorityUserDefinedAccessUrlsOutputReference", jsii.get(self, "userDefinedAccessUrls"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityIdInput")
    def certificate_authority_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateAuthorityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["PrivatecaCertificateAuthorityConfigA"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsBucketInput")
    def gcs_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcsBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreActiveCertificatesOnDeletionInput")
    def ignore_active_certificates_on_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreActiveCertificatesOnDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="keySpecInput")
    def key_spec_input(self) -> typing.Optional["PrivatecaCertificateAuthorityKeySpec"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityKeySpec"], jsii.get(self, "keySpecInput"))

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
    @jsii.member(jsii_name="pemCaCertificateInput")
    def pem_ca_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemCaCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="poolInput")
    def pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="skipGracePeriodInput")
    def skip_grace_period_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipGracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="subordinateConfigInput")
    def subordinate_config_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthoritySubordinateConfig"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthoritySubordinateConfig"], jsii.get(self, "subordinateConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivatecaCertificateAuthorityTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivatecaCertificateAuthorityTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedAccessUrlsInput")
    def user_defined_access_urls_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityUserDefinedAccessUrls"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityUserDefinedAccessUrls"], jsii.get(self, "userDefinedAccessUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityId")
    def certificate_authority_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthorityId"))

    @certificate_authority_id.setter
    def certificate_authority_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e419641c078d6a0902bc1349cd6cc523a4d99ec1ad580e9a74606579905faace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthorityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345c013081cbecfa85dd709d2cda248bfd644f028267aebdca8701aeaa91c9f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b82fd5b1582d7b1c697a45b6a598b62ba3e1933d5e0fdd37b68ab5e0886be77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcsBucket")
    def gcs_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcsBucket"))

    @gcs_bucket.setter
    def gcs_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da65a8fff5a70ed74ca8fb03563fe2776c6144a61b5188a10bde64b26a81b350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcsBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d64b879a00b9f9dd0db50cb02c270c3ae6a2ac54f20f7fca280932b4e68fa41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreActiveCertificatesOnDeletion")
    def ignore_active_certificates_on_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreActiveCertificatesOnDeletion"))

    @ignore_active_certificates_on_deletion.setter
    def ignore_active_certificates_on_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428a5f7a4e6c5ce074457c03e1993613b28551047f50245a0bc2ac83ce39396c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreActiveCertificatesOnDeletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfacf4d0993ccaeb6cc4310d4a26111f3437ab28a6dff26ab9549bb15b83587d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lifetime")
    def lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifetime"))

    @lifetime.setter
    def lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0e3b96f14d385e811d5eb1f5268f1de754721a2d1c02756ef6002056d626a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f3da325ed35b0c6db612b4405df5728dea1217bd66560e2fda69fa24dca013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pemCaCertificate")
    def pem_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemCaCertificate"))

    @pem_ca_certificate.setter
    def pem_ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca221ccd602f865ec2e7e02ddb00a20ebce9c41a6544bea6974524201b73c97a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pool")
    def pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pool"))

    @pool.setter
    def pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62e2dd5686434423089cc716bd53142bef5447fd8cda1fd1bf70522c11ff09c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66056f75680062f6bc9699ac5f58a4eae50914b8397e45f8e2c850551935cee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipGracePeriod")
    def skip_grace_period(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipGracePeriod"))

    @skip_grace_period.setter
    def skip_grace_period(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8b834be254b56ac9e279c7566101e82d6d3a8c5f7f238c40753a4f611fc78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipGracePeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487286d8483bd759dbff722a6435c33c8216fcdf45fd173c054ed11717ac6cfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityAccessUrls",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivatecaCertificateAuthorityAccessUrls:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityAccessUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityAccessUrlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityAccessUrlsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05447caf1c12171b9dfac5d3eb7f8930b745263991f73a0e56c994681e591ade)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateAuthorityAccessUrlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f61d0fa2db1ad543af28841bb2633a67d96366daf2228f9ea092d543ff0b0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateAuthorityAccessUrlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92996ae67b2669ca8d16409d678c38a88b7e719b9ea8881a85d014e49d386152)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72d07ce5df2f91f057460be3d031dd2e30923797ea2628aeef21653464cfb8bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e625e1fc2991089122653cc91bb4bbbf8ef7a8f4cd4fd277dd08f17c0f2cf32c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateAuthorityAccessUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityAccessUrlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f623f2e7408399434131478fb2d5a9146bf0e4ef136e2fd8965ed2d48f4c6b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="caCertificateAccessUrl")
    def ca_certificate_access_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertificateAccessUrl"))

    @builtins.property
    @jsii.member(jsii_name="crlAccessUrls")
    def crl_access_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "crlAccessUrls"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityAccessUrls]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityAccessUrls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityAccessUrls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c0529b59727639535f7241c5510e17d12f36e60a89f228358de693908e1046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "certificate_authority_id": "certificateAuthorityId",
        "config": "config",
        "key_spec": "keySpec",
        "location": "location",
        "pool": "pool",
        "deletion_protection": "deletionProtection",
        "desired_state": "desiredState",
        "gcs_bucket": "gcsBucket",
        "id": "id",
        "ignore_active_certificates_on_deletion": "ignoreActiveCertificatesOnDeletion",
        "labels": "labels",
        "lifetime": "lifetime",
        "pem_ca_certificate": "pemCaCertificate",
        "project": "project",
        "skip_grace_period": "skipGracePeriod",
        "subordinate_config": "subordinateConfig",
        "timeouts": "timeouts",
        "type": "type",
        "user_defined_access_urls": "userDefinedAccessUrls",
    },
)
class PrivatecaCertificateAuthorityConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        certificate_authority_id: builtins.str,
        config: typing.Union["PrivatecaCertificateAuthorityConfigA", typing.Dict[builtins.str, typing.Any]],
        key_spec: typing.Union["PrivatecaCertificateAuthorityKeySpec", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        pool: builtins.str,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        desired_state: typing.Optional[builtins.str] = None,
        gcs_bucket: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_active_certificates_on_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lifetime: typing.Optional[builtins.str] = None,
        pem_ca_certificate: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        skip_grace_period: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subordinate_config: typing.Optional[typing.Union["PrivatecaCertificateAuthoritySubordinateConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PrivatecaCertificateAuthorityTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        user_defined_access_urls: typing.Optional[typing.Union["PrivatecaCertificateAuthorityUserDefinedAccessUrls", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param certificate_authority_id: The user provided Resource ID for this Certificate Authority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#certificate_authority_id PrivatecaCertificateAuthority#certificate_authority_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#config PrivatecaCertificateAuthority#config}
        :param key_spec: key_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_spec PrivatecaCertificateAuthority#key_spec}
        :param location: Location of the CertificateAuthority. A full list of valid locations can be found by running 'gcloud privateca locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#location PrivatecaCertificateAuthority#location}
        :param pool: The name of the CaPool this Certificate Authority belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pool PrivatecaCertificateAuthority#pool}
        :param deletion_protection: Whether Terraform will be prevented from destroying the CertificateAuthority. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the CertificateAuthority will fail. When the field is set to false, deleting the CertificateAuthority is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#deletion_protection PrivatecaCertificateAuthority#deletion_protection}
        :param desired_state: Desired state of the CertificateAuthority. Set this field to 'STAGED' to create a 'STAGED' root CA. Possible values: ENABLED, DISABLED, STAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#desired_state PrivatecaCertificateAuthority#desired_state}
        :param gcs_bucket: The name of a Cloud Storage bucket where this CertificateAuthority will publish content, such as the CA certificate and CRLs. This must be a bucket name, without any prefixes (such as 'gs://') or suffixes (such as '.googleapis.com'). For example, to use a bucket named my-bucket, you would simply specify 'my-bucket'. If not specified, a managed bucket will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#gcs_bucket PrivatecaCertificateAuthority#gcs_bucket}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#id PrivatecaCertificateAuthority#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_active_certificates_on_deletion: This field allows the CA to be deleted even if the CA has active certs. Active certs include both unrevoked and unexpired certs. Use with care. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ignore_active_certificates_on_deletion PrivatecaCertificateAuthority#ignore_active_certificates_on_deletion}
        :param labels: Labels with user-defined metadata. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#labels PrivatecaCertificateAuthority#labels}
        :param lifetime: The desired lifetime of the CA certificate. Used to create the "notBeforeTime" and "notAfterTime" fields inside an X.509 certificate. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#lifetime PrivatecaCertificateAuthority#lifetime}
        :param pem_ca_certificate: The signed CA certificate issued from the subordinated CA's CSR. This is needed when activating the subordiante CA with a third party issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pem_ca_certificate PrivatecaCertificateAuthority#pem_ca_certificate}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#project PrivatecaCertificateAuthority#project}.
        :param skip_grace_period: If this flag is set, the Certificate Authority will be deleted as soon as possible without a 30-day grace period where undeletion would have been allowed. If you proceed, there will be no way to recover this CA. Use with care. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#skip_grace_period PrivatecaCertificateAuthority#skip_grace_period}
        :param subordinate_config: subordinate_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subordinate_config PrivatecaCertificateAuthority#subordinate_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#timeouts PrivatecaCertificateAuthority#timeouts}
        :param type: The Type of this CertificateAuthority. ~> **Note:** For 'SUBORDINATE' Certificate Authorities, they need to be activated before they can issue certificates. Default value: "SELF_SIGNED" Possible values: ["SELF_SIGNED", "SUBORDINATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#type PrivatecaCertificateAuthority#type}
        :param user_defined_access_urls: user_defined_access_urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#user_defined_access_urls PrivatecaCertificateAuthority#user_defined_access_urls}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = PrivatecaCertificateAuthorityConfigA(**config)
        if isinstance(key_spec, dict):
            key_spec = PrivatecaCertificateAuthorityKeySpec(**key_spec)
        if isinstance(subordinate_config, dict):
            subordinate_config = PrivatecaCertificateAuthoritySubordinateConfig(**subordinate_config)
        if isinstance(timeouts, dict):
            timeouts = PrivatecaCertificateAuthorityTimeouts(**timeouts)
        if isinstance(user_defined_access_urls, dict):
            user_defined_access_urls = PrivatecaCertificateAuthorityUserDefinedAccessUrls(**user_defined_access_urls)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7872949dd9dfffd004e280f41536b66ae6818852ecb053b2f93d96d72c179c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument certificate_authority_id", value=certificate_authority_id, expected_type=type_hints["certificate_authority_id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument key_spec", value=key_spec, expected_type=type_hints["key_spec"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument pool", value=pool, expected_type=type_hints["pool"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument gcs_bucket", value=gcs_bucket, expected_type=type_hints["gcs_bucket"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_active_certificates_on_deletion", value=ignore_active_certificates_on_deletion, expected_type=type_hints["ignore_active_certificates_on_deletion"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument lifetime", value=lifetime, expected_type=type_hints["lifetime"])
            check_type(argname="argument pem_ca_certificate", value=pem_ca_certificate, expected_type=type_hints["pem_ca_certificate"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument skip_grace_period", value=skip_grace_period, expected_type=type_hints["skip_grace_period"])
            check_type(argname="argument subordinate_config", value=subordinate_config, expected_type=type_hints["subordinate_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_defined_access_urls", value=user_defined_access_urls, expected_type=type_hints["user_defined_access_urls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_authority_id": certificate_authority_id,
            "config": config,
            "key_spec": key_spec,
            "location": location,
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
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if gcs_bucket is not None:
            self._values["gcs_bucket"] = gcs_bucket
        if id is not None:
            self._values["id"] = id
        if ignore_active_certificates_on_deletion is not None:
            self._values["ignore_active_certificates_on_deletion"] = ignore_active_certificates_on_deletion
        if labels is not None:
            self._values["labels"] = labels
        if lifetime is not None:
            self._values["lifetime"] = lifetime
        if pem_ca_certificate is not None:
            self._values["pem_ca_certificate"] = pem_ca_certificate
        if project is not None:
            self._values["project"] = project
        if skip_grace_period is not None:
            self._values["skip_grace_period"] = skip_grace_period
        if subordinate_config is not None:
            self._values["subordinate_config"] = subordinate_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type
        if user_defined_access_urls is not None:
            self._values["user_defined_access_urls"] = user_defined_access_urls

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
    def certificate_authority_id(self) -> builtins.str:
        '''The user provided Resource ID for this Certificate Authority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#certificate_authority_id PrivatecaCertificateAuthority#certificate_authority_id}
        '''
        result = self._values.get("certificate_authority_id")
        assert result is not None, "Required property 'certificate_authority_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> "PrivatecaCertificateAuthorityConfigA":
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#config PrivatecaCertificateAuthority#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("PrivatecaCertificateAuthorityConfigA", result)

    @builtins.property
    def key_spec(self) -> "PrivatecaCertificateAuthorityKeySpec":
        '''key_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_spec PrivatecaCertificateAuthority#key_spec}
        '''
        result = self._values.get("key_spec")
        assert result is not None, "Required property 'key_spec' is missing"
        return typing.cast("PrivatecaCertificateAuthorityKeySpec", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location of the CertificateAuthority. A full list of valid locations can be found by running 'gcloud privateca locations list'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#location PrivatecaCertificateAuthority#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool(self) -> builtins.str:
        '''The name of the CaPool this Certificate Authority belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pool PrivatecaCertificateAuthority#pool}
        '''
        result = self._values.get("pool")
        assert result is not None, "Required property 'pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the CertificateAuthority.

        When the field is set to true or unset in Terraform state, a 'terraform apply'
        or 'terraform destroy' that would delete the CertificateAuthority will fail.
        When the field is set to false, deleting the CertificateAuthority is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#deletion_protection PrivatecaCertificateAuthority#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Desired state of the CertificateAuthority.

        Set this field to 'STAGED' to create a 'STAGED' root CA.
        Possible values: ENABLED, DISABLED, STAGED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#desired_state PrivatecaCertificateAuthority#desired_state}
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs_bucket(self) -> typing.Optional[builtins.str]:
        '''The name of a Cloud Storage bucket where this CertificateAuthority will publish content, such as the CA certificate and CRLs.

        This must be a bucket name, without any prefixes
        (such as 'gs://') or suffixes (such as '.googleapis.com'). For example, to use a bucket named
        my-bucket, you would simply specify 'my-bucket'. If not specified, a managed bucket will be
        created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#gcs_bucket PrivatecaCertificateAuthority#gcs_bucket}
        '''
        result = self._values.get("gcs_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#id PrivatecaCertificateAuthority#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_active_certificates_on_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field allows the CA to be deleted even if the CA has active certs.

        Active certs include both unrevoked and unexpired certs.
        Use with care. Defaults to 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ignore_active_certificates_on_deletion PrivatecaCertificateAuthority#ignore_active_certificates_on_deletion}
        '''
        result = self._values.get("ignore_active_certificates_on_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels with user-defined metadata.

        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass":
        "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#labels PrivatecaCertificateAuthority#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lifetime(self) -> typing.Optional[builtins.str]:
        '''The desired lifetime of the CA certificate.

        Used to create the "notBeforeTime" and
        "notAfterTime" fields inside an X.509 certificate. A duration in seconds with up to nine
        fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#lifetime PrivatecaCertificateAuthority#lifetime}
        '''
        result = self._values.get("lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''The signed CA certificate issued from the subordinated CA's CSR.

        This is needed when activating the subordiante CA with a third party issuer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pem_ca_certificate PrivatecaCertificateAuthority#pem_ca_certificate}
        '''
        result = self._values.get("pem_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#project PrivatecaCertificateAuthority#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_grace_period(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this flag is set, the Certificate Authority will be deleted as soon as possible without a 30-day grace period where undeletion would have been allowed.

        If you proceed, there will be no way to recover this CA.
        Use with care. Defaults to 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#skip_grace_period PrivatecaCertificateAuthority#skip_grace_period}
        '''
        result = self._values.get("skip_grace_period")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subordinate_config(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthoritySubordinateConfig"]:
        '''subordinate_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subordinate_config PrivatecaCertificateAuthority#subordinate_config}
        '''
        result = self._values.get("subordinate_config")
        return typing.cast(typing.Optional["PrivatecaCertificateAuthoritySubordinateConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PrivatecaCertificateAuthorityTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#timeouts PrivatecaCertificateAuthority#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The Type of this CertificateAuthority.

        ~> **Note:** For 'SUBORDINATE' Certificate Authorities, they need to
        be activated before they can issue certificates. Default value: "SELF_SIGNED" Possible values: ["SELF_SIGNED", "SUBORDINATE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#type PrivatecaCertificateAuthority#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_defined_access_urls(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityUserDefinedAccessUrls"]:
        '''user_defined_access_urls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#user_defined_access_urls PrivatecaCertificateAuthority#user_defined_access_urls}
        '''
        result = self._values.get("user_defined_access_urls")
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityUserDefinedAccessUrls"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "subject_config": "subjectConfig",
        "x509_config": "x509Config",
        "subject_key_id": "subjectKeyId",
    },
)
class PrivatecaCertificateAuthorityConfigA:
    def __init__(
        self,
        *,
        subject_config: typing.Union["PrivatecaCertificateAuthorityConfigSubjectConfig", typing.Dict[builtins.str, typing.Any]],
        x509_config: typing.Union["PrivatecaCertificateAuthorityConfigX509Config", typing.Dict[builtins.str, typing.Any]],
        subject_key_id: typing.Optional[typing.Union["PrivatecaCertificateAuthorityConfigSubjectKeyId", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param subject_config: subject_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject_config PrivatecaCertificateAuthority#subject_config}
        :param x509_config: x509_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#x509_config PrivatecaCertificateAuthority#x509_config}
        :param subject_key_id: subject_key_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject_key_id PrivatecaCertificateAuthority#subject_key_id}
        '''
        if isinstance(subject_config, dict):
            subject_config = PrivatecaCertificateAuthorityConfigSubjectConfig(**subject_config)
        if isinstance(x509_config, dict):
            x509_config = PrivatecaCertificateAuthorityConfigX509Config(**x509_config)
        if isinstance(subject_key_id, dict):
            subject_key_id = PrivatecaCertificateAuthorityConfigSubjectKeyId(**subject_key_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a43f2b036bb8b50f0107c3afb58b6723fc5f774c82dcdf3bbcf054bd3cc4c3)
            check_type(argname="argument subject_config", value=subject_config, expected_type=type_hints["subject_config"])
            check_type(argname="argument x509_config", value=x509_config, expected_type=type_hints["x509_config"])
            check_type(argname="argument subject_key_id", value=subject_key_id, expected_type=type_hints["subject_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject_config": subject_config,
            "x509_config": x509_config,
        }
        if subject_key_id is not None:
            self._values["subject_key_id"] = subject_key_id

    @builtins.property
    def subject_config(self) -> "PrivatecaCertificateAuthorityConfigSubjectConfig":
        '''subject_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject_config PrivatecaCertificateAuthority#subject_config}
        '''
        result = self._values.get("subject_config")
        assert result is not None, "Required property 'subject_config' is missing"
        return typing.cast("PrivatecaCertificateAuthorityConfigSubjectConfig", result)

    @builtins.property
    def x509_config(self) -> "PrivatecaCertificateAuthorityConfigX509Config":
        '''x509_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#x509_config PrivatecaCertificateAuthority#x509_config}
        '''
        result = self._values.get("x509_config")
        assert result is not None, "Required property 'x509_config' is missing"
        return typing.cast("PrivatecaCertificateAuthorityConfigX509Config", result)

    @builtins.property
    def subject_key_id(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityConfigSubjectKeyId"]:
        '''subject_key_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject_key_id PrivatecaCertificateAuthority#subject_key_id}
        '''
        result = self._values.get("subject_key_id")
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityConfigSubjectKeyId"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c890d62b935fb583cf88cca701a69af7321b22c08530b13841a688e210fa2858)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubjectConfig")
    def put_subject_config(
        self,
        *,
        subject: typing.Union["PrivatecaCertificateAuthorityConfigSubjectConfigSubject", typing.Dict[builtins.str, typing.Any]],
        subject_alt_name: typing.Optional[typing.Union["PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject PrivatecaCertificateAuthority#subject}
        :param subject_alt_name: subject_alt_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject_alt_name PrivatecaCertificateAuthority#subject_alt_name}
        '''
        value = PrivatecaCertificateAuthorityConfigSubjectConfig(
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
        :param key_id: The value of the KeyId in lowercase hexadecimal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_id PrivatecaCertificateAuthority#key_id}
        '''
        value = PrivatecaCertificateAuthorityConfigSubjectKeyId(key_id=key_id)

        return typing.cast(None, jsii.invoke(self, "putSubjectKeyId", [value]))

    @jsii.member(jsii_name="putX509Config")
    def put_x509_config(
        self,
        *,
        ca_options: typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigCaOptions", typing.Dict[builtins.str, typing.Any]],
        key_usage: typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage", typing.Dict[builtins.str, typing.Any]],
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        name_constraints: typing.Optional[typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ca_options PrivatecaCertificateAuthority#ca_options}
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_usage PrivatecaCertificateAuthority#key_usage}
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#additional_extensions PrivatecaCertificateAuthority#additional_extensions}
        :param aia_ocsp_servers: Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#aia_ocsp_servers PrivatecaCertificateAuthority#aia_ocsp_servers}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#name_constraints PrivatecaCertificateAuthority#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#policy_ids PrivatecaCertificateAuthority#policy_ids}
        '''
        value = PrivatecaCertificateAuthorityConfigX509Config(
            ca_options=ca_options,
            key_usage=key_usage,
            additional_extensions=additional_extensions,
            aia_ocsp_servers=aia_ocsp_servers,
            name_constraints=name_constraints,
            policy_ids=policy_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putX509Config", [value]))

    @jsii.member(jsii_name="resetSubjectKeyId")
    def reset_subject_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="subjectConfig")
    def subject_config(
        self,
    ) -> "PrivatecaCertificateAuthorityConfigSubjectConfigOutputReference":
        return typing.cast("PrivatecaCertificateAuthorityConfigSubjectConfigOutputReference", jsii.get(self, "subjectConfig"))

    @builtins.property
    @jsii.member(jsii_name="subjectKeyId")
    def subject_key_id(
        self,
    ) -> "PrivatecaCertificateAuthorityConfigSubjectKeyIdOutputReference":
        return typing.cast("PrivatecaCertificateAuthorityConfigSubjectKeyIdOutputReference", jsii.get(self, "subjectKeyId"))

    @builtins.property
    @jsii.member(jsii_name="x509Config")
    def x509_config(
        self,
    ) -> "PrivatecaCertificateAuthorityConfigX509ConfigOutputReference":
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigOutputReference", jsii.get(self, "x509Config"))

    @builtins.property
    @jsii.member(jsii_name="subjectConfigInput")
    def subject_config_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityConfigSubjectConfig"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityConfigSubjectConfig"], jsii.get(self, "subjectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectKeyIdInput")
    def subject_key_id_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityConfigSubjectKeyId"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityConfigSubjectKeyId"], jsii.get(self, "subjectKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="x509ConfigInput")
    def x509_config_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityConfigX509Config"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityConfigX509Config"], jsii.get(self, "x509ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PrivatecaCertificateAuthorityConfigA]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b14430ad8654d79888cfc80e4c2ce3ab1d5a0f581ede2bbf47d8ac8d2cc2278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigSubjectConfig",
    jsii_struct_bases=[],
    name_mapping={"subject": "subject", "subject_alt_name": "subjectAltName"},
)
class PrivatecaCertificateAuthorityConfigSubjectConfig:
    def __init__(
        self,
        *,
        subject: typing.Union["PrivatecaCertificateAuthorityConfigSubjectConfigSubject", typing.Dict[builtins.str, typing.Any]],
        subject_alt_name: typing.Optional[typing.Union["PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject PrivatecaCertificateAuthority#subject}
        :param subject_alt_name: subject_alt_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject_alt_name PrivatecaCertificateAuthority#subject_alt_name}
        '''
        if isinstance(subject, dict):
            subject = PrivatecaCertificateAuthorityConfigSubjectConfigSubject(**subject)
        if isinstance(subject_alt_name, dict):
            subject_alt_name = PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName(**subject_alt_name)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cccfdfeabc1229045a3816c6fc0eca0f3bbe0a2b90052b225ec83753d16ede7)
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument subject_alt_name", value=subject_alt_name, expected_type=type_hints["subject_alt_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject": subject,
        }
        if subject_alt_name is not None:
            self._values["subject_alt_name"] = subject_alt_name

    @builtins.property
    def subject(self) -> "PrivatecaCertificateAuthorityConfigSubjectConfigSubject":
        '''subject block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject PrivatecaCertificateAuthority#subject}
        '''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast("PrivatecaCertificateAuthorityConfigSubjectConfigSubject", result)

    @builtins.property
    def subject_alt_name(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName"]:
        '''subject_alt_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#subject_alt_name PrivatecaCertificateAuthority#subject_alt_name}
        '''
        result = self._values.get("subject_alt_name")
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigSubjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigSubjectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigSubjectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01bc49e30fbf2436d68ae992f90c846cb99719c51766c49459d2e0127e82f03a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubject")
    def put_subject(
        self,
        *,
        common_name: builtins.str,
        country_code: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        street_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_name: The common name of the distinguished name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#common_name PrivatecaCertificateAuthority#common_name}
        :param country_code: The country code of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#country_code PrivatecaCertificateAuthority#country_code}
        :param locality: The locality or city of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#locality PrivatecaCertificateAuthority#locality}
        :param organization: The organization of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#organization PrivatecaCertificateAuthority#organization}
        :param organizational_unit: The organizational unit of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#organizational_unit PrivatecaCertificateAuthority#organizational_unit}
        :param postal_code: The postal code of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#postal_code PrivatecaCertificateAuthority#postal_code}
        :param province: The province, territory, or regional state of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#province PrivatecaCertificateAuthority#province}
        :param street_address: The street address of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#street_address PrivatecaCertificateAuthority#street_address}
        '''
        value = PrivatecaCertificateAuthorityConfigSubjectConfigSubject(
            common_name=common_name,
            country_code=country_code,
            locality=locality,
            organization=organization,
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
        :param dns_names: Contains only valid, fully-qualified host names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#dns_names PrivatecaCertificateAuthority#dns_names}
        :param email_addresses: Contains only valid RFC 2822 E-mail addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#email_addresses PrivatecaCertificateAuthority#email_addresses}
        :param ip_addresses: Contains only valid 32-bit IPv4 addresses or RFC 4291 IPv6 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ip_addresses PrivatecaCertificateAuthority#ip_addresses}
        :param uris: Contains only valid RFC 3986 URIs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#uris PrivatecaCertificateAuthority#uris}
        '''
        value = PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName(
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
    ) -> "PrivatecaCertificateAuthorityConfigSubjectConfigSubjectOutputReference":
        return typing.cast("PrivatecaCertificateAuthorityConfigSubjectConfigSubjectOutputReference", jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="subjectAltName")
    def subject_alt_name(
        self,
    ) -> "PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltNameOutputReference":
        return typing.cast("PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltNameOutputReference", jsii.get(self, "subjectAltName"))

    @builtins.property
    @jsii.member(jsii_name="subjectAltNameInput")
    def subject_alt_name_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName"], jsii.get(self, "subjectAltNameInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityConfigSubjectConfigSubject"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityConfigSubjectConfigSubject"], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfig]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37bee8188c73b52a018a5ce4ba10d160601e41c201204c531af1275e081659b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigSubjectConfigSubject",
    jsii_struct_bases=[],
    name_mapping={
        "common_name": "commonName",
        "country_code": "countryCode",
        "locality": "locality",
        "organization": "organization",
        "organizational_unit": "organizationalUnit",
        "postal_code": "postalCode",
        "province": "province",
        "street_address": "streetAddress",
    },
)
class PrivatecaCertificateAuthorityConfigSubjectConfigSubject:
    def __init__(
        self,
        *,
        common_name: builtins.str,
        country_code: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        street_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_name: The common name of the distinguished name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#common_name PrivatecaCertificateAuthority#common_name}
        :param country_code: The country code of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#country_code PrivatecaCertificateAuthority#country_code}
        :param locality: The locality or city of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#locality PrivatecaCertificateAuthority#locality}
        :param organization: The organization of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#organization PrivatecaCertificateAuthority#organization}
        :param organizational_unit: The organizational unit of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#organizational_unit PrivatecaCertificateAuthority#organizational_unit}
        :param postal_code: The postal code of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#postal_code PrivatecaCertificateAuthority#postal_code}
        :param province: The province, territory, or regional state of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#province PrivatecaCertificateAuthority#province}
        :param street_address: The street address of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#street_address PrivatecaCertificateAuthority#street_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ed142dacf80c7810112c7965e2a12b97355e62d554348a3d5932b2add4f03b)
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument street_address", value=street_address, expected_type=type_hints["street_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "common_name": common_name,
        }
        if country_code is not None:
            self._values["country_code"] = country_code
        if locality is not None:
            self._values["locality"] = locality
        if organization is not None:
            self._values["organization"] = organization
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#common_name PrivatecaCertificateAuthority#common_name}
        '''
        result = self._values.get("common_name")
        assert result is not None, "Required property 'common_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def country_code(self) -> typing.Optional[builtins.str]:
        '''The country code of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#country_code PrivatecaCertificateAuthority#country_code}
        '''
        result = self._values.get("country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''The locality or city of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#locality PrivatecaCertificateAuthority#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The organization of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#organization PrivatecaCertificateAuthority#organization}
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organizational_unit(self) -> typing.Optional[builtins.str]:
        '''The organizational unit of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#organizational_unit PrivatecaCertificateAuthority#organizational_unit}
        '''
        result = self._values.get("organizational_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''The postal code of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#postal_code PrivatecaCertificateAuthority#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''The province, territory, or regional state of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#province PrivatecaCertificateAuthority#province}
        '''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def street_address(self) -> typing.Optional[builtins.str]:
        '''The street address of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#street_address PrivatecaCertificateAuthority#street_address}
        '''
        result = self._values.get("street_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigSubjectConfigSubject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName",
    jsii_struct_bases=[],
    name_mapping={
        "dns_names": "dnsNames",
        "email_addresses": "emailAddresses",
        "ip_addresses": "ipAddresses",
        "uris": "uris",
    },
)
class PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName:
    def __init__(
        self,
        *,
        dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param dns_names: Contains only valid, fully-qualified host names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#dns_names PrivatecaCertificateAuthority#dns_names}
        :param email_addresses: Contains only valid RFC 2822 E-mail addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#email_addresses PrivatecaCertificateAuthority#email_addresses}
        :param ip_addresses: Contains only valid 32-bit IPv4 addresses or RFC 4291 IPv6 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ip_addresses PrivatecaCertificateAuthority#ip_addresses}
        :param uris: Contains only valid RFC 3986 URIs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#uris PrivatecaCertificateAuthority#uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a4c670cae9273b88f910135fe562071bb79454183b924f41b7c383c5a84ab4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#dns_names PrivatecaCertificateAuthority#dns_names}
        '''
        result = self._values.get("dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains only valid RFC 2822 E-mail addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#email_addresses PrivatecaCertificateAuthority#email_addresses}
        '''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains only valid 32-bit IPv4 addresses or RFC 4291 IPv6 addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ip_addresses PrivatecaCertificateAuthority#ip_addresses}
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains only valid RFC 3986 URIs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#uris PrivatecaCertificateAuthority#uris}
        '''
        result = self._values.get("uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__286dd68ecf7393befe84f53ddcf70b37c873a18e2b7c2b45ab72b7af63195b37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51ad48fdb2808a450af467c4a4228b6a5562d7235c74c0d168f47534bf207210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d157312c33c06d28cef325bf64352a01c16fb7832699912c6394fe08a7c51472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26efd03fb1fb457d49123d87aed7219dba62942f0272cfd4910c746eac9ab12e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uris")
    def uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "uris"))

    @uris.setter
    def uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90587abe4dac3806ddc4298d3f6f7a08e2704fb99e6858b5a82feebf3b02b9ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad05c75d97b2ab3d4f01dd0b7289ef463f086f981a8cec483274c805b1790e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateAuthorityConfigSubjectConfigSubjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigSubjectConfigSubjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc7d2d50001fff99023697e34110353f24fbef8ad976115badfb3a0e1fd81891)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCountryCode")
    def reset_country_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountryCode", []))

    @jsii.member(jsii_name="resetLocality")
    def reset_locality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocality", []))

    @jsii.member(jsii_name="resetOrganization")
    def reset_organization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganization", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9baeb5c01ac1b94d285b2693ddc93383d0f936419dac4f2dcca51c6831f1039f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc0c855389f3b45964719d086f305aea6fe922a5d70bb66214cc0df4380ca67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d005be853ecb65f5dedff5441e86e5085f466e6c3858b011627d31ee55d54bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef56d882dacec6fd2ac25ea3546bfe6cd2bb59dffeb12a989475c670072efa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationalUnit")
    def organizational_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationalUnit"))

    @organizational_unit.setter
    def organizational_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b012a6d75f23b9bee779f7474527c3bc9a98380652a18348bed9fed3d401b176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6669aeba2efb1524e2310d3c93524546cb848e629931982cc1975e729116951c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f4e73501f4486fd3bb4c3e84c87fa87254fcb71691baf595fff654ad39f78d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streetAddress")
    def street_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streetAddress"))

    @street_address.setter
    def street_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e0034765415145ef6d276ff5601cef6e7b02bf78619cc9a21353f7e7d41e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streetAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfigSubject]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfigSubject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfigSubject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e898cffdffbd2f40430323084bbb53df77990370d982151b62251c7c6b01f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigSubjectKeyId",
    jsii_struct_bases=[],
    name_mapping={"key_id": "keyId"},
)
class PrivatecaCertificateAuthorityConfigSubjectKeyId:
    def __init__(self, *, key_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param key_id: The value of the KeyId in lowercase hexadecimal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_id PrivatecaCertificateAuthority#key_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f26b322640b7d2d46fe614fd4068b0a6064208c40245cef8787a41ae0089245)
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key_id is not None:
            self._values["key_id"] = key_id

    @builtins.property
    def key_id(self) -> typing.Optional[builtins.str]:
        '''The value of the KeyId in lowercase hexadecimal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_id PrivatecaCertificateAuthority#key_id}
        '''
        result = self._values.get("key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigSubjectKeyId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigSubjectKeyIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigSubjectKeyIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00c7ceeb076f2de9011286e74ecdc4be2db599e549a023428f15667f354685bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25e9cded17a1b67b5ef83a0201f3dd808b043316b8632af03d8dabed119ac220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigSubjectKeyId]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigSubjectKeyId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigSubjectKeyId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0f7db5d014e9e216a073d57a48687d7a855df4e7ed907b43263f9dd35432c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509Config",
    jsii_struct_bases=[],
    name_mapping={
        "ca_options": "caOptions",
        "key_usage": "keyUsage",
        "additional_extensions": "additionalExtensions",
        "aia_ocsp_servers": "aiaOcspServers",
        "name_constraints": "nameConstraints",
        "policy_ids": "policyIds",
    },
)
class PrivatecaCertificateAuthorityConfigX509Config:
    def __init__(
        self,
        *,
        ca_options: typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigCaOptions", typing.Dict[builtins.str, typing.Any]],
        key_usage: typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage", typing.Dict[builtins.str, typing.Any]],
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        name_constraints: typing.Optional[typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ca_options PrivatecaCertificateAuthority#ca_options}
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_usage PrivatecaCertificateAuthority#key_usage}
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#additional_extensions PrivatecaCertificateAuthority#additional_extensions}
        :param aia_ocsp_servers: Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#aia_ocsp_servers PrivatecaCertificateAuthority#aia_ocsp_servers}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#name_constraints PrivatecaCertificateAuthority#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#policy_ids PrivatecaCertificateAuthority#policy_ids}
        '''
        if isinstance(ca_options, dict):
            ca_options = PrivatecaCertificateAuthorityConfigX509ConfigCaOptions(**ca_options)
        if isinstance(key_usage, dict):
            key_usage = PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage(**key_usage)
        if isinstance(name_constraints, dict):
            name_constraints = PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints(**name_constraints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04cef0fa5818d60d2bc525bbb3f8745b380632ecb1a61bfc1bf3b4d4fab8b54d)
            check_type(argname="argument ca_options", value=ca_options, expected_type=type_hints["ca_options"])
            check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            check_type(argname="argument additional_extensions", value=additional_extensions, expected_type=type_hints["additional_extensions"])
            check_type(argname="argument aia_ocsp_servers", value=aia_ocsp_servers, expected_type=type_hints["aia_ocsp_servers"])
            check_type(argname="argument name_constraints", value=name_constraints, expected_type=type_hints["name_constraints"])
            check_type(argname="argument policy_ids", value=policy_ids, expected_type=type_hints["policy_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ca_options": ca_options,
            "key_usage": key_usage,
        }
        if additional_extensions is not None:
            self._values["additional_extensions"] = additional_extensions
        if aia_ocsp_servers is not None:
            self._values["aia_ocsp_servers"] = aia_ocsp_servers
        if name_constraints is not None:
            self._values["name_constraints"] = name_constraints
        if policy_ids is not None:
            self._values["policy_ids"] = policy_ids

    @builtins.property
    def ca_options(self) -> "PrivatecaCertificateAuthorityConfigX509ConfigCaOptions":
        '''ca_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ca_options PrivatecaCertificateAuthority#ca_options}
        '''
        result = self._values.get("ca_options")
        assert result is not None, "Required property 'ca_options' is missing"
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigCaOptions", result)

    @builtins.property
    def key_usage(self) -> "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage":
        '''key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_usage PrivatecaCertificateAuthority#key_usage}
        '''
        result = self._values.get("key_usage")
        assert result is not None, "Required property 'key_usage' is missing"
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage", result)

    @builtins.property
    def additional_extensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions"]]]:
        '''additional_extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#additional_extensions PrivatecaCertificateAuthority#additional_extensions}
        '''
        result = self._values.get("additional_extensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions"]]], result)

    @builtins.property
    def aia_ocsp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#aia_ocsp_servers PrivatecaCertificateAuthority#aia_ocsp_servers}
        '''
        result = self._values.get("aia_ocsp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name_constraints(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints"]:
        '''name_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#name_constraints PrivatecaCertificateAuthority#name_constraints}
        '''
        result = self._values.get("name_constraints")
        return typing.cast(typing.Optional["PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints"], result)

    @builtins.property
    def policy_ids(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds"]]]:
        '''policy_ids block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#policy_ids PrivatecaCertificateAuthority#policy_ids}
        '''
        result = self._values.get("policy_ids")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions",
    jsii_struct_bases=[],
    name_mapping={"critical": "critical", "object_id": "objectId", "value": "value"},
)
class PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions:
    def __init__(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        object_id: typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId", typing.Dict[builtins.str, typing.Any]],
        value: builtins.str,
    ) -> None:
        '''
        :param critical: Indicates whether or not this extension is critical (i.e., if the client does not know how to handle this extension, the client should consider this to be an error). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#critical PrivatecaCertificateAuthority#critical}
        :param object_id: object_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#object_id PrivatecaCertificateAuthority#object_id}
        :param value: The value of this X.509 extension. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#value PrivatecaCertificateAuthority#value}
        '''
        if isinstance(object_id, dict):
            object_id = PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId(**object_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c1f0ab57f2d87deac0c84482f791de017335c67386b9052aef9842ef0d0138)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#critical PrivatecaCertificateAuthority#critical}
        '''
        result = self._values.get("critical")
        assert result is not None, "Required property 'critical' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def object_id(
        self,
    ) -> "PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId":
        '''object_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#object_id PrivatecaCertificateAuthority#object_id}
        '''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId", result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of this X.509 extension. A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#value PrivatecaCertificateAuthority#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__755a15b1a72feada4cc80239b1eea529760a6c30d7562a089eafbc626d3af73e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074bbfa789fd3c654366420b634354ac58d8c43c1470b0584489da3f9bc7b4d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ce4ca7690668efdda30726ca3be7f82be0bfd4d368fdf6b4fa675477e01cfc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ea541e59ea54abf039a6abb955632e3e41c2f5f28e6741947d0764df6e7a76e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fba7e5fda6907293495bafc3a1a982abf23a04b8ac6c8a081e8b3bdbd3e29fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b402ad8a224038a3233bed50d0511b906304bed844734f4871060278ac4809b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#object_id_path PrivatecaCertificateAuthority#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31d3c5ae4d3bc101f246b7581010f8e873098576889e71fe3b22f6992731e14)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#object_id_path PrivatecaCertificateAuthority#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bd305fb97bd279bf8f0803952996036bbe5938e1f18e5abf679ba21e565bdad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f081614ac5bf55fab4b51f0febbddd7f9a1b853d0600047d7c89032b7879f5e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53dffd5696d9825f073acfcd3f5e36ef2e082c0bde0fdac7713b5fc1b4b04ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d3ec70fa0abe980373c60e4ecc32313f07c6fe988dddac0ef1cf9cf86f04c8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putObjectId")
    def put_object_id(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#object_id_path PrivatecaCertificateAuthority#object_id_path}
        '''
        value = PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId(
            object_id_path=object_id_path
        )

        return typing.cast(None, jsii.invoke(self, "putObjectId", [value]))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(
        self,
    ) -> PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectIdOutputReference:
        return typing.cast(PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectIdOutputReference, jsii.get(self, "objectId"))

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
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId], jsii.get(self, "objectIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f516b7c82309ed1ebeae56d7c12ff17fa5e1108dcb4a08dec034019496125a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4a3425338f83e2dcc66f457d3a03b57028388d100820d7a0f5000c45dc6dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1f110de608381ecfa47e50e1ed9498a1e7a8ab6802ce27f1177fa08da0fb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigCaOptions",
    jsii_struct_bases=[],
    name_mapping={
        "is_ca": "isCa",
        "max_issuer_path_length": "maxIssuerPathLength",
        "non_ca": "nonCa",
        "zero_max_issuer_path_length": "zeroMaxIssuerPathLength",
    },
)
class PrivatecaCertificateAuthorityConfigX509ConfigCaOptions:
    def __init__(
        self,
        *,
        is_ca: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        max_issuer_path_length: typing.Optional[jsii.Number] = None,
        non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_ca: When true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#is_ca PrivatecaCertificateAuthority#is_ca}
        :param max_issuer_path_length: Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Setting the value to 0 requires setting 'zero_max_issuer_path_length = true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#max_issuer_path_length PrivatecaCertificateAuthority#max_issuer_path_length}
        :param non_ca: When true, the "CA" in Basic Constraints extension will be set to false. If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#non_ca PrivatecaCertificateAuthority#non_ca}
        :param zero_max_issuer_path_length: When true, the "path length constraint" in Basic Constraints extension will be set to 0. If both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#zero_max_issuer_path_length PrivatecaCertificateAuthority#zero_max_issuer_path_length}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c597def91b7d25c91a1a2dc808036d80a019d4878ccf67b9e34041464ac41362)
            check_type(argname="argument is_ca", value=is_ca, expected_type=type_hints["is_ca"])
            check_type(argname="argument max_issuer_path_length", value=max_issuer_path_length, expected_type=type_hints["max_issuer_path_length"])
            check_type(argname="argument non_ca", value=non_ca, expected_type=type_hints["non_ca"])
            check_type(argname="argument zero_max_issuer_path_length", value=zero_max_issuer_path_length, expected_type=type_hints["zero_max_issuer_path_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_ca": is_ca,
        }
        if max_issuer_path_length is not None:
            self._values["max_issuer_path_length"] = max_issuer_path_length
        if non_ca is not None:
            self._values["non_ca"] = non_ca
        if zero_max_issuer_path_length is not None:
            self._values["zero_max_issuer_path_length"] = zero_max_issuer_path_length

    @builtins.property
    def is_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When true, the "CA" in Basic Constraints extension will be set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#is_ca PrivatecaCertificateAuthority#is_ca}
        '''
        result = self._values.get("is_ca")
        assert result is not None, "Required property 'is_ca' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def max_issuer_path_length(self) -> typing.Optional[jsii.Number]:
        '''Refers to the "path length constraint" in Basic Constraints extension.

        For a CA certificate, this value describes the depth of
        subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Setting the value to 0
        requires setting 'zero_max_issuer_path_length = true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#max_issuer_path_length PrivatecaCertificateAuthority#max_issuer_path_length}
        '''
        result = self._values.get("max_issuer_path_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def non_ca(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the "CA" in Basic Constraints extension will be set to false.

        If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#non_ca PrivatecaCertificateAuthority#non_ca}
        '''
        result = self._values.get("non_ca")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def zero_max_issuer_path_length(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the "path length constraint" in Basic Constraints extension will be set to 0.

        If both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset,
        the max path length will be omitted from the CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#zero_max_issuer_path_length PrivatecaCertificateAuthority#zero_max_issuer_path_length}
        '''
        result = self._values.get("zero_max_issuer_path_length")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509ConfigCaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigX509ConfigCaOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigCaOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4ba7567e8ae043913ec14ec38443eeced604b7e8f15db6cd655e9700dfdb6c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__a9c3491b2e7f13b4cf6caeed92336bef52c437ef2e44f27f6220644370148099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIssuerPathLength")
    def max_issuer_path_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIssuerPathLength"))

    @max_issuer_path_length.setter
    def max_issuer_path_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8d0f1e94cd310831cfbddd00681a02560ad61da62f343b05ead81bc60a38a2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7008f1637c5398ebd65c314f2a2cdccb9175df664ebc60de0f022f2c7ae8da6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b7066f8d67ce16a90a41dd23be9d2ba55717cc7d821e88af0829928b85d6657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zeroMaxIssuerPathLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigCaOptions]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigCaOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigCaOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c6a153ea985bccac92b7a9724e6c750dd9493704372940989f5ef6851912a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "base_key_usage": "baseKeyUsage",
        "extended_key_usage": "extendedKeyUsage",
        "unknown_extended_key_usages": "unknownExtendedKeyUsages",
    },
)
class PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage:
    def __init__(
        self,
        *,
        base_key_usage: typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage", typing.Dict[builtins.str, typing.Any]],
        extended_key_usage: typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage", typing.Dict[builtins.str, typing.Any]],
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#base_key_usage PrivatecaCertificateAuthority#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#extended_key_usage PrivatecaCertificateAuthority#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#unknown_extended_key_usages PrivatecaCertificateAuthority#unknown_extended_key_usages}
        '''
        if isinstance(base_key_usage, dict):
            base_key_usage = PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage(**base_key_usage)
        if isinstance(extended_key_usage, dict):
            extended_key_usage = PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage(**extended_key_usage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d6b080f601b22d113097acd168ce1d692e16208cfbb24ec66dc8c257b127f4)
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
    ) -> "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage":
        '''base_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#base_key_usage PrivatecaCertificateAuthority#base_key_usage}
        '''
        result = self._values.get("base_key_usage")
        assert result is not None, "Required property 'base_key_usage' is missing"
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage", result)

    @builtins.property
    def extended_key_usage(
        self,
    ) -> "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage":
        '''extended_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#extended_key_usage PrivatecaCertificateAuthority#extended_key_usage}
        '''
        result = self._values.get("extended_key_usage")
        assert result is not None, "Required property 'extended_key_usage' is missing"
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage", result)

    @builtins.property
    def unknown_extended_key_usages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages"]]]:
        '''unknown_extended_key_usages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#unknown_extended_key_usages PrivatecaCertificateAuthority#unknown_extended_key_usages}
        '''
        result = self._values.get("unknown_extended_key_usages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage",
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
class PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage:
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
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#cert_sign PrivatecaCertificateAuthority#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#content_commitment PrivatecaCertificateAuthority#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#crl_sign PrivatecaCertificateAuthority#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#data_encipherment PrivatecaCertificateAuthority#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#decipher_only PrivatecaCertificateAuthority#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#digital_signature PrivatecaCertificateAuthority#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#encipher_only PrivatecaCertificateAuthority#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_agreement PrivatecaCertificateAuthority#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_encipherment PrivatecaCertificateAuthority#key_encipherment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fc02b2c241ce67172cc2de5b017b9aac12dfcac27414f432f38e368217546f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#cert_sign PrivatecaCertificateAuthority#cert_sign}
        '''
        result = self._values.get("cert_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def content_commitment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#content_commitment PrivatecaCertificateAuthority#content_commitment}
        '''
        result = self._values.get("content_commitment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crl_sign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used sign certificate revocation lists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#crl_sign PrivatecaCertificateAuthority#crl_sign}
        '''
        result = self._values.get("crl_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def data_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#data_encipherment PrivatecaCertificateAuthority#data_encipherment}
        '''
        result = self._values.get("data_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def decipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to decipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#decipher_only PrivatecaCertificateAuthority#decipher_only}
        '''
        result = self._values.get("decipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def digital_signature(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for digital signatures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#digital_signature PrivatecaCertificateAuthority#digital_signature}
        '''
        result = self._values.get("digital_signature")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#encipher_only PrivatecaCertificateAuthority#encipher_only}
        '''
        result = self._values.get("encipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_agreement(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used in a key agreement protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_agreement PrivatecaCertificateAuthority#key_agreement}
        '''
        result = self._values.get("key_agreement")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher other keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_encipherment PrivatecaCertificateAuthority#key_encipherment}
        '''
        result = self._values.get("key_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f481fe0f13f353686df2fe8a95cee2385c4de9611270cff38196e9a59232117)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e95928117cb641616750db743c3ef925d7c6dc7a2dd6b39a9528f66e7b1911ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5eb961bbe5405dfa7e6cd57ddea27c2dc6b8b54309083b5dd5b5e3fe793291a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95b68c6912907390cfbcec20961b0cdbc96172e3fcda1f4897124217bd0a3abc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e34dc2011f69aa64bb160594260a63ab22d9bae7f3e90adbdad18788321b581)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d23393b83c8ec2bdcbbda2e438a226380f2f9b39939e712640ce07fc8d230fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b463af1d5ecaf3dcff6878b08424e878a61337fe28b01071ae3c394d25697d12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ba1a28801ba6e79f3b5521acb01d48d439e4fa8eaa693e46ee3c9c335b846e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f73a2d9d14e5ccb561196163bfd20a67a7979ad35a6172766e4cc443a10a1bf3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5accbc70e01f6c8a81017e90a7df76b8f827de343446eaec643130bca2800397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyEncipherment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c25c1645eb0b6a5efa54dfc798828a5b1fcb10424dedebe9783fe52c2d924f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage",
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
class PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage:
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
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#client_auth PrivatecaCertificateAuthority#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#code_signing PrivatecaCertificateAuthority#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#email_protection PrivatecaCertificateAuthority#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ocsp_signing PrivatecaCertificateAuthority#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#server_auth PrivatecaCertificateAuthority#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#time_stamping PrivatecaCertificateAuthority#time_stamping}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c105f7b0eb4b73e0efaf58190f88f1ec90b33418688455d2cc8d3f1730c066f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#client_auth PrivatecaCertificateAuthority#client_auth}
        '''
        result = self._values.get("client_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def code_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#code_signing PrivatecaCertificateAuthority#code_signing}
        '''
        result = self._values.get("code_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def email_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#email_protection PrivatecaCertificateAuthority#email_protection}
        '''
        result = self._values.get("email_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ocsp_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ocsp_signing PrivatecaCertificateAuthority#ocsp_signing}
        '''
        result = self._values.get("ocsp_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def server_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#server_auth PrivatecaCertificateAuthority#server_auth}
        '''
        result = self._values.get("server_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_stamping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#time_stamping PrivatecaCertificateAuthority#time_stamping}
        '''
        result = self._values.get("time_stamping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49601280ec82ce46ede0c79e27c84d2af0492cc47487ec7bc698bd49bf1c7db2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31b38e4e920f9e14b6b061af556572f1a5b2f52c3d51d2fc59809815541e1613)
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
            type_hints = typing.get_type_hints(_typecheckingstub__550234823fe0907242eb9a8264b197a621017c554ffaf6b73d271751aac9a97d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__965a5909b479678912b985b71ef403cc8744f2dbace31d7269eed7a8dd9fb927)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b605430989248308fd8c1a3a496df134fabc55c523c45b8fc23b6c6c6af0f11f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27ae64eafa2add1cca76e58dd53543dfc50ce6bfe6cefbc937f262ee6581f095)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5c8e2dd1026bc24abfaaab8d69d8364c8bb650e8121b15b6cb77b2c733b6283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeStamping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e1e93fe45d843835b8886ec4fdf857a2e750c031f4c8e36d23a72379fff12f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0817969fd43722cc341b705d2c7e9a44ba183916d105f03b66074a129556a5e9)
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
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#cert_sign PrivatecaCertificateAuthority#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#content_commitment PrivatecaCertificateAuthority#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#crl_sign PrivatecaCertificateAuthority#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#data_encipherment PrivatecaCertificateAuthority#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#decipher_only PrivatecaCertificateAuthority#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#digital_signature PrivatecaCertificateAuthority#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#encipher_only PrivatecaCertificateAuthority#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_agreement PrivatecaCertificateAuthority#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#key_encipherment PrivatecaCertificateAuthority#key_encipherment}
        '''
        value = PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage(
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
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#client_auth PrivatecaCertificateAuthority#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#code_signing PrivatecaCertificateAuthority#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#email_protection PrivatecaCertificateAuthority#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#ocsp_signing PrivatecaCertificateAuthority#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#server_auth PrivatecaCertificateAuthority#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#time_stamping PrivatecaCertificateAuthority#time_stamping}
        '''
        value = PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75eef3d73a84cc394f356cbd477f767982683220ef7afdc85f7923cc216b7f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUnknownExtendedKeyUsages", [value]))

    @jsii.member(jsii_name="resetUnknownExtendedKeyUsages")
    def reset_unknown_extended_key_usages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnknownExtendedKeyUsages", []))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsage")
    def base_key_usage(
        self,
    ) -> PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsageOutputReference:
        return typing.cast(PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsageOutputReference, jsii.get(self, "baseKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsage")
    def extended_key_usage(
        self,
    ) -> PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference:
        return typing.cast(PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference, jsii.get(self, "extendedKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsages")
    def unknown_extended_key_usages(
        self,
    ) -> "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList":
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList", jsii.get(self, "unknownExtendedKeyUsages"))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsageInput")
    def base_key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage], jsii.get(self, "baseKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsageInput")
    def extended_key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage], jsii.get(self, "extendedKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsagesInput")
    def unknown_extended_key_usages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages"]]], jsii.get(self, "unknownExtendedKeyUsagesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff16b51bcd94ba113b135dcb03ce8fda2978054855a0ceb7cefb15debd06287a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#object_id_path PrivatecaCertificateAuthority#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03fb73a4761f4a95bdfb0c76f2984f2d07fd9079fbb93e99673d0067bc420f5b)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#object_id_path PrivatecaCertificateAuthority#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__156f10d94daae8874fcb2e25bf077e2459f597d509654c4268ccff3859a7042f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787eb56fc8feb2ac5dc7a31ea7a31a3078f7e178b3a02dd22b03367cf51be991)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0eb4061fa55cac008a9ae889acfed1b293984eb3aa7614fbe0237f8ca8b391f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74c86ca7b218bf7d7339f6dbc123dd73ac79b634a1a91e4066daea4570e755ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4d05dae59836811c4ac5447f39f150f4c1f6ec9ef28b76b8cebc35f2df12f86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13595ba98841bb02826446a22258e50817138bf7a77e915bd5ebdcf0d6f4fcee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4986bb58fd4448bc2f4168e954140ea67ae29f4a1196796545d8d5f8e6607edb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77c111a1c258afa22a5e90b18363ccefcd43e54741893c0a997b2fa721e2bc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d0b9618f0036cf977fb093dbc5132ff1ee9bebb67fe04048ba55acecd0a1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints",
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
class PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints:
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
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#critical PrivatecaCertificateAuthority#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_dns_names PrivatecaCertificateAuthority#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_email_addresses PrivatecaCertificateAuthority#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_ip_ranges PrivatecaCertificateAuthority#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_uris PrivatecaCertificateAuthority#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_dns_names PrivatecaCertificateAuthority#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_email_addresses PrivatecaCertificateAuthority#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_ip_ranges PrivatecaCertificateAuthority#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_uris PrivatecaCertificateAuthority#permitted_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8400cc92086caa9b97fc7b53d08ce0e4e3ec560815b2d2b4be6ddac8b946b3d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#critical PrivatecaCertificateAuthority#critical}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_dns_names PrivatecaCertificateAuthority#excluded_dns_names}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_email_addresses PrivatecaCertificateAuthority#excluded_email_addresses}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_ip_ranges PrivatecaCertificateAuthority#excluded_ip_ranges}
        '''
        result = self._values.get("excluded_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_uris PrivatecaCertificateAuthority#excluded_uris}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_dns_names PrivatecaCertificateAuthority#permitted_dns_names}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_email_addresses PrivatecaCertificateAuthority#permitted_email_addresses}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_ip_ranges PrivatecaCertificateAuthority#permitted_ip_ranges}
        '''
        result = self._values.get("permitted_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_uris PrivatecaCertificateAuthority#permitted_uris}
        '''
        result = self._values.get("permitted_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigX509ConfigNameConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigNameConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__350130dae44dd29fdf7c540e934e0c7d5911644233e758f796a01c2a43c91b69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__768c6f2707b41960eb6edfa79cb5855c710d87570dcb47c1d3a8a43f562dd326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedDnsNames")
    def excluded_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedDnsNames"))

    @excluded_dns_names.setter
    def excluded_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1561ea4a5563de8da841f75c4781401748ae928b367ddad23491bf7d59115ded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedEmailAddresses")
    def excluded_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedEmailAddresses"))

    @excluded_email_addresses.setter
    def excluded_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50b432340f07f078578239965420cc67549b53efed7f4c43d68de6f9b591de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedIpRanges")
    def excluded_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedIpRanges"))

    @excluded_ip_ranges.setter
    def excluded_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602c72e823b600cc1859f96e6deffc82f16afd2c8a744d9335e9a3700a76d626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedUris")
    def excluded_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedUris"))

    @excluded_uris.setter
    def excluded_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4f726358f50f5e224f44361175f0af0ff46c59acbd9ea7a2ef75b7413eb0ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedDnsNames")
    def permitted_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedDnsNames"))

    @permitted_dns_names.setter
    def permitted_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b8dc5039c06fe7014b66a7e0ba654509bfd5149c045a0f3d5d948b2794bb68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedEmailAddresses")
    def permitted_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedEmailAddresses"))

    @permitted_email_addresses.setter
    def permitted_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a3b1c05f1ee7e170dd8bddcb73ec917b7e56387f8e39e7b5897e46ecf78c8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedIpRanges")
    def permitted_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedIpRanges"))

    @permitted_ip_ranges.setter
    def permitted_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33af664e2a0fe6ea44cff5bfaaf7042324dc01b35d95718c146b4c943ff34d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedUris")
    def permitted_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedUris"))

    @permitted_uris.setter
    def permitted_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d112e7c3c22eef255460d25fdc59f601be010d3ee5e91e17adc960052e9054e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20809ce4c0d406d3248ea27bff085befa1123d4546de1b2b962e28c9412bff2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateAuthorityConfigX509ConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83b6c2e37dc22e6d331f55bb24e662eeb77d92d38df269b1e05e7cbb06c1fba5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalExtensions")
    def put_additional_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64ceef56981f22ae3853d60d63c2b43ddaf7aa68bd685dcf2c44663ae47dfe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalExtensions", [value]))

    @jsii.member(jsii_name="putCaOptions")
    def put_ca_options(
        self,
        *,
        is_ca: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        max_issuer_path_length: typing.Optional[jsii.Number] = None,
        non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_ca: When true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#is_ca PrivatecaCertificateAuthority#is_ca}
        :param max_issuer_path_length: Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Setting the value to 0 requires setting 'zero_max_issuer_path_length = true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#max_issuer_path_length PrivatecaCertificateAuthority#max_issuer_path_length}
        :param non_ca: When true, the "CA" in Basic Constraints extension will be set to false. If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#non_ca PrivatecaCertificateAuthority#non_ca}
        :param zero_max_issuer_path_length: When true, the "path length constraint" in Basic Constraints extension will be set to 0. If both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#zero_max_issuer_path_length PrivatecaCertificateAuthority#zero_max_issuer_path_length}
        '''
        value = PrivatecaCertificateAuthorityConfigX509ConfigCaOptions(
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
        base_key_usage: typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]],
        extended_key_usage: typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]],
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#base_key_usage PrivatecaCertificateAuthority#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#extended_key_usage PrivatecaCertificateAuthority#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#unknown_extended_key_usages PrivatecaCertificateAuthority#unknown_extended_key_usages}
        '''
        value = PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage(
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
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#critical PrivatecaCertificateAuthority#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_dns_names PrivatecaCertificateAuthority#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_email_addresses PrivatecaCertificateAuthority#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_ip_ranges PrivatecaCertificateAuthority#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#excluded_uris PrivatecaCertificateAuthority#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_dns_names PrivatecaCertificateAuthority#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_email_addresses PrivatecaCertificateAuthority#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_ip_ranges PrivatecaCertificateAuthority#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#permitted_uris PrivatecaCertificateAuthority#permitted_uris}
        '''
        value = PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc828c9f70aae478289af0033c872dcb7bf4e88b8e0e4ed3f709360543e04f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyIds", [value]))

    @jsii.member(jsii_name="resetAdditionalExtensions")
    def reset_additional_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalExtensions", []))

    @jsii.member(jsii_name="resetAiaOcspServers")
    def reset_aia_ocsp_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAiaOcspServers", []))

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
    ) -> PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsList:
        return typing.cast(PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsList, jsii.get(self, "additionalExtensions"))

    @builtins.property
    @jsii.member(jsii_name="caOptions")
    def ca_options(
        self,
    ) -> PrivatecaCertificateAuthorityConfigX509ConfigCaOptionsOutputReference:
        return typing.cast(PrivatecaCertificateAuthorityConfigX509ConfigCaOptionsOutputReference, jsii.get(self, "caOptions"))

    @builtins.property
    @jsii.member(jsii_name="keyUsage")
    def key_usage(
        self,
    ) -> PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageOutputReference:
        return typing.cast(PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageOutputReference, jsii.get(self, "keyUsage"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraints")
    def name_constraints(
        self,
    ) -> PrivatecaCertificateAuthorityConfigX509ConfigNameConstraintsOutputReference:
        return typing.cast(PrivatecaCertificateAuthorityConfigX509ConfigNameConstraintsOutputReference, jsii.get(self, "nameConstraints"))

    @builtins.property
    @jsii.member(jsii_name="policyIds")
    def policy_ids(
        self,
    ) -> "PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsList":
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsList", jsii.get(self, "policyIds"))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensionsInput")
    def additional_extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]]], jsii.get(self, "additionalExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServersInput")
    def aia_ocsp_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aiaOcspServersInput"))

    @builtins.property
    @jsii.member(jsii_name="caOptionsInput")
    def ca_options_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigCaOptions]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigCaOptions], jsii.get(self, "caOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyUsageInput")
    def key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage], jsii.get(self, "keyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraintsInput")
    def name_constraints_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints], jsii.get(self, "nameConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdsInput")
    def policy_ids_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds"]]], jsii.get(self, "policyIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServers")
    def aia_ocsp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aiaOcspServers"))

    @aia_ocsp_servers.setter
    def aia_ocsp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5dc05a0cd86071e3fc5aeb8fb3a0adb3ee18b9b67df1a39ff94acc30032bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aiaOcspServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityConfigX509Config]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityConfigX509Config], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityConfigX509Config],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b47e1892430c6b5e5251d261919f22d5f67b69da6e81fcaa60cf90b14673cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#object_id_path PrivatecaCertificateAuthority#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c149e96b28a42b472a668f7960389b0546603193374473738819a2563e6ea7ce)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#object_id_path PrivatecaCertificateAuthority#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e053fb2eb2eb193023a7eadf98597e9caaff48e9e73fd9126bdffe1b28a258d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681c9926e687b5689d5f5b1b7fe315d70a13bf02b151d987f14c889794015ab5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c596041cb2031a59905dc015e21d8df65b36d200663f33055d9532179c04aa2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbde7a5a68ae465916afe542bc43f42aff76be2c031aff0406408eb2a5d4211d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23d233f933bf30dad031d84373021259293473ee5de5a1343e242a45ad377837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beecfa9b9aeda5c35591e0e01d0cf6de109e51a4868ea876ae83c1e292c84014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b815c011d05fc6bd332fbf21de4a8708d6c3c278fbe97e3142e3f0eeccca6990)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fc3b969d6f01af2da34540a79a3992d368b3a5cf0d5299b00f638eac8521e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78fa2e4e837b00358f9d242dfcfd7cf845997e717d0d926667b4324869148524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityKeySpec",
    jsii_struct_bases=[],
    name_mapping={
        "algorithm": "algorithm",
        "cloud_kms_key_version": "cloudKmsKeyVersion",
    },
)
class PrivatecaCertificateAuthorityKeySpec:
    def __init__(
        self,
        *,
        algorithm: typing.Optional[builtins.str] = None,
        cloud_kms_key_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: The algorithm to use for creating a managed Cloud KMS key for a for a simplified experience. All managed keys will be have their ProtectionLevel as HSM. Possible values: ["SIGN_HASH_ALGORITHM_UNSPECIFIED", "RSA_PSS_2048_SHA256", "RSA_PSS_3072_SHA256", "RSA_PSS_4096_SHA256", "RSA_PKCS1_2048_SHA256", "RSA_PKCS1_3072_SHA256", "RSA_PKCS1_4096_SHA256", "EC_P256_SHA256", "EC_P384_SHA384"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#algorithm PrivatecaCertificateAuthority#algorithm}
        :param cloud_kms_key_version: The resource name for an existing Cloud KMS CryptoKeyVersion in the format 'projects/* /locations/* /keyRings/* /cryptoKeys/* /cryptoKeyVersions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#cloud_kms_key_version PrivatecaCertificateAuthority#cloud_kms_key_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643d43146d277e90eb2f11a5c168fa289461da323b5a0a0a094d9c053309b5b6)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument cloud_kms_key_version", value=cloud_kms_key_version, expected_type=type_hints["cloud_kms_key_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if algorithm is not None:
            self._values["algorithm"] = algorithm
        if cloud_kms_key_version is not None:
            self._values["cloud_kms_key_version"] = cloud_kms_key_version

    @builtins.property
    def algorithm(self) -> typing.Optional[builtins.str]:
        '''The algorithm to use for creating a managed Cloud KMS key for a for a simplified experience.

        All managed keys will be have their ProtectionLevel as HSM. Possible values: ["SIGN_HASH_ALGORITHM_UNSPECIFIED", "RSA_PSS_2048_SHA256", "RSA_PSS_3072_SHA256", "RSA_PSS_4096_SHA256", "RSA_PKCS1_2048_SHA256", "RSA_PKCS1_3072_SHA256", "RSA_PKCS1_4096_SHA256", "EC_P256_SHA256", "EC_P384_SHA384"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#algorithm PrivatecaCertificateAuthority#algorithm}
        '''
        result = self._values.get("algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_kms_key_version(self) -> typing.Optional[builtins.str]:
        '''The resource name for an existing Cloud KMS CryptoKeyVersion in the format 'projects/* /locations/* /keyRings/* /cryptoKeys/* /cryptoKeyVersions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#cloud_kms_key_version PrivatecaCertificateAuthority#cloud_kms_key_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("cloud_kms_key_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityKeySpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityKeySpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityKeySpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68dd286a5fa6b118f0a76ca94314970843826bb10d6819b7ebaa173c311514c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAlgorithm")
    def reset_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlgorithm", []))

    @jsii.member(jsii_name="resetCloudKmsKeyVersion")
    def reset_cloud_kms_key_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudKmsKeyVersion", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudKmsKeyVersionInput")
    def cloud_kms_key_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudKmsKeyVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626473b17265a93296d92af88179f7a3d843bbd8275effa17a40a2b668b1c00b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudKmsKeyVersion")
    def cloud_kms_key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudKmsKeyVersion"))

    @cloud_kms_key_version.setter
    def cloud_kms_key_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caabe507b25d0c9e127b6f5640698186ec63197f785e52be71bfbcd733e0fc4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudKmsKeyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PrivatecaCertificateAuthorityKeySpec]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityKeySpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityKeySpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238383ee1d10e76e75288740f607175f18ac2d7da9ebaaba8993aea6b44b5191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthoritySubordinateConfig",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority": "certificateAuthority",
        "pem_issuer_chain": "pemIssuerChain",
    },
)
class PrivatecaCertificateAuthoritySubordinateConfig:
    def __init__(
        self,
        *,
        certificate_authority: typing.Optional[builtins.str] = None,
        pem_issuer_chain: typing.Optional[typing.Union["PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param certificate_authority: This can refer to a CertificateAuthority that was used to create a subordinate CertificateAuthority. This field is used for information and usability purposes only. The resource name is in the format 'projects/* /locations/* /caPools/* /certificateAuthorities/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#certificate_authority PrivatecaCertificateAuthority#certificate_authority} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param pem_issuer_chain: pem_issuer_chain block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pem_issuer_chain PrivatecaCertificateAuthority#pem_issuer_chain}
        '''
        if isinstance(pem_issuer_chain, dict):
            pem_issuer_chain = PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain(**pem_issuer_chain)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2523405cfce9466f8fe3f44389e3eb6ccdcb2c4cdefb2e9c88a7f117a61f97ed)
            check_type(argname="argument certificate_authority", value=certificate_authority, expected_type=type_hints["certificate_authority"])
            check_type(argname="argument pem_issuer_chain", value=pem_issuer_chain, expected_type=type_hints["pem_issuer_chain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_authority is not None:
            self._values["certificate_authority"] = certificate_authority
        if pem_issuer_chain is not None:
            self._values["pem_issuer_chain"] = pem_issuer_chain

    @builtins.property
    def certificate_authority(self) -> typing.Optional[builtins.str]:
        '''This can refer to a CertificateAuthority that was used to create a subordinate CertificateAuthority.

        This field is used for information
        and usability purposes only. The resource name is in the format
        'projects/* /locations/* /caPools/* /certificateAuthorities/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#certificate_authority PrivatecaCertificateAuthority#certificate_authority}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("certificate_authority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_issuer_chain(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain"]:
        '''pem_issuer_chain block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pem_issuer_chain PrivatecaCertificateAuthority#pem_issuer_chain}
        '''
        result = self._values.get("pem_issuer_chain")
        return typing.cast(typing.Optional["PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthoritySubordinateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthoritySubordinateConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthoritySubordinateConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5186e958e826506e9700d8615bc6b919bcaab596bf6c9128f0afb840f61d3529)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPemIssuerChain")
    def put_pem_issuer_chain(
        self,
        *,
        pem_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param pem_certificates: Expected to be in leaf-to-root order according to RFC 5246. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pem_certificates PrivatecaCertificateAuthority#pem_certificates}
        '''
        value = PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain(
            pem_certificates=pem_certificates
        )

        return typing.cast(None, jsii.invoke(self, "putPemIssuerChain", [value]))

    @jsii.member(jsii_name="resetCertificateAuthority")
    def reset_certificate_authority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateAuthority", []))

    @jsii.member(jsii_name="resetPemIssuerChain")
    def reset_pem_issuer_chain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemIssuerChain", []))

    @builtins.property
    @jsii.member(jsii_name="pemIssuerChain")
    def pem_issuer_chain(
        self,
    ) -> "PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChainOutputReference":
        return typing.cast("PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChainOutputReference", jsii.get(self, "pemIssuerChain"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityInput")
    def certificate_authority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateAuthorityInput"))

    @builtins.property
    @jsii.member(jsii_name="pemIssuerChainInput")
    def pem_issuer_chain_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain"]:
        return typing.cast(typing.Optional["PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain"], jsii.get(self, "pemIssuerChainInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthority")
    def certificate_authority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthority"))

    @certificate_authority.setter
    def certificate_authority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c472b9ff2663d071a5295cb68ffe9bc4474de82e8f677a9295ffb6f39aa7ceb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthoritySubordinateConfig]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthoritySubordinateConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthoritySubordinateConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342c8289f1ed01f95c922f994e518988dda7740d136cf8d1e9e49bf6ccdb7783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain",
    jsii_struct_bases=[],
    name_mapping={"pem_certificates": "pemCertificates"},
)
class PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain:
    def __init__(
        self,
        *,
        pem_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param pem_certificates: Expected to be in leaf-to-root order according to RFC 5246. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pem_certificates PrivatecaCertificateAuthority#pem_certificates}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f9b78bed2d9bf5e49bb5c281105eec5217d2c7b438783778523d665b3dddc3)
            check_type(argname="argument pem_certificates", value=pem_certificates, expected_type=type_hints["pem_certificates"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pem_certificates is not None:
            self._values["pem_certificates"] = pem_certificates

    @builtins.property
    def pem_certificates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Expected to be in leaf-to-root order according to RFC 5246.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#pem_certificates PrivatecaCertificateAuthority#pem_certificates}
        '''
        result = self._values.get("pem_certificates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChainOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChainOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb6705eb1c27cd3065823a7c26cbbdc110cfbcdbcdfef5d12b727e2c032635c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPemCertificates")
    def reset_pem_certificates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemCertificates", []))

    @builtins.property
    @jsii.member(jsii_name="pemCertificatesInput")
    def pem_certificates_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pemCertificatesInput"))

    @builtins.property
    @jsii.member(jsii_name="pemCertificates")
    def pem_certificates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pemCertificates"))

    @pem_certificates.setter
    def pem_certificates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b26e5bd9f03a0345c1fad5efff96aed72552b285ae0fba80088e1f57818dbc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCertificates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b43ff29ac93a60af842d6747dd920abfe43b62c9c2380f6b4a0ac6912f68cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PrivatecaCertificateAuthorityTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#create PrivatecaCertificateAuthority#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#delete PrivatecaCertificateAuthority#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#update PrivatecaCertificateAuthority#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ab65618d60b9df98d32c6eacf7983619ec4c81c1b5a08ef5493e785918d32a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#create PrivatecaCertificateAuthority#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#delete PrivatecaCertificateAuthority#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#update PrivatecaCertificateAuthority#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__051eba190c39629b3e2d356eac147239628345b8ffdafd83102803ac10490b0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96e3a1cc7d9a4d95acd5e9dce067a55131b3f6f6f2c3ff447d14000fd8dfe065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5dc9d68d1b806889ae2e70e807784db5283051b176df5c4f541da4a6003ec25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971662c2bc49ae63340eb277fc4e8f383539ec834bfdfa89808d7c23541e3626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc1326128accf35fc3427f2f1de260d8a62a017b8dcc7cc03095087a2ea021e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityUserDefinedAccessUrls",
    jsii_struct_bases=[],
    name_mapping={
        "aia_issuing_certificate_urls": "aiaIssuingCertificateUrls",
        "crl_access_urls": "crlAccessUrls",
    },
)
class PrivatecaCertificateAuthorityUserDefinedAccessUrls:
    def __init__(
        self,
        *,
        aia_issuing_certificate_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        crl_access_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aia_issuing_certificate_urls: A list of URLs where this CertificateAuthority's CA certificate is published that is specified by users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#aia_issuing_certificate_urls PrivatecaCertificateAuthority#aia_issuing_certificate_urls}
        :param crl_access_urls: A list of URLs where this CertificateAuthority's CRLs are published that is specified by users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#crl_access_urls PrivatecaCertificateAuthority#crl_access_urls}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ab36070f19031fa7a642d367de688aad08059190da68aaba3c0e763710c4cc)
            check_type(argname="argument aia_issuing_certificate_urls", value=aia_issuing_certificate_urls, expected_type=type_hints["aia_issuing_certificate_urls"])
            check_type(argname="argument crl_access_urls", value=crl_access_urls, expected_type=type_hints["crl_access_urls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aia_issuing_certificate_urls is not None:
            self._values["aia_issuing_certificate_urls"] = aia_issuing_certificate_urls
        if crl_access_urls is not None:
            self._values["crl_access_urls"] = crl_access_urls

    @builtins.property
    def aia_issuing_certificate_urls(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs where this CertificateAuthority's CA certificate is published that is specified by users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#aia_issuing_certificate_urls PrivatecaCertificateAuthority#aia_issuing_certificate_urls}
        '''
        result = self._values.get("aia_issuing_certificate_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def crl_access_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs where this CertificateAuthority's CRLs are published that is specified by users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_authority#crl_access_urls PrivatecaCertificateAuthority#crl_access_urls}
        '''
        result = self._values.get("crl_access_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateAuthorityUserDefinedAccessUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateAuthorityUserDefinedAccessUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateAuthority.PrivatecaCertificateAuthorityUserDefinedAccessUrlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3b2cc2a0408be603c74ddd4829d9cc4672c4f6d2e15f147a50c09786af4ea60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAiaIssuingCertificateUrls")
    def reset_aia_issuing_certificate_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAiaIssuingCertificateUrls", []))

    @jsii.member(jsii_name="resetCrlAccessUrls")
    def reset_crl_access_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrlAccessUrls", []))

    @builtins.property
    @jsii.member(jsii_name="aiaIssuingCertificateUrlsInput")
    def aia_issuing_certificate_urls_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aiaIssuingCertificateUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="crlAccessUrlsInput")
    def crl_access_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "crlAccessUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaIssuingCertificateUrls")
    def aia_issuing_certificate_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aiaIssuingCertificateUrls"))

    @aia_issuing_certificate_urls.setter
    def aia_issuing_certificate_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9704b5cab241a87cbc9926110bb1bb0168627fb7e0081bfa3fdbb2f09ead99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aiaIssuingCertificateUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crlAccessUrls")
    def crl_access_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "crlAccessUrls"))

    @crl_access_urls.setter
    def crl_access_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c42f5a77af880e5b70b0679adc2fbca4eb851019133e7cd3fd97eaa7bd035a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crlAccessUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateAuthorityUserDefinedAccessUrls]:
        return typing.cast(typing.Optional[PrivatecaCertificateAuthorityUserDefinedAccessUrls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateAuthorityUserDefinedAccessUrls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa39436e9a74cff6088cf936983ac97e62d199fabea242dcc6723bf529fa530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PrivatecaCertificateAuthority",
    "PrivatecaCertificateAuthorityAccessUrls",
    "PrivatecaCertificateAuthorityAccessUrlsList",
    "PrivatecaCertificateAuthorityAccessUrlsOutputReference",
    "PrivatecaCertificateAuthorityConfig",
    "PrivatecaCertificateAuthorityConfigA",
    "PrivatecaCertificateAuthorityConfigAOutputReference",
    "PrivatecaCertificateAuthorityConfigSubjectConfig",
    "PrivatecaCertificateAuthorityConfigSubjectConfigOutputReference",
    "PrivatecaCertificateAuthorityConfigSubjectConfigSubject",
    "PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName",
    "PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltNameOutputReference",
    "PrivatecaCertificateAuthorityConfigSubjectConfigSubjectOutputReference",
    "PrivatecaCertificateAuthorityConfigSubjectKeyId",
    "PrivatecaCertificateAuthorityConfigSubjectKeyIdOutputReference",
    "PrivatecaCertificateAuthorityConfigX509Config",
    "PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions",
    "PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsList",
    "PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId",
    "PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectIdOutputReference",
    "PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsOutputReference",
    "PrivatecaCertificateAuthorityConfigX509ConfigCaOptions",
    "PrivatecaCertificateAuthorityConfigX509ConfigCaOptionsOutputReference",
    "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage",
    "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage",
    "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsageOutputReference",
    "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage",
    "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsageOutputReference",
    "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageOutputReference",
    "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages",
    "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesList",
    "PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsagesOutputReference",
    "PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints",
    "PrivatecaCertificateAuthorityConfigX509ConfigNameConstraintsOutputReference",
    "PrivatecaCertificateAuthorityConfigX509ConfigOutputReference",
    "PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds",
    "PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsList",
    "PrivatecaCertificateAuthorityConfigX509ConfigPolicyIdsOutputReference",
    "PrivatecaCertificateAuthorityKeySpec",
    "PrivatecaCertificateAuthorityKeySpecOutputReference",
    "PrivatecaCertificateAuthoritySubordinateConfig",
    "PrivatecaCertificateAuthoritySubordinateConfigOutputReference",
    "PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain",
    "PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChainOutputReference",
    "PrivatecaCertificateAuthorityTimeouts",
    "PrivatecaCertificateAuthorityTimeoutsOutputReference",
    "PrivatecaCertificateAuthorityUserDefinedAccessUrls",
    "PrivatecaCertificateAuthorityUserDefinedAccessUrlsOutputReference",
]

publication.publish()

def _typecheckingstub__a1e2ded4e1de4193797f923bbb76a625d831255ac97f311bbd90e6b36f1b1652(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    certificate_authority_id: builtins.str,
    config: typing.Union[PrivatecaCertificateAuthorityConfigA, typing.Dict[builtins.str, typing.Any]],
    key_spec: typing.Union[PrivatecaCertificateAuthorityKeySpec, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    pool: builtins.str,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    desired_state: typing.Optional[builtins.str] = None,
    gcs_bucket: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_active_certificates_on_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lifetime: typing.Optional[builtins.str] = None,
    pem_ca_certificate: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    skip_grace_period: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subordinate_config: typing.Optional[typing.Union[PrivatecaCertificateAuthoritySubordinateConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PrivatecaCertificateAuthorityTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    user_defined_access_urls: typing.Optional[typing.Union[PrivatecaCertificateAuthorityUserDefinedAccessUrls, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__82fcabfe3b4c6ee50c071e220058aed6b8962ed774fb5d0459843e6b3859573a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e419641c078d6a0902bc1349cd6cc523a4d99ec1ad580e9a74606579905faace(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345c013081cbecfa85dd709d2cda248bfd644f028267aebdca8701aeaa91c9f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b82fd5b1582d7b1c697a45b6a598b62ba3e1933d5e0fdd37b68ab5e0886be77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da65a8fff5a70ed74ca8fb03563fe2776c6144a61b5188a10bde64b26a81b350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d64b879a00b9f9dd0db50cb02c270c3ae6a2ac54f20f7fca280932b4e68fa41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428a5f7a4e6c5ce074457c03e1993613b28551047f50245a0bc2ac83ce39396c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfacf4d0993ccaeb6cc4310d4a26111f3437ab28a6dff26ab9549bb15b83587d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0e3b96f14d385e811d5eb1f5268f1de754721a2d1c02756ef6002056d626a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f3da325ed35b0c6db612b4405df5728dea1217bd66560e2fda69fa24dca013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca221ccd602f865ec2e7e02ddb00a20ebce9c41a6544bea6974524201b73c97a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e2dd5686434423089cc716bd53142bef5447fd8cda1fd1bf70522c11ff09c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66056f75680062f6bc9699ac5f58a4eae50914b8397e45f8e2c850551935cee2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8b834be254b56ac9e279c7566101e82d6d3a8c5f7f238c40753a4f611fc78e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487286d8483bd759dbff722a6435c33c8216fcdf45fd173c054ed11717ac6cfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05447caf1c12171b9dfac5d3eb7f8930b745263991f73a0e56c994681e591ade(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f61d0fa2db1ad543af28841bb2633a67d96366daf2228f9ea092d543ff0b0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92996ae67b2669ca8d16409d678c38a88b7e719b9ea8881a85d014e49d386152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d07ce5df2f91f057460be3d031dd2e30923797ea2628aeef21653464cfb8bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e625e1fc2991089122653cc91bb4bbbf8ef7a8f4cd4fd277dd08f17c0f2cf32c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f623f2e7408399434131478fb2d5a9146bf0e4ef136e2fd8965ed2d48f4c6b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c0529b59727639535f7241c5510e17d12f36e60a89f228358de693908e1046(
    value: typing.Optional[PrivatecaCertificateAuthorityAccessUrls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7872949dd9dfffd004e280f41536b66ae6818852ecb053b2f93d96d72c179c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    certificate_authority_id: builtins.str,
    config: typing.Union[PrivatecaCertificateAuthorityConfigA, typing.Dict[builtins.str, typing.Any]],
    key_spec: typing.Union[PrivatecaCertificateAuthorityKeySpec, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    pool: builtins.str,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    desired_state: typing.Optional[builtins.str] = None,
    gcs_bucket: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_active_certificates_on_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lifetime: typing.Optional[builtins.str] = None,
    pem_ca_certificate: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    skip_grace_period: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subordinate_config: typing.Optional[typing.Union[PrivatecaCertificateAuthoritySubordinateConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PrivatecaCertificateAuthorityTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    user_defined_access_urls: typing.Optional[typing.Union[PrivatecaCertificateAuthorityUserDefinedAccessUrls, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a43f2b036bb8b50f0107c3afb58b6723fc5f774c82dcdf3bbcf054bd3cc4c3(
    *,
    subject_config: typing.Union[PrivatecaCertificateAuthorityConfigSubjectConfig, typing.Dict[builtins.str, typing.Any]],
    x509_config: typing.Union[PrivatecaCertificateAuthorityConfigX509Config, typing.Dict[builtins.str, typing.Any]],
    subject_key_id: typing.Optional[typing.Union[PrivatecaCertificateAuthorityConfigSubjectKeyId, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c890d62b935fb583cf88cca701a69af7321b22c08530b13841a688e210fa2858(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b14430ad8654d79888cfc80e4c2ce3ab1d5a0f581ede2bbf47d8ac8d2cc2278(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cccfdfeabc1229045a3816c6fc0eca0f3bbe0a2b90052b225ec83753d16ede7(
    *,
    subject: typing.Union[PrivatecaCertificateAuthorityConfigSubjectConfigSubject, typing.Dict[builtins.str, typing.Any]],
    subject_alt_name: typing.Optional[typing.Union[PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01bc49e30fbf2436d68ae992f90c846cb99719c51766c49459d2e0127e82f03a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bee8188c73b52a018a5ce4ba10d160601e41c201204c531af1275e081659b2(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ed142dacf80c7810112c7965e2a12b97355e62d554348a3d5932b2add4f03b(
    *,
    common_name: builtins.str,
    country_code: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    street_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a4c670cae9273b88f910135fe562071bb79454183b924f41b7c383c5a84ab4(
    *,
    dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286dd68ecf7393befe84f53ddcf70b37c873a18e2b7c2b45ab72b7af63195b37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ad48fdb2808a450af467c4a4228b6a5562d7235c74c0d168f47534bf207210(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d157312c33c06d28cef325bf64352a01c16fb7832699912c6394fe08a7c51472(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26efd03fb1fb457d49123d87aed7219dba62942f0272cfd4910c746eac9ab12e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90587abe4dac3806ddc4298d3f6f7a08e2704fb99e6858b5a82feebf3b02b9ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad05c75d97b2ab3d4f01dd0b7289ef463f086f981a8cec483274c805b1790e8(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfigSubjectAltName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7d2d50001fff99023697e34110353f24fbef8ad976115badfb3a0e1fd81891(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9baeb5c01ac1b94d285b2693ddc93383d0f936419dac4f2dcca51c6831f1039f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc0c855389f3b45964719d086f305aea6fe922a5d70bb66214cc0df4380ca67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d005be853ecb65f5dedff5441e86e5085f466e6c3858b011627d31ee55d54bd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef56d882dacec6fd2ac25ea3546bfe6cd2bb59dffeb12a989475c670072efa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b012a6d75f23b9bee779f7474527c3bc9a98380652a18348bed9fed3d401b176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6669aeba2efb1524e2310d3c93524546cb848e629931982cc1975e729116951c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f4e73501f4486fd3bb4c3e84c87fa87254fcb71691baf595fff654ad39f78d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e0034765415145ef6d276ff5601cef6e7b02bf78619cc9a21353f7e7d41e1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e898cffdffbd2f40430323084bbb53df77990370d982151b62251c7c6b01f2(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigSubjectConfigSubject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f26b322640b7d2d46fe614fd4068b0a6064208c40245cef8787a41ae0089245(
    *,
    key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c7ceeb076f2de9011286e74ecdc4be2db599e549a023428f15667f354685bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e9cded17a1b67b5ef83a0201f3dd808b043316b8632af03d8dabed119ac220(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0f7db5d014e9e216a073d57a48687d7a855df4e7ed907b43263f9dd35432c4(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigSubjectKeyId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04cef0fa5818d60d2bc525bbb3f8745b380632ecb1a61bfc1bf3b4d4fab8b54d(
    *,
    ca_options: typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigCaOptions, typing.Dict[builtins.str, typing.Any]],
    key_usage: typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage, typing.Dict[builtins.str, typing.Any]],
    additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    name_constraints: typing.Optional[typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c1f0ab57f2d87deac0c84482f791de017335c67386b9052aef9842ef0d0138(
    *,
    critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    object_id: typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId, typing.Dict[builtins.str, typing.Any]],
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755a15b1a72feada4cc80239b1eea529760a6c30d7562a089eafbc626d3af73e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074bbfa789fd3c654366420b634354ac58d8c43c1470b0584489da3f9bc7b4d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ce4ca7690668efdda30726ca3be7f82be0bfd4d368fdf6b4fa675477e01cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea541e59ea54abf039a6abb955632e3e41c2f5f28e6741947d0764df6e7a76e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fba7e5fda6907293495bafc3a1a982abf23a04b8ac6c8a081e8b3bdbd3e29fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b402ad8a224038a3233bed50d0511b906304bed844734f4871060278ac4809b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31d3c5ae4d3bc101f246b7581010f8e873098576889e71fe3b22f6992731e14(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd305fb97bd279bf8f0803952996036bbe5938e1f18e5abf679ba21e565bdad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f081614ac5bf55fab4b51f0febbddd7f9a1b853d0600047d7c89032b7879f5e3(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53dffd5696d9825f073acfcd3f5e36ef2e082c0bde0fdac7713b5fc1b4b04ad(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensionsObjectId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3ec70fa0abe980373c60e4ecc32313f07c6fe988dddac0ef1cf9cf86f04c8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f516b7c82309ed1ebeae56d7c12ff17fa5e1108dcb4a08dec034019496125a45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4a3425338f83e2dcc66f457d3a03b57028388d100820d7a0f5000c45dc6dab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1f110de608381ecfa47e50e1ed9498a1e7a8ab6802ce27f1177fa08da0fb4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c597def91b7d25c91a1a2dc808036d80a019d4878ccf67b9e34041464ac41362(
    *,
    is_ca: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    max_issuer_path_length: typing.Optional[jsii.Number] = None,
    non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ba7567e8ae043913ec14ec38443eeced604b7e8f15db6cd655e9700dfdb6c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c3491b2e7f13b4cf6caeed92336bef52c437ef2e44f27f6220644370148099(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d0f1e94cd310831cfbddd00681a02560ad61da62f343b05ead81bc60a38a2e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7008f1637c5398ebd65c314f2a2cdccb9175df664ebc60de0f022f2c7ae8da6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7066f8d67ce16a90a41dd23be9d2ba55717cc7d821e88af0829928b85d6657(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c6a153ea985bccac92b7a9724e6c750dd9493704372940989f5ef6851912a5(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigCaOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d6b080f601b22d113097acd168ce1d692e16208cfbb24ec66dc8c257b127f4(
    *,
    base_key_usage: typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]],
    extended_key_usage: typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]],
    unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fc02b2c241ce67172cc2de5b017b9aac12dfcac27414f432f38e368217546f(
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

def _typecheckingstub__6f481fe0f13f353686df2fe8a95cee2385c4de9611270cff38196e9a59232117(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95928117cb641616750db743c3ef925d7c6dc7a2dd6b39a9528f66e7b1911ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5eb961bbe5405dfa7e6cd57ddea27c2dc6b8b54309083b5dd5b5e3fe793291a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b68c6912907390cfbcec20961b0cdbc96172e3fcda1f4897124217bd0a3abc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e34dc2011f69aa64bb160594260a63ab22d9bae7f3e90adbdad18788321b581(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d23393b83c8ec2bdcbbda2e438a226380f2f9b39939e712640ce07fc8d230fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b463af1d5ecaf3dcff6878b08424e878a61337fe28b01071ae3c394d25697d12(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba1a28801ba6e79f3b5521acb01d48d439e4fa8eaa693e46ee3c9c335b846e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73a2d9d14e5ccb561196163bfd20a67a7979ad35a6172766e4cc443a10a1bf3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5accbc70e01f6c8a81017e90a7df76b8f827de343446eaec643130bca2800397(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c25c1645eb0b6a5efa54dfc798828a5b1fcb10424dedebe9783fe52c2d924f0(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageBaseKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c105f7b0eb4b73e0efaf58190f88f1ec90b33418688455d2cc8d3f1730c066f(
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

def _typecheckingstub__49601280ec82ce46ede0c79e27c84d2af0492cc47487ec7bc698bd49bf1c7db2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b38e4e920f9e14b6b061af556572f1a5b2f52c3d51d2fc59809815541e1613(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550234823fe0907242eb9a8264b197a621017c554ffaf6b73d271751aac9a97d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965a5909b479678912b985b71ef403cc8744f2dbace31d7269eed7a8dd9fb927(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b605430989248308fd8c1a3a496df134fabc55c523c45b8fc23b6c6c6af0f11f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ae64eafa2add1cca76e58dd53543dfc50ce6bfe6cefbc937f262ee6581f095(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c8e2dd1026bc24abfaaab8d69d8364c8bb650e8121b15b6cb77b2c733b6283(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e1e93fe45d843835b8886ec4fdf857a2e750c031f4c8e36d23a72379fff12f(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageExtendedKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0817969fd43722cc341b705d2c7e9a44ba183916d105f03b66074a129556a5e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75eef3d73a84cc394f356cbd477f767982683220ef7afdc85f7923cc216b7f2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff16b51bcd94ba113b135dcb03ce8fda2978054855a0ceb7cefb15debd06287a(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03fb73a4761f4a95bdfb0c76f2984f2d07fd9079fbb93e99673d0067bc420f5b(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156f10d94daae8874fcb2e25bf077e2459f597d509654c4268ccff3859a7042f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787eb56fc8feb2ac5dc7a31ea7a31a3078f7e178b3a02dd22b03367cf51be991(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0eb4061fa55cac008a9ae889acfed1b293984eb3aa7614fbe0237f8ca8b391f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c86ca7b218bf7d7339f6dbc123dd73ac79b634a1a91e4066daea4570e755ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d05dae59836811c4ac5447f39f150f4c1f6ec9ef28b76b8cebc35f2df12f86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13595ba98841bb02826446a22258e50817138bf7a77e915bd5ebdcf0d6f4fcee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4986bb58fd4448bc2f4168e954140ea67ae29f4a1196796545d8d5f8e6607edb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c111a1c258afa22a5e90b18363ccefcd43e54741893c0a997b2fa721e2bc0d(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d0b9618f0036cf977fb093dbc5132ff1ee9bebb67fe04048ba55acecd0a1be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigKeyUsageUnknownExtendedKeyUsages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8400cc92086caa9b97fc7b53d08ce0e4e3ec560815b2d2b4be6ddac8b946b3d(
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

def _typecheckingstub__350130dae44dd29fdf7c540e934e0c7d5911644233e758f796a01c2a43c91b69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768c6f2707b41960eb6edfa79cb5855c710d87570dcb47c1d3a8a43f562dd326(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1561ea4a5563de8da841f75c4781401748ae928b367ddad23491bf7d59115ded(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50b432340f07f078578239965420cc67549b53efed7f4c43d68de6f9b591de6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602c72e823b600cc1859f96e6deffc82f16afd2c8a744d9335e9a3700a76d626(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4f726358f50f5e224f44361175f0af0ff46c59acbd9ea7a2ef75b7413eb0ac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b8dc5039c06fe7014b66a7e0ba654509bfd5149c045a0f3d5d948b2794bb68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a3b1c05f1ee7e170dd8bddcb73ec917b7e56387f8e39e7b5897e46ecf78c8a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33af664e2a0fe6ea44cff5bfaaf7042324dc01b35d95718c146b4c943ff34d35(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d112e7c3c22eef255460d25fdc59f601be010d3ee5e91e17adc960052e9054e3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20809ce4c0d406d3248ea27bff085befa1123d4546de1b2b962e28c9412bff2d(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigX509ConfigNameConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b6c2e37dc22e6d331f55bb24e662eeb77d92d38df269b1e05e7cbb06c1fba5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64ceef56981f22ae3853d60d63c2b43ddaf7aa68bd685dcf2c44663ae47dfe0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc828c9f70aae478289af0033c872dcb7bf4e88b8e0e4ed3f709360543e04f07(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5dc05a0cd86071e3fc5aeb8fb3a0adb3ee18b9b67df1a39ff94acc30032bac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b47e1892430c6b5e5251d261919f22d5f67b69da6e81fcaa60cf90b14673cd(
    value: typing.Optional[PrivatecaCertificateAuthorityConfigX509Config],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c149e96b28a42b472a668f7960389b0546603193374473738819a2563e6ea7ce(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e053fb2eb2eb193023a7eadf98597e9caaff48e9e73fd9126bdffe1b28a258d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681c9926e687b5689d5f5b1b7fe315d70a13bf02b151d987f14c889794015ab5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c596041cb2031a59905dc015e21d8df65b36d200663f33055d9532179c04aa2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbde7a5a68ae465916afe542bc43f42aff76be2c031aff0406408eb2a5d4211d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d233f933bf30dad031d84373021259293473ee5de5a1343e242a45ad377837(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beecfa9b9aeda5c35591e0e01d0cf6de109e51a4868ea876ae83c1e292c84014(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b815c011d05fc6bd332fbf21de4a8708d6c3c278fbe97e3142e3f0eeccca6990(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc3b969d6f01af2da34540a79a3992d368b3a5cf0d5299b00f638eac8521e72(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fa2e4e837b00358f9d242dfcfd7cf845997e717d0d926667b4324869148524(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityConfigX509ConfigPolicyIds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643d43146d277e90eb2f11a5c168fa289461da323b5a0a0a094d9c053309b5b6(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    cloud_kms_key_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68dd286a5fa6b118f0a76ca94314970843826bb10d6819b7ebaa173c311514c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626473b17265a93296d92af88179f7a3d843bbd8275effa17a40a2b668b1c00b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caabe507b25d0c9e127b6f5640698186ec63197f785e52be71bfbcd733e0fc4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238383ee1d10e76e75288740f607175f18ac2d7da9ebaaba8993aea6b44b5191(
    value: typing.Optional[PrivatecaCertificateAuthorityKeySpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2523405cfce9466f8fe3f44389e3eb6ccdcb2c4cdefb2e9c88a7f117a61f97ed(
    *,
    certificate_authority: typing.Optional[builtins.str] = None,
    pem_issuer_chain: typing.Optional[typing.Union[PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5186e958e826506e9700d8615bc6b919bcaab596bf6c9128f0afb840f61d3529(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c472b9ff2663d071a5295cb68ffe9bc4474de82e8f677a9295ffb6f39aa7ceb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342c8289f1ed01f95c922f994e518988dda7740d136cf8d1e9e49bf6ccdb7783(
    value: typing.Optional[PrivatecaCertificateAuthoritySubordinateConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f9b78bed2d9bf5e49bb5c281105eec5217d2c7b438783778523d665b3dddc3(
    *,
    pem_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6705eb1c27cd3065823a7c26cbbdc110cfbcdbcdfef5d12b727e2c032635c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b26e5bd9f03a0345c1fad5efff96aed72552b285ae0fba80088e1f57818dbc3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b43ff29ac93a60af842d6747dd920abfe43b62c9c2380f6b4a0ac6912f68cf(
    value: typing.Optional[PrivatecaCertificateAuthoritySubordinateConfigPemIssuerChain],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ab65618d60b9df98d32c6eacf7983619ec4c81c1b5a08ef5493e785918d32a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051eba190c39629b3e2d356eac147239628345b8ffdafd83102803ac10490b0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e3a1cc7d9a4d95acd5e9dce067a55131b3f6f6f2c3ff447d14000fd8dfe065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5dc9d68d1b806889ae2e70e807784db5283051b176df5c4f541da4a6003ec25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971662c2bc49ae63340eb277fc4e8f383539ec834bfdfa89808d7c23541e3626(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc1326128accf35fc3427f2f1de260d8a62a017b8dcc7cc03095087a2ea021e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateAuthorityTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ab36070f19031fa7a642d367de688aad08059190da68aaba3c0e763710c4cc(
    *,
    aia_issuing_certificate_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    crl_access_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b2cc2a0408be603c74ddd4829d9cc4672c4f6d2e15f147a50c09786af4ea60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9704b5cab241a87cbc9926110bb1bb0168627fb7e0081bfa3fdbb2f09ead99c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c42f5a77af880e5b70b0679adc2fbca4eb851019133e7cd3fd97eaa7bd035a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa39436e9a74cff6088cf936983ac97e62d199fabea242dcc6723bf529fa530(
    value: typing.Optional[PrivatecaCertificateAuthorityUserDefinedAccessUrls],
) -> None:
    """Type checking stubs"""
    pass
