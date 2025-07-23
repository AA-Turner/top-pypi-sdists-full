r'''
# `google_compute_interconnect_attachment`

Refer to the Terraform Registry for docs: [`google_compute_interconnect_attachment`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment).
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


class ComputeInterconnectAttachment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnectAttachment.ComputeInterconnectAttachment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment google_compute_interconnect_attachment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        router: builtins.str,
        admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bandwidth: typing.Optional[builtins.str] = None,
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
        timeouts: typing.Optional[typing.Union["ComputeInterconnectAttachmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment google_compute_interconnect_attachment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#name ComputeInterconnectAttachment#name}
        :param router: URL of the cloud router to be used for dynamic routing. This router must be in the same region as this InterconnectAttachment. The InterconnectAttachment will automatically connect the Interconnect to the network & region within which the Cloud Router is configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#router ComputeInterconnectAttachment#router}
        :param admin_enabled: Whether the VLAN attachment is enabled or disabled. When using PARTNER type this will Pre-Activate the interconnect attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#admin_enabled ComputeInterconnectAttachment#admin_enabled}
        :param bandwidth: Provisioned bandwidth capacity for the interconnect attachment. For attachments of type DEDICATED, the user can set the bandwidth. For attachments of type PARTNER, the Google Partner that is operating the interconnect must set the bandwidth. Output only for PARTNER type, mutable for PARTNER_PROVIDER and DEDICATED, Defaults to BPS_10G Possible values: ["BPS_50M", "BPS_100M", "BPS_200M", "BPS_300M", "BPS_400M", "BPS_500M", "BPS_1G", "BPS_2G", "BPS_5G", "BPS_10G", "BPS_20G", "BPS_50G", "BPS_100G"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#bandwidth ComputeInterconnectAttachment#bandwidth}
        :param candidate_subnets: Up to 16 candidate prefixes that can be used to restrict the allocation of cloudRouterIpAddress and customerRouterIpAddress for this attachment. All prefixes must be within link-local address space (169.254.0.0/16) and must be /29 or shorter (/28, /27, etc). Google will attempt to select an unused /29 from the supplied candidate prefix(es). The request will fail if all possible /29s are in use on Google's edge. If not supplied, Google will randomly select an unused /29 from all of link-local space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#candidate_subnets ComputeInterconnectAttachment#candidate_subnets}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#description ComputeInterconnectAttachment#description}
        :param edge_availability_domain: Desired availability domain for the attachment. Only available for type PARTNER, at creation time. For improved reliability, customers should configure a pair of attachments with one per availability domain. The selected availability domain will be provided to the Partner via the pairing key so that the provisioned circuit will lie in the specified domain. If not specified, the value will default to AVAILABILITY_DOMAIN_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#edge_availability_domain ComputeInterconnectAttachment#edge_availability_domain}
        :param encryption: Indicates the user-supplied encryption option of this interconnect attachment. Can only be specified at attachment creation for PARTNER or DEDICATED attachments. - NONE - This is the default value, which means that the VLAN attachment carries unencrypted traffic. VMs are able to send traffic to, or receive traffic from, such a VLAN attachment. - IPSEC - The VLAN attachment carries only encrypted traffic that is encrypted by an IPsec device, such as an HA VPN gateway or third-party IPsec VPN. VMs cannot directly send traffic to, or receive traffic from, such a VLAN attachment. To use HA VPN over Cloud Interconnect, the VLAN attachment must be created with this option. Default value: "NONE" Possible values: ["NONE", "IPSEC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#encryption ComputeInterconnectAttachment#encryption}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#id ComputeInterconnectAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect: URL of the underlying Interconnect object that this attachment's traffic will traverse through. Required if type is DEDICATED, must not be set if type is PARTNER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#interconnect ComputeInterconnectAttachment#interconnect}
        :param ipsec_internal_addresses: URL of addresses that have been reserved for the interconnect attachment, Used only for interconnect attachment that has the encryption option as IPSEC. The addresses must be RFC 1918 IP address ranges. When creating HA VPN gateway over the interconnect attachment, if the attachment is configured to use an RFC 1918 IP address, then the VPN gateway's IP address will be allocated from the IP address range specified here. For example, if the HA VPN gateway's interface 0 is paired to this interconnect attachment, then an RFC 1918 IP address for the VPN gateway interface 0 will be allocated from the IP address specified for this interconnect attachment. If this field is not specified for interconnect attachment that has encryption option as IPSEC, later on when creating HA VPN gateway on this interconnect attachment, the HA VPN gateway's IP address will be allocated from regional external IP address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#ipsec_internal_addresses ComputeInterconnectAttachment#ipsec_internal_addresses}
        :param labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#labels ComputeInterconnectAttachment#labels}
        :param mtu: Maximum Transmission Unit (MTU), in bytes, of packets passing through this interconnect attachment. Valid values are 1440, 1460, 1500, and 8896. If not specified, the value will default to 1440. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#mtu ComputeInterconnectAttachment#mtu}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#project ComputeInterconnectAttachment#project}.
        :param region: Region where the regional interconnect attachment resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#region ComputeInterconnectAttachment#region}
        :param stack_type: The stack type for this interconnect attachment to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. This field can be both set at interconnect attachments creation and update interconnect attachment operations. Possible values: ["IPV4_IPV6", "IPV4_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#stack_type ComputeInterconnectAttachment#stack_type}
        :param subnet_length: Length of the IPv4 subnet mask. Allowed values: 29 (default), 30. The default value is 29, except for Cross-Cloud Interconnect connections that use an InterconnectRemoteLocation with a constraints.subnetLengthRange.min equal to 30. For example, connections that use an Azure remote location fall into this category. In these cases, the default value is 30, and requesting 29 returns an error. Where both 29 and 30 are allowed, 29 is preferred, because it gives Google Cloud Support more debugging visibility. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#subnet_length ComputeInterconnectAttachment#subnet_length}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#timeouts ComputeInterconnectAttachment#timeouts}
        :param type: The type of InterconnectAttachment you wish to create. Defaults to DEDICATED. Possible values: ["DEDICATED", "PARTNER", "PARTNER_PROVIDER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#type ComputeInterconnectAttachment#type}
        :param vlan_tag8021_q: The IEEE 802.1Q VLAN tag for this attachment, in the range 2-4094. When using PARTNER type this will be managed upstream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#vlan_tag8021q ComputeInterconnectAttachment#vlan_tag8021q}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2582b6be3cb3112a7762e315413264b0d1c901f2db5614b717a7f94432eab6dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeInterconnectAttachmentConfig(
            name=name,
            router=router,
            admin_enabled=admin_enabled,
            bandwidth=bandwidth,
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
        '''Generates CDKTF code for importing a ComputeInterconnectAttachment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeInterconnectAttachment to import.
        :param import_from_id: The id of the existing ComputeInterconnectAttachment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeInterconnectAttachment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e73782d6c8dd82ed5498ce55ab5c23c26b57b05b38f9f747cd12873ee35ec8)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#create ComputeInterconnectAttachment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#delete ComputeInterconnectAttachment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#update ComputeInterconnectAttachment#update}.
        '''
        value = ComputeInterconnectAttachmentTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminEnabled")
    def reset_admin_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminEnabled", []))

    @jsii.member(jsii_name="resetBandwidth")
    def reset_bandwidth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidth", []))

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
    ) -> "ComputeInterconnectAttachmentPrivateInterconnectInfoList":
        return typing.cast("ComputeInterconnectAttachmentPrivateInterconnectInfoList", jsii.get(self, "privateInterconnectInfo"))

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
    def timeouts(self) -> "ComputeInterconnectAttachmentTimeoutsOutputReference":
        return typing.cast("ComputeInterconnectAttachmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInterconnectAttachmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInterconnectAttachmentTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c90645b0f7cf295df558320e73e4417bda97f5c22898601d993902ae566a0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidth"))

    @bandwidth.setter
    def bandwidth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7054cb22eb774f053e8c486d3360a62f023147f93f99f88ae4f49a6ea48b0c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="candidateSubnets")
    def candidate_subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "candidateSubnets"))

    @candidate_subnets.setter
    def candidate_subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081376befb20156c4333a975866a77a88f36c7bb809c50613b25a143b1f57e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "candidateSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b925d5c598dc7eaf7f12ba6a2c74ba7fd9724d7f2d6281b2bbea4147fba4976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeAvailabilityDomain")
    def edge_availability_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeAvailabilityDomain"))

    @edge_availability_domain.setter
    def edge_availability_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324ca615f61d22710c701a834667d02e814f49de1afe6f13275d88cd3f79b0ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeAvailabilityDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryption"))

    @encryption.setter
    def encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdfe0d9fffda1a918d77b1c5ca1dc804c35b0a671fbf7c93427515e05296d99e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9007929bd6d6cd937e0df5837f10e1205aaa6b0ce3e6aca279788ba51b5dfc74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interconnect")
    def interconnect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interconnect"))

    @interconnect.setter
    def interconnect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2223d6cf69cf40717d3ab21b892dde33e8d07b32c906c4c7d04e040a17e147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interconnect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipsecInternalAddresses")
    def ipsec_internal_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipsecInternalAddresses"))

    @ipsec_internal_addresses.setter
    def ipsec_internal_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7bc273b82bd272888c26cde6b932646b777d7574815fee31447fe159a00f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipsecInternalAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50f7efe8dd785459c02fd07efe606fa1541bf0fa68dc9e00de8c45d73c42944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625c907c42ce786f15dc484eb129565416a1fb2e856cd2a0117b28f20c17c690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080040f0b64451c3da4c197ba7da7bfb13b69015971de084b841cc2479e12c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f6a3f15702bcf5792a4b61e17734a0149c9e7ec4a8e483ccb9ba99a8bd40b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf231313ae38204976f26386d26324555c06c8a0f73b87822c3d191953b54314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="router")
    def router(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "router"))

    @router.setter
    def router(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b3232a0808a0aad3687d8cb63178a4f1105f375328a25d9bdc4dd50a4243cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "router", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackType")
    def stack_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackType"))

    @stack_type.setter
    def stack_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b870c0a07c270cb4c38b647abae2c229e0b297d81f409021f8b6511836fc0243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetLength")
    def subnet_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "subnetLength"))

    @subnet_length.setter
    def subnet_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8f48068da3de6b2aeda8c17abcf648f2c86d0e9de63a65548c593f59256181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cf44e2575095ecead4b7e5f1c4e6871b06cf0aa9049f88aa3dc0cf5f60a0d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vlanTag8021Q")
    def vlan_tag8021_q(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vlanTag8021Q"))

    @vlan_tag8021_q.setter
    def vlan_tag8021_q(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4483c650098fd70aa9e829129595c030015f932ae4724a11e35bd42257f90d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlanTag8021Q", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInterconnectAttachment.ComputeInterconnectAttachmentConfig",
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
class ComputeInterconnectAttachmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        timeouts: typing.Optional[typing.Union["ComputeInterconnectAttachmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#name ComputeInterconnectAttachment#name}
        :param router: URL of the cloud router to be used for dynamic routing. This router must be in the same region as this InterconnectAttachment. The InterconnectAttachment will automatically connect the Interconnect to the network & region within which the Cloud Router is configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#router ComputeInterconnectAttachment#router}
        :param admin_enabled: Whether the VLAN attachment is enabled or disabled. When using PARTNER type this will Pre-Activate the interconnect attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#admin_enabled ComputeInterconnectAttachment#admin_enabled}
        :param bandwidth: Provisioned bandwidth capacity for the interconnect attachment. For attachments of type DEDICATED, the user can set the bandwidth. For attachments of type PARTNER, the Google Partner that is operating the interconnect must set the bandwidth. Output only for PARTNER type, mutable for PARTNER_PROVIDER and DEDICATED, Defaults to BPS_10G Possible values: ["BPS_50M", "BPS_100M", "BPS_200M", "BPS_300M", "BPS_400M", "BPS_500M", "BPS_1G", "BPS_2G", "BPS_5G", "BPS_10G", "BPS_20G", "BPS_50G", "BPS_100G"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#bandwidth ComputeInterconnectAttachment#bandwidth}
        :param candidate_subnets: Up to 16 candidate prefixes that can be used to restrict the allocation of cloudRouterIpAddress and customerRouterIpAddress for this attachment. All prefixes must be within link-local address space (169.254.0.0/16) and must be /29 or shorter (/28, /27, etc). Google will attempt to select an unused /29 from the supplied candidate prefix(es). The request will fail if all possible /29s are in use on Google's edge. If not supplied, Google will randomly select an unused /29 from all of link-local space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#candidate_subnets ComputeInterconnectAttachment#candidate_subnets}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#description ComputeInterconnectAttachment#description}
        :param edge_availability_domain: Desired availability domain for the attachment. Only available for type PARTNER, at creation time. For improved reliability, customers should configure a pair of attachments with one per availability domain. The selected availability domain will be provided to the Partner via the pairing key so that the provisioned circuit will lie in the specified domain. If not specified, the value will default to AVAILABILITY_DOMAIN_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#edge_availability_domain ComputeInterconnectAttachment#edge_availability_domain}
        :param encryption: Indicates the user-supplied encryption option of this interconnect attachment. Can only be specified at attachment creation for PARTNER or DEDICATED attachments. - NONE - This is the default value, which means that the VLAN attachment carries unencrypted traffic. VMs are able to send traffic to, or receive traffic from, such a VLAN attachment. - IPSEC - The VLAN attachment carries only encrypted traffic that is encrypted by an IPsec device, such as an HA VPN gateway or third-party IPsec VPN. VMs cannot directly send traffic to, or receive traffic from, such a VLAN attachment. To use HA VPN over Cloud Interconnect, the VLAN attachment must be created with this option. Default value: "NONE" Possible values: ["NONE", "IPSEC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#encryption ComputeInterconnectAttachment#encryption}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#id ComputeInterconnectAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect: URL of the underlying Interconnect object that this attachment's traffic will traverse through. Required if type is DEDICATED, must not be set if type is PARTNER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#interconnect ComputeInterconnectAttachment#interconnect}
        :param ipsec_internal_addresses: URL of addresses that have been reserved for the interconnect attachment, Used only for interconnect attachment that has the encryption option as IPSEC. The addresses must be RFC 1918 IP address ranges. When creating HA VPN gateway over the interconnect attachment, if the attachment is configured to use an RFC 1918 IP address, then the VPN gateway's IP address will be allocated from the IP address range specified here. For example, if the HA VPN gateway's interface 0 is paired to this interconnect attachment, then an RFC 1918 IP address for the VPN gateway interface 0 will be allocated from the IP address specified for this interconnect attachment. If this field is not specified for interconnect attachment that has encryption option as IPSEC, later on when creating HA VPN gateway on this interconnect attachment, the HA VPN gateway's IP address will be allocated from regional external IP address pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#ipsec_internal_addresses ComputeInterconnectAttachment#ipsec_internal_addresses}
        :param labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#labels ComputeInterconnectAttachment#labels}
        :param mtu: Maximum Transmission Unit (MTU), in bytes, of packets passing through this interconnect attachment. Valid values are 1440, 1460, 1500, and 8896. If not specified, the value will default to 1440. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#mtu ComputeInterconnectAttachment#mtu}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#project ComputeInterconnectAttachment#project}.
        :param region: Region where the regional interconnect attachment resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#region ComputeInterconnectAttachment#region}
        :param stack_type: The stack type for this interconnect attachment to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. This field can be both set at interconnect attachments creation and update interconnect attachment operations. Possible values: ["IPV4_IPV6", "IPV4_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#stack_type ComputeInterconnectAttachment#stack_type}
        :param subnet_length: Length of the IPv4 subnet mask. Allowed values: 29 (default), 30. The default value is 29, except for Cross-Cloud Interconnect connections that use an InterconnectRemoteLocation with a constraints.subnetLengthRange.min equal to 30. For example, connections that use an Azure remote location fall into this category. In these cases, the default value is 30, and requesting 29 returns an error. Where both 29 and 30 are allowed, 29 is preferred, because it gives Google Cloud Support more debugging visibility. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#subnet_length ComputeInterconnectAttachment#subnet_length}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#timeouts ComputeInterconnectAttachment#timeouts}
        :param type: The type of InterconnectAttachment you wish to create. Defaults to DEDICATED. Possible values: ["DEDICATED", "PARTNER", "PARTNER_PROVIDER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#type ComputeInterconnectAttachment#type}
        :param vlan_tag8021_q: The IEEE 802.1Q VLAN tag for this attachment, in the range 2-4094. When using PARTNER type this will be managed upstream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#vlan_tag8021q ComputeInterconnectAttachment#vlan_tag8021q}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeInterconnectAttachmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666615174772dd4ca8c9aacd73cfdbb284087b0a20510451f9dccdd605051d8e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#name ComputeInterconnectAttachment#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#router ComputeInterconnectAttachment#router}
        '''
        result = self._values.get("router")
        assert result is not None, "Required property 'router' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the VLAN attachment is enabled or disabled.  When using PARTNER type this will Pre-Activate the interconnect attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#admin_enabled ComputeInterconnectAttachment#admin_enabled}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#bandwidth ComputeInterconnectAttachment#bandwidth}
        '''
        result = self._values.get("bandwidth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def candidate_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Up to 16 candidate prefixes that can be used to restrict the allocation of cloudRouterIpAddress and customerRouterIpAddress for this attachment.

        All prefixes must be within link-local address space (169.254.0.0/16)
        and must be /29 or shorter (/28, /27, etc). Google will attempt to select
        an unused /29 from the supplied candidate prefix(es). The request will
        fail if all possible /29s are in use on Google's edge. If not supplied,
        Google will randomly select an unused /29 from all of link-local space.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#candidate_subnets ComputeInterconnectAttachment#candidate_subnets}
        '''
        result = self._values.get("candidate_subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#description ComputeInterconnectAttachment#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#edge_availability_domain ComputeInterconnectAttachment#edge_availability_domain}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#encryption ComputeInterconnectAttachment#encryption}
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#id ComputeInterconnectAttachment#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#interconnect ComputeInterconnectAttachment#interconnect}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#ipsec_internal_addresses ComputeInterconnectAttachment#ipsec_internal_addresses}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#labels ComputeInterconnectAttachment#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mtu(self) -> typing.Optional[builtins.str]:
        '''Maximum Transmission Unit (MTU), in bytes, of packets passing through this interconnect attachment.

        Valid values are 1440, 1460, 1500, and 8896. If not specified, the value will default to 1440.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#mtu ComputeInterconnectAttachment#mtu}
        '''
        result = self._values.get("mtu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#project ComputeInterconnectAttachment#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the regional interconnect attachment resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#region ComputeInterconnectAttachment#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_type(self) -> typing.Optional[builtins.str]:
        '''The stack type for this interconnect attachment to identify whether the IPv6 feature is enabled or not.

        If not specified, IPV4_ONLY will be used.
        This field can be both set at interconnect attachments creation and update
        interconnect attachment operations. Possible values: ["IPV4_IPV6", "IPV4_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#stack_type ComputeInterconnectAttachment#stack_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#subnet_length ComputeInterconnectAttachment#subnet_length}
        '''
        result = self._values.get("subnet_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeInterconnectAttachmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#timeouts ComputeInterconnectAttachment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeInterconnectAttachmentTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of InterconnectAttachment you wish to create. Defaults to DEDICATED. Possible values: ["DEDICATED", "PARTNER", "PARTNER_PROVIDER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#type ComputeInterconnectAttachment#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vlan_tag8021_q(self) -> typing.Optional[jsii.Number]:
        '''The IEEE 802.1Q VLAN tag for this attachment, in the range 2-4094. When using PARTNER type this will be managed upstream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#vlan_tag8021q ComputeInterconnectAttachment#vlan_tag8021q}
        '''
        result = self._values.get("vlan_tag8021_q")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInterconnectAttachmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInterconnectAttachment.ComputeInterconnectAttachmentPrivateInterconnectInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeInterconnectAttachmentPrivateInterconnectInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInterconnectAttachmentPrivateInterconnectInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInterconnectAttachmentPrivateInterconnectInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnectAttachment.ComputeInterconnectAttachmentPrivateInterconnectInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__788417e7e958ac6e0bb9af8838f70c32fd9670b824482af3ca5aa211e9ef8d6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9985e87fef75dfba361ba380648920d12445c693271ab8eab8b61ce23d6260d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0baa1053cc4b0974846c03a360c8204b121fa36868d87b614f6aa6d0694487d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0064b58bf723bff7c2cc08c96f2f46bda936f46e4bedac3edc6b10450981b11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__415b3fd78c00b9a62154088afe6e2663e2b345750d2e139a468306dd27f598d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnectAttachment.ComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd744e3d7063d4c495d3b08adfb80806e417f1e1b8c96c5b474c77bbfdf0f25f)
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
    ) -> typing.Optional[ComputeInterconnectAttachmentPrivateInterconnectInfo]:
        return typing.cast(typing.Optional[ComputeInterconnectAttachmentPrivateInterconnectInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInterconnectAttachmentPrivateInterconnectInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da4b293798da2022705022faa3b4c16b2b617632c025cb0c227da4cc2be49aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInterconnectAttachment.ComputeInterconnectAttachmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeInterconnectAttachmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#create ComputeInterconnectAttachment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#delete ComputeInterconnectAttachment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#update ComputeInterconnectAttachment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f515e1717ba361a7f2b706a0123293df6ec5b005387680b418d1fcf048105bc9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#create ComputeInterconnectAttachment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#delete ComputeInterconnectAttachment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect_attachment#update ComputeInterconnectAttachment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInterconnectAttachmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInterconnectAttachmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnectAttachment.ComputeInterconnectAttachmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__881b8fadcbdcaf1b65cfb53855072653f87bbedc335aba3ee0d1e0134c3a19f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3499b9cae32f0642a96410ed2b5cf43e8ea8c817f442e66ab0ce529a648a3b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9008e88ca5a102a1865d2143237d23d8d69c3fc141ab3e8d6b2a4632c58a156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdef7e737a2a1edace9c1776ce64414ce7d749f8f8a6bf207496e72d4f883510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectAttachmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectAttachmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectAttachmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef729cb6e660738fd8f284dd0ba5e17b4b15871f42b10facf022d8aeb2de5266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeInterconnectAttachment",
    "ComputeInterconnectAttachmentConfig",
    "ComputeInterconnectAttachmentPrivateInterconnectInfo",
    "ComputeInterconnectAttachmentPrivateInterconnectInfoList",
    "ComputeInterconnectAttachmentPrivateInterconnectInfoOutputReference",
    "ComputeInterconnectAttachmentTimeouts",
    "ComputeInterconnectAttachmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2582b6be3cb3112a7762e315413264b0d1c901f2db5614b717a7f94432eab6dd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    router: builtins.str,
    admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bandwidth: typing.Optional[builtins.str] = None,
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
    timeouts: typing.Optional[typing.Union[ComputeInterconnectAttachmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__00e73782d6c8dd82ed5498ce55ab5c23c26b57b05b38f9f747cd12873ee35ec8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c90645b0f7cf295df558320e73e4417bda97f5c22898601d993902ae566a0e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7054cb22eb774f053e8c486d3360a62f023147f93f99f88ae4f49a6ea48b0c7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081376befb20156c4333a975866a77a88f36c7bb809c50613b25a143b1f57e1e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b925d5c598dc7eaf7f12ba6a2c74ba7fd9724d7f2d6281b2bbea4147fba4976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324ca615f61d22710c701a834667d02e814f49de1afe6f13275d88cd3f79b0ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfe0d9fffda1a918d77b1c5ca1dc804c35b0a671fbf7c93427515e05296d99e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9007929bd6d6cd937e0df5837f10e1205aaa6b0ce3e6aca279788ba51b5dfc74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2223d6cf69cf40717d3ab21b892dde33e8d07b32c906c4c7d04e040a17e147(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7bc273b82bd272888c26cde6b932646b777d7574815fee31447fe159a00f9c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50f7efe8dd785459c02fd07efe606fa1541bf0fa68dc9e00de8c45d73c42944(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625c907c42ce786f15dc484eb129565416a1fb2e856cd2a0117b28f20c17c690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080040f0b64451c3da4c197ba7da7bfb13b69015971de084b841cc2479e12c24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f6a3f15702bcf5792a4b61e17734a0149c9e7ec4a8e483ccb9ba99a8bd40b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf231313ae38204976f26386d26324555c06c8a0f73b87822c3d191953b54314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b3232a0808a0aad3687d8cb63178a4f1105f375328a25d9bdc4dd50a4243cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b870c0a07c270cb4c38b647abae2c229e0b297d81f409021f8b6511836fc0243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8f48068da3de6b2aeda8c17abcf648f2c86d0e9de63a65548c593f59256181(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cf44e2575095ecead4b7e5f1c4e6871b06cf0aa9049f88aa3dc0cf5f60a0d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4483c650098fd70aa9e829129595c030015f932ae4724a11e35bd42257f90d27(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666615174772dd4ca8c9aacd73cfdbb284087b0a20510451f9dccdd605051d8e(
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
    timeouts: typing.Optional[typing.Union[ComputeInterconnectAttachmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    vlan_tag8021_q: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788417e7e958ac6e0bb9af8838f70c32fd9670b824482af3ca5aa211e9ef8d6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9985e87fef75dfba361ba380648920d12445c693271ab8eab8b61ce23d6260d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baa1053cc4b0974846c03a360c8204b121fa36868d87b614f6aa6d0694487d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0064b58bf723bff7c2cc08c96f2f46bda936f46e4bedac3edc6b10450981b11(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415b3fd78c00b9a62154088afe6e2663e2b345750d2e139a468306dd27f598d3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd744e3d7063d4c495d3b08adfb80806e417f1e1b8c96c5b474c77bbfdf0f25f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da4b293798da2022705022faa3b4c16b2b617632c025cb0c227da4cc2be49aa(
    value: typing.Optional[ComputeInterconnectAttachmentPrivateInterconnectInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f515e1717ba361a7f2b706a0123293df6ec5b005387680b418d1fcf048105bc9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881b8fadcbdcaf1b65cfb53855072653f87bbedc335aba3ee0d1e0134c3a19f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3499b9cae32f0642a96410ed2b5cf43e8ea8c817f442e66ab0ce529a648a3b21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9008e88ca5a102a1865d2143237d23d8d69c3fc141ab3e8d6b2a4632c58a156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdef7e737a2a1edace9c1776ce64414ce7d749f8f8a6bf207496e72d4f883510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef729cb6e660738fd8f284dd0ba5e17b4b15871f42b10facf022d8aeb2de5266(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectAttachmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
