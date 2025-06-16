r'''
# `google_compute_global_forwarding_rule`

Refer to the Terraform Registry for docs: [`google_compute_global_forwarding_rule`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule).
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


class GoogleComputeGlobalForwardingRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule google_compute_global_forwarding_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        target: builtins.str,
        allow_psc_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        external_managed_backend_bucket_migration_state: typing.Optional[builtins.str] = None,
        external_managed_backend_bucket_migration_testing_percentage: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeGlobalForwardingRuleMetadataFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
        no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port_range: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        service_directory_registrations: typing.Optional[typing.Union["GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations", typing.Dict[builtins.str, typing.Any]]] = None,
        source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeGlobalForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule google_compute_global_forwarding_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. For Private Service Connect forwarding rules that forward traffic to Google APIs, the forwarding rule name must be a 1-20 characters string with lowercase letters and numbers and must start with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#name GoogleComputeGlobalForwardingRule#name}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. - For load balancers, see the "Target" column in `Port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - 'vpc-sc' - ` APIs that support VPC Service Controls <https://cloud.google.com/vpc-service-controls/docs/supported-products>`_. - 'all-apis' - `All supported Google APIs <https://cloud.google.com/vpc/docs/private-service-connect#supported-apis>`_. For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#target GoogleComputeGlobalForwardingRule#target}
        :param allow_psc_global_access: This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#allow_psc_global_access GoogleComputeGlobalForwardingRule#allow_psc_global_access}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#description GoogleComputeGlobalForwardingRule#description}
        :param external_managed_backend_bucket_migration_state: Specifies the canary migration state for the backend buckets attached to this forwarding rule. Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC. To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate traffic to backend buckets attached to this forwarding rule by percentage using externalManagedBackendBucketMigrationTestingPercentage. Rolling back a migration requires the states to be set in reverse order. So changing the scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#external_managed_backend_bucket_migration_state GoogleComputeGlobalForwardingRule#external_managed_backend_bucket_migration_state}
        :param external_managed_backend_bucket_migration_testing_percentage: Determines the fraction of requests to backend buckets that should be processed by the Global external Application Load Balancer. The value of this field must be in the range [0, 100]. This value can only be set if the loadBalancingScheme in the forwarding rule is set to EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#external_managed_backend_bucket_migration_testing_percentage GoogleComputeGlobalForwardingRule#external_managed_backend_bucket_migration_testing_percentage}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#id GoogleComputeGlobalForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced 'target'. While creating a forwarding rule, specifying an 'IPAddress' is required under the following circumstances: - When the 'target' is set to 'targetGrpcProxy' and 'validateForProxyless' is set to 'true', the 'IPAddress' should be set to '0.0.0.0'. - When the 'target' is a Private Service Connect Google APIs bundle, you must specify an 'IPAddress'. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: - IP address number, as in '100.1.2.3' - IPv6 address range, as in '2600:1234::/96' - Full resource URL, as in 'https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name' - Partial URL or by name, as in: - 'projects/project_id/regions/region/addresses/address-name' - 'regions/region/addresses/address-name' - 'global/addresses/address-name' - 'address-name' The forwarding rule's 'target', and in most cases, also the 'loadBalancingScheme', determine the type of IP address that you can use. For detailed information, see `IP address specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. When reading an 'IPAddress', the API always returns the IP address number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#ip_address GoogleComputeGlobalForwardingRule#ip_address}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are 'TCP', 'UDP', 'ESP', 'AH', 'SCTP', 'ICMP' and 'L3_DEFAULT'. The valid IP protocols are different for different load balancing products as described in `Load balancing features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#ip_protocol GoogleComputeGlobalForwardingRule#ip_protocol}
        :param ip_version: The IP Version that will be used by this global forwarding rule. Possible values: ["IPV4", "IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#ip_version GoogleComputeGlobalForwardingRule#ip_version}
        :param labels: Labels to apply to this forwarding rule. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#labels GoogleComputeGlobalForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. For more information about forwarding rules, refer to `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#load_balancing_scheme GoogleComputeGlobalForwardingRule#load_balancing_scheme}
        :param metadata_filters: metadata_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#metadata_filters GoogleComputeGlobalForwardingRule#metadata_filters}
        :param network: This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If the subnetwork is specified, the network of the subnetwork will be used. If neither subnetwork nor this field is specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#network GoogleComputeGlobalForwardingRule#network}
        :param network_tier: This signifies the networking tier used for configuring this load balancer and can only take the following values: 'PREMIUM', 'STANDARD'. For regional ForwardingRule, the valid values are 'PREMIUM' and 'STANDARD'. For GlobalForwardingRule, the valid value is 'PREMIUM'. If this field is not specified, it is assumed to be 'PREMIUM'. If 'IPAddress' is specified, this value must be equal to the networkTier of the Address. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#network_tier GoogleComputeGlobalForwardingRule#network_tier}
        :param no_automate_dns_zone: This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#no_automate_dns_zone GoogleComputeGlobalForwardingRule#no_automate_dns_zone}
        :param port_range: The 'portRange' field has the following limitations: * It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and * It's applicable only to the following products: external passthrough Network Load Balancers, internal and external proxy Network Load Balancers, internal and external Application Load Balancers, external protocol forwarding, and Classic VPN. - Some products have restrictions on what ports can be used. See `port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications>`_ for details. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#project GoogleComputeGlobalForwardingRule#project}.
        :param service_directory_registrations: service_directory_registrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#service_directory_registrations GoogleComputeGlobalForwardingRule#service_directory_registrations}
        :param source_ip_ranges: If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here. Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#source_ip_ranges GoogleComputeGlobalForwardingRule#source_ip_ranges}
        :param subnetwork: This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#subnetwork GoogleComputeGlobalForwardingRule#subnetwork}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#timeouts GoogleComputeGlobalForwardingRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be70df882a8fb64f002c7d1176f934a11211e7905d64104f64a635c5c1559e05)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeGlobalForwardingRuleConfig(
            name=name,
            target=target,
            allow_psc_global_access=allow_psc_global_access,
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
        '''Generates CDKTF code for importing a GoogleComputeGlobalForwardingRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeGlobalForwardingRule to import.
        :param import_from_id: The id of the existing GoogleComputeGlobalForwardingRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeGlobalForwardingRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc617c5e57013db08c12916c155bbbf1d5ba777c3a375398ede3e5d1ba8d959a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetadataFilters")
    def put_metadata_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeGlobalForwardingRuleMetadataFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71d694d5a5d9ecbd124b7a53904ff542b9ce904d9552cb1d4a661bb56915eed)
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
        :param namespace: Service Directory namespace to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#namespace GoogleComputeGlobalForwardingRule#namespace}
        :param service_directory_region: [Optional] Service Directory region to register this global forwarding rule under. Default to "us-central1". Only used for PSC for Google APIs. All PSC for Google APIs Forwarding Rules on the same network should use the same Service Directory region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#service_directory_region GoogleComputeGlobalForwardingRule#service_directory_region}
        '''
        value = GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#create GoogleComputeGlobalForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#delete GoogleComputeGlobalForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#update GoogleComputeGlobalForwardingRule#update}.
        '''
        value = GoogleComputeGlobalForwardingRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowPscGlobalAccess")
    def reset_allow_psc_global_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowPscGlobalAccess", []))

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
    def metadata_filters(
        self,
    ) -> "GoogleComputeGlobalForwardingRuleMetadataFiltersList":
        return typing.cast("GoogleComputeGlobalForwardingRuleMetadataFiltersList", jsii.get(self, "metadataFilters"))

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
    ) -> "GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference":
        return typing.cast("GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference", jsii.get(self, "serviceDirectoryRegistrations"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeGlobalForwardingRuleTimeoutsOutputReference":
        return typing.cast("GoogleComputeGlobalForwardingRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allowPscGlobalAccessInput")
    def allow_psc_global_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowPscGlobalAccessInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeGlobalForwardingRuleMetadataFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeGlobalForwardingRuleMetadataFilters"]]], jsii.get(self, "metadataFiltersInput"))

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
    ) -> typing.Optional["GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations"]:
        return typing.cast(typing.Optional["GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations"], jsii.get(self, "serviceDirectoryRegistrationsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeGlobalForwardingRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeGlobalForwardingRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__10d919de68dccf45b6f4f9f2ce8af341c61ad660fb4e1376ee632d4d943ac42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowPscGlobalAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b2848f3d921b2e1de4c517be8b77a568129962aaaabe9738a249c3694fd8085)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eae11740e826eb5a73778dfbfdbcd9c7c31caa008ab2d35390d693661c5edab6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e79539297613eb60ddbb0cc161fa0b5d6616749da118d9ef32c8114f06f2d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalManagedBackendBucketMigrationTestingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff76964a94ed4dbe176705e1fb3f039ebae31c76a13f9e01daf8a20460f8b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ce87d5129bfbafaa8a45e8c49ad30fc2d2c9a1fa0c3afaa83668df4b81f320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4719a3d57037f8e47628e83db30089081332eda13f09bc4c64ed0e00dd4f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipVersion")
    def ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipVersion"))

    @ip_version.setter
    def ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d62e864360ec75c4aca38c82ff18260c8f5e1018c7f70c33b3dc740333e2fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c0b52b076db8cf444efd9e22fb0836205433a4bac69592927a65f674ed7572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc45a8b1f050d0377d309cf551c4e446fce703c1454be5f4196df5f0387ad48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82540b82afce33382e028c504769ad8ff6a8f6486932c9f0c508147fa8358d9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a59df00c85b50a0378a58a79eddf615115d69ed6687c37b2de5a4618e162a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeaac2efb60e00a86688cfdfecdbd3e55f1b77064a0c499cd24273eacea97e13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ae5394233e788f5efac04e927027090013123ab34cfa864878757c4dd176160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAutomateDnsZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portRange")
    def port_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portRange"))

    @port_range.setter
    def port_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12ed137428f9a01fad4b9d15230f880f59ff9b86964190f8503e3b240c36484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d7bb6751a6c665398aecaf2807fcf40a8d9ca66edb99be47fd712d2fef8209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceIpRanges")
    def source_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceIpRanges"))

    @source_ip_ranges.setter
    def source_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd5f6ae9bb11bddb920a80283539b88893b6a1b5091ff08b482454ebaf22df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1be4d44fecf776113880b15935aaa1290ff057c4795968cfc213d109cdfb2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf81f0523161e24324ce52f63d8ad0c445866071810a567d27c0e52e335a932b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleConfig",
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
        "allow_psc_global_access": "allowPscGlobalAccess",
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
class GoogleComputeGlobalForwardingRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allow_psc_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        external_managed_backend_bucket_migration_state: typing.Optional[builtins.str] = None,
        external_managed_backend_bucket_migration_testing_percentage: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeGlobalForwardingRuleMetadataFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
        no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port_range: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        service_directory_registrations: typing.Optional[typing.Union["GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations", typing.Dict[builtins.str, typing.Any]]] = None,
        source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeGlobalForwardingRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`_. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. For Private Service Connect forwarding rules that forward traffic to Google APIs, the forwarding rule name must be a 1-20 characters string with lowercase letters and numbers and must start with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#name GoogleComputeGlobalForwardingRule#name}
        :param target: The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. - For load balancers, see the "Target" column in `Port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - 'vpc-sc' - ` APIs that support VPC Service Controls <https://cloud.google.com/vpc-service-controls/docs/supported-products>`_. - 'all-apis' - `All supported Google APIs <https://cloud.google.com/vpc/docs/private-service-connect#supported-apis>`_. For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#target GoogleComputeGlobalForwardingRule#target}
        :param allow_psc_global_access: This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#allow_psc_global_access GoogleComputeGlobalForwardingRule#allow_psc_global_access}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#description GoogleComputeGlobalForwardingRule#description}
        :param external_managed_backend_bucket_migration_state: Specifies the canary migration state for the backend buckets attached to this forwarding rule. Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC. To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate traffic to backend buckets attached to this forwarding rule by percentage using externalManagedBackendBucketMigrationTestingPercentage. Rolling back a migration requires the states to be set in reverse order. So changing the scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#external_managed_backend_bucket_migration_state GoogleComputeGlobalForwardingRule#external_managed_backend_bucket_migration_state}
        :param external_managed_backend_bucket_migration_testing_percentage: Determines the fraction of requests to backend buckets that should be processed by the Global external Application Load Balancer. The value of this field must be in the range [0, 100]. This value can only be set if the loadBalancingScheme in the forwarding rule is set to EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#external_managed_backend_bucket_migration_testing_percentage GoogleComputeGlobalForwardingRule#external_managed_backend_bucket_migration_testing_percentage}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#id GoogleComputeGlobalForwardingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced 'target'. While creating a forwarding rule, specifying an 'IPAddress' is required under the following circumstances: - When the 'target' is set to 'targetGrpcProxy' and 'validateForProxyless' is set to 'true', the 'IPAddress' should be set to '0.0.0.0'. - When the 'target' is a Private Service Connect Google APIs bundle, you must specify an 'IPAddress'. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: - IP address number, as in '100.1.2.3' - IPv6 address range, as in '2600:1234::/96' - Full resource URL, as in 'https://www.googleapis.com/compute/v1/projects/project_id/regions/region/addresses/address-name' - Partial URL or by name, as in: - 'projects/project_id/regions/region/addresses/address-name' - 'regions/region/addresses/address-name' - 'global/addresses/address-name' - 'address-name' The forwarding rule's 'target', and in most cases, also the 'loadBalancingScheme', determine the type of IP address that you can use. For detailed information, see `IP address specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications>`_. When reading an 'IPAddress', the API always returns the IP address number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#ip_address GoogleComputeGlobalForwardingRule#ip_address}
        :param ip_protocol: The IP protocol to which this rule applies. For protocol forwarding, valid options are 'TCP', 'UDP', 'ESP', 'AH', 'SCTP', 'ICMP' and 'L3_DEFAULT'. The valid IP protocols are different for different load balancing products as described in `Load balancing features <https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends>`_. Possible values: ["TCP", "UDP", "ESP", "AH", "SCTP", "ICMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#ip_protocol GoogleComputeGlobalForwardingRule#ip_protocol}
        :param ip_version: The IP Version that will be used by this global forwarding rule. Possible values: ["IPV4", "IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#ip_version GoogleComputeGlobalForwardingRule#ip_version}
        :param labels: Labels to apply to this forwarding rule. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#labels GoogleComputeGlobalForwardingRule#labels}
        :param load_balancing_scheme: Specifies the forwarding rule type. For more information about forwarding rules, refer to `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#load_balancing_scheme GoogleComputeGlobalForwardingRule#load_balancing_scheme}
        :param metadata_filters: metadata_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#metadata_filters GoogleComputeGlobalForwardingRule#metadata_filters}
        :param network: This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If the subnetwork is specified, the network of the subnetwork will be used. If neither subnetwork nor this field is specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#network GoogleComputeGlobalForwardingRule#network}
        :param network_tier: This signifies the networking tier used for configuring this load balancer and can only take the following values: 'PREMIUM', 'STANDARD'. For regional ForwardingRule, the valid values are 'PREMIUM' and 'STANDARD'. For GlobalForwardingRule, the valid value is 'PREMIUM'. If this field is not specified, it is assumed to be 'PREMIUM'. If 'IPAddress' is specified, this value must be equal to the networkTier of the Address. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#network_tier GoogleComputeGlobalForwardingRule#network_tier}
        :param no_automate_dns_zone: This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#no_automate_dns_zone GoogleComputeGlobalForwardingRule#no_automate_dns_zone}
        :param port_range: The 'portRange' field has the following limitations: * It requires that the forwarding rule 'IPProtocol' be TCP, UDP, or SCTP, and * It's applicable only to the following products: external passthrough Network Load Balancers, internal and external proxy Network Load Balancers, internal and external Application Load Balancers, external protocol forwarding, and Classic VPN. - Some products have restrictions on what ports can be used. See `port specifications <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications>`_ for details. For external forwarding rules, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's. For internal forwarding rules within the same VPC network, two or more forwarding rules cannot use the same '[IPAddress, IPProtocol]' pair, and cannot have overlapping 'portRange's.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#project GoogleComputeGlobalForwardingRule#project}.
        :param service_directory_registrations: service_directory_registrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#service_directory_registrations GoogleComputeGlobalForwardingRule#service_directory_registrations}
        :param source_ip_ranges: If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here. Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#source_ip_ranges GoogleComputeGlobalForwardingRule#source_ip_ranges}
        :param subnetwork: This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#subnetwork GoogleComputeGlobalForwardingRule#subnetwork}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#timeouts GoogleComputeGlobalForwardingRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(service_directory_registrations, dict):
            service_directory_registrations = GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations(**service_directory_registrations)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeGlobalForwardingRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5380735f39b058ca13330bb23d15e4c2572c147d965421a816b6a0a62ec5bbb3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument allow_psc_global_access", value=allow_psc_global_access, expected_type=type_hints["allow_psc_global_access"])
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
        if allow_psc_global_access is not None:
            self._values["allow_psc_global_access"] = allow_psc_global_access
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#name GoogleComputeGlobalForwardingRule#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#target GoogleComputeGlobalForwardingRule#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_psc_global_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#allow_psc_global_access GoogleComputeGlobalForwardingRule#allow_psc_global_access}
        '''
        result = self._values.get("allow_psc_global_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#description GoogleComputeGlobalForwardingRule#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#external_managed_backend_bucket_migration_state GoogleComputeGlobalForwardingRule#external_managed_backend_bucket_migration_state}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#external_managed_backend_bucket_migration_testing_percentage GoogleComputeGlobalForwardingRule#external_managed_backend_bucket_migration_testing_percentage}
        '''
        result = self._values.get("external_managed_backend_bucket_migration_testing_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#id GoogleComputeGlobalForwardingRule#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#ip_address GoogleComputeGlobalForwardingRule#ip_address}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#ip_protocol GoogleComputeGlobalForwardingRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_version(self) -> typing.Optional[builtins.str]:
        '''The IP Version that will be used by this global forwarding rule. Possible values: ["IPV4", "IPV6"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#ip_version GoogleComputeGlobalForwardingRule#ip_version}
        '''
        result = self._values.get("ip_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this forwarding rule.  A list of key->value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#labels GoogleComputeGlobalForwardingRule#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''Specifies the forwarding rule type.

        For more information about forwarding rules, refer to
        `Forwarding rule concepts <https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#load_balancing_scheme GoogleComputeGlobalForwardingRule#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeGlobalForwardingRuleMetadataFilters"]]]:
        '''metadata_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#metadata_filters GoogleComputeGlobalForwardingRule#metadata_filters}
        '''
        result = self._values.get("metadata_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeGlobalForwardingRuleMetadataFilters"]]], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#network GoogleComputeGlobalForwardingRule#network}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#network_tier GoogleComputeGlobalForwardingRule#network_tier}
        '''
        result = self._values.get("network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_automate_dns_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not.

        Non-PSC forwarding rules do not use this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#no_automate_dns_zone GoogleComputeGlobalForwardingRule#no_automate_dns_zone}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#port_range GoogleComputeGlobalForwardingRule#port_range}
        '''
        result = self._values.get("port_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#project GoogleComputeGlobalForwardingRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_registrations(
        self,
    ) -> typing.Optional["GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations"]:
        '''service_directory_registrations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#service_directory_registrations GoogleComputeGlobalForwardingRule#service_directory_registrations}
        '''
        result = self._values.get("service_directory_registrations")
        return typing.cast(typing.Optional["GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations"], result)

    @builtins.property
    def source_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If not empty, this Forwarding Rule will only forward the traffic when the source IP address matches one of the IP addresses or CIDR ranges set here.

        Note that a Forwarding Rule can only have up to 64 source IP ranges, and this field can only be used with a regional Forwarding Rule whose scheme is EXTERNAL. Each sourceIpRange entry should be either an IP address (for example, 1.2.3.4) or a CIDR range (for example, 1.2.3.0/24).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#source_ip_ranges GoogleComputeGlobalForwardingRule#source_ip_ranges}
        '''
        result = self._values.get("source_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6.

        If the network specified is in auto subnet mode, this field is optional.
        However, a subnetwork must be specified if the network is in custom subnet
        mode or when creating external forwarding rule with IPv6.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#subnetwork GoogleComputeGlobalForwardingRule#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeGlobalForwardingRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#timeouts GoogleComputeGlobalForwardingRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeGlobalForwardingRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeGlobalForwardingRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleMetadataFilters",
    jsii_struct_bases=[],
    name_mapping={
        "filter_labels": "filterLabels",
        "filter_match_criteria": "filterMatchCriteria",
    },
)
class GoogleComputeGlobalForwardingRuleMetadataFilters:
    def __init__(
        self,
        *,
        filter_labels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels", typing.Dict[builtins.str, typing.Any]]]],
        filter_match_criteria: builtins.str,
    ) -> None:
        '''
        :param filter_labels: filter_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#filter_labels GoogleComputeGlobalForwardingRule#filter_labels}
        :param filter_match_criteria: Specifies how individual filterLabel matches within the list of filterLabels contribute towards the overall metadataFilter match. MATCH_ANY - At least one of the filterLabels must have a matching label in the provided metadata. MATCH_ALL - All filterLabels must have matching labels in the provided metadata. Possible values: ["MATCH_ANY", "MATCH_ALL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#filter_match_criteria GoogleComputeGlobalForwardingRule#filter_match_criteria}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50584251ce0ff85d91d1910086f0eac537ded78e90a45b66e82bb3cfefa84313)
            check_type(argname="argument filter_labels", value=filter_labels, expected_type=type_hints["filter_labels"])
            check_type(argname="argument filter_match_criteria", value=filter_match_criteria, expected_type=type_hints["filter_match_criteria"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_labels": filter_labels,
            "filter_match_criteria": filter_match_criteria,
        }

    @builtins.property
    def filter_labels(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels"]]:
        '''filter_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#filter_labels GoogleComputeGlobalForwardingRule#filter_labels}
        '''
        result = self._values.get("filter_labels")
        assert result is not None, "Required property 'filter_labels' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels"]], result)

    @builtins.property
    def filter_match_criteria(self) -> builtins.str:
        '''Specifies how individual filterLabel matches within the list of filterLabels contribute towards the overall metadataFilter match.

        MATCH_ANY - At least one of the filterLabels must have a matching
        label in the provided metadata.
        MATCH_ALL - All filterLabels must have matching labels in the
        provided metadata. Possible values: ["MATCH_ANY", "MATCH_ALL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#filter_match_criteria GoogleComputeGlobalForwardingRule#filter_match_criteria}
        '''
        result = self._values.get("filter_match_criteria")
        assert result is not None, "Required property 'filter_match_criteria' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeGlobalForwardingRuleMetadataFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Name of the metadata label. The length must be between 1 and 1024 characters, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#name GoogleComputeGlobalForwardingRule#name}
        :param value: The value that the label must match. The value has a maximum length of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#value GoogleComputeGlobalForwardingRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5871d7a6ec591c77c64c0dbe3742ad404c5144b0ab45bca6dbd2393dd3715ac7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the metadata label. The length must be between 1 and 1024 characters, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#name GoogleComputeGlobalForwardingRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value that the label must match. The value has a maximum length of 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#value GoogleComputeGlobalForwardingRule#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__950e159f2f25fc6d9ea6369aac973710b9427bf52664e77831d2bf904e2dd14c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c63ee0abf192b6c44e8e893b362d755bb879cb44d45272a49cdb1d02d28e4fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe37b4eb673d0f8957afc9ecd2ea5cce2313cc8b918abfcd50b7ca8fbd4f6fd9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c75996915b8c8bdd11870086bbe4ee015abbc0397636f0a0cb196a9e167fd4f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f2d2b967f7ab5f2b4cecb8c97857b5f7bdf73f5c5ad969ec81aa6dd58876170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe016d82e59fdd08da791a0affe391df699273e7dde10bb867af4e8b1f8d22c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67c55b63cf8b286e3cf4d63effe3a951a1f0fc2252d21eb2f16fcdd1f6881c9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c16d1760d39be5763b9f1d47d35d44467c76a15c5107a14237fd95f4985ce4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fcff18b2d93a3ba56cfa230bbc8ff49810be4df6fa3a36a0abf8959f8a79ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834529b4fae577daad2a5939880f90f575ea268ca93ed6231540462518394fa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeGlobalForwardingRuleMetadataFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleMetadataFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ab130ae29ba861315c0a73ea86620a35d51df2ccc51b76b798f069799be1fc1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeGlobalForwardingRuleMetadataFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c517dfb323fab6d8d860f839ad873f2783059e73cd9bbab7ca2e82d7f8167778)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeGlobalForwardingRuleMetadataFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047cb7dcec2354e194b65e911ed5b45f1d8a91b7517c4ba7a88a8a48f3ec570a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e4ae4e6155228cfb1a554a135a1c980a1c300b479cc35bac75e2cb5f140ba29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3409a5b9b9567d7cf14d71bc9cc69d8bae81995b7d50776184b02a1107d1c2cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4f8c8d355be961392f72639b26835ff1156eeb6bd7de1b968d28d1f922662c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeGlobalForwardingRuleMetadataFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleMetadataFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43ad85755e6ae62dba3223e91c603d1b88bfccc1ba60d99eb064a32ee3b7b5f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilterLabels")
    def put_filter_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a66b8083b646c5826b5769dad4712d77acff74dbf486fd06221e7d789d4808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilterLabels", [value]))

    @builtins.property
    @jsii.member(jsii_name="filterLabels")
    def filter_labels(
        self,
    ) -> GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList:
        return typing.cast(GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList, jsii.get(self, "filterLabels"))

    @builtins.property
    @jsii.member(jsii_name="filterLabelsInput")
    def filter_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]], jsii.get(self, "filterLabelsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a90c783dd1ec1f606e301020a821ad9c30935e9ee2da185740f25e3095426e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterMatchCriteria", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleMetadataFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleMetadataFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleMetadataFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c25e9eea6fb2ce7b3b5da70ce5225acf7a5c76aa4da0106c4a9c04fdc784f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations",
    jsii_struct_bases=[],
    name_mapping={
        "namespace": "namespace",
        "service_directory_region": "serviceDirectoryRegion",
    },
)
class GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations:
    def __init__(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        service_directory_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace: Service Directory namespace to register the forwarding rule under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#namespace GoogleComputeGlobalForwardingRule#namespace}
        :param service_directory_region: [Optional] Service Directory region to register this global forwarding rule under. Default to "us-central1". Only used for PSC for Google APIs. All PSC for Google APIs Forwarding Rules on the same network should use the same Service Directory region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#service_directory_region GoogleComputeGlobalForwardingRule#service_directory_region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11801855b8521a9e133285b614c7cfbcc37e492c26115466c3256bffe7ba6e7a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#namespace GoogleComputeGlobalForwardingRule#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_region(self) -> typing.Optional[builtins.str]:
        '''[Optional] Service Directory region to register this global forwarding rule under.

        Default to "us-central1". Only used for PSC for Google APIs. All PSC for
        Google APIs Forwarding Rules on the same network should use the same Service
        Directory region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#service_directory_region GoogleComputeGlobalForwardingRule#service_directory_region}
        '''
        result = self._values.get("service_directory_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b8c7037bd991a4b58f319fceb766fd280c53e1fbd49516574e71d3ab393aeff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1852137651e8ab5c7dff7352fd08278407728b424111b4342eb42d7dff08bb7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryRegion")
    def service_directory_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceDirectoryRegion"))

    @service_directory_region.setter
    def service_directory_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fbbe82fa9f51fd00f5c9759123bc47a1ef6858b11a3971d75602e14af28677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceDirectoryRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations]:
        return typing.cast(typing.Optional[GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162a1190e656d67799b3a75a3a67ef8f3465523b2883a175edb09c7feec1dc78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeGlobalForwardingRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#create GoogleComputeGlobalForwardingRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#delete GoogleComputeGlobalForwardingRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#update GoogleComputeGlobalForwardingRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b16980694661717758faf57aa557743685748a82b59ce6e57c375018f6b89e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#create GoogleComputeGlobalForwardingRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#delete GoogleComputeGlobalForwardingRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_global_forwarding_rule#update GoogleComputeGlobalForwardingRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeGlobalForwardingRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeGlobalForwardingRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeGlobalForwardingRule.GoogleComputeGlobalForwardingRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bfb7a215cb4bdc4f90264ae4f532be3dfd947e5c9db755de4c77f0943e40582)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40cc36e76b2fad84b014487104f087113e0edd70c2db4e4685aac2533634c14f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1aaf794885fbe4e69ee5fd4af2e692cc19865f79de225be58f7c2fd1ba7c23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31161208ce219b0060caec8470a0c634559087ca6db11dec0d6a249405ae8c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f27691c9ccca22f9ca00595ff169e21d06ca7c4d62f22eeac25472ad8fa6d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeGlobalForwardingRule",
    "GoogleComputeGlobalForwardingRuleConfig",
    "GoogleComputeGlobalForwardingRuleMetadataFilters",
    "GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels",
    "GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsList",
    "GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabelsOutputReference",
    "GoogleComputeGlobalForwardingRuleMetadataFiltersList",
    "GoogleComputeGlobalForwardingRuleMetadataFiltersOutputReference",
    "GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations",
    "GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrationsOutputReference",
    "GoogleComputeGlobalForwardingRuleTimeouts",
    "GoogleComputeGlobalForwardingRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__be70df882a8fb64f002c7d1176f934a11211e7905d64104f64a635c5c1559e05(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    target: builtins.str,
    allow_psc_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    external_managed_backend_bucket_migration_state: typing.Optional[builtins.str] = None,
    external_managed_backend_bucket_migration_testing_percentage: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeGlobalForwardingRuleMetadataFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
    no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port_range: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    service_directory_registrations: typing.Optional[typing.Union[GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations, typing.Dict[builtins.str, typing.Any]]] = None,
    source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeGlobalForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dc617c5e57013db08c12916c155bbbf1d5ba777c3a375398ede3e5d1ba8d959a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71d694d5a5d9ecbd124b7a53904ff542b9ce904d9552cb1d4a661bb56915eed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeGlobalForwardingRuleMetadataFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d919de68dccf45b6f4f9f2ce8af341c61ad660fb4e1376ee632d4d943ac42b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2848f3d921b2e1de4c517be8b77a568129962aaaabe9738a249c3694fd8085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae11740e826eb5a73778dfbfdbcd9c7c31caa008ab2d35390d693661c5edab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e79539297613eb60ddbb0cc161fa0b5d6616749da118d9ef32c8114f06f2d3e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff76964a94ed4dbe176705e1fb3f039ebae31c76a13f9e01daf8a20460f8b09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ce87d5129bfbafaa8a45e8c49ad30fc2d2c9a1fa0c3afaa83668df4b81f320(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4719a3d57037f8e47628e83db30089081332eda13f09bc4c64ed0e00dd4f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d62e864360ec75c4aca38c82ff18260c8f5e1018c7f70c33b3dc740333e2fc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c0b52b076db8cf444efd9e22fb0836205433a4bac69592927a65f674ed7572(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc45a8b1f050d0377d309cf551c4e446fce703c1454be5f4196df5f0387ad48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82540b82afce33382e028c504769ad8ff6a8f6486932c9f0c508147fa8358d9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a59df00c85b50a0378a58a79eddf615115d69ed6687c37b2de5a4618e162a4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeaac2efb60e00a86688cfdfecdbd3e55f1b77064a0c499cd24273eacea97e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae5394233e788f5efac04e927027090013123ab34cfa864878757c4dd176160(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12ed137428f9a01fad4b9d15230f880f59ff9b86964190f8503e3b240c36484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d7bb6751a6c665398aecaf2807fcf40a8d9ca66edb99be47fd712d2fef8209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd5f6ae9bb11bddb920a80283539b88893b6a1b5091ff08b482454ebaf22df5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1be4d44fecf776113880b15935aaa1290ff057c4795968cfc213d109cdfb2ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf81f0523161e24324ce52f63d8ad0c445866071810a567d27c0e52e335a932b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5380735f39b058ca13330bb23d15e4c2572c147d965421a816b6a0a62ec5bbb3(
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
    allow_psc_global_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    external_managed_backend_bucket_migration_state: typing.Optional[builtins.str] = None,
    external_managed_backend_bucket_migration_testing_percentage: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    metadata_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeGlobalForwardingRuleMetadataFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
    no_automate_dns_zone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port_range: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    service_directory_registrations: typing.Optional[typing.Union[GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations, typing.Dict[builtins.str, typing.Any]]] = None,
    source_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeGlobalForwardingRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50584251ce0ff85d91d1910086f0eac537ded78e90a45b66e82bb3cfefa84313(
    *,
    filter_labels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels, typing.Dict[builtins.str, typing.Any]]]],
    filter_match_criteria: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5871d7a6ec591c77c64c0dbe3742ad404c5144b0ab45bca6dbd2393dd3715ac7(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950e159f2f25fc6d9ea6369aac973710b9427bf52664e77831d2bf904e2dd14c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c63ee0abf192b6c44e8e893b362d755bb879cb44d45272a49cdb1d02d28e4fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe37b4eb673d0f8957afc9ecd2ea5cce2313cc8b918abfcd50b7ca8fbd4f6fd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75996915b8c8bdd11870086bbe4ee015abbc0397636f0a0cb196a9e167fd4f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2d2b967f7ab5f2b4cecb8c97857b5f7bdf73f5c5ad969ec81aa6dd58876170(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe016d82e59fdd08da791a0affe391df699273e7dde10bb867af4e8b1f8d22c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c55b63cf8b286e3cf4d63effe3a951a1f0fc2252d21eb2f16fcdd1f6881c9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c16d1760d39be5763b9f1d47d35d44467c76a15c5107a14237fd95f4985ce4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fcff18b2d93a3ba56cfa230bbc8ff49810be4df6fa3a36a0abf8959f8a79ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834529b4fae577daad2a5939880f90f575ea268ca93ed6231540462518394fa4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab130ae29ba861315c0a73ea86620a35d51df2ccc51b76b798f069799be1fc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c517dfb323fab6d8d860f839ad873f2783059e73cd9bbab7ca2e82d7f8167778(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047cb7dcec2354e194b65e911ed5b45f1d8a91b7517c4ba7a88a8a48f3ec570a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4ae4e6155228cfb1a554a135a1c980a1c300b479cc35bac75e2cb5f140ba29(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3409a5b9b9567d7cf14d71bc9cc69d8bae81995b7d50776184b02a1107d1c2cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4f8c8d355be961392f72639b26835ff1156eeb6bd7de1b968d28d1f922662c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeGlobalForwardingRuleMetadataFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ad85755e6ae62dba3223e91c603d1b88bfccc1ba60d99eb064a32ee3b7b5f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a66b8083b646c5826b5769dad4712d77acff74dbf486fd06221e7d789d4808(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeGlobalForwardingRuleMetadataFiltersFilterLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90c783dd1ec1f606e301020a821ad9c30935e9ee2da185740f25e3095426e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c25e9eea6fb2ce7b3b5da70ce5225acf7a5c76aa4da0106c4a9c04fdc784f18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleMetadataFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11801855b8521a9e133285b614c7cfbcc37e492c26115466c3256bffe7ba6e7a(
    *,
    namespace: typing.Optional[builtins.str] = None,
    service_directory_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8c7037bd991a4b58f319fceb766fd280c53e1fbd49516574e71d3ab393aeff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1852137651e8ab5c7dff7352fd08278407728b424111b4342eb42d7dff08bb7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fbbe82fa9f51fd00f5c9759123bc47a1ef6858b11a3971d75602e14af28677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162a1190e656d67799b3a75a3a67ef8f3465523b2883a175edb09c7feec1dc78(
    value: typing.Optional[GoogleComputeGlobalForwardingRuleServiceDirectoryRegistrations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b16980694661717758faf57aa557743685748a82b59ce6e57c375018f6b89e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bfb7a215cb4bdc4f90264ae4f532be3dfd947e5c9db755de4c77f0943e40582(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cc36e76b2fad84b014487104f087113e0edd70c2db4e4685aac2533634c14f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1aaf794885fbe4e69ee5fd4af2e692cc19865f79de225be58f7c2fd1ba7c23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31161208ce219b0060caec8470a0c634559087ca6db11dec0d6a249405ae8c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f27691c9ccca22f9ca00595ff169e21d06ca7c4d62f22eeac25472ad8fa6d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeGlobalForwardingRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
