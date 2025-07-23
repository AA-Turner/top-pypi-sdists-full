r'''
# `google_compute_global_forwarding_rule`

Refer to the Terraform Registry for docs: [`google_compute_global_forwarding_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule).
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


class ComputeGlobalForwardingRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule google_compute_global_forwarding_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_managed_backend_bucket_migration_state: typing.Optional[builtins.str] = None,
        external_managed_backend_bucket_migration_testing_percentage: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeGlobalForwardingRuleMetadataFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
        no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port_range: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        service_directory_registrations: typing.Optional[typing.Union["ComputeGlobalForwardingRuleServiceDirectoryRegistrations", typing.Dict[builtins.str, typing.Any]]] = None,
        source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeGlobalForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule google_compute_global_forwarding_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. For Private Service Connect forwarding rules that forward traffic to Google APIs, the forwarding rule name must be a 1-20 characters string with lowercase letters and numbers and must start with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. - For load balancers, see the "Target" column in `Port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - 'vpc-sc' - ` APIs that support VPC Service Controls <https://cloud.google.com/vpc-service-controls/docs/supported-products>`_. - 'all-apis' - `All supported Google APIs <https://cloud.google.com/vpc/docs/private-service-connect#supported-apis>`_. For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#target ComputeGlobalForwardingRule#target}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#description ComputeGlobalForwardingRule#description}
        :param external_managed_backend_bucket_migration_state: Specifies the canary migration state for the backend buckets attached to this forwarding rule. Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC. To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate traffic to backend buckets attached to this forwarding rule by percentage using externalManagedBackendBucketMigrationTestingPercentage. Rolling back a migration requires the states to be set in reverse order. So changing the scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#external_managed_backend_bucket_migration_state ComputeGlobalForwardingRule#external_managed_backend_bucket_migration_state}
        :param external_managed_backend_bucket_migration_testing_percentage: Determines the fraction of requests to backend buckets that should be processed by the Global external Application Load Balancer. The value of this field must be in the range [0, 100]. This value can only be set if the loadBalancingScheme in the forwarding rule is set to EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#external_managed_backend_bucket_migration_testing_percentage ComputeGlobalForwardingRule#external_managed_backend_bucket_migration_testing_percentage}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#id ComputeGlobalForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced 'target'. While creating a forwarding rule, specifying an 'IPAddress' is required under the following circumstances: - When the 'target' is set to 'targetGrpcProxy' and 'validateForProxyless' is set to 'true', the 'IPAddress' should be set to '0.0.0.0'. - When the 'target' is a Private Service Connect Google APIs bundle, you must specify an 'IPAddress'. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: - IP address number, as in '100.1.2.3' - IPv6 address range, as in '2600:1234::/96' - Full resource URL, as in 'https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name' - Partial URL or by name, as in: - 'projects/project_id/regions/region/addresses/address-name' - 'regions/region/addresses/address-name' - 'global/addresses/address-name' - 'address-name' The forwarding rule's 'target', and in most cases, also the 'loadBalancingScheme', determine the type of IP address that you can use. For detailed information, see `IP address specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. When reading an 'IPAddress', the API always returns the IP address number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#ip_address ComputeGlobalForwardingRule#ip_address}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are 'TCP', 'UDP', 'ESP', 'AH', 'SCTP', 'ICMP' and 'L3_DEFAULT'. The valid IP protocols are different for different load balancing products as described in `Load balancing features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#ip_protocol ComputeGlobalForwardingRule#ip_protocol}
        :param ip_version: The IP Version that will be used by this global forwarding rule. Possible values: ["IPV4", "IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#ip_version ComputeGlobalForwardingRule#ip_version}
        :param labels: Labels to apply to this forwarding rule. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#labels ComputeGlobalForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. For more information about forwarding rules, refer to `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#load_balancing_scheme ComputeGlobalForwardingRule#load_balancing_scheme}
        :param metadata_filters: metadata_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#metadata_filters ComputeGlobalForwardingRule#metadata_filters}
        :param network: This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If the subnetwork is specified, the network of the subnetwork will be used. If neither subnetwork nor this field is specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#network ComputeGlobalForwardingRule#network}
        :param network_tier: This signifies the networking tier used for configuring this load balancer and can only take the following values: 'PREMIUM', 'STANDARD'. For regional ForwardingRule, the valid values are 'PREMIUM' and 'STANDARD'. For GlobalForwardingRule, the valid value is 'PREMIUM'. If this field is not specified, it is assumed to be 'PREMIUM'. If 'IPAddress' is specified, this value must be equal to the networkTier of the Address. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#network_tier ComputeGlobalForwardingRule#network_tier}
        :param no_automate_dns_zone: This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#no_automate_dns_zone ComputeGlobalForwardingRule#no_automate_dns_zone}
        :param port_range: The 'portRange' field has the following limitations: * It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and * It's applicable only to the following products: external passthrough Network Load Balancers, internal and external proxy Network Load Balancers, internal and external Application Load Balancers, external protocol forwarding, and Classic VPN. - Some products have restrictions on what ports can be used. See `port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications>`_ for details. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#project ComputeGlobalForwardingRule#project}.
        :param service_directory_registrations: service_directory_registrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#service_directory_registrations ComputeGlobalForwardingRule#service_directory_registrations}
        :param source_ip_ranges: If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here. Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#source_ip_ranges ComputeGlobalForwardingRule#source_ip_ranges}
        :param subnetwork: This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#subnetwork ComputeGlobalForwardingRule#subnetwork}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#timeouts ComputeGlobalForwardingRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07c6b8df8839697e16cbcd5e3857a8f9633622cc0a8e09c826725c04262fbeb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeGlobalForwardingRuleConfig(
            name=name,
            target=target,
            description=description,
            external_managed_backend_bucket_migration_state=external_managed_backend_bucket_migration_state,
            external_managed_backend_bucket_migration_testing_percentage=external_managed_backend_bucket_migration_testing_percentage,
            id=id,
            ip_address=ip_address,
            ip_protocol=ip_protocol,
            ip_version=ip_version,
            labels=labels,
            load_balancing_scheme=load_balancing_scheme,
            metadata_filters=metadata_filters,
            network=network,
            network_tier=network_tier,
            no_automate_dns_zone=no_automate_dns_zone,
            port_range=port_range,
            project=project,
            service_directory_registrations=service_directory_registrations,
            source_ip_ranges=source_ip_ranges,
            subnetwork=subnetwork,
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
        '''Generates CDKTF code for importing a ComputeGlobalForwardingRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeGlobalForwardingRule to import.
        :param import_from_id: The id of the existing ComputeGlobalForwardingRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeGlobalForwardingRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c30cb7fa7fa7bba1d88cb2ed2aea6a5c9e9477fd0068e66a39121e8f6067a1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetadataFilters")
    def put_metadata_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeGlobalForwardingRuleMetadataFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3da6aed82913615e21b1e245dbb09143c830e165a8666be04bce3dd900389b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataFilters", [value]))

    @jsii.member(jsii_name="putServiceDirectoryRegistrations")
    def put_service_directory_registrations(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        service_directory_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace: Service Directory namespace to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#namespace ComputeGlobalForwardingRule#namespace}
        :param service_directory_region: [Optional] Service Directory region to register this global forwarding rule under. Default to "us-central1". Only used for PSC for Google APIs. All PSC for Google APIs Forwarding Rules on the same network should use the same Service Directory region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#service_directory_region ComputeGlobalForwardingRule#service_directory_region}
        '''
        value = ComputeGlobalForwardingRuleServiceDirectoryRegistrations(
            namespace=namespace, service_directory_region=service_directory_region
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#create ComputeGlobalForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#delete ComputeGlobalForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#update ComputeGlobalForwardingRule#update}.
        '''
        value = ComputeGlobalForwardingRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExternalManagedBackendBucketMigrationState")
    def reset_external_managed_backend_bucket_migration_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalManagedBackendBucketMigrationState", []))

    @jsii.member(jsii_name="resetExternalManagedBackendBucketMigrationTestingPercentage")
    def reset_external_managed_backend_bucket_migration_testing_percentage(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalManagedBackendBucketMigrationTestingPercentage", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetIpProtocol")
    def reset_ip_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpProtocol", []))

    @jsii.member(jsii_name="resetIpVersion")
    def reset_ip_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpVersion", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLoadBalancingScheme")
    def reset_load_balancing_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingScheme", []))

    @jsii.member(jsii_name="resetMetadataFilters")
    def reset_metadata_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataFilters", []))

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

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetServiceDirectoryRegistrations")
    def reset_service_directory_registrations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryRegistrations", []))

    @jsii.member(jsii_name="resetSourceIpRanges")
    def reset_source_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceIpRanges", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

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
    @jsii.member(jsii_name="metadataFilters")
    def metadata_filters(self) -> "ComputeGlobalForwardingRuleMetadataFiltersList":
        return typing.cast("ComputeGlobalForwardingRuleMetadataFiltersList", jsii.get(self, "metadataFilters"))

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
    ) -> "ComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference":
        return typing.cast("ComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference", jsii.get(self, "serviceDirectoryRegistrations"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeGlobalForwardingRuleTimeoutsOutputReference":
        return typing.cast("ComputeGlobalForwardingRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="externalManagedBackendBucketMigrationStateInput")
    def external_managed_backend_bucket_migration_state_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalManagedBackendBucketMigrationStateInput"))

    @builtins.property
    @jsii.member(jsii_name="externalManagedBackendBucketMigrationTestingPercentageInput")
    def external_managed_backend_bucket_migration_testing_percentage_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "externalManagedBackendBucketMigrationTestingPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="ipVersionInput")
    def ip_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipVersionInput"))

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
    @jsii.member(jsii_name="metadataFiltersInput")
    def metadata_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFilters"]]], jsii.get(self, "metadataFiltersInput"))

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
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryRegistrationsInput")
    def service_directory_registrations_input(
        self,
    ) -> typing.Optional["ComputeGlobalForwardingRuleServiceDirectoryRegistrations"]:
        return typing.cast(typing.Optional["ComputeGlobalForwardingRuleServiceDirectoryRegistrations"], jsii.get(self, "serviceDirectoryRegistrationsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeGlobalForwardingRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeGlobalForwardingRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7396904b9fa6cc3785d9ee1f639d0722d44b1f8c3db2dfbd5840f9c65e50127a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalManagedBackendBucketMigrationState")
    def external_managed_backend_bucket_migration_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalManagedBackendBucketMigrationState"))

    @external_managed_backend_bucket_migration_state.setter
    def external_managed_backend_bucket_migration_state(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe409544ff2dc8d3f38aedd92767dbedb4a2bb2378ad2f0e8b1b9d301af904a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalManagedBackendBucketMigrationState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalManagedBackendBucketMigrationTestingPercentage")
    def external_managed_backend_bucket_migration_testing_percentage(
        self,
    ) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "externalManagedBackendBucketMigrationTestingPercentage"))

    @external_managed_backend_bucket_migration_testing_percentage.setter
    def external_managed_backend_bucket_migration_testing_percentage(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4f4ef7eb1a5c3e1b93c74116768e31bf3b40270d9eaa3c48804a63cf5560a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalManagedBackendBucketMigrationTestingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05df454c0bd3584aff5eebae81ab50fd50f7f22d9ed35a9c8d459d98fda5257c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec05748b913f9cf2d81848f50a3713e855c72e331f5cf4951ed65cfba1795ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1974ffc65d8718b70079ff3d85806e2a4b578dcc5311dd44624f48e4c970532f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipVersion")
    def ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipVersion"))

    @ip_version.setter
    def ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab37d490f81a1ff4285090e3229e8af901a1a5cabe7bc90b4d66021e2dca607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3599d947c04d4b88ffd0da76af3a4a6fddb2c58f37fc6a1a2d77a467e43f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01956d3d8fc393605654f6ee523bcea5523db6da9584a6189ffc6827c3672b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ec55655ca2e121bd9057038c5dbc03bbd94a93a7535e816aa6dbd8a83c7c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ad46a452b5d9e83d13f9aaa71b63e9244c53365bcc58c6e2b39b2cb72ede08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13b1a776935d87a85cd980f8a5aa58cbb7566812bad2bb5cf3c335169664ef8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef69d91acaccf2262451a3d15f02c212623bc9b5a0b097d973348df6034ac853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAutomateDnsZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portRange")
    def port_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portRange"))

    @port_range.setter
    def port_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83050467b3e420986f10437d51eb071e85a197f5d7a4ca942c38d271b937a52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65489ee1239755aef95520d70360be444b00f4c1ebe301939b86a6e699db15f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceIpRanges")
    def source_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceIpRanges"))

    @source_ip_ranges.setter
    def source_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9854810c63c2f9cb79dec6b723dcc246309139c6c08d70f1d0d26b907523294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82862ebfa0e64dcf64b1e9ec3e7fe365ed29efa2e316a32d219d1c153ac89b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314e637db451689b13f3f66ae6b3ba8e446a67d09392d3ffadcd765c83b042c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleConfig",
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
        "target": "target",
        "description": "description",
        "external_managed_backend_bucket_migration_state": "externalManagedBackendBucketMigrationState",
        "external_managed_backend_bucket_migration_testing_percentage": "externalManagedBackendBucketMigrationTestingPercentage",
        "id": "id",
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "ip_version": "ipVersion",
        "labels": "labels",
        "load_balancing_scheme": "loadBalancingScheme",
        "metadata_filters": "metadataFilters",
        "network": "network",
        "network_tier": "networkTier",
        "no_automate_dns_zone": "noAutomateDnsZone",
        "port_range": "portRange",
        "project": "project",
        "service_directory_registrations": "serviceDirectoryRegistrations",
        "source_ip_ranges": "sourceIpRanges",
        "subnetwork": "subnetwork",
        "timeouts": "timeouts",
    },
)
class ComputeGlobalForwardingRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_managed_backend_bucket_migration_state: typing.Optional[builtins.str] = None,
        external_managed_backend_bucket_migration_testing_percentage: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeGlobalForwardingRuleMetadataFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
        no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port_range: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        service_directory_registrations: typing.Optional[typing.Union["ComputeGlobalForwardingRuleServiceDirectoryRegistrations", typing.Dict[builtins.str, typing.Any]]] = None,
        source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeGlobalForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. For Private Service Connect forwarding rules that forward traffic to Google APIs, the forwarding rule name must be a 1-20 characters string with lowercase letters and numbers and must start with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. - For load balancers, see the "Target" column in `Port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - 'vpc-sc' - ` APIs that support VPC Service Controls <https://cloud.google.com/vpc-service-controls/docs/supported-products>`_. - 'all-apis' - `All supported Google APIs <https://cloud.google.com/vpc/docs/private-service-connect#supported-apis>`_. For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#target ComputeGlobalForwardingRule#target}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#description ComputeGlobalForwardingRule#description}
        :param external_managed_backend_bucket_migration_state: Specifies the canary migration state for the backend buckets attached to this forwarding rule. Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC. To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate traffic to backend buckets attached to this forwarding rule by percentage using externalManagedBackendBucketMigrationTestingPercentage. Rolling back a migration requires the states to be set in reverse order. So changing the scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#external_managed_backend_bucket_migration_state ComputeGlobalForwardingRule#external_managed_backend_bucket_migration_state}
        :param external_managed_backend_bucket_migration_testing_percentage: Determines the fraction of requests to backend buckets that should be processed by the Global external Application Load Balancer. The value of this field must be in the range [0, 100]. This value can only be set if the loadBalancingScheme in the forwarding rule is set to EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#external_managed_backend_bucket_migration_testing_percentage ComputeGlobalForwardingRule#external_managed_backend_bucket_migration_testing_percentage}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#id ComputeGlobalForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced 'target'. While creating a forwarding rule, specifying an 'IPAddress' is required under the following circumstances: - When the 'target' is set to 'targetGrpcProxy' and 'validateForProxyless' is set to 'true', the 'IPAddress' should be set to '0.0.0.0'. - When the 'target' is a Private Service Connect Google APIs bundle, you must specify an 'IPAddress'. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: - IP address number, as in '100.1.2.3' - IPv6 address range, as in '2600:1234::/96' - Full resource URL, as in 'https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name' - Partial URL or by name, as in: - 'projects/project_id/regions/region/addresses/address-name' - 'regions/region/addresses/address-name' - 'global/addresses/address-name' - 'address-name' The forwarding rule's 'target', and in most cases, also the 'loadBalancingScheme', determine the type of IP address that you can use. For detailed information, see `IP address specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. When reading an 'IPAddress', the API always returns the IP address number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#ip_address ComputeGlobalForwardingRule#ip_address}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are 'TCP', 'UDP', 'ESP', 'AH', 'SCTP', 'ICMP' and 'L3_DEFAULT'. The valid IP protocols are different for different load balancing products as described in `Load balancing features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#ip_protocol ComputeGlobalForwardingRule#ip_protocol}
        :param ip_version: The IP Version that will be used by this global forwarding rule. Possible values: ["IPV4", "IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#ip_version ComputeGlobalForwardingRule#ip_version}
        :param labels: Labels to apply to this forwarding rule. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#labels ComputeGlobalForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. For more information about forwarding rules, refer to `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#load_balancing_scheme ComputeGlobalForwardingRule#load_balancing_scheme}
        :param metadata_filters: metadata_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#metadata_filters ComputeGlobalForwardingRule#metadata_filters}
        :param network: This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If the subnetwork is specified, the network of the subnetwork will be used. If neither subnetwork nor this field is specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#network ComputeGlobalForwardingRule#network}
        :param network_tier: This signifies the networking tier used for configuring this load balancer and can only take the following values: 'PREMIUM', 'STANDARD'. For regional ForwardingRule, the valid values are 'PREMIUM' and 'STANDARD'. For GlobalForwardingRule, the valid value is 'PREMIUM'. If this field is not specified, it is assumed to be 'PREMIUM'. If 'IPAddress' is specified, this value must be equal to the networkTier of the Address. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#network_tier ComputeGlobalForwardingRule#network_tier}
        :param no_automate_dns_zone: This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#no_automate_dns_zone ComputeGlobalForwardingRule#no_automate_dns_zone}
        :param port_range: The 'portRange' field has the following limitations: * It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and * It's applicable only to the following products: external passthrough Network Load Balancers, internal and external proxy Network Load Balancers, internal and external Application Load Balancers, external protocol forwarding, and Classic VPN. - Some products have restrictions on what ports can be used. See `port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications>`_ for details. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#project ComputeGlobalForwardingRule#project}.
        :param service_directory_registrations: service_directory_registrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#service_directory_registrations ComputeGlobalForwardingRule#service_directory_registrations}
        :param source_ip_ranges: If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here. Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#source_ip_ranges ComputeGlobalForwardingRule#source_ip_ranges}
        :param subnetwork: This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#subnetwork ComputeGlobalForwardingRule#subnetwork}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#timeouts ComputeGlobalForwardingRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(service_directory_registrations, dict):
            service_directory_registrations = ComputeGlobalForwardingRuleServiceDirectoryRegistrations(**service_directory_registrations)
        if isinstance(timeouts, dict):
            timeouts = ComputeGlobalForwardingRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e403e09b2b631185a4e4e82b793529ec650d24fde948a93a328e0c4e06112c46)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_managed_backend_bucket_migration_state", value=external_managed_backend_bucket_migration_state, expected_type=type_hints["external_managed_backend_bucket_migration_state"])
            check_type(argname="argument external_managed_backend_bucket_migration_testing_percentage", value=external_managed_backend_bucket_migration_testing_percentage, expected_type=type_hints["external_managed_backend_bucket_migration_testing_percentage"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument ip_version", value=ip_version, expected_type=type_hints["ip_version"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument load_balancing_scheme", value=load_balancing_scheme, expected_type=type_hints["load_balancing_scheme"])
            check_type(argname="argument metadata_filters", value=metadata_filters, expected_type=type_hints["metadata_filters"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_tier", value=network_tier, expected_type=type_hints["network_tier"])
            check_type(argname="argument no_automate_dns_zone", value=no_automate_dns_zone, expected_type=type_hints["no_automate_dns_zone"])
            check_type(argname="argument port_range", value=port_range, expected_type=type_hints["port_range"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument service_directory_registrations", value=service_directory_registrations, expected_type=type_hints["service_directory_registrations"])
            check_type(argname="argument source_ip_ranges", value=source_ip_ranges, expected_type=type_hints["source_ip_ranges"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "target": target,
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
        if external_managed_backend_bucket_migration_state is not None:
            self._values["external_managed_backend_bucket_migration_state"] = external_managed_backend_bucket_migration_state
        if external_managed_backend_bucket_migration_testing_percentage is not None:
            self._values["external_managed_backend_bucket_migration_testing_percentage"] = external_managed_backend_bucket_migration_testing_percentage
        if id is not None:
            self._values["id"] = id
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if ip_protocol is not None:
            self._values["ip_protocol"] = ip_protocol
        if ip_version is not None:
            self._values["ip_version"] = ip_version
        if labels is not None:
            self._values["labels"] = labels
        if load_balancing_scheme is not None:
            self._values["load_balancing_scheme"] = load_balancing_scheme
        if metadata_filters is not None:
            self._values["metadata_filters"] = metadata_filters
        if network is not None:
            self._values["network"] = network
        if network_tier is not None:
            self._values["network_tier"] = network_tier
        if no_automate_dns_zone is not None:
            self._values["no_automate_dns_zone"] = no_automate_dns_zone
        if port_range is not None:
            self._values["port_range"] = port_range
        if project is not None:
            self._values["project"] = project
        if service_directory_registrations is not None:
            self._values["service_directory_registrations"] = service_directory_registrations
        if source_ip_ranges is not None:
            self._values["source_ip_ranges"] = source_ip_ranges
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#target ComputeGlobalForwardingRule#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#description ComputeGlobalForwardingRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_managed_backend_bucket_migration_state(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Specifies the canary migration state for the backend buckets attached to this forwarding rule.

        Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC.

        To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to
        PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be
        changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate
        traffic to backend buckets attached to this forwarding rule by percentage using
        externalManagedBackendBucketMigrationTestingPercentage.

        Rolling back a migration requires the states to be set in reverse order. So changing the
        scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at
        the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic
        back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#external_managed_backend_bucket_migration_state ComputeGlobalForwardingRule#external_managed_backend_bucket_migration_state}
        '''
        result = self._values.get("external_managed_backend_bucket_migration_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_managed_backend_bucket_migration_testing_percentage(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Determines the fraction of requests to backend buckets that should be processed by the Global external Application Load Balancer.

        The value of this field must be in the range [0, 100].

        This value can only be set if the loadBalancingScheme in the forwarding rule is set to
        EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#external_managed_backend_bucket_migration_testing_percentage ComputeGlobalForwardingRule#external_managed_backend_bucket_migration_testing_percentage}
        '''
        result = self._values.get("external_managed_backend_bucket_migration_testing_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#id ComputeGlobalForwardingRule#id}.

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
        to the referenced 'target'.

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

        The forwarding rule's 'target',
        and in most cases, also the 'loadBalancingScheme', determine the
        type of IP address that you can use. For detailed information, see
        `IP address
        specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_.

        When reading an 'IPAddress', the API always returns the IP
        address number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#ip_address ComputeGlobalForwardingRule#ip_address}
        '''
        result = self._values.get("ip_address")
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
        features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#ip_protocol ComputeGlobalForwardingRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_version(self) -> typing.Optional[builtins.str]:
        '''The IP Version that will be used by this global forwarding rule. Possible values: ["IPV4", "IPV6"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#ip_version ComputeGlobalForwardingRule#ip_version}
        '''
        result = self._values.get("ip_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this forwarding rule.  A list of key->value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#labels ComputeGlobalForwardingRule#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''Specifies the forwarding rule type.

        For more information about forwarding rules, refer to
        `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#load_balancing_scheme ComputeGlobalForwardingRule#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFilters"]]]:
        '''metadata_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#metadata_filters ComputeGlobalForwardingRule#metadata_filters}
        '''
        result = self._values.get("metadata_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFilters"]]], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#network ComputeGlobalForwardingRule#network}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#network_tier ComputeGlobalForwardingRule#network_tier}
        '''
        result = self._values.get("network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_automate_dns_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not.

        Non-PSC forwarding rules do not use this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#no_automate_dns_zone ComputeGlobalForwardingRule#no_automate_dns_zone}
        '''
        result = self._values.get("no_automate_dns_zone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def port_range(self) -> typing.Optional[builtins.str]:
        '''The 'portRange' field has the following limitations: * It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and * It's applicable only to the following products: external passthrough Network Load Balancers, internal and external proxy Network Load Balancers, internal and external Application Load Balancers, external protocol forwarding, and Classic VPN.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#port_range ComputeGlobalForwardingRule#port_range}
        '''
        result = self._values.get("port_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#project ComputeGlobalForwardingRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_registrations(
        self,
    ) -> typing.Optional["ComputeGlobalForwardingRuleServiceDirectoryRegistrations"]:
        '''service_directory_registrations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#service_directory_registrations ComputeGlobalForwardingRule#service_directory_registrations}
        '''
        result = self._values.get("service_directory_registrations")
        return typing.cast(typing.Optional["ComputeGlobalForwardingRuleServiceDirectoryRegistrations"], result)

    @builtins.property
    def source_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here.

        Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#source_ip_ranges ComputeGlobalForwardingRule#source_ip_ranges}
        '''
        result = self._values.get("source_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6.

        If the network specified is in auto subnet mode, this field is optional.
        However, a subnetwork must be specified if the network is in custom subnet
        mode or when creating external forwarding rule with IPv6.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#subnetwork ComputeGlobalForwardingRule#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeGlobalForwardingRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#timeouts ComputeGlobalForwardingRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeGlobalForwardingRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeGlobalForwardingRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFilters",
    jsii_struct_bases=[],
    name_mapping={
        "filter_labels": "filterLabels",
        "filter_match_criteria": "filterMatchCriteria",
    },
)
class ComputeGlobalForwardingRuleMetadataFilters:
    def __init__(
        self,
        *,
        filter_labels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeGlobalForwardingRuleMetadataFiltersFilterLabels", typing.Dict[builtins.str, typing.Any]]]],
        filter_match_criteria: builtins.str,
    ) -> None:
        '''
        :param filter_labels: filter_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#filter_labels ComputeGlobalForwardingRule#filter_labels}
        :param filter_match_criteria: Specifies how individual filterLabel matches within the list of filterLabels contribute towards the overall metadataFilter match. MATCH_ANY - At least one of the filterLabels must have a matching label in the provided metadata. MATCH_ALL - All filterLabels must have matching labels in the provided metadata. Possible values: ["MATCH_ANY", "MATCH_ALL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#filter_match_criteria ComputeGlobalForwardingRule#filter_match_criteria}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae3463ee3d611ccea9ea9e5f3668e8a7f945179fe73cc74189ad864e513919a)
            check_type(argname="argument filter_labels", value=filter_labels, expected_type=type_hints["filter_labels"])
            check_type(argname="argument filter_match_criteria", value=filter_match_criteria, expected_type=type_hints["filter_match_criteria"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_labels": filter_labels,
            "filter_match_criteria": filter_match_criteria,
        }

    @builtins.property
    def filter_labels(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFiltersFilterLabels"]]:
        '''filter_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#filter_labels ComputeGlobalForwardingRule#filter_labels}
        '''
        result = self._values.get("filter_labels")
        assert result is not None, "Required property 'filter_labels' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeGlobalForwardingRuleMetadataFiltersFilterLabels"]], result)

    @builtins.property
    def filter_match_criteria(self) -> builtins.str:
        '''Specifies how individual filterLabel matches within the list of filterLabels contribute towards the overall metadataFilter match.

        MATCH_ANY - At least one of the filterLabels must have a matching
        label in the provided metadata.
        MATCH_ALL - All filterLabels must have matching labels in the
        provided metadata. Possible values: ["MATCH_ANY", "MATCH_ALL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#filter_match_criteria ComputeGlobalForwardingRule#filter_match_criteria}
        '''
        result = self._values.get("filter_match_criteria")
        assert result is not None, "Required property 'filter_match_criteria' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeGlobalForwardingRuleMetadataFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersFilterLabels",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ComputeGlobalForwardingRuleMetadataFiltersFilterLabels:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Name of the metadata label. The length must be between 1 and 1024 characters, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        :param value: The value that the label must match. The value has a maximum length of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#value ComputeGlobalForwardingRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ecfa75d857dec099070fcfcaf0ffffcdfbcec65330f7c3ff0b67add22b12234)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the metadata label. The length must be between 1 and 1024 characters, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#name ComputeGlobalForwardingRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value that the label must match. The value has a maximum length of 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#value ComputeGlobalForwardingRule#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeGlobalForwardingRuleMetadataFiltersFilterLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0256dc72e1cb2a6b0e6ab733e680e5b16b41c5713b4897cb0d91f1fa45b04b92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1b44a2e7731c35da30340240bf46c9f5ab276a7d61678ac268694b279ff2fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9d043f6b5face30e867cb1a6d59297dd530cc19390e9bc2f91aae42db9baba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__336d1873c4387eefefc5161d559d06c36702d1db411a36f16f659fc97a36f7c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b7afe22e7517ff87f51dafc1a5f123455b382eafb90b7b0ac562e2192f9df61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579f5898101e8ed379295e473748f9f129d33883350f7e1feaa5e9eac901d32d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1f3ba113f612ab0f3ed58e911371462efab09b550f1a30a96c0168a16e439c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a785af3ce6e77a7f8d15cc30aefd33984fb774fe5b90b38aaf9434c3b2dcae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9591135e33691bd2c47e35b1888773b89ed2e833eee9c00fe69c6e98f0e01474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa55770f37104c3ed4562ceef0a36d22ac23abe554abe65964d362773e7f2e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeGlobalForwardingRuleMetadataFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d23a3fb369a8e25b0a267e7f885c01fdad124ba08601ebc201371f133a9aa00f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeGlobalForwardingRuleMetadataFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b286c98fb415450bb2cb6253ae45a243bee1bc9429e61f89c367e88e33de05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeGlobalForwardingRuleMetadataFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b71511edf1db94bbc319433facfe9c20d8dd990cf4b9597f546e76a460fb8bb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f536524257da377d6479fbd6aad8133124a20b416d28e0270aa6b328c0d3fb2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb28c0b9801ca46ff358ce3a1eb6e3a09300870335f0df7bc2a8a7a70cd17829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a511060dab1ad6ef10dd579724eb9d21546d7791c77fb03886c16bcdf3f359e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeGlobalForwardingRuleMetadataFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleMetadataFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46e8764eb6ea807e5541e7728c459aa3720391fd640ce74094a374ca13a4a683)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilterLabels")
    def put_filter_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b03d252ce96b4c565039680e5c0ffef871f6454619a126085e1dcf714d20fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilterLabels", [value]))

    @builtins.property
    @jsii.member(jsii_name="filterLabels")
    def filter_labels(
        self,
    ) -> ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList:
        return typing.cast(ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList, jsii.get(self, "filterLabels"))

    @builtins.property
    @jsii.member(jsii_name="filterLabelsInput")
    def filter_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]], jsii.get(self, "filterLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="filterMatchCriteriaInput")
    def filter_match_criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterMatchCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="filterMatchCriteria")
    def filter_match_criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterMatchCriteria"))

    @filter_match_criteria.setter
    def filter_match_criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fff1bcaa1c75228ae6362bd55f1b8603e62fddcef4cc2fad4436788fc9e400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterMatchCriteria", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleMetadataFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleMetadataFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleMetadataFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53002c926cb97a225d3d55fc9c62cf0fce64e51dab35107f78e6350a16f64de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleServiceDirectoryRegistrations",
    jsii_struct_bases=[],
    name_mapping={
        "namespace": "namespace",
        "service_directory_region": "serviceDirectoryRegion",
    },
)
class ComputeGlobalForwardingRuleServiceDirectoryRegistrations:
    def __init__(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        service_directory_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace: Service Directory namespace to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#namespace ComputeGlobalForwardingRule#namespace}
        :param service_directory_region: [Optional] Service Directory region to register this global forwarding rule under. Default to "us-central1". Only used for PSC for Google APIs. All PSC for Google APIs Forwarding Rules on the same network should use the same Service Directory region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#service_directory_region ComputeGlobalForwardingRule#service_directory_region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea244a692aaed70279360ced8899f6e36fa8b8a822c18c161063b8b833203d68)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument service_directory_region", value=service_directory_region, expected_type=type_hints["service_directory_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if namespace is not None:
            self._values["namespace"] = namespace
        if service_directory_region is not None:
            self._values["service_directory_region"] = service_directory_region

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Service Directory namespace to register the forwarding rule under.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#namespace ComputeGlobalForwardingRule#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_region(self) -> typing.Optional[builtins.str]:
        '''[Optional] Service Directory region to register this global forwarding rule under.

        Default to "us-central1". Only used for PSC for Google APIs. All PSC for
        Google APIs Forwarding Rules on the same network should use the same Service
        Directory region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#service_directory_region ComputeGlobalForwardingRule#service_directory_region}
        '''
        result = self._values.get("service_directory_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeGlobalForwardingRuleServiceDirectoryRegistrations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccf248340bf7d30719427d49c45ac177d7dd9b1010052917e44cc060e3a212b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetServiceDirectoryRegion")
    def reset_service_directory_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryRegion", []))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryRegionInput")
    def service_directory_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceDirectoryRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6815fb9d1560b30802a35f90f1dfe2e0172372c174f3317accb690ff2a1510bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryRegion")
    def service_directory_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceDirectoryRegion"))

    @service_directory_region.setter
    def service_directory_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a9827954e97365c7384819ab3228eefc27ecb516f40aae1dee4211042544b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceDirectoryRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeGlobalForwardingRuleServiceDirectoryRegistrations]:
        return typing.cast(typing.Optional[ComputeGlobalForwardingRuleServiceDirectoryRegistrations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeGlobalForwardingRuleServiceDirectoryRegistrations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c43cb1a7c11fedcf3deb2f4448ea034803ea38a28ea943c5cf366fdd3b73fa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeGlobalForwardingRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#create ComputeGlobalForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#delete ComputeGlobalForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#update ComputeGlobalForwardingRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76058cca11fe4fd284279603d636b8cf18e27eb31e82b906e36169496aed93f8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#create ComputeGlobalForwardingRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#delete ComputeGlobalForwardingRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_global_forwarding_rule#update ComputeGlobalForwardingRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeGlobalForwardingRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeGlobalForwardingRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeGlobalForwardingRule.ComputeGlobalForwardingRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__961e4612af4e06848e69b441d4f4435a9369e0ffd8fd98e4d4a02ad1c2d1cc9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97f805bdfb2ae64c2f0711977e2ce52703a1cce4d4862ae6c2dd1e8244bdde01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e06f1828edc598cf9c652630ae406ee0f42c522a8d73ccf438e8e229c8deb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8717a5a27635f9f7acc5c86034ca8130d1fa359085c4b55fb2b9a745c2a82968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de59a92ee11b84b5480f9fe27da6b40229acdb8b1aec74b49d32ad63c7d266fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeGlobalForwardingRule",
    "ComputeGlobalForwardingRuleConfig",
    "ComputeGlobalForwardingRuleMetadataFilters",
    "ComputeGlobalForwardingRuleMetadataFiltersFilterLabels",
    "ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList",
    "ComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference",
    "ComputeGlobalForwardingRuleMetadataFiltersList",
    "ComputeGlobalForwardingRuleMetadataFiltersOutputReference",
    "ComputeGlobalForwardingRuleServiceDirectoryRegistrations",
    "ComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference",
    "ComputeGlobalForwardingRuleTimeouts",
    "ComputeGlobalForwardingRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a07c6b8df8839697e16cbcd5e3857a8f9633622cc0a8e09c826725c04262fbeb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    external_managed_backend_bucket_migration_state: typing.Optional[builtins.str] = None,
    external_managed_backend_bucket_migration_testing_percentage: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
    no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port_range: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    service_directory_registrations: typing.Optional[typing.Union[ComputeGlobalForwardingRuleServiceDirectoryRegistrations, typing.Dict[builtins.str, typing.Any]]] = None,
    source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeGlobalForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2c30cb7fa7fa7bba1d88cb2ed2aea6a5c9e9477fd0068e66a39121e8f6067a1f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3da6aed82913615e21b1e245dbb09143c830e165a8666be04bce3dd900389b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7396904b9fa6cc3785d9ee1f639d0722d44b1f8c3db2dfbd5840f9c65e50127a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe409544ff2dc8d3f38aedd92767dbedb4a2bb2378ad2f0e8b1b9d301af904a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4f4ef7eb1a5c3e1b93c74116768e31bf3b40270d9eaa3c48804a63cf5560a0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05df454c0bd3584aff5eebae81ab50fd50f7f22d9ed35a9c8d459d98fda5257c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec05748b913f9cf2d81848f50a3713e855c72e331f5cf4951ed65cfba1795ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1974ffc65d8718b70079ff3d85806e2a4b578dcc5311dd44624f48e4c970532f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab37d490f81a1ff4285090e3229e8af901a1a5cabe7bc90b4d66021e2dca607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3599d947c04d4b88ffd0da76af3a4a6fddb2c58f37fc6a1a2d77a467e43f64(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01956d3d8fc393605654f6ee523bcea5523db6da9584a6189ffc6827c3672b78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ec55655ca2e121bd9057038c5dbc03bbd94a93a7535e816aa6dbd8a83c7c7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ad46a452b5d9e83d13f9aaa71b63e9244c53365bcc58c6e2b39b2cb72ede08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13b1a776935d87a85cd980f8a5aa58cbb7566812bad2bb5cf3c335169664ef8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef69d91acaccf2262451a3d15f02c212623bc9b5a0b097d973348df6034ac853(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83050467b3e420986f10437d51eb071e85a197f5d7a4ca942c38d271b937a52a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65489ee1239755aef95520d70360be444b00f4c1ebe301939b86a6e699db15f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9854810c63c2f9cb79dec6b723dcc246309139c6c08d70f1d0d26b907523294(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82862ebfa0e64dcf64b1e9ec3e7fe365ed29efa2e316a32d219d1c153ac89b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314e637db451689b13f3f66ae6b3ba8e446a67d09392d3ffadcd765c83b042c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e403e09b2b631185a4e4e82b793529ec650d24fde948a93a328e0c4e06112c46(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    external_managed_backend_bucket_migration_state: typing.Optional[builtins.str] = None,
    external_managed_backend_bucket_migration_testing_percentage: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
    no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port_range: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    service_directory_registrations: typing.Optional[typing.Union[ComputeGlobalForwardingRuleServiceDirectoryRegistrations, typing.Dict[builtins.str, typing.Any]]] = None,
    source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeGlobalForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae3463ee3d611ccea9ea9e5f3668e8a7f945179fe73cc74189ad864e513919a(
    *,
    filter_labels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, typing.Dict[builtins.str, typing.Any]]]],
    filter_match_criteria: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecfa75d857dec099070fcfcaf0ffffcdfbcec65330f7c3ff0b67add22b12234(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0256dc72e1cb2a6b0e6ab733e680e5b16b41c5713b4897cb0d91f1fa45b04b92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1b44a2e7731c35da30340240bf46c9f5ab276a7d61678ac268694b279ff2fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9d043f6b5face30e867cb1a6d59297dd530cc19390e9bc2f91aae42db9baba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336d1873c4387eefefc5161d559d06c36702d1db411a36f16f659fc97a36f7c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7afe22e7517ff87f51dafc1a5f123455b382eafb90b7b0ac562e2192f9df61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579f5898101e8ed379295e473748f9f129d33883350f7e1feaa5e9eac901d32d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1f3ba113f612ab0f3ed58e911371462efab09b550f1a30a96c0168a16e439c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a785af3ce6e77a7f8d15cc30aefd33984fb774fe5b90b38aaf9434c3b2dcae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9591135e33691bd2c47e35b1888773b89ed2e833eee9c00fe69c6e98f0e01474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa55770f37104c3ed4562ceef0a36d22ac23abe554abe65964d362773e7f2e06(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleMetadataFiltersFilterLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23a3fb369a8e25b0a267e7f885c01fdad124ba08601ebc201371f133a9aa00f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b286c98fb415450bb2cb6253ae45a243bee1bc9429e61f89c367e88e33de05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71511edf1db94bbc319433facfe9c20d8dd990cf4b9597f546e76a460fb8bb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f536524257da377d6479fbd6aad8133124a20b416d28e0270aa6b328c0d3fb2d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb28c0b9801ca46ff358ce3a1eb6e3a09300870335f0df7bc2a8a7a70cd17829(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a511060dab1ad6ef10dd579724eb9d21546d7791c77fb03886c16bcdf3f359e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeGlobalForwardingRuleMetadataFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e8764eb6ea807e5541e7728c459aa3720391fd640ce74094a374ca13a4a683(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b03d252ce96b4c565039680e5c0ffef871f6454619a126085e1dcf714d20fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeGlobalForwardingRuleMetadataFiltersFilterLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fff1bcaa1c75228ae6362bd55f1b8603e62fddcef4cc2fad4436788fc9e400(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53002c926cb97a225d3d55fc9c62cf0fce64e51dab35107f78e6350a16f64de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleMetadataFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea244a692aaed70279360ced8899f6e36fa8b8a822c18c161063b8b833203d68(
    *,
    namespace: typing.Optional[builtins.str] = None,
    service_directory_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf248340bf7d30719427d49c45ac177d7dd9b1010052917e44cc060e3a212b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6815fb9d1560b30802a35f90f1dfe2e0172372c174f3317accb690ff2a1510bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a9827954e97365c7384819ab3228eefc27ecb516f40aae1dee4211042544b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c43cb1a7c11fedcf3deb2f4448ea034803ea38a28ea943c5cf366fdd3b73fa5(
    value: typing.Optional[ComputeGlobalForwardingRuleServiceDirectoryRegistrations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76058cca11fe4fd284279603d636b8cf18e27eb31e82b906e36169496aed93f8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961e4612af4e06848e69b441d4f4435a9369e0ffd8fd98e4d4a02ad1c2d1cc9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f805bdfb2ae64c2f0711977e2ce52703a1cce4d4862ae6c2dd1e8244bdde01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e06f1828edc598cf9c652630ae406ee0f42c522a8d73ccf438e8e229c8deb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8717a5a27635f9f7acc5c86034ca8130d1fa359085c4b55fb2b9a745c2a82968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de59a92ee11b84b5480f9fe27da6b40229acdb8b1aec74b49d32ad63c7d266fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeGlobalForwardingRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
