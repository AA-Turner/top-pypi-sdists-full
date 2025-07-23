r'''
# `google_compute_region_security_policy_rule`

Refer to the Terraform Registry for docs: [`google_compute_region_security_policy_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule).
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


class ComputeRegionSecurityPolicyRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule google_compute_region_security_policy_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        priority: jsii.Number,
        region: builtins.str,
        security_policy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        network_match: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleNetworkMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        preconfigured_waf_config: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limit_options: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleRateLimitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule google_compute_region_security_policy_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: The Action to perform when the rule is matched. The following are the valid actions:. - allow: allow access to target. - deny(STATUS): deny access to target, returns the HTTP response code specified. Valid values for STATUS are 403, 404, and 502. - rate_based_ban: limit client traffic to the configured threshold and ban the client if the traffic exceeds the threshold. Configure parameters for this action in RateLimitOptions. Requires rateLimitOptions to be set. - redirect: redirect to a different target. This can either be an internal reCAPTCHA redirect, or an external URL-based redirect via a 302 response. Parameters for this action can be configured via redirectOptions. This action is only supported in Global Security Policies of type CLOUD_ARMOR. - throttle: limit client traffic to the configured threshold. Configure parameters for this action in rateLimitOptions. Requires rateLimitOptions to be set for this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#action ComputeRegionSecurityPolicyRule#action}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#priority ComputeRegionSecurityPolicyRule#priority}
        :param region: The Region in which the created Region Security Policy rule should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#region ComputeRegionSecurityPolicyRule#region}
        :param security_policy: The name of the security policy this rule belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#security_policy ComputeRegionSecurityPolicyRule#security_policy}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#description ComputeRegionSecurityPolicyRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#id ComputeRegionSecurityPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#match ComputeRegionSecurityPolicyRule#match}
        :param network_match: network_match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#network_match ComputeRegionSecurityPolicyRule#network_match}
        :param preconfigured_waf_config: preconfigured_waf_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#preconfigured_waf_config ComputeRegionSecurityPolicyRule#preconfigured_waf_config}
        :param preview: If set to true, the specified action is not enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#preview ComputeRegionSecurityPolicyRule#preview}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#project ComputeRegionSecurityPolicyRule#project}.
        :param rate_limit_options: rate_limit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#rate_limit_options ComputeRegionSecurityPolicyRule#rate_limit_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#timeouts ComputeRegionSecurityPolicyRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df3c8ef98b083f131d1d6a36b958dc7c40a0c9b88067156522a2a7cf8c46b4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionSecurityPolicyRuleConfig(
            action=action,
            priority=priority,
            region=region,
            security_policy=security_policy,
            description=description,
            id=id,
            match=match,
            network_match=network_match,
            preconfigured_waf_config=preconfigured_waf_config,
            preview=preview,
            project=project,
            rate_limit_options=rate_limit_options,
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
        '''Generates CDKTF code for importing a ComputeRegionSecurityPolicyRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionSecurityPolicyRule to import.
        :param import_from_id: The id of the existing ComputeRegionSecurityPolicyRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionSecurityPolicyRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a24533a54c5399dd03845eb847dba23341099a20c34661dc84281f3cfb5425b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        config: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleMatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleMatchExpr", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#config ComputeRegionSecurityPolicyRule#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#expr ComputeRegionSecurityPolicyRule#expr}
        :param versioned_expr: Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#versioned_expr ComputeRegionSecurityPolicyRule#versioned_expr}
        '''
        value = ComputeRegionSecurityPolicyRuleMatch(
            config=config, expr=expr, versioned_expr=versioned_expr
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putNetworkMatch")
    def put_network_match(
        self,
        *,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_asns: typing.Optional[typing.Sequence[jsii.Number]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dest_ip_ranges: Destination IPv4/IPv6 addresses or CIDR prefixes, in standard text format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#dest_ip_ranges ComputeRegionSecurityPolicyRule#dest_ip_ranges}
        :param dest_ports: Destination port numbers for TCP/UDP/SCTP. Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#dest_ports ComputeRegionSecurityPolicyRule#dest_ports}
        :param ip_protocols: IPv4 protocol / IPv6 next header (after extension headers). Each element can be an 8-bit unsigned decimal number (e.g. "6"), range (e.g. "253-254"), or one of the following protocol names: "tcp", "udp", "icmp", "esp", "ah", "ipip", or "sctp". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#ip_protocols ComputeRegionSecurityPolicyRule#ip_protocols}
        :param src_asns: BGP Autonomous System Number associated with the source IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_asns ComputeRegionSecurityPolicyRule#src_asns}
        :param src_ip_ranges: Source IPv4/IPv6 addresses or CIDR prefixes, in standard text format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_ip_ranges ComputeRegionSecurityPolicyRule#src_ip_ranges}
        :param src_ports: Source port numbers for TCP/UDP/SCTP. Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_ports ComputeRegionSecurityPolicyRule#src_ports}
        :param src_region_codes: Two-letter ISO 3166-1 alpha-2 country code associated with the source IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_region_codes ComputeRegionSecurityPolicyRule#src_region_codes}
        :param user_defined_fields: user_defined_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#user_defined_fields ComputeRegionSecurityPolicyRule#user_defined_fields}
        '''
        value = ComputeRegionSecurityPolicyRuleNetworkMatch(
            dest_ip_ranges=dest_ip_ranges,
            dest_ports=dest_ports,
            ip_protocols=ip_protocols,
            src_asns=src_asns,
            src_ip_ranges=src_ip_ranges,
            src_ports=src_ports,
            src_region_codes=src_region_codes,
            user_defined_fields=user_defined_fields,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkMatch", [value]))

    @jsii.member(jsii_name="putPreconfiguredWafConfig")
    def put_preconfigured_waf_config(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#exclusion ComputeRegionSecurityPolicyRule#exclusion}
        '''
        value = ComputeRegionSecurityPolicyRulePreconfiguredWafConfig(
            exclusion=exclusion
        )

        return typing.cast(None, jsii.invoke(self, "putPreconfiguredWafConfig", [value]))

    @jsii.member(jsii_name="putRateLimitOptions")
    def put_rate_limit_options(
        self,
        *,
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        conform_action: typing.Optional[builtins.str] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_action: typing.Optional[builtins.str] = None,
        rate_limit_threshold: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#ban_duration_sec ComputeRegionSecurityPolicyRule#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#ban_threshold ComputeRegionSecurityPolicyRule#ban_threshold}
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#conform_action ComputeRegionSecurityPolicyRule#conform_action}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key ComputeRegionSecurityPolicyRule#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_configs ComputeRegionSecurityPolicyRule#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_name ComputeRegionSecurityPolicyRule#enforce_on_key_name}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to deny with a specified HTTP response code. Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#exceed_action ComputeRegionSecurityPolicyRule#exceed_action}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#rate_limit_threshold ComputeRegionSecurityPolicyRule#rate_limit_threshold}
        '''
        value = ComputeRegionSecurityPolicyRuleRateLimitOptions(
            ban_duration_sec=ban_duration_sec,
            ban_threshold=ban_threshold,
            conform_action=conform_action,
            enforce_on_key=enforce_on_key,
            enforce_on_key_configs=enforce_on_key_configs,
            enforce_on_key_name=enforce_on_key_name,
            exceed_action=exceed_action,
            rate_limit_threshold=rate_limit_threshold,
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimitOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#create ComputeRegionSecurityPolicyRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#delete ComputeRegionSecurityPolicyRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#update ComputeRegionSecurityPolicyRule#update}.
        '''
        value = ComputeRegionSecurityPolicyRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetNetworkMatch")
    def reset_network_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkMatch", []))

    @jsii.member(jsii_name="resetPreconfiguredWafConfig")
    def reset_preconfigured_waf_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreconfiguredWafConfig", []))

    @jsii.member(jsii_name="resetPreview")
    def reset_preview(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreview", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRateLimitOptions")
    def reset_rate_limit_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimitOptions", []))

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
    @jsii.member(jsii_name="match")
    def match(self) -> "ComputeRegionSecurityPolicyRuleMatchOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyRuleMatchOutputReference", jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="networkMatch")
    def network_match(
        self,
    ) -> "ComputeRegionSecurityPolicyRuleNetworkMatchOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyRuleNetworkMatchOutputReference", jsii.get(self, "networkMatch"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfig")
    def preconfigured_waf_config(
        self,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigOutputReference", jsii.get(self, "preconfiguredWafConfig"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitOptions")
    def rate_limit_options(
        self,
    ) -> "ComputeRegionSecurityPolicyRuleRateLimitOptionsOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyRuleRateLimitOptionsOutputReference", jsii.get(self, "rateLimitOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionSecurityPolicyRuleTimeoutsOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional["ComputeRegionSecurityPolicyRuleMatch"]:
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleMatch"], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="networkMatchInput")
    def network_match_input(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRuleNetworkMatch"]:
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleNetworkMatch"], jsii.get(self, "networkMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfigInput")
    def preconfigured_waf_config_input(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulePreconfiguredWafConfig"]:
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulePreconfiguredWafConfig"], jsii.get(self, "preconfiguredWafConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="previewInput")
    def preview_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "previewInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitOptionsInput")
    def rate_limit_options_input(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptions"]:
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptions"], jsii.get(self, "rateLimitOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPolicyInput")
    def security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionSecurityPolicyRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionSecurityPolicyRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878d27c7b4dc4e0a6a4df8b6d514905602d1f3d5b8eb798a4e226e919cf35f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f216d7688074fda651fc8d9c192ec02ab4a78eb3b5d392e7f28a981e62ffb84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614d5305fe00cf56b537f900e082d75ad597c970dd867fe7e871bf46569606dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preview")
    def preview(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preview"))

    @preview.setter
    def preview(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afd45f0367e46d50ff195df832279e71e90ab838c1ebc9f9ab2c648d2606c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preview", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67397b6a61208353ca0f2768a5c1d954a12e1b504c4d6ae0a0acf944ddd4e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7306d2346823cba4887ba93d9ceba23d2ee902e9cbad074943f36af56dbc46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879bc87702f7911c0d50177c0b7ef41b8194d7eb066077ba857655e55f560d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicy")
    def security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicy"))

    @security_policy.setter
    def security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d6ddc230edb70c6d3b82a1adbb2783a225fc81f1ad57e207184f98e8d62d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleConfig",
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
        "priority": "priority",
        "region": "region",
        "security_policy": "securityPolicy",
        "description": "description",
        "id": "id",
        "match": "match",
        "network_match": "networkMatch",
        "preconfigured_waf_config": "preconfiguredWafConfig",
        "preview": "preview",
        "project": "project",
        "rate_limit_options": "rateLimitOptions",
        "timeouts": "timeouts",
    },
)
class ComputeRegionSecurityPolicyRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        priority: jsii.Number,
        region: builtins.str,
        security_policy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        network_match: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleNetworkMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        preconfigured_waf_config: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limit_options: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleRateLimitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: The Action to perform when the rule is matched. The following are the valid actions:. - allow: allow access to target. - deny(STATUS): deny access to target, returns the HTTP response code specified. Valid values for STATUS are 403, 404, and 502. - rate_based_ban: limit client traffic to the configured threshold and ban the client if the traffic exceeds the threshold. Configure parameters for this action in RateLimitOptions. Requires rateLimitOptions to be set. - redirect: redirect to a different target. This can either be an internal reCAPTCHA redirect, or an external URL-based redirect via a 302 response. Parameters for this action can be configured via redirectOptions. This action is only supported in Global Security Policies of type CLOUD_ARMOR. - throttle: limit client traffic to the configured threshold. Configure parameters for this action in rateLimitOptions. Requires rateLimitOptions to be set for this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#action ComputeRegionSecurityPolicyRule#action}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#priority ComputeRegionSecurityPolicyRule#priority}
        :param region: The Region in which the created Region Security Policy rule should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#region ComputeRegionSecurityPolicyRule#region}
        :param security_policy: The name of the security policy this rule belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#security_policy ComputeRegionSecurityPolicyRule#security_policy}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#description ComputeRegionSecurityPolicyRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#id ComputeRegionSecurityPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#match ComputeRegionSecurityPolicyRule#match}
        :param network_match: network_match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#network_match ComputeRegionSecurityPolicyRule#network_match}
        :param preconfigured_waf_config: preconfigured_waf_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#preconfigured_waf_config ComputeRegionSecurityPolicyRule#preconfigured_waf_config}
        :param preview: If set to true, the specified action is not enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#preview ComputeRegionSecurityPolicyRule#preview}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#project ComputeRegionSecurityPolicyRule#project}.
        :param rate_limit_options: rate_limit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#rate_limit_options ComputeRegionSecurityPolicyRule#rate_limit_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#timeouts ComputeRegionSecurityPolicyRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(match, dict):
            match = ComputeRegionSecurityPolicyRuleMatch(**match)
        if isinstance(network_match, dict):
            network_match = ComputeRegionSecurityPolicyRuleNetworkMatch(**network_match)
        if isinstance(preconfigured_waf_config, dict):
            preconfigured_waf_config = ComputeRegionSecurityPolicyRulePreconfiguredWafConfig(**preconfigured_waf_config)
        if isinstance(rate_limit_options, dict):
            rate_limit_options = ComputeRegionSecurityPolicyRuleRateLimitOptions(**rate_limit_options)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionSecurityPolicyRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186da766d1fb58808cca052eb2470bd9ff41953c961ea67508a62122d743ee69)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument network_match", value=network_match, expected_type=type_hints["network_match"])
            check_type(argname="argument preconfigured_waf_config", value=preconfigured_waf_config, expected_type=type_hints["preconfigured_waf_config"])
            check_type(argname="argument preview", value=preview, expected_type=type_hints["preview"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument rate_limit_options", value=rate_limit_options, expected_type=type_hints["rate_limit_options"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "priority": priority,
            "region": region,
            "security_policy": security_policy,
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
        if id is not None:
            self._values["id"] = id
        if match is not None:
            self._values["match"] = match
        if network_match is not None:
            self._values["network_match"] = network_match
        if preconfigured_waf_config is not None:
            self._values["preconfigured_waf_config"] = preconfigured_waf_config
        if preview is not None:
            self._values["preview"] = preview
        if project is not None:
            self._values["project"] = project
        if rate_limit_options is not None:
            self._values["rate_limit_options"] = rate_limit_options
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
    def action(self) -> builtins.str:
        '''The Action to perform when the rule is matched. The following are the valid actions:.

        - allow: allow access to target.
        - deny(STATUS): deny access to target, returns the HTTP response code specified. Valid values for STATUS are 403, 404, and 502.
        - rate_based_ban: limit client traffic to the configured threshold and ban the client if the traffic exceeds the threshold. Configure parameters for this action in RateLimitOptions. Requires rateLimitOptions to be set.
        - redirect: redirect to a different target. This can either be an internal reCAPTCHA redirect, or an external URL-based redirect via a 302 response. Parameters for this action can be configured via redirectOptions. This action is only supported in Global Security Policies of type CLOUD_ARMOR.
        - throttle: limit client traffic to the configured threshold. Configure parameters for this action in rateLimitOptions. Requires rateLimitOptions to be set for this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#action ComputeRegionSecurityPolicyRule#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An integer indicating the priority of a rule in the list.

        The priority must be a positive value between 0 and 2147483647.
        Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#priority ComputeRegionSecurityPolicyRule#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''The Region in which the created Region Security Policy rule should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#region ComputeRegionSecurityPolicyRule#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_policy(self) -> builtins.str:
        '''The name of the security policy this rule belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#security_policy ComputeRegionSecurityPolicyRule#security_policy}
        '''
        result = self._values.get("security_policy")
        assert result is not None, "Required property 'security_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#description ComputeRegionSecurityPolicyRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#id ComputeRegionSecurityPolicyRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match(self) -> typing.Optional["ComputeRegionSecurityPolicyRuleMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#match ComputeRegionSecurityPolicyRule#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleMatch"], result)

    @builtins.property
    def network_match(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRuleNetworkMatch"]:
        '''network_match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#network_match ComputeRegionSecurityPolicyRule#network_match}
        '''
        result = self._values.get("network_match")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleNetworkMatch"], result)

    @builtins.property
    def preconfigured_waf_config(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulePreconfiguredWafConfig"]:
        '''preconfigured_waf_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#preconfigured_waf_config ComputeRegionSecurityPolicyRule#preconfigured_waf_config}
        '''
        result = self._values.get("preconfigured_waf_config")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulePreconfiguredWafConfig"], result)

    @builtins.property
    def preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the specified action is not enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#preview ComputeRegionSecurityPolicyRule#preview}
        '''
        result = self._values.get("preview")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#project ComputeRegionSecurityPolicyRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limit_options(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptions"]:
        '''rate_limit_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#rate_limit_options ComputeRegionSecurityPolicyRule#rate_limit_options}
        '''
        result = self._values.get("rate_limit_options")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptions"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionSecurityPolicyRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#timeouts ComputeRegionSecurityPolicyRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleMatch",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "expr": "expr",
        "versioned_expr": "versionedExpr",
    },
)
class ComputeRegionSecurityPolicyRuleMatch:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleMatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleMatchExpr", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#config ComputeRegionSecurityPolicyRule#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#expr ComputeRegionSecurityPolicyRule#expr}
        :param versioned_expr: Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#versioned_expr ComputeRegionSecurityPolicyRule#versioned_expr}
        '''
        if isinstance(config, dict):
            config = ComputeRegionSecurityPolicyRuleMatchConfig(**config)
        if isinstance(expr, dict):
            expr = ComputeRegionSecurityPolicyRuleMatchExpr(**expr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701aaba32c96bbfaf7cccffb28e66603f46267052a6ef2b8dfdbc1409a343f8d)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument expr", value=expr, expected_type=type_hints["expr"])
            check_type(argname="argument versioned_expr", value=versioned_expr, expected_type=type_hints["versioned_expr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if expr is not None:
            self._values["expr"] = expr
        if versioned_expr is not None:
            self._values["versioned_expr"] = versioned_expr

    @builtins.property
    def config(self) -> typing.Optional["ComputeRegionSecurityPolicyRuleMatchConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#config ComputeRegionSecurityPolicyRule#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleMatchConfig"], result)

    @builtins.property
    def expr(self) -> typing.Optional["ComputeRegionSecurityPolicyRuleMatchExpr"]:
        '''expr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#expr ComputeRegionSecurityPolicyRule#expr}
        '''
        result = self._values.get("expr")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleMatchExpr"], result)

    @builtins.property
    def versioned_expr(self) -> typing.Optional[builtins.str]:
        '''Preconfigured versioned expression.

        If this field is specified, config must also be specified.
        Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#versioned_expr ComputeRegionSecurityPolicyRule#versioned_expr}
        '''
        result = self._values.get("versioned_expr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleMatchConfig",
    jsii_struct_bases=[],
    name_mapping={"src_ip_ranges": "srcIpRanges"},
)
class ComputeRegionSecurityPolicyRuleMatchConfig:
    def __init__(
        self,
        *,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param src_ip_ranges: CIDR IP address range. Maximum number of srcIpRanges allowed is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_ip_ranges ComputeRegionSecurityPolicyRule#src_ip_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b399797566fc0aa096c9e6a83c4748697751f2841285fad3f214b27e24ea718d)
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if src_ip_ranges is not None:
            self._values["src_ip_ranges"] = src_ip_ranges

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of srcIpRanges allowed is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_ip_ranges ComputeRegionSecurityPolicyRule#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleMatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRuleMatchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleMatchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__493c77714054e8d6b2e9d74869a576cd368f2d380a0c6cedd95ab2c6e508abf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSrcIpRanges")
    def reset_src_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcIpRanges", []))

    @builtins.property
    @jsii.member(jsii_name="srcIpRangesInput")
    def src_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @src_ip_ranges.setter
    def src_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc23092b663a203d55685e9e7458432a041fe79122931e5b4b8da6e5ffcc2949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRuleMatchConfig]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleMatchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRuleMatchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb03d5ba6ade618aefddcf6fab83bf7beea4fd449021b187d5825040e7f2857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleMatchExpr",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class ComputeRegionSecurityPolicyRuleMatchExpr:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#expression ComputeRegionSecurityPolicyRule#expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39602ca742789ee74db2f78e72907dff33af3f385f9bc3d13392e8bd25d0567b)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        The application context of the containing message determines which well-known feature set of CEL is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#expression ComputeRegionSecurityPolicyRule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleMatchExpr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRuleMatchExprOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleMatchExprOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4564664da315a7a5d5a40544a094554267fd478b8316c74c00d02ff95acf0fda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a0746b0bef21351834fdbc1d5554c5c1cfe70caa772c559a7db6fe6dc3794fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRuleMatchExpr]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleMatchExpr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRuleMatchExpr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3f32664d536f441ec60afb1372076d053718147ad6a9142a718b4048cf2a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__feea12b656a90aa1b56722acf16dd592967d2dfb88b3598abad59ce9d6cdcf71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param src_ip_ranges: CIDR IP address range. Maximum number of srcIpRanges allowed is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_ip_ranges ComputeRegionSecurityPolicyRule#src_ip_ranges}
        '''
        value = ComputeRegionSecurityPolicyRuleMatchConfig(src_ip_ranges=src_ip_ranges)

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putExpr")
    def put_expr(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#expression ComputeRegionSecurityPolicyRule#expression}
        '''
        value = ComputeRegionSecurityPolicyRuleMatchExpr(expression=expression)

        return typing.cast(None, jsii.invoke(self, "putExpr", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetExpr")
    def reset_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpr", []))

    @jsii.member(jsii_name="resetVersionedExpr")
    def reset_versioned_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionedExpr", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> ComputeRegionSecurityPolicyRuleMatchConfigOutputReference:
        return typing.cast(ComputeRegionSecurityPolicyRuleMatchConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="expr")
    def expr(self) -> ComputeRegionSecurityPolicyRuleMatchExprOutputReference:
        return typing.cast(ComputeRegionSecurityPolicyRuleMatchExprOutputReference, jsii.get(self, "expr"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRuleMatchConfig]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleMatchConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="exprInput")
    def expr_input(self) -> typing.Optional[ComputeRegionSecurityPolicyRuleMatchExpr]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleMatchExpr], jsii.get(self, "exprInput"))

    @builtins.property
    @jsii.member(jsii_name="versionedExprInput")
    def versioned_expr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionedExprInput"))

    @builtins.property
    @jsii.member(jsii_name="versionedExpr")
    def versioned_expr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionedExpr"))

    @versioned_expr.setter
    def versioned_expr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f0e6906d792149d3a474a77df59c0baa582afa43ab6314ea0293ebfd470501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionedExpr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionSecurityPolicyRuleMatch]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRuleMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3dc00d7b715373537ff1495216347b8c0e3ea7a724956e29d4e80477afb7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleNetworkMatch",
    jsii_struct_bases=[],
    name_mapping={
        "dest_ip_ranges": "destIpRanges",
        "dest_ports": "destPorts",
        "ip_protocols": "ipProtocols",
        "src_asns": "srcAsns",
        "src_ip_ranges": "srcIpRanges",
        "src_ports": "srcPorts",
        "src_region_codes": "srcRegionCodes",
        "user_defined_fields": "userDefinedFields",
    },
)
class ComputeRegionSecurityPolicyRuleNetworkMatch:
    def __init__(
        self,
        *,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_asns: typing.Optional[typing.Sequence[jsii.Number]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dest_ip_ranges: Destination IPv4/IPv6 addresses or CIDR prefixes, in standard text format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#dest_ip_ranges ComputeRegionSecurityPolicyRule#dest_ip_ranges}
        :param dest_ports: Destination port numbers for TCP/UDP/SCTP. Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#dest_ports ComputeRegionSecurityPolicyRule#dest_ports}
        :param ip_protocols: IPv4 protocol / IPv6 next header (after extension headers). Each element can be an 8-bit unsigned decimal number (e.g. "6"), range (e.g. "253-254"), or one of the following protocol names: "tcp", "udp", "icmp", "esp", "ah", "ipip", or "sctp". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#ip_protocols ComputeRegionSecurityPolicyRule#ip_protocols}
        :param src_asns: BGP Autonomous System Number associated with the source IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_asns ComputeRegionSecurityPolicyRule#src_asns}
        :param src_ip_ranges: Source IPv4/IPv6 addresses or CIDR prefixes, in standard text format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_ip_ranges ComputeRegionSecurityPolicyRule#src_ip_ranges}
        :param src_ports: Source port numbers for TCP/UDP/SCTP. Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_ports ComputeRegionSecurityPolicyRule#src_ports}
        :param src_region_codes: Two-letter ISO 3166-1 alpha-2 country code associated with the source IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_region_codes ComputeRegionSecurityPolicyRule#src_region_codes}
        :param user_defined_fields: user_defined_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#user_defined_fields ComputeRegionSecurityPolicyRule#user_defined_fields}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ba7e6c1a17bfd23540ae360b52d3917c7a0cb003385c83fecaf0018d075034)
            check_type(argname="argument dest_ip_ranges", value=dest_ip_ranges, expected_type=type_hints["dest_ip_ranges"])
            check_type(argname="argument dest_ports", value=dest_ports, expected_type=type_hints["dest_ports"])
            check_type(argname="argument ip_protocols", value=ip_protocols, expected_type=type_hints["ip_protocols"])
            check_type(argname="argument src_asns", value=src_asns, expected_type=type_hints["src_asns"])
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
            check_type(argname="argument src_ports", value=src_ports, expected_type=type_hints["src_ports"])
            check_type(argname="argument src_region_codes", value=src_region_codes, expected_type=type_hints["src_region_codes"])
            check_type(argname="argument user_defined_fields", value=user_defined_fields, expected_type=type_hints["user_defined_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dest_ip_ranges is not None:
            self._values["dest_ip_ranges"] = dest_ip_ranges
        if dest_ports is not None:
            self._values["dest_ports"] = dest_ports
        if ip_protocols is not None:
            self._values["ip_protocols"] = ip_protocols
        if src_asns is not None:
            self._values["src_asns"] = src_asns
        if src_ip_ranges is not None:
            self._values["src_ip_ranges"] = src_ip_ranges
        if src_ports is not None:
            self._values["src_ports"] = src_ports
        if src_region_codes is not None:
            self._values["src_region_codes"] = src_region_codes
        if user_defined_fields is not None:
            self._values["user_defined_fields"] = user_defined_fields

    @builtins.property
    def dest_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Destination IPv4/IPv6 addresses or CIDR prefixes, in standard text format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#dest_ip_ranges ComputeRegionSecurityPolicyRule#dest_ip_ranges}
        '''
        result = self._values.get("dest_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Destination port numbers for TCP/UDP/SCTP.

        Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#dest_ports ComputeRegionSecurityPolicyRule#dest_ports}
        '''
        result = self._values.get("dest_ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IPv4 protocol / IPv6 next header (after extension headers).

        Each element can be an 8-bit unsigned decimal number (e.g. "6"), range (e.g. "253-254"), or one of the following protocol names: "tcp", "udp", "icmp", "esp", "ah", "ipip", or "sctp".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#ip_protocols ComputeRegionSecurityPolicyRule#ip_protocols}
        '''
        result = self._values.get("ip_protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_asns(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''BGP Autonomous System Number associated with the source IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_asns ComputeRegionSecurityPolicyRule#src_asns}
        '''
        result = self._values.get("src_asns")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Source IPv4/IPv6 addresses or CIDR prefixes, in standard text format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_ip_ranges ComputeRegionSecurityPolicyRule#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Source port numbers for TCP/UDP/SCTP.

        Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_ports ComputeRegionSecurityPolicyRule#src_ports}
        '''
        result = self._values.get("src_ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Two-letter ISO 3166-1 alpha-2 country code associated with the source IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#src_region_codes ComputeRegionSecurityPolicyRule#src_region_codes}
        '''
        result = self._values.get("src_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_defined_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields"]]]:
        '''user_defined_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#user_defined_fields ComputeRegionSecurityPolicyRule#user_defined_fields}
        '''
        result = self._values.get("user_defined_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleNetworkMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRuleNetworkMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleNetworkMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5464a0dc3a4f61676401ff162ba4ca964dea36045be7ea7302bba2f4533ab294)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putUserDefinedFields")
    def put_user_defined_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9acec81397e3893e252cb4f416e939c7fd9d6acbbdce7181e780488f9705617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUserDefinedFields", [value]))

    @jsii.member(jsii_name="resetDestIpRanges")
    def reset_dest_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestIpRanges", []))

    @jsii.member(jsii_name="resetDestPorts")
    def reset_dest_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestPorts", []))

    @jsii.member(jsii_name="resetIpProtocols")
    def reset_ip_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpProtocols", []))

    @jsii.member(jsii_name="resetSrcAsns")
    def reset_src_asns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcAsns", []))

    @jsii.member(jsii_name="resetSrcIpRanges")
    def reset_src_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcIpRanges", []))

    @jsii.member(jsii_name="resetSrcPorts")
    def reset_src_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcPorts", []))

    @jsii.member(jsii_name="resetSrcRegionCodes")
    def reset_src_region_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcRegionCodes", []))

    @jsii.member(jsii_name="resetUserDefinedFields")
    def reset_user_defined_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefinedFields", []))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFields")
    def user_defined_fields(
        self,
    ) -> "ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsList":
        return typing.cast("ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsList", jsii.get(self, "userDefinedFields"))

    @builtins.property
    @jsii.member(jsii_name="destIpRangesInput")
    def dest_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="destPortsInput")
    def dest_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolsInput")
    def ip_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcAsnsInput")
    def src_asns_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "srcAsnsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcIpRangesInput")
    def src_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="srcPortsInput")
    def src_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodesInput")
    def src_region_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcRegionCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFieldsInput")
    def user_defined_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields"]]], jsii.get(self, "userDefinedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="destIpRanges")
    def dest_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destIpRanges"))

    @dest_ip_ranges.setter
    def dest_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ec6df5e1039a4b894507b2956340d2daa849dc337b274ef40e35dc9c0fc292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destPorts")
    def dest_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destPorts"))

    @dest_ports.setter
    def dest_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ea444c829d3fe2ae769557e968a6d6f5f52bdd8396703bb59d3ad618128913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocols")
    def ip_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipProtocols"))

    @ip_protocols.setter
    def ip_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b883e046ba4b0baf0a10f8fcb1df88ad1c080d1e364bfbbc1664dfa59d2d815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcAsns")
    def src_asns(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "srcAsns"))

    @src_asns.setter
    def src_asns(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55696cd7f16cb43ea445b33105d9b02e836ba276d6d7797117c45f340363353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcAsns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @src_ip_ranges.setter
    def src_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8e18c9f36177cdabe4512925eeaa2f28fecda8a30a140f8badb74cd703683d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcPorts")
    def src_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcPorts"))

    @src_ports.setter
    def src_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b461673c5a9fe183dc1881b762a603924529a721476157808569c9be71fef7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodes")
    def src_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcRegionCodes"))

    @src_region_codes.setter
    def src_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf15a2b078980eef588d8a7269830f101c8f3e157b1d0dfbb6ced1d32f641ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRuleNetworkMatch]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleNetworkMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRuleNetworkMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69aa13123edbf749bd7290e9656d9985082aab32857e00c5ec7ddf64ea477f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Name of the user-defined field, as given in the definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#name ComputeRegionSecurityPolicyRule#name}
        :param values: Matching values of the field. Each element can be a 32-bit unsigned decimal or hexadecimal (starting with "0x") number (e.g. "64") or range (e.g. "0x400-0x7ff"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#values ComputeRegionSecurityPolicyRule#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb53e2e5559f5823d2b8ff1ce1bb8ed0915204d7c18f0920491f48a8dec87692)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the user-defined field, as given in the definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#name ComputeRegionSecurityPolicyRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Matching values of the field.

        Each element can be a 32-bit unsigned decimal or hexadecimal (starting with "0x") number (e.g. "64") or range (e.g. "0x400-0x7ff").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#values ComputeRegionSecurityPolicyRule#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e4f78f44e8ec5161af1d64ac81831abd5011cdb1542c023688a9d695cf0d68a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581602eccbf86bfae41fc9f5fe988b5ce2963c28effc597a9c234c0be3067882)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b5fa1c2faabdabecc98e68b1229a45658e6e8dcabaf0e61c20029d88cf64e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b5b7636b6440eba1e42fec7916f4587c5e33d294172c4b9aed0142ace29eacb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c97ec0ce41b895ce20876635cb4a702b64c719388dea9d57b8dd304fd7d234a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec85abe57101eeed4228257ad2518f3a90f8f45353d93c556bdb7aca2b1bf439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8b35286585b97501297b7db80720362ee1bc799b9f1f9c432a61334e84de10e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc5dd506c9380f449252d94fb4a5efd66c0a680160549ffb1e5ae7f9d3fb57c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2d41b9e9261dcd17065b64a995cb06e4f575bc1dff2058b7da47538d18a773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32fb270e4b660a9018f969eaa4fafe6d29b102dc5507b277de7cee22187ba02f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfig",
    jsii_struct_bases=[],
    name_mapping={"exclusion": "exclusion"},
)
class ComputeRegionSecurityPolicyRulePreconfiguredWafConfig:
    def __init__(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#exclusion ComputeRegionSecurityPolicyRule#exclusion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021feebc0c49c2ee424ba11f158cdb2c845ea882fdf97a47d84d071ca3047d92)
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusion is not None:
            self._values["exclusion"] = exclusion

    @builtins.property
    def exclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion"]]]:
        '''exclusion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#exclusion ComputeRegionSecurityPolicyRule#exclusion}
        '''
        result = self._values.get("exclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulePreconfiguredWafConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion",
    jsii_struct_bases=[],
    name_mapping={
        "target_rule_set": "targetRuleSet",
        "request_cookie": "requestCookie",
        "request_header": "requestHeader",
        "request_query_param": "requestQueryParam",
        "request_uri": "requestUri",
        "target_rule_ids": "targetRuleIds",
    },
)
class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion:
    def __init__(
        self,
        *,
        target_rule_set: builtins.str,
        request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param target_rule_set: Target WAF rule set to apply the preconfigured WAF exclusion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#target_rule_set ComputeRegionSecurityPolicyRule#target_rule_set}
        :param request_cookie: request_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#request_cookie ComputeRegionSecurityPolicyRule#request_cookie}
        :param request_header: request_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#request_header ComputeRegionSecurityPolicyRule#request_header}
        :param request_query_param: request_query_param block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#request_query_param ComputeRegionSecurityPolicyRule#request_query_param}
        :param request_uri: request_uri block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#request_uri ComputeRegionSecurityPolicyRule#request_uri}
        :param target_rule_ids: A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion. If omitted, it refers to all the rule IDs under the WAF rule set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#target_rule_ids ComputeRegionSecurityPolicyRule#target_rule_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ba7fabe2f7c8aa0a4ff4c66cc5fff8c5e1bba3b787a03c700edf2270235666)
            check_type(argname="argument target_rule_set", value=target_rule_set, expected_type=type_hints["target_rule_set"])
            check_type(argname="argument request_cookie", value=request_cookie, expected_type=type_hints["request_cookie"])
            check_type(argname="argument request_header", value=request_header, expected_type=type_hints["request_header"])
            check_type(argname="argument request_query_param", value=request_query_param, expected_type=type_hints["request_query_param"])
            check_type(argname="argument request_uri", value=request_uri, expected_type=type_hints["request_uri"])
            check_type(argname="argument target_rule_ids", value=target_rule_ids, expected_type=type_hints["target_rule_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_rule_set": target_rule_set,
        }
        if request_cookie is not None:
            self._values["request_cookie"] = request_cookie
        if request_header is not None:
            self._values["request_header"] = request_header
        if request_query_param is not None:
            self._values["request_query_param"] = request_query_param
        if request_uri is not None:
            self._values["request_uri"] = request_uri
        if target_rule_ids is not None:
            self._values["target_rule_ids"] = target_rule_ids

    @builtins.property
    def target_rule_set(self) -> builtins.str:
        '''Target WAF rule set to apply the preconfigured WAF exclusion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#target_rule_set ComputeRegionSecurityPolicyRule#target_rule_set}
        '''
        result = self._values.get("target_rule_set")
        assert result is not None, "Required property 'target_rule_set' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_cookie(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]]:
        '''request_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#request_cookie ComputeRegionSecurityPolicyRule#request_cookie}
        '''
        result = self._values.get("request_cookie")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]], result)

    @builtins.property
    def request_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]]:
        '''request_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#request_header ComputeRegionSecurityPolicyRule#request_header}
        '''
        result = self._values.get("request_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]], result)

    @builtins.property
    def request_query_param(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]]:
        '''request_query_param block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#request_query_param ComputeRegionSecurityPolicyRule#request_query_param}
        '''
        result = self._values.get("request_query_param")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]], result)

    @builtins.property
    def request_uri(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]]:
        '''request_uri block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#request_uri ComputeRegionSecurityPolicyRule#request_uri}
        '''
        result = self._values.get("request_uri")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]], result)

    @builtins.property
    def target_rule_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion.

        If omitted, it refers to all the rule IDs under the WAF rule set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#target_rule_ids ComputeRegionSecurityPolicyRule#target_rule_ids}
        '''
        result = self._values.get("target_rule_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16f91d868661678ecc6f625cb942ec299d33d81a0698ba64ec65a09205b14f47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01bfbe62fecf1510b0e396f9a7ba465fab850ed2a4ffabf70188d6061d9686bd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700849e1dbb73f0fdf4d65cfa00d31c6165acc9a035bb9fd33ead92ca79fec14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d34feee52563464e6a2f8a460173ff493c4f7d10e48a81c909063ab10c7e97ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5094fc5c4aba6befc0794598e54a170ce0c9be79c4734b668eab8caaf22ff3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ccb6a2479833bbda4e3fc6d1aeca5e8025d01bb1d133cba9f152d74d259b194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e99a4b6ff36a416c865c76efae22a3f18cab24ccedc3b537a41d495da7583029)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRequestCookie")
    def put_request_cookie(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97553f88480401b392d458805d333955acd083a38a88658ed18db5376a3a6145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestCookie", [value]))

    @jsii.member(jsii_name="putRequestHeader")
    def put_request_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2b0941125440e2fffc8561b90c34ef471f451766146ccd66b5b1e16f4ae376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeader", [value]))

    @jsii.member(jsii_name="putRequestQueryParam")
    def put_request_query_param(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429f2520df738763fcb58ea6439a9f2a32e6ef391a7eeb2bfc5a11318bcc280f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestQueryParam", [value]))

    @jsii.member(jsii_name="putRequestUri")
    def put_request_uri(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e88a0e2dc7672ae6cdc9525f037eac83f4aa3a356371fe6225f439d615b840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestUri", [value]))

    @jsii.member(jsii_name="resetRequestCookie")
    def reset_request_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestCookie", []))

    @jsii.member(jsii_name="resetRequestHeader")
    def reset_request_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeader", []))

    @jsii.member(jsii_name="resetRequestQueryParam")
    def reset_request_query_param(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestQueryParam", []))

    @jsii.member(jsii_name="resetRequestUri")
    def reset_request_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestUri", []))

    @jsii.member(jsii_name="resetTargetRuleIds")
    def reset_target_rule_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetRuleIds", []))

    @builtins.property
    @jsii.member(jsii_name="requestCookie")
    def request_cookie(
        self,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList":
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList", jsii.get(self, "requestCookie"))

    @builtins.property
    @jsii.member(jsii_name="requestHeader")
    def request_header(
        self,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList":
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList", jsii.get(self, "requestHeader"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParam")
    def request_query_param(
        self,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList":
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList", jsii.get(self, "requestQueryParam"))

    @builtins.property
    @jsii.member(jsii_name="requestUri")
    def request_uri(
        self,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList":
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList", jsii.get(self, "requestUri"))

    @builtins.property
    @jsii.member(jsii_name="requestCookieInput")
    def request_cookie_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]], jsii.get(self, "requestCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderInput")
    def request_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]], jsii.get(self, "requestHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParamInput")
    def request_query_param_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]], jsii.get(self, "requestQueryParamInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriInput")
    def request_uri_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]], jsii.get(self, "requestUriInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRuleIdsInput")
    def target_rule_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetRuleIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRuleSetInput")
    def target_rule_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRuleSetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRuleIds")
    def target_rule_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetRuleIds"))

    @target_rule_ids.setter
    def target_rule_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522399552c67ebb19ed0c3632f4e560fc242ccb8d6e5c4fb8e7ef888d50b8661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRuleSet")
    def target_rule_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRuleSet"))

    @target_rule_set.setter
    def target_rule_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938e0523f77f981ef5551d8ecc0da98ef47993afd8cde9a915f9d424e7968622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91be5e7fa383ff8a2f707619c6ea4bb95be0170ba7eda7846b9e43774578b97e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#operator ComputeRegionSecurityPolicyRule#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#value ComputeRegionSecurityPolicyRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1e114d59f647477c8de19c538d13d15c2e6a67f9c3825972dacf2cd39558f8)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def operator(self) -> builtins.str:
        '''You can specify an exact match or a partial match by using a field operator and a field value.

        Available options:
        EQUALS: The operator matches if the field value equals the specified value.
        STARTS_WITH: The operator matches if the field value starts with the specified value.
        ENDS_WITH: The operator matches if the field value ends with the specified value.
        CONTAINS: The operator matches if the field value contains the specified value.
        EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#operator ComputeRegionSecurityPolicyRule#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#value ComputeRegionSecurityPolicyRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5bc795918a190275f8584b0733a4a8834065147d81a077ea62d0d8ba07eb09d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28aac98dd2e2e16a9ebea077a251b8f574464a7f70e98e4ee33a1332fe28bff8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a26a6dcdc06355f6cd0b72365fdf44d8741ddd0ae4376dc30882949c9aaf755)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f79749328cef71f15dccc078b4c01551c7341e7a0de379bb50ee7d3e8818c33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2c0b6c87154effa066ed69abaa5d483bac2cd494deb4cf11f0d91174e734816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bda2aea34ae17a94396bc09039a435dec67a963218bf9a193aab8a9549773b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57cc4ea459e6f55cbfb67cc0c7cacd6d6280169a9f4c8983c2399e828b1218ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9adf3ff86b1f154fa4240c6c4b743d34eed8ed67147533096d875970ac3f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7110553ea6df8776eb688ae94e1d631cac113f1b1502d3e324568e8c81cd6146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a021d455fca1db71647c948cee4e1f9ec664005c9a7fb4aa5d4b1f8cb97632f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#operator ComputeRegionSecurityPolicyRule#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#value ComputeRegionSecurityPolicyRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba52e13acc1df4c7664f42b5efb86ca0d108ffd00cd14506f5e88aff2bd3f75)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def operator(self) -> builtins.str:
        '''You can specify an exact match or a partial match by using a field operator and a field value.

        Available options:
        EQUALS: The operator matches if the field value equals the specified value.
        STARTS_WITH: The operator matches if the field value starts with the specified value.
        ENDS_WITH: The operator matches if the field value ends with the specified value.
        CONTAINS: The operator matches if the field value contains the specified value.
        EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#operator ComputeRegionSecurityPolicyRule#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#value ComputeRegionSecurityPolicyRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e450b4279636959e2146e44d6018d26ae53ff077de3c329d04c7d0a862add21f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c64d15c727468db2965011c68c6872b75472fd6f0b846d555d34c3db1e2fd20)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6affd07cc1c67e3938e2cf46596fbda39275ed44e2e5286e5f26feda398cc7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23ddf78110e7edffd2ca3cd81638ef3300bd81185eb1880f6088bef78c4c5594)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c24615150592dec5e30d12c15c20673b02c18c99e13f48d6afe70176fd644d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20d05b80a48c3608056bd9aba19ad260c9c9192a24403c44d1c8e8657810f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3f9ebab0331e3c23aca8618697eb59d8273e0c76687c8a882a216b0cbbe511e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614e6478e094abbd2f527528ad7866cb4cded7cbb22fcc13ee32bfcddea0ac44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bc3d98b0918e3fd23bb73bb9541170fc70fbe2505cb265cf596d4520746094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015de449e4995549b7cf2362bbb96d672786a2e7f843ab9b117781db8b810b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#operator ComputeRegionSecurityPolicyRule#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#value ComputeRegionSecurityPolicyRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f49373d24ad38d7df31d7966c9f4bdb226212573eda4890c51c7e7db1d6a6cf)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def operator(self) -> builtins.str:
        '''You can specify an exact match or a partial match by using a field operator and a field value.

        Available options:
        EQUALS: The operator matches if the field value equals the specified value.
        STARTS_WITH: The operator matches if the field value starts with the specified value.
        ENDS_WITH: The operator matches if the field value ends with the specified value.
        CONTAINS: The operator matches if the field value contains the specified value.
        EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#operator ComputeRegionSecurityPolicyRule#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#value ComputeRegionSecurityPolicyRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f66213305033f982c0bd55be2e67c7b8e08313c6cc7dc0b597be953d2758cce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e307c5fac44cf1752c85b13edf5a13d8e08aa4381d75b33ef6c5d2a79907ec24)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8065030b2d589b11ff233c727a0cc524f857de869ba5dcad5a66dea7d90fc19c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e94a8c30a0482c0feb4c1db19e00a2838acb36be2ac932c665b69d2ac4a3314f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e83be0406299c3a426691f85095ea9f80268f7cd6a732c7a75cfc4867fddb5bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0432377735bac802e996e4b3ae37a4f08ad5d9469e62aed9012997916f7aaea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__766a084d7a4cd3fc5dc5b054526cbc51e93766d6d5e8fa3e99cbb59a30990011)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7c518b001c13d34c58fcdfbbd42297edd934c0ef1bcf32a5b9c47c25241d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb8da28dd0d09bee5fc96211d4592ac58443dd5ecf67ea8bd463bb48087e544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f96ebae1eddbda7f70f66a9bbb60cc96f3a8e3200107e1cf641438b671a031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#operator ComputeRegionSecurityPolicyRule#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#value ComputeRegionSecurityPolicyRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446500db0fbd5dae58cd7c0ad5820a4c51f63981ef2738c78929943f8ac1348d)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def operator(self) -> builtins.str:
        '''You can specify an exact match or a partial match by using a field operator and a field value.

        Available options:
        EQUALS: The operator matches if the field value equals the specified value.
        STARTS_WITH: The operator matches if the field value starts with the specified value.
        ENDS_WITH: The operator matches if the field value ends with the specified value.
        CONTAINS: The operator matches if the field value contains the specified value.
        EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#operator ComputeRegionSecurityPolicyRule#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#value ComputeRegionSecurityPolicyRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b377ed040b0698327f98403a0949b734407483071b1778c9f69c10054afdb81b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913968e83473973827acf849704bcf2147fcd45fb9a7bae4d349a7d115af1774)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1808638e65822e900c73f2620187edf75ac33aded4f78c9336d99204d5c049db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f012c179f46504a8d6a308c62eca064850b05335fcc8170051baf5e6173a860)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1583884370306e227a50f5cffded0bde4b1bf36fde3f8ea5b5e7275294a18c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ac4af61ba1d44b5a271e1c0f16848514c78aca5824c0501980b1f896e84ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac39a87a3e35cdc318a0e7057a5089d174cfd0a8f43d05ec0c06d0fb383e74c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d934583e255b4491b6be62a9b87e25656eab96066539aafd65fbd0219aba7616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afaaea7f3c70b9534bc16c00cc05aba48504aeba0de1ea5200e4cb32ccbaaa23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5f3d03cbf88c398ca05da540956fc8a4469b5c56f715c4f6480895f8f6efc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulePreconfiguredWafConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRulePreconfiguredWafConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6693d2b1e381af4e16018bbdf44dcfa76616bf37042233370c81be5ae92f42bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusion")
    def put_exclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7df7fbd7ca0dd082878a065433a30b8e6343d8bea8621c0c6754a323fcf0f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusion", [value]))

    @jsii.member(jsii_name="resetExclusion")
    def reset_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusion", []))

    @builtins.property
    @jsii.member(jsii_name="exclusion")
    def exclusion(
        self,
    ) -> ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionList:
        return typing.cast(ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionList, jsii.get(self, "exclusion"))

    @builtins.property
    @jsii.member(jsii_name="exclusionInput")
    def exclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]]], jsii.get(self, "exclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulePreconfiguredWafConfig]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulePreconfiguredWafConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRulePreconfiguredWafConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e1004357d512381e626bc081b388eafa153e4712b5aa0e500928a439ee01b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleRateLimitOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ban_duration_sec": "banDurationSec",
        "ban_threshold": "banThreshold",
        "conform_action": "conformAction",
        "enforce_on_key": "enforceOnKey",
        "enforce_on_key_configs": "enforceOnKeyConfigs",
        "enforce_on_key_name": "enforceOnKeyName",
        "exceed_action": "exceedAction",
        "rate_limit_threshold": "rateLimitThreshold",
    },
)
class ComputeRegionSecurityPolicyRuleRateLimitOptions:
    def __init__(
        self,
        *,
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        conform_action: typing.Optional[builtins.str] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_action: typing.Optional[builtins.str] = None,
        rate_limit_threshold: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#ban_duration_sec ComputeRegionSecurityPolicyRule#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#ban_threshold ComputeRegionSecurityPolicyRule#ban_threshold}
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#conform_action ComputeRegionSecurityPolicyRule#conform_action}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key ComputeRegionSecurityPolicyRule#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_configs ComputeRegionSecurityPolicyRule#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_name ComputeRegionSecurityPolicyRule#enforce_on_key_name}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to deny with a specified HTTP response code. Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#exceed_action ComputeRegionSecurityPolicyRule#exceed_action}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#rate_limit_threshold ComputeRegionSecurityPolicyRule#rate_limit_threshold}
        '''
        if isinstance(ban_threshold, dict):
            ban_threshold = ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold(**ban_threshold)
        if isinstance(rate_limit_threshold, dict):
            rate_limit_threshold = ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold(**rate_limit_threshold)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a6f47230258ae381e30d0e3baa6267889e636c7bddaa5fea0908718122b01b)
            check_type(argname="argument ban_duration_sec", value=ban_duration_sec, expected_type=type_hints["ban_duration_sec"])
            check_type(argname="argument ban_threshold", value=ban_threshold, expected_type=type_hints["ban_threshold"])
            check_type(argname="argument conform_action", value=conform_action, expected_type=type_hints["conform_action"])
            check_type(argname="argument enforce_on_key", value=enforce_on_key, expected_type=type_hints["enforce_on_key"])
            check_type(argname="argument enforce_on_key_configs", value=enforce_on_key_configs, expected_type=type_hints["enforce_on_key_configs"])
            check_type(argname="argument enforce_on_key_name", value=enforce_on_key_name, expected_type=type_hints["enforce_on_key_name"])
            check_type(argname="argument exceed_action", value=exceed_action, expected_type=type_hints["exceed_action"])
            check_type(argname="argument rate_limit_threshold", value=rate_limit_threshold, expected_type=type_hints["rate_limit_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ban_duration_sec is not None:
            self._values["ban_duration_sec"] = ban_duration_sec
        if ban_threshold is not None:
            self._values["ban_threshold"] = ban_threshold
        if conform_action is not None:
            self._values["conform_action"] = conform_action
        if enforce_on_key is not None:
            self._values["enforce_on_key"] = enforce_on_key
        if enforce_on_key_configs is not None:
            self._values["enforce_on_key_configs"] = enforce_on_key_configs
        if enforce_on_key_name is not None:
            self._values["enforce_on_key_name"] = enforce_on_key_name
        if exceed_action is not None:
            self._values["exceed_action"] = exceed_action
        if rate_limit_threshold is not None:
            self._values["rate_limit_threshold"] = rate_limit_threshold

    @builtins.property
    def ban_duration_sec(self) -> typing.Optional[jsii.Number]:
        '''Can only be specified if the action for the rule is "rate_based_ban".

        If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#ban_duration_sec ComputeRegionSecurityPolicyRule#ban_duration_sec}
        '''
        result = self._values.get("ban_duration_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ban_threshold(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold"]:
        '''ban_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#ban_threshold ComputeRegionSecurityPolicyRule#ban_threshold}
        '''
        result = self._values.get("ban_threshold")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold"], result)

    @builtins.property
    def conform_action(self) -> typing.Optional[builtins.str]:
        '''Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#conform_action ComputeRegionSecurityPolicyRule#conform_action}
        '''
        result = self._values.get("conform_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key(self) -> typing.Optional[builtins.str]:
        '''Determines the key to enforce the rateLimitThreshold on.

        Possible values are:

        - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured.
        - IP: The source IP address of the request is the key. Each IP has this limit enforced separately.
        - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL.
        - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP.
        - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL.
        - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes.
        - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session.
        - REGION_CODE: The country/region from which the request originates.
        - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL.
        - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL.
        - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key ComputeRegionSecurityPolicyRule#enforce_on_key}
        '''
        result = self._values.get("enforce_on_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs"]]]:
        '''enforce_on_key_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_configs ComputeRegionSecurityPolicyRule#enforce_on_key_configs}
        '''
        result = self._values.get("enforce_on_key_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs"]]], result)

    @builtins.property
    def enforce_on_key_name(self) -> typing.Optional[builtins.str]:
        '''Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value.

        HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_name ComputeRegionSecurityPolicyRule#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exceed_action(self) -> typing.Optional[builtins.str]:
        '''Action to take for requests that are above the configured rate limit threshold, to deny with a specified HTTP response code.

        Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#exceed_action ComputeRegionSecurityPolicyRule#exceed_action}
        '''
        result = self._values.get("exceed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limit_threshold(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold"]:
        '''rate_limit_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#rate_limit_threshold ComputeRegionSecurityPolicyRule#rate_limit_threshold}
        '''
        result = self._values.get("rate_limit_threshold")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleRateLimitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#count ComputeRegionSecurityPolicyRule#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#interval_sec ComputeRegionSecurityPolicyRule#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206b60357996820ea0cd36c9b4239a3c7f3e162c0b55e6e1429826a4ce45a9ee)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval_sec", value=interval_sec, expected_type=type_hints["interval_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval_sec is not None:
            self._values["interval_sec"] = interval_sec

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Number of HTTP(S) requests for calculating the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#count ComputeRegionSecurityPolicyRule#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_sec(self) -> typing.Optional[jsii.Number]:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#interval_sec ComputeRegionSecurityPolicyRule#interval_sec}
        '''
        result = self._values.get("interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9420b08794541fa20911d2cd7e0c9237d6d6331adba8d81cd502723e3ea60273)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetIntervalSec")
    def reset_interval_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSec", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecInput")
    def interval_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187cb2b3ad732de2d38062ec82bbe07f92aa7d02bd201cd2b59491be0fa6112d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a55bb262db765ff43b92ad4f8adce09845fe3b2b900cc0e30733f6df459500d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41f85d8940afab7a705cdbfdd043ddd5aca018c4cedea3ac47079a58670edfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "enforce_on_key_name": "enforceOnKeyName",
        "enforce_on_key_type": "enforceOnKeyType",
    },
)
class ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs:
    def __init__(
        self,
        *,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        enforce_on_key_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_name ComputeRegionSecurityPolicyRule#enforce_on_key_name}
        :param enforce_on_key_type: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKeyConfigs" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_type ComputeRegionSecurityPolicyRule#enforce_on_key_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3bd3702c7b0ed9bbfc1f89b8174f8285d6477580c55af37757d03612f81ac04)
            check_type(argname="argument enforce_on_key_name", value=enforce_on_key_name, expected_type=type_hints["enforce_on_key_name"])
            check_type(argname="argument enforce_on_key_type", value=enforce_on_key_type, expected_type=type_hints["enforce_on_key_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enforce_on_key_name is not None:
            self._values["enforce_on_key_name"] = enforce_on_key_name
        if enforce_on_key_type is not None:
            self._values["enforce_on_key_type"] = enforce_on_key_type

    @builtins.property
    def enforce_on_key_name(self) -> typing.Optional[builtins.str]:
        '''Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value.

        HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_name ComputeRegionSecurityPolicyRule#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_type(self) -> typing.Optional[builtins.str]:
        '''Determines the key to enforce the rateLimitThreshold on.

        Possible values are:

        - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKeyConfigs" is not configured.
        - IP: The source IP address of the request is the key. Each IP has this limit enforced separately.
        - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL.
        - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP.
        - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL.
        - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes.
        - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session.
        - REGION_CODE: The country/region from which the request originates.
        - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL.
        - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL.
        - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#enforce_on_key_type ComputeRegionSecurityPolicyRule#enforce_on_key_type}
        '''
        result = self._values.get("enforce_on_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__573bc21c0790ae15ced9c6475ea0f42b5292c04a1df3a7966bdd6a12dd4bc595)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2a53ad18a1d91c1ade3083680076aafd53e577669aa39c3ba5e942edc521bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__326d2f2a4550004c2b0abda23705f3f5c480b62fb63ea951fb3503f1f3e028f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f36414746b63c24d80fb3e268d838d0370931a98665c8f890593d0730304599)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61ed7c370fdddbb025818c1ebb306750dfab25e97e32f1ba0cac3b34be8a8c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7344ec0f6a7d547b65046837ddeb823c624f215064d7956c4ee950a4a1692377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__723ca41e4003150bf17377f25500a95cdc4735b9f3182e1158faf5d2a8bee525)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnforceOnKeyName")
    def reset_enforce_on_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyName", []))

    @jsii.member(jsii_name="resetEnforceOnKeyType")
    def reset_enforce_on_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyType", []))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyNameInput")
    def enforce_on_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceOnKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyTypeInput")
    def enforce_on_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceOnKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyName")
    def enforce_on_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyName"))

    @enforce_on_key_name.setter
    def enforce_on_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c442533b6e892727e80c4f956972399fd1d36ae9cca430f22012439cbc1ef7d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyType")
    def enforce_on_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyType"))

    @enforce_on_key_type.setter
    def enforce_on_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d1ee1afd9172d581943a29e425392518d2a864adc7bae56c2bd1e9003949db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9eb9d57351b1e1f056ad85480c7f380bec719ccf3afb115d0e0d6393ba0421a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRuleRateLimitOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleRateLimitOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f6693aea83f7385a2accf0f0c55da22a2f4892998fd776cb54b78245980cbf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBanThreshold")
    def put_ban_threshold(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#count ComputeRegionSecurityPolicyRule#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#interval_sec ComputeRegionSecurityPolicyRule#interval_sec}
        '''
        value = ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold(
            count=count, interval_sec=interval_sec
        )

        return typing.cast(None, jsii.invoke(self, "putBanThreshold", [value]))

    @jsii.member(jsii_name="putEnforceOnKeyConfigs")
    def put_enforce_on_key_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953dacdd635080b7f586ce686ebe98e4e61eb2ffe2d8bd8cef82ccccd0d2a6c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnforceOnKeyConfigs", [value]))

    @jsii.member(jsii_name="putRateLimitThreshold")
    def put_rate_limit_threshold(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#count ComputeRegionSecurityPolicyRule#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#interval_sec ComputeRegionSecurityPolicyRule#interval_sec}
        '''
        value = ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold(
            count=count, interval_sec=interval_sec
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimitThreshold", [value]))

    @jsii.member(jsii_name="resetBanDurationSec")
    def reset_ban_duration_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBanDurationSec", []))

    @jsii.member(jsii_name="resetBanThreshold")
    def reset_ban_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBanThreshold", []))

    @jsii.member(jsii_name="resetConformAction")
    def reset_conform_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConformAction", []))

    @jsii.member(jsii_name="resetEnforceOnKey")
    def reset_enforce_on_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKey", []))

    @jsii.member(jsii_name="resetEnforceOnKeyConfigs")
    def reset_enforce_on_key_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyConfigs", []))

    @jsii.member(jsii_name="resetEnforceOnKeyName")
    def reset_enforce_on_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyName", []))

    @jsii.member(jsii_name="resetExceedAction")
    def reset_exceed_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExceedAction", []))

    @jsii.member(jsii_name="resetRateLimitThreshold")
    def reset_rate_limit_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimitThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="banThreshold")
    def ban_threshold(
        self,
    ) -> ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference:
        return typing.cast(ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference, jsii.get(self, "banThreshold"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigs")
    def enforce_on_key_configs(
        self,
    ) -> ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList:
        return typing.cast(ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList, jsii.get(self, "enforceOnKeyConfigs"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThreshold")
    def rate_limit_threshold(
        self,
    ) -> "ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference", jsii.get(self, "rateLimitThreshold"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSecInput")
    def ban_duration_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "banDurationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="banThresholdInput")
    def ban_threshold_input(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold], jsii.get(self, "banThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="conformActionInput")
    def conform_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conformActionInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigsInput")
    def enforce_on_key_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]], jsii.get(self, "enforceOnKeyConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyInput")
    def enforce_on_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceOnKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyNameInput")
    def enforce_on_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceOnKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exceedActionInput")
    def exceed_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exceedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThresholdInput")
    def rate_limit_threshold_input(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold"]:
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold"], jsii.get(self, "rateLimitThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSec")
    def ban_duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "banDurationSec"))

    @ban_duration_sec.setter
    def ban_duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bd3142c1dda06065e3d5fd5ed8a5c7d6e3227200d1cd13869ebfa5760cecba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "banDurationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conformAction")
    def conform_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conformAction"))

    @conform_action.setter
    def conform_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c786f18fb2bc19fa84b4e7848fc77879b4676b8e1980f2ea3a37049eb114d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conformAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKey")
    def enforce_on_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKey"))

    @enforce_on_key.setter
    def enforce_on_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65457886411a7758ec7cf9c2ebd2da08f58f24a0bdb9534377a8f82f8a307a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyName")
    def enforce_on_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyName"))

    @enforce_on_key_name.setter
    def enforce_on_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f330b5f2d4d5802e4089facba192a6e39767f8b110206733431b79843ff37442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exceedAction")
    def exceed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exceedAction"))

    @exceed_action.setter
    def exceed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c50aa77f3fc6bc4c9b7270f5edbea21f3291b08701dc35452489befc6ca314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exceedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptions]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c570a02ae4bac6889e60590a81d36be91cd5b47310ebd7a35639fb829f491207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#count ComputeRegionSecurityPolicyRule#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#interval_sec ComputeRegionSecurityPolicyRule#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a3f9e19e5122041c372b1b1d659cd0c5641a613164b584a5fd03bed0e5fa50)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval_sec", value=interval_sec, expected_type=type_hints["interval_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval_sec is not None:
            self._values["interval_sec"] = interval_sec

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Number of HTTP(S) requests for calculating the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#count ComputeRegionSecurityPolicyRule#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_sec(self) -> typing.Optional[jsii.Number]:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#interval_sec ComputeRegionSecurityPolicyRule#interval_sec}
        '''
        result = self._values.get("interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4e59248db8d323cebe53416f49c164e7c6f907a51e72a72cb1659814beac2a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetIntervalSec")
    def reset_interval_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSec", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecInput")
    def interval_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ec9b827b3135ef0f2e982d57730e282eae7505abbd7d4f7f1c89fa1848914d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1428f97495cf2d36f0ad5da186cc005572432bfe040917bb079b32af7ff2b9e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e15fe31048b9f02f9d4a485d8a7db2885f5ad2747fdd0715f69fea781747f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionSecurityPolicyRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#create ComputeRegionSecurityPolicyRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#delete ComputeRegionSecurityPolicyRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#update ComputeRegionSecurityPolicyRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95a3b9c6e3887d6ce205bfe013ef7417d2a8584ee29c08f6397cc2e0291914d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#create ComputeRegionSecurityPolicyRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#delete ComputeRegionSecurityPolicyRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy_rule#update ComputeRegionSecurityPolicyRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicyRule.ComputeRegionSecurityPolicyRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__904c6d375ef011fca34cb231010ba77a371ed61edaed5902d3983cc172afb057)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc98908af6aa0abfe828ab17303a564efb230b8edfaf9ef48558e8d49f6f09dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5485ca35ccbd60d682fe7609a59d58af5b306c4459a32bcf97d8ff4d466da0e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fbb9d110d8601d72bda2aaa6d555feb7ca05c91248a65c1f08b66a2e0087ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db2309bc0c46f43c412032a5e624831cee12c74b07e87c6d208273513ed27976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionSecurityPolicyRule",
    "ComputeRegionSecurityPolicyRuleConfig",
    "ComputeRegionSecurityPolicyRuleMatch",
    "ComputeRegionSecurityPolicyRuleMatchConfig",
    "ComputeRegionSecurityPolicyRuleMatchConfigOutputReference",
    "ComputeRegionSecurityPolicyRuleMatchExpr",
    "ComputeRegionSecurityPolicyRuleMatchExprOutputReference",
    "ComputeRegionSecurityPolicyRuleMatchOutputReference",
    "ComputeRegionSecurityPolicyRuleNetworkMatch",
    "ComputeRegionSecurityPolicyRuleNetworkMatchOutputReference",
    "ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields",
    "ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsList",
    "ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFieldsOutputReference",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfig",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionList",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference",
    "ComputeRegionSecurityPolicyRulePreconfiguredWafConfigOutputReference",
    "ComputeRegionSecurityPolicyRuleRateLimitOptions",
    "ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold",
    "ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference",
    "ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs",
    "ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList",
    "ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference",
    "ComputeRegionSecurityPolicyRuleRateLimitOptionsOutputReference",
    "ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold",
    "ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference",
    "ComputeRegionSecurityPolicyRuleTimeouts",
    "ComputeRegionSecurityPolicyRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4df3c8ef98b083f131d1d6a36b958dc7c40a0c9b88067156522a2a7cf8c46b4b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    priority: jsii.Number,
    region: builtins.str,
    security_policy: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    network_match: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleNetworkMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    preconfigured_waf_config: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limit_options: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleRateLimitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6a24533a54c5399dd03845eb847dba23341099a20c34661dc84281f3cfb5425b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878d27c7b4dc4e0a6a4df8b6d514905602d1f3d5b8eb798a4e226e919cf35f4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f216d7688074fda651fc8d9c192ec02ab4a78eb3b5d392e7f28a981e62ffb84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614d5305fe00cf56b537f900e082d75ad597c970dd867fe7e871bf46569606dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afd45f0367e46d50ff195df832279e71e90ab838c1ebc9f9ab2c648d2606c48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67397b6a61208353ca0f2768a5c1d954a12e1b504c4d6ae0a0acf944ddd4e60(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7306d2346823cba4887ba93d9ceba23d2ee902e9cbad074943f36af56dbc46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879bc87702f7911c0d50177c0b7ef41b8194d7eb066077ba857655e55f560d15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d6ddc230edb70c6d3b82a1adbb2783a225fc81f1ad57e207184f98e8d62d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186da766d1fb58808cca052eb2470bd9ff41953c961ea67508a62122d743ee69(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    priority: jsii.Number,
    region: builtins.str,
    security_policy: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    network_match: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleNetworkMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    preconfigured_waf_config: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limit_options: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleRateLimitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701aaba32c96bbfaf7cccffb28e66603f46267052a6ef2b8dfdbc1409a343f8d(
    *,
    config: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleMatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    expr: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleMatchExpr, typing.Dict[builtins.str, typing.Any]]] = None,
    versioned_expr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b399797566fc0aa096c9e6a83c4748697751f2841285fad3f214b27e24ea718d(
    *,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493c77714054e8d6b2e9d74869a576cd368f2d380a0c6cedd95ab2c6e508abf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc23092b663a203d55685e9e7458432a041fe79122931e5b4b8da6e5ffcc2949(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb03d5ba6ade618aefddcf6fab83bf7beea4fd449021b187d5825040e7f2857(
    value: typing.Optional[ComputeRegionSecurityPolicyRuleMatchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39602ca742789ee74db2f78e72907dff33af3f385f9bc3d13392e8bd25d0567b(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4564664da315a7a5d5a40544a094554267fd478b8316c74c00d02ff95acf0fda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0746b0bef21351834fdbc1d5554c5c1cfe70caa772c559a7db6fe6dc3794fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3f32664d536f441ec60afb1372076d053718147ad6a9142a718b4048cf2a41(
    value: typing.Optional[ComputeRegionSecurityPolicyRuleMatchExpr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feea12b656a90aa1b56722acf16dd592967d2dfb88b3598abad59ce9d6cdcf71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f0e6906d792149d3a474a77df59c0baa582afa43ab6314ea0293ebfd470501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3dc00d7b715373537ff1495216347b8c0e3ea7a724956e29d4e80477afb7e8(
    value: typing.Optional[ComputeRegionSecurityPolicyRuleMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ba7e6c1a17bfd23540ae360b52d3917c7a0cb003385c83fecaf0018d075034(
    *,
    dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_asns: typing.Optional[typing.Sequence[jsii.Number]] = None,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5464a0dc3a4f61676401ff162ba4ca964dea36045be7ea7302bba2f4533ab294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9acec81397e3893e252cb4f416e939c7fd9d6acbbdce7181e780488f9705617(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ec6df5e1039a4b894507b2956340d2daa849dc337b274ef40e35dc9c0fc292(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ea444c829d3fe2ae769557e968a6d6f5f52bdd8396703bb59d3ad618128913(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b883e046ba4b0baf0a10f8fcb1df88ad1c080d1e364bfbbc1664dfa59d2d815(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55696cd7f16cb43ea445b33105d9b02e836ba276d6d7797117c45f340363353(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8e18c9f36177cdabe4512925eeaa2f28fecda8a30a140f8badb74cd703683d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b461673c5a9fe183dc1881b762a603924529a721476157808569c9be71fef7f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf15a2b078980eef588d8a7269830f101c8f3e157b1d0dfbb6ced1d32f641ee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69aa13123edbf749bd7290e9656d9985082aab32857e00c5ec7ddf64ea477f5(
    value: typing.Optional[ComputeRegionSecurityPolicyRuleNetworkMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb53e2e5559f5823d2b8ff1ce1bb8ed0915204d7c18f0920491f48a8dec87692(
    *,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4f78f44e8ec5161af1d64ac81831abd5011cdb1542c023688a9d695cf0d68a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581602eccbf86bfae41fc9f5fe988b5ce2963c28effc597a9c234c0be3067882(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b5fa1c2faabdabecc98e68b1229a45658e6e8dcabaf0e61c20029d88cf64e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5b7636b6440eba1e42fec7916f4587c5e33d294172c4b9aed0142ace29eacb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c97ec0ce41b895ce20876635cb4a702b64c719388dea9d57b8dd304fd7d234a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec85abe57101eeed4228257ad2518f3a90f8f45353d93c556bdb7aca2b1bf439(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b35286585b97501297b7db80720362ee1bc799b9f1f9c432a61334e84de10e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc5dd506c9380f449252d94fb4a5efd66c0a680160549ffb1e5ae7f9d3fb57c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2d41b9e9261dcd17065b64a995cb06e4f575bc1dff2058b7da47538d18a773(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fb270e4b660a9018f969eaa4fafe6d29b102dc5507b277de7cee22187ba02f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleNetworkMatchUserDefinedFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021feebc0c49c2ee424ba11f158cdb2c845ea882fdf97a47d84d071ca3047d92(
    *,
    exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ba7fabe2f7c8aa0a4ff4c66cc5fff8c5e1bba3b787a03c700edf2270235666(
    *,
    target_rule_set: builtins.str,
    request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f91d868661678ecc6f625cb942ec299d33d81a0698ba64ec65a09205b14f47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01bfbe62fecf1510b0e396f9a7ba465fab850ed2a4ffabf70188d6061d9686bd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700849e1dbb73f0fdf4d65cfa00d31c6165acc9a035bb9fd33ead92ca79fec14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34feee52563464e6a2f8a460173ff493c4f7d10e48a81c909063ab10c7e97ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5094fc5c4aba6befc0794598e54a170ce0c9be79c4734b668eab8caaf22ff3c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ccb6a2479833bbda4e3fc6d1aeca5e8025d01bb1d133cba9f152d74d259b194(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99a4b6ff36a416c865c76efae22a3f18cab24ccedc3b537a41d495da7583029(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97553f88480401b392d458805d333955acd083a38a88658ed18db5376a3a6145(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2b0941125440e2fffc8561b90c34ef471f451766146ccd66b5b1e16f4ae376(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429f2520df738763fcb58ea6439a9f2a32e6ef391a7eeb2bfc5a11318bcc280f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e88a0e2dc7672ae6cdc9525f037eac83f4aa3a356371fe6225f439d615b840(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522399552c67ebb19ed0c3632f4e560fc242ccb8d6e5c4fb8e7ef888d50b8661(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938e0523f77f981ef5551d8ecc0da98ef47993afd8cde9a915f9d424e7968622(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91be5e7fa383ff8a2f707619c6ea4bb95be0170ba7eda7846b9e43774578b97e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1e114d59f647477c8de19c538d13d15c2e6a67f9c3825972dacf2cd39558f8(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bc795918a190275f8584b0733a4a8834065147d81a077ea62d0d8ba07eb09d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28aac98dd2e2e16a9ebea077a251b8f574464a7f70e98e4ee33a1332fe28bff8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a26a6dcdc06355f6cd0b72365fdf44d8741ddd0ae4376dc30882949c9aaf755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f79749328cef71f15dccc078b4c01551c7341e7a0de379bb50ee7d3e8818c33(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c0b6c87154effa066ed69abaa5d483bac2cd494deb4cf11f0d91174e734816(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bda2aea34ae17a94396bc09039a435dec67a963218bf9a193aab8a9549773b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cc4ea459e6f55cbfb67cc0c7cacd6d6280169a9f4c8983c2399e828b1218ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9adf3ff86b1f154fa4240c6c4b743d34eed8ed67147533096d875970ac3f14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7110553ea6df8776eb688ae94e1d631cac113f1b1502d3e324568e8c81cd6146(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a021d455fca1db71647c948cee4e1f9ec664005c9a7fb4aa5d4b1f8cb97632f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba52e13acc1df4c7664f42b5efb86ca0d108ffd00cd14506f5e88aff2bd3f75(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e450b4279636959e2146e44d6018d26ae53ff077de3c329d04c7d0a862add21f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c64d15c727468db2965011c68c6872b75472fd6f0b846d555d34c3db1e2fd20(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6affd07cc1c67e3938e2cf46596fbda39275ed44e2e5286e5f26feda398cc7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ddf78110e7edffd2ca3cd81638ef3300bd81185eb1880f6088bef78c4c5594(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24615150592dec5e30d12c15c20673b02c18c99e13f48d6afe70176fd644d2c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20d05b80a48c3608056bd9aba19ad260c9c9192a24403c44d1c8e8657810f81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f9ebab0331e3c23aca8618697eb59d8273e0c76687c8a882a216b0cbbe511e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614e6478e094abbd2f527528ad7866cb4cded7cbb22fcc13ee32bfcddea0ac44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bc3d98b0918e3fd23bb73bb9541170fc70fbe2505cb265cf596d4520746094(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015de449e4995549b7cf2362bbb96d672786a2e7f843ab9b117781db8b810b42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f49373d24ad38d7df31d7966c9f4bdb226212573eda4890c51c7e7db1d6a6cf(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f66213305033f982c0bd55be2e67c7b8e08313c6cc7dc0b597be953d2758cce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e307c5fac44cf1752c85b13edf5a13d8e08aa4381d75b33ef6c5d2a79907ec24(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8065030b2d589b11ff233c727a0cc524f857de869ba5dcad5a66dea7d90fc19c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94a8c30a0482c0feb4c1db19e00a2838acb36be2ac932c665b69d2ac4a3314f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83be0406299c3a426691f85095ea9f80268f7cd6a732c7a75cfc4867fddb5bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0432377735bac802e996e4b3ae37a4f08ad5d9469e62aed9012997916f7aaea4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766a084d7a4cd3fc5dc5b054526cbc51e93766d6d5e8fa3e99cbb59a30990011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7c518b001c13d34c58fcdfbbd42297edd934c0ef1bcf32a5b9c47c25241d4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb8da28dd0d09bee5fc96211d4592ac58443dd5ecf67ea8bd463bb48087e544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f96ebae1eddbda7f70f66a9bbb60cc96f3a8e3200107e1cf641438b671a031(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446500db0fbd5dae58cd7c0ad5820a4c51f63981ef2738c78929943f8ac1348d(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b377ed040b0698327f98403a0949b734407483071b1778c9f69c10054afdb81b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913968e83473973827acf849704bcf2147fcd45fb9a7bae4d349a7d115af1774(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1808638e65822e900c73f2620187edf75ac33aded4f78c9336d99204d5c049db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f012c179f46504a8d6a308c62eca064850b05335fcc8170051baf5e6173a860(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1583884370306e227a50f5cffded0bde4b1bf36fde3f8ea5b5e7275294a18c79(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ac4af61ba1d44b5a271e1c0f16848514c78aca5824c0501980b1f896e84ee5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac39a87a3e35cdc318a0e7057a5089d174cfd0a8f43d05ec0c06d0fb383e74c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d934583e255b4491b6be62a9b87e25656eab96066539aafd65fbd0219aba7616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afaaea7f3c70b9534bc16c00cc05aba48504aeba0de1ea5200e4cb32ccbaaa23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5f3d03cbf88c398ca05da540956fc8a4469b5c56f715c4f6480895f8f6efc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6693d2b1e381af4e16018bbdf44dcfa76616bf37042233370c81be5ae92f42bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7df7fbd7ca0dd082878a065433a30b8e6343d8bea8621c0c6754a323fcf0f8e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulePreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e1004357d512381e626bc081b388eafa153e4712b5aa0e500928a439ee01b7(
    value: typing.Optional[ComputeRegionSecurityPolicyRulePreconfiguredWafConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a6f47230258ae381e30d0e3baa6267889e636c7bddaa5fea0908718122b01b(
    *,
    ban_duration_sec: typing.Optional[jsii.Number] = None,
    ban_threshold: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
    conform_action: typing.Optional[builtins.str] = None,
    enforce_on_key: typing.Optional[builtins.str] = None,
    enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    exceed_action: typing.Optional[builtins.str] = None,
    rate_limit_threshold: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206b60357996820ea0cd36c9b4239a3c7f3e162c0b55e6e1429826a4ce45a9ee(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9420b08794541fa20911d2cd7e0c9237d6d6331adba8d81cd502723e3ea60273(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187cb2b3ad732de2d38062ec82bbe07f92aa7d02bd201cd2b59491be0fa6112d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a55bb262db765ff43b92ad4f8adce09845fe3b2b900cc0e30733f6df459500d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41f85d8940afab7a705cdbfdd043ddd5aca018c4cedea3ac47079a58670edfc(
    value: typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsBanThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3bd3702c7b0ed9bbfc1f89b8174f8285d6477580c55af37757d03612f81ac04(
    *,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    enforce_on_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573bc21c0790ae15ced9c6475ea0f42b5292c04a1df3a7966bdd6a12dd4bc595(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2a53ad18a1d91c1ade3083680076aafd53e577669aa39c3ba5e942edc521bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__326d2f2a4550004c2b0abda23705f3f5c480b62fb63ea951fb3503f1f3e028f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f36414746b63c24d80fb3e268d838d0370931a98665c8f890593d0730304599(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ed7c370fdddbb025818c1ebb306750dfab25e97e32f1ba0cac3b34be8a8c9d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7344ec0f6a7d547b65046837ddeb823c624f215064d7956c4ee950a4a1692377(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723ca41e4003150bf17377f25500a95cdc4735b9f3182e1158faf5d2a8bee525(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c442533b6e892727e80c4f956972399fd1d36ae9cca430f22012439cbc1ef7d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d1ee1afd9172d581943a29e425392518d2a864adc7bae56c2bd1e9003949db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9eb9d57351b1e1f056ad85480c7f380bec719ccf3afb115d0e0d6393ba0421a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6693aea83f7385a2accf0f0c55da22a2f4892998fd776cb54b78245980cbf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953dacdd635080b7f586ce686ebe98e4e61eb2ffe2d8bd8cef82ccccd0d2a6c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bd3142c1dda06065e3d5fd5ed8a5c7d6e3227200d1cd13869ebfa5760cecba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c786f18fb2bc19fa84b4e7848fc77879b4676b8e1980f2ea3a37049eb114d6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65457886411a7758ec7cf9c2ebd2da08f58f24a0bdb9534377a8f82f8a307a08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f330b5f2d4d5802e4089facba192a6e39767f8b110206733431b79843ff37442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c50aa77f3fc6bc4c9b7270f5edbea21f3291b08701dc35452489befc6ca314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c570a02ae4bac6889e60590a81d36be91cd5b47310ebd7a35639fb829f491207(
    value: typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a3f9e19e5122041c372b1b1d659cd0c5641a613164b584a5fd03bed0e5fa50(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e59248db8d323cebe53416f49c164e7c6f907a51e72a72cb1659814beac2a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ec9b827b3135ef0f2e982d57730e282eae7505abbd7d4f7f1c89fa1848914d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1428f97495cf2d36f0ad5da186cc005572432bfe040917bb079b32af7ff2b9e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e15fe31048b9f02f9d4a485d8a7db2885f5ad2747fdd0715f69fea781747f3(
    value: typing.Optional[ComputeRegionSecurityPolicyRuleRateLimitOptionsRateLimitThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95a3b9c6e3887d6ce205bfe013ef7417d2a8584ee29c08f6397cc2e0291914d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904c6d375ef011fca34cb231010ba77a371ed61edaed5902d3983cc172afb057(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc98908af6aa0abfe828ab17303a564efb230b8edfaf9ef48558e8d49f6f09dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5485ca35ccbd60d682fe7609a59d58af5b306c4459a32bcf97d8ff4d466da0e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fbb9d110d8601d72bda2aaa6d555feb7ca05c91248a65c1f08b66a2e0087ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2309bc0c46f43c412032a5e624831cee12c74b07e87c6d208273513ed27976(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
