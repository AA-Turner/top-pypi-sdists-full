r'''
# `google_active_directory_domain_trust`

Refer to the Terraform Registry for docs: [`google_active_directory_domain_trust`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust).
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


class ActiveDirectoryDomainTrust(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.activeDirectoryDomainTrust.ActiveDirectoryDomainTrust",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust google_active_directory_domain_trust}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain: builtins.str,
        target_dns_ip_addresses: typing.Sequence[builtins.str],
        target_domain_name: builtins.str,
        trust_direction: builtins.str,
        trust_handshake_secret: builtins.str,
        trust_type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        selective_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ActiveDirectoryDomainTrustTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust google_active_directory_domain_trust} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain: The fully qualified domain name. e.g. mydomain.myorganization.com, with the restrictions of https://cloud.google.com/managed-microsoft-ad/reference/rest/v1/projects.locations.global.domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#domain ActiveDirectoryDomainTrust#domain}
        :param target_dns_ip_addresses: The target DNS server IP addresses which can resolve the remote domain involved in the trust. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#target_dns_ip_addresses ActiveDirectoryDomainTrust#target_dns_ip_addresses}
        :param target_domain_name: The fully qualified target domain name which will be in trust with the current domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#target_domain_name ActiveDirectoryDomainTrust#target_domain_name}
        :param trust_direction: The trust direction, which decides if the current domain is trusted, trusting, or both. Possible values: ["INBOUND", "OUTBOUND", "BIDIRECTIONAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#trust_direction ActiveDirectoryDomainTrust#trust_direction}
        :param trust_handshake_secret: The trust secret used for the handshake with the target domain. This will not be stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#trust_handshake_secret ActiveDirectoryDomainTrust#trust_handshake_secret}
        :param trust_type: The type of trust represented by the trust resource. Possible values: ["FOREST", "EXTERNAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#trust_type ActiveDirectoryDomainTrust#trust_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#id ActiveDirectoryDomainTrust#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#project ActiveDirectoryDomainTrust#project}.
        :param selective_authentication: Whether the trusted side has forest/domain wide access or selective access to an approved set of resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#selective_authentication ActiveDirectoryDomainTrust#selective_authentication}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#timeouts ActiveDirectoryDomainTrust#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd5dfbf43f005f2a114788109770490458adaafdf7a4bc0a275fe6691b0b69a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ActiveDirectoryDomainTrustConfig(
            domain=domain,
            target_dns_ip_addresses=target_dns_ip_addresses,
            target_domain_name=target_domain_name,
            trust_direction=trust_direction,
            trust_handshake_secret=trust_handshake_secret,
            trust_type=trust_type,
            id=id,
            project=project,
            selective_authentication=selective_authentication,
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
        '''Generates CDKTF code for importing a ActiveDirectoryDomainTrust resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ActiveDirectoryDomainTrust to import.
        :param import_from_id: The id of the existing ActiveDirectoryDomainTrust that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ActiveDirectoryDomainTrust to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b18037e742ae696ca920a29c60f98cedfd145a93ec5672ead3bc3b91f0f771)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#create ActiveDirectoryDomainTrust#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#delete ActiveDirectoryDomainTrust#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#update ActiveDirectoryDomainTrust#update}.
        '''
        value = ActiveDirectoryDomainTrustTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSelectiveAuthentication")
    def reset_selective_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectiveAuthentication", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ActiveDirectoryDomainTrustTimeoutsOutputReference":
        return typing.cast("ActiveDirectoryDomainTrustTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="selectiveAuthenticationInput")
    def selective_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "selectiveAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDnsIpAddressesInput")
    def target_dns_ip_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetDnsIpAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDomainNameInput")
    def target_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ActiveDirectoryDomainTrustTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ActiveDirectoryDomainTrustTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustDirectionInput")
    def trust_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="trustHandshakeSecretInput")
    def trust_handshake_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustHandshakeSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="trustTypeInput")
    def trust_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af335aeb95eb13fb833c3cc02e8b62487308724e49b4b773540a782b0c0c21b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb8bcf4186c58a4eb91abf809f81887e2b57e1150459acc10c912ec0c313649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea532660f4ba9426bf5d0103d0de5badf05fc0f8eaf45d30b85817649552e81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selectiveAuthentication")
    def selective_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "selectiveAuthentication"))

    @selective_authentication.setter
    def selective_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa843c4c16b990e0075f66363a271f8811f6d68bb9b553fadf7d7ed2bd296dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectiveAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDnsIpAddresses")
    def target_dns_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetDnsIpAddresses"))

    @target_dns_ip_addresses.setter
    def target_dns_ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fc97ebdaa8b364e2a1e9c70f5447e833f439d08974c896b7449cfaef7a4401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDnsIpAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDomainName")
    def target_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDomainName"))

    @target_domain_name.setter
    def target_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8398578cc9559a7353b2404b275041551b4c16ccc4663b83faac6a23dc90665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustDirection")
    def trust_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustDirection"))

    @trust_direction.setter
    def trust_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78850eb43e897bbd1f611cdc0ab935f4ad7aa8d2c5a4a461eb0511d230ef7e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustDirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustHandshakeSecret")
    def trust_handshake_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustHandshakeSecret"))

    @trust_handshake_secret.setter
    def trust_handshake_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ef57d7d61f2abb054c77083c5a3cd7194c0a09869d5d7fde7d370f25f859ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustHandshakeSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustType")
    def trust_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustType"))

    @trust_type.setter
    def trust_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec395a5ba1e547aa833ed4e344a16a08da06fd56b7fac2acafaa92d5b6b977b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.activeDirectoryDomainTrust.ActiveDirectoryDomainTrustConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "domain": "domain",
        "target_dns_ip_addresses": "targetDnsIpAddresses",
        "target_domain_name": "targetDomainName",
        "trust_direction": "trustDirection",
        "trust_handshake_secret": "trustHandshakeSecret",
        "trust_type": "trustType",
        "id": "id",
        "project": "project",
        "selective_authentication": "selectiveAuthentication",
        "timeouts": "timeouts",
    },
)
class ActiveDirectoryDomainTrustConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        domain: builtins.str,
        target_dns_ip_addresses: typing.Sequence[builtins.str],
        target_domain_name: builtins.str,
        trust_direction: builtins.str,
        trust_handshake_secret: builtins.str,
        trust_type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        selective_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ActiveDirectoryDomainTrustTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param domain: The fully qualified domain name. e.g. mydomain.myorganization.com, with the restrictions of https://cloud.google.com/managed-microsoft-ad/reference/rest/v1/projects.locations.global.domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#domain ActiveDirectoryDomainTrust#domain}
        :param target_dns_ip_addresses: The target DNS server IP addresses which can resolve the remote domain involved in the trust. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#target_dns_ip_addresses ActiveDirectoryDomainTrust#target_dns_ip_addresses}
        :param target_domain_name: The fully qualified target domain name which will be in trust with the current domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#target_domain_name ActiveDirectoryDomainTrust#target_domain_name}
        :param trust_direction: The trust direction, which decides if the current domain is trusted, trusting, or both. Possible values: ["INBOUND", "OUTBOUND", "BIDIRECTIONAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#trust_direction ActiveDirectoryDomainTrust#trust_direction}
        :param trust_handshake_secret: The trust secret used for the handshake with the target domain. This will not be stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#trust_handshake_secret ActiveDirectoryDomainTrust#trust_handshake_secret}
        :param trust_type: The type of trust represented by the trust resource. Possible values: ["FOREST", "EXTERNAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#trust_type ActiveDirectoryDomainTrust#trust_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#id ActiveDirectoryDomainTrust#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#project ActiveDirectoryDomainTrust#project}.
        :param selective_authentication: Whether the trusted side has forest/domain wide access or selective access to an approved set of resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#selective_authentication ActiveDirectoryDomainTrust#selective_authentication}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#timeouts ActiveDirectoryDomainTrust#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ActiveDirectoryDomainTrustTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b1fd130bdfe39407437ca616980baa0f9aa7145d496d9083800ba9fcd68530)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument target_dns_ip_addresses", value=target_dns_ip_addresses, expected_type=type_hints["target_dns_ip_addresses"])
            check_type(argname="argument target_domain_name", value=target_domain_name, expected_type=type_hints["target_domain_name"])
            check_type(argname="argument trust_direction", value=trust_direction, expected_type=type_hints["trust_direction"])
            check_type(argname="argument trust_handshake_secret", value=trust_handshake_secret, expected_type=type_hints["trust_handshake_secret"])
            check_type(argname="argument trust_type", value=trust_type, expected_type=type_hints["trust_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument selective_authentication", value=selective_authentication, expected_type=type_hints["selective_authentication"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
            "target_dns_ip_addresses": target_dns_ip_addresses,
            "target_domain_name": target_domain_name,
            "trust_direction": trust_direction,
            "trust_handshake_secret": trust_handshake_secret,
            "trust_type": trust_type,
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
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if selective_authentication is not None:
            self._values["selective_authentication"] = selective_authentication
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
    def domain(self) -> builtins.str:
        '''The fully qualified domain name. e.g. mydomain.myorganization.com, with the restrictions of https://cloud.google.com/managed-microsoft-ad/reference/rest/v1/projects.locations.global.domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#domain ActiveDirectoryDomainTrust#domain}
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_dns_ip_addresses(self) -> typing.List[builtins.str]:
        '''The target DNS server IP addresses which can resolve the remote domain involved in the trust.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#target_dns_ip_addresses ActiveDirectoryDomainTrust#target_dns_ip_addresses}
        '''
        result = self._values.get("target_dns_ip_addresses")
        assert result is not None, "Required property 'target_dns_ip_addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target_domain_name(self) -> builtins.str:
        '''The fully qualified target domain name which will be in trust with the current domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#target_domain_name ActiveDirectoryDomainTrust#target_domain_name}
        '''
        result = self._values.get("target_domain_name")
        assert result is not None, "Required property 'target_domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trust_direction(self) -> builtins.str:
        '''The trust direction, which decides if the current domain is trusted, trusting, or both. Possible values: ["INBOUND", "OUTBOUND", "BIDIRECTIONAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#trust_direction ActiveDirectoryDomainTrust#trust_direction}
        '''
        result = self._values.get("trust_direction")
        assert result is not None, "Required property 'trust_direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trust_handshake_secret(self) -> builtins.str:
        '''The trust secret used for the handshake with the target domain. This will not be stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#trust_handshake_secret ActiveDirectoryDomainTrust#trust_handshake_secret}
        '''
        result = self._values.get("trust_handshake_secret")
        assert result is not None, "Required property 'trust_handshake_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trust_type(self) -> builtins.str:
        '''The type of trust represented by the trust resource. Possible values: ["FOREST", "EXTERNAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#trust_type ActiveDirectoryDomainTrust#trust_type}
        '''
        result = self._values.get("trust_type")
        assert result is not None, "Required property 'trust_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#id ActiveDirectoryDomainTrust#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#project ActiveDirectoryDomainTrust#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def selective_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the trusted side has forest/domain wide access or selective access to an approved set of resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#selective_authentication ActiveDirectoryDomainTrust#selective_authentication}
        '''
        result = self._values.get("selective_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ActiveDirectoryDomainTrustTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#timeouts ActiveDirectoryDomainTrust#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ActiveDirectoryDomainTrustTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActiveDirectoryDomainTrustConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.activeDirectoryDomainTrust.ActiveDirectoryDomainTrustTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ActiveDirectoryDomainTrustTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#create ActiveDirectoryDomainTrust#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#delete ActiveDirectoryDomainTrust#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#update ActiveDirectoryDomainTrust#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdb24b9403e444195442621a7a2dae866890b0d6c63a5a1779669c873cb5fd0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#create ActiveDirectoryDomainTrust#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#delete ActiveDirectoryDomainTrust#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/active_directory_domain_trust#update ActiveDirectoryDomainTrust#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActiveDirectoryDomainTrustTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActiveDirectoryDomainTrustTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.activeDirectoryDomainTrust.ActiveDirectoryDomainTrustTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__426fc943fccc17d042fd875c1e183431d6b66e4b5382b78306cfde7de669ff8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fcb689ef0fdd2111492174a5e85891c6fb2597fd49911f0f335ed44ea297c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ca1c92abcd94ac80fa04a492201cdd961c37dbaa7793e9fc151c95479c4dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee8e488323e727d30ef583745357589af74c79e46f15bcdf0611145899cf580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActiveDirectoryDomainTrustTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActiveDirectoryDomainTrustTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActiveDirectoryDomainTrustTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ff448e25dba0059699417f0315c954090eeb33c8d4923ef514778f8984af70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ActiveDirectoryDomainTrust",
    "ActiveDirectoryDomainTrustConfig",
    "ActiveDirectoryDomainTrustTimeouts",
    "ActiveDirectoryDomainTrustTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0cd5dfbf43f005f2a114788109770490458adaafdf7a4bc0a275fe6691b0b69a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain: builtins.str,
    target_dns_ip_addresses: typing.Sequence[builtins.str],
    target_domain_name: builtins.str,
    trust_direction: builtins.str,
    trust_handshake_secret: builtins.str,
    trust_type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    selective_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ActiveDirectoryDomainTrustTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__36b18037e742ae696ca920a29c60f98cedfd145a93ec5672ead3bc3b91f0f771(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af335aeb95eb13fb833c3cc02e8b62487308724e49b4b773540a782b0c0c21b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb8bcf4186c58a4eb91abf809f81887e2b57e1150459acc10c912ec0c313649(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea532660f4ba9426bf5d0103d0de5badf05fc0f8eaf45d30b85817649552e81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa843c4c16b990e0075f66363a271f8811f6d68bb9b553fadf7d7ed2bd296dc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fc97ebdaa8b364e2a1e9c70f5447e833f439d08974c896b7449cfaef7a4401(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8398578cc9559a7353b2404b275041551b4c16ccc4663b83faac6a23dc90665(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78850eb43e897bbd1f611cdc0ab935f4ad7aa8d2c5a4a461eb0511d230ef7e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ef57d7d61f2abb054c77083c5a3cd7194c0a09869d5d7fde7d370f25f859ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec395a5ba1e547aa833ed4e344a16a08da06fd56b7fac2acafaa92d5b6b977b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b1fd130bdfe39407437ca616980baa0f9aa7145d496d9083800ba9fcd68530(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain: builtins.str,
    target_dns_ip_addresses: typing.Sequence[builtins.str],
    target_domain_name: builtins.str,
    trust_direction: builtins.str,
    trust_handshake_secret: builtins.str,
    trust_type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    selective_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ActiveDirectoryDomainTrustTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdb24b9403e444195442621a7a2dae866890b0d6c63a5a1779669c873cb5fd0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426fc943fccc17d042fd875c1e183431d6b66e4b5382b78306cfde7de669ff8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcb689ef0fdd2111492174a5e85891c6fb2597fd49911f0f335ed44ea297c64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ca1c92abcd94ac80fa04a492201cdd961c37dbaa7793e9fc151c95479c4dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee8e488323e727d30ef583745357589af74c79e46f15bcdf0611145899cf580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ff448e25dba0059699417f0315c954090eeb33c8d4923ef514778f8984af70(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActiveDirectoryDomainTrustTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
