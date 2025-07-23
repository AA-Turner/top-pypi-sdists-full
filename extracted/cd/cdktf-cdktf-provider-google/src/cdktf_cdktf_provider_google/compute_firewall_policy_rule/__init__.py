r'''
# `google_compute_firewall_policy_rule`

Refer to the Terraform Registry for docs: [`google_compute_firewall_policy_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule).
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


class ComputeFirewallPolicyRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule google_compute_firewall_policy_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        direction: builtins.str,
        firewall_policy: builtins.str,
        match: typing.Union["ComputeFirewallPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        security_profile_group: typing.Optional[builtins.str] = None,
        target_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyRuleTargetSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeFirewallPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule google_compute_firewall_policy_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: The Action to perform when the client connection triggers the rule. Valid actions are "allow", "deny", "goto_next" and "apply_security_profile_group". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#action ComputeFirewallPolicyRule#action}
        :param direction: The direction in which this rule applies. Possible values: ["INGRESS", "EGRESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#direction ComputeFirewallPolicyRule#direction}
        :param firewall_policy: The firewall policy of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#firewall_policy ComputeFirewallPolicyRule#firewall_policy}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#match ComputeFirewallPolicyRule#match}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#priority ComputeFirewallPolicyRule#priority}
        :param description: An optional description for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#description ComputeFirewallPolicyRule#description}
        :param disabled: Denotes whether the firewall policy rule is disabled. When set to true, the firewall policy rule is not enforced and traffic behaves as if it did not exist. If this is unspecified, the firewall policy rule will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#disabled ComputeFirewallPolicyRule#disabled}
        :param enable_logging: Denotes whether to enable logging for a particular rule. If logging is enabled, logs will be exported to the configured export destination in Stackdriver. Logs may be exported to BigQuery or Pub/Sub. Note: you cannot enable logging on "goto_next" rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#enable_logging ComputeFirewallPolicyRule#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#id ComputeFirewallPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param security_profile_group: A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action = 'apply_security_profile_group' and cannot be specified for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#security_profile_group ComputeFirewallPolicyRule#security_profile_group}
        :param target_resources: A list of network resource URLs to which this rule applies. This field allows you to control which network's VMs get this rule. If this field is left blank, all VMs within the organization will receive the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#target_resources ComputeFirewallPolicyRule#target_resources}
        :param target_secure_tags: target_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#target_secure_tags ComputeFirewallPolicyRule#target_secure_tags}
        :param target_service_accounts: A list of service accounts indicating the sets of instances that are applied with this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#target_service_accounts ComputeFirewallPolicyRule#target_service_accounts}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#timeouts ComputeFirewallPolicyRule#timeouts}
        :param tls_inspect: Boolean flag indicating if the traffic should be TLS decrypted. Can be set only if action = 'apply_security_profile_group' and cannot be set for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#tls_inspect ComputeFirewallPolicyRule#tls_inspect}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc310c95580f8123781e53a3a63fee58f11babca892566bbc1a3e53d69edc2f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeFirewallPolicyRuleConfig(
            action=action,
            direction=direction,
            firewall_policy=firewall_policy,
            match=match,
            priority=priority,
            description=description,
            disabled=disabled,
            enable_logging=enable_logging,
            id=id,
            security_profile_group=security_profile_group,
            target_resources=target_resources,
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
        '''Generates CDKTF code for importing a ComputeFirewallPolicyRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeFirewallPolicyRule to import.
        :param import_from_id: The id of the existing ComputeFirewallPolicyRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeFirewallPolicyRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3205242800de2f54e9cfc000f75387758d4e0eefd5b9cfb4ccefe03c21c8aa11)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        layer4_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyRuleMatchLayer4Configs", typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyRuleMatchSrcSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_configs: layer4_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#layer4_configs ComputeFirewallPolicyRule#layer4_configs}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_address_groups ComputeFirewallPolicyRule#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_fqdns ComputeFirewallPolicyRule#dest_fqdns}
        :param dest_ip_ranges: CIDR IP address range. Maximum number of destination CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_ip_ranges ComputeFirewallPolicyRule#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of dest region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_region_codes ComputeFirewallPolicyRule#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_threat_intelligences ComputeFirewallPolicyRule#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_address_groups ComputeFirewallPolicyRule#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_fqdns ComputeFirewallPolicyRule#src_fqdns}
        :param src_ip_ranges: CIDR IP address range. Maximum number of source CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_ip_ranges ComputeFirewallPolicyRule#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_region_codes ComputeFirewallPolicyRule#src_region_codes}
        :param src_secure_tags: src_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_secure_tags ComputeFirewallPolicyRule#src_secure_tags}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_threat_intelligences ComputeFirewallPolicyRule#src_threat_intelligences}
        '''
        value = ComputeFirewallPolicyRuleMatch(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyRuleTargetSecureTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f518f00580bd563580def0acbfbd66920b03863c1e7e05ea41da73e9ef7236)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#create ComputeFirewallPolicyRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#delete ComputeFirewallPolicyRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#update ComputeFirewallPolicyRule#update}.
        '''
        value = ComputeFirewallPolicyRuleTimeouts(
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

    @jsii.member(jsii_name="resetSecurityProfileGroup")
    def reset_security_profile_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityProfileGroup", []))

    @jsii.member(jsii_name="resetTargetResources")
    def reset_target_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResources", []))

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
    def match(self) -> "ComputeFirewallPolicyRuleMatchOutputReference":
        return typing.cast("ComputeFirewallPolicyRuleMatchOutputReference", jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="ruleTupleCount")
    def rule_tuple_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleTupleCount"))

    @builtins.property
    @jsii.member(jsii_name="targetSecureTags")
    def target_secure_tags(self) -> "ComputeFirewallPolicyRuleTargetSecureTagsList":
        return typing.cast("ComputeFirewallPolicyRuleTargetSecureTagsList", jsii.get(self, "targetSecureTags"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeFirewallPolicyRuleTimeoutsOutputReference":
        return typing.cast("ComputeFirewallPolicyRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def match_input(self) -> typing.Optional["ComputeFirewallPolicyRuleMatch"]:
        return typing.cast(typing.Optional["ComputeFirewallPolicyRuleMatch"], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileGroupInput")
    def security_profile_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityProfileGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourcesInput")
    def target_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSecureTagsInput")
    def target_secure_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleTargetSecureTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleTargetSecureTags"]]], jsii.get(self, "targetSecureTagsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeFirewallPolicyRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeFirewallPolicyRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__db803cf88d76bb61ff641f721faa6524ec964f77c3905d8fd64e599e4a28e8ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216bc2cd24e7b10db5062b9b9ebe0bccb2b57cfdcd332e7439f60cbda567c453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4cc585d2b66cae726e7f39479dbd398aef7200ee22cd683bb8c2895ccb2847)
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
            type_hints = typing.get_type_hints(_typecheckingstub__254b7e978648afd539821f92a3f6a4e7a9fa9286981a4510daf96c78731b1885)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35c1168c2b05fff960f3360a67c1b765962f48de9aad19310046c09e11486874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firewallPolicy")
    def firewall_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicy"))

    @firewall_policy.setter
    def firewall_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acba60c84297b9d987b48f827542b9fdf0b122527aa9657d32b71cf03cecab07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a0f2a77634337f85a4c1a03d491f987675bbe8e1e942c3a91ec228a7f8cf28a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afecd6967b022a59d4c65d481bbf19224921c579c87a82ab4750c48cb5b9f4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityProfileGroup")
    def security_profile_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProfileGroup"))

    @security_profile_group.setter
    def security_profile_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4120ed48c0c33b56778285a1430514471e86ecba8e2ac412d82fab0c4c48273b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProfileGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResources")
    def target_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetResources"))

    @target_resources.setter
    def target_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb728e8091aa67b3a4c226dafb3b775eb97f001afb1ae983bdd54ab4cfd70de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetServiceAccounts")
    def target_service_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetServiceAccounts"))

    @target_service_accounts.setter
    def target_service_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f981b6cfdd6f355b523eef5e74e203f3493ece2831df1be4d607957b48d924c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b33e70f38bfe27493324e794a6115764e7351672c87101490a2084fa9999b634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsInspect", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleConfig",
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
        "security_profile_group": "securityProfileGroup",
        "target_resources": "targetResources",
        "target_secure_tags": "targetSecureTags",
        "target_service_accounts": "targetServiceAccounts",
        "timeouts": "timeouts",
        "tls_inspect": "tlsInspect",
    },
)
class ComputeFirewallPolicyRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        match: typing.Union["ComputeFirewallPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        security_profile_group: typing.Optional[builtins.str] = None,
        target_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyRuleTargetSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeFirewallPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param action: The Action to perform when the client connection triggers the rule. Valid actions are "allow", "deny", "goto_next" and "apply_security_profile_group". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#action ComputeFirewallPolicyRule#action}
        :param direction: The direction in which this rule applies. Possible values: ["INGRESS", "EGRESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#direction ComputeFirewallPolicyRule#direction}
        :param firewall_policy: The firewall policy of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#firewall_policy ComputeFirewallPolicyRule#firewall_policy}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#match ComputeFirewallPolicyRule#match}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#priority ComputeFirewallPolicyRule#priority}
        :param description: An optional description for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#description ComputeFirewallPolicyRule#description}
        :param disabled: Denotes whether the firewall policy rule is disabled. When set to true, the firewall policy rule is not enforced and traffic behaves as if it did not exist. If this is unspecified, the firewall policy rule will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#disabled ComputeFirewallPolicyRule#disabled}
        :param enable_logging: Denotes whether to enable logging for a particular rule. If logging is enabled, logs will be exported to the configured export destination in Stackdriver. Logs may be exported to BigQuery or Pub/Sub. Note: you cannot enable logging on "goto_next" rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#enable_logging ComputeFirewallPolicyRule#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#id ComputeFirewallPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param security_profile_group: A fully-qualified URL of a SecurityProfile resource instance. Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group Must be specified if action = 'apply_security_profile_group' and cannot be specified for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#security_profile_group ComputeFirewallPolicyRule#security_profile_group}
        :param target_resources: A list of network resource URLs to which this rule applies. This field allows you to control which network's VMs get this rule. If this field is left blank, all VMs within the organization will receive the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#target_resources ComputeFirewallPolicyRule#target_resources}
        :param target_secure_tags: target_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#target_secure_tags ComputeFirewallPolicyRule#target_secure_tags}
        :param target_service_accounts: A list of service accounts indicating the sets of instances that are applied with this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#target_service_accounts ComputeFirewallPolicyRule#target_service_accounts}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#timeouts ComputeFirewallPolicyRule#timeouts}
        :param tls_inspect: Boolean flag indicating if the traffic should be TLS decrypted. Can be set only if action = 'apply_security_profile_group' and cannot be set for other actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#tls_inspect ComputeFirewallPolicyRule#tls_inspect}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(match, dict):
            match = ComputeFirewallPolicyRuleMatch(**match)
        if isinstance(timeouts, dict):
            timeouts = ComputeFirewallPolicyRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253a2a168b141fca8cca7c5a716217035eb3b46750645899a305de826ee38eb4)
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
            check_type(argname="argument security_profile_group", value=security_profile_group, expected_type=type_hints["security_profile_group"])
            check_type(argname="argument target_resources", value=target_resources, expected_type=type_hints["target_resources"])
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
        if security_profile_group is not None:
            self._values["security_profile_group"] = security_profile_group
        if target_resources is not None:
            self._values["target_resources"] = target_resources
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#action ComputeFirewallPolicyRule#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def direction(self) -> builtins.str:
        '''The direction in which this rule applies. Possible values: ["INGRESS", "EGRESS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#direction ComputeFirewallPolicyRule#direction}
        '''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def firewall_policy(self) -> builtins.str:
        '''The firewall policy of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#firewall_policy ComputeFirewallPolicyRule#firewall_policy}
        '''
        result = self._values.get("firewall_policy")
        assert result is not None, "Required property 'firewall_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(self) -> "ComputeFirewallPolicyRuleMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#match ComputeFirewallPolicyRule#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("ComputeFirewallPolicyRuleMatch", result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An integer indicating the priority of a rule in the list.

        The priority must be a positive value between 0 and 2147483647.
        Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#priority ComputeFirewallPolicyRule#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#description ComputeFirewallPolicyRule#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#disabled ComputeFirewallPolicyRule#disabled}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#enable_logging ComputeFirewallPolicyRule#enable_logging}
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#id ComputeFirewallPolicyRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_profile_group(self) -> typing.Optional[builtins.str]:
        '''A fully-qualified URL of a SecurityProfile resource instance.

        Example: https://networksecurity.googleapis.com/v1/projects/{project}/locations/{location}/securityProfileGroups/my-security-profile-group
        Must be specified if action = 'apply_security_profile_group' and cannot be specified for other actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#security_profile_group ComputeFirewallPolicyRule#security_profile_group}
        '''
        result = self._values.get("security_profile_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of network resource URLs to which this rule applies.

        This field allows you to control which network's VMs get this rule.
        If this field is left blank, all VMs within the organization will receive the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#target_resources ComputeFirewallPolicyRule#target_resources}
        '''
        result = self._values.get("target_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_secure_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleTargetSecureTags"]]]:
        '''target_secure_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#target_secure_tags ComputeFirewallPolicyRule#target_secure_tags}
        '''
        result = self._values.get("target_secure_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleTargetSecureTags"]]], result)

    @builtins.property
    def target_service_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of service accounts indicating the sets of instances that are applied with this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#target_service_accounts ComputeFirewallPolicyRule#target_service_accounts}
        '''
        result = self._values.get("target_service_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeFirewallPolicyRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#timeouts ComputeFirewallPolicyRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeFirewallPolicyRuleTimeouts"], result)

    @builtins.property
    def tls_inspect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean flag indicating if the traffic should be TLS decrypted.

        Can be set only if action = 'apply_security_profile_group' and cannot be set for other actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#tls_inspect ComputeFirewallPolicyRule#tls_inspect}
        '''
        result = self._values.get("tls_inspect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleMatch",
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
class ComputeFirewallPolicyRuleMatch:
    def __init__(
        self,
        *,
        layer4_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyRuleMatchLayer4Configs", typing.Dict[builtins.str, typing.Any]]]],
        dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyRuleMatchSrcSecureTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param layer4_configs: layer4_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#layer4_configs ComputeFirewallPolicyRule#layer4_configs}
        :param dest_address_groups: Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_address_groups ComputeFirewallPolicyRule#dest_address_groups}
        :param dest_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic destination. Maximum number of destination fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_fqdns ComputeFirewallPolicyRule#dest_fqdns}
        :param dest_ip_ranges: CIDR IP address range. Maximum number of destination CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_ip_ranges ComputeFirewallPolicyRule#dest_ip_ranges}
        :param dest_region_codes: Region codes whose IP addresses will be used to match for destination of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of dest region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_region_codes ComputeFirewallPolicyRule#dest_region_codes}
        :param dest_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_threat_intelligences ComputeFirewallPolicyRule#dest_threat_intelligences}
        :param src_address_groups: Address groups which should be matched against the traffic source. Maximum number of source address groups is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_address_groups ComputeFirewallPolicyRule#src_address_groups}
        :param src_fqdns: Fully Qualified Domain Name (FQDN) which should be matched against traffic source. Maximum number of source fqdn allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_fqdns ComputeFirewallPolicyRule#src_fqdns}
        :param src_ip_ranges: CIDR IP address range. Maximum number of source CIDR IP ranges allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_ip_ranges ComputeFirewallPolicyRule#src_ip_ranges}
        :param src_region_codes: Region codes whose IP addresses will be used to match for source of traffic. Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_region_codes ComputeFirewallPolicyRule#src_region_codes}
        :param src_secure_tags: src_secure_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_secure_tags ComputeFirewallPolicyRule#src_secure_tags}
        :param src_threat_intelligences: Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_threat_intelligences ComputeFirewallPolicyRule#src_threat_intelligences}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c99c3616500aaffcacdb9c247e12a208900ce40b21d22724a4e473d03ede765)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleMatchLayer4Configs"]]:
        '''layer4_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#layer4_configs ComputeFirewallPolicyRule#layer4_configs}
        '''
        result = self._values.get("layer4_configs")
        assert result is not None, "Required property 'layer4_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleMatchLayer4Configs"]], result)

    @builtins.property
    def dest_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic destination. Maximum number of destination address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_address_groups ComputeFirewallPolicyRule#dest_address_groups}
        '''
        result = self._values.get("dest_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic destination.

        Maximum number of destination fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_fqdns ComputeFirewallPolicyRule#dest_fqdns}
        '''
        result = self._values.get("dest_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of destination CIDR IP ranges allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_ip_ranges ComputeFirewallPolicyRule#dest_ip_ranges}
        '''
        result = self._values.get("dest_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for destination of traffic.

        Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of dest region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_region_codes ComputeFirewallPolicyRule#dest_region_codes}
        '''
        result = self._values.get("dest_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#dest_threat_intelligences ComputeFirewallPolicyRule#dest_threat_intelligences}
        '''
        result = self._values.get("dest_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_address_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Address groups which should be matched against the traffic source. Maximum number of source address groups is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_address_groups ComputeFirewallPolicyRule#src_address_groups}
        '''
        result = self._values.get("src_address_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fully Qualified Domain Name (FQDN) which should be matched against traffic source.

        Maximum number of source fqdn allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_fqdns ComputeFirewallPolicyRule#src_fqdns}
        '''
        result = self._values.get("src_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of source CIDR IP ranges allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_ip_ranges ComputeFirewallPolicyRule#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Region codes whose IP addresses will be used to match for source of traffic.

        Should be specified as 2 letter country code defined as per ISO 3166 alpha-2 country codes. ex."US" Maximum number of source region codes allowed is 5000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_region_codes ComputeFirewallPolicyRule#src_region_codes}
        '''
        result = self._values.get("src_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_secure_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleMatchSrcSecureTags"]]]:
        '''src_secure_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_secure_tags ComputeFirewallPolicyRule#src_secure_tags}
        '''
        result = self._values.get("src_secure_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleMatchSrcSecureTags"]]], result)

    @builtins.property
    def src_threat_intelligences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Network Threat Intelligence lists. The IPs in these lists will be matched against traffic source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#src_threat_intelligences ComputeFirewallPolicyRule#src_threat_intelligences}
        '''
        result = self._values.get("src_threat_intelligences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleMatchLayer4Configs",
    jsii_struct_bases=[],
    name_mapping={"ip_protocol": "ipProtocol", "ports": "ports"},
)
class ComputeFirewallPolicyRuleMatchLayer4Configs:
    def __init__(
        self,
        *,
        ip_protocol: builtins.str,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ip_protocol: The IP protocol to which this rule applies. The protocol type is required when creating a firewall rule. This value can either be one of the following well known protocol strings (tcp, udp, icmp, esp, ah, ipip, sctp), or the IP protocol number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#ip_protocol ComputeFirewallPolicyRule#ip_protocol}
        :param ports: An optional list of ports to which this rule applies. This field is only applicable for UDP or TCP protocol. Each entry must be either an integer or a range. If not specified, this rule applies to connections through any port. Example inputs include: ["22"], ["80","443"], and ["12345-12349"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#ports ComputeFirewallPolicyRule#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f82599934b696a759aabab1bb07144c2dbab65a6e4faac02d20cd244e97946)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#ip_protocol ComputeFirewallPolicyRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional list of ports to which this rule applies.

        This field is only applicable for UDP or TCP protocol. Each entry must be either an integer or a range. If not specified, this rule applies to connections through any port.
        Example inputs include: ["22"], ["80","443"], and ["12345-12349"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#ports ComputeFirewallPolicyRule#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyRuleMatchLayer4Configs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyRuleMatchLayer4ConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleMatchLayer4ConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7af8208fe5691739202fe4e8dc48a40f0c2c82276e788fac1d84c0b27fe3ec8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyRuleMatchLayer4ConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4d0b27c7a0719332e3e6513e9d6a12a358ade6afc80b38d4876bc9485ea494)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyRuleMatchLayer4ConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca0d76a4c0a4491ea19485bcea4693d34fac12696ec3ad9961cf34418935830)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a55208dc516fb8111a78431894e1532154ce8021928fc411405c274af6de576)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba62523772852cd9ed3e7ce528394b79cef3ac32754764b1478a5fd1b0800f02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchLayer4Configs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchLayer4Configs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchLayer4Configs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7246e32c65c837551913425597ca1543b33745ad35a0124e806d0ec700a633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyRuleMatchLayer4ConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleMatchLayer4ConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0dd641b9c3ca4f9527284ec3374f147230d30b20221684833a8db102efa6470)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99bda572accb78ea9d11d008b0d5f2d72a672e91af7e6c3fad1b80300a1c6a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541a249dbb86b9c681268b57fe1625c5ae7deb3e29997a4c9a78d97c7bd45b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleMatchLayer4Configs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleMatchLayer4Configs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleMatchLayer4Configs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfa74872d2af7a85cc88cc769a5f78f6e65f62d25d9a4d9d2740c1db96dfe17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cadd39cacd39d2cbc00a16abf89592716b0874f3f243cffef8a7fddf071858c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLayer4Configs")
    def put_layer4_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyRuleMatchLayer4Configs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18a08cb40c9b59e7522276e148c5479e02f7076d552d61f7ab0ebb414a67170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLayer4Configs", [value]))

    @jsii.member(jsii_name="putSrcSecureTags")
    def put_src_secure_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeFirewallPolicyRuleMatchSrcSecureTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49191465d61796acda9b3a1403a8bb60e4caf7786134cec045846d996d5d7c9)
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
    def layer4_configs(self) -> ComputeFirewallPolicyRuleMatchLayer4ConfigsList:
        return typing.cast(ComputeFirewallPolicyRuleMatchLayer4ConfigsList, jsii.get(self, "layer4Configs"))

    @builtins.property
    @jsii.member(jsii_name="srcSecureTags")
    def src_secure_tags(self) -> "ComputeFirewallPolicyRuleMatchSrcSecureTagsList":
        return typing.cast("ComputeFirewallPolicyRuleMatchSrcSecureTagsList", jsii.get(self, "srcSecureTags"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchLayer4Configs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchLayer4Configs]]], jsii.get(self, "layer4ConfigsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleMatchSrcSecureTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeFirewallPolicyRuleMatchSrcSecureTags"]]], jsii.get(self, "srcSecureTagsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ec4dce939ba1c4efb96f9bdb0ed224b26a54eeab73b352a92502c364276e15bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destFqdns")
    def dest_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destFqdns"))

    @dest_fqdns.setter
    def dest_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b8a40039493cb60562f6d85f6bfe6bb79a295ae08fc5dde99a93082c92b096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destIpRanges")
    def dest_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destIpRanges"))

    @dest_ip_ranges.setter
    def dest_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8c0b2b54363b5d7f31765825ab9b76a943caa355e4634b167540900ea4edbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destRegionCodes")
    def dest_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destRegionCodes"))

    @dest_region_codes.setter
    def dest_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ae008243caa6888134bf3c730c3ed5a18c0e06b8ab1779992e040f7b501b17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destThreatIntelligences")
    def dest_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destThreatIntelligences"))

    @dest_threat_intelligences.setter
    def dest_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d0f018bf86cc4980570a269b9334a6bbd010d37819c6d8c937f2703c033c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcAddressGroups")
    def src_address_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcAddressGroups"))

    @src_address_groups.setter
    def src_address_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996f6e646aabc716aaf1b9b39dfe9c7be4bb1798b7c50b39185bcae684e2e635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcAddressGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcFqdns")
    def src_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcFqdns"))

    @src_fqdns.setter
    def src_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781fc632d13e44cfaa1b2a59f0815200ab5d65993802f77ec35af82b2af4ff2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @src_ip_ranges.setter
    def src_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe6785aa455702a0e6f63f9a7e3f90c64a82d0378707a233f92db6c9ac72cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodes")
    def src_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcRegionCodes"))

    @src_region_codes.setter
    def src_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e29168c25301daf7ad3c7b79f527aef93c6d226ce4781b92e4160a8c12dde4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcThreatIntelligences")
    def src_threat_intelligences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcThreatIntelligences"))

    @src_threat_intelligences.setter
    def src_threat_intelligences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f15cefc369498a25da986f7b2d79838e6fc393b93ff7907cc808b71ee94cbcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcThreatIntelligences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeFirewallPolicyRuleMatch]:
        return typing.cast(typing.Optional[ComputeFirewallPolicyRuleMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeFirewallPolicyRuleMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a47e45098ae369cdd8cbecd157756ec1cdc3dc89264ff989ef0f19923ee71e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleMatchSrcSecureTags",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeFirewallPolicyRuleMatchSrcSecureTags:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#name ComputeFirewallPolicyRule#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a1baf4e6621d1c83761a78de34c3743bc9743d97b63adf85ded597cdaa6362)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#name ComputeFirewallPolicyRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyRuleMatchSrcSecureTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyRuleMatchSrcSecureTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleMatchSrcSecureTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cd936482ec8510ef5cd4b8a959e571a5d59c29d5e0244e06ec69d45f1f0e8d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyRuleMatchSrcSecureTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf14e12ab55e2df301e9b04b94ef04bdd5aa167ee9aaa1bd4cd530b37bb14d48)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyRuleMatchSrcSecureTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde44571a517a2e09ffe41724d812ddd50c8a508f84fb1d13c2c9498f8fa5998)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4ef4f0e464e1767aa74b8c0e6545c3172b9a86cfd94eaf78331a8599098c2bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d5bdfffe226e578fb4a2c1edd6a73b22931071ddac5f2a88a5354b2c2d23b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchSrcSecureTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchSrcSecureTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchSrcSecureTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9d5c607705702964ed1bca5b8f5d3353217feef2861b341922c7c2bbc05ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyRuleMatchSrcSecureTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleMatchSrcSecureTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2351562f8139fc747f753f3885d74b381f6fa636516d4a0be3ed3a807b7e5fd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__077be0b55992828b0c55a1b05dfbb52d124e64baa16deba670631a48fba5c894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleMatchSrcSecureTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleMatchSrcSecureTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleMatchSrcSecureTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c44bcdad24f43d061457143f87aad780597c1308cc251c574c34ecb662a9fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleTargetSecureTags",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeFirewallPolicyRuleTargetSecureTags:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Name of the secure tag, created with TagManager's TagValue API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#name ComputeFirewallPolicyRule#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb92ccfea88d60d9741405d8db0bd9e58ba6a239f9b69bc41432cd92b889048)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the secure tag, created with TagManager's TagValue API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#name ComputeFirewallPolicyRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyRuleTargetSecureTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyRuleTargetSecureTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleTargetSecureTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45a0ec21d3a8e16e085d53b91cf2a659fcc2465e77118fa75aed9371d976ea6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeFirewallPolicyRuleTargetSecureTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd461450dd61816f71ad0f6a00d2b248aa9ca1a7c87cd38e634266db0a1e438d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeFirewallPolicyRuleTargetSecureTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444b8b88f55e4d776b39d8ab7ab12db67a01ef41eff7eff2cb58eaf44f9b4821)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3719488cf02b4bc6460f5ae8b282eca2dbdc67e11253d47810eb27561bc7e256)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3058414bf175359451aa9c5d34fc02aee977368301364d3da9da2fe25a087973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleTargetSecureTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleTargetSecureTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleTargetSecureTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0bd1516dd94368a06ac36dd529b734be6aca313ff1dedbc00ef1f515584f5ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeFirewallPolicyRuleTargetSecureTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleTargetSecureTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ce9838ec70d1c5e3d9ffa3adf6fcc6b5ceef88c478f5bf0ccae570264367e35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5611744eaf0769c8f2f0aa2ce3deb6dc63e952272f1cc30cfbb9d71161490567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleTargetSecureTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleTargetSecureTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleTargetSecureTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6db55a84370426409737c01fb8cb4e3b7c2e1401aa350eafcb9b8cbebd22f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeFirewallPolicyRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#create ComputeFirewallPolicyRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#delete ComputeFirewallPolicyRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#update ComputeFirewallPolicyRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d925a2cbe882fb47c07a7e4e6eb0e7e7e107b415923024efe8abb3dbd7493e4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#create ComputeFirewallPolicyRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#delete ComputeFirewallPolicyRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_firewall_policy_rule#update ComputeFirewallPolicyRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFirewallPolicyRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeFirewallPolicyRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeFirewallPolicyRule.ComputeFirewallPolicyRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__020da2e07d6094a3a701f6de4a7588eae5da6ed1c55e2f8103944c4686954712)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53f44fdcf98c98350aedd5f8d0507c8c165a35cceb0f72326c11bdafc0b3c9ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c26d553753c3da1728ad899a6893a5c6ca26b39f59e8c61f53566874d6ad7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae7bd4fdc1e9b44b169922d9b1e0a809b11313f13e1966878c1ab3af41c1e27e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ccf489166c77dfc7d33777f6dc5114412a00d7b0b692d841d53bb306b897c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeFirewallPolicyRule",
    "ComputeFirewallPolicyRuleConfig",
    "ComputeFirewallPolicyRuleMatch",
    "ComputeFirewallPolicyRuleMatchLayer4Configs",
    "ComputeFirewallPolicyRuleMatchLayer4ConfigsList",
    "ComputeFirewallPolicyRuleMatchLayer4ConfigsOutputReference",
    "ComputeFirewallPolicyRuleMatchOutputReference",
    "ComputeFirewallPolicyRuleMatchSrcSecureTags",
    "ComputeFirewallPolicyRuleMatchSrcSecureTagsList",
    "ComputeFirewallPolicyRuleMatchSrcSecureTagsOutputReference",
    "ComputeFirewallPolicyRuleTargetSecureTags",
    "ComputeFirewallPolicyRuleTargetSecureTagsList",
    "ComputeFirewallPolicyRuleTargetSecureTagsOutputReference",
    "ComputeFirewallPolicyRuleTimeouts",
    "ComputeFirewallPolicyRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dc310c95580f8123781e53a3a63fee58f11babca892566bbc1a3e53d69edc2f8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    direction: builtins.str,
    firewall_policy: builtins.str,
    match: typing.Union[ComputeFirewallPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    security_profile_group: typing.Optional[builtins.str] = None,
    target_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyRuleTargetSecureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeFirewallPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3205242800de2f54e9cfc000f75387758d4e0eefd5b9cfb4ccefe03c21c8aa11(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f518f00580bd563580def0acbfbd66920b03863c1e7e05ea41da73e9ef7236(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyRuleTargetSecureTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db803cf88d76bb61ff641f721faa6524ec964f77c3905d8fd64e599e4a28e8ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216bc2cd24e7b10db5062b9b9ebe0bccb2b57cfdcd332e7439f60cbda567c453(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4cc585d2b66cae726e7f39479dbd398aef7200ee22cd683bb8c2895ccb2847(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254b7e978648afd539821f92a3f6a4e7a9fa9286981a4510daf96c78731b1885(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c1168c2b05fff960f3360a67c1b765962f48de9aad19310046c09e11486874(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acba60c84297b9d987b48f827542b9fdf0b122527aa9657d32b71cf03cecab07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0f2a77634337f85a4c1a03d491f987675bbe8e1e942c3a91ec228a7f8cf28a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afecd6967b022a59d4c65d481bbf19224921c579c87a82ab4750c48cb5b9f4d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4120ed48c0c33b56778285a1430514471e86ecba8e2ac412d82fab0c4c48273b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb728e8091aa67b3a4c226dafb3b775eb97f001afb1ae983bdd54ab4cfd70de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f981b6cfdd6f355b523eef5e74e203f3493ece2831df1be4d607957b48d924c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33e70f38bfe27493324e794a6115764e7351672c87101490a2084fa9999b634(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253a2a168b141fca8cca7c5a716217035eb3b46750645899a305de826ee38eb4(
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
    match: typing.Union[ComputeFirewallPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    security_profile_group: typing.Optional[builtins.str] = None,
    target_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyRuleTargetSecureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeFirewallPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_inspect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c99c3616500aaffcacdb9c247e12a208900ce40b21d22724a4e473d03ede765(
    *,
    layer4_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyRuleMatchLayer4Configs, typing.Dict[builtins.str, typing.Any]]]],
    dest_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_address_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_secure_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyRuleMatchSrcSecureTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    src_threat_intelligences: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f82599934b696a759aabab1bb07144c2dbab65a6e4faac02d20cd244e97946(
    *,
    ip_protocol: builtins.str,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af8208fe5691739202fe4e8dc48a40f0c2c82276e788fac1d84c0b27fe3ec8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4d0b27c7a0719332e3e6513e9d6a12a358ade6afc80b38d4876bc9485ea494(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca0d76a4c0a4491ea19485bcea4693d34fac12696ec3ad9961cf34418935830(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a55208dc516fb8111a78431894e1532154ce8021928fc411405c274af6de576(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba62523772852cd9ed3e7ce528394b79cef3ac32754764b1478a5fd1b0800f02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7246e32c65c837551913425597ca1543b33745ad35a0124e806d0ec700a633(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchLayer4Configs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0dd641b9c3ca4f9527284ec3374f147230d30b20221684833a8db102efa6470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bda572accb78ea9d11d008b0d5f2d72a672e91af7e6c3fad1b80300a1c6a04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541a249dbb86b9c681268b57fe1625c5ae7deb3e29997a4c9a78d97c7bd45b5c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfa74872d2af7a85cc88cc769a5f78f6e65f62d25d9a4d9d2740c1db96dfe17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleMatchLayer4Configs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cadd39cacd39d2cbc00a16abf89592716b0874f3f243cffef8a7fddf071858c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18a08cb40c9b59e7522276e148c5479e02f7076d552d61f7ab0ebb414a67170(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyRuleMatchLayer4Configs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49191465d61796acda9b3a1403a8bb60e4caf7786134cec045846d996d5d7c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeFirewallPolicyRuleMatchSrcSecureTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4dce939ba1c4efb96f9bdb0ed224b26a54eeab73b352a92502c364276e15bb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b8a40039493cb60562f6d85f6bfe6bb79a295ae08fc5dde99a93082c92b096(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8c0b2b54363b5d7f31765825ab9b76a943caa355e4634b167540900ea4edbb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ae008243caa6888134bf3c730c3ed5a18c0e06b8ab1779992e040f7b501b17(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d0f018bf86cc4980570a269b9334a6bbd010d37819c6d8c937f2703c033c8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996f6e646aabc716aaf1b9b39dfe9c7be4bb1798b7c50b39185bcae684e2e635(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781fc632d13e44cfaa1b2a59f0815200ab5d65993802f77ec35af82b2af4ff2f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe6785aa455702a0e6f63f9a7e3f90c64a82d0378707a233f92db6c9ac72cf5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e29168c25301daf7ad3c7b79f527aef93c6d226ce4781b92e4160a8c12dde4e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f15cefc369498a25da986f7b2d79838e6fc393b93ff7907cc808b71ee94cbcc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a47e45098ae369cdd8cbecd157756ec1cdc3dc89264ff989ef0f19923ee71e4(
    value: typing.Optional[ComputeFirewallPolicyRuleMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a1baf4e6621d1c83761a78de34c3743bc9743d97b63adf85ded597cdaa6362(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd936482ec8510ef5cd4b8a959e571a5d59c29d5e0244e06ec69d45f1f0e8d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf14e12ab55e2df301e9b04b94ef04bdd5aa167ee9aaa1bd4cd530b37bb14d48(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde44571a517a2e09ffe41724d812ddd50c8a508f84fb1d13c2c9498f8fa5998(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ef4f0e464e1767aa74b8c0e6545c3172b9a86cfd94eaf78331a8599098c2bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5bdfffe226e578fb4a2c1edd6a73b22931071ddac5f2a88a5354b2c2d23b8a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9d5c607705702964ed1bca5b8f5d3353217feef2861b341922c7c2bbc05ee9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleMatchSrcSecureTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2351562f8139fc747f753f3885d74b381f6fa636516d4a0be3ed3a807b7e5fd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077be0b55992828b0c55a1b05dfbb52d124e64baa16deba670631a48fba5c894(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c44bcdad24f43d061457143f87aad780597c1308cc251c574c34ecb662a9fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleMatchSrcSecureTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb92ccfea88d60d9741405d8db0bd9e58ba6a239f9b69bc41432cd92b889048(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a0ec21d3a8e16e085d53b91cf2a659fcc2465e77118fa75aed9371d976ea6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd461450dd61816f71ad0f6a00d2b248aa9ca1a7c87cd38e634266db0a1e438d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444b8b88f55e4d776b39d8ab7ab12db67a01ef41eff7eff2cb58eaf44f9b4821(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3719488cf02b4bc6460f5ae8b282eca2dbdc67e11253d47810eb27561bc7e256(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3058414bf175359451aa9c5d34fc02aee977368301364d3da9da2fe25a087973(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bd1516dd94368a06ac36dd529b734be6aca313ff1dedbc00ef1f515584f5ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeFirewallPolicyRuleTargetSecureTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce9838ec70d1c5e3d9ffa3adf6fcc6b5ceef88c478f5bf0ccae570264367e35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5611744eaf0769c8f2f0aa2ce3deb6dc63e952272f1cc30cfbb9d71161490567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6db55a84370426409737c01fb8cb4e3b7c2e1401aa350eafcb9b8cbebd22f5f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleTargetSecureTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d925a2cbe882fb47c07a7e4e6eb0e7e7e107b415923024efe8abb3dbd7493e4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020da2e07d6094a3a701f6de4a7588eae5da6ed1c55e2f8103944c4686954712(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f44fdcf98c98350aedd5f8d0507c8c165a35cceb0f72326c11bdafc0b3c9ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c26d553753c3da1728ad899a6893a5c6ca26b39f59e8c61f53566874d6ad7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7bd4fdc1e9b44b169922d9b1e0a809b11313f13e1966878c1ab3af41c1e27e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccf489166c77dfc7d33777f6dc5114412a00d7b0b692d841d53bb306b897c7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeFirewallPolicyRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
