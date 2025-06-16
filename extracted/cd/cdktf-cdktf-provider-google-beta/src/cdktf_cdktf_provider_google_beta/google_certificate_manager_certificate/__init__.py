r'''
# `google_certificate_manager_certificate`

Refer to the Terraform Registry for docs: [`google_certificate_manager_certificate`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate).
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


class GoogleCertificateManagerCertificate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate google_certificate_manager_certificate}.'''

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
        managed: typing.Optional[typing.Union["GoogleCertificateManagerCertificateManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        self_managed: typing.Optional[typing.Union["GoogleCertificateManagerCertificateSelfManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCertificateManagerCertificateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate google_certificate_manager_certificate} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A user-defined name of the certificate. Certificate names must be unique The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#name GoogleCertificateManagerCertificate#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#description GoogleCertificateManagerCertificate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#id GoogleCertificateManagerCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the Certificate resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#labels GoogleCertificateManagerCertificate#labels}
        :param location: The Certificate Manager location. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#location GoogleCertificateManagerCertificate#location}
        :param managed: managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#managed GoogleCertificateManagerCertificate#managed}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#project GoogleCertificateManagerCertificate#project}.
        :param scope: The scope of the certificate. DEFAULT: Certificates with default scope are served from core Google data centers. If unsure, choose this option. EDGE_CACHE: Certificates with scope EDGE_CACHE are special-purposed certificates, served from Edge Points of Presence. See https://cloud.google.com/vpc/docs/edge-locations. ALL_REGIONS: Certificates with ALL_REGIONS scope are served from all GCP regions (You can only use ALL_REGIONS with global certs). See https://cloud.google.com/compute/docs/regions-zones. CLIENT_AUTH: Certificates with CLIENT_AUTH scope are used by a load balancer (TLS client) to be presented to the backend (TLS server) when backend mTLS is configured. See https://cloud.google.com/load-balancing/docs/backend-authenticated-tls-backend-mtls#client-certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#scope GoogleCertificateManagerCertificate#scope}
        :param self_managed: self_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#self_managed GoogleCertificateManagerCertificate#self_managed}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#timeouts GoogleCertificateManagerCertificate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b2fe7f5876bb6204af9dd4385b578ece493ebb5267ffe8ce49f576ff35f584)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCertificateManagerCertificateConfig(
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
        '''Generates CDKTF code for importing a GoogleCertificateManagerCertificate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCertificateManagerCertificate to import.
        :param import_from_id: The id of the existing GoogleCertificateManagerCertificate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCertificateManagerCertificate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d87f404c0664d86ad10ae3955ad9d504c6a1e012947e4dc74d90a503355e23)
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
        :param dns_authorizations: Authorizations that will be used for performing domain authorization. Either issuanceConfig or dnsAuthorizations should be specificed, but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#dns_authorizations GoogleCertificateManagerCertificate#dns_authorizations}
        :param domains: The domains for which a managed SSL certificate will be generated. Wildcard domains are only supported with DNS challenge resolution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#domains GoogleCertificateManagerCertificate#domains}
        :param issuance_config: The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/* /locations/* /certificateIssuanceConfigs/*. If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa. Either issuanceConfig or dnsAuthorizations should be specificed, but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#issuance_config GoogleCertificateManagerCertificate#issuance_config} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleCertificateManagerCertificateManaged(
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
        :param certificate_pem: The certificate chain in PEM-encoded form. Leaf certificate comes first, followed by intermediate ones if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#certificate_pem GoogleCertificateManagerCertificate#certificate_pem}
        :param pem_certificate: The certificate chain in PEM-encoded form. Leaf certificate comes first, followed by intermediate ones if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#pem_certificate GoogleCertificateManagerCertificate#pem_certificate}
        :param pem_private_key: The private key of the leaf certificate in PEM-encoded form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#pem_private_key GoogleCertificateManagerCertificate#pem_private_key}
        :param private_key_pem: The private key of the leaf certificate in PEM-encoded form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#private_key_pem GoogleCertificateManagerCertificate#private_key_pem}
        '''
        value = GoogleCertificateManagerCertificateSelfManaged(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#create GoogleCertificateManagerCertificate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#delete GoogleCertificateManagerCertificate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#update GoogleCertificateManagerCertificate#update}.
        '''
        value = GoogleCertificateManagerCertificateTimeouts(
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
    def managed(self) -> "GoogleCertificateManagerCertificateManagedOutputReference":
        return typing.cast("GoogleCertificateManagerCertificateManagedOutputReference", jsii.get(self, "managed"))

    @builtins.property
    @jsii.member(jsii_name="sanDnsnames")
    def san_dnsnames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sanDnsnames"))

    @builtins.property
    @jsii.member(jsii_name="selfManaged")
    def self_managed(
        self,
    ) -> "GoogleCertificateManagerCertificateSelfManagedOutputReference":
        return typing.cast("GoogleCertificateManagerCertificateSelfManagedOutputReference", jsii.get(self, "selfManaged"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCertificateManagerCertificateTimeoutsOutputReference":
        return typing.cast("GoogleCertificateManagerCertificateTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def managed_input(
        self,
    ) -> typing.Optional["GoogleCertificateManagerCertificateManaged"]:
        return typing.cast(typing.Optional["GoogleCertificateManagerCertificateManaged"], jsii.get(self, "managedInput"))

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
    ) -> typing.Optional["GoogleCertificateManagerCertificateSelfManaged"]:
        return typing.cast(typing.Optional["GoogleCertificateManagerCertificateSelfManaged"], jsii.get(self, "selfManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCertificateManagerCertificateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCertificateManagerCertificateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1e5a264704f703911ff8f77e4e640fc8a44008152bff9dd0069e4492533351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039be805be73158d725d68c5a0dad0f087c464bb818e721b2c4fc11874daaa56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1057e843b6677c2f42c77efb0e0b0064eb2a712fc4e653ccaa417d3ec653522b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597245701ddc3d67e17725d236e39f63e4c1bb9aba13c3f82e0710d3da925abc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bba126e1a0317e9775ae0f92c34c3b7e4b2b4b9ab20b1c17e9619782b0842e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467926ebfdcd7e065f4ca548d5ff6b1eff6312361eeeb415d65276f4e6dad688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996485592592d78b240eb002166a2de7243e0bd008fcc5d4334dad297646137d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateConfig",
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
class GoogleCertificateManagerCertificateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        managed: typing.Optional[typing.Union["GoogleCertificateManagerCertificateManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        self_managed: typing.Optional[typing.Union["GoogleCertificateManagerCertificateSelfManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCertificateManagerCertificateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: A user-defined name of the certificate. Certificate names must be unique The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#name GoogleCertificateManagerCertificate#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#description GoogleCertificateManagerCertificate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#id GoogleCertificateManagerCertificate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the Certificate resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#labels GoogleCertificateManagerCertificate#labels}
        :param location: The Certificate Manager location. If not specified, "global" is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#location GoogleCertificateManagerCertificate#location}
        :param managed: managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#managed GoogleCertificateManagerCertificate#managed}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#project GoogleCertificateManagerCertificate#project}.
        :param scope: The scope of the certificate. DEFAULT: Certificates with default scope are served from core Google data centers. If unsure, choose this option. EDGE_CACHE: Certificates with scope EDGE_CACHE are special-purposed certificates, served from Edge Points of Presence. See https://cloud.google.com/vpc/docs/edge-locations. ALL_REGIONS: Certificates with ALL_REGIONS scope are served from all GCP regions (You can only use ALL_REGIONS with global certs). See https://cloud.google.com/compute/docs/regions-zones. CLIENT_AUTH: Certificates with CLIENT_AUTH scope are used by a load balancer (TLS client) to be presented to the backend (TLS server) when backend mTLS is configured. See https://cloud.google.com/load-balancing/docs/backend-authenticated-tls-backend-mtls#client-certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#scope GoogleCertificateManagerCertificate#scope}
        :param self_managed: self_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#self_managed GoogleCertificateManagerCertificate#self_managed}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#timeouts GoogleCertificateManagerCertificate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(managed, dict):
            managed = GoogleCertificateManagerCertificateManaged(**managed)
        if isinstance(self_managed, dict):
            self_managed = GoogleCertificateManagerCertificateSelfManaged(**self_managed)
        if isinstance(timeouts, dict):
            timeouts = GoogleCertificateManagerCertificateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8a8cb294083f934e045eadd14adb23a1b7c014ed0194f0d7de857098a03ecb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#name GoogleCertificateManagerCertificate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#description GoogleCertificateManagerCertificate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#id GoogleCertificateManagerCertificate#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#labels GoogleCertificateManagerCertificate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The Certificate Manager location. If not specified, "global" is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#location GoogleCertificateManagerCertificate#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed(self) -> typing.Optional["GoogleCertificateManagerCertificateManaged"]:
        '''managed block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#managed GoogleCertificateManagerCertificate#managed}
        '''
        result = self._values.get("managed")
        return typing.cast(typing.Optional["GoogleCertificateManagerCertificateManaged"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#project GoogleCertificateManagerCertificate#project}.'''
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#scope GoogleCertificateManagerCertificate#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def self_managed(
        self,
    ) -> typing.Optional["GoogleCertificateManagerCertificateSelfManaged"]:
        '''self_managed block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#self_managed GoogleCertificateManagerCertificate#self_managed}
        '''
        result = self._values.get("self_managed")
        return typing.cast(typing.Optional["GoogleCertificateManagerCertificateSelfManaged"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleCertificateManagerCertificateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#timeouts GoogleCertificateManagerCertificate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCertificateManagerCertificateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateManaged",
    jsii_struct_bases=[],
    name_mapping={
        "dns_authorizations": "dnsAuthorizations",
        "domains": "domains",
        "issuance_config": "issuanceConfig",
    },
)
class GoogleCertificateManagerCertificateManaged:
    def __init__(
        self,
        *,
        dns_authorizations: typing.Optional[typing.Sequence[builtins.str]] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        issuance_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dns_authorizations: Authorizations that will be used for performing domain authorization. Either issuanceConfig or dnsAuthorizations should be specificed, but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#dns_authorizations GoogleCertificateManagerCertificate#dns_authorizations}
        :param domains: The domains for which a managed SSL certificate will be generated. Wildcard domains are only supported with DNS challenge resolution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#domains GoogleCertificateManagerCertificate#domains}
        :param issuance_config: The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/* /locations/* /certificateIssuanceConfigs/*. If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa. Either issuanceConfig or dnsAuthorizations should be specificed, but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#issuance_config GoogleCertificateManagerCertificate#issuance_config} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f23cfce9ecf703912bdcd6acde3fa5bf0d9c2664884ce49a269ad9537cd722)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#dns_authorizations GoogleCertificateManagerCertificate#dns_authorizations}
        '''
        result = self._values.get("dns_authorizations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The domains for which a managed SSL certificate will be generated. Wildcard domains are only supported with DNS challenge resolution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#domains GoogleCertificateManagerCertificate#domains}
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def issuance_config(self) -> typing.Optional[builtins.str]:
        '''The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/* /locations/* /certificateIssuanceConfigs/*.

        If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa.
        Either issuanceConfig or dnsAuthorizations should be specificed, but not both.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#issuance_config GoogleCertificateManagerCertificate#issuance_config}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("issuance_config")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateManaged(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc90700cb03c28ec40c6ec9bd1269d8b711b79a391ba26ab88c9203e134d40a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21afc45f048a54058a9c63fdc465809e8ca8e1d7b2540b7b45f7ce8fcfee7143)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81105214d74fa47bbec16d16a8ece79dae20555290f5d398b4e3c5cc4e28f57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f18748492447b95d9e889b011b5f603e547b376a93fde5c43c5cdcf52db276d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95f157a25d6e79545ead15eca061f060c9fa7a51c34e4014c515221852a246f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7590cb6cfd0099e215f2a425ad0769575a38cbb34baeacbf36d5854a5c4255c2)
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
    ) -> typing.Optional[GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfo]:
        return typing.cast(typing.Optional[GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe8c783edba26527189faeb3f46ca6d66972fa159120a25de18538b65030b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCertificateManagerCertificateManagedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateManagedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__383e9fafb59033e6feefc4a27a458542cd976a91b4f7efeedfbce532163ab2d0)
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
    ) -> GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoList:
        return typing.cast(GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoList, jsii.get(self, "authorizationAttemptInfo"))

    @builtins.property
    @jsii.member(jsii_name="provisioningIssue")
    def provisioning_issue(
        self,
    ) -> "GoogleCertificateManagerCertificateManagedProvisioningIssueList":
        return typing.cast("GoogleCertificateManagerCertificateManagedProvisioningIssueList", jsii.get(self, "provisioningIssue"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8e61c3d40c0e5878c3089dfacd9ce54eaeab029f44742c57451201f52d44926f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsAuthorizations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @domains.setter
    def domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3583732a40f232cf90e2eaf8dd9d0c220bbed175cb1ea19af5e8004c2a55f190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuanceConfig")
    def issuance_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuanceConfig"))

    @issuance_config.setter
    def issuance_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48110d8cee08eb32d75cb6ab443bc6fef4b2e967f4b3e9f8163baf7933739e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuanceConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCertificateManagerCertificateManaged]:
        return typing.cast(typing.Optional[GoogleCertificateManagerCertificateManaged], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCertificateManagerCertificateManaged],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6215b53e69fcb1abe8ffbe9300aaa16fe1f64260c4df3eb55c99bd681ac2258f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateManagedProvisioningIssue",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCertificateManagerCertificateManagedProvisioningIssue:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateManagedProvisioningIssue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCertificateManagerCertificateManagedProvisioningIssueList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateManagedProvisioningIssueList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7d632262a5c999b2a3a1b9e16eff0f7cb97f68ec5b84284edf209eacce1cddd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCertificateManagerCertificateManagedProvisioningIssueOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb6dc5b1e7c650530f34e85ae94aa613194b327c4524cb19d6ab61c7b8697a2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCertificateManagerCertificateManagedProvisioningIssueOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5943a84125bf1ab541c2c3012e0bc7d36b706b5f51a01fbe5cec0b2d52c4f7ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15694debc41fac9ac0dd276b6f4aad85221d51745aae661f4020441e88519b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b59b9fc040ad79f21f3ef414462226295c9902b50129977cc4f4145d1dad865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCertificateManagerCertificateManagedProvisioningIssueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateManagedProvisioningIssueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e21f7d2bda69b702505c082732ffd3e4e96064054e61a4491d783f5459a1eb4)
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
    ) -> typing.Optional[GoogleCertificateManagerCertificateManagedProvisioningIssue]:
        return typing.cast(typing.Optional[GoogleCertificateManagerCertificateManagedProvisioningIssue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCertificateManagerCertificateManagedProvisioningIssue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43bbdc10ee1712726f6c4e08045b4c29eb11afe20daf8269a4639a3f3fa6d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateSelfManaged",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_pem": "certificatePem",
        "pem_certificate": "pemCertificate",
        "pem_private_key": "pemPrivateKey",
        "private_key_pem": "privateKeyPem",
    },
)
class GoogleCertificateManagerCertificateSelfManaged:
    def __init__(
        self,
        *,
        certificate_pem: typing.Optional[builtins.str] = None,
        pem_certificate: typing.Optional[builtins.str] = None,
        pem_private_key: typing.Optional[builtins.str] = None,
        private_key_pem: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param certificate_pem: The certificate chain in PEM-encoded form. Leaf certificate comes first, followed by intermediate ones if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#certificate_pem GoogleCertificateManagerCertificate#certificate_pem}
        :param pem_certificate: The certificate chain in PEM-encoded form. Leaf certificate comes first, followed by intermediate ones if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#pem_certificate GoogleCertificateManagerCertificate#pem_certificate}
        :param pem_private_key: The private key of the leaf certificate in PEM-encoded form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#pem_private_key GoogleCertificateManagerCertificate#pem_private_key}
        :param private_key_pem: The private key of the leaf certificate in PEM-encoded form. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#private_key_pem GoogleCertificateManagerCertificate#private_key_pem}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc8822ab87d210d8ac454e2cd07efd1c0f7409c6559948e3740225d99105a5d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#certificate_pem GoogleCertificateManagerCertificate#certificate_pem}
        '''
        result = self._values.get("certificate_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_certificate(self) -> typing.Optional[builtins.str]:
        '''The certificate chain in PEM-encoded form.

        Leaf certificate comes first, followed by intermediate ones if any.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#pem_certificate GoogleCertificateManagerCertificate#pem_certificate}
        '''
        result = self._values.get("pem_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_private_key(self) -> typing.Optional[builtins.str]:
        '''The private key of the leaf certificate in PEM-encoded form.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#pem_private_key GoogleCertificateManagerCertificate#pem_private_key}
        '''
        result = self._values.get("pem_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_pem(self) -> typing.Optional[builtins.str]:
        '''The private key of the leaf certificate in PEM-encoded form.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#private_key_pem GoogleCertificateManagerCertificate#private_key_pem}
        '''
        result = self._values.get("private_key_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateSelfManaged(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCertificateManagerCertificateSelfManagedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateSelfManagedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56f467206cf5da12fe7accb499457c7dcf318c98209ae2cc5e235262b4449aef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd9bae820b63f04996baec34da6c482f3daeeb5e18617fc5a62f2b388d41243d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificatePem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pemCertificate")
    def pem_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemCertificate"))

    @pem_certificate.setter
    def pem_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2cbe42f9d253c4951f04e006ef0a90da38fc93a0b63c25c2576c48b917b7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pemPrivateKey")
    def pem_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemPrivateKey"))

    @pem_private_key.setter
    def pem_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fccdc0653776b49a9c4a2a267a82d46d4f38ad046ed7f99cc08d07d4ba10c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyPem")
    def private_key_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyPem"))

    @private_key_pem.setter
    def private_key_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b83efd475c0146f42085c180e65d65df0fdcab73c350c3a0b54db89452cfc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCertificateManagerCertificateSelfManaged]:
        return typing.cast(typing.Optional[GoogleCertificateManagerCertificateSelfManaged], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCertificateManagerCertificateSelfManaged],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db9276c96b3daa02655f52464fbade17a60bcaf81a3109f79da4ae618eef57d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCertificateManagerCertificateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#create GoogleCertificateManagerCertificate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#delete GoogleCertificateManagerCertificate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#update GoogleCertificateManagerCertificate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c67eb9a091cf5ebe0dee88f62368e3f99cb955b81adbefa620183224923759)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#create GoogleCertificateManagerCertificate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#delete GoogleCertificateManagerCertificate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_certificate_manager_certificate#update GoogleCertificateManagerCertificate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCertificateManagerCertificateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCertificateManagerCertificateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCertificateManagerCertificate.GoogleCertificateManagerCertificateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e4463f4bbd6cac1b34ddfbe2fdd76b711fd32d2a0bd79690f5df511fec82dac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b28c840957c40b95c6cca1c9365ef05ccfc6f87d1e50a4af1906dff34b5a8f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a25400c0281383cfd94e8e8d8d9e43cc105ec617247038a9e8ea90e67dadef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdc338332bca02a5ceb46a39aaa6a57118b7e1853111ba2739f89c1695d4239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCertificateManagerCertificateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCertificateManagerCertificateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCertificateManagerCertificateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44dd0c0ef1ec72e047fdeb96939d91f82626eabd1f1942d4dbe84338bcac5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCertificateManagerCertificate",
    "GoogleCertificateManagerCertificateConfig",
    "GoogleCertificateManagerCertificateManaged",
    "GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfo",
    "GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoList",
    "GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfoOutputReference",
    "GoogleCertificateManagerCertificateManagedOutputReference",
    "GoogleCertificateManagerCertificateManagedProvisioningIssue",
    "GoogleCertificateManagerCertificateManagedProvisioningIssueList",
    "GoogleCertificateManagerCertificateManagedProvisioningIssueOutputReference",
    "GoogleCertificateManagerCertificateSelfManaged",
    "GoogleCertificateManagerCertificateSelfManagedOutputReference",
    "GoogleCertificateManagerCertificateTimeouts",
    "GoogleCertificateManagerCertificateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c9b2fe7f5876bb6204af9dd4385b578ece493ebb5267ffe8ce49f576ff35f584(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    managed: typing.Optional[typing.Union[GoogleCertificateManagerCertificateManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    self_managed: typing.Optional[typing.Union[GoogleCertificateManagerCertificateSelfManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCertificateManagerCertificateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__97d87f404c0664d86ad10ae3955ad9d504c6a1e012947e4dc74d90a503355e23(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1e5a264704f703911ff8f77e4e640fc8a44008152bff9dd0069e4492533351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039be805be73158d725d68c5a0dad0f087c464bb818e721b2c4fc11874daaa56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1057e843b6677c2f42c77efb0e0b0064eb2a712fc4e653ccaa417d3ec653522b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597245701ddc3d67e17725d236e39f63e4c1bb9aba13c3f82e0710d3da925abc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bba126e1a0317e9775ae0f92c34c3b7e4b2b4b9ab20b1c17e9619782b0842e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467926ebfdcd7e065f4ca548d5ff6b1eff6312361eeeb415d65276f4e6dad688(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996485592592d78b240eb002166a2de7243e0bd008fcc5d4334dad297646137d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8a8cb294083f934e045eadd14adb23a1b7c014ed0194f0d7de857098a03ecb(
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
    managed: typing.Optional[typing.Union[GoogleCertificateManagerCertificateManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    self_managed: typing.Optional[typing.Union[GoogleCertificateManagerCertificateSelfManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCertificateManagerCertificateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f23cfce9ecf703912bdcd6acde3fa5bf0d9c2664884ce49a269ad9537cd722(
    *,
    dns_authorizations: typing.Optional[typing.Sequence[builtins.str]] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    issuance_config: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc90700cb03c28ec40c6ec9bd1269d8b711b79a391ba26ab88c9203e134d40a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21afc45f048a54058a9c63fdc465809e8ca8e1d7b2540b7b45f7ce8fcfee7143(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81105214d74fa47bbec16d16a8ece79dae20555290f5d398b4e3c5cc4e28f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f18748492447b95d9e889b011b5f603e547b376a93fde5c43c5cdcf52db276d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f157a25d6e79545ead15eca061f060c9fa7a51c34e4014c515221852a246f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7590cb6cfd0099e215f2a425ad0769575a38cbb34baeacbf36d5854a5c4255c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe8c783edba26527189faeb3f46ca6d66972fa159120a25de18538b65030b96(
    value: typing.Optional[GoogleCertificateManagerCertificateManagedAuthorizationAttemptInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383e9fafb59033e6feefc4a27a458542cd976a91b4f7efeedfbce532163ab2d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e61c3d40c0e5878c3089dfacd9ce54eaeab029f44742c57451201f52d44926f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3583732a40f232cf90e2eaf8dd9d0c220bbed175cb1ea19af5e8004c2a55f190(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48110d8cee08eb32d75cb6ab443bc6fef4b2e967f4b3e9f8163baf7933739e69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6215b53e69fcb1abe8ffbe9300aaa16fe1f64260c4df3eb55c99bd681ac2258f(
    value: typing.Optional[GoogleCertificateManagerCertificateManaged],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d632262a5c999b2a3a1b9e16eff0f7cb97f68ec5b84284edf209eacce1cddd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb6dc5b1e7c650530f34e85ae94aa613194b327c4524cb19d6ab61c7b8697a2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5943a84125bf1ab541c2c3012e0bc7d36b706b5f51a01fbe5cec0b2d52c4f7ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15694debc41fac9ac0dd276b6f4aad85221d51745aae661f4020441e88519b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b59b9fc040ad79f21f3ef414462226295c9902b50129977cc4f4145d1dad865(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e21f7d2bda69b702505c082732ffd3e4e96064054e61a4491d783f5459a1eb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43bbdc10ee1712726f6c4e08045b4c29eb11afe20daf8269a4639a3f3fa6d0b(
    value: typing.Optional[GoogleCertificateManagerCertificateManagedProvisioningIssue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc8822ab87d210d8ac454e2cd07efd1c0f7409c6559948e3740225d99105a5d(
    *,
    certificate_pem: typing.Optional[builtins.str] = None,
    pem_certificate: typing.Optional[builtins.str] = None,
    pem_private_key: typing.Optional[builtins.str] = None,
    private_key_pem: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f467206cf5da12fe7accb499457c7dcf318c98209ae2cc5e235262b4449aef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9bae820b63f04996baec34da6c482f3daeeb5e18617fc5a62f2b388d41243d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2cbe42f9d253c4951f04e006ef0a90da38fc93a0b63c25c2576c48b917b7cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fccdc0653776b49a9c4a2a267a82d46d4f38ad046ed7f99cc08d07d4ba10c22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b83efd475c0146f42085c180e65d65df0fdcab73c350c3a0b54db89452cfc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db9276c96b3daa02655f52464fbade17a60bcaf81a3109f79da4ae618eef57d(
    value: typing.Optional[GoogleCertificateManagerCertificateSelfManaged],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c67eb9a091cf5ebe0dee88f62368e3f99cb955b81adbefa620183224923759(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4463f4bbd6cac1b34ddfbe2fdd76b711fd32d2a0bd79690f5df511fec82dac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b28c840957c40b95c6cca1c9365ef05ccfc6f87d1e50a4af1906dff34b5a8f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a25400c0281383cfd94e8e8d8d9e43cc105ec617247038a9e8ea90e67dadef4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdc338332bca02a5ceb46a39aaa6a57118b7e1853111ba2739f89c1695d4239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44dd0c0ef1ec72e047fdeb96939d91f82626eabd1f1942d4dbe84338bcac5c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCertificateManagerCertificateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
