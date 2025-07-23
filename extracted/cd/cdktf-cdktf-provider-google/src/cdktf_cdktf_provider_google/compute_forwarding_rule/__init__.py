r'''
# `google_compute_forwarding_rule`

Refer to the Terraform Registry for docs: [`google_compute_forwarding_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule).
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


class ComputeForwardingRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeForwardingRule.ComputeForwardingRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule google_compute_forwarding_rule}.'''

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
        service_directory_registrations: typing.Optional[typing.Union["ComputeForwardingRuleServiceDirectoryRegistrations", typing.Dict[builtins.str, typing.Any]]] = None,
        service_label: typing.Optional[builtins.str] = None,
        source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule google_compute_forwarding_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. For Private Service Connect forwarding rules that forward traffic to Google APIs, the forwarding rule name must be a 1-20 characters string with lowercase letters and numbers and must start with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#name ComputeForwardingRule#name}
        :param allow_global_access: This field is used along with the 'backend_service' field for internal load balancing or with the 'target' field for internal TargetInstance. If the field is set to 'TRUE', clients can access ILB from all regions. Otherwise only allows access from clients in the same region as the internal load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#allow_global_access ComputeForwardingRule#allow_global_access}
        :param allow_psc_global_access: This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#allow_psc_global_access ComputeForwardingRule#allow_psc_global_access}
        :param all_ports: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'allPorts' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, SCTP, or L3_DEFAULT. - It's applicable only to the following products: internal passthrough Network Load Balancers, backend service-based external passthrough Network Load Balancers, and internal and external protocol forwarding. - Set this field to true to allow packets addressed to any port or packets lacking destination port information (for example, UDP fragments after the first fragment) to be forwarded to the backends configured with this forwarding rule. The L3_DEFAULT protocol requires 'allPorts' be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#all_ports ComputeForwardingRule#all_ports}
        :param backend_service: Identifies the backend service to which the forwarding rule sends traffic. Required for Internal TCP/UDP Load Balancing and Network Load Balancing; must be omitted for all other load balancer types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#backend_service ComputeForwardingRule#backend_service}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#description ComputeForwardingRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#id ComputeForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced 'target' or 'backendService'. While creating a forwarding rule, specifying an 'IPAddress' is required under the following circumstances: - When the 'target' is set to 'targetGrpcProxy' and 'validateForProxyless' is set to 'true', the 'IPAddress' should be set to '0.0.0.0'. - When the 'target' is a Private Service Connect Google APIs bundle, you must specify an 'IPAddress'. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: - IP address number, as in '100.1.2.3' - IPv6 address range, as in '2600:1234::/96' - Full resource URL, as in 'https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name' - Partial URL or by name, as in: - 'projects/project_id/regions/region/addresses/address-name' - 'regions/region/addresses/address-name' - 'global/addresses/address-name' - 'address-name' The forwarding rule's 'target' or 'backendService', and in most cases, also the 'loadBalancingScheme', determine the type of IP address that you can use. For detailed information, see `IP address specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. When reading an 'IPAddress', the API always returns the IP address number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_address ComputeForwardingRule#ip_address}
        :param ip_collection: Resource reference of a PublicDelegatedPrefix. The PDP must be a sub-PDP in EXTERNAL_IPV6_FORWARDING_RULE_CREATION mode. Use one of the following formats to specify a sub-PDP when creating an IPv6 NetLB forwarding rule using BYOIP: Full resource URL, as in: - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Partial URL, as in: - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}' - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_collection ComputeForwardingRule#ip_collection}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are 'TCP', 'UDP', 'ESP', 'AH', 'SCTP', 'ICMP' and 'L3_DEFAULT'. The valid IP protocols are different for different load balancing products as described in `Load balancing features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_. A Forwarding Rule with protocol L3_DEFAULT can attach with target instance or backend service with UNSPECIFIED protocol. A forwarding rule with "L3_DEFAULT" IPProtocal cannot be attached to a backend service with TCP or UDP. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP", "L3_DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_protocol ComputeForwardingRule#ip_protocol}
        :param ip_version: The IP address version that will be used by this forwarding rule. Valid options are IPV4 and IPV6. If not set, the IPv4 address will be used by default. Possible values: ["IPV4", "IPV6"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_version ComputeForwardingRule#ip_version}
        :param is_mirroring_collector: Indicates whether or not this load balancer can be used as a collector for packet mirroring. To prevent mirroring loops, instances behind this load balancer will not have their traffic mirrored even if a 'PacketMirroring' rule applies to them. This can only be set to true for load balancers that have their 'loadBalancingScheme' set to 'INTERNAL'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#is_mirroring_collector ComputeForwardingRule#is_mirroring_collector}
        :param labels: Labels to apply to this forwarding rule. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#labels ComputeForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. Note that an empty string value ('""') is also supported for some use cases, for example PSC (private service connection) regional forwarding rules. For more information about forwarding rules, refer to `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#load_balancing_scheme ComputeForwardingRule#load_balancing_scheme}
        :param network: This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If the subnetwork is specified, the network of the subnetwork will be used. If neither subnetwork nor this field is specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#network ComputeForwardingRule#network}
        :param network_tier: This signifies the networking tier used for configuring this load balancer and can only take the following values: 'PREMIUM', 'STANDARD'. For regional ForwardingRule, the valid values are 'PREMIUM' and 'STANDARD'. For GlobalForwardingRule, the valid value is 'PREMIUM'. If this field is not specified, it is assumed to be 'PREMIUM'. If 'IPAddress' is specified, this value must be equal to the networkTier of the Address. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#network_tier ComputeForwardingRule#network_tier}
        :param no_automate_dns_zone: This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#no_automate_dns_zone ComputeForwardingRule#no_automate_dns_zone}
        :param port_range: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'portRange' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and - It's applicable only to the following products: external passthrough Network Load Balancers, internal and external proxy Network Load Balancers, internal and external Application Load Balancers, external protocol forwarding, and Classic VPN. - Some products have restrictions on what ports can be used. See `port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications>`_ for details. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's.
        :param ports: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'ports' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and - It's applicable only to the following products: internal passthrough Network Load Balancers, backend service-based external passthrough Network Load Balancers, and internal protocol forwarding. - You can specify a list of up to five ports by number, separated by commas. The ports can be contiguous or discontiguous. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair if they share at least one port number. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair if they share at least one port number.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#project ComputeForwardingRule#project}.
        :param recreate_closed_psc: This is used in PSC consumer ForwardingRule to make terraform recreate the ForwardingRule when the status is closed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#recreate_closed_psc ComputeForwardingRule#recreate_closed_psc}
        :param region: A reference to the region where the regional forwarding rule resides. This field is not applicable to global forwarding rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#region ComputeForwardingRule#region}
        :param service_directory_registrations: service_directory_registrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#service_directory_registrations ComputeForwardingRule#service_directory_registrations}
        :param service_label: An optional prefix to the service name for this Forwarding Rule. If specified, will be the first label of the fully qualified service name. The label must be 1-63 characters long, and comply with RFC1035. Specifically, the label must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. This field is only used for INTERNAL load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#service_label ComputeForwardingRule#service_label}
        :param source_ip_ranges: If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here. Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#source_ip_ranges ComputeForwardingRule#source_ip_ranges}
        :param subnetwork: This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#subnetwork ComputeForwardingRule#subnetwork}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. - For load balancers, see the "Target" column in `Port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - 'vpc-sc' - ` APIs that support VPC Service Controls <https://cloud.google.com/vpc-service-controls/docs/supported-products>`_. - 'all-apis' - `All supported Google APIs <https://cloud.google.com/vpc/docs/private-service-connect#supported-apis>`_. For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#target ComputeForwardingRule#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#timeouts ComputeForwardingRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7372c51506266c10431315b4fadc9d5bb288959f1095d4769bc18c78b6df2ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeForwardingRuleConfig(
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
        '''Generates CDKTF code for importing a ComputeForwardingRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeForwardingRule to import.
        :param import_from_id: The id of the existing ComputeForwardingRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeForwardingRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588e0409647f6f6cdaa8102ef80ea8e12ba42d38598b02cff6c838b27fdce009)
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
        :param namespace: Service Directory namespace to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#namespace ComputeForwardingRule#namespace}
        :param service: Service Directory service to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#service ComputeForwardingRule#service}
        '''
        value = ComputeForwardingRuleServiceDirectoryRegistrations(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#create ComputeForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#delete ComputeForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#update ComputeForwardingRule#update}.
        '''
        value = ComputeForwardingRuleTimeouts(
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
    ) -> "ComputeForwardingRuleServiceDirectoryRegistrationsOutputReference":
        return typing.cast("ComputeForwardingRuleServiceDirectoryRegistrationsOutputReference", jsii.get(self, "serviceDirectoryRegistrations"))

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
    def timeouts(self) -> "ComputeForwardingRuleTimeoutsOutputReference":
        return typing.cast("ComputeForwardingRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["ComputeForwardingRuleServiceDirectoryRegistrations"]:
        return typing.cast(typing.Optional["ComputeForwardingRuleServiceDirectoryRegistrations"], jsii.get(self, "serviceDirectoryRegistrationsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeForwardingRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeForwardingRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e83d9886930772e32eda3f83575bf6d632f5965e05edcda05dba098adb9c5cde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__679f5af44506fa2b0cb9fed7f128208217f022e45b23b8a93e5b0acd43053262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cab0ca698b77098182d9a555a854e451a0c8cfa39e1273842e7a23c70e4fbf25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backendService")
    def backend_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendService"))

    @backend_service.setter
    def backend_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7508a2948935d7dba425cbd2c96c06788615eb2272a566b0ec4191ff9fa71202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5982185346246925f47700b95339fe9171ed7da078bdaa3464ebf165c7bfa1c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffec22e27fba647b3bbb50b3022811ff49dc49e8ebeaf5d4b3953a9a1d424bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67013e041e8225d78fc23e4ab6d2b2a600b97be2a7ffc870bb7297ce20d6549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipCollection")
    def ip_collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCollection"))

    @ip_collection.setter
    def ip_collection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416ab50e468fca3e94ff4d27949857757a89f425dc10173fad21c1e792517ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCollection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7df2df98bd49c9a2a5d946d2f229a061a47b66ea9ac4e9d9b9b32d603dd9945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipVersion")
    def ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipVersion"))

    @ip_version.setter
    def ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e7c5618daf45d293499a6176c5c99276c1b3f99a754409156089b9a058b8c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1c6fc32531b8b1707bc4582f49e71f1471caca133bfe3bf48ee89ca76ab93c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isMirroringCollector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3aa58719523889649c21454fd13f76a2d17089b05b08a3dabba2ce72d1ec7e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69090430a1a759e85a3a132ffcc5f061b2b0312e9d6fe2bf9ad04e4aa72d049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6520c1ad58a1d8f1620710557a770bfab880d609f2f929ad40de2967e7364466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dded1f8fa8e2b73ff8d3ab2756ea83aba88d2e4f0a9b4d1cce79e2330762c4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc71406ec54e71bdbdbaa8bdcdff4e1b0e2bab5fd6496a3cf7d334bb3fa3e240)
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
            type_hints = typing.get_type_hints(_typecheckingstub__175869baefdbff8b4b36b0a12063a83447233c4efba7adfb84cc8501e677c3bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAutomateDnsZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portRange")
    def port_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portRange"))

    @port_range.setter
    def port_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64bbc049ff79795ed026b00d001cd54adb4815f1d6d678bbce0f2a8ffc6173d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567e1b0339f789e98f7d2643ae864daebcade2714cff7af149ae03cb77eb68ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4022f2e03f4b129034c9783730496075d0915e47f859480bc2dc82ac4a5ab7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38b41a8532d8c9cd7a6ad9e5cc2af69e418fc096661f698584328cca7dc66b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recreateClosedPsc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d324571bde6b9c49d78e6cd25cf6f03cf075a0a3fdbeb7c0b89980766832e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceLabel")
    def service_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLabel"))

    @service_label.setter
    def service_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77e479ce39d11eb2a4879e1eb665a9ab97ea25414578139c53994dde749c607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceIpRanges")
    def source_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceIpRanges"))

    @source_ip_ranges.setter
    def source_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704608146502e5feac9899c5665f68c981d6d661df3fdd56387843b6789b7b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754f75583218fdd71727da54c6a345385ea999110e039b3961866352bb6e0f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b235de770c8e921793c52c35166daa7e83a440e43dd8e648084e87fc5b17707e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeForwardingRule.ComputeForwardingRuleConfig",
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
class ComputeForwardingRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        service_directory_registrations: typing.Optional[typing.Union["ComputeForwardingRuleServiceDirectoryRegistrations", typing.Dict[builtins.str, typing.Any]]] = None,
        service_label: typing.Optional[builtins.str] = None,
        source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. For Private Service Connect forwarding rules that forward traffic to Google APIs, the forwarding rule name must be a 1-20 characters string with lowercase letters and numbers and must start with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#name ComputeForwardingRule#name}
        :param allow_global_access: This field is used along with the 'backend_service' field for internal load balancing or with the 'target' field for internal TargetInstance. If the field is set to 'TRUE', clients can access ILB from all regions. Otherwise only allows access from clients in the same region as the internal load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#allow_global_access ComputeForwardingRule#allow_global_access}
        :param allow_psc_global_access: This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#allow_psc_global_access ComputeForwardingRule#allow_psc_global_access}
        :param all_ports: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'allPorts' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, SCTP, or L3_DEFAULT. - It's applicable only to the following products: internal passthrough Network Load Balancers, backend service-based external passthrough Network Load Balancers, and internal and external protocol forwarding. - Set this field to true to allow packets addressed to any port or packets lacking destination port information (for example, UDP fragments after the first fragment) to be forwarded to the backends configured with this forwarding rule. The L3_DEFAULT protocol requires 'allPorts' be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#all_ports ComputeForwardingRule#all_ports}
        :param backend_service: Identifies the backend service to which the forwarding rule sends traffic. Required for Internal TCP/UDP Load Balancing and Network Load Balancing; must be omitted for all other load balancer types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#backend_service ComputeForwardingRule#backend_service}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#description ComputeForwardingRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#id ComputeForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced 'target' or 'backendService'. While creating a forwarding rule, specifying an 'IPAddress' is required under the following circumstances: - When the 'target' is set to 'targetGrpcProxy' and 'validateForProxyless' is set to 'true', the 'IPAddress' should be set to '0.0.0.0'. - When the 'target' is a Private Service Connect Google APIs bundle, you must specify an 'IPAddress'. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: - IP address number, as in '100.1.2.3' - IPv6 address range, as in '2600:1234::/96' - Full resource URL, as in 'https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name' - Partial URL or by name, as in: - 'projects/project_id/regions/region/addresses/address-name' - 'regions/region/addresses/address-name' - 'global/addresses/address-name' - 'address-name' The forwarding rule's 'target' or 'backendService', and in most cases, also the 'loadBalancingScheme', determine the type of IP address that you can use. For detailed information, see `IP address specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. When reading an 'IPAddress', the API always returns the IP address number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_address ComputeForwardingRule#ip_address}
        :param ip_collection: Resource reference of a PublicDelegatedPrefix. The PDP must be a sub-PDP in EXTERNAL_IPV6_FORWARDING_RULE_CREATION mode. Use one of the following formats to specify a sub-PDP when creating an IPv6 NetLB forwarding rule using BYOIP: Full resource URL, as in: - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Partial URL, as in: - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}' - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_collection ComputeForwardingRule#ip_collection}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are 'TCP', 'UDP', 'ESP', 'AH', 'SCTP', 'ICMP' and 'L3_DEFAULT'. The valid IP protocols are different for different load balancing products as described in `Load balancing features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_. A Forwarding Rule with protocol L3_DEFAULT can attach with target instance or backend service with UNSPECIFIED protocol. A forwarding rule with "L3_DEFAULT" IPProtocal cannot be attached to a backend service with TCP or UDP. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP", "L3_DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_protocol ComputeForwardingRule#ip_protocol}
        :param ip_version: The IP address version that will be used by this forwarding rule. Valid options are IPV4 and IPV6. If not set, the IPv4 address will be used by default. Possible values: ["IPV4", "IPV6"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_version ComputeForwardingRule#ip_version}
        :param is_mirroring_collector: Indicates whether or not this load balancer can be used as a collector for packet mirroring. To prevent mirroring loops, instances behind this load balancer will not have their traffic mirrored even if a 'PacketMirroring' rule applies to them. This can only be set to true for load balancers that have their 'loadBalancingScheme' set to 'INTERNAL'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#is_mirroring_collector ComputeForwardingRule#is_mirroring_collector}
        :param labels: Labels to apply to this forwarding rule. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#labels ComputeForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. Note that an empty string value ('""') is also supported for some use cases, for example PSC (private service connection) regional forwarding rules. For more information about forwarding rules, refer to `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#load_balancing_scheme ComputeForwardingRule#load_balancing_scheme}
        :param network: This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If the subnetwork is specified, the network of the subnetwork will be used. If neither subnetwork nor this field is specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#network ComputeForwardingRule#network}
        :param network_tier: This signifies the networking tier used for configuring this load balancer and can only take the following values: 'PREMIUM', 'STANDARD'. For regional ForwardingRule, the valid values are 'PREMIUM' and 'STANDARD'. For GlobalForwardingRule, the valid value is 'PREMIUM'. If this field is not specified, it is assumed to be 'PREMIUM'. If 'IPAddress' is specified, this value must be equal to the networkTier of the Address. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#network_tier ComputeForwardingRule#network_tier}
        :param no_automate_dns_zone: This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#no_automate_dns_zone ComputeForwardingRule#no_automate_dns_zone}
        :param port_range: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'portRange' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and - It's applicable only to the following products: external passthrough Network Load Balancers, internal and external proxy Network Load Balancers, internal and external Application Load Balancers, external protocol forwarding, and Classic VPN. - Some products have restrictions on what ports can be used. See `port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications>`_ for details. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's.
        :param ports: The 'ports', 'portRange', and 'allPorts' fields are mutually exclusive. Only packets addressed to ports in the specified range will be forwarded to the backends configured with this forwarding rule. The 'ports' field has the following limitations: - It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and - It's applicable only to the following products: internal passthrough Network Load Balancers, backend service-based external passthrough Network Load Balancers, and internal protocol forwarding. - You can specify a list of up to five ports by number, separated by commas. The ports can be contiguous or discontiguous. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair if they share at least one port number. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair if they share at least one port number.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#project ComputeForwardingRule#project}.
        :param recreate_closed_psc: This is used in PSC consumer ForwardingRule to make terraform recreate the ForwardingRule when the status is closed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#recreate_closed_psc ComputeForwardingRule#recreate_closed_psc}
        :param region: A reference to the region where the regional forwarding rule resides. This field is not applicable to global forwarding rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#region ComputeForwardingRule#region}
        :param service_directory_registrations: service_directory_registrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#service_directory_registrations ComputeForwardingRule#service_directory_registrations}
        :param service_label: An optional prefix to the service name for this Forwarding Rule. If specified, will be the first label of the fully qualified service name. The label must be 1-63 characters long, and comply with RFC1035. Specifically, the label must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. This field is only used for INTERNAL load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#service_label ComputeForwardingRule#service_label}
        :param source_ip_ranges: If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here. Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#source_ip_ranges ComputeForwardingRule#source_ip_ranges}
        :param subnetwork: This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#subnetwork ComputeForwardingRule#subnetwork}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. - For load balancers, see the "Target" column in `Port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - 'vpc-sc' - ` APIs that support VPC Service Controls <https://cloud.google.com/vpc-service-controls/docs/supported-products>`_. - 'all-apis' - `All supported Google APIs <https://cloud.google.com/vpc/docs/private-service-connect#supported-apis>`_. For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#target ComputeForwardingRule#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#timeouts ComputeForwardingRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(service_directory_registrations, dict):
            service_directory_registrations = ComputeForwardingRuleServiceDirectoryRegistrations(**service_directory_registrations)
        if isinstance(timeouts, dict):
            timeouts = ComputeForwardingRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d88eac52aca26c2b779c20f0f2c4505c93507b4abd7999111bf56fae8e47f15)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#name ComputeForwardingRule#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#allow_global_access ComputeForwardingRule#allow_global_access}
        '''
        result = self._values.get("allow_global_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_psc_global_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#allow_psc_global_access ComputeForwardingRule#allow_psc_global_access}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#all_ports ComputeForwardingRule#all_ports}
        '''
        result = self._values.get("all_ports")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backend_service(self) -> typing.Optional[builtins.str]:
        '''Identifies the backend service to which the forwarding rule sends traffic.

        Required for Internal TCP/UDP Load Balancing and Network Load Balancing;
        must be omitted for all other load balancer types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#backend_service ComputeForwardingRule#backend_service}
        '''
        result = self._values.get("backend_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#description ComputeForwardingRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#id ComputeForwardingRule#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_address ComputeForwardingRule#ip_address}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_collection ComputeForwardingRule#ip_collection}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_protocol ComputeForwardingRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_version(self) -> typing.Optional[builtins.str]:
        '''The IP address version that will be used by this forwarding rule. Valid options are IPV4 and IPV6.

        If not set, the IPv4 address will be used by default. Possible values: ["IPV4", "IPV6"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ip_version ComputeForwardingRule#ip_version}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#is_mirroring_collector ComputeForwardingRule#is_mirroring_collector}
        '''
        result = self._values.get("is_mirroring_collector")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this forwarding rule.  A list of key->value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#labels ComputeForwardingRule#labels}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#load_balancing_scheme ComputeForwardingRule#load_balancing_scheme}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#network ComputeForwardingRule#network}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#network_tier ComputeForwardingRule#network_tier}
        '''
        result = self._values.get("network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_automate_dns_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not.

        Non-PSC forwarding rules do not use this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#no_automate_dns_zone ComputeForwardingRule#no_automate_dns_zone}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#port_range ComputeForwardingRule#port_range}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#ports ComputeForwardingRule#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#project ComputeForwardingRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recreate_closed_psc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This is used in PSC consumer ForwardingRule to make terraform recreate the ForwardingRule when the status is closed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#recreate_closed_psc ComputeForwardingRule#recreate_closed_psc}
        '''
        result = self._values.get("recreate_closed_psc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''A reference to the region where the regional forwarding rule resides.

        This field is not applicable to global forwarding rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#region ComputeForwardingRule#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_registrations(
        self,
    ) -> typing.Optional["ComputeForwardingRuleServiceDirectoryRegistrations"]:
        '''service_directory_registrations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#service_directory_registrations ComputeForwardingRule#service_directory_registrations}
        '''
        result = self._values.get("service_directory_registrations")
        return typing.cast(typing.Optional["ComputeForwardingRuleServiceDirectoryRegistrations"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#service_label ComputeForwardingRule#service_label}
        '''
        result = self._values.get("service_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here.

        Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#source_ip_ranges ComputeForwardingRule#source_ip_ranges}
        '''
        result = self._values.get("source_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6.

        If the network specified is in auto subnet mode, this field is optional.
        However, a subnetwork must be specified if the network is in custom subnet
        mode or when creating external forwarding rule with IPv6.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#subnetwork ComputeForwardingRule#subnetwork}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#target ComputeForwardingRule#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeForwardingRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#timeouts ComputeForwardingRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeForwardingRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeForwardingRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeForwardingRule.ComputeForwardingRuleServiceDirectoryRegistrations",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace", "service": "service"},
)
class ComputeForwardingRuleServiceDirectoryRegistrations:
    def __init__(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace: Service Directory namespace to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#namespace ComputeForwardingRule#namespace}
        :param service: Service Directory service to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#service ComputeForwardingRule#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62fd603b4476f13376bcf695b1a8ef704c8a0c66d4be53edd1b8178afc5316cb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#namespace ComputeForwardingRule#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Service Directory service to register the forwarding rule under.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#service ComputeForwardingRule#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeForwardingRuleServiceDirectoryRegistrations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeForwardingRuleServiceDirectoryRegistrationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeForwardingRule.ComputeForwardingRuleServiceDirectoryRegistrationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cb9a6756984b3dc9d3af6e3d02916ee10ae15a4b61859730adbdbd79435f71d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__748090b8345ec5d9bc4424b0ff3a84ee4d81489d563574d9c95efe5aa8bfcafd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d3a38ec86234d843ade3906dc00701b7bc8df424ab22d5a48ee66e3e15a31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeForwardingRuleServiceDirectoryRegistrations]:
        return typing.cast(typing.Optional[ComputeForwardingRuleServiceDirectoryRegistrations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeForwardingRuleServiceDirectoryRegistrations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00e9cb306c18d625cccdd53283e2d708ee09b2e1a1c80226f0c8e660192761d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeForwardingRule.ComputeForwardingRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeForwardingRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#create ComputeForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#delete ComputeForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#update ComputeForwardingRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf28cf4842fe527a6c737ff881098a84b5c9548bf4e5f9660884d6983bbf871d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#create ComputeForwardingRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#delete ComputeForwardingRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_forwarding_rule#update ComputeForwardingRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeForwardingRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeForwardingRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeForwardingRule.ComputeForwardingRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24df6c2537ec83b9decce0ea5d1b79d15c9c7ac85ac93448f466b7863ce8e8de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__deaddc49bfb48412ae8b676241fd6bf0d197343c214605244c33e5412ff6fd30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8682aa17d1cbc205e1a6327b98b320c8bce9e0cc75dd4d5d8f75c8482f36a749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4815b6f63866a32241bb08bb377be652b79b2b7d13dc30e00ac2e3da1feee2c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeForwardingRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeForwardingRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeForwardingRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bbb6570b0b9c982b4425999edd91ef258025131ca26c1a9d987742b30fb5f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeForwardingRule",
    "ComputeForwardingRuleConfig",
    "ComputeForwardingRuleServiceDirectoryRegistrations",
    "ComputeForwardingRuleServiceDirectoryRegistrationsOutputReference",
    "ComputeForwardingRuleTimeouts",
    "ComputeForwardingRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d7372c51506266c10431315b4fadc9d5bb288959f1095d4769bc18c78b6df2ee(
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
    service_directory_registrations: typing.Optional[typing.Union[ComputeForwardingRuleServiceDirectoryRegistrations, typing.Dict[builtins.str, typing.Any]]] = None,
    service_label: typing.Optional[builtins.str] = None,
    source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__588e0409647f6f6cdaa8102ef80ea8e12ba42d38598b02cff6c838b27fdce009(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83d9886930772e32eda3f83575bf6d632f5965e05edcda05dba098adb9c5cde(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679f5af44506fa2b0cb9fed7f128208217f022e45b23b8a93e5b0acd43053262(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab0ca698b77098182d9a555a854e451a0c8cfa39e1273842e7a23c70e4fbf25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7508a2948935d7dba425cbd2c96c06788615eb2272a566b0ec4191ff9fa71202(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5982185346246925f47700b95339fe9171ed7da078bdaa3464ebf165c7bfa1c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffec22e27fba647b3bbb50b3022811ff49dc49e8ebeaf5d4b3953a9a1d424bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67013e041e8225d78fc23e4ab6d2b2a600b97be2a7ffc870bb7297ce20d6549(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416ab50e468fca3e94ff4d27949857757a89f425dc10173fad21c1e792517ccd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7df2df98bd49c9a2a5d946d2f229a061a47b66ea9ac4e9d9b9b32d603dd9945(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e7c5618daf45d293499a6176c5c99276c1b3f99a754409156089b9a058b8c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1c6fc32531b8b1707bc4582f49e71f1471caca133bfe3bf48ee89ca76ab93c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3aa58719523889649c21454fd13f76a2d17089b05b08a3dabba2ce72d1ec7e1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69090430a1a759e85a3a132ffcc5f061b2b0312e9d6fe2bf9ad04e4aa72d049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6520c1ad58a1d8f1620710557a770bfab880d609f2f929ad40de2967e7364466(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dded1f8fa8e2b73ff8d3ab2756ea83aba88d2e4f0a9b4d1cce79e2330762c4f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc71406ec54e71bdbdbaa8bdcdff4e1b0e2bab5fd6496a3cf7d334bb3fa3e240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175869baefdbff8b4b36b0a12063a83447233c4efba7adfb84cc8501e677c3bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64bbc049ff79795ed026b00d001cd54adb4815f1d6d678bbce0f2a8ffc6173d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567e1b0339f789e98f7d2643ae864daebcade2714cff7af149ae03cb77eb68ee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4022f2e03f4b129034c9783730496075d0915e47f859480bc2dc82ac4a5ab7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b41a8532d8c9cd7a6ad9e5cc2af69e418fc096661f698584328cca7dc66b29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d324571bde6b9c49d78e6cd25cf6f03cf075a0a3fdbeb7c0b89980766832e09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77e479ce39d11eb2a4879e1eb665a9ab97ea25414578139c53994dde749c607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704608146502e5feac9899c5665f68c981d6d661df3fdd56387843b6789b7b7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754f75583218fdd71727da54c6a345385ea999110e039b3961866352bb6e0f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b235de770c8e921793c52c35166daa7e83a440e43dd8e648084e87fc5b17707e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d88eac52aca26c2b779c20f0f2c4505c93507b4abd7999111bf56fae8e47f15(
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
    service_directory_registrations: typing.Optional[typing.Union[ComputeForwardingRuleServiceDirectoryRegistrations, typing.Dict[builtins.str, typing.Any]]] = None,
    service_label: typing.Optional[builtins.str] = None,
    source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62fd603b4476f13376bcf695b1a8ef704c8a0c66d4be53edd1b8178afc5316cb(
    *,
    namespace: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb9a6756984b3dc9d3af6e3d02916ee10ae15a4b61859730adbdbd79435f71d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748090b8345ec5d9bc4424b0ff3a84ee4d81489d563574d9c95efe5aa8bfcafd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d3a38ec86234d843ade3906dc00701b7bc8df424ab22d5a48ee66e3e15a31b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00e9cb306c18d625cccdd53283e2d708ee09b2e1a1c80226f0c8e660192761d(
    value: typing.Optional[ComputeForwardingRuleServiceDirectoryRegistrations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf28cf4842fe527a6c737ff881098a84b5c9548bf4e5f9660884d6983bbf871d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24df6c2537ec83b9decce0ea5d1b79d15c9c7ac85ac93448f466b7863ce8e8de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deaddc49bfb48412ae8b676241fd6bf0d197343c214605244c33e5412ff6fd30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8682aa17d1cbc205e1a6327b98b320c8bce9e0cc75dd4d5d8f75c8482f36a749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4815b6f63866a32241bb08bb377be652b79b2b7d13dc30e00ac2e3da1feee2c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbb6570b0b9c982b4425999edd91ef258025131ca26c1a9d987742b30fb5f27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeForwardingRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
