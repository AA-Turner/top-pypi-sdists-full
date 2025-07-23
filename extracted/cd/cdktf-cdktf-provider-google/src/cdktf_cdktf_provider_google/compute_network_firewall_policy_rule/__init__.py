r'''
# `google_compute_network_firewall_policy_rule`

Refer to the Terraform Registry for docs: [`google_compute_network_firewall_policy_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule).
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


class ComputeNetworkFirewallPolicyRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule google_compute_network_firewall_policy_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        direction: builtins.str,
        firewall_policy: builtins.str,
        match: typing.Union["ComputeNetworkFirewallPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_profile_group: typing.Optional[builtins.str] = None,
        target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNetworkFirewallPolicyRuleTargetSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeNetworkFirewallPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule google_compute_network_firewall_policy_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: The Action to perform when the client connection triggers the rule. Valid actions are "allow", "deny", "goto_next" and "apply_security_profile_group". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#action ComputeNetworkFirewallPolicyRule#action}
        :param direction: The direction in which this rule applies. Possible values: ["INGRESS", "EGRESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#direction ComputeNetworkFirewallPolicyRule#direction}
        :param firewall_policy: The firewall policy of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#firewall_policy ComputeNetworkFirewallPolicyRule#firewall_policy}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#match ComputeNetworkFirewallPolicyRule#match}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#priority ComputeNetworkFirewallPolicyRule#priority}
        :param description: An optional description for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#description ComputeNetworkFirewallPolicyRule#description}
        :param disabled: Denotes whether the firewall policy rule is disabled. When set to true, the firewall policy rule is not enforced and traffic behaves as if it did not exist. If this is unspecified, the firewall policy rule will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#disabled ComputeNetworkFirewallPolicyRule#disabled}
        :param enable_logging: Denotes whether to enable logging for a particular rule. If logging is enabled, logs will be exported to the configured export destination in Stackdriver. Logs may be exported to BigQuery or Pub/Sub. Note: you cannot enable logging on "goto_next" rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#enable_logging ComputeNetworkFirewallPolicyRule#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#id ComputeNetworkFirewallPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#project ComputeNetworkFirewallPolicyRule#project}.
        :param rule_name: An optional name for the rule. This field is not a unique identifier and can be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#rule_name ComputeNetworkFirewallPolicyRule#rule_name}
        :param security_profile_group: A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action = 'apply_security_profile_group' and cannot be specified for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#security_profile_group ComputeNetworkFirewallPolicyRule#security_profile_group}
        :param target_secure_tags: target_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#target_secure_tags ComputeNetworkFirewallPolicyRule#target_secure_tags}
        :param target_service_accounts: A list of service accounts indicating the sets of instances that are applied with this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#target_service_accounts ComputeNetworkFirewallPolicyRule#target_service_accounts}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#timeouts ComputeNetworkFirewallPolicyRule#timeouts}
        :param tls_inspect: Boolean flag indicating if the traffic should be TLS decrypted. Can be set only if action = 'apply_security_profile_group' and cannot be set for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#tls_inspect ComputeNetworkFirewallPolicyRule#tls_inspect}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e1ca3545e46c242e96586a46ee409bfe3d645f704e335648fedcb79bb7f4af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeNetworkFirewallPolicyRuleConfig(
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
        '''Generates CDKTF code for importing a ComputeNetworkFirewallPolicyRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeNetworkFirewallPolicyRule to import.
        :param import_from_id: The id of the existing ComputeNetworkFirewallPolicyRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeNetworkFirewallPolicyRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c440377a20f8d0dfd68f2dc0b3680025a317ae0526e40801ca40bb2ba73193)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        layer4_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNetworkFirewallPolicyRuleMatchLayer4Configs", typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_configs: layer4_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#layer4_configs ComputeNetworkFirewallPolicyRule#layer4_configs}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_address_groups ComputeNetworkFirewallPolicyRule#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_fqdns ComputeNetworkFirewallPolicyRule#dest_fqdns}
        :param dest_ip_ranges: CIDR IP address range. Maximum number of destination CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_ip_ranges ComputeNetworkFirewallPolicyRule#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of dest region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_region_codes ComputeNetworkFirewallPolicyRule#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_threat_intelligences ComputeNetworkFirewallPolicyRule#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_address_groups ComputeNetworkFirewallPolicyRule#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_fqdns ComputeNetworkFirewallPolicyRule#src_fqdns}
        :param src_ip_ranges: CIDR IP address range. Maximum number of source CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_ip_ranges ComputeNetworkFirewallPolicyRule#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_region_codes ComputeNetworkFirewallPolicyRule#src_region_codes}
        :param src_secure_tags: src_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_secure_tags ComputeNetworkFirewallPolicyRule#src_secure_tags}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_threat_intelligences ComputeNetworkFirewallPolicyRule#src_threat_intelligences}
        '''
        value = ComputeNetworkFirewallPolicyRuleMatch(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNetworkFirewallPolicyRuleTargetSecureTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9607a526ddfe7353c1e852e77b2857227703ac9a5ca852bd140c752fcab01ea)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#create ComputeNetworkFirewallPolicyRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#delete ComputeNetworkFirewallPolicyRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#update ComputeNetworkFirewallPolicyRule#update}.
        '''
        value = ComputeNetworkFirewallPolicyRuleTimeouts(
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
    def match(self) -> "ComputeNetworkFirewallPolicyRuleMatchOutputReference":
        return typing.cast("ComputeNetworkFirewallPolicyRuleMatchOutputReference", jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="ruleTupleCount")
    def rule_tuple_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleTupleCount"))

    @builtins.property
    @jsii.member(jsii_name="targetSecureTags")
    def target_secure_tags(
        self,
    ) -> "ComputeNetworkFirewallPolicyRuleTargetSecureTagsList":
        return typing.cast("ComputeNetworkFirewallPolicyRuleTargetSecureTagsList", jsii.get(self, "targetSecureTags"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeNetworkFirewallPolicyRuleTimeoutsOutputReference":
        return typing.cast("ComputeNetworkFirewallPolicyRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def match_input(self) -> typing.Optional["ComputeNetworkFirewallPolicyRuleMatch"]:
        return typing.cast(typing.Optional["ComputeNetworkFirewallPolicyRuleMatch"], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleTargetSecureTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleTargetSecureTags"]]], jsii.get(self, "targetSecureTagsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeNetworkFirewallPolicyRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeNetworkFirewallPolicyRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1743067e7c4cd65158fd61e68cae2420dbb261673a0c60750b3bf47fc8d3b162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00942dc12771eb5ac1f6011eb8e54096713d82fbccb6ec0c6cbc354ebe42d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324f5756954274cd738cc50803f4120a65beb9a19298a1639cc445218c7c55d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bb2083ee71582bbf28bda7da98874b04307f7777a797d4b1f38837995e1f991)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e8cd565196cdc8a13064fbb92bcf73dac5ad27508a9ebb82a81d5e8e3455b25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firewallPolicy")
    def firewall_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicy"))

    @firewall_policy.setter
    def firewall_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0023e5cc01ff2263102cb029d208899e49620c5ea7ff733651ab496683ba8e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553f9b3bba9db3570f0f62b93163aeb46e3f5227a7ab349917b0afe0c30e54be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f0c994cf27f7d2d9b156f1c27623bbda7890293d4a94c933472f172e77d249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a4fb3c1beb6a71b8ebe49f7a3db2f9590352738f407f6aa5bc630472e1099f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cf49870065876cd6acffa40686c730d0e4708cb4f2da5e28c78934e06f6f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityProfileGroup")
    def security_profile_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProfileGroup"))

    @security_profile_group.setter
    def security_profile_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375d244610f81c070bcbc339f43bf636effad9d0da9c91e800beeaa1e2db40ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProfileGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetServiceAccounts")
    def target_service_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetServiceAccounts"))

    @target_service_accounts.setter
    def target_service_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49278d771f22862630ff4655ab130b2b103407f854ca9289f176ff0a2c978111)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5552a09c40b8918ce4221dafd4ca6fba3000db2e879ea2f9eeb57fcb89cb989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsInspect", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleConfig",
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
        "rule_name": "ruleName",
        "security_profile_group": "securityProfileGroup",
        "target_secure_tags": "targetSecureTags",
        "target_service_accounts": "targetServiceAccounts",
        "timeouts": "timeouts",
        "tls_inspect": "tlsInspect",
    },
)
class ComputeNetworkFirewallPolicyRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        match: typing.Union["ComputeNetworkFirewallPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_profile_group: typing.Optional[builtins.str] = None,
        target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNetworkFirewallPolicyRuleTargetSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeNetworkFirewallPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param action: The Action to perform when the client connection triggers the rule. Valid actions are "allow", "deny", "goto_next" and "apply_security_profile_group". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#action ComputeNetworkFirewallPolicyRule#action}
        :param direction: The direction in which this rule applies. Possible values: ["INGRESS", "EGRESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#direction ComputeNetworkFirewallPolicyRule#direction}
        :param firewall_policy: The firewall policy of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#firewall_policy ComputeNetworkFirewallPolicyRule#firewall_policy}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#match ComputeNetworkFirewallPolicyRule#match}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#priority ComputeNetworkFirewallPolicyRule#priority}
        :param description: An optional description for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#description ComputeNetworkFirewallPolicyRule#description}
        :param disabled: Denotes whether the firewall policy rule is disabled. When set to true, the firewall policy rule is not enforced and traffic behaves as if it did not exist. If this is unspecified, the firewall policy rule will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#disabled ComputeNetworkFirewallPolicyRule#disabled}
        :param enable_logging: Denotes whether to enable logging for a particular rule. If logging is enabled, logs will be exported to the configured export destination in Stackdriver. Logs may be exported to BigQuery or Pub/Sub. Note: you cannot enable logging on "goto_next" rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#enable_logging ComputeNetworkFirewallPolicyRule#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#id ComputeNetworkFirewallPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#project ComputeNetworkFirewallPolicyRule#project}.
        :param rule_name: An optional name for the rule. This field is not a unique identifier and can be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#rule_name ComputeNetworkFirewallPolicyRule#rule_name}
        :param security_profile_group: A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action = 'apply_security_profile_group' and cannot be specified for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#security_profile_group ComputeNetworkFirewallPolicyRule#security_profile_group}
        :param target_secure_tags: target_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#target_secure_tags ComputeNetworkFirewallPolicyRule#target_secure_tags}
        :param target_service_accounts: A list of service accounts indicating the sets of instances that are applied with this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#target_service_accounts ComputeNetworkFirewallPolicyRule#target_service_accounts}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#timeouts ComputeNetworkFirewallPolicyRule#timeouts}
        :param tls_inspect: Boolean flag indicating if the traffic should be TLS decrypted. Can be set only if action = 'apply_security_profile_group' and cannot be set for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#tls_inspect ComputeNetworkFirewallPolicyRule#tls_inspect}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(match, dict):
            match = ComputeNetworkFirewallPolicyRuleMatch(**match)
        if isinstance(timeouts, dict):
            timeouts = ComputeNetworkFirewallPolicyRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b294df0a7b37f2e753c5bd9a83a8ee43c883ad242a6e32970e31187d8d5ac69)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#action ComputeNetworkFirewallPolicyRule#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def direction(self) -> builtins.str:
        '''The direction in which this rule applies. Possible values: ["INGRESS", "EGRESS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#direction ComputeNetworkFirewallPolicyRule#direction}
        '''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def firewall_policy(self) -> builtins.str:
        '''The firewall policy of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#firewall_policy ComputeNetworkFirewallPolicyRule#firewall_policy}
        '''
        result = self._values.get("firewall_policy")
        assert result is not None, "Required property 'firewall_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(self) -> "ComputeNetworkFirewallPolicyRuleMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#match ComputeNetworkFirewallPolicyRule#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("ComputeNetworkFirewallPolicyRuleMatch", result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An integer indicating the priority of a rule in the list.

        The priority must be a positive value between 0 and 2147483647.
        Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#priority ComputeNetworkFirewallPolicyRule#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#description ComputeNetworkFirewallPolicyRule#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#disabled ComputeNetworkFirewallPolicyRule#disabled}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#enable_logging ComputeNetworkFirewallPolicyRule#enable_logging}
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#id ComputeNetworkFirewallPolicyRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#project ComputeNetworkFirewallPolicyRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the rule. This field is not a unique identifier and can be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#rule_name ComputeNetworkFirewallPolicyRule#rule_name}
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_profile_group(self) -> typing.Optional[builtins.str]:
        '''A fully-qualified URL of a SecurityProfile resource instance.

        Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group
        Must be specified if action = 'apply_security_profile_group' and cannot be specified for other actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#security_profile_group ComputeNetworkFirewallPolicyRule#security_profile_group}
        '''
        result = self._values.get("security_profile_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_secure_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleTargetSecureTags"]]]:
        '''target_secure_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#target_secure_tags ComputeNetworkFirewallPolicyRule#target_secure_tags}
        '''
        result = self._values.get("target_secure_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleTargetSecureTags"]]], result)

    @builtins.property
    def target_service_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of service accounts indicating the sets of instances that are applied with this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#target_service_accounts ComputeNetworkFirewallPolicyRule#target_service_accounts}
        '''
        result = self._values.get("target_service_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeNetworkFirewallPolicyRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#timeouts ComputeNetworkFirewallPolicyRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeNetworkFirewallPolicyRuleTimeouts"], result)

    @builtins.property
    def tls_inspect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean flag indicating if the traffic should be TLS decrypted.

        Can be set only if action = 'apply_security_profile_group' and cannot be set for other actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#tls_inspect ComputeNetworkFirewallPolicyRule#tls_inspect}
        '''
        result = self._values.get("tls_inspect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNetworkFirewallPolicyRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleMatch",
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
class ComputeNetworkFirewallPolicyRuleMatch:
    def __init__(
        self,
        *,
        layer4_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNetworkFirewallPolicyRuleMatchLayer4Configs", typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_configs: layer4_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#layer4_configs ComputeNetworkFirewallPolicyRule#layer4_configs}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_address_groups ComputeNetworkFirewallPolicyRule#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_fqdns ComputeNetworkFirewallPolicyRule#dest_fqdns}
        :param dest_ip_ranges: CIDR IP address range. Maximum number of destination CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_ip_ranges ComputeNetworkFirewallPolicyRule#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of dest region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_region_codes ComputeNetworkFirewallPolicyRule#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_threat_intelligences ComputeNetworkFirewallPolicyRule#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_address_groups ComputeNetworkFirewallPolicyRule#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_fqdns ComputeNetworkFirewallPolicyRule#src_fqdns}
        :param src_ip_ranges: CIDR IP address range. Maximum number of source CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_ip_ranges ComputeNetworkFirewallPolicyRule#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_region_codes ComputeNetworkFirewallPolicyRule#src_region_codes}
        :param src_secure_tags: src_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_secure_tags ComputeNetworkFirewallPolicyRule#src_secure_tags}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_threat_intelligences ComputeNetworkFirewallPolicyRule#src_threat_intelligences}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf36a78764487594a1cac828102bbfb5755ca6a0c26c53b8aa6e2d8ab490544b)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleMatchLayer4Configs"]]:
        '''layer4_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#layer4_configs ComputeNetworkFirewallPolicyRule#layer4_configs}
        '''
        result = self._values.get("layer4_configs")
        assert result is not None, "Required property 'layer4_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleMatchLayer4Configs"]], result)

    @builtins.property
    def dest_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_address_groups ComputeNetworkFirewallPolicyRule#dest_address_groups}
        '''
        result = self._values.get("dest_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic destination.

        Maximum number of destination fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_fqdns ComputeNetworkFirewallPolicyRule#dest_fqdns}
        '''
        result = self._values.get("dest_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of destination CIDR IP ranges allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_ip_ranges ComputeNetworkFirewallPolicyRule#dest_ip_ranges}
        '''
        result = self._values.get("dest_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for destination of traffic.

        Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of dest region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_region_codes ComputeNetworkFirewallPolicyRule#dest_region_codes}
        '''
        result = self._values.get("dest_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#dest_threat_intelligences ComputeNetworkFirewallPolicyRule#dest_threat_intelligences}
        '''
        result = self._values.get("dest_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic source. Maximum number of source address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_address_groups ComputeNetworkFirewallPolicyRule#src_address_groups}
        '''
        result = self._values.get("src_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic source.

        Maximum number of source fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_fqdns ComputeNetworkFirewallPolicyRule#src_fqdns}
        '''
        result = self._values.get("src_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of source CIDR IP ranges allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_ip_ranges ComputeNetworkFirewallPolicyRule#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for source of traffic.

        Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_region_codes ComputeNetworkFirewallPolicyRule#src_region_codes}
        '''
        result = self._values.get("src_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_secure_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags"]]]:
        '''src_secure_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_secure_tags ComputeNetworkFirewallPolicyRule#src_secure_tags}
        '''
        result = self._values.get("src_secure_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags"]]], result)

    @builtins.property
    def src_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#src_threat_intelligences ComputeNetworkFirewallPolicyRule#src_threat_intelligences}
        '''
        result = self._values.get("src_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNetworkFirewallPolicyRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleMatchLayer4Configs",
    jsii_struct_bases=[],
    name_mapping={"ip_protocol": "ipProtocol", "ports": "ports"},
)
class ComputeNetworkFirewallPolicyRuleMatchLayer4Configs:
    def __init__(
        self,
        *,
        ip_protocol: builtins.str,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ip_protocol: The IP protocol to which this rule applies. The protocol type is required when creating a firewall rule. This value can either be one of the following well known protocol strings (tcp, udp, icmp, esp, ah, ipip, sctp), or the IP protocol number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#ip_protocol ComputeNetworkFirewallPolicyRule#ip_protocol}
        :param ports: An optional list of ports to which this rule applies. This field is only applicable for UDP or TCP protocol. Each entry must be either an integer or a range. If not specified, this rule applies to connections through any port. Example inputs include: ["22"], ["80","443"], and ["12345-12349"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#ports ComputeNetworkFirewallPolicyRule#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c00e6cd0336f891ea3c5fbc7e5f978f747ecd44c4f3ea267eb2763b52c97c5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#ip_protocol ComputeNetworkFirewallPolicyRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional list of ports to which this rule applies.

        This field is only applicable for UDP or TCP protocol. Each entry must be either an integer or a range. If not specified, this rule applies to connections through any port.
        Example inputs include: ["22"], ["80","443"], and ["12345-12349"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#ports ComputeNetworkFirewallPolicyRule#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNetworkFirewallPolicyRuleMatchLayer4Configs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4f9481bb2eb3f41b8358b53a2e2718bfbd4d6bdd0bbb7943325d51bc452e71f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4ec268de254299aed0dd3f2165ba32f505ff1fb0b6ae06bde0038a8905fcaa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c19687070b224ffada7f1fa4a4577b29e768c45c3335aa3b83f971652900d9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c012a484743d03e9e67b0655ac85989227184fc23042c0aae4873cc67464d070)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff4dc8e1a0f2368cab6a53ccbc446e8a4f42f67ad3c75c8c301dbb1b97ab7ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b88c0de793691e0c68480944bc9ca57b2d9d48f42da9eb79f8df2ec396a9f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af501a5e868af4cac333b0244af3be80c88c4d1f425a053adb812448e12be74a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e522c43306f274ed2eeaa1b452c82c58cc1d7a35f9dd6501ef0618c2caae5cfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d11dd23d551f96ef862bd47f5df956b367ce4f3849620b24420decc374f04c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f92caa3bc27d541467251d7d43407a829be29635f135ec5a29cf1cfbd485878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeNetworkFirewallPolicyRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf633c6e903cdd1c3a879c548e634a7f7472d57b67b1122a4291d15b1c40feca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLayer4Configs")
    def put_layer4_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNetworkFirewallPolicyRuleMatchLayer4Configs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e94dde6e432a69af4acba881fea191e632db9163cfbcc259fd1439dfc77a939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLayer4Configs", [value]))

    @jsii.member(jsii_name="putSrcSecureTags")
    def put_src_secure_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581c3bae52e7f35545cc6b03ec5d002d33e8d6be5a5d364c871ba45308c5390d)
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
    def layer4_configs(self) -> ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsList:
        return typing.cast(ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsList, jsii.get(self, "layer4Configs"))

    @builtins.property
    @jsii.member(jsii_name="srcSecureTags")
    def src_secure_tags(
        self,
    ) -> "ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsList":
        return typing.cast("ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsList", jsii.get(self, "srcSecureTags"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]]], jsii.get(self, "layer4ConfigsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags"]]], jsii.get(self, "srcSecureTagsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c3e671a8bc8c3d62042440c806848bf11061527689b24c4658eddafe878be177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destFqdns")
    def dest_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destFqdns"))

    @dest_fqdns.setter
    def dest_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fb845b102cfcca304326608c93675e32cd82ac1e5e7e6b18a1de6a0ed10ea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destIpRanges")
    def dest_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destIpRanges"))

    @dest_ip_ranges.setter
    def dest_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecdca2c2f58556d45d8b690c8ad6819db0189a203fdaad19ca0f3785eeb79f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destRegionCodes")
    def dest_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destRegionCodes"))

    @dest_region_codes.setter
    def dest_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bc583f7418df6523be831971a6ac9e433384a43a806e6a4587aca61bb9bdb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destThreatIntelligences")
    def dest_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destThreatIntelligences"))

    @dest_threat_intelligences.setter
    def dest_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94cf1ae783922bd7f81dee51090866c93d503a7bbd9e346206e9cc12ff1198a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcAddressGroups")
    def src_address_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcAddressGroups"))

    @src_address_groups.setter
    def src_address_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce87a15dbb3410bc75ce9081a61ed71fdcb39682025b7b579b635e939ee9f04a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcFqdns")
    def src_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcFqdns"))

    @src_fqdns.setter
    def src_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67224cc07ef552c8c1cee651306329cef0ebc28005f404d48d6ee82486c271b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @src_ip_ranges.setter
    def src_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d47d36fd7d9d388fc7d28d0f1902f94e040a17f9f0b5280277b1017e6f15a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodes")
    def src_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcRegionCodes"))

    @src_region_codes.setter
    def src_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39ad550ad0d0a50413eb70d8e3f56e67f85e73f176d7bc3689f413d907aa7ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcThreatIntelligences")
    def src_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcThreatIntelligences"))

    @src_threat_intelligences.setter
    def src_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c78bb7df1b5bce91dca9daa89010850befe49ea26bf7db419f70096847456d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeNetworkFirewallPolicyRuleMatch]:
        return typing.cast(typing.Optional[ComputeNetworkFirewallPolicyRuleMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeNetworkFirewallPolicyRuleMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b925ffb8e3e29e0ed93ff1795097cc11c89ce06d9b80df5332846c52eadc77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#name ComputeNetworkFirewallPolicyRule#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2dea561fd5966f71b758cfe7dda9499fb90ac164093ce5f39450e0fc82e3b0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#name ComputeNetworkFirewallPolicyRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84bacdc66530f37ff5b57734ff360f84f7d8e2290ed0094355aebdf72c01a910)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0407126dbf14b79e5b25b9b4e1ffdc020c2fe0f4d586f949134533975dbd32)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613a28a34bed27b1180391aa2f4b7891408b160cbd67b5877c70890644b8ee0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a1e8af014da4e5c9ee07ac5d9bc8ff7a495b319532927e2cd891d47febb6f70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__903a56ad5f8cc5cc3e7b0b45177ca8c00fe3326aef49dc85dde41d19e5aaa81c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418cf6ae61c758f48c2a5bd5a508217e49fe63744c5795b3e6b6690c0c3ce1f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__414de2838707afb32d180ede98190fd0d50d57a99c27b5bc39bfa4b263700a9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b47f98f2b852ff89d50b5887636bd8d524d0eec863e7308a5698dcb0ba3013fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae7b82fbbe59d1cc453e250cfce6d946e3fbc605e66d09aea5e97c59110ec705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleTargetSecureTags",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeNetworkFirewallPolicyRuleTargetSecureTags:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#name ComputeNetworkFirewallPolicyRule#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db7801f427341bef4209a2b28c15439cb0334a74d6998e8522c8819bed3d217)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#name ComputeNetworkFirewallPolicyRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNetworkFirewallPolicyRuleTargetSecureTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNetworkFirewallPolicyRuleTargetSecureTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleTargetSecureTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__229c50b70ea172b7760fb1309d3b87b9dc1fc9ad322b069b97e468d3a152dc19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeNetworkFirewallPolicyRuleTargetSecureTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a16ae4afd00f08909214934499b6a89292a4d58983162a597b318ea1b0b713)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeNetworkFirewallPolicyRuleTargetSecureTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a23123bfe5af8892e6fe23d943b22fee2bfaee36ae88467ece3927a559dc21b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0942ab063f02c5525a4c8bdeeeab8dd352672d4f934bbdb87016529ffdcbafa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8046b70ed103ffe575f2ea4dac56b143d526366087546f50e33e8a909dd5e386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleTargetSecureTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleTargetSecureTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleTargetSecureTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e093b4363d3f768376ad1bcae4813ed60ef02caba32c2e2d7a8f38cf827228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeNetworkFirewallPolicyRuleTargetSecureTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleTargetSecureTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__006c5eaa72f902970354ef335d2dd1b16fe4353eccab1d6499aacf2d320fcf42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bf77c61ba65930f58fc04942165d01f60e30b4ff03692ae44348f7c16b62b50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleTargetSecureTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleTargetSecureTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleTargetSecureTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7535f582776dc1d925077cf7373fa6759953dc25704c6d3dfd7ff7575d321789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeNetworkFirewallPolicyRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#create ComputeNetworkFirewallPolicyRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#delete ComputeNetworkFirewallPolicyRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#update ComputeNetworkFirewallPolicyRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ce2fbfa41ef6ee9d1d7f257991388dda3496d7c9157c8a5851eae4023551d8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#create ComputeNetworkFirewallPolicyRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#delete ComputeNetworkFirewallPolicyRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network_firewall_policy_rule#update ComputeNetworkFirewallPolicyRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNetworkFirewallPolicyRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNetworkFirewallPolicyRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetworkFirewallPolicyRule.ComputeNetworkFirewallPolicyRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__336c83aec251089bb9fdc9703aab1fedaac5fc76d317e252e632f14777481f7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df8def661309ef6502b743f086c00323bcd117cb31a57f0b85f6e53930c2713c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bfe3f0597d5e3245fb50192ddc54a28f9212bc07ff5b076b636458aed6ab523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6de786f2b9bd1023dac135b40fcb2fc1f1e6e56aaa576345793f1130004a26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d796b40397a92bdc9a0c0be6f260b1088184524a1384e4d37c87fd7a9864191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeNetworkFirewallPolicyRule",
    "ComputeNetworkFirewallPolicyRuleConfig",
    "ComputeNetworkFirewallPolicyRuleMatch",
    "ComputeNetworkFirewallPolicyRuleMatchLayer4Configs",
    "ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsList",
    "ComputeNetworkFirewallPolicyRuleMatchLayer4ConfigsOutputReference",
    "ComputeNetworkFirewallPolicyRuleMatchOutputReference",
    "ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags",
    "ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsList",
    "ComputeNetworkFirewallPolicyRuleMatchSrcSecureTagsOutputReference",
    "ComputeNetworkFirewallPolicyRuleTargetSecureTags",
    "ComputeNetworkFirewallPolicyRuleTargetSecureTagsList",
    "ComputeNetworkFirewallPolicyRuleTargetSecureTagsOutputReference",
    "ComputeNetworkFirewallPolicyRuleTimeouts",
    "ComputeNetworkFirewallPolicyRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__46e1ca3545e46c242e96586a46ee409bfe3d645f704e335648fedcb79bb7f4af(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    direction: builtins.str,
    firewall_policy: builtins.str,
    match: typing.Union[ComputeNetworkFirewallPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_profile_group: typing.Optional[builtins.str] = None,
    target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNetworkFirewallPolicyRuleTargetSecureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeNetworkFirewallPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__77c440377a20f8d0dfd68f2dc0b3680025a317ae0526e40801ca40bb2ba73193(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9607a526ddfe7353c1e852e77b2857227703ac9a5ca852bd140c752fcab01ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNetworkFirewallPolicyRuleTargetSecureTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1743067e7c4cd65158fd61e68cae2420dbb261673a0c60750b3bf47fc8d3b162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00942dc12771eb5ac1f6011eb8e54096713d82fbccb6ec0c6cbc354ebe42d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324f5756954274cd738cc50803f4120a65beb9a19298a1639cc445218c7c55d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb2083ee71582bbf28bda7da98874b04307f7777a797d4b1f38837995e1f991(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8cd565196cdc8a13064fbb92bcf73dac5ad27508a9ebb82a81d5e8e3455b25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0023e5cc01ff2263102cb029d208899e49620c5ea7ff733651ab496683ba8e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553f9b3bba9db3570f0f62b93163aeb46e3f5227a7ab349917b0afe0c30e54be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f0c994cf27f7d2d9b156f1c27623bbda7890293d4a94c933472f172e77d249(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a4fb3c1beb6a71b8ebe49f7a3db2f9590352738f407f6aa5bc630472e1099f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cf49870065876cd6acffa40686c730d0e4708cb4f2da5e28c78934e06f6f99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375d244610f81c070bcbc339f43bf636effad9d0da9c91e800beeaa1e2db40ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49278d771f22862630ff4655ab130b2b103407f854ca9289f176ff0a2c978111(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5552a09c40b8918ce4221dafd4ca6fba3000db2e879ea2f9eeb57fcb89cb989(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b294df0a7b37f2e753c5bd9a83a8ee43c883ad242a6e32970e31187d8d5ac69(
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
    match: typing.Union[ComputeNetworkFirewallPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_profile_group: typing.Optional[builtins.str] = None,
    target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNetworkFirewallPolicyRuleTargetSecureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeNetworkFirewallPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf36a78764487594a1cac828102bbfb5755ca6a0c26c53b8aa6e2d8ab490544b(
    *,
    layer4_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNetworkFirewallPolicyRuleMatchLayer4Configs, typing.Dict[builtins.str, typing.Any]]]],
    dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c00e6cd0336f891ea3c5fbc7e5f978f747ecd44c4f3ea267eb2763b52c97c5(
    *,
    ip_protocol: builtins.str,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f9481bb2eb3f41b8358b53a2e2718bfbd4d6bdd0bbb7943325d51bc452e71f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4ec268de254299aed0dd3f2165ba32f505ff1fb0b6ae06bde0038a8905fcaa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c19687070b224ffada7f1fa4a4577b29e768c45c3335aa3b83f971652900d9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c012a484743d03e9e67b0655ac85989227184fc23042c0aae4873cc67464d070(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4dc8e1a0f2368cab6a53ccbc446e8a4f42f67ad3c75c8c301dbb1b97ab7ebb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b88c0de793691e0c68480944bc9ca57b2d9d48f42da9eb79f8df2ec396a9f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af501a5e868af4cac333b0244af3be80c88c4d1f425a053adb812448e12be74a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e522c43306f274ed2eeaa1b452c82c58cc1d7a35f9dd6501ef0618c2caae5cfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d11dd23d551f96ef862bd47f5df956b367ce4f3849620b24420decc374f04c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f92caa3bc27d541467251d7d43407a829be29635f135ec5a29cf1cfbd485878(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleMatchLayer4Configs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf633c6e903cdd1c3a879c548e634a7f7472d57b67b1122a4291d15b1c40feca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e94dde6e432a69af4acba881fea191e632db9163cfbcc259fd1439dfc77a939(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNetworkFirewallPolicyRuleMatchLayer4Configs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581c3bae52e7f35545cc6b03ec5d002d33e8d6be5a5d364c871ba45308c5390d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e671a8bc8c3d62042440c806848bf11061527689b24c4658eddafe878be177(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fb845b102cfcca304326608c93675e32cd82ac1e5e7e6b18a1de6a0ed10ea5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecdca2c2f58556d45d8b690c8ad6819db0189a203fdaad19ca0f3785eeb79f93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bc583f7418df6523be831971a6ac9e433384a43a806e6a4587aca61bb9bdb3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94cf1ae783922bd7f81dee51090866c93d503a7bbd9e346206e9cc12ff1198a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce87a15dbb3410bc75ce9081a61ed71fdcb39682025b7b579b635e939ee9f04a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67224cc07ef552c8c1cee651306329cef0ebc28005f404d48d6ee82486c271b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d47d36fd7d9d388fc7d28d0f1902f94e040a17f9f0b5280277b1017e6f15a0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ad550ad0d0a50413eb70d8e3f56e67f85e73f176d7bc3689f413d907aa7ef5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78bb7df1b5bce91dca9daa89010850befe49ea26bf7db419f70096847456d74(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b925ffb8e3e29e0ed93ff1795097cc11c89ce06d9b80df5332846c52eadc77(
    value: typing.Optional[ComputeNetworkFirewallPolicyRuleMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2dea561fd5966f71b758cfe7dda9499fb90ac164093ce5f39450e0fc82e3b0(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bacdc66530f37ff5b57734ff360f84f7d8e2290ed0094355aebdf72c01a910(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0407126dbf14b79e5b25b9b4e1ffdc020c2fe0f4d586f949134533975dbd32(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613a28a34bed27b1180391aa2f4b7891408b160cbd67b5877c70890644b8ee0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1e8af014da4e5c9ee07ac5d9bc8ff7a495b319532927e2cd891d47febb6f70(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903a56ad5f8cc5cc3e7b0b45177ca8c00fe3326aef49dc85dde41d19e5aaa81c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418cf6ae61c758f48c2a5bd5a508217e49fe63744c5795b3e6b6690c0c3ce1f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414de2838707afb32d180ede98190fd0d50d57a99c27b5bc39bfa4b263700a9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47f98f2b852ff89d50b5887636bd8d524d0eec863e7308a5698dcb0ba3013fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7b82fbbe59d1cc453e250cfce6d946e3fbc605e66d09aea5e97c59110ec705(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleMatchSrcSecureTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db7801f427341bef4209a2b28c15439cb0334a74d6998e8522c8819bed3d217(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229c50b70ea172b7760fb1309d3b87b9dc1fc9ad322b069b97e468d3a152dc19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a16ae4afd00f08909214934499b6a89292a4d58983162a597b318ea1b0b713(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a23123bfe5af8892e6fe23d943b22fee2bfaee36ae88467ece3927a559dc21b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0942ab063f02c5525a4c8bdeeeab8dd352672d4f934bbdb87016529ffdcbafa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8046b70ed103ffe575f2ea4dac56b143d526366087546f50e33e8a909dd5e386(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e093b4363d3f768376ad1bcae4813ed60ef02caba32c2e2d7a8f38cf827228(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNetworkFirewallPolicyRuleTargetSecureTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006c5eaa72f902970354ef335d2dd1b16fe4353eccab1d6499aacf2d320fcf42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf77c61ba65930f58fc04942165d01f60e30b4ff03692ae44348f7c16b62b50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7535f582776dc1d925077cf7373fa6759953dc25704c6d3dfd7ff7575d321789(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleTargetSecureTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ce2fbfa41ef6ee9d1d7f257991388dda3496d7c9157c8a5851eae4023551d8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336c83aec251089bb9fdc9703aab1fedaac5fc76d317e252e632f14777481f7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8def661309ef6502b743f086c00323bcd117cb31a57f0b85f6e53930c2713c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bfe3f0597d5e3245fb50192ddc54a28f9212bc07ff5b076b636458aed6ab523(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6de786f2b9bd1023dac135b40fcb2fc1f1e6e56aaa576345793f1130004a26a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d796b40397a92bdc9a0c0be6f260b1088184524a1384e4d37c87fd7a9864191(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkFirewallPolicyRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
