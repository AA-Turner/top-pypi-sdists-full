r'''
# `google_compute_region_network_firewall_policy_rule`

Refer to the Terraform Registry for docs: [`google_compute_region_network_firewall_policy_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule).
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


class ComputeRegionNetworkFirewallPolicyRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule google_compute_region_network_firewall_policy_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        direction: builtins.str,
        firewall_policy: builtins.str,
        match: typing.Union["ComputeRegionNetworkFirewallPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_profile_group: typing.Optional[builtins.str] = None,
        target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionNetworkFirewallPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule google_compute_region_network_firewall_policy_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: The Action to perform when the client connection triggers the rule. Valid actions are "allow", "deny", "goto_next" and "apply_security_profile_group". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#action ComputeRegionNetworkFirewallPolicyRule#action}
        :param direction: The direction in which this rule applies. Possible values: ["INGRESS", "EGRESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#direction ComputeRegionNetworkFirewallPolicyRule#direction}
        :param firewall_policy: The firewall policy of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#firewall_policy ComputeRegionNetworkFirewallPolicyRule#firewall_policy}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#match ComputeRegionNetworkFirewallPolicyRule#match}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#priority ComputeRegionNetworkFirewallPolicyRule#priority}
        :param description: An optional description for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#description ComputeRegionNetworkFirewallPolicyRule#description}
        :param disabled: Denotes whether the firewall policy rule is disabled. When set to true, the firewall policy rule is not enforced and traffic behaves as if it did not exist. If this is unspecified, the firewall policy rule will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#disabled ComputeRegionNetworkFirewallPolicyRule#disabled}
        :param enable_logging: Denotes whether to enable logging for a particular rule. If logging is enabled, logs will be exported to the configured export destination in Stackdriver. Logs may be exported to BigQuery or Pub/Sub. Note: you cannot enable logging on "goto_next" rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#enable_logging ComputeRegionNetworkFirewallPolicyRule#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#id ComputeRegionNetworkFirewallPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#project ComputeRegionNetworkFirewallPolicyRule#project}.
        :param region: The location of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#region ComputeRegionNetworkFirewallPolicyRule#region}
        :param rule_name: An optional name for the rule. This field is not a unique identifier and can be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#rule_name ComputeRegionNetworkFirewallPolicyRule#rule_name}
        :param security_profile_group: A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action = 'apply_security_profile_group' and cannot be specified for other actions. Security Profile Group and Firewall Policy Rule must be in the same scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#security_profile_group ComputeRegionNetworkFirewallPolicyRule#security_profile_group}
        :param target_secure_tags: target_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#target_secure_tags ComputeRegionNetworkFirewallPolicyRule#target_secure_tags}
        :param target_service_accounts: A list of service accounts indicating the sets of instances that are applied with this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#target_service_accounts ComputeRegionNetworkFirewallPolicyRule#target_service_accounts}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#timeouts ComputeRegionNetworkFirewallPolicyRule#timeouts}
        :param tls_inspect: Boolean flag indicating if the traffic should be TLS decrypted. Can be set only if action = 'apply_security_profile_group' and cannot be set for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#tls_inspect ComputeRegionNetworkFirewallPolicyRule#tls_inspect}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094a67dce9735141914cf28f8d4d4694f1ea76eb4299dd070796590035d0272e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionNetworkFirewallPolicyRuleConfig(
            action=action,
            direction=direction,
            firewall_policy=firewall_policy,
            match=match,
            priority=priority,
            description=description,
            disabled=disabled,
            enable_logging=enable_logging,
            id=id,
            project=project,
            region=region,
            rule_name=rule_name,
            security_profile_group=security_profile_group,
            target_secure_tags=target_secure_tags,
            target_service_accounts=target_service_accounts,
            timeouts=timeouts,
            tls_inspect=tls_inspect,
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
        '''Generates CDKTF code for importing a ComputeRegionNetworkFirewallPolicyRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionNetworkFirewallPolicyRule to import.
        :param import_from_id: The id of the existing ComputeRegionNetworkFirewallPolicyRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionNetworkFirewallPolicyRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8ee88f3aaa685921d5d4115382688f0fa73fd8e0939f0b462f64576e02b046)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        layer4_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs", typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_configs: layer4_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#layer4_configs ComputeRegionNetworkFirewallPolicyRule#layer4_configs}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_address_groups ComputeRegionNetworkFirewallPolicyRule#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_fqdns ComputeRegionNetworkFirewallPolicyRule#dest_fqdns}
        :param dest_ip_ranges: CIDR IP address range. Maximum number of destination CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_ip_ranges ComputeRegionNetworkFirewallPolicyRule#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of dest region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_region_codes ComputeRegionNetworkFirewallPolicyRule#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_threat_intelligences ComputeRegionNetworkFirewallPolicyRule#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_address_groups ComputeRegionNetworkFirewallPolicyRule#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_fqdns ComputeRegionNetworkFirewallPolicyRule#src_fqdns}
        :param src_ip_ranges: CIDR IP address range. Maximum number of source CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_ip_ranges ComputeRegionNetworkFirewallPolicyRule#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_region_codes ComputeRegionNetworkFirewallPolicyRule#src_region_codes}
        :param src_secure_tags: src_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_secure_tags ComputeRegionNetworkFirewallPolicyRule#src_secure_tags}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_threat_intelligences ComputeRegionNetworkFirewallPolicyRule#src_threat_intelligences}
        '''
        value = ComputeRegionNetworkFirewallPolicyRuleMatch(
            layer4_configs=layer4_configs,
            dest_address_groups=dest_address_groups,
            dest_fqdns=dest_fqdns,
            dest_ip_ranges=dest_ip_ranges,
            dest_region_codes=dest_region_codes,
            dest_threat_intelligences=dest_threat_intelligences,
            src_address_groups=src_address_groups,
            src_fqdns=src_fqdns,
            src_ip_ranges=src_ip_ranges,
            src_region_codes=src_region_codes,
            src_secure_tags=src_secure_tags,
            src_threat_intelligences=src_threat_intelligences,
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putTargetSecureTags")
    def put_target_secure_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d631ed295f5bae188acb242b0c0998b22083f4afb76a65d0a98f84006250a24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetSecureTags", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#create ComputeRegionNetworkFirewallPolicyRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#delete ComputeRegionNetworkFirewallPolicyRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#update ComputeRegionNetworkFirewallPolicyRule#update}.
        '''
        value = ComputeRegionNetworkFirewallPolicyRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetEnableLogging")
    def reset_enable_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLogging", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRuleName")
    def reset_rule_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleName", []))

    @jsii.member(jsii_name="resetSecurityProfileGroup")
    def reset_security_profile_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityProfileGroup", []))

    @jsii.member(jsii_name="resetTargetSecureTags")
    def reset_target_secure_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetSecureTags", []))

    @jsii.member(jsii_name="resetTargetServiceAccounts")
    def reset_target_service_accounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetServiceAccounts", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTlsInspect")
    def reset_tls_inspect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsInspect", []))

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
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> "ComputeRegionNetworkFirewallPolicyRuleMatchOutputReference":
        return typing.cast("ComputeRegionNetworkFirewallPolicyRuleMatchOutputReference", jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="ruleTupleCount")
    def rule_tuple_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleTupleCount"))

    @builtins.property
    @jsii.member(jsii_name="targetSecureTags")
    def target_secure_tags(
        self,
    ) -> "ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsList":
        return typing.cast("ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsList", jsii.get(self, "targetSecureTags"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "ComputeRegionNetworkFirewallPolicyRuleTimeoutsOutputReference":
        return typing.cast("ComputeRegionNetworkFirewallPolicyRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLoggingInput")
    def enable_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyInput")
    def firewall_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional["ComputeRegionNetworkFirewallPolicyRuleMatch"]:
        return typing.cast(typing.Optional["ComputeRegionNetworkFirewallPolicyRuleMatch"], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileGroupInput")
    def security_profile_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityProfileGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSecureTagsInput")
    def target_secure_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags"]]], jsii.get(self, "targetSecureTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetServiceAccountsInput")
    def target_service_accounts_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetServiceAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionNetworkFirewallPolicyRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionNetworkFirewallPolicyRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInspectInput")
    def tls_inspect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsInspectInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6feeee79faba1fa75a5dbc196033e4cc4d754558ce794da4dcf6b4ad8676bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ea652ed9018dc61ff48e13a2d90d20a19581a046fe9bdb769dc2d6a923af85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5b8a45d4a0c5f950076f46a26161d19edb99cae2919f6bf7b02a2ad18c33b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ce7707520e98a50d395fa5a25813f92ed7751b36235fe7700f8378823e42fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableLogging")
    def enable_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLogging"))

    @enable_logging.setter
    def enable_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfd259e951e3fdd768d1535be2049eda37a33f5da52a9c06f27f9fdbfcc592e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firewallPolicy")
    def firewall_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicy"))

    @firewall_policy.setter
    def firewall_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f8d9cc9274e6e8c71c65677e48560dd161886b4277b5885d7e7a8079ba847f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973716c2bc5be8474975f7b6d30d02705f62767f3a3dd8992aefb79bbf05558b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc0ca1c7714523c66cca6604f9769f712428d64550e23b2ccfeca4763348c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845bb68b6a216b18023e27363d061cc386894495a6bc5d443bfe333a4994f265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fe1f7e5a202eb932ef4370fd0f79fe0a6b049542f3ad03cc085ceffad0d0ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6117955970c7490fff28a48585e6ea8b1915a87499d34ec70d946cc0f8366ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityProfileGroup")
    def security_profile_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProfileGroup"))

    @security_profile_group.setter
    def security_profile_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7688d941514cccffbb9cee6fb88f3ef102173a2ed49db5eda79ace86c262279c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProfileGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetServiceAccounts")
    def target_service_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetServiceAccounts"))

    @target_service_accounts.setter
    def target_service_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b2a0ff42a961fdc4f846cfa4412562d8a8b5ae12ee16f94fba9beab187f5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetServiceAccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsInspect")
    def tls_inspect(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsInspect"))

    @tls_inspect.setter
    def tls_inspect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e3113ed4300feffef095c18ba4dde2f4efa6be8a33ce17734868a95c044830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsInspect", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action": "action",
        "direction": "direction",
        "firewall_policy": "firewallPolicy",
        "match": "match",
        "priority": "priority",
        "description": "description",
        "disabled": "disabled",
        "enable_logging": "enableLogging",
        "id": "id",
        "project": "project",
        "region": "region",
        "rule_name": "ruleName",
        "security_profile_group": "securityProfileGroup",
        "target_secure_tags": "targetSecureTags",
        "target_service_accounts": "targetServiceAccounts",
        "timeouts": "timeouts",
        "tls_inspect": "tlsInspect",
    },
)
class ComputeRegionNetworkFirewallPolicyRuleConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        action: builtins.str,
        direction: builtins.str,
        firewall_policy: builtins.str,
        match: typing.Union["ComputeRegionNetworkFirewallPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_profile_group: typing.Optional[builtins.str] = None,
        target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionNetworkFirewallPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: The Action to perform when the client connection triggers the rule. Valid actions are "allow", "deny", "goto_next" and "apply_security_profile_group". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#action ComputeRegionNetworkFirewallPolicyRule#action}
        :param direction: The direction in which this rule applies. Possible values: ["INGRESS", "EGRESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#direction ComputeRegionNetworkFirewallPolicyRule#direction}
        :param firewall_policy: The firewall policy of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#firewall_policy ComputeRegionNetworkFirewallPolicyRule#firewall_policy}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#match ComputeRegionNetworkFirewallPolicyRule#match}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#priority ComputeRegionNetworkFirewallPolicyRule#priority}
        :param description: An optional description for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#description ComputeRegionNetworkFirewallPolicyRule#description}
        :param disabled: Denotes whether the firewall policy rule is disabled. When set to true, the firewall policy rule is not enforced and traffic behaves as if it did not exist. If this is unspecified, the firewall policy rule will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#disabled ComputeRegionNetworkFirewallPolicyRule#disabled}
        :param enable_logging: Denotes whether to enable logging for a particular rule. If logging is enabled, logs will be exported to the configured export destination in Stackdriver. Logs may be exported to BigQuery or Pub/Sub. Note: you cannot enable logging on "goto_next" rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#enable_logging ComputeRegionNetworkFirewallPolicyRule#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#id ComputeRegionNetworkFirewallPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#project ComputeRegionNetworkFirewallPolicyRule#project}.
        :param region: The location of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#region ComputeRegionNetworkFirewallPolicyRule#region}
        :param rule_name: An optional name for the rule. This field is not a unique identifier and can be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#rule_name ComputeRegionNetworkFirewallPolicyRule#rule_name}
        :param security_profile_group: A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action = 'apply_security_profile_group' and cannot be specified for other actions. Security Profile Group and Firewall Policy Rule must be in the same scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#security_profile_group ComputeRegionNetworkFirewallPolicyRule#security_profile_group}
        :param target_secure_tags: target_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#target_secure_tags ComputeRegionNetworkFirewallPolicyRule#target_secure_tags}
        :param target_service_accounts: A list of service accounts indicating the sets of instances that are applied with this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#target_service_accounts ComputeRegionNetworkFirewallPolicyRule#target_service_accounts}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#timeouts ComputeRegionNetworkFirewallPolicyRule#timeouts}
        :param tls_inspect: Boolean flag indicating if the traffic should be TLS decrypted. Can be set only if action = 'apply_security_profile_group' and cannot be set for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#tls_inspect ComputeRegionNetworkFirewallPolicyRule#tls_inspect}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(match, dict):
            match = ComputeRegionNetworkFirewallPolicyRuleMatch(**match)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionNetworkFirewallPolicyRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2454b24e5c79c921860a4259e0f54a81c0f1bfe6b97e2cef1f3dbbe99e4f703d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument firewall_policy", value=firewall_policy, expected_type=type_hints["firewall_policy"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument security_profile_group", value=security_profile_group, expected_type=type_hints["security_profile_group"])
            check_type(argname="argument target_secure_tags", value=target_secure_tags, expected_type=type_hints["target_secure_tags"])
            check_type(argname="argument target_service_accounts", value=target_service_accounts, expected_type=type_hints["target_service_accounts"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tls_inspect", value=tls_inspect, expected_type=type_hints["tls_inspect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "direction": direction,
            "firewall_policy": firewall_policy,
            "match": match,
            "priority": priority,
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
        if disabled is not None:
            self._values["disabled"] = disabled
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if security_profile_group is not None:
            self._values["security_profile_group"] = security_profile_group
        if target_secure_tags is not None:
            self._values["target_secure_tags"] = target_secure_tags
        if target_service_accounts is not None:
            self._values["target_service_accounts"] = target_service_accounts
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tls_inspect is not None:
            self._values["tls_inspect"] = tls_inspect

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
    def action(self) -> builtins.str:
        '''The Action to perform when the client connection triggers the rule. Valid actions are "allow", "deny", "goto_next" and "apply_security_profile_group".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#action ComputeRegionNetworkFirewallPolicyRule#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def direction(self) -> builtins.str:
        '''The direction in which this rule applies. Possible values: ["INGRESS", "EGRESS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#direction ComputeRegionNetworkFirewallPolicyRule#direction}
        '''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def firewall_policy(self) -> builtins.str:
        '''The firewall policy of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#firewall_policy ComputeRegionNetworkFirewallPolicyRule#firewall_policy}
        '''
        result = self._values.get("firewall_policy")
        assert result is not None, "Required property 'firewall_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(self) -> "ComputeRegionNetworkFirewallPolicyRuleMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#match ComputeRegionNetworkFirewallPolicyRule#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("ComputeRegionNetworkFirewallPolicyRuleMatch", result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An integer indicating the priority of a rule in the list.

        The priority must be a positive value between 0 and 2147483647.
        Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#priority ComputeRegionNetworkFirewallPolicyRule#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#description ComputeRegionNetworkFirewallPolicyRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes whether the firewall policy rule is disabled.

        When set to true, the firewall policy rule is not enforced and traffic behaves as if it did not exist.
        If this is unspecified, the firewall policy rule will be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#disabled ComputeRegionNetworkFirewallPolicyRule#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes whether to enable logging for a particular rule.

        If logging is enabled, logs will be exported to the configured export destination in Stackdriver.
        Logs may be exported to BigQuery or Pub/Sub.
        Note: you cannot enable logging on "goto_next" rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#enable_logging ComputeRegionNetworkFirewallPolicyRule#enable_logging}
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#id ComputeRegionNetworkFirewallPolicyRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#project ComputeRegionNetworkFirewallPolicyRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The location of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#region ComputeRegionNetworkFirewallPolicyRule#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the rule. This field is not a unique identifier and can be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#rule_name ComputeRegionNetworkFirewallPolicyRule#rule_name}
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_profile_group(self) -> typing.Optional[builtins.str]:
        '''A fully-qualified URL of a SecurityProfile resource instance.

        Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group
        Must be specified if action = 'apply_security_profile_group' and cannot be specified for other actions.

        Security Profile Group and Firewall Policy Rule must be in the same scope.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#security_profile_group ComputeRegionNetworkFirewallPolicyRule#security_profile_group}
        '''
        result = self._values.get("security_profile_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_secure_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags"]]]:
        '''target_secure_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#target_secure_tags ComputeRegionNetworkFirewallPolicyRule#target_secure_tags}
        '''
        result = self._values.get("target_secure_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags"]]], result)

    @builtins.property
    def target_service_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of service accounts indicating the sets of instances that are applied with this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#target_service_accounts ComputeRegionNetworkFirewallPolicyRule#target_service_accounts}
        '''
        result = self._values.get("target_service_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["ComputeRegionNetworkFirewallPolicyRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#timeouts ComputeRegionNetworkFirewallPolicyRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionNetworkFirewallPolicyRuleTimeouts"], result)

    @builtins.property
    def tls_inspect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean flag indicating if the traffic should be TLS decrypted.

        Can be set only if action = 'apply_security_profile_group' and cannot be set for other actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#tls_inspect ComputeRegionNetworkFirewallPolicyRule#tls_inspect}
        '''
        result = self._values.get("tls_inspect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleMatch",
    jsii_struct_bases=[],
    name_mapping={
        "layer4_configs": "layer4Configs",
        "dest_address_groups": "destAddressGroups",
        "dest_fqdns": "destFqdns",
        "dest_ip_ranges": "destIpRanges",
        "dest_region_codes": "destRegionCodes",
        "dest_threat_intelligences": "destThreatIntelligences",
        "src_address_groups": "srcAddressGroups",
        "src_fqdns": "srcFqdns",
        "src_ip_ranges": "srcIpRanges",
        "src_region_codes": "srcRegionCodes",
        "src_secure_tags": "srcSecureTags",
        "src_threat_intelligences": "srcThreatIntelligences",
    },
)
class ComputeRegionNetworkFirewallPolicyRuleMatch:
    def __init__(
        self,
        *,
        layer4_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs", typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_configs: layer4_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#layer4_configs ComputeRegionNetworkFirewallPolicyRule#layer4_configs}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_address_groups ComputeRegionNetworkFirewallPolicyRule#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_fqdns ComputeRegionNetworkFirewallPolicyRule#dest_fqdns}
        :param dest_ip_ranges: CIDR IP address range. Maximum number of destination CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_ip_ranges ComputeRegionNetworkFirewallPolicyRule#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of dest region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_region_codes ComputeRegionNetworkFirewallPolicyRule#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_threat_intelligences ComputeRegionNetworkFirewallPolicyRule#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_address_groups ComputeRegionNetworkFirewallPolicyRule#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_fqdns ComputeRegionNetworkFirewallPolicyRule#src_fqdns}
        :param src_ip_ranges: CIDR IP address range. Maximum number of source CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_ip_ranges ComputeRegionNetworkFirewallPolicyRule#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_region_codes ComputeRegionNetworkFirewallPolicyRule#src_region_codes}
        :param src_secure_tags: src_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_secure_tags ComputeRegionNetworkFirewallPolicyRule#src_secure_tags}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_threat_intelligences ComputeRegionNetworkFirewallPolicyRule#src_threat_intelligences}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6443c30c2148b7dbdfbbb55e3054c328f4a2b70a6498ad14b4a1101cea944c)
            check_type(argname="argument layer4_configs", value=layer4_configs, expected_type=type_hints["layer4_configs"])
            check_type(argname="argument dest_address_groups", value=dest_address_groups, expected_type=type_hints["dest_address_groups"])
            check_type(argname="argument dest_fqdns", value=dest_fqdns, expected_type=type_hints["dest_fqdns"])
            check_type(argname="argument dest_ip_ranges", value=dest_ip_ranges, expected_type=type_hints["dest_ip_ranges"])
            check_type(argname="argument dest_region_codes", value=dest_region_codes, expected_type=type_hints["dest_region_codes"])
            check_type(argname="argument dest_threat_intelligences", value=dest_threat_intelligences, expected_type=type_hints["dest_threat_intelligences"])
            check_type(argname="argument src_address_groups", value=src_address_groups, expected_type=type_hints["src_address_groups"])
            check_type(argname="argument src_fqdns", value=src_fqdns, expected_type=type_hints["src_fqdns"])
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
            check_type(argname="argument src_region_codes", value=src_region_codes, expected_type=type_hints["src_region_codes"])
            check_type(argname="argument src_secure_tags", value=src_secure_tags, expected_type=type_hints["src_secure_tags"])
            check_type(argname="argument src_threat_intelligences", value=src_threat_intelligences, expected_type=type_hints["src_threat_intelligences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "layer4_configs": layer4_configs,
        }
        if dest_address_groups is not None:
            self._values["dest_address_groups"] = dest_address_groups
        if dest_fqdns is not None:
            self._values["dest_fqdns"] = dest_fqdns
        if dest_ip_ranges is not None:
            self._values["dest_ip_ranges"] = dest_ip_ranges
        if dest_region_codes is not None:
            self._values["dest_region_codes"] = dest_region_codes
        if dest_threat_intelligences is not None:
            self._values["dest_threat_intelligences"] = dest_threat_intelligences
        if src_address_groups is not None:
            self._values["src_address_groups"] = src_address_groups
        if src_fqdns is not None:
            self._values["src_fqdns"] = src_fqdns
        if src_ip_ranges is not None:
            self._values["src_ip_ranges"] = src_ip_ranges
        if src_region_codes is not None:
            self._values["src_region_codes"] = src_region_codes
        if src_secure_tags is not None:
            self._values["src_secure_tags"] = src_secure_tags
        if src_threat_intelligences is not None:
            self._values["src_threat_intelligences"] = src_threat_intelligences

    @builtins.property
    def layer4_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs"]]:
        '''layer4_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#layer4_configs ComputeRegionNetworkFirewallPolicyRule#layer4_configs}
        '''
        result = self._values.get("layer4_configs")
        assert result is not None, "Required property 'layer4_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs"]], result)

    @builtins.property
    def dest_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_address_groups ComputeRegionNetworkFirewallPolicyRule#dest_address_groups}
        '''
        result = self._values.get("dest_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic destination.

        Maximum number of destination fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_fqdns ComputeRegionNetworkFirewallPolicyRule#dest_fqdns}
        '''
        result = self._values.get("dest_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of destination CIDR IP ranges allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_ip_ranges ComputeRegionNetworkFirewallPolicyRule#dest_ip_ranges}
        '''
        result = self._values.get("dest_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for destination of traffic.

        Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of dest region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_region_codes ComputeRegionNetworkFirewallPolicyRule#dest_region_codes}
        '''
        result = self._values.get("dest_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#dest_threat_intelligences ComputeRegionNetworkFirewallPolicyRule#dest_threat_intelligences}
        '''
        result = self._values.get("dest_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic source. Maximum number of source address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_address_groups ComputeRegionNetworkFirewallPolicyRule#src_address_groups}
        '''
        result = self._values.get("src_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic source.

        Maximum number of source fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_fqdns ComputeRegionNetworkFirewallPolicyRule#src_fqdns}
        '''
        result = self._values.get("src_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of source CIDR IP ranges allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_ip_ranges ComputeRegionNetworkFirewallPolicyRule#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for source of traffic.

        Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_region_codes ComputeRegionNetworkFirewallPolicyRule#src_region_codes}
        '''
        result = self._values.get("src_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_secure_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags"]]]:
        '''src_secure_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_secure_tags ComputeRegionNetworkFirewallPolicyRule#src_secure_tags}
        '''
        result = self._values.get("src_secure_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags"]]], result)

    @builtins.property
    def src_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#src_threat_intelligences ComputeRegionNetworkFirewallPolicyRule#src_threat_intelligences}
        '''
        result = self._values.get("src_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs",
    jsii_struct_bases=[],
    name_mapping={"ip_protocol": "ipProtocol", "ports": "ports"},
)
class ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs:
    def __init__(
        self,
        *,
        ip_protocol: builtins.str,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ip_protocol: The IP protocol to which this rule applies. The protocol type is required when creating a firewall rule. This value can either be one of the following well known protocol strings (tcp, udp, icmp, esp, ah, ipip, sctp), or the IP protocol number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#ip_protocol ComputeRegionNetworkFirewallPolicyRule#ip_protocol}
        :param ports: An optional list of ports to which this rule applies. This field is only applicable for UDP or TCP protocol. Each entry must be either an integer or a range. If not specified, this rule applies to connections through any port. Example inputs include: ["22"], ["80","443"], and ["12345-12349"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#ports ComputeRegionNetworkFirewallPolicyRule#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61ddbd7b35cd59bbd7ea9cf227694ddf09da33ab7a41e4f9c7f09807964b73b)
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_protocol": ip_protocol,
        }
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The IP protocol to which this rule applies.

        The protocol type is required when creating a firewall rule.
        This value can either be one of the following well known protocol strings (tcp, udp, icmp, esp, ah, ipip, sctp), or the IP protocol number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#ip_protocol ComputeRegionNetworkFirewallPolicyRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional list of ports to which this rule applies.

        This field is only applicable for UDP or TCP protocol. Each entry must be either an integer or a range. If not specified, this rule applies to connections through any port.
        Example inputs include: ["22"], ["80","443"], and ["12345-12349"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#ports ComputeRegionNetworkFirewallPolicyRule#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c6367965b55b7ae0609aec3bfa7d15d8f1a45adb7d2436341b6cfc44ed9370)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5f2bc4c18da600c270b6e47e5ae865ed6f9d89be7ebfd353156bc449cbb520)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3476019a124a0a05cbbdaee44d10465c0329754de974c002d1253ccf5c65b479)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b8f3968d02025db285de1edbb27ca5fe0b7add8dcdeee311f4bdbc2d5ed5cee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06dd0bdc9386341dfa8224c6a4bc6faa38affb84047491a333eb351f0c48570f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b677df7c5f181c293a5aa6da762e293acce507a5b33f0a72c6fc15f14f1cdf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d64117f1d87342bf483fb6f822f0b462ce5dddd83d666b0851c25b82b3e28a12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6dc59eb3a0c7c164391b13de244756bcc05cb573d090a6a569856505c21afef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddb85ae4beb245d29218df76718d6a314f1844cbda286db8e4bcc376383d260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7ebd9be5cb80dad2c00792b28e6c46e7ac19cfe3bb2f78ea3d4e029de0c6d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5f87e6be6059f5f59a8925d21d49ad9dc0b149e0682d2f18b0c320cc2ea5627)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLayer4Configs")
    def put_layer4_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47183342a5e4cd07fd064ac96bbe877c0b2c0f228c37a449ec1dd5678f7a25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLayer4Configs", [value]))

    @jsii.member(jsii_name="putSrcSecureTags")
    def put_src_secure_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798805fe766c603ba7582892c89a3379b2074dfe480c1703965a93d213605543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSrcSecureTags", [value]))

    @jsii.member(jsii_name="resetDestAddressGroups")
    def reset_dest_address_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestAddressGroups", []))

    @jsii.member(jsii_name="resetDestFqdns")
    def reset_dest_fqdns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestFqdns", []))

    @jsii.member(jsii_name="resetDestIpRanges")
    def reset_dest_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestIpRanges", []))

    @jsii.member(jsii_name="resetDestRegionCodes")
    def reset_dest_region_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestRegionCodes", []))

    @jsii.member(jsii_name="resetDestThreatIntelligences")
    def reset_dest_threat_intelligences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestThreatIntelligences", []))

    @jsii.member(jsii_name="resetSrcAddressGroups")
    def reset_src_address_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcAddressGroups", []))

    @jsii.member(jsii_name="resetSrcFqdns")
    def reset_src_fqdns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcFqdns", []))

    @jsii.member(jsii_name="resetSrcIpRanges")
    def reset_src_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcIpRanges", []))

    @jsii.member(jsii_name="resetSrcRegionCodes")
    def reset_src_region_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcRegionCodes", []))

    @jsii.member(jsii_name="resetSrcSecureTags")
    def reset_src_secure_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcSecureTags", []))

    @jsii.member(jsii_name="resetSrcThreatIntelligences")
    def reset_src_threat_intelligences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcThreatIntelligences", []))

    @builtins.property
    @jsii.member(jsii_name="layer4Configs")
    def layer4_configs(
        self,
    ) -> ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsList:
        return typing.cast(ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsList, jsii.get(self, "layer4Configs"))

    @builtins.property
    @jsii.member(jsii_name="srcSecureTags")
    def src_secure_tags(
        self,
    ) -> "ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsList":
        return typing.cast("ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsList", jsii.get(self, "srcSecureTags"))

    @builtins.property
    @jsii.member(jsii_name="destAddressGroupsInput")
    def dest_address_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destAddressGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="destFqdnsInput")
    def dest_fqdns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destFqdnsInput"))

    @builtins.property
    @jsii.member(jsii_name="destIpRangesInput")
    def dest_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="destRegionCodesInput")
    def dest_region_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destRegionCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="destThreatIntelligencesInput")
    def dest_threat_intelligences_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destThreatIntelligencesInput"))

    @builtins.property
    @jsii.member(jsii_name="layer4ConfigsInput")
    def layer4_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]]], jsii.get(self, "layer4ConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcAddressGroupsInput")
    def src_address_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcAddressGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcFqdnsInput")
    def src_fqdns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcFqdnsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcIpRangesInput")
    def src_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodesInput")
    def src_region_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcRegionCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="srcSecureTagsInput")
    def src_secure_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags"]]], jsii.get(self, "srcSecureTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcThreatIntelligencesInput")
    def src_threat_intelligences_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcThreatIntelligencesInput"))

    @builtins.property
    @jsii.member(jsii_name="destAddressGroups")
    def dest_address_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destAddressGroups"))

    @dest_address_groups.setter
    def dest_address_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b6c2772eb5ce8fbb17ad786741a9c770d25150b857158b2891eb8da7e0c4a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destFqdns")
    def dest_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destFqdns"))

    @dest_fqdns.setter
    def dest_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d260d348ab5ec364173bbecbb32d7cb4c9a0886d420c1ad6688349f21a3344b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destIpRanges")
    def dest_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destIpRanges"))

    @dest_ip_ranges.setter
    def dest_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d0944aa81843c435df6eeccff5ccf3a9e5453b81154edbad60defe7bb471b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destRegionCodes")
    def dest_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destRegionCodes"))

    @dest_region_codes.setter
    def dest_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ba4ccc333ac786e0716f8bbc3704f8c614696e4d8312d2e267e65581bf6f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destThreatIntelligences")
    def dest_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destThreatIntelligences"))

    @dest_threat_intelligences.setter
    def dest_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8123327464072925d078312ccf16dd444505f7c839c3045c21d7098b5af5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcAddressGroups")
    def src_address_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcAddressGroups"))

    @src_address_groups.setter
    def src_address_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a988c1acc37672fdbb90c14c8cf0dd129c5066cd6c66bc63f53a5bf767dfb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcFqdns")
    def src_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcFqdns"))

    @src_fqdns.setter
    def src_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60e926a8c334347e7fbe3918d34f243bc35743b932fb5730109e3c5d39580a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @src_ip_ranges.setter
    def src_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27f65ab329ff31dd92311dfd11bc49b522d881325fcdf4b28bc4c9fabcc4887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodes")
    def src_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcRegionCodes"))

    @src_region_codes.setter
    def src_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2f43601f58bbd07167cff3cb1135dc2afb2c6f5f8c983694323e04169c1bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcThreatIntelligences")
    def src_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcThreatIntelligences"))

    @src_threat_intelligences.setter
    def src_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f3bb63521b907e4520c4137d0b5138d071580aa299547a1a73e2748983d580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionNetworkFirewallPolicyRuleMatch]:
        return typing.cast(typing.Optional[ComputeRegionNetworkFirewallPolicyRuleMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkFirewallPolicyRuleMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e2ee1b1aa43274c06c52cf5591730b32e362bb72be3da80af69150640cad35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#name ComputeRegionNetworkFirewallPolicyRule#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86c1d6becc7f8465aca9eb9cfc957129f62899cf6e3b4e8ebd7265560184d67)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#name ComputeRegionNetworkFirewallPolicyRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7421b6810a3d5d78ba15f1ab55a70b28256535ff732dbe4ce9bbcdbd604720a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a89b01397ab0cbbebd2d748910280629bf7bdc1f7701033d054005595d1faf8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fd0e7b8123f01488a4d8b4b60e63bc8268484fa7fcb71148349daedb02f520)
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
            type_hints = typing.get_type_hints(_typecheckingstub__280337a8bb5802ba68504f7447ebd9227c7bb3643a45ebb0c0b4bc6a0d4a8670)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93b4ed87a0d0e8c8e6893f3a4b6ac46bafcd3e6502ce7c8cff9b113c06653603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec34fbd7f386326e42de14f8b21501105b6feb0b8c4a6adb137770a5d56bc773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7061776a5480577f454b004f32d4881a06d6c8671cd7a38d4259b30412855e4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c909070ae702da9e2e386d86b08efdcde5712ade4cc2def3c073cf513e86c2ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a8a19cbae6d870a438a39214f0230c73a991e41abbfac91d4a2330f42389ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#name ComputeRegionNetworkFirewallPolicyRule#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf379e02646774cce2d3e51b83ca82839f5929d0ae3fb08638762e716bf6ff7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#name ComputeRegionNetworkFirewallPolicyRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02b31f8567ea20b1c4cc7c5fbff8820e5b1180f129fefd3c147a659d7b04832e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2601f5e142cd66c5afc03d31fc8c64fbdfab9d84e8f32e7e83905723713e4918)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a548ce3cb18c028135307dc7ebf1452156b53e62b3490d5e0cb8c3af6b17768c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78a51282dbb663236a92aaac563191962b20470e258e47fd6132af18f7361822)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bf7f8ce165988f5d65abda5c4648875a4fc94588877e27b15fe790b40db1ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169a4b6554ec5431d729bdcc728f17074901b6e3afc3900e127a7e88caedf186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b4f36ffa0124eb1b3d6f0873945fa126f62135525d6deed13af7f3014193b63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7accb10716330f1075addef28c356c12e273c89a3aa183adb44748d2cef7d608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db1d7e72e732b188d4c5b6d7842daf4f348412c4a8428a1f4f2a1dd6d0ae652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionNetworkFirewallPolicyRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#create ComputeRegionNetworkFirewallPolicyRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#delete ComputeRegionNetworkFirewallPolicyRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#update ComputeRegionNetworkFirewallPolicyRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdde3f92e7f31ee3c0d3f88f304cc063188d23eafd7d4742d8ed7b2b60e8a17a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#create ComputeRegionNetworkFirewallPolicyRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#delete ComputeRegionNetworkFirewallPolicyRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_firewall_policy_rule#update ComputeRegionNetworkFirewallPolicyRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkFirewallPolicyRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkFirewallPolicyRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkFirewallPolicyRule.ComputeRegionNetworkFirewallPolicyRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22dae023c36fc7e77ce83ad3c6862d8b822ed84f023d63e75a32d805bebcce1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa38bab38ea3c7517c7986f156288799cb1cf17a52897a8c103001f5389e8a2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b022cf6b9e12ef8f8b01c15706cfe621da2e4037ecd679f19d966da0cc9c3563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158371d7d795dded6fee2cde7fb6d91c18a748eea08284c7036162259c33ee2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97086106a934c1cbc00f82382db8d836d3c7ead9537dc6df7beb2d94a82e5962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionNetworkFirewallPolicyRule",
    "ComputeRegionNetworkFirewallPolicyRuleConfig",
    "ComputeRegionNetworkFirewallPolicyRuleMatch",
    "ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs",
    "ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsList",
    "ComputeRegionNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference",
    "ComputeRegionNetworkFirewallPolicyRuleMatchOutputReference",
    "ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags",
    "ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsList",
    "ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference",
    "ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags",
    "ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsList",
    "ComputeRegionNetworkFirewallPolicyRuleTargetSecureTagsOutputReference",
    "ComputeRegionNetworkFirewallPolicyRuleTimeouts",
    "ComputeRegionNetworkFirewallPolicyRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__094a67dce9735141914cf28f8d4d4694f1ea76eb4299dd070796590035d0272e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    direction: builtins.str,
    firewall_policy: builtins.str,
    match: typing.Union[ComputeRegionNetworkFirewallPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_profile_group: typing.Optional[builtins.str] = None,
    target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionNetworkFirewallPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__9b8ee88f3aaa685921d5d4115382688f0fa73fd8e0939f0b462f64576e02b046(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d631ed295f5bae188acb242b0c0998b22083f4afb76a65d0a98f84006250a24(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6feeee79faba1fa75a5dbc196033e4cc4d754558ce794da4dcf6b4ad8676bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ea652ed9018dc61ff48e13a2d90d20a19581a046fe9bdb769dc2d6a923af85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5b8a45d4a0c5f950076f46a26161d19edb99cae2919f6bf7b02a2ad18c33b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ce7707520e98a50d395fa5a25813f92ed7751b36235fe7700f8378823e42fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfd259e951e3fdd768d1535be2049eda37a33f5da52a9c06f27f9fdbfcc592e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f8d9cc9274e6e8c71c65677e48560dd161886b4277b5885d7e7a8079ba847f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973716c2bc5be8474975f7b6d30d02705f62767f3a3dd8992aefb79bbf05558b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc0ca1c7714523c66cca6604f9769f712428d64550e23b2ccfeca4763348c9e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845bb68b6a216b18023e27363d061cc386894495a6bc5d443bfe333a4994f265(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fe1f7e5a202eb932ef4370fd0f79fe0a6b049542f3ad03cc085ceffad0d0ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6117955970c7490fff28a48585e6ea8b1915a87499d34ec70d946cc0f8366ca1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7688d941514cccffbb9cee6fb88f3ef102173a2ed49db5eda79ace86c262279c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b2a0ff42a961fdc4f846cfa4412562d8a8b5ae12ee16f94fba9beab187f5bd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e3113ed4300feffef095c18ba4dde2f4efa6be8a33ce17734868a95c044830(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2454b24e5c79c921860a4259e0f54a81c0f1bfe6b97e2cef1f3dbbe99e4f703d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    direction: builtins.str,
    firewall_policy: builtins.str,
    match: typing.Union[ComputeRegionNetworkFirewallPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_profile_group: typing.Optional[builtins.str] = None,
    target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionNetworkFirewallPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6443c30c2148b7dbdfbbb55e3054c328f4a2b70a6498ad14b4a1101cea944c(
    *,
    layer4_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs, typing.Dict[builtins.str, typing.Any]]]],
    dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61ddbd7b35cd59bbd7ea9cf227694ddf09da33ab7a41e4f9c7f09807964b73b(
    *,
    ip_protocol: builtins.str,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c6367965b55b7ae0609aec3bfa7d15d8f1a45adb7d2436341b6cfc44ed9370(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5f2bc4c18da600c270b6e47e5ae865ed6f9d89be7ebfd353156bc449cbb520(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3476019a124a0a05cbbdaee44d10465c0329754de974c002d1253ccf5c65b479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8f3968d02025db285de1edbb27ca5fe0b7add8dcdeee311f4bdbc2d5ed5cee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06dd0bdc9386341dfa8224c6a4bc6faa38affb84047491a333eb351f0c48570f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b677df7c5f181c293a5aa6da762e293acce507a5b33f0a72c6fc15f14f1cdf5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64117f1d87342bf483fb6f822f0b462ce5dddd83d666b0851c25b82b3e28a12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6dc59eb3a0c7c164391b13de244756bcc05cb573d090a6a569856505c21afef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ddb85ae4beb245d29218df76718d6a314f1844cbda286db8e4bcc376383d260(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7ebd9be5cb80dad2c00792b28e6c46e7ac19cfe3bb2f78ea3d4e029de0c6d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f87e6be6059f5f59a8925d21d49ad9dc0b149e0682d2f18b0c320cc2ea5627(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47183342a5e4cd07fd064ac96bbe877c0b2c0f228c37a449ec1dd5678f7a25c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyRuleMatchLayer4Configs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798805fe766c603ba7582892c89a3379b2074dfe480c1703965a93d213605543(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b6c2772eb5ce8fbb17ad786741a9c770d25150b857158b2891eb8da7e0c4a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d260d348ab5ec364173bbecbb32d7cb4c9a0886d420c1ad6688349f21a3344b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d0944aa81843c435df6eeccff5ccf3a9e5453b81154edbad60defe7bb471b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ba4ccc333ac786e0716f8bbc3704f8c614696e4d8312d2e267e65581bf6f91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8123327464072925d078312ccf16dd444505f7c839c3045c21d7098b5af5ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a988c1acc37672fdbb90c14c8cf0dd129c5066cd6c66bc63f53a5bf767dfb0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60e926a8c334347e7fbe3918d34f243bc35743b932fb5730109e3c5d39580a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27f65ab329ff31dd92311dfd11bc49b522d881325fcdf4b28bc4c9fabcc4887(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2f43601f58bbd07167cff3cb1135dc2afb2c6f5f8c983694323e04169c1bf0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f3bb63521b907e4520c4137d0b5138d071580aa299547a1a73e2748983d580(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e2ee1b1aa43274c06c52cf5591730b32e362bb72be3da80af69150640cad35(
    value: typing.Optional[ComputeRegionNetworkFirewallPolicyRuleMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86c1d6becc7f8465aca9eb9cfc957129f62899cf6e3b4e8ebd7265560184d67(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7421b6810a3d5d78ba15f1ab55a70b28256535ff732dbe4ce9bbcdbd604720a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a89b01397ab0cbbebd2d748910280629bf7bdc1f7701033d054005595d1faf8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fd0e7b8123f01488a4d8b4b60e63bc8268484fa7fcb71148349daedb02f520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280337a8bb5802ba68504f7447ebd9227c7bb3643a45ebb0c0b4bc6a0d4a8670(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b4ed87a0d0e8c8e6893f3a4b6ac46bafcd3e6502ce7c8cff9b113c06653603(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec34fbd7f386326e42de14f8b21501105b6feb0b8c4a6adb137770a5d56bc773(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7061776a5480577f454b004f32d4881a06d6c8671cd7a38d4259b30412855e4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c909070ae702da9e2e386d86b08efdcde5712ade4cc2def3c073cf513e86c2ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a8a19cbae6d870a438a39214f0230c73a991e41abbfac91d4a2330f42389ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleMatchSrcSecureTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf379e02646774cce2d3e51b83ca82839f5929d0ae3fb08638762e716bf6ff7(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b31f8567ea20b1c4cc7c5fbff8820e5b1180f129fefd3c147a659d7b04832e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2601f5e142cd66c5afc03d31fc8c64fbdfab9d84e8f32e7e83905723713e4918(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a548ce3cb18c028135307dc7ebf1452156b53e62b3490d5e0cb8c3af6b17768c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a51282dbb663236a92aaac563191962b20470e258e47fd6132af18f7361822(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf7f8ce165988f5d65abda5c4648875a4fc94588877e27b15fe790b40db1ff6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169a4b6554ec5431d729bdcc728f17074901b6e3afc3900e127a7e88caedf186(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4f36ffa0124eb1b3d6f0873945fa126f62135525d6deed13af7f3014193b63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7accb10716330f1075addef28c356c12e273c89a3aa183adb44748d2cef7d608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db1d7e72e732b188d4c5b6d7842daf4f348412c4a8428a1f4f2a1dd6d0ae652(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleTargetSecureTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdde3f92e7f31ee3c0d3f88f304cc063188d23eafd7d4742d8ed7b2b60e8a17a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dae023c36fc7e77ce83ad3c6862d8b822ed84f023d63e75a32d805bebcce1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa38bab38ea3c7517c7986f156288799cb1cf17a52897a8c103001f5389e8a2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b022cf6b9e12ef8f8b01c15706cfe621da2e4037ecd679f19d966da0cc9c3563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158371d7d795dded6fee2cde7fb6d91c18a748eea08284c7036162259c33ee2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97086106a934c1cbc00f82382db8d836d3c7ead9537dc6df7beb2d94a82e5962(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkFirewallPolicyRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
