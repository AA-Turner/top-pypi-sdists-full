r'''
# `google_compute_security_policy_rule`

Refer to the Terraform Registry for docs: [`google_compute_security_policy_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule).
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


class ComputeSecurityPolicyRuleA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleA",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule google_compute_security_policy_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        priority: jsii.Number,
        security_policy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        header_action: typing.Optional[typing.Union["ComputeSecurityPolicyRuleHeaderActionA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchA", typing.Dict[builtins.str, typing.Any]]] = None,
        preconfigured_waf_config: typing.Optional[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limit_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRedirectOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeSecurityPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule google_compute_security_policy_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: The Action to perform when the rule is matched. The following are the valid actions:. - allow: allow access to target. - deny(STATUS): deny access to target, returns the HTTP response code specified. Valid values for STATUS are 403, 404, and 502. - rate_based_ban: limit client traffic to the configured threshold and ban the client if the traffic exceeds the threshold. Configure parameters for this action in RateLimitOptions. Requires rateLimitOptions to be set. - redirect: redirect to a different target. This can either be an internal reCAPTCHA redirect, or an external URL-based redirect via a 302 response. Parameters for this action can be configured via redirectOptions. This action is only supported in Global Security Policies of type CLOUD_ARMOR. - throttle: limit client traffic to the configured threshold. Configure parameters for this action in rateLimitOptions. Requires rateLimitOptions to be set for this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#action ComputeSecurityPolicyRuleA#action}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#priority ComputeSecurityPolicyRuleA#priority}
        :param security_policy: The name of the security policy this rule belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#security_policy ComputeSecurityPolicyRuleA#security_policy}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#description ComputeSecurityPolicyRuleA#description}
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#header_action ComputeSecurityPolicyRuleA#header_action}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#id ComputeSecurityPolicyRuleA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#match ComputeSecurityPolicyRuleA#match}
        :param preconfigured_waf_config: preconfigured_waf_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#preconfigured_waf_config ComputeSecurityPolicyRuleA#preconfigured_waf_config}
        :param preview: If set to true, the specified action is not enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#preview ComputeSecurityPolicyRuleA#preview}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#project ComputeSecurityPolicyRuleA#project}.
        :param rate_limit_options: rate_limit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#rate_limit_options ComputeSecurityPolicyRuleA#rate_limit_options}
        :param redirect_options: redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#redirect_options ComputeSecurityPolicyRuleA#redirect_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#timeouts ComputeSecurityPolicyRuleA#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691f7fcc7d22a9e12d0f0baadf49d6abcd3ba135731c4245351c0262fa8b3fde)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeSecurityPolicyRuleAConfig(
            action=action,
            priority=priority,
            security_policy=security_policy,
            description=description,
            header_action=header_action,
            id=id,
            match=match,
            preconfigured_waf_config=preconfigured_waf_config,
            preview=preview,
            project=project,
            rate_limit_options=rate_limit_options,
            redirect_options=redirect_options,
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
        '''Generates CDKTF code for importing a ComputeSecurityPolicyRuleA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeSecurityPolicyRuleA to import.
        :param import_from_id: The id of the existing ComputeSecurityPolicyRuleA that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeSecurityPolicyRuleA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa84346c8250fe4aa3cb3a595f9ecdb997e3fad4998ab8605aeb2a892f236b36)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putHeaderAction")
    def put_header_action(
        self,
        *,
        request_headers_to_adds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_headers_to_adds: request_headers_to_adds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_headers_to_adds ComputeSecurityPolicyRuleA#request_headers_to_adds}
        '''
        value = ComputeSecurityPolicyRuleHeaderActionA(
            request_headers_to_adds=request_headers_to_adds
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        config: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchExprA", typing.Dict[builtins.str, typing.Any]]] = None,
        expr_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchExprOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#config ComputeSecurityPolicyRuleA#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#expr ComputeSecurityPolicyRuleA#expr}
        :param expr_options: expr_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#expr_options ComputeSecurityPolicyRuleA#expr_options}
        :param versioned_expr: Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#versioned_expr ComputeSecurityPolicyRuleA#versioned_expr}
        '''
        value = ComputeSecurityPolicyRuleMatchA(
            config=config,
            expr=expr,
            expr_options=expr_options,
            versioned_expr=versioned_expr,
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putPreconfiguredWafConfig")
    def put_preconfigured_waf_config(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#exclusion ComputeSecurityPolicyRuleA#exclusion}
        '''
        value = ComputeSecurityPolicyRulePreconfiguredWafConfigA(exclusion=exclusion)

        return typing.cast(None, jsii.invoke(self, "putPreconfiguredWafConfig", [value]))

    @jsii.member(jsii_name="putRateLimitOptions")
    def put_rate_limit_options(
        self,
        *,
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA", typing.Dict[builtins.str, typing.Any]]] = None,
        conform_action: typing.Optional[builtins.str] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_action: typing.Optional[builtins.str] = None,
        exceed_redirect_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        rate_limit_threshold: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#ban_duration_sec ComputeSecurityPolicyRuleA#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#ban_threshold ComputeSecurityPolicyRuleA#ban_threshold}
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#conform_action ComputeSecurityPolicyRuleA#conform_action}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key ComputeSecurityPolicyRuleA#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_configs ComputeSecurityPolicyRuleA#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_name ComputeSecurityPolicyRuleA#enforce_on_key_name}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint. Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#exceed_action ComputeSecurityPolicyRuleA#exceed_action}
        :param exceed_redirect_options: exceed_redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#exceed_redirect_options ComputeSecurityPolicyRuleA#exceed_redirect_options}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#rate_limit_threshold ComputeSecurityPolicyRuleA#rate_limit_threshold}
        '''
        value = ComputeSecurityPolicyRuleRateLimitOptionsA(
            ban_duration_sec=ban_duration_sec,
            ban_threshold=ban_threshold,
            conform_action=conform_action,
            enforce_on_key=enforce_on_key,
            enforce_on_key_configs=enforce_on_key_configs,
            enforce_on_key_name=enforce_on_key_name,
            exceed_action=exceed_action,
            exceed_redirect_options=exceed_redirect_options,
            rate_limit_threshold=rate_limit_threshold,
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimitOptions", [value]))

    @jsii.member(jsii_name="putRedirectOptions")
    def put_redirect_options(
        self,
        *,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target ComputeSecurityPolicyRuleA#target}
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#type ComputeSecurityPolicyRuleA#type}
        '''
        value = ComputeSecurityPolicyRuleRedirectOptionsA(target=target, type=type)

        return typing.cast(None, jsii.invoke(self, "putRedirectOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#create ComputeSecurityPolicyRuleA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#delete ComputeSecurityPolicyRuleA#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#update ComputeSecurityPolicyRuleA#update}.
        '''
        value = ComputeSecurityPolicyRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHeaderAction")
    def reset_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderAction", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

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

    @jsii.member(jsii_name="resetRedirectOptions")
    def reset_redirect_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectOptions", []))

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
    @jsii.member(jsii_name="headerAction")
    def header_action(self) -> "ComputeSecurityPolicyRuleHeaderActionAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleHeaderActionAOutputReference", jsii.get(self, "headerAction"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> "ComputeSecurityPolicyRuleMatchAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleMatchAOutputReference", jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfig")
    def preconfigured_waf_config(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference", jsii.get(self, "preconfiguredWafConfig"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitOptions")
    def rate_limit_options(
        self,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsAOutputReference", jsii.get(self, "rateLimitOptions"))

    @builtins.property
    @jsii.member(jsii_name="redirectOptions")
    def redirect_options(
        self,
    ) -> "ComputeSecurityPolicyRuleRedirectOptionsAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleRedirectOptionsAOutputReference", jsii.get(self, "redirectOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeSecurityPolicyRuleTimeoutsOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="headerActionInput")
    def header_action_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleHeaderActionA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleHeaderActionA"], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional["ComputeSecurityPolicyRuleMatchA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchA"], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfigInput")
    def preconfigured_waf_config_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRulePreconfiguredWafConfigA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRulePreconfiguredWafConfigA"], jsii.get(self, "preconfiguredWafConfigInput"))

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
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsA"], jsii.get(self, "rateLimitOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectOptionsInput")
    def redirect_options_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRedirectOptionsA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRedirectOptionsA"], jsii.get(self, "redirectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPolicyInput")
    def security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeSecurityPolicyRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeSecurityPolicyRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0494db04cb5b1f1caeb403ab3d889b55e48eea59cc56416223ae312cb5fcf73d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1184b3c648b0898eac47d0b8ffa6df9229cb50e4cedb33f6077418976f6bb1fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b173ad9c43ba279beb002ec1b70ce9afcbb424915397ae9333f1c56cb5f566)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb1a6ca95315f3d93af6a43694e4312cb281fba62b4105a59d6949d2c1651b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preview", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b83a45982f4dd220ccf728ccf32e3283d2530568395a232756338e0f720026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2708c45644fe79b7c84f86b351ed589155d2586c6e08c2ac87c83bb009e7a665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicy")
    def security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicy"))

    @security_policy.setter
    def security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9357b6cb3d30ccbe9167f3e9a51317c20986025ffea9c25383185ddda1defbe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleAConfig",
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
        "security_policy": "securityPolicy",
        "description": "description",
        "header_action": "headerAction",
        "id": "id",
        "match": "match",
        "preconfigured_waf_config": "preconfiguredWafConfig",
        "preview": "preview",
        "project": "project",
        "rate_limit_options": "rateLimitOptions",
        "redirect_options": "redirectOptions",
        "timeouts": "timeouts",
    },
)
class ComputeSecurityPolicyRuleAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        security_policy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        header_action: typing.Optional[typing.Union["ComputeSecurityPolicyRuleHeaderActionA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchA", typing.Dict[builtins.str, typing.Any]]] = None,
        preconfigured_waf_config: typing.Optional[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limit_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRedirectOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeSecurityPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: The Action to perform when the rule is matched. The following are the valid actions:. - allow: allow access to target. - deny(STATUS): deny access to target, returns the HTTP response code specified. Valid values for STATUS are 403, 404, and 502. - rate_based_ban: limit client traffic to the configured threshold and ban the client if the traffic exceeds the threshold. Configure parameters for this action in RateLimitOptions. Requires rateLimitOptions to be set. - redirect: redirect to a different target. This can either be an internal reCAPTCHA redirect, or an external URL-based redirect via a 302 response. Parameters for this action can be configured via redirectOptions. This action is only supported in Global Security Policies of type CLOUD_ARMOR. - throttle: limit client traffic to the configured threshold. Configure parameters for this action in rateLimitOptions. Requires rateLimitOptions to be set for this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#action ComputeSecurityPolicyRuleA#action}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#priority ComputeSecurityPolicyRuleA#priority}
        :param security_policy: The name of the security policy this rule belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#security_policy ComputeSecurityPolicyRuleA#security_policy}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#description ComputeSecurityPolicyRuleA#description}
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#header_action ComputeSecurityPolicyRuleA#header_action}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#id ComputeSecurityPolicyRuleA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#match ComputeSecurityPolicyRuleA#match}
        :param preconfigured_waf_config: preconfigured_waf_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#preconfigured_waf_config ComputeSecurityPolicyRuleA#preconfigured_waf_config}
        :param preview: If set to true, the specified action is not enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#preview ComputeSecurityPolicyRuleA#preview}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#project ComputeSecurityPolicyRuleA#project}.
        :param rate_limit_options: rate_limit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#rate_limit_options ComputeSecurityPolicyRuleA#rate_limit_options}
        :param redirect_options: redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#redirect_options ComputeSecurityPolicyRuleA#redirect_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#timeouts ComputeSecurityPolicyRuleA#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(header_action, dict):
            header_action = ComputeSecurityPolicyRuleHeaderActionA(**header_action)
        if isinstance(match, dict):
            match = ComputeSecurityPolicyRuleMatchA(**match)
        if isinstance(preconfigured_waf_config, dict):
            preconfigured_waf_config = ComputeSecurityPolicyRulePreconfiguredWafConfigA(**preconfigured_waf_config)
        if isinstance(rate_limit_options, dict):
            rate_limit_options = ComputeSecurityPolicyRuleRateLimitOptionsA(**rate_limit_options)
        if isinstance(redirect_options, dict):
            redirect_options = ComputeSecurityPolicyRuleRedirectOptionsA(**redirect_options)
        if isinstance(timeouts, dict):
            timeouts = ComputeSecurityPolicyRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4262c59dde9bd7ab66c95d422d2fce00e6ef6259eff20144ed8cd410969c5f6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument header_action", value=header_action, expected_type=type_hints["header_action"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument preconfigured_waf_config", value=preconfigured_waf_config, expected_type=type_hints["preconfigured_waf_config"])
            check_type(argname="argument preview", value=preview, expected_type=type_hints["preview"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument rate_limit_options", value=rate_limit_options, expected_type=type_hints["rate_limit_options"])
            check_type(argname="argument redirect_options", value=redirect_options, expected_type=type_hints["redirect_options"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "priority": priority,
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
        if header_action is not None:
            self._values["header_action"] = header_action
        if id is not None:
            self._values["id"] = id
        if match is not None:
            self._values["match"] = match
        if preconfigured_waf_config is not None:
            self._values["preconfigured_waf_config"] = preconfigured_waf_config
        if preview is not None:
            self._values["preview"] = preview
        if project is not None:
            self._values["project"] = project
        if rate_limit_options is not None:
            self._values["rate_limit_options"] = rate_limit_options
        if redirect_options is not None:
            self._values["redirect_options"] = redirect_options
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#action ComputeSecurityPolicyRuleA#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An integer indicating the priority of a rule in the list.

        The priority must be a positive value between 0 and 2147483647.
        Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#priority ComputeSecurityPolicyRuleA#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def security_policy(self) -> builtins.str:
        '''The name of the security policy this rule belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#security_policy ComputeSecurityPolicyRuleA#security_policy}
        '''
        result = self._values.get("security_policy")
        assert result is not None, "Required property 'security_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#description ComputeSecurityPolicyRuleA#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_action(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleHeaderActionA"]:
        '''header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#header_action ComputeSecurityPolicyRuleA#header_action}
        '''
        result = self._values.get("header_action")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleHeaderActionA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#id ComputeSecurityPolicyRuleA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match(self) -> typing.Optional["ComputeSecurityPolicyRuleMatchA"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#match ComputeSecurityPolicyRuleA#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchA"], result)

    @builtins.property
    def preconfigured_waf_config(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRulePreconfiguredWafConfigA"]:
        '''preconfigured_waf_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#preconfigured_waf_config ComputeSecurityPolicyRuleA#preconfigured_waf_config}
        '''
        result = self._values.get("preconfigured_waf_config")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRulePreconfiguredWafConfigA"], result)

    @builtins.property
    def preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the specified action is not enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#preview ComputeSecurityPolicyRuleA#preview}
        '''
        result = self._values.get("preview")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#project ComputeSecurityPolicyRuleA#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limit_options(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsA"]:
        '''rate_limit_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#rate_limit_options ComputeSecurityPolicyRuleA#rate_limit_options}
        '''
        result = self._values.get("rate_limit_options")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsA"], result)

    @builtins.property
    def redirect_options(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRedirectOptionsA"]:
        '''redirect_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#redirect_options ComputeSecurityPolicyRuleA#redirect_options}
        '''
        result = self._values.get("redirect_options")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRedirectOptionsA"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeSecurityPolicyRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#timeouts ComputeSecurityPolicyRuleA#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleHeaderActionA",
    jsii_struct_bases=[],
    name_mapping={"request_headers_to_adds": "requestHeadersToAdds"},
)
class ComputeSecurityPolicyRuleHeaderActionA:
    def __init__(
        self,
        *,
        request_headers_to_adds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_headers_to_adds: request_headers_to_adds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_headers_to_adds ComputeSecurityPolicyRuleA#request_headers_to_adds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644ccddb690dfb75550d500f55b473f2805ab9af079362944a83dbaa5feeb776)
            check_type(argname="argument request_headers_to_adds", value=request_headers_to_adds, expected_type=type_hints["request_headers_to_adds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if request_headers_to_adds is not None:
            self._values["request_headers_to_adds"] = request_headers_to_adds

    @builtins.property
    def request_headers_to_adds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA"]]]:
        '''request_headers_to_adds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_headers_to_adds ComputeSecurityPolicyRuleA#request_headers_to_adds}
        '''
        result = self._values.get("request_headers_to_adds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleHeaderActionA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleHeaderActionAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleHeaderActionAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6414801bf9841e0034c714273bdf10735d2bcf27355e862a889506ecdf1fa5ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeadersToAdds")
    def put_request_headers_to_adds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f799705f538dd525f74be2dbe657c1384a630bf6185276078cd666ab8ca22a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeadersToAdds", [value]))

    @jsii.member(jsii_name="resetRequestHeadersToAdds")
    def reset_request_headers_to_adds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeadersToAdds", []))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAdds")
    def request_headers_to_adds(
        self,
    ) -> "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList":
        return typing.cast("ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList", jsii.get(self, "requestHeadersToAdds"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAddsInput")
    def request_headers_to_adds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA"]]], jsii.get(self, "requestHeadersToAddsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSecurityPolicyRuleHeaderActionA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleHeaderActionA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleHeaderActionA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a4f3eea02bc7f92b646e81da59d013c601f99102300db17846591e89f2f013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName", "header_value": "headerValue"},
)
class ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA:
    def __init__(
        self,
        *,
        header_name: typing.Optional[builtins.str] = None,
        header_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#header_name ComputeSecurityPolicyRuleA#header_name}
        :param header_value: The value to set the named header to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#header_value ComputeSecurityPolicyRuleA#header_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c0ae89b8c20313dbf35e6b74e69fd6cbf332a4828b8ad60e189407f16395830)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_name is not None:
            self._values["header_name"] = header_name
        if header_value is not None:
            self._values["header_value"] = header_value

    @builtins.property
    def header_name(self) -> typing.Optional[builtins.str]:
        '''The name of the header to set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#header_name ComputeSecurityPolicyRuleA#header_name}
        '''
        result = self._values.get("header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_value(self) -> typing.Optional[builtins.str]:
        '''The value to set the named header to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#header_value ComputeSecurityPolicyRuleA#header_value}
        '''
        result = self._values.get("header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60f19f2117204b5d3f6f0f1f23935ee3c2e177dfc32ad2f0a62ce59ce61e5ca9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf4351cc93632a889abd80390c269973bdfff3883eed245548faaed7747814e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b2edd4b86c68e0d346c4fd440b850188621cfd5723f319a9b20d572f256aca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87c0b473212d8684289ec858bc8fba915c89815be1fa790e03702928c1157926)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6312b7ed790415d442e46a1bb06344729e0242b014e23cc1e5a3a4df476714e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d846ac2ca4943b2bbdf77c1d57de26cd26a789dd2bee455054a6f950fdbde1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71a888a9da899c8f0cdd68cc4fd91bc5b379f204c194461fe93e5b320e2a0c1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHeaderName")
    def reset_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderName", []))

    @jsii.member(jsii_name="resetHeaderValue")
    def reset_header_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderValue", []))

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="headerValueInput")
    def header_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace213b7d47aee07733d03ddb64766c217cd040e66ba6ad0e06d37a6aef308b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af97b8d109d0300ad9e7ec227885213cbc012014470559e6a3d522e4c4622c0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a271c7373fbf811af842fbf47ab0ef787638c3e825ff3a43e676a862fb953ba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchA",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "expr": "expr",
        "expr_options": "exprOptions",
        "versioned_expr": "versionedExpr",
    },
)
class ComputeSecurityPolicyRuleMatchA:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchExprA", typing.Dict[builtins.str, typing.Any]]] = None,
        expr_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchExprOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#config ComputeSecurityPolicyRuleA#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#expr ComputeSecurityPolicyRuleA#expr}
        :param expr_options: expr_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#expr_options ComputeSecurityPolicyRuleA#expr_options}
        :param versioned_expr: Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#versioned_expr ComputeSecurityPolicyRuleA#versioned_expr}
        '''
        if isinstance(config, dict):
            config = ComputeSecurityPolicyRuleMatchConfigA(**config)
        if isinstance(expr, dict):
            expr = ComputeSecurityPolicyRuleMatchExprA(**expr)
        if isinstance(expr_options, dict):
            expr_options = ComputeSecurityPolicyRuleMatchExprOptionsA(**expr_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65174d8f91f150dcac58e1d728372be3b0633231ede5bdd54ea57b7f7df2165c)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument expr", value=expr, expected_type=type_hints["expr"])
            check_type(argname="argument expr_options", value=expr_options, expected_type=type_hints["expr_options"])
            check_type(argname="argument versioned_expr", value=versioned_expr, expected_type=type_hints["versioned_expr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if expr is not None:
            self._values["expr"] = expr
        if expr_options is not None:
            self._values["expr_options"] = expr_options
        if versioned_expr is not None:
            self._values["versioned_expr"] = versioned_expr

    @builtins.property
    def config(self) -> typing.Optional["ComputeSecurityPolicyRuleMatchConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#config ComputeSecurityPolicyRuleA#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchConfigA"], result)

    @builtins.property
    def expr(self) -> typing.Optional["ComputeSecurityPolicyRuleMatchExprA"]:
        '''expr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#expr ComputeSecurityPolicyRuleA#expr}
        '''
        result = self._values.get("expr")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchExprA"], result)

    @builtins.property
    def expr_options(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleMatchExprOptionsA"]:
        '''expr_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#expr_options ComputeSecurityPolicyRuleA#expr_options}
        '''
        result = self._values.get("expr_options")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchExprOptionsA"], result)

    @builtins.property
    def versioned_expr(self) -> typing.Optional[builtins.str]:
        '''Preconfigured versioned expression.

        If this field is specified, config must also be specified.
        Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#versioned_expr ComputeSecurityPolicyRuleA#versioned_expr}
        '''
        result = self._values.get("versioned_expr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatchA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleMatchAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3cf7ec571d9282573fd4c4c528c1177fc318faeee54c39fb28eedd1b34acacc)
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
        :param src_ip_ranges: CIDR IP address range. Maximum number of srcIpRanges allowed is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#src_ip_ranges ComputeSecurityPolicyRuleA#src_ip_ranges}
        '''
        value = ComputeSecurityPolicyRuleMatchConfigA(src_ip_ranges=src_ip_ranges)

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putExpr")
    def put_expr(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#expression ComputeSecurityPolicyRuleA#expression}
        '''
        value = ComputeSecurityPolicyRuleMatchExprA(expression=expression)

        return typing.cast(None, jsii.invoke(self, "putExpr", [value]))

    @jsii.member(jsii_name="putExprOptions")
    def put_expr_options(
        self,
        *,
        recaptcha_options: typing.Union["ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recaptcha_options: recaptcha_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#recaptcha_options ComputeSecurityPolicyRuleA#recaptcha_options}
        '''
        value = ComputeSecurityPolicyRuleMatchExprOptionsA(
            recaptcha_options=recaptcha_options
        )

        return typing.cast(None, jsii.invoke(self, "putExprOptions", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetExpr")
    def reset_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpr", []))

    @jsii.member(jsii_name="resetExprOptions")
    def reset_expr_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExprOptions", []))

    @jsii.member(jsii_name="resetVersionedExpr")
    def reset_versioned_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionedExpr", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "ComputeSecurityPolicyRuleMatchConfigAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleMatchConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="expr")
    def expr(self) -> "ComputeSecurityPolicyRuleMatchExprAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleMatchExprAOutputReference", jsii.get(self, "expr"))

    @builtins.property
    @jsii.member(jsii_name="exprOptions")
    def expr_options(
        self,
    ) -> "ComputeSecurityPolicyRuleMatchExprOptionsAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleMatchExprOptionsAOutputReference", jsii.get(self, "exprOptions"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["ComputeSecurityPolicyRuleMatchConfigA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="exprInput")
    def expr_input(self) -> typing.Optional["ComputeSecurityPolicyRuleMatchExprA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchExprA"], jsii.get(self, "exprInput"))

    @builtins.property
    @jsii.member(jsii_name="exprOptionsInput")
    def expr_options_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleMatchExprOptionsA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchExprOptionsA"], jsii.get(self, "exprOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__59647a7baa9c1256980a903143cc704b556bc779dc5a6b64ccf48afe0903b676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionedExpr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSecurityPolicyRuleMatchA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatchA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840439d5051bc274b962eb072c1e27b16c24f61551a3a4c618ac5808980e27e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchConfigA",
    jsii_struct_bases=[],
    name_mapping={"src_ip_ranges": "srcIpRanges"},
)
class ComputeSecurityPolicyRuleMatchConfigA:
    def __init__(
        self,
        *,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param src_ip_ranges: CIDR IP address range. Maximum number of srcIpRanges allowed is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#src_ip_ranges ComputeSecurityPolicyRuleA#src_ip_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b6ab2577b3c54368655c6d34d83d27c17c78d97c419cb239e85ca822397f13)
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if src_ip_ranges is not None:
            self._values["src_ip_ranges"] = src_ip_ranges

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of srcIpRanges allowed is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#src_ip_ranges ComputeSecurityPolicyRuleA#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatchConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleMatchConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b04cc9efd64a083969f0780ec78860ce7e37eb4fa1fb1c0f601a36bc49884d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36b67d93a953c4a841fee0257bd3fc80202e01d42b4ae546e1dc41981a4314b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSecurityPolicyRuleMatchConfigA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatchConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b50d2d9301f0976b51e0501aa539e2fbe9b29772586a12f66c8fe7e0ebf4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchExprA",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class ComputeSecurityPolicyRuleMatchExprA:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#expression ComputeSecurityPolicyRuleA#expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4e1bab806a7c61d681ea6878e985e466a1c79c4e8c7af3d0664434a0ae4256)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        The application context of the containing message determines which well-known feature set of CEL is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#expression ComputeSecurityPolicyRuleA#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatchExprA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleMatchExprAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchExprAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc9ceda20ac2988a4e62cebf98e9148fda21535ad47e8d8a0398f4809f2212bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2740bf3d2a484c57d599f7f9bbc0728459f8d871bb93ab3f48e6e4de9862b6ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSecurityPolicyRuleMatchExprA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchExprA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatchExprA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b9e433e9c35e26a16d8b5b438d8575cf8e1424bff1cb1c8f02e80bfc57a96a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchExprOptionsA",
    jsii_struct_bases=[],
    name_mapping={"recaptcha_options": "recaptchaOptions"},
)
class ComputeSecurityPolicyRuleMatchExprOptionsA:
    def __init__(
        self,
        *,
        recaptcha_options: typing.Union["ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recaptcha_options: recaptcha_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#recaptcha_options ComputeSecurityPolicyRuleA#recaptcha_options}
        '''
        if isinstance(recaptcha_options, dict):
            recaptcha_options = ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA(**recaptcha_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055bf2d0d71f440aa828c41c8a4b4e22a07285e5d79ca34e7394305233e5b60d)
            check_type(argname="argument recaptcha_options", value=recaptcha_options, expected_type=type_hints["recaptcha_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recaptcha_options": recaptcha_options,
        }

    @builtins.property
    def recaptcha_options(
        self,
    ) -> "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA":
        '''recaptcha_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#recaptcha_options ComputeSecurityPolicyRuleA#recaptcha_options}
        '''
        result = self._values.get("recaptcha_options")
        assert result is not None, "Required property 'recaptcha_options' is missing"
        return typing.cast("ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatchExprOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleMatchExprOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchExprOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca8858b9b4ebb3761b6ef83756ff82ecfe5bb019170a0ec7c422451c940d1e95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecaptchaOptions")
    def put_recaptcha_options(
        self,
        *,
        action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA action-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#action_token_site_keys ComputeSecurityPolicyRuleA#action_token_site_keys}
        :param session_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA session-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#session_token_site_keys ComputeSecurityPolicyRuleA#session_token_site_keys}
        '''
        value = ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA(
            action_token_site_keys=action_token_site_keys,
            session_token_site_keys=session_token_site_keys,
        )

        return typing.cast(None, jsii.invoke(self, "putRecaptchaOptions", [value]))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptions")
    def recaptcha_options(
        self,
    ) -> "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference", jsii.get(self, "recaptchaOptions"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptionsInput")
    def recaptcha_options_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA"], jsii.get(self, "recaptchaOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a45ed025a064552c9bd4755e6ce04a1f882ff85380f62c326969858a43cc2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA",
    jsii_struct_bases=[],
    name_mapping={
        "action_token_site_keys": "actionTokenSiteKeys",
        "session_token_site_keys": "sessionTokenSiteKeys",
    },
)
class ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA:
    def __init__(
        self,
        *,
        action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA action-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#action_token_site_keys ComputeSecurityPolicyRuleA#action_token_site_keys}
        :param session_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA session-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#session_token_site_keys ComputeSecurityPolicyRuleA#session_token_site_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7abf57ca54b23bd0ffd27b075c465845cf1994307e7a784fab7f68c2e30c8a)
            check_type(argname="argument action_token_site_keys", value=action_token_site_keys, expected_type=type_hints["action_token_site_keys"])
            check_type(argname="argument session_token_site_keys", value=session_token_site_keys, expected_type=type_hints["session_token_site_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_token_site_keys is not None:
            self._values["action_token_site_keys"] = action_token_site_keys
        if session_token_site_keys is not None:
            self._values["session_token_site_keys"] = session_token_site_keys

    @builtins.property
    def action_token_site_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of site keys to be used during the validation of reCAPTCHA action-tokens.

        The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#action_token_site_keys ComputeSecurityPolicyRuleA#action_token_site_keys}
        '''
        result = self._values.get("action_token_site_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_token_site_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of site keys to be used during the validation of reCAPTCHA session-tokens.

        The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#session_token_site_keys ComputeSecurityPolicyRuleA#session_token_site_keys}
        '''
        result = self._values.get("session_token_site_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__432bcd1f8ad5cce52f6af6803e9e39dc45e0447d3078d93f6ae264c77b9fe1df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActionTokenSiteKeys")
    def reset_action_token_site_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionTokenSiteKeys", []))

    @jsii.member(jsii_name="resetSessionTokenSiteKeys")
    def reset_session_token_site_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTokenSiteKeys", []))

    @builtins.property
    @jsii.member(jsii_name="actionTokenSiteKeysInput")
    def action_token_site_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionTokenSiteKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTokenSiteKeysInput")
    def session_token_site_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sessionTokenSiteKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="actionTokenSiteKeys")
    def action_token_site_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actionTokenSiteKeys"))

    @action_token_site_keys.setter
    def action_token_site_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a516228e6148beff957229ec7bb2533c546e034098e6b2e40bce5a8d6350ef31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionTokenSiteKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTokenSiteKeys")
    def session_token_site_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sessionTokenSiteKeys"))

    @session_token_site_keys.setter
    def session_token_site_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b062e24842185c2638e781f43a43d6d839772c897a5812513a70fdad9632037d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTokenSiteKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1932c30d6536ac49bb7dd8c62fbeb21b6767c86a490bda27f190faac015cf494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigA",
    jsii_struct_bases=[],
    name_mapping={"exclusion": "exclusion"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigA:
    def __init__(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#exclusion ComputeSecurityPolicyRuleA#exclusion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287cdc7356f3874f4dbfaeb3817aaf722133bb1598f2df3204b56470de15879c)
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusion is not None:
            self._values["exclusion"] = exclusion

    @builtins.property
    def exclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA"]]]:
        '''exclusion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#exclusion ComputeSecurityPolicyRuleA#exclusion}
        '''
        result = self._values.get("exclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__caa0f7e8d6c804130e379130f363cdfede1d769ec08fd9666f71b66ff697867d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusion")
    def put_exclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84df2ba8ad77d0e8804eb761da07549dd9e095e490d1c1ddfe0e9c5cde370a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusion", [value]))

    @jsii.member(jsii_name="resetExclusion")
    def reset_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusion", []))

    @builtins.property
    @jsii.member(jsii_name="exclusion")
    def exclusion(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList", jsii.get(self, "exclusion"))

    @builtins.property
    @jsii.member(jsii_name="exclusionInput")
    def exclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA"]]], jsii.get(self, "exclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRulePreconfiguredWafConfigA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRulePreconfiguredWafConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRulePreconfiguredWafConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643f99851738649af5f219baf57e0d192fa27dcbabcf394cb2dd905846c1b3f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA",
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
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA:
    def __init__(
        self,
        *,
        target_rule_set: builtins.str,
        request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param target_rule_set: Target WAF rule set to apply the preconfigured WAF exclusion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target_rule_set ComputeSecurityPolicyRuleA#target_rule_set}
        :param request_cookie: request_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_cookie ComputeSecurityPolicyRuleA#request_cookie}
        :param request_header: request_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_header ComputeSecurityPolicyRuleA#request_header}
        :param request_query_param: request_query_param block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_query_param ComputeSecurityPolicyRuleA#request_query_param}
        :param request_uri: request_uri block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_uri ComputeSecurityPolicyRuleA#request_uri}
        :param target_rule_ids: A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion. If omitted, it refers to all the rule IDs under the WAF rule set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target_rule_ids ComputeSecurityPolicyRuleA#target_rule_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09409a0f88a17f93a4326bae5a8ef8470a7dd50a5692284fa20ee7506bc5ddde)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target_rule_set ComputeSecurityPolicyRuleA#target_rule_set}
        '''
        result = self._values.get("target_rule_set")
        assert result is not None, "Required property 'target_rule_set' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_cookie(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA"]]]:
        '''request_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_cookie ComputeSecurityPolicyRuleA#request_cookie}
        '''
        result = self._values.get("request_cookie")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA"]]], result)

    @builtins.property
    def request_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA"]]]:
        '''request_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_header ComputeSecurityPolicyRuleA#request_header}
        '''
        result = self._values.get("request_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA"]]], result)

    @builtins.property
    def request_query_param(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA"]]]:
        '''request_query_param block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_query_param ComputeSecurityPolicyRuleA#request_query_param}
        '''
        result = self._values.get("request_query_param")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA"]]], result)

    @builtins.property
    def request_uri(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA"]]]:
        '''request_uri block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#request_uri ComputeSecurityPolicyRuleA#request_uri}
        '''
        result = self._values.get("request_uri")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA"]]], result)

    @builtins.property
    def target_rule_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion.

        If omitted, it refers to all the rule IDs under the WAF rule set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target_rule_ids ComputeSecurityPolicyRuleA#target_rule_ids}
        '''
        result = self._values.get("target_rule_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b202d111e19e31c2ac121a27313719b0b1e697d41326cda9ca29aa1d49de2a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296c4542722baf33f688ce68d8d2028d9301b0f234f447f46c2c421e60d13013)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fa88ae0a95e9c3afb121517273a6f18ea5fac26aa0c1b9fdf44e627b6284d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a07430d878704b3f3ff15e77baf3a989e3704ce0e97df0f41762e77022256dc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9c4a8d0a8b440e4bbfc4f72f69ad3dd096a5f8a1bffe9df45cf8614e30d517a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9015ece2390ae9d603ff285331a25363b6de83eedbea406a927bef9346a04d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e0088add0a270fe20321b28ad8f24b5f7c827fa99b33222086fbd20d8bb9ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRequestCookie")
    def put_request_cookie(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3caca70ac27a66db48f7f29173622dc21806067f7a90167d86498c4d7bdb666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestCookie", [value]))

    @jsii.member(jsii_name="putRequestHeader")
    def put_request_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd02fb8aea3cb9fd3fe9606d711f4345d84a9835ecb087ebd34323a6cd095280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeader", [value]))

    @jsii.member(jsii_name="putRequestQueryParam")
    def put_request_query_param(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b84a56d33da4c2d576b9596184b0640f3dabb5fb51a6ae697b72e30f104c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestQueryParam", [value]))

    @jsii.member(jsii_name="putRequestUri")
    def put_request_uri(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bb76abd048a1c8700da7e8fc4969c9e3f22942e5a4e5dfe611543cccfd63ae)
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
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList", jsii.get(self, "requestCookie"))

    @builtins.property
    @jsii.member(jsii_name="requestHeader")
    def request_header(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList", jsii.get(self, "requestHeader"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParam")
    def request_query_param(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList", jsii.get(self, "requestQueryParam"))

    @builtins.property
    @jsii.member(jsii_name="requestUri")
    def request_uri(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList", jsii.get(self, "requestUri"))

    @builtins.property
    @jsii.member(jsii_name="requestCookieInput")
    def request_cookie_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA"]]], jsii.get(self, "requestCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderInput")
    def request_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA"]]], jsii.get(self, "requestHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParamInput")
    def request_query_param_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA"]]], jsii.get(self, "requestQueryParamInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriInput")
    def request_uri_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA"]]], jsii.get(self, "requestUriInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__89743f6899d2b8d0fa3bf513a75d87e5187db5a662f0e8a3f61696f3741e5509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRuleSet")
    def target_rule_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRuleSet"))

    @target_rule_set.setter
    def target_rule_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813acd9c72c844a825a23e3b02a9f5be70cae6e3b812867c79a0e679714895ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63da5b3dfbb01af917392fd4c9fc05ba4d120b15fab476c5afec68738c5ee682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#operator ComputeSecurityPolicyRuleA#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#value ComputeSecurityPolicyRuleA#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db067c5d08346c23f6bbbbdcfbf3fb35fc6cc09f54c0a6b8db684a1a9db576fe)
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
        EQUALS_ANY: The operator matches if the field value is any value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#operator ComputeSecurityPolicyRuleA#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#value ComputeSecurityPolicyRuleA#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55377edfbf161e5c77455fae3f835d543684ea9a4f2657e1311b4fc6839efde0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96bab36c5717530189eda20dcea864d796a2182a6e8261e9adb2c80a0395dd40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f503e61edfab201d1d967e2303ad11c53e83ab1c12aae68adb57704712490b3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5081d5b9a9bd2a89387fbe90d35e386f5e7182efcfa8d06f6e1262403cbb7b35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12bd4634d221c48ef8372a9e9ddd972859a295d592f061031ee9558280684982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356105e0859e0a99b35e88fb9df5da70e42e286c638d5dac5544e253e76e3ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf6bf8a0d27e2b4047f9bf9cff8bc10282a301cb9b6f5cb058348966681af62d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a218eaa2438220fa65371c6ac76fcb586e8b5195ba7d5678a37ec365b226113f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a200a05bdd6f54de4b13fc0ed9a9279ba98225cad3be98834d354da2d8e38f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e29762ce9d3dc301e7edf9ba9a37d13dbd6a3919999609e77ea6d9c69b9921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#operator ComputeSecurityPolicyRuleA#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#value ComputeSecurityPolicyRuleA#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae7bc0990449cf71bfefe77791700f41011eced3eb80e50bbc9a777e483660c)
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
        EQUALS_ANY: The operator matches if the field value is any value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#operator ComputeSecurityPolicyRuleA#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#value ComputeSecurityPolicyRuleA#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e45369b30e58ec9b5c865d653299402f79bc002b892ba4445da7eb48340afbeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186a0a443a7d4b449921ed43e81c20b7d1ca24a6efee168e1ae71fcf9049ba80)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b728d4bf212d75fbcea712de2ba6e07d083aaed2cabccccdd6d67ddabf3d5b80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0efd23210a5e7449f28916883895cd8e63841040ea458104ceb838c813c08bbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__264db8637e4fc3e0916ec45dbc0f87d703937ead026e4f4891488a7a538b5f65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95de6e99920d6ab28d5bfeeb0e8dce0a43a9ae316c1342cd3fec81097db477b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a599fa62e8acd45e5644dee0d291ee4b5b830b816baaa6d5a6dc04992a4cdde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c295e5092696ce0c9e56cf08c5654ffb3a5d5a11cae262595eb3fda8213e55e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e34db4f849ef25763e1c3cb2c3832f4b745b08f11cf7bd1110146e3cb9aea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64d7ea80da1795fc714da6fabbf6edc6ebdd22fbbedcae35a9ec72393fbd1f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#operator ComputeSecurityPolicyRuleA#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#value ComputeSecurityPolicyRuleA#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f34494ccd8587d872a433afa9e2016768a09fbaf691a30ea885c7264c36d411)
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
        EQUALS_ANY: The operator matches if the field value is any value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#operator ComputeSecurityPolicyRuleA#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#value ComputeSecurityPolicyRuleA#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75eb7593479966ac6cc22a640c54d53b1839569c81f6a894a90ccdae8dbbbd34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d81f6e3e62e2028da08f470daa35ebff8d71165a779c264e5cea67c8d282d5d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a018dfcc32fd65adb259403130ed58ffbf517e484a22fb4db26ec215ecbc86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7962affac43a89fcb906f2f50d3c06b50aad5a85773a8813698e27c25b9baa1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84021e429dd72c0e695d4f194d2ec2bc1fa62860935fc8a403040db86dda2c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271fdfc52bb31c9f9991fdfaf1961c495bc2ba01bcc63c5c19c61e3dd406a245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__742c3132b9ff76726494e005f22a2861c53fa17cb86d6063a3f98f517cc6b795)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d42afffd1c48bb6cb48e6b34afa3ee2148ec0a9057d50f285398bd8ce14d86fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d142437ee82d4f8e54282f907785485c72786a342605054dc3eda05d255b663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b04b6144189e06ab28f15faec46d875444da006b0ea0a48adbf91286302317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#operator ComputeSecurityPolicyRuleA#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#value ComputeSecurityPolicyRuleA#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fb2f4fa2932fa6c1bfe96f550fa1254b2224e3f39c49d3854ef302cf981a42)
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
        EQUALS_ANY: The operator matches if the field value is any value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#operator ComputeSecurityPolicyRuleA#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#value ComputeSecurityPolicyRuleA#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d858314efc59b10be227257146650d63f9127c0b79030527aeba334a19eb9578)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb879b177870f3d564015ac02aa5ded720a34bd7560e7c858d8eb48d340835f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11e5b51acd4b2881c3c0bce3a885e3bea20b683daf79c57a2858b10e3a42840)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca7155166d0318390c2d4fd5d20158bca35ee128024571d4ba3f127d836f26d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54d305b1f995be8435c9ffc8920937e3dee62b19986edef54e602f1990e045ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fcdbb97ecc7f593d19fc676f814f6e4a4fbc782ffafaf6ce30e5d4dc94ba68d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f033e73bfb4f196c94ce50375495309c74298933221bc841f94749d23ccfbc85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af66c73a72fb3f2e26ca59ebaa3844410ae7a9366da089ac55a13af4faeec01b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6c8ca73c17e37a87e00ef6444e10e36dc23ccf07cbada90a19fff90e22518c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e8811f458a717fb1c36a03e540f7ac2df49d31e2e25a0ca752cbaadd81c8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsA",
    jsii_struct_bases=[],
    name_mapping={
        "ban_duration_sec": "banDurationSec",
        "ban_threshold": "banThreshold",
        "conform_action": "conformAction",
        "enforce_on_key": "enforceOnKey",
        "enforce_on_key_configs": "enforceOnKeyConfigs",
        "enforce_on_key_name": "enforceOnKeyName",
        "exceed_action": "exceedAction",
        "exceed_redirect_options": "exceedRedirectOptions",
        "rate_limit_threshold": "rateLimitThreshold",
    },
)
class ComputeSecurityPolicyRuleRateLimitOptionsA:
    def __init__(
        self,
        *,
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA", typing.Dict[builtins.str, typing.Any]]] = None,
        conform_action: typing.Optional[builtins.str] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_action: typing.Optional[builtins.str] = None,
        exceed_redirect_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        rate_limit_threshold: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#ban_duration_sec ComputeSecurityPolicyRuleA#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#ban_threshold ComputeSecurityPolicyRuleA#ban_threshold}
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#conform_action ComputeSecurityPolicyRuleA#conform_action}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key ComputeSecurityPolicyRuleA#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_configs ComputeSecurityPolicyRuleA#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_name ComputeSecurityPolicyRuleA#enforce_on_key_name}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint. Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#exceed_action ComputeSecurityPolicyRuleA#exceed_action}
        :param exceed_redirect_options: exceed_redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#exceed_redirect_options ComputeSecurityPolicyRuleA#exceed_redirect_options}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#rate_limit_threshold ComputeSecurityPolicyRuleA#rate_limit_threshold}
        '''
        if isinstance(ban_threshold, dict):
            ban_threshold = ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA(**ban_threshold)
        if isinstance(exceed_redirect_options, dict):
            exceed_redirect_options = ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA(**exceed_redirect_options)
        if isinstance(rate_limit_threshold, dict):
            rate_limit_threshold = ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA(**rate_limit_threshold)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79ab185097daf9e58182b59b3b5ca352314fb25cf6100f6cc5e721e8b36aeec)
            check_type(argname="argument ban_duration_sec", value=ban_duration_sec, expected_type=type_hints["ban_duration_sec"])
            check_type(argname="argument ban_threshold", value=ban_threshold, expected_type=type_hints["ban_threshold"])
            check_type(argname="argument conform_action", value=conform_action, expected_type=type_hints["conform_action"])
            check_type(argname="argument enforce_on_key", value=enforce_on_key, expected_type=type_hints["enforce_on_key"])
            check_type(argname="argument enforce_on_key_configs", value=enforce_on_key_configs, expected_type=type_hints["enforce_on_key_configs"])
            check_type(argname="argument enforce_on_key_name", value=enforce_on_key_name, expected_type=type_hints["enforce_on_key_name"])
            check_type(argname="argument exceed_action", value=exceed_action, expected_type=type_hints["exceed_action"])
            check_type(argname="argument exceed_redirect_options", value=exceed_redirect_options, expected_type=type_hints["exceed_redirect_options"])
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
        if exceed_redirect_options is not None:
            self._values["exceed_redirect_options"] = exceed_redirect_options
        if rate_limit_threshold is not None:
            self._values["rate_limit_threshold"] = rate_limit_threshold

    @builtins.property
    def ban_duration_sec(self) -> typing.Optional[jsii.Number]:
        '''Can only be specified if the action for the rule is "rate_based_ban".

        If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#ban_duration_sec ComputeSecurityPolicyRuleA#ban_duration_sec}
        '''
        result = self._values.get("ban_duration_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ban_threshold(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA"]:
        '''ban_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#ban_threshold ComputeSecurityPolicyRuleA#ban_threshold}
        '''
        result = self._values.get("ban_threshold")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA"], result)

    @builtins.property
    def conform_action(self) -> typing.Optional[builtins.str]:
        '''Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#conform_action ComputeSecurityPolicyRuleA#conform_action}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key ComputeSecurityPolicyRuleA#enforce_on_key}
        '''
        result = self._values.get("enforce_on_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA"]]]:
        '''enforce_on_key_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_configs ComputeSecurityPolicyRuleA#enforce_on_key_configs}
        '''
        result = self._values.get("enforce_on_key_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA"]]], result)

    @builtins.property
    def enforce_on_key_name(self) -> typing.Optional[builtins.str]:
        '''Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value.

        HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_name ComputeSecurityPolicyRuleA#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exceed_action(self) -> typing.Optional[builtins.str]:
        '''Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint.

        Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#exceed_action ComputeSecurityPolicyRuleA#exceed_action}
        '''
        result = self._values.get("exceed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exceed_redirect_options(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA"]:
        '''exceed_redirect_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#exceed_redirect_options ComputeSecurityPolicyRuleA#exceed_redirect_options}
        '''
        result = self._values.get("exceed_redirect_options")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA"], result)

    @builtins.property
    def rate_limit_threshold(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA"]:
        '''rate_limit_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#rate_limit_threshold ComputeSecurityPolicyRuleA#rate_limit_threshold}
        '''
        result = self._values.get("rate_limit_threshold")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRateLimitOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__517ae0201347d559419b0411a9fa4bc30393568baababa6677bc101a8b27b6d8)
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
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#count ComputeSecurityPolicyRuleA#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#interval_sec ComputeSecurityPolicyRuleA#interval_sec}
        '''
        value = ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA(
            count=count, interval_sec=interval_sec
        )

        return typing.cast(None, jsii.invoke(self, "putBanThreshold", [value]))

    @jsii.member(jsii_name="putEnforceOnKeyConfigs")
    def put_enforce_on_key_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60ef09f264e420642506263511c03c94a81b27f34905622199600b9333b0572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnforceOnKeyConfigs", [value]))

    @jsii.member(jsii_name="putExceedRedirectOptions")
    def put_exceed_redirect_options(
        self,
        *,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target ComputeSecurityPolicyRuleA#target}
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#type ComputeSecurityPolicyRuleA#type}
        '''
        value = ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA(
            target=target, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putExceedRedirectOptions", [value]))

    @jsii.member(jsii_name="putRateLimitThreshold")
    def put_rate_limit_threshold(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#count ComputeSecurityPolicyRuleA#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#interval_sec ComputeSecurityPolicyRuleA#interval_sec}
        '''
        value = ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA(
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

    @jsii.member(jsii_name="resetExceedRedirectOptions")
    def reset_exceed_redirect_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExceedRedirectOptions", []))

    @jsii.member(jsii_name="resetRateLimitThreshold")
    def reset_rate_limit_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimitThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="banThreshold")
    def ban_threshold(
        self,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference", jsii.get(self, "banThreshold"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigs")
    def enforce_on_key_configs(
        self,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList":
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList", jsii.get(self, "enforceOnKeyConfigs"))

    @builtins.property
    @jsii.member(jsii_name="exceedRedirectOptions")
    def exceed_redirect_options(
        self,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference", jsii.get(self, "exceedRedirectOptions"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThreshold")
    def rate_limit_threshold(
        self,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference", jsii.get(self, "rateLimitThreshold"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSecInput")
    def ban_duration_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "banDurationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="banThresholdInput")
    def ban_threshold_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA"], jsii.get(self, "banThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="conformActionInput")
    def conform_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conformActionInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigsInput")
    def enforce_on_key_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA"]]], jsii.get(self, "enforceOnKeyConfigsInput"))

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
    @jsii.member(jsii_name="exceedRedirectOptionsInput")
    def exceed_redirect_options_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA"], jsii.get(self, "exceedRedirectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThresholdInput")
    def rate_limit_threshold_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA"], jsii.get(self, "rateLimitThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSec")
    def ban_duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "banDurationSec"))

    @ban_duration_sec.setter
    def ban_duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea0ea8fb31a1663b259eb973e0e174b8c5a7c42004d5341710c8a22201d8e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "banDurationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conformAction")
    def conform_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conformAction"))

    @conform_action.setter
    def conform_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe3e1e41a57d010983287acc5c589deab6859c491f3eac4ac76228d7863a9d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conformAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKey")
    def enforce_on_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKey"))

    @enforce_on_key.setter
    def enforce_on_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b3d1c7bb4db0cceced61f1fb35abc046ed389d78c49b2fa944d431f9f2b67f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyName")
    def enforce_on_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyName"))

    @enforce_on_key_name.setter
    def enforce_on_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f214f36c68191382a49aa64f6ac157e0d00c8e73b9732e6d67239d742e5e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exceedAction")
    def exceed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exceedAction"))

    @exceed_action.setter
    def exceed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d93b183f633ce88a627fd176f913c47b44595eed0227c75bbf1c5a9ec37a23d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exceedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c275f8a1d0a807eeead27b982e986ed198276b771c6d3a40a0b4f8145a542738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#count ComputeSecurityPolicyRuleA#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#interval_sec ComputeSecurityPolicyRuleA#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e8f33aef11460c1cd6d3f46ca83d615ed19ed15806843a10527b0fc4683c31)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#count ComputeSecurityPolicyRuleA#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_sec(self) -> typing.Optional[jsii.Number]:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#interval_sec ComputeSecurityPolicyRuleA#interval_sec}
        '''
        result = self._values.get("interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28b7be881b50a12ec335a13ed247f11526bbf671bd5e40e1aebdb64c70220c6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c0351b3d9145548c9bb6167e227c11dde4138177a3b87efe88bc0673268dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f193cc4b031313cb6f921a37efad1b3a86f9b862e5c725e6200599bfe2d65c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8c3b4dd0fb0b4b5a17800b68f58866f14a969306891457c854523ccd02a53d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA",
    jsii_struct_bases=[],
    name_mapping={
        "enforce_on_key_name": "enforceOnKeyName",
        "enforce_on_key_type": "enforceOnKeyType",
    },
)
class ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA:
    def __init__(
        self,
        *,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        enforce_on_key_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_name ComputeSecurityPolicyRuleA#enforce_on_key_name}
        :param enforce_on_key_type: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKeyConfigs" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_type ComputeSecurityPolicyRuleA#enforce_on_key_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3df9160c9de23d39ccc95e205dc890ef3dd796ba8838e6ced551cd43075926)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_name ComputeSecurityPolicyRuleA#enforce_on_key_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#enforce_on_key_type ComputeSecurityPolicyRuleA#enforce_on_key_type}
        '''
        result = self._values.get("enforce_on_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12ef1a02e7c2aacaf4edfe1d1fb91da6e3d947f61b308cdb05d619078f4cb44a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b978d96e352cccc36996f4466747311ae0fdda8c6bb34110dd686c964655b14)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a87d7e550dfd008c873e8c935e4c2d27d0264cc159aa4aa709c4e1bbc9905f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24f79f44495e6250ee7d2150e988e469845ab5006d9861b28a0023f480d53fcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d09bfb4fa620486b87d8c849a2064b81961d9eb06f332b127e1d486801b2b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebdea887a0c2b5abe4e49a8b4fc096af3961a6600b8f7afdd3fef44aa94318dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aec07837944019f918c39081b44e52d09d88751a379ddf2978437fb7a47cc99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c42ee6b1b68b688c25cc28d53032899f85b93752246fe76856c60c129b57dcb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyType")
    def enforce_on_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyType"))

    @enforce_on_key_type.setter
    def enforce_on_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871718bf41aace8f34159f001caa55ff8538d3a2376989ff1b13d416c652c232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a144615cb747f9a4b648ccdf3b12cab08aff4c51b3e0f0024c25bca184a358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "type": "type"},
)
class ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA:
    def __init__(
        self,
        *,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target ComputeSecurityPolicyRuleA#target}
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#type ComputeSecurityPolicyRuleA#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1690255bcbfb56dcafbb0c19ccb150c61ee20fd8755313a606a6c2f1ebfeaaca)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target is not None:
            self._values["target"] = target
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target ComputeSecurityPolicyRuleA#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of the redirect action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#type ComputeSecurityPolicyRuleA#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5403c904cb982f3903081d1481c881cea599d93600d5e510982783f68fb00883)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfba1caa7be9054d2a44a745e5880b54640f7f479eb5efe566ecd455b9e08cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afa41225184bf503392e5306ebf89b8d20f04377ae47aa62f4fa2defd356c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a67d7405370de76e8190a0249fb37b6267cbbd5009498f439340edbca99fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#count ComputeSecurityPolicyRuleA#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#interval_sec ComputeSecurityPolicyRuleA#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52aeb2c5edf02c0882bb6d3d7862522981a2abc162aebd87cc462699b0cf4a98)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#count ComputeSecurityPolicyRuleA#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_sec(self) -> typing.Optional[jsii.Number]:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#interval_sec ComputeSecurityPolicyRuleA#interval_sec}
        '''
        result = self._values.get("interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3610558c12f590f37a281c96014316b816ea4ecaee6f280522887c8ed991e29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16f8227e521b0a5f7c389cb2dbd59baf93b99cc61f8f4575c1d169d482e5beed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1f84769e3fabb1050a5f222d5574eed1997d8a2cb2c2021e2d2db5e9e8e671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb6d9685b51ca85dff9cfc54a548096c74cb988df9270a7b93df8f0c462c137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRedirectOptionsA",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "type": "type"},
)
class ComputeSecurityPolicyRuleRedirectOptionsA:
    def __init__(
        self,
        *,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target ComputeSecurityPolicyRuleA#target}
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#type ComputeSecurityPolicyRuleA#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a77d8de000ebca418aec76fc6c779d1667ce9fcc7de2c902d9c386f060dcd86)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target is not None:
            self._values["target"] = target
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#target ComputeSecurityPolicyRuleA#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of the redirect action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#type ComputeSecurityPolicyRuleA#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRedirectOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRedirectOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleRedirectOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fd15c46411f1f2c50c47de3ff3366f1d2b2ecc44482baf9dcb18f3e770a250c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf2b155790a952157b68d8ed935626b5f89bcaaaf39e43867f41b42e5ff9151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4190e17a367ea48b23e0ab02c60086654b28edad0804de05dd76ac7327e3829f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRedirectOptionsA]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRedirectOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRedirectOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df670b3bb73fe17ce9e8d4cdc1903e8bdf84c4fb21e0aa0f592638437bd1eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeSecurityPolicyRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#create ComputeSecurityPolicyRuleA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#delete ComputeSecurityPolicyRuleA#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#update ComputeSecurityPolicyRuleA#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1451b3be5e8eb523da1c8fa8732c563b6d6965b83437a91328a7d4afa212590c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#create ComputeSecurityPolicyRuleA#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#delete ComputeSecurityPolicyRuleA#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy_rule#update ComputeSecurityPolicyRuleA#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicyRule.ComputeSecurityPolicyRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__467e9ddd2bf1ce7c180d84633a87d37313a6d142846a6ccb0f9bb0573ea0839f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82a0c250ae1627bec651aa94658b8e7f5677456ea10292ffbc23c9b53e4cc219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf53ee5c247b3610d52ff7d8dd0c8266bb9f50e0fdca4b0f286fb787bac87c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0410ee830d131ed6cb7da46da729b0516e7ad812b870a1bdd93d49a76b05a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ced097535d29ae8f817736f3ee232479bb26acf36adc4f5559599ba5402655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeSecurityPolicyRuleA",
    "ComputeSecurityPolicyRuleAConfig",
    "ComputeSecurityPolicyRuleHeaderActionA",
    "ComputeSecurityPolicyRuleHeaderActionAOutputReference",
    "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA",
    "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList",
    "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference",
    "ComputeSecurityPolicyRuleMatchA",
    "ComputeSecurityPolicyRuleMatchAOutputReference",
    "ComputeSecurityPolicyRuleMatchConfigA",
    "ComputeSecurityPolicyRuleMatchConfigAOutputReference",
    "ComputeSecurityPolicyRuleMatchExprA",
    "ComputeSecurityPolicyRuleMatchExprAOutputReference",
    "ComputeSecurityPolicyRuleMatchExprOptionsA",
    "ComputeSecurityPolicyRuleMatchExprOptionsAOutputReference",
    "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA",
    "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigA",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptionsA",
    "ComputeSecurityPolicyRuleRateLimitOptionsAOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA",
    "ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA",
    "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList",
    "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA",
    "ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA",
    "ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference",
    "ComputeSecurityPolicyRuleRedirectOptionsA",
    "ComputeSecurityPolicyRuleRedirectOptionsAOutputReference",
    "ComputeSecurityPolicyRuleTimeouts",
    "ComputeSecurityPolicyRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__691f7fcc7d22a9e12d0f0baadf49d6abcd3ba135731c4245351c0262fa8b3fde(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    priority: jsii.Number,
    security_policy: builtins.str,
    description: typing.Optional[builtins.str] = None,
    header_action: typing.Optional[typing.Union[ComputeSecurityPolicyRuleHeaderActionA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchA, typing.Dict[builtins.str, typing.Any]]] = None,
    preconfigured_waf_config: typing.Optional[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limit_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRedirectOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeSecurityPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fa84346c8250fe4aa3cb3a595f9ecdb997e3fad4998ab8605aeb2a892f236b36(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0494db04cb5b1f1caeb403ab3d889b55e48eea59cc56416223ae312cb5fcf73d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1184b3c648b0898eac47d0b8ffa6df9229cb50e4cedb33f6077418976f6bb1fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b173ad9c43ba279beb002ec1b70ce9afcbb424915397ae9333f1c56cb5f566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1a6ca95315f3d93af6a43694e4312cb281fba62b4105a59d6949d2c1651b1b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b83a45982f4dd220ccf728ccf32e3283d2530568395a232756338e0f720026(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2708c45644fe79b7c84f86b351ed589155d2586c6e08c2ac87c83bb009e7a665(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9357b6cb3d30ccbe9167f3e9a51317c20986025ffea9c25383185ddda1defbe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4262c59dde9bd7ab66c95d422d2fce00e6ef6259eff20144ed8cd410969c5f6(
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
    security_policy: builtins.str,
    description: typing.Optional[builtins.str] = None,
    header_action: typing.Optional[typing.Union[ComputeSecurityPolicyRuleHeaderActionA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchA, typing.Dict[builtins.str, typing.Any]]] = None,
    preconfigured_waf_config: typing.Optional[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limit_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRedirectOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeSecurityPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644ccddb690dfb75550d500f55b473f2805ab9af079362944a83dbaa5feeb776(
    *,
    request_headers_to_adds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6414801bf9841e0034c714273bdf10735d2bcf27355e862a889506ecdf1fa5ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f799705f538dd525f74be2dbe657c1384a630bf6185276078cd666ab8ca22a47(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a4f3eea02bc7f92b646e81da59d013c601f99102300db17846591e89f2f013(
    value: typing.Optional[ComputeSecurityPolicyRuleHeaderActionA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0ae89b8c20313dbf35e6b74e69fd6cbf332a4828b8ad60e189407f16395830(
    *,
    header_name: typing.Optional[builtins.str] = None,
    header_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f19f2117204b5d3f6f0f1f23935ee3c2e177dfc32ad2f0a62ce59ce61e5ca9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf4351cc93632a889abd80390c269973bdfff3883eed245548faaed7747814e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b2edd4b86c68e0d346c4fd440b850188621cfd5723f319a9b20d572f256aca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c0b473212d8684289ec858bc8fba915c89815be1fa790e03702928c1157926(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6312b7ed790415d442e46a1bb06344729e0242b014e23cc1e5a3a4df476714e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d846ac2ca4943b2bbdf77c1d57de26cd26a789dd2bee455054a6f950fdbde1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a888a9da899c8f0cdd68cc4fd91bc5b379f204c194461fe93e5b320e2a0c1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace213b7d47aee07733d03ddb64766c217cd040e66ba6ad0e06d37a6aef308b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af97b8d109d0300ad9e7ec227885213cbc012014470559e6a3d522e4c4622c0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a271c7373fbf811af842fbf47ab0ef787638c3e825ff3a43e676a862fb953ba6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65174d8f91f150dcac58e1d728372be3b0633231ede5bdd54ea57b7f7df2165c(
    *,
    config: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    expr: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchExprA, typing.Dict[builtins.str, typing.Any]]] = None,
    expr_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchExprOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    versioned_expr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3cf7ec571d9282573fd4c4c528c1177fc318faeee54c39fb28eedd1b34acacc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59647a7baa9c1256980a903143cc704b556bc779dc5a6b64ccf48afe0903b676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840439d5051bc274b962eb072c1e27b16c24f61551a3a4c618ac5808980e27e4(
    value: typing.Optional[ComputeSecurityPolicyRuleMatchA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b6ab2577b3c54368655c6d34d83d27c17c78d97c419cb239e85ca822397f13(
    *,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b04cc9efd64a083969f0780ec78860ce7e37eb4fa1fb1c0f601a36bc49884d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b67d93a953c4a841fee0257bd3fc80202e01d42b4ae546e1dc41981a4314b6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b50d2d9301f0976b51e0501aa539e2fbe9b29772586a12f66c8fe7e0ebf4e4(
    value: typing.Optional[ComputeSecurityPolicyRuleMatchConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4e1bab806a7c61d681ea6878e985e466a1c79c4e8c7af3d0664434a0ae4256(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9ceda20ac2988a4e62cebf98e9148fda21535ad47e8d8a0398f4809f2212bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2740bf3d2a484c57d599f7f9bbc0728459f8d871bb93ab3f48e6e4de9862b6ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b9e433e9c35e26a16d8b5b438d8575cf8e1424bff1cb1c8f02e80bfc57a96a(
    value: typing.Optional[ComputeSecurityPolicyRuleMatchExprA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055bf2d0d71f440aa828c41c8a4b4e22a07285e5d79ca34e7394305233e5b60d(
    *,
    recaptcha_options: typing.Union[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8858b9b4ebb3761b6ef83756ff82ecfe5bb019170a0ec7c422451c940d1e95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a45ed025a064552c9bd4755e6ce04a1f882ff85380f62c326969858a43cc2d(
    value: typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7abf57ca54b23bd0ffd27b075c465845cf1994307e7a784fab7f68c2e30c8a(
    *,
    action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432bcd1f8ad5cce52f6af6803e9e39dc45e0447d3078d93f6ae264c77b9fe1df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a516228e6148beff957229ec7bb2533c546e034098e6b2e40bce5a8d6350ef31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b062e24842185c2638e781f43a43d6d839772c897a5812513a70fdad9632037d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1932c30d6536ac49bb7dd8c62fbeb21b6767c86a490bda27f190faac015cf494(
    value: typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287cdc7356f3874f4dbfaeb3817aaf722133bb1598f2df3204b56470de15879c(
    *,
    exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa0f7e8d6c804130e379130f363cdfede1d769ec08fd9666f71b66ff697867d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84df2ba8ad77d0e8804eb761da07549dd9e095e490d1c1ddfe0e9c5cde370a1b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643f99851738649af5f219baf57e0d192fa27dcbabcf394cb2dd905846c1b3f5(
    value: typing.Optional[ComputeSecurityPolicyRulePreconfiguredWafConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09409a0f88a17f93a4326bae5a8ef8470a7dd50a5692284fa20ee7506bc5ddde(
    *,
    target_rule_set: builtins.str,
    request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b202d111e19e31c2ac121a27313719b0b1e697d41326cda9ca29aa1d49de2a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296c4542722baf33f688ce68d8d2028d9301b0f234f447f46c2c421e60d13013(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fa88ae0a95e9c3afb121517273a6f18ea5fac26aa0c1b9fdf44e627b6284d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07430d878704b3f3ff15e77baf3a989e3704ce0e97df0f41762e77022256dc6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c4a8d0a8b440e4bbfc4f72f69ad3dd096a5f8a1bffe9df45cf8614e30d517a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9015ece2390ae9d603ff285331a25363b6de83eedbea406a927bef9346a04d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e0088add0a270fe20321b28ad8f24b5f7c827fa99b33222086fbd20d8bb9ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3caca70ac27a66db48f7f29173622dc21806067f7a90167d86498c4d7bdb666(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd02fb8aea3cb9fd3fe9606d711f4345d84a9835ecb087ebd34323a6cd095280(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b84a56d33da4c2d576b9596184b0640f3dabb5fb51a6ae697b72e30f104c52(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bb76abd048a1c8700da7e8fc4969c9e3f22942e5a4e5dfe611543cccfd63ae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89743f6899d2b8d0fa3bf513a75d87e5187db5a662f0e8a3f61696f3741e5509(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813acd9c72c844a825a23e3b02a9f5be70cae6e3b812867c79a0e679714895ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63da5b3dfbb01af917392fd4c9fc05ba4d120b15fab476c5afec68738c5ee682(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db067c5d08346c23f6bbbbdcfbf3fb35fc6cc09f54c0a6b8db684a1a9db576fe(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55377edfbf161e5c77455fae3f835d543684ea9a4f2657e1311b4fc6839efde0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bab36c5717530189eda20dcea864d796a2182a6e8261e9adb2c80a0395dd40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f503e61edfab201d1d967e2303ad11c53e83ab1c12aae68adb57704712490b3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5081d5b9a9bd2a89387fbe90d35e386f5e7182efcfa8d06f6e1262403cbb7b35(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12bd4634d221c48ef8372a9e9ddd972859a295d592f061031ee9558280684982(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356105e0859e0a99b35e88fb9df5da70e42e286c638d5dac5544e253e76e3ebf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6bf8a0d27e2b4047f9bf9cff8bc10282a301cb9b6f5cb058348966681af62d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a218eaa2438220fa65371c6ac76fcb586e8b5195ba7d5678a37ec365b226113f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a200a05bdd6f54de4b13fc0ed9a9279ba98225cad3be98834d354da2d8e38f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e29762ce9d3dc301e7edf9ba9a37d13dbd6a3919999609e77ea6d9c69b9921(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae7bc0990449cf71bfefe77791700f41011eced3eb80e50bbc9a777e483660c(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45369b30e58ec9b5c865d653299402f79bc002b892ba4445da7eb48340afbeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186a0a443a7d4b449921ed43e81c20b7d1ca24a6efee168e1ae71fcf9049ba80(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b728d4bf212d75fbcea712de2ba6e07d083aaed2cabccccdd6d67ddabf3d5b80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efd23210a5e7449f28916883895cd8e63841040ea458104ceb838c813c08bbf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264db8637e4fc3e0916ec45dbc0f87d703937ead026e4f4891488a7a538b5f65(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95de6e99920d6ab28d5bfeeb0e8dce0a43a9ae316c1342cd3fec81097db477b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a599fa62e8acd45e5644dee0d291ee4b5b830b816baaa6d5a6dc04992a4cdde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c295e5092696ce0c9e56cf08c5654ffb3a5d5a11cae262595eb3fda8213e55e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e34db4f849ef25763e1c3cb2c3832f4b745b08f11cf7bd1110146e3cb9aea0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64d7ea80da1795fc714da6fabbf6edc6ebdd22fbbedcae35a9ec72393fbd1f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f34494ccd8587d872a433afa9e2016768a09fbaf691a30ea885c7264c36d411(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75eb7593479966ac6cc22a640c54d53b1839569c81f6a894a90ccdae8dbbbd34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d81f6e3e62e2028da08f470daa35ebff8d71165a779c264e5cea67c8d282d5d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a018dfcc32fd65adb259403130ed58ffbf517e484a22fb4db26ec215ecbc86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7962affac43a89fcb906f2f50d3c06b50aad5a85773a8813698e27c25b9baa1d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84021e429dd72c0e695d4f194d2ec2bc1fa62860935fc8a403040db86dda2c79(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271fdfc52bb31c9f9991fdfaf1961c495bc2ba01bcc63c5c19c61e3dd406a245(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742c3132b9ff76726494e005f22a2861c53fa17cb86d6063a3f98f517cc6b795(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42afffd1c48bb6cb48e6b34afa3ee2148ec0a9057d50f285398bd8ce14d86fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d142437ee82d4f8e54282f907785485c72786a342605054dc3eda05d255b663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b04b6144189e06ab28f15faec46d875444da006b0ea0a48adbf91286302317(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fb2f4fa2932fa6c1bfe96f550fa1254b2224e3f39c49d3854ef302cf981a42(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d858314efc59b10be227257146650d63f9127c0b79030527aeba334a19eb9578(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb879b177870f3d564015ac02aa5ded720a34bd7560e7c858d8eb48d340835f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11e5b51acd4b2881c3c0bce3a885e3bea20b683daf79c57a2858b10e3a42840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7155166d0318390c2d4fd5d20158bca35ee128024571d4ba3f127d836f26d9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d305b1f995be8435c9ffc8920937e3dee62b19986edef54e602f1990e045ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcdbb97ecc7f593d19fc676f814f6e4a4fbc782ffafaf6ce30e5d4dc94ba68d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f033e73bfb4f196c94ce50375495309c74298933221bc841f94749d23ccfbc85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af66c73a72fb3f2e26ca59ebaa3844410ae7a9366da089ac55a13af4faeec01b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6c8ca73c17e37a87e00ef6444e10e36dc23ccf07cbada90a19fff90e22518c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e8811f458a717fb1c36a03e540f7ac2df49d31e2e25a0ca752cbaadd81c8fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79ab185097daf9e58182b59b3b5ca352314fb25cf6100f6cc5e721e8b36aeec(
    *,
    ban_duration_sec: typing.Optional[jsii.Number] = None,
    ban_threshold: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA, typing.Dict[builtins.str, typing.Any]]] = None,
    conform_action: typing.Optional[builtins.str] = None,
    enforce_on_key: typing.Optional[builtins.str] = None,
    enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    exceed_action: typing.Optional[builtins.str] = None,
    exceed_redirect_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    rate_limit_threshold: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517ae0201347d559419b0411a9fa4bc30393568baababa6677bc101a8b27b6d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60ef09f264e420642506263511c03c94a81b27f34905622199600b9333b0572(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea0ea8fb31a1663b259eb973e0e174b8c5a7c42004d5341710c8a22201d8e60(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe3e1e41a57d010983287acc5c589deab6859c491f3eac4ac76228d7863a9d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b3d1c7bb4db0cceced61f1fb35abc046ed389d78c49b2fa944d431f9f2b67f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f214f36c68191382a49aa64f6ac157e0d00c8e73b9732e6d67239d742e5e07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d93b183f633ce88a627fd176f913c47b44595eed0227c75bbf1c5a9ec37a23d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c275f8a1d0a807eeead27b982e986ed198276b771c6d3a40a0b4f8145a542738(
    value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e8f33aef11460c1cd6d3f46ca83d615ed19ed15806843a10527b0fc4683c31(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b7be881b50a12ec335a13ed247f11526bbf671bd5e40e1aebdb64c70220c6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c0351b3d9145548c9bb6167e227c11dde4138177a3b87efe88bc0673268dac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f193cc4b031313cb6f921a37efad1b3a86f9b862e5c725e6200599bfe2d65c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8c3b4dd0fb0b4b5a17800b68f58866f14a969306891457c854523ccd02a53d(
    value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3df9160c9de23d39ccc95e205dc890ef3dd796ba8838e6ced551cd43075926(
    *,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    enforce_on_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ef1a02e7c2aacaf4edfe1d1fb91da6e3d947f61b308cdb05d619078f4cb44a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b978d96e352cccc36996f4466747311ae0fdda8c6bb34110dd686c964655b14(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a87d7e550dfd008c873e8c935e4c2d27d0264cc159aa4aa709c4e1bbc9905f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f79f44495e6250ee7d2150e988e469845ab5006d9861b28a0023f480d53fcf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d09bfb4fa620486b87d8c849a2064b81961d9eb06f332b127e1d486801b2b29(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdea887a0c2b5abe4e49a8b4fc096af3961a6600b8f7afdd3fef44aa94318dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aec07837944019f918c39081b44e52d09d88751a379ddf2978437fb7a47cc99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42ee6b1b68b688c25cc28d53032899f85b93752246fe76856c60c129b57dcb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871718bf41aace8f34159f001caa55ff8538d3a2376989ff1b13d416c652c232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a144615cb747f9a4b648ccdf3b12cab08aff4c51b3e0f0024c25bca184a358(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1690255bcbfb56dcafbb0c19ccb150c61ee20fd8755313a606a6c2f1ebfeaaca(
    *,
    target: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5403c904cb982f3903081d1481c881cea599d93600d5e510982783f68fb00883(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfba1caa7be9054d2a44a745e5880b54640f7f479eb5efe566ecd455b9e08cca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afa41225184bf503392e5306ebf89b8d20f04377ae47aa62f4fa2defd356c01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a67d7405370de76e8190a0249fb37b6267cbbd5009498f439340edbca99fa8(
    value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52aeb2c5edf02c0882bb6d3d7862522981a2abc162aebd87cc462699b0cf4a98(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3610558c12f590f37a281c96014316b816ea4ecaee6f280522887c8ed991e29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f8227e521b0a5f7c389cb2dbd59baf93b99cc61f8f4575c1d169d482e5beed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1f84769e3fabb1050a5f222d5574eed1997d8a2cb2c2021e2d2db5e9e8e671(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb6d9685b51ca85dff9cfc54a548096c74cb988df9270a7b93df8f0c462c137(
    value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a77d8de000ebca418aec76fc6c779d1667ce9fcc7de2c902d9c386f060dcd86(
    *,
    target: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd15c46411f1f2c50c47de3ff3366f1d2b2ecc44482baf9dcb18f3e770a250c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf2b155790a952157b68d8ed935626b5f89bcaaaf39e43867f41b42e5ff9151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4190e17a367ea48b23e0ab02c60086654b28edad0804de05dd76ac7327e3829f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df670b3bb73fe17ce9e8d4cdc1903e8bdf84c4fb21e0aa0f592638437bd1eef(
    value: typing.Optional[ComputeSecurityPolicyRuleRedirectOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1451b3be5e8eb523da1c8fa8732c563b6d6965b83437a91328a7d4afa212590c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467e9ddd2bf1ce7c180d84633a87d37313a6d142846a6ccb0f9bb0573ea0839f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a0c250ae1627bec651aa94658b8e7f5677456ea10292ffbc23c9b53e4cc219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf53ee5c247b3610d52ff7d8dd0c8266bb9f50e0fdca4b0f286fb787bac87c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0410ee830d131ed6cb7da46da729b0516e7ad812b870a1bdd93d49a76b05a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ced097535d29ae8f817736f3ee232479bb26acf36adc4f5559599ba5402655(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
