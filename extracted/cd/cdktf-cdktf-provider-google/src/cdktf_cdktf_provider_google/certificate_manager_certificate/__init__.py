r'''
# `google_certificate_manager_certificate`

Refer to the Terraform Registry for docs: [`google_certificate_manager_certificate`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate).
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


class CertificateManagerCertificate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate google_certificate_manager_certificate}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        managed: typing.Optional[typing.Union["CertificateManagerCertificateManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        self_managed: typing.Optional[typing.Union["CertificateManagerCertificateSelfManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CertificateManagerCertificateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate google_certificate_manager_certificate} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A user-defined name of the certificate. Certificate names must be unique The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#name CertificateManagerCertificate#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#description CertificateManagerCertificate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#id CertificateManagerCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the Certificate resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#labels CertificateManagerCertificate#labels}
        :param location: The Certificate Manager location. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#location CertificateManagerCertificate#location}
        :param managed: managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#managed CertificateManagerCertificate#managed}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#project CertificateManagerCertificate#project}.
        :param scope: The scope of the certificate. DEFAULT: Certificates with default scope are served from core Google data centers. If unsure, choose this option. EDGE_CACHE: Certificates with scope EDGE_CACHE are special-purposed certificates, served from Edge Points of Presence. See https://cloud.google.com/vpc/docs/edge-locations. ALL_REGIONS: Certificates with ALL_REGIONS scope are served from all GCP regions (You can only use ALL_REGIONS with global certs). See https://cloud.google.com/compute/docs/regions-zones. CLIENT_AUTH: Certificates with CLIENT_AUTH scope are used by a load balancer (TLS client) to be presented to the backend (TLS server) when backend mTLS is configured. See https://cloud.google.com/load-balancing/docs/backend-authenticated-tls-backend-mtls#client-certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#scope CertificateManagerCertificate#scope}
        :param self_managed: self_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#self_managed CertificateManagerCertificate#self_managed}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#timeouts CertificateManagerCertificate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1132dbda380d65e0651dfb0e22dd5c31e676db3821b961e22bb3e972472df5)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CertificateManagerCertificateConfig(
            name=name,
            description=description,
            id=id,
            labels=labels,
            location=location,
            managed=managed,
            project=project,
            scope=scope,
            self_managed=self_managed,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a CertificateManagerCertificate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CertificateManagerCertificate to import.
        :param import_from_id: The id of the existing CertificateManagerCertificate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CertificateManagerCertificate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047af41d432e651d2c3f1cd74c2b2c8766b7fc67f2595c194ac3f20b83659d79)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putManaged")
    def put_managed(
        self,
        *,
        dns_authorizations: typing.Optional[typing.Sequence[builtins.str]] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        issuance_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dns_authorizations: Authorizations that will be used for performing domain authorization. Either issuanceConfig or dnsAuthorizations should be specificed, but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#dns_authorizations CertificateManagerCertificate#dns_authorizations}
        :param domains: The domains for which a managed SSL certificate will be generated. Wildcard domains are only supported with DNS challenge resolution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#domains CertificateManagerCertificate#domains}
        :param issuance_config: The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/* /locations/* /certificateIssuanceConfigs/*. If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa. Either issuanceConfig or dnsAuthorizations should be specificed, but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#issuance_config CertificateManagerCertificate#issuance_config} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = CertificateManagerCertificateManaged(
            dns_authorizations=dns_authorizations,
            domains=domains,
            issuance_config=issuance_config,
        )

        return typing.cast(None, jsii.invoke(self, "putManaged", [value]))

    @jsii.member(jsii_name="putSelfManaged")
    def put_self_managed(
        self,
        *,
        certificate_pem: typing.Optional[builtins.str] = None,
        pem_certificate: typing.Optional[builtins.str] = None,
        pem_private_key: typing.Optional[builtins.str] = None,
        private_key_pem: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param certificate_pem: The certificate chain in PEM-encoded form. Leaf certificate comes first, followed by intermediate ones if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#certificate_pem CertificateManagerCertificate#certificate_pem}
        :param pem_certificate: The certificate chain in PEM-encoded form. Leaf certificate comes first, followed by intermediate ones if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#pem_certificate CertificateManagerCertificate#pem_certificate}
        :param pem_private_key: The private key of the leaf certificate in PEM-encoded form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#pem_private_key CertificateManagerCertificate#pem_private_key}
        :param private_key_pem: The private key of the leaf certificate in PEM-encoded form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#private_key_pem CertificateManagerCertificate#private_key_pem}
        '''
        value = CertificateManagerCertificateSelfManaged(
            certificate_pem=certificate_pem,
            pem_certificate=pem_certificate,
            pem_private_key=pem_private_key,
            private_key_pem=private_key_pem,
        )

        return typing.cast(None, jsii.invoke(self, "putSelfManaged", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#create CertificateManagerCertificate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#delete CertificateManagerCertificate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#update CertificateManagerCertificate#update}.
        '''
        value = CertificateManagerCertificateTimeouts(
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

    @jsii.member(jsii_name="resetManaged")
    def reset_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManaged", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetSelfManaged")
    def reset_self_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManaged", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="managed")
    def managed(self) -> "CertificateManagerCertificateManagedOutputReference":
        return typing.cast("CertificateManagerCertificateManagedOutputReference", jsii.get(self, "managed"))

    @builtins.property
    @jsii.member(jsii_name="sanDnsnames")
    def san_dnsnames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sanDnsnames"))

    @builtins.property
    @jsii.member(jsii_name="selfManaged")
    def self_managed(self) -> "CertificateManagerCertificateSelfManagedOutputReference":
        return typing.cast("CertificateManagerCertificateSelfManagedOutputReference", jsii.get(self, "selfManaged"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CertificateManagerCertificateTimeoutsOutputReference":
        return typing.cast("CertificateManagerCertificateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInput")
    def managed_input(self) -> typing.Optional["CertificateManagerCertificateManaged"]:
        return typing.cast(typing.Optional["CertificateManagerCertificateManaged"], jsii.get(self, "managedInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedInput")
    def self_managed_input(
        self,
    ) -> typing.Optional["CertificateManagerCertificateSelfManaged"]:
        return typing.cast(typing.Optional["CertificateManagerCertificateSelfManaged"], jsii.get(self, "selfManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CertificateManagerCertificateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CertificateManagerCertificateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae360e53cfb733f6c80b1875de873784041a7f898d9fe7dc92deff9eff458935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a38d28fefc064458cf2082bbe8382c91298d52c3b7c665695fca443c7d4eedb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b664cac6eaec263cacf7484e0c12bde1b80e08da87352c271ebf077afc06d61e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3893a8cb17aa7d8b040e7e964d8cbb356909defddf80904f252cd8d784e1d33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827bb7355ce2df537a41453b2a32e06244cbdb7bd9fb799a2dfe61e4903626e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be804d6420b8a991e7e84bf7cf90a6b9672217e291ab678d3f2228b753c022b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98685dc48887f23c0ace238c1c9606600a0cf7c835c55e40b1be439f10a0564b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "managed": "managed",
        "project": "project",
        "scope": "scope",
        "self_managed": "selfManaged",
        "timeouts": "timeouts",
    },
)
class CertificateManagerCertificateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        managed: typing.Optional[typing.Union["CertificateManagerCertificateManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        self_managed: typing.Optional[typing.Union["CertificateManagerCertificateSelfManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CertificateManagerCertificateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: A user-defined name of the certificate. Certificate names must be unique The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#name CertificateManagerCertificate#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#description CertificateManagerCertificate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#id CertificateManagerCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the Certificate resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#labels CertificateManagerCertificate#labels}
        :param location: The Certificate Manager location. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#location CertificateManagerCertificate#location}
        :param managed: managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#managed CertificateManagerCertificate#managed}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#project CertificateManagerCertificate#project}.
        :param scope: The scope of the certificate. DEFAULT: Certificates with default scope are served from core Google data centers. If unsure, choose this option. EDGE_CACHE: Certificates with scope EDGE_CACHE are special-purposed certificates, served from Edge Points of Presence. See https://cloud.google.com/vpc/docs/edge-locations. ALL_REGIONS: Certificates with ALL_REGIONS scope are served from all GCP regions (You can only use ALL_REGIONS with global certs). See https://cloud.google.com/compute/docs/regions-zones. CLIENT_AUTH: Certificates with CLIENT_AUTH scope are used by a load balancer (TLS client) to be presented to the backend (TLS server) when backend mTLS is configured. See https://cloud.google.com/load-balancing/docs/backend-authenticated-tls-backend-mtls#client-certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#scope CertificateManagerCertificate#scope}
        :param self_managed: self_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#self_managed CertificateManagerCertificate#self_managed}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#timeouts CertificateManagerCertificate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(managed, dict):
            managed = CertificateManagerCertificateManaged(**managed)
        if isinstance(self_managed, dict):
            self_managed = CertificateManagerCertificateSelfManaged(**self_managed)
        if isinstance(timeouts, dict):
            timeouts = CertificateManagerCertificateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e13929f43634b7cf91b2aac97bcde0886f240b74f35b7bf75972deb390b949)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument managed", value=managed, expected_type=type_hints["managed"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument self_managed", value=self_managed, expected_type=type_hints["self_managed"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if managed is not None:
            self._values["managed"] = managed
        if project is not None:
            self._values["project"] = project
        if scope is not None:
            self._values["scope"] = scope
        if self_managed is not None:
            self._values["self_managed"] = self_managed
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
    def name(self) -> builtins.str:
        '''A user-defined name of the certificate.

        Certificate names must be unique
        The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
        and all following characters must be a dash, underscore, letter or digit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#name CertificateManagerCertificate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#description CertificateManagerCertificate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#id CertificateManagerCertificate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of label tags associated with the Certificate resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#labels CertificateManagerCertificate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The Certificate Manager location. If not specified, "global" is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#location CertificateManagerCertificate#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed(self) -> typing.Optional["CertificateManagerCertificateManaged"]:
        '''managed block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#managed CertificateManagerCertificate#managed}
        '''
        result = self._values.get("managed")
        return typing.cast(typing.Optional["CertificateManagerCertificateManaged"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#project CertificateManagerCertificate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''The scope of the certificate.

        DEFAULT: Certificates with default scope are served from core Google data centers.
        If unsure, choose this option.

        EDGE_CACHE: Certificates with scope EDGE_CACHE are special-purposed certificates, served from Edge Points of Presence.
        See https://cloud.google.com/vpc/docs/edge-locations.

        ALL_REGIONS: Certificates with ALL_REGIONS scope are served from all GCP regions (You can only use ALL_REGIONS with global certs).
        See https://cloud.google.com/compute/docs/regions-zones.

        CLIENT_AUTH: Certificates with CLIENT_AUTH scope are used by a load balancer (TLS client) to be presented to the backend (TLS server) when backend mTLS is configured.
        See https://cloud.google.com/load-balancing/docs/backend-authenticated-tls-backend-mtls#client-certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#scope CertificateManagerCertificate#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def self_managed(
        self,
    ) -> typing.Optional["CertificateManagerCertificateSelfManaged"]:
        '''self_managed block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#self_managed CertificateManagerCertificate#self_managed}
        '''
        result = self._values.get("self_managed")
        return typing.cast(typing.Optional["CertificateManagerCertificateSelfManaged"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CertificateManagerCertificateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#timeouts CertificateManagerCertificate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CertificateManagerCertificateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertificateManagerCertificateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateManaged",
    jsii_struct_bases=[],
    name_mapping={
        "dns_authorizations": "dnsAuthorizations",
        "domains": "domains",
        "issuance_config": "issuanceConfig",
    },
)
class CertificateManagerCertificateManaged:
    def __init__(
        self,
        *,
        dns_authorizations: typing.Optional[typing.Sequence[builtins.str]] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        issuance_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dns_authorizations: Authorizations that will be used for performing domain authorization. Either issuanceConfig or dnsAuthorizations should be specificed, but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#dns_authorizations CertificateManagerCertificate#dns_authorizations}
        :param domains: The domains for which a managed SSL certificate will be generated. Wildcard domains are only supported with DNS challenge resolution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#domains CertificateManagerCertificate#domains}
        :param issuance_config: The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/* /locations/* /certificateIssuanceConfigs/*. If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa. Either issuanceConfig or dnsAuthorizations should be specificed, but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#issuance_config CertificateManagerCertificate#issuance_config} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9420b1a760ceee71836c11ec61b2df641cb5b23ebceb65fe008597e23fb8595d)
            check_type(argname="argument dns_authorizations", value=dns_authorizations, expected_type=type_hints["dns_authorizations"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument issuance_config", value=issuance_config, expected_type=type_hints["issuance_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_authorizations is not None:
            self._values["dns_authorizations"] = dns_authorizations
        if domains is not None:
            self._values["domains"] = domains
        if issuance_config is not None:
            self._values["issuance_config"] = issuance_config

    @builtins.property
    def dns_authorizations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Authorizations that will be used for performing domain authorization. Either issuanceConfig or dnsAuthorizations should be specificed, but not both.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#dns_authorizations CertificateManagerCertificate#dns_authorizations}
        '''
        result = self._values.get("dns_authorizations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The domains for which a managed SSL certificate will be generated. Wildcard domains are only supported with DNS challenge resolution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#domains CertificateManagerCertificate#domains}
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def issuance_config(self) -> typing.Optional[builtins.str]:
        '''The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/* /locations/* /certificateIssuanceConfigs/*.

        If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa.
        Either issuanceConfig or dnsAuthorizations should be specificed, but not both.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#issuance_config CertificateManagerCertificate#issuance_config}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("issuance_config")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertificateManagerCertificateManaged(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateManagedAuthorizationAttemptInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class CertificateManagerCertificateManagedAuthorizationAttemptInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertificateManagerCertificateManagedAuthorizationAttemptInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CertificateManagerCertificateManagedAuthorizationAttemptInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateManagedAuthorizationAttemptInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adb8dd35b2e1109cffc5d9c30c18318af24aed739fb0043df79ca954ca94e38f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e64b152818932f6d6ca397c9081d95d95f721ac6f64c66deb4bb3681c0f1448)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d93096ded0862e1e8dcbf360a373fbbf80cb73c088c2486705e0466e28382f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a7b1e6c75ebc3a8e3903b3728729d0b062a20ed244488e66172cac884d04afa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__765ddefb473f972463e1d79ee84e43f4cb1ba3ae3799829eab664918aaf1e700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9b302291d0e26eae7ccdf3c52587e62b68c795cdbe862830f7be92ed839722b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="failureReason")
    def failure_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failureReason"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CertificateManagerCertificateManagedAuthorizationAttemptInfo]:
        return typing.cast(typing.Optional[CertificateManagerCertificateManagedAuthorizationAttemptInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CertificateManagerCertificateManagedAuthorizationAttemptInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54e50da2eb226e3516d20ed2c3beb54d1f4aee7092242f390a045e4b34eea35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CertificateManagerCertificateManagedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateManagedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a61e2400c32ea7390aaab3efadc2a5cb9dc3ee47b342c03baa53ae51d53900d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDnsAuthorizations")
    def reset_dns_authorizations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsAuthorizations", []))

    @jsii.member(jsii_name="resetDomains")
    def reset_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomains", []))

    @jsii.member(jsii_name="resetIssuanceConfig")
    def reset_issuance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuanceConfig", []))

    @builtins.property
    @jsii.member(jsii_name="authorizationAttemptInfo")
    def authorization_attempt_info(
        self,
    ) -> CertificateManagerCertificateManagedAuthorizationAttemptInfoList:
        return typing.cast(CertificateManagerCertificateManagedAuthorizationAttemptInfoList, jsii.get(self, "authorizationAttemptInfo"))

    @builtins.property
    @jsii.member(jsii_name="provisioningIssue")
    def provisioning_issue(
        self,
    ) -> "CertificateManagerCertificateManagedProvisioningIssueList":
        return typing.cast("CertificateManagerCertificateManagedProvisioningIssueList", jsii.get(self, "provisioningIssue"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="dnsAuthorizationsInput")
    def dns_authorizations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsAuthorizationsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainsInput")
    def domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainsInput"))

    @builtins.property
    @jsii.member(jsii_name="issuanceConfigInput")
    def issuance_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsAuthorizations")
    def dns_authorizations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsAuthorizations"))

    @dns_authorizations.setter
    def dns_authorizations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0570cb6e48e3865a50b007041753edc45b68d4f49165eaebbe5d58e0323c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsAuthorizations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @domains.setter
    def domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd028ed45f47b20edc55b2990d36d209037796a6a7d7372fd62ecd687144738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuanceConfig")
    def issuance_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuanceConfig"))

    @issuance_config.setter
    def issuance_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0cd1f973d02df222325a5bb95653bbd2b4056edb54b7acc54c4af7ee1a5743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuanceConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CertificateManagerCertificateManaged]:
        return typing.cast(typing.Optional[CertificateManagerCertificateManaged], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CertificateManagerCertificateManaged],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2be7bf480413c7e4057614551c3ed07eecbc1f6faeb21a396b258a4e01d504d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateManagedProvisioningIssue",
    jsii_struct_bases=[],
    name_mapping={},
)
class CertificateManagerCertificateManagedProvisioningIssue:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertificateManagerCertificateManagedProvisioningIssue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CertificateManagerCertificateManagedProvisioningIssueList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateManagedProvisioningIssueList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e14e2ddc9c666260ddb57f921fa7299bec596a3a09450322eb576ddeaa4905ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CertificateManagerCertificateManagedProvisioningIssueOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b489bb2bbba662ec101a1af9349a1a1238b13a14b3ba94bab3fccb2581c1c478)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CertificateManagerCertificateManagedProvisioningIssueOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb330b7f16aab6f164703d2be57ea8e4e8721100a8ff74bcb71c30d362f51239)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b79ef616abe112792b3e4023ae2cd700a4df5b732f8e0c0c26a77f5567bc3dfd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19f108da45fe8c2c5356c9d776bab03398cc2a72624647798d1de27104b02ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CertificateManagerCertificateManagedProvisioningIssueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateManagedProvisioningIssueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__732512113e8e0f450a37faf5fede744e131bb24bba6983012b79a5ce8ed53cbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CertificateManagerCertificateManagedProvisioningIssue]:
        return typing.cast(typing.Optional[CertificateManagerCertificateManagedProvisioningIssue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CertificateManagerCertificateManagedProvisioningIssue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8daff82de983ed36fe59667f469d09e32f67e503cd906fd6d44555be3e9a6bf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateSelfManaged",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_pem": "certificatePem",
        "pem_certificate": "pemCertificate",
        "pem_private_key": "pemPrivateKey",
        "private_key_pem": "privateKeyPem",
    },
)
class CertificateManagerCertificateSelfManaged:
    def __init__(
        self,
        *,
        certificate_pem: typing.Optional[builtins.str] = None,
        pem_certificate: typing.Optional[builtins.str] = None,
        pem_private_key: typing.Optional[builtins.str] = None,
        private_key_pem: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param certificate_pem: The certificate chain in PEM-encoded form. Leaf certificate comes first, followed by intermediate ones if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#certificate_pem CertificateManagerCertificate#certificate_pem}
        :param pem_certificate: The certificate chain in PEM-encoded form. Leaf certificate comes first, followed by intermediate ones if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#pem_certificate CertificateManagerCertificate#pem_certificate}
        :param pem_private_key: The private key of the leaf certificate in PEM-encoded form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#pem_private_key CertificateManagerCertificate#pem_private_key}
        :param private_key_pem: The private key of the leaf certificate in PEM-encoded form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#private_key_pem CertificateManagerCertificate#private_key_pem}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772ce21b9496a8a2c52131c768974964072a92ca4937f5028f55136d75fc2c06)
            check_type(argname="argument certificate_pem", value=certificate_pem, expected_type=type_hints["certificate_pem"])
            check_type(argname="argument pem_certificate", value=pem_certificate, expected_type=type_hints["pem_certificate"])
            check_type(argname="argument pem_private_key", value=pem_private_key, expected_type=type_hints["pem_private_key"])
            check_type(argname="argument private_key_pem", value=private_key_pem, expected_type=type_hints["private_key_pem"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_pem is not None:
            self._values["certificate_pem"] = certificate_pem
        if pem_certificate is not None:
            self._values["pem_certificate"] = pem_certificate
        if pem_private_key is not None:
            self._values["pem_private_key"] = pem_private_key
        if private_key_pem is not None:
            self._values["private_key_pem"] = private_key_pem

    @builtins.property
    def certificate_pem(self) -> typing.Optional[builtins.str]:
        '''The certificate chain in PEM-encoded form.

        Leaf certificate comes first, followed by intermediate ones if any.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#certificate_pem CertificateManagerCertificate#certificate_pem}
        '''
        result = self._values.get("certificate_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_certificate(self) -> typing.Optional[builtins.str]:
        '''The certificate chain in PEM-encoded form.

        Leaf certificate comes first, followed by intermediate ones if any.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#pem_certificate CertificateManagerCertificate#pem_certificate}
        '''
        result = self._values.get("pem_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_private_key(self) -> typing.Optional[builtins.str]:
        '''The private key of the leaf certificate in PEM-encoded form.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#pem_private_key CertificateManagerCertificate#pem_private_key}
        '''
        result = self._values.get("pem_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_pem(self) -> typing.Optional[builtins.str]:
        '''The private key of the leaf certificate in PEM-encoded form.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#private_key_pem CertificateManagerCertificate#private_key_pem}
        '''
        result = self._values.get("private_key_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertificateManagerCertificateSelfManaged(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CertificateManagerCertificateSelfManagedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateSelfManagedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eb318e17bc68cdd523ac4c0265eb450af30f20e4f466efa1a28b10f8069ee21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCertificatePem")
    def reset_certificate_pem(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificatePem", []))

    @jsii.member(jsii_name="resetPemCertificate")
    def reset_pem_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemCertificate", []))

    @jsii.member(jsii_name="resetPemPrivateKey")
    def reset_pem_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemPrivateKey", []))

    @jsii.member(jsii_name="resetPrivateKeyPem")
    def reset_private_key_pem(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyPem", []))

    @builtins.property
    @jsii.member(jsii_name="certificatePemInput")
    def certificate_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePemInput"))

    @builtins.property
    @jsii.member(jsii_name="pemCertificateInput")
    def pem_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="pemPrivateKeyInput")
    def pem_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyPemInput")
    def private_key_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyPemInput"))

    @builtins.property
    @jsii.member(jsii_name="certificatePem")
    def certificate_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificatePem"))

    @certificate_pem.setter
    def certificate_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50f1920c6c3a8ec71f56596e11dc16deb85e5cc5332d7660b1679d0e7786b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pemCertificate")
    def pem_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemCertificate"))

    @pem_certificate.setter
    def pem_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45989325211960628bc29453bdebb122d41ae16542f7749a10931aa54c4d11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pemPrivateKey")
    def pem_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemPrivateKey"))

    @pem_private_key.setter
    def pem_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32312fc2dedad69356614bddba4bc1e30f083c4cc25be603f0bb593a93bca5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyPem")
    def private_key_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyPem"))

    @private_key_pem.setter
    def private_key_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73aafac2d00d0fa3ea42b8fb0f8212369eb7fe03ec8c0db94017a1df60ac7dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CertificateManagerCertificateSelfManaged]:
        return typing.cast(typing.Optional[CertificateManagerCertificateSelfManaged], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CertificateManagerCertificateSelfManaged],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354d931a83ad6274c8191424516f04cf5981e0ea69d4db887eae26df66decd65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CertificateManagerCertificateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#create CertificateManagerCertificate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#delete CertificateManagerCertificate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#update CertificateManagerCertificate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb90ae0112092f223d80a18b2cbba29cbe11a8b1a1f20e56fa028242ddc5ee04)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#create CertificateManagerCertificate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#delete CertificateManagerCertificate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/certificate_manager_certificate#update CertificateManagerCertificate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertificateManagerCertificateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CertificateManagerCertificateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.certificateManagerCertificate.CertificateManagerCertificateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2934eb4b4f7f828915d1d187152ced374935e6743867b092628471bce9ad1300)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5abc77738e798bd69abe592afe378a44a85c3087dd204f764e47bf2fd62a04d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad034b531eb0b9d91d8caa41b52e0833f6869db517f96aa808e0766a766a2c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725da657102402ad89e6a31aa4a37f3c54809368bd2fd9418ed2f06c574ab9ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CertificateManagerCertificateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CertificateManagerCertificateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CertificateManagerCertificateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739c2bf8f8e728271d2b6d32ab0a0f6b7369c7e5fbb0ff73c06d533801ff628a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CertificateManagerCertificate",
    "CertificateManagerCertificateConfig",
    "CertificateManagerCertificateManaged",
    "CertificateManagerCertificateManagedAuthorizationAttemptInfo",
    "CertificateManagerCertificateManagedAuthorizationAttemptInfoList",
    "CertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference",
    "CertificateManagerCertificateManagedOutputReference",
    "CertificateManagerCertificateManagedProvisioningIssue",
    "CertificateManagerCertificateManagedProvisioningIssueList",
    "CertificateManagerCertificateManagedProvisioningIssueOutputReference",
    "CertificateManagerCertificateSelfManaged",
    "CertificateManagerCertificateSelfManagedOutputReference",
    "CertificateManagerCertificateTimeouts",
    "CertificateManagerCertificateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6b1132dbda380d65e0651dfb0e22dd5c31e676db3821b961e22bb3e972472df5(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    managed: typing.Optional[typing.Union[CertificateManagerCertificateManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    self_managed: typing.Optional[typing.Union[CertificateManagerCertificateSelfManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CertificateManagerCertificateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__047af41d432e651d2c3f1cd74c2b2c8766b7fc67f2595c194ac3f20b83659d79(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae360e53cfb733f6c80b1875de873784041a7f898d9fe7dc92deff9eff458935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a38d28fefc064458cf2082bbe8382c91298d52c3b7c665695fca443c7d4eedb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b664cac6eaec263cacf7484e0c12bde1b80e08da87352c271ebf077afc06d61e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3893a8cb17aa7d8b040e7e964d8cbb356909defddf80904f252cd8d784e1d33f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827bb7355ce2df537a41453b2a32e06244cbdb7bd9fb799a2dfe61e4903626e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be804d6420b8a991e7e84bf7cf90a6b9672217e291ab678d3f2228b753c022b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98685dc48887f23c0ace238c1c9606600a0cf7c835c55e40b1be439f10a0564b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e13929f43634b7cf91b2aac97bcde0886f240b74f35b7bf75972deb390b949(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    managed: typing.Optional[typing.Union[CertificateManagerCertificateManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    self_managed: typing.Optional[typing.Union[CertificateManagerCertificateSelfManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CertificateManagerCertificateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9420b1a760ceee71836c11ec61b2df641cb5b23ebceb65fe008597e23fb8595d(
    *,
    dns_authorizations: typing.Optional[typing.Sequence[builtins.str]] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    issuance_config: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb8dd35b2e1109cffc5d9c30c18318af24aed739fb0043df79ca954ca94e38f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e64b152818932f6d6ca397c9081d95d95f721ac6f64c66deb4bb3681c0f1448(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d93096ded0862e1e8dcbf360a373fbbf80cb73c088c2486705e0466e28382f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7b1e6c75ebc3a8e3903b3728729d0b062a20ed244488e66172cac884d04afa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765ddefb473f972463e1d79ee84e43f4cb1ba3ae3799829eab664918aaf1e700(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b302291d0e26eae7ccdf3c52587e62b68c795cdbe862830f7be92ed839722b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54e50da2eb226e3516d20ed2c3beb54d1f4aee7092242f390a045e4b34eea35(
    value: typing.Optional[CertificateManagerCertificateManagedAuthorizationAttemptInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61e2400c32ea7390aaab3efadc2a5cb9dc3ee47b342c03baa53ae51d53900d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0570cb6e48e3865a50b007041753edc45b68d4f49165eaebbe5d58e0323c44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd028ed45f47b20edc55b2990d36d209037796a6a7d7372fd62ecd687144738(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0cd1f973d02df222325a5bb95653bbd2b4056edb54b7acc54c4af7ee1a5743(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2be7bf480413c7e4057614551c3ed07eecbc1f6faeb21a396b258a4e01d504d(
    value: typing.Optional[CertificateManagerCertificateManaged],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14e2ddc9c666260ddb57f921fa7299bec596a3a09450322eb576ddeaa4905ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b489bb2bbba662ec101a1af9349a1a1238b13a14b3ba94bab3fccb2581c1c478(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb330b7f16aab6f164703d2be57ea8e4e8721100a8ff74bcb71c30d362f51239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79ef616abe112792b3e4023ae2cd700a4df5b732f8e0c0c26a77f5567bc3dfd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f108da45fe8c2c5356c9d776bab03398cc2a72624647798d1de27104b02ed4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732512113e8e0f450a37faf5fede744e131bb24bba6983012b79a5ce8ed53cbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8daff82de983ed36fe59667f469d09e32f67e503cd906fd6d44555be3e9a6bf6(
    value: typing.Optional[CertificateManagerCertificateManagedProvisioningIssue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772ce21b9496a8a2c52131c768974964072a92ca4937f5028f55136d75fc2c06(
    *,
    certificate_pem: typing.Optional[builtins.str] = None,
    pem_certificate: typing.Optional[builtins.str] = None,
    pem_private_key: typing.Optional[builtins.str] = None,
    private_key_pem: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb318e17bc68cdd523ac4c0265eb450af30f20e4f466efa1a28b10f8069ee21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50f1920c6c3a8ec71f56596e11dc16deb85e5cc5332d7660b1679d0e7786b89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45989325211960628bc29453bdebb122d41ae16542f7749a10931aa54c4d11b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32312fc2dedad69356614bddba4bc1e30f083c4cc25be603f0bb593a93bca5b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73aafac2d00d0fa3ea42b8fb0f8212369eb7fe03ec8c0db94017a1df60ac7dbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354d931a83ad6274c8191424516f04cf5981e0ea69d4db887eae26df66decd65(
    value: typing.Optional[CertificateManagerCertificateSelfManaged],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb90ae0112092f223d80a18b2cbba29cbe11a8b1a1f20e56fa028242ddc5ee04(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2934eb4b4f7f828915d1d187152ced374935e6743867b092628471bce9ad1300(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abc77738e798bd69abe592afe378a44a85c3087dd204f764e47bf2fd62a04d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad034b531eb0b9d91d8caa41b52e0833f6869db517f96aa808e0766a766a2c1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725da657102402ad89e6a31aa4a37f3c54809368bd2fd9418ed2f06c574ab9ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739c2bf8f8e728271d2b6d32ab0a0f6b7369c7e5fbb0ff73c06d533801ff628a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CertificateManagerCertificateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
