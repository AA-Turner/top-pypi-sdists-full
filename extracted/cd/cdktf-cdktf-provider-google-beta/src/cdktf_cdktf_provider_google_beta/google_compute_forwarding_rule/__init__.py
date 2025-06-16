r'''
# `google_compute_forwarding_rule`

Refer to the Terraform Registry for docs: [`google_compute_forwarding_rule`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule).
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


class GoogleComputeForwardingRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeForwardingRule.GoogleComputeForwardingRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule google_compute_forwarding_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        allow_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_psc_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        all_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_service: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ip_collection: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[builtins.str] = None,
        is_mirroring_collector: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
        no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port_range: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        recreate_closed_psc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        service_directory_registrations: typing.Optional[typing.Union["GoogleComputeForwardingRuleServiceDirectoryRegistrations", typing.Dict[builtins.str, typing.Any]]] = None,
        service_label: typing.Optional[builtins.str] = None,
        source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule google_compute_forwarding_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. For Private Service Connect forwarding rules that forward traffic to Google APIs, the forwarding rule name must be a 1-20 characters string with lowercase letters and numbers and must start with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#name GoogleComputeForwardingRule#name}
        :param allow_global_access: This field is used along with the 'backend_service' field for internal load balancing or with the 'target' field for internal TargetInstance. If the field is set to 'TRUE', clients can access ILB from all regions. Otherwise only allows access from clients in the same region as the internal load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#allow_global_access GoogleComputeForwardingRule#allow_global_access}
        :param allow_psc_global_access: This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#allow_psc_global_access GoogleComputeForwardingRule#allow_psc_global_access}
        :param all_ports: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'allPorts' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, SCTP, or L3_DEFAULT. - It's applicable only to the following products: internal passthrough Network Load Balancers, backend service-based external passthrough Network Load Balancers, and internal and external protocol forwarding. - Set this field to true to allow packets addressed to any port or packets lacking destination port information (for example, UDP fragments after the first fragment) to be forwarded to the backends configured with this forwarding rule. The L3_DEFAULT protocol requires 'allPorts' be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#all_ports GoogleComputeForwardingRule#all_ports}
        :param backend_service: Identifies the backend service to which the forwarding rule sends traffic. Required for Internal TCP/UDP Load Balancing and Network Load Balancing; must be omitted for all other load balancer types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#backend_service GoogleComputeForwardingRule#backend_service}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#description GoogleComputeForwardingRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#id GoogleComputeForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced 'target' or 'backendService'. While creating a forwarding rule, specifying an 'IPAddress' is required under the following circumstances: - When the 'target' is set to 'targetGrpcProxy' and 'validateForProxyless' is set to 'true', the 'IPAddress' should be set to '0.0.0.0'. - When the 'target' is a Private Service Connect Google APIs bundle, you must specify an 'IPAddress'. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: - IP address number, as in '100.1.2.3' - IPv6 address range, as in '2600:1234::/96' - Full resource URL, as in 'https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name' - Partial URL or by name, as in: - 'projects/project_id/regions/region/addresses/address-name' - 'regions/region/addresses/address-name' - 'global/addresses/address-name' - 'address-name' The forwarding rule's 'target' or 'backendService', and in most cases, also the 'loadBalancingScheme', determine the type of IP address that you can use. For detailed information, see `IP address specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. When reading an 'IPAddress', the API always returns the IP address number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_address GoogleComputeForwardingRule#ip_address}
        :param ip_collection: Resource reference of a PublicDelegatedPrefix. The PDP must be a sub-PDP in EXTERNAL_IPV6_FORWARDING_RULE_CREATION mode. Use one of the following formats to specify a sub-PDP when creating an IPv6 NetLB forwarding rule using BYOIP: Full resource URL, as in: - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Partial URL, as in: - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}' - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_collection GoogleComputeForwardingRule#ip_collection}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are 'TCP', 'UDP', 'ESP', 'AH', 'SCTP', 'ICMP' and 'L3_DEFAULT'. The valid IP protocols are different for different load balancing products as described in `Load balancing features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_. A Forwarding Rule with protocol L3_DEFAULT can attach with target instance or backend service with UNSPECIFIED protocol. A forwarding rule with "L3_DEFAULT" IPProtocal cannot be attached to a backend service with TCP or UDP. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP", "L3_DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_protocol GoogleComputeForwardingRule#ip_protocol}
        :param ip_version: The IP address version that will be used by this forwarding rule. Valid options are IPV4 and IPV6. If not set, the IPv4 address will be used by default. Possible values: ["IPV4", "IPV6"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_version GoogleComputeForwardingRule#ip_version}
        :param is_mirroring_collector: Indicates whether or not this load balancer can be used as a collector for packet mirroring. To prevent mirroring loops, instances behind this load balancer will not have their traffic mirrored even if a 'PacketMirroring' rule applies to them. This can only be set to true for load balancers that have their 'loadBalancingScheme' set to 'INTERNAL'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#is_mirroring_collector GoogleComputeForwardingRule#is_mirroring_collector}
        :param labels: Labels to apply to this forwarding rule. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#labels GoogleComputeForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. Note that an empty string value ('""') is also supported for some use cases, for example PSC (private service connection) regional forwarding rules. For more information about forwarding rules, refer to `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#load_balancing_scheme GoogleComputeForwardingRule#load_balancing_scheme}
        :param network: This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If the subnetwork is specified, the network of the subnetwork will be used. If neither subnetwork nor this field is specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#network GoogleComputeForwardingRule#network}
        :param network_tier: This signifies the networking tier used for configuring this load balancer and can only take the following values: 'PREMIUM', 'STANDARD'. For regional ForwardingRule, the valid values are 'PREMIUM' and 'STANDARD'. For GlobalForwardingRule, the valid value is 'PREMIUM'. If this field is not specified, it is assumed to be 'PREMIUM'. If 'IPAddress' is specified, this value must be equal to the networkTier of the Address. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#network_tier GoogleComputeForwardingRule#network_tier}
        :param no_automate_dns_zone: This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#no_automate_dns_zone GoogleComputeForwardingRule#no_automate_dns_zone}
        :param port_range: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'portRange' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and - It's applicable only to the following products: external passthrough Network Load Balancers, internal and external proxy Network Load Balancers, internal and external Application Load Balancers, external protocol forwarding, and Classic VPN. - Some products have restrictions on what ports can be used. See `port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications>`_ for details. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's.
        :param ports: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'ports' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and - It's applicable only to the following products: internal passthrough Network Load Balancers, backend service-based external passthrough Network Load Balancers, and internal protocol forwarding. - You can specify a list of up to five ports by number, separated by commas. The ports can be contiguous or discontiguous. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair if they share at least one port number. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair if they share at least one port number.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#project GoogleComputeForwardingRule#project}.
        :param recreate_closed_psc: This is used in PSC consumer ForwardingRule to make terraform recreate the ForwardingRule when the status is closed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#recreate_closed_psc GoogleComputeForwardingRule#recreate_closed_psc}
        :param region: A reference to the region where the regional forwarding rule resides. This field is not applicable to global forwarding rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#region GoogleComputeForwardingRule#region}
        :param service_directory_registrations: service_directory_registrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#service_directory_registrations GoogleComputeForwardingRule#service_directory_registrations}
        :param service_label: An optional prefix to the service name for this Forwarding Rule. If specified, will be the first label of the fully qualified service name. The label must be 1-63 characters long, and comply with RFC1035. Specifically, the label must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. This field is only used for INTERNAL load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#service_label GoogleComputeForwardingRule#service_label}
        :param source_ip_ranges: If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here. Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#source_ip_ranges GoogleComputeForwardingRule#source_ip_ranges}
        :param subnetwork: This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#subnetwork GoogleComputeForwardingRule#subnetwork}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. - For load balancers, see the "Target" column in `Port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - 'vpc-sc' - ` APIs that support VPC Service Controls <https://cloud.google.com/vpc-service-controls/docs/supported-products>`_. - 'all-apis' - `All supported Google APIs <https://cloud.google.com/vpc/docs/private-service-connect#supported-apis>`_. For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#target GoogleComputeForwardingRule#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#timeouts GoogleComputeForwardingRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbba47e9ae1a7b4cfdd0e4ab24cc4a141e8b5458793f425d19ddb76b13c36981)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeForwardingRuleConfig(
            name=name,
            allow_global_access=allow_global_access,
            allow_psc_global_access=allow_psc_global_access,
            all_ports=all_ports,
            backend_service=backend_service,
            description=description,
            id=id,
            ip_address=ip_address,
            ip_collection=ip_collection,
            ip_protocol=ip_protocol,
            ip_version=ip_version,
            is_mirroring_collector=is_mirroring_collector,
            labels=labels,
            load_balancing_scheme=load_balancing_scheme,
            network=network,
            network_tier=network_tier,
            no_automate_dns_zone=no_automate_dns_zone,
            port_range=port_range,
            ports=ports,
            project=project,
            recreate_closed_psc=recreate_closed_psc,
            region=region,
            service_directory_registrations=service_directory_registrations,
            service_label=service_label,
            source_ip_ranges=source_ip_ranges,
            subnetwork=subnetwork,
            target=target,
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
        '''Generates CDKTF code for importing a GoogleComputeForwardingRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeForwardingRule to import.
        :param import_from_id: The id of the existing GoogleComputeForwardingRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeForwardingRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__803feb8e8a673c57f80d01e9cff70b243a960105e37e433edab82e117bce7df3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putServiceDirectoryRegistrations")
    def put_service_directory_registrations(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace: Service Directory namespace to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#namespace GoogleComputeForwardingRule#namespace}
        :param service: Service Directory service to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#service GoogleComputeForwardingRule#service}
        '''
        value = GoogleComputeForwardingRuleServiceDirectoryRegistrations(
            namespace=namespace, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryRegistrations", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#create GoogleComputeForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#delete GoogleComputeForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#update GoogleComputeForwardingRule#update}.
        '''
        value = GoogleComputeForwardingRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowGlobalAccess")
    def reset_allow_global_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowGlobalAccess", []))

    @jsii.member(jsii_name="resetAllowPscGlobalAccess")
    def reset_allow_psc_global_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowPscGlobalAccess", []))

    @jsii.member(jsii_name="resetAllPorts")
    def reset_all_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllPorts", []))

    @jsii.member(jsii_name="resetBackendService")
    def reset_backend_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendService", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetIpCollection")
    def reset_ip_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpCollection", []))

    @jsii.member(jsii_name="resetIpProtocol")
    def reset_ip_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpProtocol", []))

    @jsii.member(jsii_name="resetIpVersion")
    def reset_ip_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpVersion", []))

    @jsii.member(jsii_name="resetIsMirroringCollector")
    def reset_is_mirroring_collector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsMirroringCollector", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLoadBalancingScheme")
    def reset_load_balancing_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingScheme", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkTier")
    def reset_network_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkTier", []))

    @jsii.member(jsii_name="resetNoAutomateDnsZone")
    def reset_no_automate_dns_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoAutomateDnsZone", []))

    @jsii.member(jsii_name="resetPortRange")
    def reset_port_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortRange", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRecreateClosedPsc")
    def reset_recreate_closed_psc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecreateClosedPsc", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetServiceDirectoryRegistrations")
    def reset_service_directory_registrations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryRegistrations", []))

    @jsii.member(jsii_name="resetServiceLabel")
    def reset_service_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceLabel", []))

    @jsii.member(jsii_name="resetSourceIpRanges")
    def reset_source_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceIpRanges", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

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
    @jsii.member(jsii_name="baseForwardingRule")
    def base_forwarding_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseForwardingRule"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="forwardingRuleId")
    def forwarding_rule_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "forwardingRuleId"))

    @builtins.property
    @jsii.member(jsii_name="labelFingerprint")
    def label_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionStatus")
    def psc_connection_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionStatus"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryRegistrations")
    def service_directory_registrations(
        self,
    ) -> "GoogleComputeForwardingRuleServiceDirectoryRegistrationsOutputReference":
        return typing.cast("GoogleComputeForwardingRuleServiceDirectoryRegistrationsOutputReference", jsii.get(self, "serviceDirectoryRegistrations"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeForwardingRuleTimeoutsOutputReference":
        return typing.cast("GoogleComputeForwardingRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allowGlobalAccessInput")
    def allow_global_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowGlobalAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="allowPscGlobalAccessInput")
    def allow_psc_global_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowPscGlobalAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="allPortsInput")
    def all_ports_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="backendServiceInput")
    def backend_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipCollectionInput")
    def ip_collection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipCollectionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="ipVersionInput")
    def ip_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="isMirroringCollectorInput")
    def is_mirroring_collector_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isMirroringCollectorInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingSchemeInput")
    def load_balancing_scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingSchemeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTierInput")
    def network_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTierInput"))

    @builtins.property
    @jsii.member(jsii_name="noAutomateDnsZoneInput")
    def no_automate_dns_zone_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noAutomateDnsZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="portRangeInput")
    def port_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="recreateClosedPscInput")
    def recreate_closed_psc_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recreateClosedPscInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryRegistrationsInput")
    def service_directory_registrations_input(
        self,
    ) -> typing.Optional["GoogleComputeForwardingRuleServiceDirectoryRegistrations"]:
        return typing.cast(typing.Optional["GoogleComputeForwardingRuleServiceDirectoryRegistrations"], jsii.get(self, "serviceDirectoryRegistrationsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceLabelInput")
    def service_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIpRangesInput")
    def source_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeForwardingRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeForwardingRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowGlobalAccess")
    def allow_global_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowGlobalAccess"))

    @allow_global_access.setter
    def allow_global_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e160b60bb1d55bda357a270a744349df5a78439571383bd04b23a2c1dcc1ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowGlobalAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowPscGlobalAccess")
    def allow_psc_global_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowPscGlobalAccess"))

    @allow_psc_global_access.setter
    def allow_psc_global_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f38e9a9852195303eb075d5d3ed5e2fff47a3c6831f475914a25ac527c577e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowPscGlobalAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allPorts")
    def all_ports(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allPorts"))

    @all_ports.setter
    def all_ports(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3a0799ae504e33e235628fc7b5e07998329ccc97901e9e615bc7d2f653385f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backendService")
    def backend_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendService"))

    @backend_service.setter
    def backend_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe07321261a937d147dae839026142400cc0096ca047454fe8004bf1e9c8cd80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef12db98376a1c4908d02275ff8063338158a761e3223cd5d7397e55aa577390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c18f70bd52d85f96618ed464344d29c425949cb55a17a071e497d5364d55fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac579707a47bf7cb4c0bc632d3e0a49acd8d4aca2140e6215504b49163827968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipCollection")
    def ip_collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCollection"))

    @ip_collection.setter
    def ip_collection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0dbca54da994dde21612f2e59519c66b947d51f95b070093eacd195eaa42635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCollection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a85b5c8ccf31a3f72db30e1e3f65dd8a3e248c0a305916c35d24080f558938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipVersion")
    def ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipVersion"))

    @ip_version.setter
    def ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d040e42e3e1baf4679c550b1f61867de7e9416f115b9d78cfc24afc9eb264468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isMirroringCollector")
    def is_mirroring_collector(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isMirroringCollector"))

    @is_mirroring_collector.setter
    def is_mirroring_collector(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bbfab9c27d664e521a0936e61583c7679bd8f876807f8ae424ac86d0cc42dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isMirroringCollector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a9f0f560ad82cb991dd99d9c9fc07674424c4eb420295921834b1a2b0611e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93482362372720fb928396b5ac53a71dc5b25a6e983de86f94c576963b2bacc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a76361f70d7e263a51fcc22327b8d00c5cf059c8a9c90501b72f2ec45bfa2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c14d0dcf27ba1fdde5ce22da3f967a486158d869faf3d20ac024af6937f92f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8c67feeed2dc093607b03904f5c89f693ac24fc8c070392bd295033ffde322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noAutomateDnsZone")
    def no_automate_dns_zone(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noAutomateDnsZone"))

    @no_automate_dns_zone.setter
    def no_automate_dns_zone(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf8d11d4333ad894a3c5706dcf86d46508ec2355921fed1a30c7589d695ec62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAutomateDnsZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portRange")
    def port_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portRange"))

    @port_range.setter
    def port_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb821e2fd1da6e0b93dbeff2b51b3e28a1c65a1b4ea961175992148185edf2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8284e772d8f90abec692f99f75ef69e5494095f62602fcefcda3971c6b9aac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3de9a3c70a8f55288062a1ea54fba8eab3b0ad19d959c8cf6b7f93d46ecaafe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recreateClosedPsc")
    def recreate_closed_psc(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recreateClosedPsc"))

    @recreate_closed_psc.setter
    def recreate_closed_psc(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b380afcf2720bc5ffa7f918323821d9bfbd551a8cad3655530e3d33ba175d161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recreateClosedPsc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ad329be02f1b5a6f62a889a21613e2435f16068255b36d8940839486e433f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceLabel")
    def service_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLabel"))

    @service_label.setter
    def service_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041921e5386b28461869575fa3607c9251eef089c3eed5ce33ce93127d5ce3a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceIpRanges")
    def source_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceIpRanges"))

    @source_ip_ranges.setter
    def source_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a9eb2ceb07de49878575abc67c22dc60bd41a03b6c347bb4ec8e6d3cc4f234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957e48225f0090fe3206d0b5a9870186f128d97ace6d9e14c7a40809045d3122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a784ace60347f0c09739b4100a86290097da410505683da522ca9289c17c9e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeForwardingRule.GoogleComputeForwardingRuleConfig",
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
        "allow_global_access": "allowGlobalAccess",
        "allow_psc_global_access": "allowPscGlobalAccess",
        "all_ports": "allPorts",
        "backend_service": "backendService",
        "description": "description",
        "id": "id",
        "ip_address": "ipAddress",
        "ip_collection": "ipCollection",
        "ip_protocol": "ipProtocol",
        "ip_version": "ipVersion",
        "is_mirroring_collector": "isMirroringCollector",
        "labels": "labels",
        "load_balancing_scheme": "loadBalancingScheme",
        "network": "network",
        "network_tier": "networkTier",
        "no_automate_dns_zone": "noAutomateDnsZone",
        "port_range": "portRange",
        "ports": "ports",
        "project": "project",
        "recreate_closed_psc": "recreateClosedPsc",
        "region": "region",
        "service_directory_registrations": "serviceDirectoryRegistrations",
        "service_label": "serviceLabel",
        "source_ip_ranges": "sourceIpRanges",
        "subnetwork": "subnetwork",
        "target": "target",
        "timeouts": "timeouts",
    },
)
class GoogleComputeForwardingRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allow_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_psc_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        all_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_service: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ip_collection: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[builtins.str] = None,
        is_mirroring_collector: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
        no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port_range: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        recreate_closed_psc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        service_directory_registrations: typing.Optional[typing.Union["GoogleComputeForwardingRuleServiceDirectoryRegistrations", typing.Dict[builtins.str, typing.Any]]] = None,
        service_label: typing.Optional[builtins.str] = None,
        source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. For Private Service Connect forwarding rules that forward traffic to Google APIs, the forwarding rule name must be a 1-20 characters string with lowercase letters and numbers and must start with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#name GoogleComputeForwardingRule#name}
        :param allow_global_access: This field is used along with the 'backend_service' field for internal load balancing or with the 'target' field for internal TargetInstance. If the field is set to 'TRUE', clients can access ILB from all regions. Otherwise only allows access from clients in the same region as the internal load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#allow_global_access GoogleComputeForwardingRule#allow_global_access}
        :param allow_psc_global_access: This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#allow_psc_global_access GoogleComputeForwardingRule#allow_psc_global_access}
        :param all_ports: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'allPorts' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, SCTP, or L3_DEFAULT. - It's applicable only to the following products: internal passthrough Network Load Balancers, backend service-based external passthrough Network Load Balancers, and internal and external protocol forwarding. - Set this field to true to allow packets addressed to any port or packets lacking destination port information (for example, UDP fragments after the first fragment) to be forwarded to the backends configured with this forwarding rule. The L3_DEFAULT protocol requires 'allPorts' be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#all_ports GoogleComputeForwardingRule#all_ports}
        :param backend_service: Identifies the backend service to which the forwarding rule sends traffic. Required for Internal TCP/UDP Load Balancing and Network Load Balancing; must be omitted for all other load balancer types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#backend_service GoogleComputeForwardingRule#backend_service}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#description GoogleComputeForwardingRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#id GoogleComputeForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced 'target' or 'backendService'. While creating a forwarding rule, specifying an 'IPAddress' is required under the following circumstances: - When the 'target' is set to 'targetGrpcProxy' and 'validateForProxyless' is set to 'true', the 'IPAddress' should be set to '0.0.0.0'. - When the 'target' is a Private Service Connect Google APIs bundle, you must specify an 'IPAddress'. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: - IP address number, as in '100.1.2.3' - IPv6 address range, as in '2600:1234::/96' - Full resource URL, as in 'https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name' - Partial URL or by name, as in: - 'projects/project_id/regions/region/addresses/address-name' - 'regions/region/addresses/address-name' - 'global/addresses/address-name' - 'address-name' The forwarding rule's 'target' or 'backendService', and in most cases, also the 'loadBalancingScheme', determine the type of IP address that you can use. For detailed information, see `IP address specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. When reading an 'IPAddress', the API always returns the IP address number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_address GoogleComputeForwardingRule#ip_address}
        :param ip_collection: Resource reference of a PublicDelegatedPrefix. The PDP must be a sub-PDP in EXTERNAL_IPV6_FORWARDING_RULE_CREATION mode. Use one of the following formats to specify a sub-PDP when creating an IPv6 NetLB forwarding rule using BYOIP: Full resource URL, as in: - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Partial URL, as in: - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}' - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_collection GoogleComputeForwardingRule#ip_collection}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are 'TCP', 'UDP', 'ESP', 'AH', 'SCTP', 'ICMP' and 'L3_DEFAULT'. The valid IP protocols are different for different load balancing products as described in `Load balancing features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_. A Forwarding Rule with protocol L3_DEFAULT can attach with target instance or backend service with UNSPECIFIED protocol. A forwarding rule with "L3_DEFAULT" IPProtocal cannot be attached to a backend service with TCP or UDP. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP", "L3_DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_protocol GoogleComputeForwardingRule#ip_protocol}
        :param ip_version: The IP address version that will be used by this forwarding rule. Valid options are IPV4 and IPV6. If not set, the IPv4 address will be used by default. Possible values: ["IPV4", "IPV6"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_version GoogleComputeForwardingRule#ip_version}
        :param is_mirroring_collector: Indicates whether or not this load balancer can be used as a collector for packet mirroring. To prevent mirroring loops, instances behind this load balancer will not have their traffic mirrored even if a 'PacketMirroring' rule applies to them. This can only be set to true for load balancers that have their 'loadBalancingScheme' set to 'INTERNAL'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#is_mirroring_collector GoogleComputeForwardingRule#is_mirroring_collector}
        :param labels: Labels to apply to this forwarding rule. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#labels GoogleComputeForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. Note that an empty string value ('""') is also supported for some use cases, for example PSC (private service connection) regional forwarding rules. For more information about forwarding rules, refer to `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#load_balancing_scheme GoogleComputeForwardingRule#load_balancing_scheme}
        :param network: This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If the subnetwork is specified, the network of the subnetwork will be used. If neither subnetwork nor this field is specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#network GoogleComputeForwardingRule#network}
        :param network_tier: This signifies the networking tier used for configuring this load balancer and can only take the following values: 'PREMIUM', 'STANDARD'. For regional ForwardingRule, the valid values are 'PREMIUM' and 'STANDARD'. For GlobalForwardingRule, the valid value is 'PREMIUM'. If this field is not specified, it is assumed to be 'PREMIUM'. If 'IPAddress' is specified, this value must be equal to the networkTier of the Address. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#network_tier GoogleComputeForwardingRule#network_tier}
        :param no_automate_dns_zone: This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#no_automate_dns_zone GoogleComputeForwardingRule#no_automate_dns_zone}
        :param port_range: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'portRange' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and - It's applicable only to the following products: external passthrough Network Load Balancers, internal and external proxy Network Load Balancers, internal and external Application Load Balancers, external protocol forwarding, and Classic VPN. - Some products have restrictions on what ports can be used. See `port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications>`_ for details. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's.
        :param ports: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'ports' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and - It's applicable only to the following products: internal passthrough Network Load Balancers, backend service-based external passthrough Network Load Balancers, and internal protocol forwarding. - You can specify a list of up to five ports by number, separated by commas. The ports can be contiguous or discontiguous. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair if they share at least one port number. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair if they share at least one port number.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#project GoogleComputeForwardingRule#project}.
        :param recreate_closed_psc: This is used in PSC consumer ForwardingRule to make terraform recreate the ForwardingRule when the status is closed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#recreate_closed_psc GoogleComputeForwardingRule#recreate_closed_psc}
        :param region: A reference to the region where the regional forwarding rule resides. This field is not applicable to global forwarding rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#region GoogleComputeForwardingRule#region}
        :param service_directory_registrations: service_directory_registrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#service_directory_registrations GoogleComputeForwardingRule#service_directory_registrations}
        :param service_label: An optional prefix to the service name for this Forwarding Rule. If specified, will be the first label of the fully qualified service name. The label must be 1-63 characters long, and comply with RFC1035. Specifically, the label must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. This field is only used for INTERNAL load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#service_label GoogleComputeForwardingRule#service_label}
        :param source_ip_ranges: If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here. Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#source_ip_ranges GoogleComputeForwardingRule#source_ip_ranges}
        :param subnetwork: This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#subnetwork GoogleComputeForwardingRule#subnetwork}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. - For load balancers, see the "Target" column in `Port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - 'vpc-sc' - ` APIs that support VPC Service Controls <https://cloud.google.com/vpc-service-controls/docs/supported-products>`_. - 'all-apis' - `All supported Google APIs <https://cloud.google.com/vpc/docs/private-service-connect#supported-apis>`_. For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#target GoogleComputeForwardingRule#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#timeouts GoogleComputeForwardingRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(service_directory_registrations, dict):
            service_directory_registrations = GoogleComputeForwardingRuleServiceDirectoryRegistrations(**service_directory_registrations)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeForwardingRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e6336a5178d3dc24ac5167117e25791933547fd8bd11839e9b4bd0ad62b634)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_global_access", value=allow_global_access, expected_type=type_hints["allow_global_access"])
            check_type(argname="argument allow_psc_global_access", value=allow_psc_global_access, expected_type=type_hints["allow_psc_global_access"])
            check_type(argname="argument all_ports", value=all_ports, expected_type=type_hints["all_ports"])
            check_type(argname="argument backend_service", value=backend_service, expected_type=type_hints["backend_service"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_collection", value=ip_collection, expected_type=type_hints["ip_collection"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument ip_version", value=ip_version, expected_type=type_hints["ip_version"])
            check_type(argname="argument is_mirroring_collector", value=is_mirroring_collector, expected_type=type_hints["is_mirroring_collector"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument load_balancing_scheme", value=load_balancing_scheme, expected_type=type_hints["load_balancing_scheme"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_tier", value=network_tier, expected_type=type_hints["network_tier"])
            check_type(argname="argument no_automate_dns_zone", value=no_automate_dns_zone, expected_type=type_hints["no_automate_dns_zone"])
            check_type(argname="argument port_range", value=port_range, expected_type=type_hints["port_range"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument recreate_closed_psc", value=recreate_closed_psc, expected_type=type_hints["recreate_closed_psc"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument service_directory_registrations", value=service_directory_registrations, expected_type=type_hints["service_directory_registrations"])
            check_type(argname="argument service_label", value=service_label, expected_type=type_hints["service_label"])
            check_type(argname="argument source_ip_ranges", value=source_ip_ranges, expected_type=type_hints["source_ip_ranges"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
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
        if allow_global_access is not None:
            self._values["allow_global_access"] = allow_global_access
        if allow_psc_global_access is not None:
            self._values["allow_psc_global_access"] = allow_psc_global_access
        if all_ports is not None:
            self._values["all_ports"] = all_ports
        if backend_service is not None:
            self._values["backend_service"] = backend_service
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if ip_collection is not None:
            self._values["ip_collection"] = ip_collection
        if ip_protocol is not None:
            self._values["ip_protocol"] = ip_protocol
        if ip_version is not None:
            self._values["ip_version"] = ip_version
        if is_mirroring_collector is not None:
            self._values["is_mirroring_collector"] = is_mirroring_collector
        if labels is not None:
            self._values["labels"] = labels
        if load_balancing_scheme is not None:
            self._values["load_balancing_scheme"] = load_balancing_scheme
        if network is not None:
            self._values["network"] = network
        if network_tier is not None:
            self._values["network_tier"] = network_tier
        if no_automate_dns_zone is not None:
            self._values["no_automate_dns_zone"] = no_automate_dns_zone
        if port_range is not None:
            self._values["port_range"] = port_range
        if ports is not None:
            self._values["ports"] = ports
        if project is not None:
            self._values["project"] = project
        if recreate_closed_psc is not None:
            self._values["recreate_closed_psc"] = recreate_closed_psc
        if region is not None:
            self._values["region"] = region
        if service_directory_registrations is not None:
            self._values["service_directory_registrations"] = service_directory_registrations
        if service_label is not None:
            self._values["service_label"] = service_label
        if source_ip_ranges is not None:
            self._values["source_ip_ranges"] = source_ip_ranges
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if target is not None:
            self._values["target"] = target
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
        '''Name of the resource;

        provided by the client when the resource is created.
        The name must be 1-63 characters long, and comply with
        `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_.

        Specifically, the name must be 1-63 characters long and match the regular
        expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first
        character must be a lowercase letter, and all following characters must
        be a dash, lowercase letter, or digit, except the last character, which
        cannot be a dash.

        For Private Service Connect forwarding rules that forward traffic to Google
        APIs, the forwarding rule name must be a 1-20 characters string with
        lowercase letters and numbers and must start with a letter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#name GoogleComputeForwardingRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_global_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field is used along with the 'backend_service' field for internal load balancing or with the 'target' field for internal TargetInstance.

        If the field is set to 'TRUE', clients can access ILB from all
        regions.

        Otherwise only allows access from clients in the same region as the
        internal load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#allow_global_access GoogleComputeForwardingRule#allow_global_access}
        '''
        result = self._values.get("allow_global_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_psc_global_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#allow_psc_global_access GoogleComputeForwardingRule#allow_psc_global_access}
        '''
        result = self._values.get("allow_psc_global_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def all_ports(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive.

        Only packets addressed to ports in the specified range will be forwarded
        to the backends configured with this forwarding rule.

        The 'allPorts' field has the following limitations:

        - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, SCTP, or
          L3_DEFAULT.
        - It's applicable only to the following products: internal passthrough
          Network Load Balancers, backend service-based external passthrough Network
          Load Balancers, and internal and external protocol forwarding.
        - Set this field to true to allow packets addressed to any port or packets
          lacking destination port information (for example, UDP fragments after the
          first fragment) to be forwarded to the backends configured with this
          forwarding rule. The L3_DEFAULT protocol requires 'allPorts' be set to
          true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#all_ports GoogleComputeForwardingRule#all_ports}
        '''
        result = self._values.get("all_ports")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backend_service(self) -> typing.Optional[builtins.str]:
        '''Identifies the backend service to which the forwarding rule sends traffic.

        Required for Internal TCP/UDP Load Balancing and Network Load Balancing;
        must be omitted for all other load balancer types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#backend_service GoogleComputeForwardingRule#backend_service}
        '''
        result = self._values.get("backend_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#description GoogleComputeForwardingRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#id GoogleComputeForwardingRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''IP address for which this forwarding rule accepts traffic.

        When a client
        sends traffic to this IP address, the forwarding rule directs the traffic
        to the referenced 'target' or 'backendService'.

        While creating a forwarding rule, specifying an 'IPAddress' is
        required under the following circumstances:

        - When the 'target' is set to 'targetGrpcProxy' and
          'validateForProxyless' is set to 'true', the
          'IPAddress' should be set to '0.0.0.0'.
        - When the 'target' is a Private Service Connect Google APIs
          bundle, you must specify an 'IPAddress'.

        Otherwise, you can optionally specify an IP address that references an
        existing static (reserved) IP address resource. When omitted, Google Cloud
        assigns an ephemeral IP address.

        Use one of the following formats to specify an IP address while creating a
        forwarding rule:

        - IP address number, as in '100.1.2.3'
        - IPv6 address range, as in '2600:1234::/96'
        - Full resource URL, as in
          'https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name'
        - Partial URL or by name, as in:

          - 'projects/project_id/regions/region/addresses/address-name'
          - 'regions/region/addresses/address-name'
          - 'global/addresses/address-name'
          - 'address-name'

        The forwarding rule's 'target' or 'backendService',
        and in most cases, also the 'loadBalancingScheme', determine the
        type of IP address that you can use. For detailed information, see
        `IP address
        specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_.

        When reading an 'IPAddress', the API always returns the IP
        address number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_address GoogleComputeForwardingRule#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_collection(self) -> typing.Optional[builtins.str]:
        '''Resource reference of a PublicDelegatedPrefix.

        The PDP must be a sub-PDP
        in EXTERNAL_IPV6_FORWARDING_RULE_CREATION mode.
        Use one of the following formats to specify a sub-PDP when creating an
        IPv6 NetLB forwarding rule using BYOIP:
        Full resource URL, as in:

        - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}'
          Partial URL, as in:
        - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}'
        - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_collection GoogleComputeForwardingRule#ip_collection}
        '''
        result = self._values.get("ip_collection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_protocol(self) -> typing.Optional[builtins.str]:
        '''The IP protocol to which this rule applies.

        For protocol forwarding, valid
        options are 'TCP', 'UDP', 'ESP',
        'AH', 'SCTP', 'ICMP' and
        'L3_DEFAULT'.

        The valid IP protocols are different for different load balancing products
        as described in `Load balancing
        features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_.

        A Forwarding Rule with protocol L3_DEFAULT can attach with target instance or
        backend service with UNSPECIFIED protocol.
        A forwarding rule with "L3_DEFAULT" IPProtocal cannot be attached to a backend service with TCP or UDP. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP", "L3_DEFAULT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_protocol GoogleComputeForwardingRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_version(self) -> typing.Optional[builtins.str]:
        '''The IP address version that will be used by this forwarding rule. Valid options are IPV4 and IPV6.

        If not set, the IPv4 address will be used by default. Possible values: ["IPV4", "IPV6"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ip_version GoogleComputeForwardingRule#ip_version}
        '''
        result = self._values.get("ip_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_mirroring_collector(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether or not this load balancer can be used as a collector for packet mirroring.

        To prevent mirroring loops, instances behind this
        load balancer will not have their traffic mirrored even if a
        'PacketMirroring' rule applies to them.

        This can only be set to true for load balancers that have their
        'loadBalancingScheme' set to 'INTERNAL'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#is_mirroring_collector GoogleComputeForwardingRule#is_mirroring_collector}
        '''
        result = self._values.get("is_mirroring_collector")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this forwarding rule.  A list of key->value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#labels GoogleComputeForwardingRule#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''Specifies the forwarding rule type.

        Note that an empty string value ('""') is also supported for some use
        cases, for example PSC (private service connection) regional forwarding
        rules.

        For more information about forwarding rules, refer to
        `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#load_balancing_scheme GoogleComputeForwardingRule#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''This field is not used for external load balancing.

        For Internal TCP/UDP Load Balancing, this field identifies the network that
        the load balanced IP should belong to for this Forwarding Rule.
        If the subnetwork is specified, the network of the subnetwork will be used.
        If neither subnetwork nor this field is specified, the default network will
        be used.

        For Private Service Connect forwarding rules that forward traffic to Google
        APIs, a network must be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#network GoogleComputeForwardingRule#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tier(self) -> typing.Optional[builtins.str]:
        '''This signifies the networking tier used for configuring this load balancer and can only take the following values: 'PREMIUM', 'STANDARD'.

        For regional ForwardingRule, the valid values are 'PREMIUM' and
        'STANDARD'. For GlobalForwardingRule, the valid value is
        'PREMIUM'.

        If this field is not specified, it is assumed to be 'PREMIUM'.
        If 'IPAddress' is specified, this value must be equal to the
        networkTier of the Address. Possible values: ["PREMIUM", "STANDARD"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#network_tier GoogleComputeForwardingRule#network_tier}
        '''
        result = self._values.get("network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_automate_dns_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not.

        Non-PSC forwarding rules do not use this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#no_automate_dns_zone GoogleComputeForwardingRule#no_automate_dns_zone}
        '''
        result = self._values.get("no_automate_dns_zone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def port_range(self) -> typing.Optional[builtins.str]:
        '''The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive.

        Only packets addressed to ports in the specified range will be forwarded
        to the backends configured with this forwarding rule.

        The 'portRange' field has the following limitations:

        - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP,
          and
        - It's applicable only to the following products: external passthrough
          Network Load Balancers, internal and external proxy Network Load
          Balancers, internal and external Application Load Balancers, external
          protocol forwarding, and Classic VPN.
        - Some products have restrictions on what ports can be used. See
          `port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications>`_
          for details.

        For external forwarding rules, two or more forwarding rules cannot use the
        same '[IPAddress, IPProtocol]' pair, and cannot have overlapping
        'portRange's.

        For internal forwarding rules within the same VPC network, two or more
        forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and
        cannot have overlapping 'portRange's.

        :pattern:

        : \\d+(?:-\\d+)?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#port_range GoogleComputeForwardingRule#port_range}
        '''
        result = self._values.get("port_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive.

        Only packets addressed to ports in the specified range will be forwarded
        to the backends configured with this forwarding rule.

        The 'ports' field has the following limitations:

        - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP,
          and
        - It's applicable only to the following products: internal passthrough
          Network Load Balancers, backend service-based external passthrough Network
          Load Balancers, and internal protocol forwarding.
        - You can specify a list of up to five ports by number, separated by
          commas. The ports can be contiguous or discontiguous.

        For external forwarding rules, two or more forwarding rules cannot use the
        same '[IPAddress, IPProtocol]' pair if they share at least one port
        number.

        For internal forwarding rules within the same VPC network, two or more
        forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair if
        they share at least one port number.

        :pattern:

        : \\d+(?:-\\d+)?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#ports GoogleComputeForwardingRule#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#project GoogleComputeForwardingRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recreate_closed_psc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This is used in PSC consumer ForwardingRule to make terraform recreate the ForwardingRule when the status is closed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#recreate_closed_psc GoogleComputeForwardingRule#recreate_closed_psc}
        '''
        result = self._values.get("recreate_closed_psc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''A reference to the region where the regional forwarding rule resides.

        This field is not applicable to global forwarding rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#region GoogleComputeForwardingRule#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_registrations(
        self,
    ) -> typing.Optional["GoogleComputeForwardingRuleServiceDirectoryRegistrations"]:
        '''service_directory_registrations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#service_directory_registrations GoogleComputeForwardingRule#service_directory_registrations}
        '''
        result = self._values.get("service_directory_registrations")
        return typing.cast(typing.Optional["GoogleComputeForwardingRuleServiceDirectoryRegistrations"], result)

    @builtins.property
    def service_label(self) -> typing.Optional[builtins.str]:
        '''An optional prefix to the service name for this Forwarding Rule.

        If specified, will be the first label of the fully qualified service
        name.

        The label must be 1-63 characters long, and comply with RFC1035.
        Specifically, the label must be 1-63 characters long and match the
        regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first
        character must be a lowercase letter, and all following characters
        must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        This field is only used for INTERNAL load balancing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#service_label GoogleComputeForwardingRule#service_label}
        '''
        result = self._values.get("service_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here.

        Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#source_ip_ranges GoogleComputeForwardingRule#source_ip_ranges}
        '''
        result = self._values.get("source_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6.

        If the network specified is in auto subnet mode, this field is optional.
        However, a subnetwork must be specified if the network is in custom subnet
        mode or when creating external forwarding rule with IPv6.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#subnetwork GoogleComputeForwardingRule#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''The URL of the target resource to receive the matched traffic.

        For
        regional forwarding rules, this target must be in the same region as the
        forwarding rule. For global forwarding rules, this target must be a global
        load balancing resource.

        The forwarded traffic must be of a type appropriate to the target object.

        - For load balancers, see the "Target" column in `Port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_.
        - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle:
        - 'vpc-sc' - ` APIs that support VPC Service Controls <https://cloud.google.com/vpc-service-controls/docs/supported-products>`_.
        - 'all-apis' - `All supported Google APIs <https://cloud.google.com/vpc/docs/private-service-connect#supported-apis>`_.

        For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#target GoogleComputeForwardingRule#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeForwardingRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#timeouts GoogleComputeForwardingRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeForwardingRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeForwardingRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeForwardingRule.GoogleComputeForwardingRuleServiceDirectoryRegistrations",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace", "service": "service"},
)
class GoogleComputeForwardingRuleServiceDirectoryRegistrations:
    def __init__(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace: Service Directory namespace to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#namespace GoogleComputeForwardingRule#namespace}
        :param service: Service Directory service to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#service GoogleComputeForwardingRule#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2dbba088d3a2a7ea1e4bee9ff630397980fa54c17fa6ce051920a36a69dd4a)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if namespace is not None:
            self._values["namespace"] = namespace
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Service Directory namespace to register the forwarding rule under.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#namespace GoogleComputeForwardingRule#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Service Directory service to register the forwarding rule under.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#service GoogleComputeForwardingRule#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeForwardingRuleServiceDirectoryRegistrations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeForwardingRuleServiceDirectoryRegistrationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeForwardingRule.GoogleComputeForwardingRuleServiceDirectoryRegistrationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b2563e95cef41b6b3e5e8f47b8039045428500a317f52d500e3353f50feafd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b923a98b2a9d29c5e2dabbb01154ba2bf66433407ad234e33928f394c56815a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d443a93eca71bc3e44c8ab4f7027bd3e0ac25ffc8a279c3a4a5af8ef897d66a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeForwardingRuleServiceDirectoryRegistrations]:
        return typing.cast(typing.Optional[GoogleComputeForwardingRuleServiceDirectoryRegistrations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeForwardingRuleServiceDirectoryRegistrations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fdc64fba21592866194c6c338eb6ed7fda959344ed581bcfa0206937a3722d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeForwardingRule.GoogleComputeForwardingRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeForwardingRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#create GoogleComputeForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#delete GoogleComputeForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#update GoogleComputeForwardingRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8c9570475d2de7ab98eb26c9d429d4f48405e739fda39a0878219d00ac0c3e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#create GoogleComputeForwardingRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#delete GoogleComputeForwardingRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_forwarding_rule#update GoogleComputeForwardingRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeForwardingRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeForwardingRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeForwardingRule.GoogleComputeForwardingRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1992483a2b16e80452b6fbe7633d53d8acdfa678f2b2808052a207707900063)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e96938d438ddb565c637ef9161ae0685887fe630fa5c84c45584b090ed15ffc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7091b8c0bbb04a4b99ab886fb00dbe2590ef69fa7c33687f233c05888f7e9f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c58f90481b667814bf2ff031fdfda61cf9b9cf593a8f2459fc74508ead1dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeForwardingRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeForwardingRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeForwardingRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__156bb4a50d11296444f470cccf084aa1459f90aea5a3f914a1f19486e2305240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeForwardingRule",
    "GoogleComputeForwardingRuleConfig",
    "GoogleComputeForwardingRuleServiceDirectoryRegistrations",
    "GoogleComputeForwardingRuleServiceDirectoryRegistrationsOutputReference",
    "GoogleComputeForwardingRuleTimeouts",
    "GoogleComputeForwardingRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cbba47e9ae1a7b4cfdd0e4ab24cc4a141e8b5458793f425d19ddb76b13c36981(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    allow_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_psc_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    all_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backend_service: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ip_collection: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[builtins.str] = None,
    is_mirroring_collector: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
    no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port_range: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    recreate_closed_psc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    service_directory_registrations: typing.Optional[typing.Union[GoogleComputeForwardingRuleServiceDirectoryRegistrations, typing.Dict[builtins.str, typing.Any]]] = None,
    service_label: typing.Optional[builtins.str] = None,
    source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__803feb8e8a673c57f80d01e9cff70b243a960105e37e433edab82e117bce7df3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e160b60bb1d55bda357a270a744349df5a78439571383bd04b23a2c1dcc1ab2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f38e9a9852195303eb075d5d3ed5e2fff47a3c6831f475914a25ac527c577e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3a0799ae504e33e235628fc7b5e07998329ccc97901e9e615bc7d2f653385f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe07321261a937d147dae839026142400cc0096ca047454fe8004bf1e9c8cd80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef12db98376a1c4908d02275ff8063338158a761e3223cd5d7397e55aa577390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c18f70bd52d85f96618ed464344d29c425949cb55a17a071e497d5364d55fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac579707a47bf7cb4c0bc632d3e0a49acd8d4aca2140e6215504b49163827968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0dbca54da994dde21612f2e59519c66b947d51f95b070093eacd195eaa42635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a85b5c8ccf31a3f72db30e1e3f65dd8a3e248c0a305916c35d24080f558938(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d040e42e3e1baf4679c550b1f61867de7e9416f115b9d78cfc24afc9eb264468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bbfab9c27d664e521a0936e61583c7679bd8f876807f8ae424ac86d0cc42dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a9f0f560ad82cb991dd99d9c9fc07674424c4eb420295921834b1a2b0611e9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93482362372720fb928396b5ac53a71dc5b25a6e983de86f94c576963b2bacc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a76361f70d7e263a51fcc22327b8d00c5cf059c8a9c90501b72f2ec45bfa2ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c14d0dcf27ba1fdde5ce22da3f967a486158d869faf3d20ac024af6937f92f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8c67feeed2dc093607b03904f5c89f693ac24fc8c070392bd295033ffde322(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf8d11d4333ad894a3c5706dcf86d46508ec2355921fed1a30c7589d695ec62(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb821e2fd1da6e0b93dbeff2b51b3e28a1c65a1b4ea961175992148185edf2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8284e772d8f90abec692f99f75ef69e5494095f62602fcefcda3971c6b9aac1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3de9a3c70a8f55288062a1ea54fba8eab3b0ad19d959c8cf6b7f93d46ecaafe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b380afcf2720bc5ffa7f918323821d9bfbd551a8cad3655530e3d33ba175d161(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ad329be02f1b5a6f62a889a21613e2435f16068255b36d8940839486e433f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041921e5386b28461869575fa3607c9251eef089c3eed5ce33ce93127d5ce3a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a9eb2ceb07de49878575abc67c22dc60bd41a03b6c347bb4ec8e6d3cc4f234(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957e48225f0090fe3206d0b5a9870186f128d97ace6d9e14c7a40809045d3122(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a784ace60347f0c09739b4100a86290097da410505683da522ca9289c17c9e4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e6336a5178d3dc24ac5167117e25791933547fd8bd11839e9b4bd0ad62b634(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    allow_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_psc_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    all_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backend_service: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ip_collection: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[builtins.str] = None,
    is_mirroring_collector: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
    no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port_range: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    recreate_closed_psc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    service_directory_registrations: typing.Optional[typing.Union[GoogleComputeForwardingRuleServiceDirectoryRegistrations, typing.Dict[builtins.str, typing.Any]]] = None,
    service_label: typing.Optional[builtins.str] = None,
    source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2dbba088d3a2a7ea1e4bee9ff630397980fa54c17fa6ce051920a36a69dd4a(
    *,
    namespace: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2563e95cef41b6b3e5e8f47b8039045428500a317f52d500e3353f50feafd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b923a98b2a9d29c5e2dabbb01154ba2bf66433407ad234e33928f394c56815a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d443a93eca71bc3e44c8ab4f7027bd3e0ac25ffc8a279c3a4a5af8ef897d66a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdc64fba21592866194c6c338eb6ed7fda959344ed581bcfa0206937a3722d1(
    value: typing.Optional[GoogleComputeForwardingRuleServiceDirectoryRegistrations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8c9570475d2de7ab98eb26c9d429d4f48405e739fda39a0878219d00ac0c3e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1992483a2b16e80452b6fbe7633d53d8acdfa678f2b2808052a207707900063(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96938d438ddb565c637ef9161ae0685887fe630fa5c84c45584b090ed15ffc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7091b8c0bbb04a4b99ab886fb00dbe2590ef69fa7c33687f233c05888f7e9f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c58f90481b667814bf2ff031fdfda61cf9b9cf593a8f2459fc74508ead1dc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156bb4a50d11296444f470cccf084aa1459f90aea5a3f914a1f19486e2305240(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeForwardingRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
