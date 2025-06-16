r'''
# `google_compute_security_policy_rule`

Refer to the Terraform Registry for docs: [`google_compute_security_policy_rule`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule).
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


class GoogleComputeSecurityPolicyRuleA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleA",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule google_compute_security_policy_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        priority: jsii.Number,
        security_policy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        header_action: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleHeaderActionA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchA", typing.Dict[builtins.str, typing.Any]]] = None,
        preconfigured_waf_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limit_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRedirectOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule google_compute_security_policy_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: The Action to perform when the rule is matched. The following are the valid actions:. - allow: allow access to target. - deny(STATUS): deny access to target, returns the HTTP response code specified. Valid values for STATUS are 403, 404, and 502. - rate_based_ban: limit client traffic to the configured threshold and ban the client if the traffic exceeds the threshold. Configure parameters for this action in RateLimitOptions. Requires rateLimitOptions to be set. - redirect: redirect to a different target. This can either be an internal reCAPTCHA redirect, or an external URL-based redirect via a 302 response. Parameters for this action can be configured via redirectOptions. This action is only supported in Global Security Policies of type CLOUD_ARMOR. - throttle: limit client traffic to the configured threshold. Configure parameters for this action in rateLimitOptions. Requires rateLimitOptions to be set for this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#action GoogleComputeSecurityPolicyRuleA#action}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#priority GoogleComputeSecurityPolicyRuleA#priority}
        :param security_policy: The name of the security policy this rule belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#security_policy GoogleComputeSecurityPolicyRuleA#security_policy}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#description GoogleComputeSecurityPolicyRuleA#description}
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#header_action GoogleComputeSecurityPolicyRuleA#header_action}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#id GoogleComputeSecurityPolicyRuleA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#match GoogleComputeSecurityPolicyRuleA#match}
        :param preconfigured_waf_config: preconfigured_waf_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#preconfigured_waf_config GoogleComputeSecurityPolicyRuleA#preconfigured_waf_config}
        :param preview: If set to true, the specified action is not enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#preview GoogleComputeSecurityPolicyRuleA#preview}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#project GoogleComputeSecurityPolicyRuleA#project}.
        :param rate_limit_options: rate_limit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#rate_limit_options GoogleComputeSecurityPolicyRuleA#rate_limit_options}
        :param redirect_options: redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#redirect_options GoogleComputeSecurityPolicyRuleA#redirect_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#timeouts GoogleComputeSecurityPolicyRuleA#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc93a95ffa3cd8b3e3cafcc3b516db97865213392dab0c1d9603ea730aa5eee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeSecurityPolicyRuleAConfig(
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
        '''Generates CDKTF code for importing a GoogleComputeSecurityPolicyRuleA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeSecurityPolicyRuleA to import.
        :param import_from_id: The id of the existing GoogleComputeSecurityPolicyRuleA that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeSecurityPolicyRuleA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e7b3cd3626cf2fcf89ee32bf9468321fb9f066b84ef780a32919887f142914)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putHeaderAction")
    def put_header_action(
        self,
        *,
        request_headers_to_adds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_headers_to_adds: request_headers_to_adds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_headers_to_adds GoogleComputeSecurityPolicyRuleA#request_headers_to_adds}
        '''
        value = GoogleComputeSecurityPolicyRuleHeaderActionA(
            request_headers_to_adds=request_headers_to_adds
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchExprA", typing.Dict[builtins.str, typing.Any]]] = None,
        expr_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchExprOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#config GoogleComputeSecurityPolicyRuleA#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#expr GoogleComputeSecurityPolicyRuleA#expr}
        :param expr_options: expr_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#expr_options GoogleComputeSecurityPolicyRuleA#expr_options}
        :param versioned_expr: Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#versioned_expr GoogleComputeSecurityPolicyRuleA#versioned_expr}
        '''
        value = GoogleComputeSecurityPolicyRuleMatchA(
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
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#exclusion GoogleComputeSecurityPolicyRuleA#exclusion}
        '''
        value = GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA(
            exclusion=exclusion
        )

        return typing.cast(None, jsii.invoke(self, "putPreconfiguredWafConfig", [value]))

    @jsii.member(jsii_name="putRateLimitOptions")
    def put_rate_limit_options(
        self,
        *,
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA", typing.Dict[builtins.str, typing.Any]]] = None,
        conform_action: typing.Optional[builtins.str] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_action: typing.Optional[builtins.str] = None,
        exceed_redirect_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        rate_limit_threshold: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#ban_duration_sec GoogleComputeSecurityPolicyRuleA#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#ban_threshold GoogleComputeSecurityPolicyRuleA#ban_threshold}
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#conform_action GoogleComputeSecurityPolicyRuleA#conform_action}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key GoogleComputeSecurityPolicyRuleA#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_configs GoogleComputeSecurityPolicyRuleA#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_name GoogleComputeSecurityPolicyRuleA#enforce_on_key_name}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint. Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#exceed_action GoogleComputeSecurityPolicyRuleA#exceed_action}
        :param exceed_redirect_options: exceed_redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#exceed_redirect_options GoogleComputeSecurityPolicyRuleA#exceed_redirect_options}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#rate_limit_threshold GoogleComputeSecurityPolicyRuleA#rate_limit_threshold}
        '''
        value = GoogleComputeSecurityPolicyRuleRateLimitOptionsA(
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
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target GoogleComputeSecurityPolicyRuleA#target}
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#type GoogleComputeSecurityPolicyRuleA#type}
        '''
        value = GoogleComputeSecurityPolicyRuleRedirectOptionsA(
            target=target, type=type
        )

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#create GoogleComputeSecurityPolicyRuleA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#delete GoogleComputeSecurityPolicyRuleA#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#update GoogleComputeSecurityPolicyRuleA#update}.
        '''
        value = GoogleComputeSecurityPolicyRuleTimeouts(
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
    def header_action(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleHeaderActionAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleHeaderActionAOutputReference", jsii.get(self, "headerAction"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> "GoogleComputeSecurityPolicyRuleMatchAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleMatchAOutputReference", jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfig")
    def preconfigured_waf_config(
        self,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference", jsii.get(self, "preconfiguredWafConfig"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitOptions")
    def rate_limit_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsAOutputReference", jsii.get(self, "rateLimitOptions"))

    @builtins.property
    @jsii.member(jsii_name="redirectOptions")
    def redirect_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleRedirectOptionsAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleRedirectOptionsAOutputReference", jsii.get(self, "redirectOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeSecurityPolicyRuleTimeoutsOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleHeaderActionA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleHeaderActionA"], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchA"], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfigInput")
    def preconfigured_waf_config_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA"], jsii.get(self, "preconfiguredWafConfigInput"))

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
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsA"], jsii.get(self, "rateLimitOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectOptionsInput")
    def redirect_options_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRedirectOptionsA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRedirectOptionsA"], jsii.get(self, "redirectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPolicyInput")
    def security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeSecurityPolicyRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeSecurityPolicyRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef55439734609d5b4b0d84ced394d0c9e7f10011d2cfdac998219d56641e925d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc0eb4464e4a0b2b50147a19b33e8fa5a3a21713a39062767e641eb3487042f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39516fa6434b92668693ff6834d2ead2f67e11a3b94ffc0fb8a2beb8acb84f67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__081d5d619f749a7aef935735f49d4ee838b21bdeccb1d951b0892d2f37d61473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preview", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e379040931f34bde3d29788cb1142e4bc14cbf0dff49287f98d11aa8f6c93e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842a2d956af97f39623d915194e272961b8e3531d4f91b8949247a07a21c2b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicy")
    def security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicy"))

    @security_policy.setter
    def security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e5e2830e67cfd7478c09d9d7ed5c587e3cc87e7fee0eb4cb97a083795c9750a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleAConfig",
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
class GoogleComputeSecurityPolicyRuleAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        header_action: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleHeaderActionA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchA", typing.Dict[builtins.str, typing.Any]]] = None,
        preconfigured_waf_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limit_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRedirectOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: The Action to perform when the rule is matched. The following are the valid actions:. - allow: allow access to target. - deny(STATUS): deny access to target, returns the HTTP response code specified. Valid values for STATUS are 403, 404, and 502. - rate_based_ban: limit client traffic to the configured threshold and ban the client if the traffic exceeds the threshold. Configure parameters for this action in RateLimitOptions. Requires rateLimitOptions to be set. - redirect: redirect to a different target. This can either be an internal reCAPTCHA redirect, or an external URL-based redirect via a 302 response. Parameters for this action can be configured via redirectOptions. This action is only supported in Global Security Policies of type CLOUD_ARMOR. - throttle: limit client traffic to the configured threshold. Configure parameters for this action in rateLimitOptions. Requires rateLimitOptions to be set for this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#action GoogleComputeSecurityPolicyRuleA#action}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#priority GoogleComputeSecurityPolicyRuleA#priority}
        :param security_policy: The name of the security policy this rule belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#security_policy GoogleComputeSecurityPolicyRuleA#security_policy}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#description GoogleComputeSecurityPolicyRuleA#description}
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#header_action GoogleComputeSecurityPolicyRuleA#header_action}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#id GoogleComputeSecurityPolicyRuleA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#match GoogleComputeSecurityPolicyRuleA#match}
        :param preconfigured_waf_config: preconfigured_waf_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#preconfigured_waf_config GoogleComputeSecurityPolicyRuleA#preconfigured_waf_config}
        :param preview: If set to true, the specified action is not enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#preview GoogleComputeSecurityPolicyRuleA#preview}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#project GoogleComputeSecurityPolicyRuleA#project}.
        :param rate_limit_options: rate_limit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#rate_limit_options GoogleComputeSecurityPolicyRuleA#rate_limit_options}
        :param redirect_options: redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#redirect_options GoogleComputeSecurityPolicyRuleA#redirect_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#timeouts GoogleComputeSecurityPolicyRuleA#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(header_action, dict):
            header_action = GoogleComputeSecurityPolicyRuleHeaderActionA(**header_action)
        if isinstance(match, dict):
            match = GoogleComputeSecurityPolicyRuleMatchA(**match)
        if isinstance(preconfigured_waf_config, dict):
            preconfigured_waf_config = GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA(**preconfigured_waf_config)
        if isinstance(rate_limit_options, dict):
            rate_limit_options = GoogleComputeSecurityPolicyRuleRateLimitOptionsA(**rate_limit_options)
        if isinstance(redirect_options, dict):
            redirect_options = GoogleComputeSecurityPolicyRuleRedirectOptionsA(**redirect_options)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeSecurityPolicyRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ee6646e8514f872b6e4a21c13ec545392f08fbb20082d609bcde1bac1dce9f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#action GoogleComputeSecurityPolicyRuleA#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An integer indicating the priority of a rule in the list.

        The priority must be a positive value between 0 and 2147483647.
        Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#priority GoogleComputeSecurityPolicyRuleA#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def security_policy(self) -> builtins.str:
        '''The name of the security policy this rule belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#security_policy GoogleComputeSecurityPolicyRuleA#security_policy}
        '''
        result = self._values.get("security_policy")
        assert result is not None, "Required property 'security_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#description GoogleComputeSecurityPolicyRuleA#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_action(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleHeaderActionA"]:
        '''header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#header_action GoogleComputeSecurityPolicyRuleA#header_action}
        '''
        result = self._values.get("header_action")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleHeaderActionA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#id GoogleComputeSecurityPolicyRuleA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match(self) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchA"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#match GoogleComputeSecurityPolicyRuleA#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchA"], result)

    @builtins.property
    def preconfigured_waf_config(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA"]:
        '''preconfigured_waf_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#preconfigured_waf_config GoogleComputeSecurityPolicyRuleA#preconfigured_waf_config}
        '''
        result = self._values.get("preconfigured_waf_config")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA"], result)

    @builtins.property
    def preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the specified action is not enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#preview GoogleComputeSecurityPolicyRuleA#preview}
        '''
        result = self._values.get("preview")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#project GoogleComputeSecurityPolicyRuleA#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limit_options(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsA"]:
        '''rate_limit_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#rate_limit_options GoogleComputeSecurityPolicyRuleA#rate_limit_options}
        '''
        result = self._values.get("rate_limit_options")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsA"], result)

    @builtins.property
    def redirect_options(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRedirectOptionsA"]:
        '''redirect_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#redirect_options GoogleComputeSecurityPolicyRuleA#redirect_options}
        '''
        result = self._values.get("redirect_options")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRedirectOptionsA"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeSecurityPolicyRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#timeouts GoogleComputeSecurityPolicyRuleA#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleHeaderActionA",
    jsii_struct_bases=[],
    name_mapping={"request_headers_to_adds": "requestHeadersToAdds"},
)
class GoogleComputeSecurityPolicyRuleHeaderActionA:
    def __init__(
        self,
        *,
        request_headers_to_adds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_headers_to_adds: request_headers_to_adds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_headers_to_adds GoogleComputeSecurityPolicyRuleA#request_headers_to_adds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca93e47be9e0e507b8748e151c002f7d6876292f2b85858646954632a7c19479)
            check_type(argname="argument request_headers_to_adds", value=request_headers_to_adds, expected_type=type_hints["request_headers_to_adds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if request_headers_to_adds is not None:
            self._values["request_headers_to_adds"] = request_headers_to_adds

    @builtins.property
    def request_headers_to_adds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA"]]]:
        '''request_headers_to_adds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_headers_to_adds GoogleComputeSecurityPolicyRuleA#request_headers_to_adds}
        '''
        result = self._values.get("request_headers_to_adds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleHeaderActionA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleHeaderActionAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleHeaderActionAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd07eeee031970c0631e11cdc1d43986060b99df729fbc6203f59551559a533)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeadersToAdds")
    def put_request_headers_to_adds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f415c248d2fd4d11bb42c83104946bf0d3b49e4bc6cc23507467a9d591b6dd32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeadersToAdds", [value]))

    @jsii.member(jsii_name="resetRequestHeadersToAdds")
    def reset_request_headers_to_adds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeadersToAdds", []))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAdds")
    def request_headers_to_adds(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList":
        return typing.cast("GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList", jsii.get(self, "requestHeadersToAdds"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAddsInput")
    def request_headers_to_adds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA"]]], jsii.get(self, "requestHeadersToAddsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleHeaderActionA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleHeaderActionA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleHeaderActionA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4da8a2a8ba88093b5bc7bf304469e5b62007f286878f654beb58a42c4c530b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName", "header_value": "headerValue"},
)
class GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA:
    def __init__(
        self,
        *,
        header_name: typing.Optional[builtins.str] = None,
        header_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#header_name GoogleComputeSecurityPolicyRuleA#header_name}
        :param header_value: The value to set the named header to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#header_value GoogleComputeSecurityPolicyRuleA#header_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ced839e3ff4f08fea381143e30911a5a728f410fcf5fa7a9abd3fc3e7b4bf7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#header_name GoogleComputeSecurityPolicyRuleA#header_name}
        '''
        result = self._values.get("header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_value(self) -> typing.Optional[builtins.str]:
        '''The value to set the named header to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#header_value GoogleComputeSecurityPolicyRuleA#header_value}
        '''
        result = self._values.get("header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ab91146eb531fa36abf7f9cad107ba0dc03682abfa44b296bee51fa34d6cba6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c7d30a726978e590e0d1d1d665453a5647ebe29780c3650c767d6bca72b4d6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c5383e5acf732063117567806a16ebed02fa926f5ba2ed0d0d0b972de6c0a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a02cdb90e1a3b1c3b82771954c38ab0ac48baa0ee1c931b60f926b095befcb83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__140ee5e38b5cd02af94c39a91b0ecfdea1723590423444f5763fde6e42217234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82884824a8f29eff60f107af2bc9e24fa2d2b01d4fec89ef583c0b88c583f83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f806fb03b2e5c38f508160c6f132eace676a37dcf6099de8bd4288d9575cab3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cea50b76db20ede3ce02a26e50cbc50fa8d453ce788d8dd1433cf6d6e25cc9d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bda4aebbb320c4fd5f2ff45b4d49ef74e7e0730a3d5a45d20ca29467eddb161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f78141bfaa249e8e0cb82990753716606c7bbac23b8d63d3f1e7e93aa02d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchA",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "expr": "expr",
        "expr_options": "exprOptions",
        "versioned_expr": "versionedExpr",
    },
)
class GoogleComputeSecurityPolicyRuleMatchA:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchExprA", typing.Dict[builtins.str, typing.Any]]] = None,
        expr_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchExprOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#config GoogleComputeSecurityPolicyRuleA#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#expr GoogleComputeSecurityPolicyRuleA#expr}
        :param expr_options: expr_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#expr_options GoogleComputeSecurityPolicyRuleA#expr_options}
        :param versioned_expr: Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#versioned_expr GoogleComputeSecurityPolicyRuleA#versioned_expr}
        '''
        if isinstance(config, dict):
            config = GoogleComputeSecurityPolicyRuleMatchConfigA(**config)
        if isinstance(expr, dict):
            expr = GoogleComputeSecurityPolicyRuleMatchExprA(**expr)
        if isinstance(expr_options, dict):
            expr_options = GoogleComputeSecurityPolicyRuleMatchExprOptionsA(**expr_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1074a85708c3ff12ddd94479bbec723dc47b07962599c97b709cb4e24afbee24)
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
    def config(self) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#config GoogleComputeSecurityPolicyRuleA#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchConfigA"], result)

    @builtins.property
    def expr(self) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprA"]:
        '''expr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#expr GoogleComputeSecurityPolicyRuleA#expr}
        '''
        result = self._values.get("expr")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprA"], result)

    @builtins.property
    def expr_options(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptionsA"]:
        '''expr_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#expr_options GoogleComputeSecurityPolicyRuleA#expr_options}
        '''
        result = self._values.get("expr_options")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptionsA"], result)

    @builtins.property
    def versioned_expr(self) -> typing.Optional[builtins.str]:
        '''Preconfigured versioned expression.

        If this field is specified, config must also be specified.
        Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#versioned_expr GoogleComputeSecurityPolicyRuleA#versioned_expr}
        '''
        result = self._values.get("versioned_expr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatchA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleMatchAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0c652714b48770cd61d30bfa60aaa6eab44bb11306f97bc9d9b3664dac96972)
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
        :param src_ip_ranges: CIDR IP address range. Maximum number of srcIpRanges allowed is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#src_ip_ranges GoogleComputeSecurityPolicyRuleA#src_ip_ranges}
        '''
        value = GoogleComputeSecurityPolicyRuleMatchConfigA(
            src_ip_ranges=src_ip_ranges
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putExpr")
    def put_expr(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#expression GoogleComputeSecurityPolicyRuleA#expression}
        '''
        value = GoogleComputeSecurityPolicyRuleMatchExprA(expression=expression)

        return typing.cast(None, jsii.invoke(self, "putExpr", [value]))

    @jsii.member(jsii_name="putExprOptions")
    def put_expr_options(
        self,
        *,
        recaptcha_options: typing.Union["GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recaptcha_options: recaptcha_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#recaptcha_options GoogleComputeSecurityPolicyRuleA#recaptcha_options}
        '''
        value = GoogleComputeSecurityPolicyRuleMatchExprOptionsA(
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
    def config(self) -> "GoogleComputeSecurityPolicyRuleMatchConfigAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleMatchConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="expr")
    def expr(self) -> "GoogleComputeSecurityPolicyRuleMatchExprAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleMatchExprAOutputReference", jsii.get(self, "expr"))

    @builtins.property
    @jsii.member(jsii_name="exprOptions")
    def expr_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleMatchExprOptionsAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleMatchExprOptionsAOutputReference", jsii.get(self, "exprOptions"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchConfigA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="exprInput")
    def expr_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprA"], jsii.get(self, "exprInput"))

    @builtins.property
    @jsii.member(jsii_name="exprOptionsInput")
    def expr_options_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptionsA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptionsA"], jsii.get(self, "exprOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__46f21730f5fa3c2a7dbde8c149558ce6ffd39c25ed3555d602b0d2c99f3ecded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionedExpr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2caf6d8876020371ca2e81b8a298990dd39282ffea26a3a3349b31214032719a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchConfigA",
    jsii_struct_bases=[],
    name_mapping={"src_ip_ranges": "srcIpRanges"},
)
class GoogleComputeSecurityPolicyRuleMatchConfigA:
    def __init__(
        self,
        *,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param src_ip_ranges: CIDR IP address range. Maximum number of srcIpRanges allowed is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#src_ip_ranges GoogleComputeSecurityPolicyRuleA#src_ip_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d33e0efaef4b0d1896711f88e057b08275dca247757439d0035a8f88d863d4f)
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if src_ip_ranges is not None:
            self._values["src_ip_ranges"] = src_ip_ranges

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of srcIpRanges allowed is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#src_ip_ranges GoogleComputeSecurityPolicyRuleA#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatchConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleMatchConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dafc43a2375c3607eeb3a6f02bcac7c6aa8010e99326afe6c5650bc103db49e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93481ebded63e21d75baca32465397d1e1e81dae5ae84242c8ca7f13e61e0a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfigA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4209abba2b278135d80660df255feda771f3d47c412f71e215c61a138f336dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchExprA",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class GoogleComputeSecurityPolicyRuleMatchExprA:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#expression GoogleComputeSecurityPolicyRuleA#expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__789a15d6d6e833977ffb820e08ef1cdc189999fba20b4e215fee139cd1136a73)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        The application context of the containing message determines which well-known feature set of CEL is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#expression GoogleComputeSecurityPolicyRuleA#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatchExprA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleMatchExprAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchExprAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5adea5023c04e985973c63bd1fee31ab22c318018ac53d7f40ec94c6354fd93e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e9f0b59e217df8516726cb5eedef2ed1029a0053aba220b08ae6e4324117f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe4152202f33b2409a51accdc94741630fb2428c415a1b325948f17ec41ada8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchExprOptionsA",
    jsii_struct_bases=[],
    name_mapping={"recaptcha_options": "recaptchaOptions"},
)
class GoogleComputeSecurityPolicyRuleMatchExprOptionsA:
    def __init__(
        self,
        *,
        recaptcha_options: typing.Union["GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recaptcha_options: recaptcha_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#recaptcha_options GoogleComputeSecurityPolicyRuleA#recaptcha_options}
        '''
        if isinstance(recaptcha_options, dict):
            recaptcha_options = GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA(**recaptcha_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0a8867cc34f5983ff86489fbd795d7e2950d5779437d38da378ac6225e512b)
            check_type(argname="argument recaptcha_options", value=recaptcha_options, expected_type=type_hints["recaptcha_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recaptcha_options": recaptcha_options,
        }

    @builtins.property
    def recaptcha_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA":
        '''recaptcha_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#recaptcha_options GoogleComputeSecurityPolicyRuleA#recaptcha_options}
        '''
        result = self._values.get("recaptcha_options")
        assert result is not None, "Required property 'recaptcha_options' is missing"
        return typing.cast("GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatchExprOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleMatchExprOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchExprOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43fab20a5ba13ec5695e5705462bcb2f7c577ed7e690cc5b03c77cc803ae35f5)
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
        :param action_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA action-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#action_token_site_keys GoogleComputeSecurityPolicyRuleA#action_token_site_keys}
        :param session_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA session-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#session_token_site_keys GoogleComputeSecurityPolicyRuleA#session_token_site_keys}
        '''
        value = GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA(
            action_token_site_keys=action_token_site_keys,
            session_token_site_keys=session_token_site_keys,
        )

        return typing.cast(None, jsii.invoke(self, "putRecaptchaOptions", [value]))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptions")
    def recaptcha_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference", jsii.get(self, "recaptchaOptions"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptionsInput")
    def recaptcha_options_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA"], jsii.get(self, "recaptchaOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79880172444b35fe79b77cc6318f7a6c4396f8ba58fbf2bec5cbe0db75c899c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA",
    jsii_struct_bases=[],
    name_mapping={
        "action_token_site_keys": "actionTokenSiteKeys",
        "session_token_site_keys": "sessionTokenSiteKeys",
    },
)
class GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA:
    def __init__(
        self,
        *,
        action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA action-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#action_token_site_keys GoogleComputeSecurityPolicyRuleA#action_token_site_keys}
        :param session_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA session-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#session_token_site_keys GoogleComputeSecurityPolicyRuleA#session_token_site_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ea02272b51b8b10ce8a26574c5e528d971617a7d028fe4a573b5559abdd70d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#action_token_site_keys GoogleComputeSecurityPolicyRuleA#action_token_site_keys}
        '''
        result = self._values.get("action_token_site_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_token_site_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of site keys to be used during the validation of reCAPTCHA session-tokens.

        The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#session_token_site_keys GoogleComputeSecurityPolicyRuleA#session_token_site_keys}
        '''
        result = self._values.get("session_token_site_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a398397183ee00a1fca5925c216a0f110384a700caad81177b5659dd414fb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5773a25772511bb2928e071a5cc76c7d53ba67fb866a7ee134159d69ff293606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionTokenSiteKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTokenSiteKeys")
    def session_token_site_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sessionTokenSiteKeys"))

    @session_token_site_keys.setter
    def session_token_site_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b180e57671e1551637892fd11c9aae76b6e6845892eb98af215750fe7aff97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTokenSiteKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6cfec65c1e48dc079a7452d6981bf052704feeab3f835226ad8754472a30ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA",
    jsii_struct_bases=[],
    name_mapping={"exclusion": "exclusion"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA:
    def __init__(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#exclusion GoogleComputeSecurityPolicyRuleA#exclusion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8723eded37088a42f66e85e5101b383b7f4d98e3af1baa4e43f0bc1267dd89eb)
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusion is not None:
            self._values["exclusion"] = exclusion

    @builtins.property
    def exclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA"]]]:
        '''exclusion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#exclusion GoogleComputeSecurityPolicyRuleA#exclusion}
        '''
        result = self._values.get("exclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3aa54cb05754658665e93dd785499144a447b178b20e33558f663cd941184ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusion")
    def put_exclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bc03c30eb719ad2f4c7765b14c898ba6269df83808e4ebd15366d6233fd199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusion", [value]))

    @jsii.member(jsii_name="resetExclusion")
    def reset_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusion", []))

    @builtins.property
    @jsii.member(jsii_name="exclusion")
    def exclusion(
        self,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList", jsii.get(self, "exclusion"))

    @builtins.property
    @jsii.member(jsii_name="exclusionInput")
    def exclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA"]]], jsii.get(self, "exclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e5a2f5d242f20f8cf764c90e38b569da27729481f19eb20bab714f24b0d9db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA",
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
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA:
    def __init__(
        self,
        *,
        target_rule_set: builtins.str,
        request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param target_rule_set: Target WAF rule set to apply the preconfigured WAF exclusion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target_rule_set GoogleComputeSecurityPolicyRuleA#target_rule_set}
        :param request_cookie: request_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_cookie GoogleComputeSecurityPolicyRuleA#request_cookie}
        :param request_header: request_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_header GoogleComputeSecurityPolicyRuleA#request_header}
        :param request_query_param: request_query_param block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_query_param GoogleComputeSecurityPolicyRuleA#request_query_param}
        :param request_uri: request_uri block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_uri GoogleComputeSecurityPolicyRuleA#request_uri}
        :param target_rule_ids: A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion. If omitted, it refers to all the rule IDs under the WAF rule set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target_rule_ids GoogleComputeSecurityPolicyRuleA#target_rule_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06eabce8e65c7cf4a877bfa447c468a5a7e652928a95f67ce825b5a9672bd38f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target_rule_set GoogleComputeSecurityPolicyRuleA#target_rule_set}
        '''
        result = self._values.get("target_rule_set")
        assert result is not None, "Required property 'target_rule_set' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_cookie(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA"]]]:
        '''request_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_cookie GoogleComputeSecurityPolicyRuleA#request_cookie}
        '''
        result = self._values.get("request_cookie")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA"]]], result)

    @builtins.property
    def request_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA"]]]:
        '''request_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_header GoogleComputeSecurityPolicyRuleA#request_header}
        '''
        result = self._values.get("request_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA"]]], result)

    @builtins.property
    def request_query_param(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA"]]]:
        '''request_query_param block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_query_param GoogleComputeSecurityPolicyRuleA#request_query_param}
        '''
        result = self._values.get("request_query_param")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA"]]], result)

    @builtins.property
    def request_uri(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA"]]]:
        '''request_uri block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#request_uri GoogleComputeSecurityPolicyRuleA#request_uri}
        '''
        result = self._values.get("request_uri")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA"]]], result)

    @builtins.property
    def target_rule_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion.

        If omitted, it refers to all the rule IDs under the WAF rule set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target_rule_ids GoogleComputeSecurityPolicyRuleA#target_rule_ids}
        '''
        result = self._values.get("target_rule_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__783175a6f3a28408f01532934d89b5ed0a90ab781fb7d0edf504390922cff8d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b3998fbe2845d279003245902289a769233ba6ab08b08c492e5241539b0585)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57749f471976490f3ceff949865ca727004429e5890f7607c6f247448dc0fa85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2b6d503555208adf80339794ae817c28c40ea82b6654a16ea0ea9cc67568c59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05709ff6491f9db861a0568db2239fbd5967714242941bbeee8b843b2bfe70ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1666fbd072343bb8cbab2f768212dbd5fd29434d2b2147479b15b4c1c9cbcfea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9e0ab28ea97cec782cdf6a5bd499d7425bcbbd5c2a5071b30d8b0b45581c158)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRequestCookie")
    def put_request_cookie(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e181fb122e05fa0f7570d917756c1fe53de0abcd7e736ec52f08bedda7338d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestCookie", [value]))

    @jsii.member(jsii_name="putRequestHeader")
    def put_request_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94ac1ddb0cb17cdfe15f6e763176349a13593fecaed7aa943ea013ccc93afc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeader", [value]))

    @jsii.member(jsii_name="putRequestQueryParam")
    def put_request_query_param(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85f028b76006a0865aa199cade4c71ca244df1186c18a86c61ecc77c78c050f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestQueryParam", [value]))

    @jsii.member(jsii_name="putRequestUri")
    def put_request_uri(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f94f4cdc4b2de87244bd71d57202dc531c07bc53f43b2a5f0b1f3aa1f10d37)
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
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList", jsii.get(self, "requestCookie"))

    @builtins.property
    @jsii.member(jsii_name="requestHeader")
    def request_header(
        self,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList", jsii.get(self, "requestHeader"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParam")
    def request_query_param(
        self,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList", jsii.get(self, "requestQueryParam"))

    @builtins.property
    @jsii.member(jsii_name="requestUri")
    def request_uri(
        self,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList", jsii.get(self, "requestUri"))

    @builtins.property
    @jsii.member(jsii_name="requestCookieInput")
    def request_cookie_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA"]]], jsii.get(self, "requestCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderInput")
    def request_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA"]]], jsii.get(self, "requestHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParamInput")
    def request_query_param_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA"]]], jsii.get(self, "requestQueryParamInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriInput")
    def request_uri_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA"]]], jsii.get(self, "requestUriInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__034f9c6d1e978f41eb9bd2e187fc7769f4d7156bf69f0fbb7ef62694afeaeb45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRuleSet")
    def target_rule_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRuleSet"))

    @target_rule_set.setter
    def target_rule_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67f03470cd101a71bc4f6edc0eaa5393fb4f3032cd57e9a765324aa2660a4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5781013fe114241fd8e55266504b5e805a80772177b3aea4c4a8ef39c5205dec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#operator GoogleComputeSecurityPolicyRuleA#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#value GoogleComputeSecurityPolicyRuleA#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee2eccd47fb781c5141b6f0da835907a38c47dd260a252a08bdbf2999fc054e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#operator GoogleComputeSecurityPolicyRuleA#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#value GoogleComputeSecurityPolicyRuleA#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d75296eb4e1de90452b97355760fbac7b03159c4190e9947dab36bb78447bfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2874d6f8d82f17ff96a62802c4d86b074df2354d198038011814e4e1fe40b266)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7512a6ab14f70c0a62a6ba2defe683d25d4adc246f56f63c931456de534c640d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51b06ca7c2e630a35fb257c15c3265cf145454347cb3e50ee60ff6189f1d7a06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d59559af1568ec84f05db1590cdb7c60a2bfe03d0f78d216b4f457015521e723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4ba4077349818eb0a2c86b8b43c8f3c8f0d661b666b34559e3d7f56a8ed41a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f295e3c8e1e44a2bd00c67607f6ee6e004a64fde6965f6caf20e8da143a4a410)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c94c1a03fe924951d183cf61dce7d8268cf28f5bc3278b6639702a528366dc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa299d2efc26c2f3d78f5eaf91e9f12fc35c98dda68f4c0f353c8c72f6296011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50295405ab7eba222b01bf09751e8f931ab9da518e368d5f0645e4b754daced0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#operator GoogleComputeSecurityPolicyRuleA#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#value GoogleComputeSecurityPolicyRuleA#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007c3bf2d9eb054f21f0f7f13c2a61038d4fa5da3a8327b4b0d417c2b000a527)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#operator GoogleComputeSecurityPolicyRuleA#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#value GoogleComputeSecurityPolicyRuleA#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9537535d1c09141b7c8414579b5cff82e32efba7a9ea39de365602e3b824fb85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19403eae96b191611ae53500465e1fc8cff32e5b548850cf8faa1fc5ee42e1f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cefb382bd61f4d074bb7e50021a74ac52f9e4aa328a52396e4633e02261a05d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ab785b6e8c72741d36004fc6e77ac317226e20261eb9b87396e8c87b980bff7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e814474a0aaca5fb865aed10de1a0493f7877d7939fe1fc491cd3867dcaf4d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4e98fd99ab5967540572ca182f27cfc85e39fcc51ea64dc469f60882110175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27e359907d8708da42babe4269e899278bdf7d50cf443f5ea57cc03ca4d9248e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0159a6435de8cd5cee0c0191e5dfc93d8ced9ee8d16b97e6cff259fa0bbb7e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a293f9bd08add245c08780f72ba85ea16d0021c5de82a99443eb30d552da2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a03669ce8189471afb5795403955caf363460e58a49e6089efb1613ace4e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#operator GoogleComputeSecurityPolicyRuleA#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#value GoogleComputeSecurityPolicyRuleA#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03a1cee9e56b4821663d99576f1798ff2308ca8c87b60db99373199c3df242b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#operator GoogleComputeSecurityPolicyRuleA#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#value GoogleComputeSecurityPolicyRuleA#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f493074de2fff83105c14e1919933063fc35dbac0fa6656cb52b1708d18d222)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5078644cee1245deb7ee80281f796108dcafa7beeb6abd9e2e255cb4bc202cfb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8346363fd31ac47185d3a08445efea1ea3a2cd153e6ee02153386e57d90a2bd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08fb64586d597ccade7f9f786ffcbd038c96b025ca8c98541ee3bda998782a83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8779dc4fde0e28a45b8131d2383183defcb522c3eaa694bae3f5ceafd27f1fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3825b3eec8c5d32f2bb2920be16a0bfb31a0971e26dfaa118c0f5e2f4944bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a9e1773ae2fe71dc537896f49d68114c8d340bf61e69a08c96cadd0df7888d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb20f361fa7a625cbe4686ff172d15f67d0548f903962fcfe750d37ad548397b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f212ed15cfedfbf7c387f9d314122d15c3b6e327c9e56ee8f090300bfe78ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a21c7f88abe2d151c619e939fb1b33fe014410f2597d6ff2c2cd34969471ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#operator GoogleComputeSecurityPolicyRuleA#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#value GoogleComputeSecurityPolicyRuleA#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06aebdc5c23253d4e4da65d0aaddea4445797abad9f5f34ffa78d4cdd864c25b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#operator GoogleComputeSecurityPolicyRuleA#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#value GoogleComputeSecurityPolicyRuleA#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13db9fde8f1f336d654839693f6907fd128d5ab26576c1a664133f48c787dd9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770bbdc59703b01423af026a8f1df481832b79bb25aee06b44f7d117d8fbd912)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50c72cb23d72e4f7292ab371095e265a6611d70a3db33b94531ce8435e2919e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73138ffe883b013df24b8947c8c3811fd3709689421bfa3ede5c82f6888e0f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac5d1b5d454cec367020f5fdf1ccb40e67d9a20fab4425993ab60b972f8903e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f23d60221669e21a0080e4bc9974d31cb997dd7f9db7ff0a3bec866f4bad3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32f22e80f429b9da223ae7924c03d9b629c45efe52156bdb59cbc18280a95652)
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
            type_hints = typing.get_type_hints(_typecheckingstub__291f54446a463c54ca841c2e5decdfda1a673098e114d659153392886b2ff580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c412efd2ef1e19212d046972fbd5f3015c3e16b5e9e25b7b8e8369cb8f1349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb434dbd48c59e37a357ee1a3025861d6701cc3c6d930755de6adad244a639c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsA",
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
class GoogleComputeSecurityPolicyRuleRateLimitOptionsA:
    def __init__(
        self,
        *,
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA", typing.Dict[builtins.str, typing.Any]]] = None,
        conform_action: typing.Optional[builtins.str] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_action: typing.Optional[builtins.str] = None,
        exceed_redirect_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA", typing.Dict[builtins.str, typing.Any]]] = None,
        rate_limit_threshold: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#ban_duration_sec GoogleComputeSecurityPolicyRuleA#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#ban_threshold GoogleComputeSecurityPolicyRuleA#ban_threshold}
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#conform_action GoogleComputeSecurityPolicyRuleA#conform_action}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key GoogleComputeSecurityPolicyRuleA#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_configs GoogleComputeSecurityPolicyRuleA#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_name GoogleComputeSecurityPolicyRuleA#enforce_on_key_name}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint. Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#exceed_action GoogleComputeSecurityPolicyRuleA#exceed_action}
        :param exceed_redirect_options: exceed_redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#exceed_redirect_options GoogleComputeSecurityPolicyRuleA#exceed_redirect_options}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#rate_limit_threshold GoogleComputeSecurityPolicyRuleA#rate_limit_threshold}
        '''
        if isinstance(ban_threshold, dict):
            ban_threshold = GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA(**ban_threshold)
        if isinstance(exceed_redirect_options, dict):
            exceed_redirect_options = GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA(**exceed_redirect_options)
        if isinstance(rate_limit_threshold, dict):
            rate_limit_threshold = GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA(**rate_limit_threshold)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32dbc9e29f254631a662db26b49042a5b49efe76754f95c8dbbcb21671313b96)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#ban_duration_sec GoogleComputeSecurityPolicyRuleA#ban_duration_sec}
        '''
        result = self._values.get("ban_duration_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ban_threshold(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA"]:
        '''ban_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#ban_threshold GoogleComputeSecurityPolicyRuleA#ban_threshold}
        '''
        result = self._values.get("ban_threshold")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA"], result)

    @builtins.property
    def conform_action(self) -> typing.Optional[builtins.str]:
        '''Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#conform_action GoogleComputeSecurityPolicyRuleA#conform_action}
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
        - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "USER_IP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key GoogleComputeSecurityPolicyRuleA#enforce_on_key}
        '''
        result = self._values.get("enforce_on_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA"]]]:
        '''enforce_on_key_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_configs GoogleComputeSecurityPolicyRuleA#enforce_on_key_configs}
        '''
        result = self._values.get("enforce_on_key_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA"]]], result)

    @builtins.property
    def enforce_on_key_name(self) -> typing.Optional[builtins.str]:
        '''Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value.

        HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_name GoogleComputeSecurityPolicyRuleA#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exceed_action(self) -> typing.Optional[builtins.str]:
        '''Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint.

        Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#exceed_action GoogleComputeSecurityPolicyRuleA#exceed_action}
        '''
        result = self._values.get("exceed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exceed_redirect_options(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA"]:
        '''exceed_redirect_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#exceed_redirect_options GoogleComputeSecurityPolicyRuleA#exceed_redirect_options}
        '''
        result = self._values.get("exceed_redirect_options")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA"], result)

    @builtins.property
    def rate_limit_threshold(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA"]:
        '''rate_limit_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#rate_limit_threshold GoogleComputeSecurityPolicyRuleA#rate_limit_threshold}
        '''
        result = self._values.get("rate_limit_threshold")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRateLimitOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73fd3d3c70f942fb8d54c9f59f730b58dc7fcc25e98841d1d4aeb6c4975a96a3)
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
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#count GoogleComputeSecurityPolicyRuleA#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#interval_sec GoogleComputeSecurityPolicyRuleA#interval_sec}
        '''
        value = GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA(
            count=count, interval_sec=interval_sec
        )

        return typing.cast(None, jsii.invoke(self, "putBanThreshold", [value]))

    @jsii.member(jsii_name="putEnforceOnKeyConfigs")
    def put_enforce_on_key_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0e1dc49ee9fc09bb11e0184cda8cadbbcfb60497aa6627f0682d3c135b879c)
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
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target GoogleComputeSecurityPolicyRuleA#target}
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#type GoogleComputeSecurityPolicyRuleA#type}
        '''
        value = GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA(
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
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#count GoogleComputeSecurityPolicyRuleA#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#interval_sec GoogleComputeSecurityPolicyRuleA#interval_sec}
        '''
        value = GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA(
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
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference", jsii.get(self, "banThreshold"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigs")
    def enforce_on_key_configs(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList":
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList", jsii.get(self, "enforceOnKeyConfigs"))

    @builtins.property
    @jsii.member(jsii_name="exceedRedirectOptions")
    def exceed_redirect_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference", jsii.get(self, "exceedRedirectOptions"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThreshold")
    def rate_limit_threshold(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference", jsii.get(self, "rateLimitThreshold"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSecInput")
    def ban_duration_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "banDurationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="banThresholdInput")
    def ban_threshold_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA"], jsii.get(self, "banThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="conformActionInput")
    def conform_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conformActionInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigsInput")
    def enforce_on_key_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA"]]], jsii.get(self, "enforceOnKeyConfigsInput"))

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
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA"], jsii.get(self, "exceedRedirectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThresholdInput")
    def rate_limit_threshold_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA"], jsii.get(self, "rateLimitThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSec")
    def ban_duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "banDurationSec"))

    @ban_duration_sec.setter
    def ban_duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0824f407c91797e425b20d60cb54a7986f2e09cff07e533ba1f708f89c4c32b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "banDurationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conformAction")
    def conform_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conformAction"))

    @conform_action.setter
    def conform_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf5b12c9946a2af2cf71ebd56ad7522ad470ad95b3d02845633448ce3a51cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conformAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKey")
    def enforce_on_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKey"))

    @enforce_on_key.setter
    def enforce_on_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28490809c9c1fae8e400bba251e01de9426d3cb191f737efa83df25333338014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyName")
    def enforce_on_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyName"))

    @enforce_on_key_name.setter
    def enforce_on_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf95db751af04336c114f6185a169aea9469dbec98e36f3d2b406200382ffec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exceedAction")
    def exceed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exceedAction"))

    @exceed_action.setter
    def exceed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5bd49b3bebd1e27f7de48f0886d6bd306a33638970f0c9852d31720d5bb369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exceedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab734d81b94d8be022ba7a1967cdf3d44b2833e327c206294f996d3cbfc19d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#count GoogleComputeSecurityPolicyRuleA#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#interval_sec GoogleComputeSecurityPolicyRuleA#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4bc047ef6656b8b94368f5864fbcc3e425fc392cb6f7d0e94bb4c2218392cd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#count GoogleComputeSecurityPolicyRuleA#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_sec(self) -> typing.Optional[jsii.Number]:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#interval_sec GoogleComputeSecurityPolicyRuleA#interval_sec}
        '''
        result = self._values.get("interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef4b250ff66843db60c82ad4e4f7b002951e6d1387453f274280b5ba6b482933)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4add8636da39db7406326d4af3d0ef4f5629154e9123ca96dc4bc5da2e9fe959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b6f64084442f178d82c4a81fad0db74ed9c9cf5cd3744b7b46c5ffdcfd8dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00a278b71aa8cdbbfc6e8f3fa8af6ca9c476e20ecf2ce9b28d6492477f339ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA",
    jsii_struct_bases=[],
    name_mapping={
        "enforce_on_key_name": "enforceOnKeyName",
        "enforce_on_key_type": "enforceOnKeyType",
    },
)
class GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA:
    def __init__(
        self,
        *,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        enforce_on_key_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_name GoogleComputeSecurityPolicyRuleA#enforce_on_key_name}
        :param enforce_on_key_type: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKeyConfigs" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_type GoogleComputeSecurityPolicyRuleA#enforce_on_key_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853f3168d78d0b371bee45f23968a27f5ef27e3bd0dedcdc2aecf5f48ac621c5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_name GoogleComputeSecurityPolicyRuleA#enforce_on_key_name}
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
        - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "USER_IP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#enforce_on_key_type GoogleComputeSecurityPolicyRuleA#enforce_on_key_type}
        '''
        result = self._values.get("enforce_on_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b6ee33c1af949c2fcc753f029a101ce460f7750c6741fd7754b093271df4c7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071b2b5a0a0bfc12d7cd60762192b7ea0956800c5d158e2ad33c8807b8cf91c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34bddb1600e6a591ae4272627ea5d0b925997ca634a084a9576f00637dd6bf4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__392781f0eaef944dbf8d181aa2691c3bb26d7b248c84aca4d82267c19d2a3061)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62be5b914e37439ef3211ec43a5b40c6195fa7f179666d7b35e6dfb1adb10085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4419d6c0b4099a6121d1e1739cba6f7959071ad69d7e739d9bfd3c80df489085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51eb59501eda796ff101402fe117bb8c0d0ca61807db1d30c428b6589df0be77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d16639abeec8e075cc92ce8072e08d0c307879c55fc2c6147fc9cae1475935ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyType")
    def enforce_on_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyType"))

    @enforce_on_key_type.setter
    def enforce_on_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08f73046c6776aa7d477817bef7e623dd4dd748f5ac22c3f244cccbd4954377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ab3d7b89367352ecd821f4e42b937c1ed69c3fb8b9d11d5a74ce0a55253a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "type": "type"},
)
class GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA:
    def __init__(
        self,
        *,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target GoogleComputeSecurityPolicyRuleA#target}
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#type GoogleComputeSecurityPolicyRuleA#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c712659c1d8280f91011fcfdfbf0a494e779428bb5f1ade2ead60728fc32ec2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target GoogleComputeSecurityPolicyRuleA#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of the redirect action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#type GoogleComputeSecurityPolicyRuleA#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97724bf82859ba81b0a46a361adf8a2ae4f2fcee42b4d44132a707988e07ad13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c3aa2120b5c8d1f4f29324710e4fc2d44e8b6527587002a35c4da22cf8356f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db84bee3ffea11b2d861145a6b323b6fbbb05fdc9a51b3205d341b437e8d625a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28499f188bab3c59f3b037652f136f9162bcff59b2021466ab607c2df7bd2877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#count GoogleComputeSecurityPolicyRuleA#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#interval_sec GoogleComputeSecurityPolicyRuleA#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3c1cdc330ac742b2acf8ea443d99548e21e030b670db82046114bd951fd799)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#count GoogleComputeSecurityPolicyRuleA#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_sec(self) -> typing.Optional[jsii.Number]:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#interval_sec GoogleComputeSecurityPolicyRuleA#interval_sec}
        '''
        result = self._values.get("interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef3e15949031eb1c853398ad68af2d09213054f9461fa759dff334542ecce5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f34bb82a00f7842e7259d526f5df7f08f9817b0170d5ec77f10959810ca15fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4d0dab113bc4bc94e8ede8e232c8f749a8b887704e0cc501b9bbb1fd756b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d519f1268f76b31bcf730d39b2d33172adc1aa1c137e67a2a2bae15e6303b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRedirectOptionsA",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "type": "type"},
)
class GoogleComputeSecurityPolicyRuleRedirectOptionsA:
    def __init__(
        self,
        *,
        target: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target GoogleComputeSecurityPolicyRuleA#target}
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#type GoogleComputeSecurityPolicyRuleA#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea55e18dc7dc292f39b0af5d8236cb7f6f50c45ac0720be9c24781d482fc997)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#target GoogleComputeSecurityPolicyRuleA#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of the redirect action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#type GoogleComputeSecurityPolicyRuleA#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRedirectOptionsA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRedirectOptionsAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleRedirectOptionsAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__804532eb0cc827cf7155ec424e9f74ce84917a7ae0769e0a93e38ed39ba95f21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35b46d5baae1f0584505070ce4d69660a8b897a03f5721f9bbeaab99d67729d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e159a87610bfa8beccb6515b8e5b43e47d49fa3f0acd6a98338c515735e758e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRedirectOptionsA]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRedirectOptionsA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRedirectOptionsA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c801b253ce82e85c0f4379157dc56cc0ef3e0699267d196520019c3492eb7eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeSecurityPolicyRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#create GoogleComputeSecurityPolicyRuleA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#delete GoogleComputeSecurityPolicyRuleA#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#update GoogleComputeSecurityPolicyRuleA#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8c9b3f6f6fa3c091025a45772bf95eac1a694b42f753abee6cc64297809156)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#create GoogleComputeSecurityPolicyRuleA#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#delete GoogleComputeSecurityPolicyRuleA#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy_rule#update GoogleComputeSecurityPolicyRuleA#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicyRule.GoogleComputeSecurityPolicyRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__285cc87930e834642508e3560d1086f1e19e7738eb97b3f7c563e49c0004622e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d382ea559625bc980a814c5d16b3ba27386b547ed44df1822bd6fbb1415d3a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3899466d967864d2118eb229e3b92ec134e265f476fdfde3d61ed4fd732eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b98a6f728017c7697229a30bb0d27f7f73b219eef2def79457dd28c893b5abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec2fb1624c095be66dfb7c2b37771649a56451198c00069dc5f6d43c2db067b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeSecurityPolicyRuleA",
    "GoogleComputeSecurityPolicyRuleAConfig",
    "GoogleComputeSecurityPolicyRuleHeaderActionA",
    "GoogleComputeSecurityPolicyRuleHeaderActionAOutputReference",
    "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA",
    "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAList",
    "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsAOutputReference",
    "GoogleComputeSecurityPolicyRuleMatchA",
    "GoogleComputeSecurityPolicyRuleMatchAOutputReference",
    "GoogleComputeSecurityPolicyRuleMatchConfigA",
    "GoogleComputeSecurityPolicyRuleMatchConfigAOutputReference",
    "GoogleComputeSecurityPolicyRuleMatchExprA",
    "GoogleComputeSecurityPolicyRuleMatchExprAOutputReference",
    "GoogleComputeSecurityPolicyRuleMatchExprOptionsA",
    "GoogleComputeSecurityPolicyRuleMatchExprOptionsAOutputReference",
    "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA",
    "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsAOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigAOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionAOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieAOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderAOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamAOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriAOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsA",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsAOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdAOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAList",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsAOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsAOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdAOutputReference",
    "GoogleComputeSecurityPolicyRuleRedirectOptionsA",
    "GoogleComputeSecurityPolicyRuleRedirectOptionsAOutputReference",
    "GoogleComputeSecurityPolicyRuleTimeouts",
    "GoogleComputeSecurityPolicyRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__edc93a95ffa3cd8b3e3cafcc3b516db97865213392dab0c1d9603ea730aa5eee(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    priority: jsii.Number,
    security_policy: builtins.str,
    description: typing.Optional[builtins.str] = None,
    header_action: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleHeaderActionA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchA, typing.Dict[builtins.str, typing.Any]]] = None,
    preconfigured_waf_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limit_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRedirectOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f9e7b3cd3626cf2fcf89ee32bf9468321fb9f066b84ef780a32919887f142914(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef55439734609d5b4b0d84ced394d0c9e7f10011d2cfdac998219d56641e925d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc0eb4464e4a0b2b50147a19b33e8fa5a3a21713a39062767e641eb3487042f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39516fa6434b92668693ff6834d2ead2f67e11a3b94ffc0fb8a2beb8acb84f67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081d5d619f749a7aef935735f49d4ee838b21bdeccb1d951b0892d2f37d61473(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e379040931f34bde3d29788cb1142e4bc14cbf0dff49287f98d11aa8f6c93e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842a2d956af97f39623d915194e272961b8e3531d4f91b8949247a07a21c2b13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5e2830e67cfd7478c09d9d7ed5c587e3cc87e7fee0eb4cb97a083795c9750a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ee6646e8514f872b6e4a21c13ec545392f08fbb20082d609bcde1bac1dce9f(
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
    header_action: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleHeaderActionA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchA, typing.Dict[builtins.str, typing.Any]]] = None,
    preconfigured_waf_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limit_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRedirectOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca93e47be9e0e507b8748e151c002f7d6876292f2b85858646954632a7c19479(
    *,
    request_headers_to_adds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd07eeee031970c0631e11cdc1d43986060b99df729fbc6203f59551559a533(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f415c248d2fd4d11bb42c83104946bf0d3b49e4bc6cc23507467a9d591b6dd32(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4da8a2a8ba88093b5bc7bf304469e5b62007f286878f654beb58a42c4c530b(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleHeaderActionA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ced839e3ff4f08fea381143e30911a5a728f410fcf5fa7a9abd3fc3e7b4bf7(
    *,
    header_name: typing.Optional[builtins.str] = None,
    header_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab91146eb531fa36abf7f9cad107ba0dc03682abfa44b296bee51fa34d6cba6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c7d30a726978e590e0d1d1d665453a5647ebe29780c3650c767d6bca72b4d6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c5383e5acf732063117567806a16ebed02fa926f5ba2ed0d0d0b972de6c0a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02cdb90e1a3b1c3b82771954c38ab0ac48baa0ee1c931b60f926b095befcb83(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140ee5e38b5cd02af94c39a91b0ecfdea1723590423444f5763fde6e42217234(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82884824a8f29eff60f107af2bc9e24fa2d2b01d4fec89ef583c0b88c583f83c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f806fb03b2e5c38f508160c6f132eace676a37dcf6099de8bd4288d9575cab3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea50b76db20ede3ce02a26e50cbc50fa8d453ce788d8dd1433cf6d6e25cc9d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bda4aebbb320c4fd5f2ff45b4d49ef74e7e0730a3d5a45d20ca29467eddb161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f78141bfaa249e8e0cb82990753716606c7bbac23b8d63d3f1e7e93aa02d5b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1074a85708c3ff12ddd94479bbec723dc47b07962599c97b709cb4e24afbee24(
    *,
    config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    expr: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchExprA, typing.Dict[builtins.str, typing.Any]]] = None,
    expr_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchExprOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    versioned_expr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c652714b48770cd61d30bfa60aaa6eab44bb11306f97bc9d9b3664dac96972(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f21730f5fa3c2a7dbde8c149558ce6ffd39c25ed3555d602b0d2c99f3ecded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2caf6d8876020371ca2e81b8a298990dd39282ffea26a3a3349b31214032719a(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d33e0efaef4b0d1896711f88e057b08275dca247757439d0035a8f88d863d4f(
    *,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafc43a2375c3607eeb3a6f02bcac7c6aa8010e99326afe6c5650bc103db49e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93481ebded63e21d75baca32465397d1e1e81dae5ae84242c8ca7f13e61e0a3b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4209abba2b278135d80660df255feda771f3d47c412f71e215c61a138f336dbc(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789a15d6d6e833977ffb820e08ef1cdc189999fba20b4e215fee139cd1136a73(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adea5023c04e985973c63bd1fee31ab22c318018ac53d7f40ec94c6354fd93e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9f0b59e217df8516726cb5eedef2ed1029a0053aba220b08ae6e4324117f8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe4152202f33b2409a51accdc94741630fb2428c415a1b325948f17ec41ada8(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0a8867cc34f5983ff86489fbd795d7e2950d5779437d38da378ac6225e512b(
    *,
    recaptcha_options: typing.Union[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fab20a5ba13ec5695e5705462bcb2f7c577ed7e690cc5b03c77cc803ae35f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79880172444b35fe79b77cc6318f7a6c4396f8ba58fbf2bec5cbe0db75c899c(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ea02272b51b8b10ce8a26574c5e528d971617a7d028fe4a573b5559abdd70d(
    *,
    action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a398397183ee00a1fca5925c216a0f110384a700caad81177b5659dd414fb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5773a25772511bb2928e071a5cc76c7d53ba67fb866a7ee134159d69ff293606(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b180e57671e1551637892fd11c9aae76b6e6845892eb98af215750fe7aff97(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6cfec65c1e48dc079a7452d6981bf052704feeab3f835226ad8754472a30ef7(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8723eded37088a42f66e85e5101b383b7f4d98e3af1baa4e43f0bc1267dd89eb(
    *,
    exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3aa54cb05754658665e93dd785499144a447b178b20e33558f663cd941184ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bc03c30eb719ad2f4c7765b14c898ba6269df83808e4ebd15366d6233fd199(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e5a2f5d242f20f8cf764c90e38b569da27729481f19eb20bab714f24b0d9db(
    value: typing.Optional[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06eabce8e65c7cf4a877bfa447c468a5a7e652928a95f67ce825b5a9672bd38f(
    *,
    target_rule_set: builtins.str,
    request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783175a6f3a28408f01532934d89b5ed0a90ab781fb7d0edf504390922cff8d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b3998fbe2845d279003245902289a769233ba6ab08b08c492e5241539b0585(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57749f471976490f3ceff949865ca727004429e5890f7607c6f247448dc0fa85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b6d503555208adf80339794ae817c28c40ea82b6654a16ea0ea9cc67568c59(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05709ff6491f9db861a0568db2239fbd5967714242941bbeee8b843b2bfe70ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1666fbd072343bb8cbab2f768212dbd5fd29434d2b2147479b15b4c1c9cbcfea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e0ab28ea97cec782cdf6a5bd499d7425bcbbd5c2a5071b30d8b0b45581c158(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e181fb122e05fa0f7570d917756c1fe53de0abcd7e736ec52f08bedda7338d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94ac1ddb0cb17cdfe15f6e763176349a13593fecaed7aa943ea013ccc93afc6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85f028b76006a0865aa199cade4c71ca244df1186c18a86c61ecc77c78c050f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f94f4cdc4b2de87244bd71d57202dc531c07bc53f43b2a5f0b1f3aa1f10d37(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034f9c6d1e978f41eb9bd2e187fc7769f4d7156bf69f0fbb7ef62694afeaeb45(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67f03470cd101a71bc4f6edc0eaa5393fb4f3032cd57e9a765324aa2660a4f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5781013fe114241fd8e55266504b5e805a80772177b3aea4c4a8ef39c5205dec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee2eccd47fb781c5141b6f0da835907a38c47dd260a252a08bdbf2999fc054e(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d75296eb4e1de90452b97355760fbac7b03159c4190e9947dab36bb78447bfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2874d6f8d82f17ff96a62802c4d86b074df2354d198038011814e4e1fe40b266(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7512a6ab14f70c0a62a6ba2defe683d25d4adc246f56f63c931456de534c640d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b06ca7c2e630a35fb257c15c3265cf145454347cb3e50ee60ff6189f1d7a06(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59559af1568ec84f05db1590cdb7c60a2bfe03d0f78d216b4f457015521e723(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4ba4077349818eb0a2c86b8b43c8f3c8f0d661b666b34559e3d7f56a8ed41a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f295e3c8e1e44a2bd00c67607f6ee6e004a64fde6965f6caf20e8da143a4a410(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94c1a03fe924951d183cf61dce7d8268cf28f5bc3278b6639702a528366dc6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa299d2efc26c2f3d78f5eaf91e9f12fc35c98dda68f4c0f353c8c72f6296011(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50295405ab7eba222b01bf09751e8f931ab9da518e368d5f0645e4b754daced0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007c3bf2d9eb054f21f0f7f13c2a61038d4fa5da3a8327b4b0d417c2b000a527(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9537535d1c09141b7c8414579b5cff82e32efba7a9ea39de365602e3b824fb85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19403eae96b191611ae53500465e1fc8cff32e5b548850cf8faa1fc5ee42e1f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cefb382bd61f4d074bb7e50021a74ac52f9e4aa328a52396e4633e02261a05d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab785b6e8c72741d36004fc6e77ac317226e20261eb9b87396e8c87b980bff7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e814474a0aaca5fb865aed10de1a0493f7877d7939fe1fc491cd3867dcaf4d1e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4e98fd99ab5967540572ca182f27cfc85e39fcc51ea64dc469f60882110175(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e359907d8708da42babe4269e899278bdf7d50cf443f5ea57cc03ca4d9248e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0159a6435de8cd5cee0c0191e5dfc93d8ced9ee8d16b97e6cff259fa0bbb7e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a293f9bd08add245c08780f72ba85ea16d0021c5de82a99443eb30d552da2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a03669ce8189471afb5795403955caf363460e58a49e6089efb1613ace4e7f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03a1cee9e56b4821663d99576f1798ff2308ca8c87b60db99373199c3df242b(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f493074de2fff83105c14e1919933063fc35dbac0fa6656cb52b1708d18d222(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5078644cee1245deb7ee80281f796108dcafa7beeb6abd9e2e255cb4bc202cfb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8346363fd31ac47185d3a08445efea1ea3a2cd153e6ee02153386e57d90a2bd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08fb64586d597ccade7f9f786ffcbd038c96b025ca8c98541ee3bda998782a83(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8779dc4fde0e28a45b8131d2383183defcb522c3eaa694bae3f5ceafd27f1fd2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3825b3eec8c5d32f2bb2920be16a0bfb31a0971e26dfaa118c0f5e2f4944bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9e1773ae2fe71dc537896f49d68114c8d340bf61e69a08c96cadd0df7888d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb20f361fa7a625cbe4686ff172d15f67d0548f903962fcfe750d37ad548397b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f212ed15cfedfbf7c387f9d314122d15c3b6e327c9e56ee8f090300bfe78ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a21c7f88abe2d151c619e939fb1b33fe014410f2597d6ff2c2cd34969471ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06aebdc5c23253d4e4da65d0aaddea4445797abad9f5f34ffa78d4cdd864c25b(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13db9fde8f1f336d654839693f6907fd128d5ab26576c1a664133f48c787dd9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770bbdc59703b01423af026a8f1df481832b79bb25aee06b44f7d117d8fbd912(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50c72cb23d72e4f7292ab371095e265a6611d70a3db33b94531ce8435e2919e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73138ffe883b013df24b8947c8c3811fd3709689421bfa3ede5c82f6888e0f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5d1b5d454cec367020f5fdf1ccb40e67d9a20fab4425993ab60b972f8903e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f23d60221669e21a0080e4bc9974d31cb997dd7f9db7ff0a3bec866f4bad3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f22e80f429b9da223ae7924c03d9b629c45efe52156bdb59cbc18280a95652(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291f54446a463c54ca841c2e5decdfda1a673098e114d659153392886b2ff580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c412efd2ef1e19212d046972fbd5f3015c3e16b5e9e25b7b8e8369cb8f1349(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb434dbd48c59e37a357ee1a3025861d6701cc3c6d930755de6adad244a639c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32dbc9e29f254631a662db26b49042a5b49efe76754f95c8dbbcb21671313b96(
    *,
    ban_duration_sec: typing.Optional[jsii.Number] = None,
    ban_threshold: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA, typing.Dict[builtins.str, typing.Any]]] = None,
    conform_action: typing.Optional[builtins.str] = None,
    enforce_on_key: typing.Optional[builtins.str] = None,
    enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    exceed_action: typing.Optional[builtins.str] = None,
    exceed_redirect_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA, typing.Dict[builtins.str, typing.Any]]] = None,
    rate_limit_threshold: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73fd3d3c70f942fb8d54c9f59f730b58dc7fcc25e98841d1d4aeb6c4975a96a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0e1dc49ee9fc09bb11e0184cda8cadbbcfb60497aa6627f0682d3c135b879c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0824f407c91797e425b20d60cb54a7986f2e09cff07e533ba1f708f89c4c32b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf5b12c9946a2af2cf71ebd56ad7522ad470ad95b3d02845633448ce3a51cfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28490809c9c1fae8e400bba251e01de9426d3cb191f737efa83df25333338014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf95db751af04336c114f6185a169aea9469dbec98e36f3d2b406200382ffec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5bd49b3bebd1e27f7de48f0886d6bd306a33638970f0c9852d31720d5bb369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab734d81b94d8be022ba7a1967cdf3d44b2833e327c206294f996d3cbfc19d3(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4bc047ef6656b8b94368f5864fbcc3e425fc392cb6f7d0e94bb4c2218392cd(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4b250ff66843db60c82ad4e4f7b002951e6d1387453f274280b5ba6b482933(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4add8636da39db7406326d4af3d0ef4f5629154e9123ca96dc4bc5da2e9fe959(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b6f64084442f178d82c4a81fad0db74ed9c9cf5cd3744b7b46c5ffdcfd8dad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00a278b71aa8cdbbfc6e8f3fa8af6ca9c476e20ecf2ce9b28d6492477f339ae(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853f3168d78d0b371bee45f23968a27f5ef27e3bd0dedcdc2aecf5f48ac621c5(
    *,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    enforce_on_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6ee33c1af949c2fcc753f029a101ce460f7750c6741fd7754b093271df4c7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071b2b5a0a0bfc12d7cd60762192b7ea0956800c5d158e2ad33c8807b8cf91c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34bddb1600e6a591ae4272627ea5d0b925997ca634a084a9576f00637dd6bf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392781f0eaef944dbf8d181aa2691c3bb26d7b248c84aca4d82267c19d2a3061(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62be5b914e37439ef3211ec43a5b40c6195fa7f179666d7b35e6dfb1adb10085(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4419d6c0b4099a6121d1e1739cba6f7959071ad69d7e739d9bfd3c80df489085(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51eb59501eda796ff101402fe117bb8c0d0ca61807db1d30c428b6589df0be77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16639abeec8e075cc92ce8072e08d0c307879c55fc2c6147fc9cae1475935ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08f73046c6776aa7d477817bef7e623dd4dd748f5ac22c3f244cccbd4954377(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ab3d7b89367352ecd821f4e42b937c1ed69c3fb8b9d11d5a74ce0a55253a90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c712659c1d8280f91011fcfdfbf0a494e779428bb5f1ade2ead60728fc32ec2(
    *,
    target: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97724bf82859ba81b0a46a361adf8a2ae4f2fcee42b4d44132a707988e07ad13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c3aa2120b5c8d1f4f29324710e4fc2d44e8b6527587002a35c4da22cf8356f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db84bee3ffea11b2d861145a6b323b6fbbb05fdc9a51b3205d341b437e8d625a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28499f188bab3c59f3b037652f136f9162bcff59b2021466ab607c2df7bd2877(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3c1cdc330ac742b2acf8ea443d99548e21e030b670db82046114bd951fd799(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef3e15949031eb1c853398ad68af2d09213054f9461fa759dff334542ecce5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34bb82a00f7842e7259d526f5df7f08f9817b0170d5ec77f10959810ca15fb1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4d0dab113bc4bc94e8ede8e232c8f749a8b887704e0cc501b9bbb1fd756b98(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d519f1268f76b31bcf730d39b2d33172adc1aa1c137e67a2a2bae15e6303b7f(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea55e18dc7dc292f39b0af5d8236cb7f6f50c45ac0720be9c24781d482fc997(
    *,
    target: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804532eb0cc827cf7155ec424e9f74ce84917a7ae0769e0a93e38ed39ba95f21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b46d5baae1f0584505070ce4d69660a8b897a03f5721f9bbeaab99d67729d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e159a87610bfa8beccb6515b8e5b43e47d49fa3f0acd6a98338c515735e758e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c801b253ce82e85c0f4379157dc56cc0ef3e0699267d196520019c3492eb7eab(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRedirectOptionsA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8c9b3f6f6fa3c091025a45772bf95eac1a694b42f753abee6cc64297809156(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285cc87930e834642508e3560d1086f1e19e7738eb97b3f7c563e49c0004622e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d382ea559625bc980a814c5d16b3ba27386b547ed44df1822bd6fbb1415d3a64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3899466d967864d2118eb229e3b92ec134e265f476fdfde3d61ed4fd732eca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b98a6f728017c7697229a30bb0d27f7f73b219eef2def79457dd28c893b5abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec2fb1624c095be66dfb7c2b37771649a56451198c00069dc5f6d43c2db067b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
