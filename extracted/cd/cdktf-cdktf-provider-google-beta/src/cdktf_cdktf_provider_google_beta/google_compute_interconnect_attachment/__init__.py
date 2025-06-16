r'''
# `google_compute_interconnect_attachment`

Refer to the Terraform Registry for docs: [`google_compute_interconnect_attachment`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment).
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


class GoogleComputeInterconnectAttachment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnectAttachment.GoogleComputeInterconnectAttachment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment google_compute_interconnect_attachment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        router: builtins.str,
        admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bandwidth: typing.Optional[builtins.str] = None,
        candidate_cloud_router_ip_address: typing.Optional[builtins.str] = None,
        candidate_cloud_router_ipv6_address: typing.Optional[builtins.str] = None,
        candidate_customer_router_ip_address: typing.Optional[builtins.str] = None,
        candidate_customer_router_ipv6_address: typing.Optional[builtins.str] = None,
        candidate_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_availability_domain: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect: typing.Optional[builtins.str] = None,
        ipsec_internal_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mtu: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        stack_type: typing.Optional[builtins.str] = None,
        subnet_length: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeInterconnectAttachmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        vlan_tag8021_q: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment google_compute_interconnect_attachment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#name GoogleComputeInterconnectAttachment#name}
        :param router: URL of the cloud router to be used for dynamic routing. This router must be in the same region as this InterconnectAttachment. The InterconnectAttachment will automatically connect the Interconnect to the network & region within which the Cloud Router is configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#router GoogleComputeInterconnectAttachment#router}
        :param admin_enabled: Whether the VLAN attachment is enabled or disabled. When using PARTNER type this will Pre-Activate the interconnect attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#admin_enabled GoogleComputeInterconnectAttachment#admin_enabled}
        :param bandwidth: Provisioned bandwidth capacity for the interconnect attachment. For attachments of type DEDICATED, the user can set the bandwidth. For attachments of type PARTNER, the Google Partner that is operating the interconnect must set the bandwidth. Output only for PARTNER type, mutable for PARTNER_PROVIDER and DEDICATED, Defaults to BPS_10G Possible values: ["BPS_50M", "BPS_100M", "BPS_200M", "BPS_300M", "BPS_400M", "BPS_500M", "BPS_1G", "BPS_2G", "BPS_5G", "BPS_10G", "BPS_20G", "BPS_50G", "BPS_100G"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#bandwidth GoogleComputeInterconnectAttachment#bandwidth}
        :param candidate_cloud_router_ip_address: Single IPv4 address + prefix length to be configured on the cloud router interface for this interconnect attachment. Example: 203.0.113.1/29. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_cloud_router_ip_address GoogleComputeInterconnectAttachment#candidate_cloud_router_ip_address}
        :param candidate_cloud_router_ipv6_address: Single IPv6 address + prefix length to be configured on the cloud router interface for this interconnect attachment. Example: 2001:db8::1/125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_cloud_router_ipv6_address GoogleComputeInterconnectAttachment#candidate_cloud_router_ipv6_address}
        :param candidate_customer_router_ip_address: Single IPv4 address + prefix length to be configured on the customer router interface for this interconnect attachment. Example: 203.0.113.2/29. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_customer_router_ip_address GoogleComputeInterconnectAttachment#candidate_customer_router_ip_address}
        :param candidate_customer_router_ipv6_address: Single IPv6 address + prefix length to be configured on the customer router interface for this interconnect attachment. Example: 2001:db8::2/125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_customer_router_ipv6_address GoogleComputeInterconnectAttachment#candidate_customer_router_ipv6_address}
        :param candidate_subnets: Up to 16 candidate prefixes that can be used to restrict the allocation of cloudRouterIpAddress and customerRouterIpAddress for this attachment. All prefixes must be within link-local address space (169.254.0.0/16) and must be /29 or shorter (/28, /27, etc). Google will attempt to select an unused /29 from the supplied candidate prefix(es). The request will fail if all possible /29s are in use on Google's edge. If not supplied, Google will randomly select an unused /29 from all of link-local space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_subnets GoogleComputeInterconnectAttachment#candidate_subnets}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#description GoogleComputeInterconnectAttachment#description}
        :param edge_availability_domain: Desired availability domain for the attachment. Only available for type PARTNER, at creation time. For improved reliability, customers should configure a pair of attachments with one per availability domain. The selected availability domain will be provided to the Partner via the pairing key so that the provisioned circuit will lie in the specified domain. If not specified, the value will default to AVAILABILITY_DOMAIN_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#edge_availability_domain GoogleComputeInterconnectAttachment#edge_availability_domain}
        :param encryption: Indicates the user-supplied encryption option of this interconnect attachment. Can only be specified at attachment creation for PARTNER or DEDICATED attachments. - NONE - This is the default value, which means that the VLAN attachment carries unencrypted traffic. VMs are able to send traffic to, or receive traffic from, such a VLAN attachment. - IPSEC - The VLAN attachment carries only encrypted traffic that is encrypted by an IPsec device, such as an HA VPN gateway or third-party IPsec VPN. VMs cannot directly send traffic to, or receive traffic from, such a VLAN attachment. To use HA VPN over Cloud Interconnect, the VLAN attachment must be created with this option. Default value: "NONE" Possible values: ["NONE", "IPSEC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#encryption GoogleComputeInterconnectAttachment#encryption}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#id GoogleComputeInterconnectAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect: URL of the underlying Interconnect object that this attachment's traffic will traverse through. Required if type is DEDICATED, must not be set if type is PARTNER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#interconnect GoogleComputeInterconnectAttachment#interconnect}
        :param ipsec_internal_addresses: URL of addresses that have been reserved for the interconnect attachment, Used only for interconnect attachment that has the encryption option as IPSEC. The addresses must be RFC 1918 IP address ranges. When creating HA VPN gateway over the interconnect attachment, if the attachment is configured to use an RFC 1918 IP address, then the VPN gateway's IP address will be allocated from the IP address range specified here. For example, if the HA VPN gateway's interface 0 is paired to this interconnect attachment, then an RFC 1918 IP address for the VPN gateway interface 0 will be allocated from the IP address specified for this interconnect attachment. If this field is not specified for interconnect attachment that has encryption option as IPSEC, later on when creating HA VPN gateway on this interconnect attachment, the HA VPN gateway's IP address will be allocated from regional external IP address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#ipsec_internal_addresses GoogleComputeInterconnectAttachment#ipsec_internal_addresses}
        :param labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#labels GoogleComputeInterconnectAttachment#labels}
        :param mtu: Maximum Transmission Unit (MTU), in bytes, of packets passing through this interconnect attachment. Valid values are 1440, 1460, 1500, and 8896. If not specified, the value will default to 1440. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#mtu GoogleComputeInterconnectAttachment#mtu}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#project GoogleComputeInterconnectAttachment#project}.
        :param region: Region where the regional interconnect attachment resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#region GoogleComputeInterconnectAttachment#region}
        :param stack_type: The stack type for this interconnect attachment to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. This field can be both set at interconnect attachments creation and update interconnect attachment operations. Possible values: ["IPV4_IPV6", "IPV4_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#stack_type GoogleComputeInterconnectAttachment#stack_type}
        :param subnet_length: Length of the IPv4 subnet mask. Allowed values: 29 (default), 30. The default value is 29, except for Cross-Cloud Interconnect connections that use an InterconnectRemoteLocation with a constraints.subnetLengthRange.min equal to 30. For example, connections that use an Azure remote location fall into this category. In these cases, the default value is 30, and requesting 29 returns an error. Where both 29 and 30 are allowed, 29 is preferred, because it gives Google Cloud Support more debugging visibility. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#subnet_length GoogleComputeInterconnectAttachment#subnet_length}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#timeouts GoogleComputeInterconnectAttachment#timeouts}
        :param type: The type of InterconnectAttachment you wish to create. Defaults to DEDICATED. Possible values: ["DEDICATED", "PARTNER", "PARTNER_PROVIDER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#type GoogleComputeInterconnectAttachment#type}
        :param vlan_tag8021_q: The IEEE 802.1Q VLAN tag for this attachment, in the range 2-4094. When using PARTNER type this will be managed upstream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#vlan_tag8021q GoogleComputeInterconnectAttachment#vlan_tag8021q}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39774e0a138de5b8012a3bbcf6c0b1af85b0cbd3d0706a218291aec40041dae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeInterconnectAttachmentConfig(
            name=name,
            router=router,
            admin_enabled=admin_enabled,
            bandwidth=bandwidth,
            candidate_cloud_router_ip_address=candidate_cloud_router_ip_address,
            candidate_cloud_router_ipv6_address=candidate_cloud_router_ipv6_address,
            candidate_customer_router_ip_address=candidate_customer_router_ip_address,
            candidate_customer_router_ipv6_address=candidate_customer_router_ipv6_address,
            candidate_subnets=candidate_subnets,
            description=description,
            edge_availability_domain=edge_availability_domain,
            encryption=encryption,
            id=id,
            interconnect=interconnect,
            ipsec_internal_addresses=ipsec_internal_addresses,
            labels=labels,
            mtu=mtu,
            project=project,
            region=region,
            stack_type=stack_type,
            subnet_length=subnet_length,
            timeouts=timeouts,
            type=type,
            vlan_tag8021_q=vlan_tag8021_q,
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
        '''Generates CDKTF code for importing a GoogleComputeInterconnectAttachment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeInterconnectAttachment to import.
        :param import_from_id: The id of the existing GoogleComputeInterconnectAttachment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeInterconnectAttachment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc489dfab38c7f7dccd7e16f87056d403bdbd680ae2e80a1cb8e62de4668593)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#create GoogleComputeInterconnectAttachment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#delete GoogleComputeInterconnectAttachment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#update GoogleComputeInterconnectAttachment#update}.
        '''
        value = GoogleComputeInterconnectAttachmentTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminEnabled")
    def reset_admin_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminEnabled", []))

    @jsii.member(jsii_name="resetBandwidth")
    def reset_bandwidth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidth", []))

    @jsii.member(jsii_name="resetCandidateCloudRouterIpAddress")
    def reset_candidate_cloud_router_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCandidateCloudRouterIpAddress", []))

    @jsii.member(jsii_name="resetCandidateCloudRouterIpv6Address")
    def reset_candidate_cloud_router_ipv6_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCandidateCloudRouterIpv6Address", []))

    @jsii.member(jsii_name="resetCandidateCustomerRouterIpAddress")
    def reset_candidate_customer_router_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCandidateCustomerRouterIpAddress", []))

    @jsii.member(jsii_name="resetCandidateCustomerRouterIpv6Address")
    def reset_candidate_customer_router_ipv6_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCandidateCustomerRouterIpv6Address", []))

    @jsii.member(jsii_name="resetCandidateSubnets")
    def reset_candidate_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCandidateSubnets", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEdgeAvailabilityDomain")
    def reset_edge_availability_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeAvailabilityDomain", []))

    @jsii.member(jsii_name="resetEncryption")
    def reset_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryption", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInterconnect")
    def reset_interconnect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterconnect", []))

    @jsii.member(jsii_name="resetIpsecInternalAddresses")
    def reset_ipsec_internal_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpsecInternalAddresses", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMtu")
    def reset_mtu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMtu", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetStackType")
    def reset_stack_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStackType", []))

    @jsii.member(jsii_name="resetSubnetLength")
    def reset_subnet_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetLength", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVlanTag8021Q")
    def reset_vlan_tag8021_q(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVlanTag8021Q", []))

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
    @jsii.member(jsii_name="attachmentGroup")
    def attachment_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attachmentGroup"))

    @builtins.property
    @jsii.member(jsii_name="cloudRouterIpAddress")
    def cloud_router_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudRouterIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="cloudRouterIpv6Address")
    def cloud_router_ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudRouterIpv6Address"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="customerRouterIpAddress")
    def customer_router_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerRouterIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="customerRouterIpv6Address")
    def customer_router_ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerRouterIpv6Address"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="googleReferenceId")
    def google_reference_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleReferenceId"))

    @builtins.property
    @jsii.member(jsii_name="labelFingerprint")
    def label_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="pairingKey")
    def pairing_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pairingKey"))

    @builtins.property
    @jsii.member(jsii_name="partnerAsn")
    def partner_asn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partnerAsn"))

    @builtins.property
    @jsii.member(jsii_name="privateInterconnectInfo")
    def private_interconnect_info(
        self,
    ) -> "GoogleComputeInterconnectAttachmentPrivateInterconnectInfoList":
        return typing.cast("GoogleComputeInterconnectAttachmentPrivateInterconnectInfoList", jsii.get(self, "privateInterconnectInfo"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeInterconnectAttachmentTimeoutsOutputReference":
        return typing.cast("GoogleComputeInterconnectAttachmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="adminEnabledInput")
    def admin_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthInput")
    def bandwidth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthInput"))

    @builtins.property
    @jsii.member(jsii_name="candidateCloudRouterIpAddressInput")
    def candidate_cloud_router_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "candidateCloudRouterIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="candidateCloudRouterIpv6AddressInput")
    def candidate_cloud_router_ipv6_address_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "candidateCloudRouterIpv6AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="candidateCustomerRouterIpAddressInput")
    def candidate_customer_router_ip_address_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "candidateCustomerRouterIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="candidateCustomerRouterIpv6AddressInput")
    def candidate_customer_router_ipv6_address_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "candidateCustomerRouterIpv6AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="candidateSubnetsInput")
    def candidate_subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "candidateSubnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeAvailabilityDomainInput")
    def edge_availability_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeAvailabilityDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInput")
    def encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interconnectInput")
    def interconnect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interconnectInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsecInternalAddressesInput")
    def ipsec_internal_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipsecInternalAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="mtuInput")
    def mtu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mtuInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="routerInput")
    def router_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerInput"))

    @builtins.property
    @jsii.member(jsii_name="stackTypeInput")
    def stack_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetLengthInput")
    def subnet_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "subnetLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeInterconnectAttachmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeInterconnectAttachmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vlanTag8021QInput")
    def vlan_tag8021_q_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vlanTag8021QInput"))

    @builtins.property
    @jsii.member(jsii_name="adminEnabled")
    def admin_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminEnabled"))

    @admin_enabled.setter
    def admin_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fb23c7d4a9a04aba88c57a3dcd78f440a466df76b5e1c035f8606810094b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidth"))

    @bandwidth.setter
    def bandwidth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebde522462ca2e0cb74cb27375a5298620da5659bdd75dc6991baad37b348b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="candidateCloudRouterIpAddress")
    def candidate_cloud_router_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "candidateCloudRouterIpAddress"))

    @candidate_cloud_router_ip_address.setter
    def candidate_cloud_router_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f855e4d7b7d59945c21145bfecb72fd909bade7e490adfbca6d8429ebd3db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "candidateCloudRouterIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="candidateCloudRouterIpv6Address")
    def candidate_cloud_router_ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "candidateCloudRouterIpv6Address"))

    @candidate_cloud_router_ipv6_address.setter
    def candidate_cloud_router_ipv6_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f183b254abe5eabaef1a8dc8e6274a1aeac68a864c5b71fa6d981854aa0539f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "candidateCloudRouterIpv6Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="candidateCustomerRouterIpAddress")
    def candidate_customer_router_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "candidateCustomerRouterIpAddress"))

    @candidate_customer_router_ip_address.setter
    def candidate_customer_router_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a23819442278ab6d807d11a5146b7d4b93002faeadd3a8ad28d7cdf5805cc25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "candidateCustomerRouterIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="candidateCustomerRouterIpv6Address")
    def candidate_customer_router_ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "candidateCustomerRouterIpv6Address"))

    @candidate_customer_router_ipv6_address.setter
    def candidate_customer_router_ipv6_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1306a2c6b48505bbcf83f5d9fafe34378f3e4111b0329dbd43af6b54b246134a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "candidateCustomerRouterIpv6Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="candidateSubnets")
    def candidate_subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "candidateSubnets"))

    @candidate_subnets.setter
    def candidate_subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f508353b3744a1545837b770fd5ecde951855c5498a364d6aaf62c99c287ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "candidateSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2acf89133a93930879a53dac86a3b9a5f1bff467191da01c40eba839cce8fe34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeAvailabilityDomain")
    def edge_availability_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeAvailabilityDomain"))

    @edge_availability_domain.setter
    def edge_availability_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce4ff8562608981677d169381c52f4c13952b8e5ddf33e6f779b4830c631ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeAvailabilityDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryption"))

    @encryption.setter
    def encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2e0b29bd0ddf9b647512a7092c3a76e8eed3b28715e9e32f84eaa3a104fe45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76269b67029d4e1033904f32c6e7f2b788988b1dbdcb291634d77abc0455fce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interconnect")
    def interconnect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interconnect"))

    @interconnect.setter
    def interconnect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fad2f09757d56840eac8971d9c66a767e85c6cce03b94a4aedc021da51f2111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interconnect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipsecInternalAddresses")
    def ipsec_internal_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipsecInternalAddresses"))

    @ipsec_internal_addresses.setter
    def ipsec_internal_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7d4c9ea0020a4f1ad9334f6cf986391ef84dab903d53ea6765449304983dda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipsecInternalAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a525b81289a0ffb5e513743eee8202bd134c561fe7fc8595471c4b39dd5fbfc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19848bf7126152666b66a54953f56ed5b6689f7db89f621f2917b3919f3b0607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbcfbbc3b1cba32447b226e6564e6fb2184052f868f35926c19915d5fa0a3fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edcadf5a9bb97557449ced0c0f184335d7b78a6da7491194b36d08b66c1d71a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528c94a76cbb0e330b04d11966c05ce15e006772272a9d6b2b0d196f4ff85844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="router")
    def router(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "router"))

    @router.setter
    def router(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a6d8c48cc10d047fc138dde56a8f1db14f4d9c7e40ce41b099f082f99a48ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "router", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackType")
    def stack_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackType"))

    @stack_type.setter
    def stack_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ed07c744202a1fd56610b876121d99384fca904ac37aa23de5f3576674c13c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetLength")
    def subnet_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "subnetLength"))

    @subnet_length.setter
    def subnet_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76f2e5d18dc99653fe572044ced423407c8f5ca12e2c34e1568184647f7efb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4585b607c0abbf42d96a3d082ecee8fa9a45f83550fe2d2937993e1b2211ca8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vlanTag8021Q")
    def vlan_tag8021_q(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vlanTag8021Q"))

    @vlan_tag8021_q.setter
    def vlan_tag8021_q(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337c204ca086aaed609369afeb38c5515285761a924f66cc3faa94fda1afd1f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlanTag8021Q", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnectAttachment.GoogleComputeInterconnectAttachmentConfig",
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
        "router": "router",
        "admin_enabled": "adminEnabled",
        "bandwidth": "bandwidth",
        "candidate_cloud_router_ip_address": "candidateCloudRouterIpAddress",
        "candidate_cloud_router_ipv6_address": "candidateCloudRouterIpv6Address",
        "candidate_customer_router_ip_address": "candidateCustomerRouterIpAddress",
        "candidate_customer_router_ipv6_address": "candidateCustomerRouterIpv6Address",
        "candidate_subnets": "candidateSubnets",
        "description": "description",
        "edge_availability_domain": "edgeAvailabilityDomain",
        "encryption": "encryption",
        "id": "id",
        "interconnect": "interconnect",
        "ipsec_internal_addresses": "ipsecInternalAddresses",
        "labels": "labels",
        "mtu": "mtu",
        "project": "project",
        "region": "region",
        "stack_type": "stackType",
        "subnet_length": "subnetLength",
        "timeouts": "timeouts",
        "type": "type",
        "vlan_tag8021_q": "vlanTag8021Q",
    },
)
class GoogleComputeInterconnectAttachmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        router: builtins.str,
        admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bandwidth: typing.Optional[builtins.str] = None,
        candidate_cloud_router_ip_address: typing.Optional[builtins.str] = None,
        candidate_cloud_router_ipv6_address: typing.Optional[builtins.str] = None,
        candidate_customer_router_ip_address: typing.Optional[builtins.str] = None,
        candidate_customer_router_ipv6_address: typing.Optional[builtins.str] = None,
        candidate_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_availability_domain: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect: typing.Optional[builtins.str] = None,
        ipsec_internal_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mtu: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        stack_type: typing.Optional[builtins.str] = None,
        subnet_length: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeInterconnectAttachmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        vlan_tag8021_q: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#name GoogleComputeInterconnectAttachment#name}
        :param router: URL of the cloud router to be used for dynamic routing. This router must be in the same region as this InterconnectAttachment. The InterconnectAttachment will automatically connect the Interconnect to the network & region within which the Cloud Router is configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#router GoogleComputeInterconnectAttachment#router}
        :param admin_enabled: Whether the VLAN attachment is enabled or disabled. When using PARTNER type this will Pre-Activate the interconnect attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#admin_enabled GoogleComputeInterconnectAttachment#admin_enabled}
        :param bandwidth: Provisioned bandwidth capacity for the interconnect attachment. For attachments of type DEDICATED, the user can set the bandwidth. For attachments of type PARTNER, the Google Partner that is operating the interconnect must set the bandwidth. Output only for PARTNER type, mutable for PARTNER_PROVIDER and DEDICATED, Defaults to BPS_10G Possible values: ["BPS_50M", "BPS_100M", "BPS_200M", "BPS_300M", "BPS_400M", "BPS_500M", "BPS_1G", "BPS_2G", "BPS_5G", "BPS_10G", "BPS_20G", "BPS_50G", "BPS_100G"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#bandwidth GoogleComputeInterconnectAttachment#bandwidth}
        :param candidate_cloud_router_ip_address: Single IPv4 address + prefix length to be configured on the cloud router interface for this interconnect attachment. Example: 203.0.113.1/29. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_cloud_router_ip_address GoogleComputeInterconnectAttachment#candidate_cloud_router_ip_address}
        :param candidate_cloud_router_ipv6_address: Single IPv6 address + prefix length to be configured on the cloud router interface for this interconnect attachment. Example: 2001:db8::1/125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_cloud_router_ipv6_address GoogleComputeInterconnectAttachment#candidate_cloud_router_ipv6_address}
        :param candidate_customer_router_ip_address: Single IPv4 address + prefix length to be configured on the customer router interface for this interconnect attachment. Example: 203.0.113.2/29. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_customer_router_ip_address GoogleComputeInterconnectAttachment#candidate_customer_router_ip_address}
        :param candidate_customer_router_ipv6_address: Single IPv6 address + prefix length to be configured on the customer router interface for this interconnect attachment. Example: 2001:db8::2/125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_customer_router_ipv6_address GoogleComputeInterconnectAttachment#candidate_customer_router_ipv6_address}
        :param candidate_subnets: Up to 16 candidate prefixes that can be used to restrict the allocation of cloudRouterIpAddress and customerRouterIpAddress for this attachment. All prefixes must be within link-local address space (169.254.0.0/16) and must be /29 or shorter (/28, /27, etc). Google will attempt to select an unused /29 from the supplied candidate prefix(es). The request will fail if all possible /29s are in use on Google's edge. If not supplied, Google will randomly select an unused /29 from all of link-local space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_subnets GoogleComputeInterconnectAttachment#candidate_subnets}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#description GoogleComputeInterconnectAttachment#description}
        :param edge_availability_domain: Desired availability domain for the attachment. Only available for type PARTNER, at creation time. For improved reliability, customers should configure a pair of attachments with one per availability domain. The selected availability domain will be provided to the Partner via the pairing key so that the provisioned circuit will lie in the specified domain. If not specified, the value will default to AVAILABILITY_DOMAIN_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#edge_availability_domain GoogleComputeInterconnectAttachment#edge_availability_domain}
        :param encryption: Indicates the user-supplied encryption option of this interconnect attachment. Can only be specified at attachment creation for PARTNER or DEDICATED attachments. - NONE - This is the default value, which means that the VLAN attachment carries unencrypted traffic. VMs are able to send traffic to, or receive traffic from, such a VLAN attachment. - IPSEC - The VLAN attachment carries only encrypted traffic that is encrypted by an IPsec device, such as an HA VPN gateway or third-party IPsec VPN. VMs cannot directly send traffic to, or receive traffic from, such a VLAN attachment. To use HA VPN over Cloud Interconnect, the VLAN attachment must be created with this option. Default value: "NONE" Possible values: ["NONE", "IPSEC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#encryption GoogleComputeInterconnectAttachment#encryption}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#id GoogleComputeInterconnectAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect: URL of the underlying Interconnect object that this attachment's traffic will traverse through. Required if type is DEDICATED, must not be set if type is PARTNER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#interconnect GoogleComputeInterconnectAttachment#interconnect}
        :param ipsec_internal_addresses: URL of addresses that have been reserved for the interconnect attachment, Used only for interconnect attachment that has the encryption option as IPSEC. The addresses must be RFC 1918 IP address ranges. When creating HA VPN gateway over the interconnect attachment, if the attachment is configured to use an RFC 1918 IP address, then the VPN gateway's IP address will be allocated from the IP address range specified here. For example, if the HA VPN gateway's interface 0 is paired to this interconnect attachment, then an RFC 1918 IP address for the VPN gateway interface 0 will be allocated from the IP address specified for this interconnect attachment. If this field is not specified for interconnect attachment that has encryption option as IPSEC, later on when creating HA VPN gateway on this interconnect attachment, the HA VPN gateway's IP address will be allocated from regional external IP address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#ipsec_internal_addresses GoogleComputeInterconnectAttachment#ipsec_internal_addresses}
        :param labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#labels GoogleComputeInterconnectAttachment#labels}
        :param mtu: Maximum Transmission Unit (MTU), in bytes, of packets passing through this interconnect attachment. Valid values are 1440, 1460, 1500, and 8896. If not specified, the value will default to 1440. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#mtu GoogleComputeInterconnectAttachment#mtu}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#project GoogleComputeInterconnectAttachment#project}.
        :param region: Region where the regional interconnect attachment resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#region GoogleComputeInterconnectAttachment#region}
        :param stack_type: The stack type for this interconnect attachment to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. This field can be both set at interconnect attachments creation and update interconnect attachment operations. Possible values: ["IPV4_IPV6", "IPV4_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#stack_type GoogleComputeInterconnectAttachment#stack_type}
        :param subnet_length: Length of the IPv4 subnet mask. Allowed values: 29 (default), 30. The default value is 29, except for Cross-Cloud Interconnect connections that use an InterconnectRemoteLocation with a constraints.subnetLengthRange.min equal to 30. For example, connections that use an Azure remote location fall into this category. In these cases, the default value is 30, and requesting 29 returns an error. Where both 29 and 30 are allowed, 29 is preferred, because it gives Google Cloud Support more debugging visibility. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#subnet_length GoogleComputeInterconnectAttachment#subnet_length}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#timeouts GoogleComputeInterconnectAttachment#timeouts}
        :param type: The type of InterconnectAttachment you wish to create. Defaults to DEDICATED. Possible values: ["DEDICATED", "PARTNER", "PARTNER_PROVIDER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#type GoogleComputeInterconnectAttachment#type}
        :param vlan_tag8021_q: The IEEE 802.1Q VLAN tag for this attachment, in the range 2-4094. When using PARTNER type this will be managed upstream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#vlan_tag8021q GoogleComputeInterconnectAttachment#vlan_tag8021q}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeInterconnectAttachmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8a2c0c28ce2189b9689e9a4c3a01abd39e3bc6f9394a1128a21fc37214245d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument router", value=router, expected_type=type_hints["router"])
            check_type(argname="argument admin_enabled", value=admin_enabled, expected_type=type_hints["admin_enabled"])
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument candidate_cloud_router_ip_address", value=candidate_cloud_router_ip_address, expected_type=type_hints["candidate_cloud_router_ip_address"])
            check_type(argname="argument candidate_cloud_router_ipv6_address", value=candidate_cloud_router_ipv6_address, expected_type=type_hints["candidate_cloud_router_ipv6_address"])
            check_type(argname="argument candidate_customer_router_ip_address", value=candidate_customer_router_ip_address, expected_type=type_hints["candidate_customer_router_ip_address"])
            check_type(argname="argument candidate_customer_router_ipv6_address", value=candidate_customer_router_ipv6_address, expected_type=type_hints["candidate_customer_router_ipv6_address"])
            check_type(argname="argument candidate_subnets", value=candidate_subnets, expected_type=type_hints["candidate_subnets"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edge_availability_domain", value=edge_availability_domain, expected_type=type_hints["edge_availability_domain"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument interconnect", value=interconnect, expected_type=type_hints["interconnect"])
            check_type(argname="argument ipsec_internal_addresses", value=ipsec_internal_addresses, expected_type=type_hints["ipsec_internal_addresses"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
            check_type(argname="argument subnet_length", value=subnet_length, expected_type=type_hints["subnet_length"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vlan_tag8021_q", value=vlan_tag8021_q, expected_type=type_hints["vlan_tag8021_q"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "router": router,
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
        if admin_enabled is not None:
            self._values["admin_enabled"] = admin_enabled
        if bandwidth is not None:
            self._values["bandwidth"] = bandwidth
        if candidate_cloud_router_ip_address is not None:
            self._values["candidate_cloud_router_ip_address"] = candidate_cloud_router_ip_address
        if candidate_cloud_router_ipv6_address is not None:
            self._values["candidate_cloud_router_ipv6_address"] = candidate_cloud_router_ipv6_address
        if candidate_customer_router_ip_address is not None:
            self._values["candidate_customer_router_ip_address"] = candidate_customer_router_ip_address
        if candidate_customer_router_ipv6_address is not None:
            self._values["candidate_customer_router_ipv6_address"] = candidate_customer_router_ipv6_address
        if candidate_subnets is not None:
            self._values["candidate_subnets"] = candidate_subnets
        if description is not None:
            self._values["description"] = description
        if edge_availability_domain is not None:
            self._values["edge_availability_domain"] = edge_availability_domain
        if encryption is not None:
            self._values["encryption"] = encryption
        if id is not None:
            self._values["id"] = id
        if interconnect is not None:
            self._values["interconnect"] = interconnect
        if ipsec_internal_addresses is not None:
            self._values["ipsec_internal_addresses"] = ipsec_internal_addresses
        if labels is not None:
            self._values["labels"] = labels
        if mtu is not None:
            self._values["mtu"] = mtu
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if stack_type is not None:
            self._values["stack_type"] = stack_type
        if subnet_length is not None:
            self._values["subnet_length"] = subnet_length
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type
        if vlan_tag8021_q is not None:
            self._values["vlan_tag8021_q"] = vlan_tag8021_q

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
        '''Name of the resource.

        Provided by the client when the resource is created. The
        name must be 1-63 characters long, and comply with RFC1035. Specifically, the
        name must be 1-63 characters long and match the regular expression
        '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a
        lowercase letter, and all following characters must be a dash, lowercase
        letter, or digit, except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#name GoogleComputeInterconnectAttachment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def router(self) -> builtins.str:
        '''URL of the cloud router to be used for dynamic routing.

        This router must be in
        the same region as this InterconnectAttachment. The InterconnectAttachment will
        automatically connect the Interconnect to the network & region within which the
        Cloud Router is configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#router GoogleComputeInterconnectAttachment#router}
        '''
        result = self._values.get("router")
        assert result is not None, "Required property 'router' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the VLAN attachment is enabled or disabled.  When using PARTNER type this will Pre-Activate the interconnect attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#admin_enabled GoogleComputeInterconnectAttachment#admin_enabled}
        '''
        result = self._values.get("admin_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bandwidth(self) -> typing.Optional[builtins.str]:
        '''Provisioned bandwidth capacity for the interconnect attachment.

        For attachments of type DEDICATED, the user can set the bandwidth.
        For attachments of type PARTNER, the Google Partner that is operating the interconnect must set the bandwidth.
        Output only for PARTNER type, mutable for PARTNER_PROVIDER and DEDICATED,
        Defaults to BPS_10G Possible values: ["BPS_50M", "BPS_100M", "BPS_200M", "BPS_300M", "BPS_400M", "BPS_500M", "BPS_1G", "BPS_2G", "BPS_5G", "BPS_10G", "BPS_20G", "BPS_50G", "BPS_100G"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#bandwidth GoogleComputeInterconnectAttachment#bandwidth}
        '''
        result = self._values.get("bandwidth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def candidate_cloud_router_ip_address(self) -> typing.Optional[builtins.str]:
        '''Single IPv4 address + prefix length to be configured on the cloud router interface for this interconnect attachment. Example: 203.0.113.1/29.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_cloud_router_ip_address GoogleComputeInterconnectAttachment#candidate_cloud_router_ip_address}
        '''
        result = self._values.get("candidate_cloud_router_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def candidate_cloud_router_ipv6_address(self) -> typing.Optional[builtins.str]:
        '''Single IPv6 address + prefix length to be configured on the cloud router interface for this interconnect attachment. Example: 2001:db8::1/125.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_cloud_router_ipv6_address GoogleComputeInterconnectAttachment#candidate_cloud_router_ipv6_address}
        '''
        result = self._values.get("candidate_cloud_router_ipv6_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def candidate_customer_router_ip_address(self) -> typing.Optional[builtins.str]:
        '''Single IPv4 address + prefix length to be configured on the customer router interface for this interconnect attachment. Example: 203.0.113.2/29.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_customer_router_ip_address GoogleComputeInterconnectAttachment#candidate_customer_router_ip_address}
        '''
        result = self._values.get("candidate_customer_router_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def candidate_customer_router_ipv6_address(self) -> typing.Optional[builtins.str]:
        '''Single IPv6 address + prefix length to be configured on the customer router interface for this interconnect attachment. Example: 2001:db8::2/125.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_customer_router_ipv6_address GoogleComputeInterconnectAttachment#candidate_customer_router_ipv6_address}
        '''
        result = self._values.get("candidate_customer_router_ipv6_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def candidate_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Up to 16 candidate prefixes that can be used to restrict the allocation of cloudRouterIpAddress and customerRouterIpAddress for this attachment.

        All prefixes must be within link-local address space (169.254.0.0/16)
        and must be /29 or shorter (/28, /27, etc). Google will attempt to select
        an unused /29 from the supplied candidate prefix(es). The request will
        fail if all possible /29s are in use on Google's edge. If not supplied,
        Google will randomly select an unused /29 from all of link-local space.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#candidate_subnets GoogleComputeInterconnectAttachment#candidate_subnets}
        '''
        result = self._values.get("candidate_subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#description GoogleComputeInterconnectAttachment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_availability_domain(self) -> typing.Optional[builtins.str]:
        '''Desired availability domain for the attachment.

        Only available for type
        PARTNER, at creation time. For improved reliability, customers should
        configure a pair of attachments with one per availability domain. The
        selected availability domain will be provided to the Partner via the
        pairing key so that the provisioned circuit will lie in the specified
        domain. If not specified, the value will default to AVAILABILITY_DOMAIN_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#edge_availability_domain GoogleComputeInterconnectAttachment#edge_availability_domain}
        '''
        result = self._values.get("edge_availability_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(self) -> typing.Optional[builtins.str]:
        '''Indicates the user-supplied encryption option of this interconnect attachment.

        Can only be specified at attachment creation for PARTNER or
        DEDICATED attachments.

        - NONE - This is the default value, which means that the VLAN attachment
          carries unencrypted traffic. VMs are able to send traffic to, or receive
          traffic from, such a VLAN attachment.
        - IPSEC - The VLAN attachment carries only encrypted traffic that is
          encrypted by an IPsec device, such as an HA VPN gateway or third-party
          IPsec VPN. VMs cannot directly send traffic to, or receive traffic from,
          such a VLAN attachment. To use HA VPN over Cloud Interconnect, the VLAN
          attachment must be created with this option. Default value: "NONE" Possible values: ["NONE", "IPSEC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#encryption GoogleComputeInterconnectAttachment#encryption}
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#id GoogleComputeInterconnectAttachment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interconnect(self) -> typing.Optional[builtins.str]:
        '''URL of the underlying Interconnect object that this attachment's traffic will traverse through.

        Required if type is DEDICATED, must not
        be set if type is PARTNER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#interconnect GoogleComputeInterconnectAttachment#interconnect}
        '''
        result = self._values.get("interconnect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipsec_internal_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URL of addresses that have been reserved for the interconnect attachment, Used only for interconnect attachment that has the encryption option as IPSEC.

        The addresses must be RFC 1918 IP address ranges. When creating HA VPN
        gateway over the interconnect attachment, if the attachment is configured
        to use an RFC 1918 IP address, then the VPN gateway's IP address will be
        allocated from the IP address range specified here.
        For example, if the HA VPN gateway's interface 0 is paired to this
        interconnect attachment, then an RFC 1918 IP address for the VPN gateway
        interface 0 will be allocated from the IP address specified for this
        interconnect attachment.
        If this field is not specified for interconnect attachment that has
        encryption option as IPSEC, later on when creating HA VPN gateway on this
        interconnect attachment, the HA VPN gateway's IP address will be
        allocated from regional external IP address pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#ipsec_internal_addresses GoogleComputeInterconnectAttachment#ipsec_internal_addresses}
        '''
        result = self._values.get("ipsec_internal_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels for this resource.

        These can only be added or modified by the setLabels
        method. Each label key/value pair must comply with RFC1035. Label values may be empty.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#labels GoogleComputeInterconnectAttachment#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mtu(self) -> typing.Optional[builtins.str]:
        '''Maximum Transmission Unit (MTU), in bytes, of packets passing through this interconnect attachment.

        Valid values are 1440, 1460, 1500, and 8896. If not specified, the value will default to 1440.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#mtu GoogleComputeInterconnectAttachment#mtu}
        '''
        result = self._values.get("mtu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#project GoogleComputeInterconnectAttachment#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the regional interconnect attachment resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#region GoogleComputeInterconnectAttachment#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_type(self) -> typing.Optional[builtins.str]:
        '''The stack type for this interconnect attachment to identify whether the IPv6 feature is enabled or not.

        If not specified, IPV4_ONLY will be used.
        This field can be both set at interconnect attachments creation and update
        interconnect attachment operations. Possible values: ["IPV4_IPV6", "IPV4_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#stack_type GoogleComputeInterconnectAttachment#stack_type}
        '''
        result = self._values.get("stack_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_length(self) -> typing.Optional[jsii.Number]:
        '''Length of the IPv4 subnet mask.

        Allowed values: 29 (default), 30. The default value is 29,
        except for Cross-Cloud Interconnect connections that use an InterconnectRemoteLocation with a
        constraints.subnetLengthRange.min equal to 30. For example, connections that use an Azure
        remote location fall into this category. In these cases, the default value is 30, and
        requesting 29 returns an error. Where both 29 and 30 are allowed, 29 is preferred, because it
        gives Google Cloud Support more debugging visibility.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#subnet_length GoogleComputeInterconnectAttachment#subnet_length}
        '''
        result = self._values.get("subnet_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleComputeInterconnectAttachmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#timeouts GoogleComputeInterconnectAttachment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeInterconnectAttachmentTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of InterconnectAttachment you wish to create. Defaults to DEDICATED. Possible values: ["DEDICATED", "PARTNER", "PARTNER_PROVIDER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#type GoogleComputeInterconnectAttachment#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vlan_tag8021_q(self) -> typing.Optional[jsii.Number]:
        '''The IEEE 802.1Q VLAN tag for this attachment, in the range 2-4094. When using PARTNER type this will be managed upstream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#vlan_tag8021q GoogleComputeInterconnectAttachment#vlan_tag8021q}
        '''
        result = self._values.get("vlan_tag8021_q")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeInterconnectAttachmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnectAttachment.GoogleComputeInterconnectAttachmentPrivateInterconnectInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeInterconnectAttachmentPrivateInterconnectInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeInterconnectAttachmentPrivateInterconnectInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeInterconnectAttachmentPrivateInterconnectInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnectAttachment.GoogleComputeInterconnectAttachmentPrivateInterconnectInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d513030a0e84502dfebe78ab555c998f754d1814880dc691e6799171e93bc8fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83fca419d344d386b9c66281e1c8529c9694b518fdb645e4d6db22eacbb50845)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129eec3d8c70c4a3ed50c7fc018e8c9f016d3f200298b4f8ea29c678e301ec0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1206c185e9afd4ed46d30e2a244ab256592eb4d787dbcf3be7612140c09a01eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6eca899e50143e1c9aa182f574f49fd76e12019b7896e3c46e41bfd6d652d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnectAttachment.GoogleComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53e5de318e642b1ccc437b593581d6eb2e06378e051196b69115575dad66eb35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="tag8021Q")
    def tag8021_q(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tag8021Q"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeInterconnectAttachmentPrivateInterconnectInfo]:
        return typing.cast(typing.Optional[GoogleComputeInterconnectAttachmentPrivateInterconnectInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeInterconnectAttachmentPrivateInterconnectInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5a7d0871ef2fa2d90a187e8833a26e123e19cf884e3796f90fb3d8f0716b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnectAttachment.GoogleComputeInterconnectAttachmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeInterconnectAttachmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#create GoogleComputeInterconnectAttachment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#delete GoogleComputeInterconnectAttachment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#update GoogleComputeInterconnectAttachment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c6d69434603b37d840d45a59160760988fb3256e3d0bf63e04fcebb6f3de56)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#create GoogleComputeInterconnectAttachment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#delete GoogleComputeInterconnectAttachment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect_attachment#update GoogleComputeInterconnectAttachment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeInterconnectAttachmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeInterconnectAttachmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnectAttachment.GoogleComputeInterconnectAttachmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56caa8f726fe74b6aa5ecd935aacc2b297378109475653217eddb024688c3edb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2cb1218ea520e5bdaed2010dd508a21b9f80ac83d03bc055bf87a9db0cebb31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1338bf5cdad86741a4ad99d5e76c5a74efbe4a6bc01de4b31c4187bc6f5de8b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0873deae8fbf7f1574ebed7a77397adffaeec3a1b48b181c07a04c0c3fc5b9f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectAttachmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectAttachmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectAttachmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7fb19ca0f7430ce25dfdf50663314b0590e32e8182c72cf80c13f2661d791b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeInterconnectAttachment",
    "GoogleComputeInterconnectAttachmentConfig",
    "GoogleComputeInterconnectAttachmentPrivateInterconnectInfo",
    "GoogleComputeInterconnectAttachmentPrivateInterconnectInfoList",
    "GoogleComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference",
    "GoogleComputeInterconnectAttachmentTimeouts",
    "GoogleComputeInterconnectAttachmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f39774e0a138de5b8012a3bbcf6c0b1af85b0cbd3d0706a218291aec40041dae(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    router: builtins.str,
    admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bandwidth: typing.Optional[builtins.str] = None,
    candidate_cloud_router_ip_address: typing.Optional[builtins.str] = None,
    candidate_cloud_router_ipv6_address: typing.Optional[builtins.str] = None,
    candidate_customer_router_ip_address: typing.Optional[builtins.str] = None,
    candidate_customer_router_ipv6_address: typing.Optional[builtins.str] = None,
    candidate_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_availability_domain: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect: typing.Optional[builtins.str] = None,
    ipsec_internal_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mtu: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    stack_type: typing.Optional[builtins.str] = None,
    subnet_length: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeInterconnectAttachmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    vlan_tag8021_q: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__4dc489dfab38c7f7dccd7e16f87056d403bdbd680ae2e80a1cb8e62de4668593(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fb23c7d4a9a04aba88c57a3dcd78f440a466df76b5e1c035f8606810094b7a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebde522462ca2e0cb74cb27375a5298620da5659bdd75dc6991baad37b348b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f855e4d7b7d59945c21145bfecb72fd909bade7e490adfbca6d8429ebd3db7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f183b254abe5eabaef1a8dc8e6274a1aeac68a864c5b71fa6d981854aa0539f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a23819442278ab6d807d11a5146b7d4b93002faeadd3a8ad28d7cdf5805cc25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1306a2c6b48505bbcf83f5d9fafe34378f3e4111b0329dbd43af6b54b246134a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f508353b3744a1545837b770fd5ecde951855c5498a364d6aaf62c99c287ad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2acf89133a93930879a53dac86a3b9a5f1bff467191da01c40eba839cce8fe34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce4ff8562608981677d169381c52f4c13952b8e5ddf33e6f779b4830c631ca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2e0b29bd0ddf9b647512a7092c3a76e8eed3b28715e9e32f84eaa3a104fe45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76269b67029d4e1033904f32c6e7f2b788988b1dbdcb291634d77abc0455fce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fad2f09757d56840eac8971d9c66a767e85c6cce03b94a4aedc021da51f2111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7d4c9ea0020a4f1ad9334f6cf986391ef84dab903d53ea6765449304983dda(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a525b81289a0ffb5e513743eee8202bd134c561fe7fc8595471c4b39dd5fbfc2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19848bf7126152666b66a54953f56ed5b6689f7db89f621f2917b3919f3b0607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbcfbbc3b1cba32447b226e6564e6fb2184052f868f35926c19915d5fa0a3fd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcadf5a9bb97557449ced0c0f184335d7b78a6da7491194b36d08b66c1d71a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528c94a76cbb0e330b04d11966c05ce15e006772272a9d6b2b0d196f4ff85844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a6d8c48cc10d047fc138dde56a8f1db14f4d9c7e40ce41b099f082f99a48ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ed07c744202a1fd56610b876121d99384fca904ac37aa23de5f3576674c13c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76f2e5d18dc99653fe572044ced423407c8f5ca12e2c34e1568184647f7efb3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4585b607c0abbf42d96a3d082ecee8fa9a45f83550fe2d2937993e1b2211ca8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337c204ca086aaed609369afeb38c5515285761a924f66cc3faa94fda1afd1f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8a2c0c28ce2189b9689e9a4c3a01abd39e3bc6f9394a1128a21fc37214245d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    router: builtins.str,
    admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bandwidth: typing.Optional[builtins.str] = None,
    candidate_cloud_router_ip_address: typing.Optional[builtins.str] = None,
    candidate_cloud_router_ipv6_address: typing.Optional[builtins.str] = None,
    candidate_customer_router_ip_address: typing.Optional[builtins.str] = None,
    candidate_customer_router_ipv6_address: typing.Optional[builtins.str] = None,
    candidate_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_availability_domain: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect: typing.Optional[builtins.str] = None,
    ipsec_internal_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mtu: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    stack_type: typing.Optional[builtins.str] = None,
    subnet_length: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeInterconnectAttachmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    vlan_tag8021_q: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d513030a0e84502dfebe78ab555c998f754d1814880dc691e6799171e93bc8fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83fca419d344d386b9c66281e1c8529c9694b518fdb645e4d6db22eacbb50845(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129eec3d8c70c4a3ed50c7fc018e8c9f016d3f200298b4f8ea29c678e301ec0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1206c185e9afd4ed46d30e2a244ab256592eb4d787dbcf3be7612140c09a01eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6eca899e50143e1c9aa182f574f49fd76e12019b7896e3c46e41bfd6d652d66(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e5de318e642b1ccc437b593581d6eb2e06378e051196b69115575dad66eb35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5a7d0871ef2fa2d90a187e8833a26e123e19cf884e3796f90fb3d8f0716b85(
    value: typing.Optional[GoogleComputeInterconnectAttachmentPrivateInterconnectInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c6d69434603b37d840d45a59160760988fb3256e3d0bf63e04fcebb6f3de56(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56caa8f726fe74b6aa5ecd935aacc2b297378109475653217eddb024688c3edb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2cb1218ea520e5bdaed2010dd508a21b9f80ac83d03bc055bf87a9db0cebb31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1338bf5cdad86741a4ad99d5e76c5a74efbe4a6bc01de4b31c4187bc6f5de8b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0873deae8fbf7f1574ebed7a77397adffaeec3a1b48b181c07a04c0c3fc5b9f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7fb19ca0f7430ce25dfdf50663314b0590e32e8182c72cf80c13f2661d791b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectAttachmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
