r'''
# `azurerm_firewall_policy`

Refer to the Terraform Registry for docs: [`azurerm_firewall_policy`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy).
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


class FirewallPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy azurerm_firewall_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        auto_learn_private_ranges_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        base_policy_id: typing.Optional[builtins.str] = None,
        dns: typing.Optional[typing.Union["FirewallPolicyDns", typing.Dict[builtins.str, typing.Any]]] = None,
        explicit_proxy: typing.Optional[typing.Union["FirewallPolicyExplicitProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["FirewallPolicyIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        insights: typing.Optional[typing.Union["FirewallPolicyInsights", typing.Dict[builtins.str, typing.Any]]] = None,
        intrusion_detection: typing.Optional[typing.Union["FirewallPolicyIntrusionDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        private_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        sku: typing.Optional[builtins.str] = None,
        sql_redirect_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        threat_intelligence_allowlist: typing.Optional[typing.Union["FirewallPolicyThreatIntelligenceAllowlistStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        threat_intelligence_mode: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["FirewallPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_certificate: typing.Optional[typing.Union["FirewallPolicyTlsCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy azurerm_firewall_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#location FirewallPolicy#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#name FirewallPolicy#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#resource_group_name FirewallPolicy#resource_group_name}.
        :param auto_learn_private_ranges_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#auto_learn_private_ranges_enabled FirewallPolicy#auto_learn_private_ranges_enabled}.
        :param base_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#base_policy_id FirewallPolicy#base_policy_id}.
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#dns FirewallPolicy#dns}
        :param explicit_proxy: explicit_proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#explicit_proxy FirewallPolicy#explicit_proxy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#id FirewallPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#identity FirewallPolicy#identity}
        :param insights: insights block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#insights FirewallPolicy#insights}
        :param intrusion_detection: intrusion_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#intrusion_detection FirewallPolicy#intrusion_detection}
        :param private_ip_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#private_ip_ranges FirewallPolicy#private_ip_ranges}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#sku FirewallPolicy#sku}.
        :param sql_redirect_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#sql_redirect_allowed FirewallPolicy#sql_redirect_allowed}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#tags FirewallPolicy#tags}.
        :param threat_intelligence_allowlist: threat_intelligence_allowlist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#threat_intelligence_allowlist FirewallPolicy#threat_intelligence_allowlist}
        :param threat_intelligence_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#threat_intelligence_mode FirewallPolicy#threat_intelligence_mode}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#timeouts FirewallPolicy#timeouts}
        :param tls_certificate: tls_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#tls_certificate FirewallPolicy#tls_certificate}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__019c06c2a343ec961e5f9c63ef1b04cb321fc4369a208a1bb8b370a1e2bedc22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FirewallPolicyConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            auto_learn_private_ranges_enabled=auto_learn_private_ranges_enabled,
            base_policy_id=base_policy_id,
            dns=dns,
            explicit_proxy=explicit_proxy,
            id=id,
            identity=identity,
            insights=insights,
            intrusion_detection=intrusion_detection,
            private_ip_ranges=private_ip_ranges,
            sku=sku,
            sql_redirect_allowed=sql_redirect_allowed,
            tags=tags,
            threat_intelligence_allowlist=threat_intelligence_allowlist,
            threat_intelligence_mode=threat_intelligence_mode,
            timeouts=timeouts,
            tls_certificate=tls_certificate,
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
        '''Generates CDKTF code for importing a FirewallPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FirewallPolicy to import.
        :param import_from_id: The id of the existing FirewallPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FirewallPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2b555550016130bd89aa9ea4a4925638d7b646d20671b6165240ce565e1890)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDns")
    def put_dns(
        self,
        *,
        proxy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param proxy_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#proxy_enabled FirewallPolicy#proxy_enabled}.
        :param servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#servers FirewallPolicy#servers}.
        '''
        value = FirewallPolicyDns(proxy_enabled=proxy_enabled, servers=servers)

        return typing.cast(None, jsii.invoke(self, "putDns", [value]))

    @jsii.member(jsii_name="putExplicitProxy")
    def put_explicit_proxy(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_pac_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        pac_file: typing.Optional[builtins.str] = None,
        pac_file_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#enabled FirewallPolicy#enabled}.
        :param enable_pac_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#enable_pac_file FirewallPolicy#enable_pac_file}.
        :param http_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#http_port FirewallPolicy#http_port}.
        :param https_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#https_port FirewallPolicy#https_port}.
        :param pac_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#pac_file FirewallPolicy#pac_file}.
        :param pac_file_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#pac_file_port FirewallPolicy#pac_file_port}.
        '''
        value = FirewallPolicyExplicitProxy(
            enabled=enabled,
            enable_pac_file=enable_pac_file,
            http_port=http_port,
            https_port=https_port,
            pac_file=pac_file,
            pac_file_port=pac_file_port,
        )

        return typing.cast(None, jsii.invoke(self, "putExplicitProxy", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#type FirewallPolicy#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#identity_ids FirewallPolicy#identity_ids}.
        '''
        value = FirewallPolicyIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putInsights")
    def put_insights(
        self,
        *,
        default_log_analytics_workspace_id: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_analytics_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirewallPolicyInsightsLogAnalyticsWorkspace", typing.Dict[builtins.str, typing.Any]]]]] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param default_log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#default_log_analytics_workspace_id FirewallPolicy#default_log_analytics_workspace_id}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#enabled FirewallPolicy#enabled}.
        :param log_analytics_workspace: log_analytics_workspace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#log_analytics_workspace FirewallPolicy#log_analytics_workspace}
        :param retention_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#retention_in_days FirewallPolicy#retention_in_days}.
        '''
        value = FirewallPolicyInsights(
            default_log_analytics_workspace_id=default_log_analytics_workspace_id,
            enabled=enabled,
            log_analytics_workspace=log_analytics_workspace,
            retention_in_days=retention_in_days,
        )

        return typing.cast(None, jsii.invoke(self, "putInsights", [value]))

    @jsii.member(jsii_name="putIntrusionDetection")
    def put_intrusion_detection(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        private_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        signature_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirewallPolicyIntrusionDetectionSignatureOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        traffic_bypass: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirewallPolicyIntrusionDetectionTrafficBypass", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#mode FirewallPolicy#mode}.
        :param private_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#private_ranges FirewallPolicy#private_ranges}.
        :param signature_overrides: signature_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#signature_overrides FirewallPolicy#signature_overrides}
        :param traffic_bypass: traffic_bypass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#traffic_bypass FirewallPolicy#traffic_bypass}
        '''
        value = FirewallPolicyIntrusionDetection(
            mode=mode,
            private_ranges=private_ranges,
            signature_overrides=signature_overrides,
            traffic_bypass=traffic_bypass,
        )

        return typing.cast(None, jsii.invoke(self, "putIntrusionDetection", [value]))

    @jsii.member(jsii_name="putThreatIntelligenceAllowlist")
    def put_threat_intelligence_allowlist(
        self,
        *,
        fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param fqdns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#fqdns FirewallPolicy#fqdns}.
        :param ip_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#ip_addresses FirewallPolicy#ip_addresses}.
        '''
        value = FirewallPolicyThreatIntelligenceAllowlistStruct(
            fqdns=fqdns, ip_addresses=ip_addresses
        )

        return typing.cast(None, jsii.invoke(self, "putThreatIntelligenceAllowlist", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#create FirewallPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#delete FirewallPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#read FirewallPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#update FirewallPolicy#update}.
        '''
        value = FirewallPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTlsCertificate")
    def put_tls_certificate(
        self,
        *,
        key_vault_secret_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param key_vault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#key_vault_secret_id FirewallPolicy#key_vault_secret_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#name FirewallPolicy#name}.
        '''
        value = FirewallPolicyTlsCertificate(
            key_vault_secret_id=key_vault_secret_id, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putTlsCertificate", [value]))

    @jsii.member(jsii_name="resetAutoLearnPrivateRangesEnabled")
    def reset_auto_learn_private_ranges_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoLearnPrivateRangesEnabled", []))

    @jsii.member(jsii_name="resetBasePolicyId")
    def reset_base_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasePolicyId", []))

    @jsii.member(jsii_name="resetDns")
    def reset_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns", []))

    @jsii.member(jsii_name="resetExplicitProxy")
    def reset_explicit_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExplicitProxy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetInsights")
    def reset_insights(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsights", []))

    @jsii.member(jsii_name="resetIntrusionDetection")
    def reset_intrusion_detection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntrusionDetection", []))

    @jsii.member(jsii_name="resetPrivateIpRanges")
    def reset_private_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpRanges", []))

    @jsii.member(jsii_name="resetSku")
    def reset_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSku", []))

    @jsii.member(jsii_name="resetSqlRedirectAllowed")
    def reset_sql_redirect_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlRedirectAllowed", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetThreatIntelligenceAllowlist")
    def reset_threat_intelligence_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatIntelligenceAllowlist", []))

    @jsii.member(jsii_name="resetThreatIntelligenceMode")
    def reset_threat_intelligence_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatIntelligenceMode", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTlsCertificate")
    def reset_tls_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsCertificate", []))

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
    @jsii.member(jsii_name="childPolicies")
    def child_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "childPolicies"))

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(self) -> "FirewallPolicyDnsOutputReference":
        return typing.cast("FirewallPolicyDnsOutputReference", jsii.get(self, "dns"))

    @builtins.property
    @jsii.member(jsii_name="explicitProxy")
    def explicit_proxy(self) -> "FirewallPolicyExplicitProxyOutputReference":
        return typing.cast("FirewallPolicyExplicitProxyOutputReference", jsii.get(self, "explicitProxy"))

    @builtins.property
    @jsii.member(jsii_name="firewalls")
    def firewalls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "firewalls"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "FirewallPolicyIdentityOutputReference":
        return typing.cast("FirewallPolicyIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="insights")
    def insights(self) -> "FirewallPolicyInsightsOutputReference":
        return typing.cast("FirewallPolicyInsightsOutputReference", jsii.get(self, "insights"))

    @builtins.property
    @jsii.member(jsii_name="intrusionDetection")
    def intrusion_detection(self) -> "FirewallPolicyIntrusionDetectionOutputReference":
        return typing.cast("FirewallPolicyIntrusionDetectionOutputReference", jsii.get(self, "intrusionDetection"))

    @builtins.property
    @jsii.member(jsii_name="ruleCollectionGroups")
    def rule_collection_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ruleCollectionGroups"))

    @builtins.property
    @jsii.member(jsii_name="threatIntelligenceAllowlist")
    def threat_intelligence_allowlist(
        self,
    ) -> "FirewallPolicyThreatIntelligenceAllowlistStructOutputReference":
        return typing.cast("FirewallPolicyThreatIntelligenceAllowlistStructOutputReference", jsii.get(self, "threatIntelligenceAllowlist"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FirewallPolicyTimeoutsOutputReference":
        return typing.cast("FirewallPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="tlsCertificate")
    def tls_certificate(self) -> "FirewallPolicyTlsCertificateOutputReference":
        return typing.cast("FirewallPolicyTlsCertificateOutputReference", jsii.get(self, "tlsCertificate"))

    @builtins.property
    @jsii.member(jsii_name="autoLearnPrivateRangesEnabledInput")
    def auto_learn_private_ranges_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoLearnPrivateRangesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="basePolicyIdInput")
    def base_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "basePolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsInput")
    def dns_input(self) -> typing.Optional["FirewallPolicyDns"]:
        return typing.cast(typing.Optional["FirewallPolicyDns"], jsii.get(self, "dnsInput"))

    @builtins.property
    @jsii.member(jsii_name="explicitProxyInput")
    def explicit_proxy_input(self) -> typing.Optional["FirewallPolicyExplicitProxy"]:
        return typing.cast(typing.Optional["FirewallPolicyExplicitProxy"], jsii.get(self, "explicitProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["FirewallPolicyIdentity"]:
        return typing.cast(typing.Optional["FirewallPolicyIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsInput")
    def insights_input(self) -> typing.Optional["FirewallPolicyInsights"]:
        return typing.cast(typing.Optional["FirewallPolicyInsights"], jsii.get(self, "insightsInput"))

    @builtins.property
    @jsii.member(jsii_name="intrusionDetectionInput")
    def intrusion_detection_input(
        self,
    ) -> typing.Optional["FirewallPolicyIntrusionDetection"]:
        return typing.cast(typing.Optional["FirewallPolicyIntrusionDetection"], jsii.get(self, "intrusionDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpRangesInput")
    def private_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "privateIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlRedirectAllowedInput")
    def sql_redirect_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sqlRedirectAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="threatIntelligenceAllowlistInput")
    def threat_intelligence_allowlist_input(
        self,
    ) -> typing.Optional["FirewallPolicyThreatIntelligenceAllowlistStruct"]:
        return typing.cast(typing.Optional["FirewallPolicyThreatIntelligenceAllowlistStruct"], jsii.get(self, "threatIntelligenceAllowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="threatIntelligenceModeInput")
    def threat_intelligence_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "threatIntelligenceModeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirewallPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirewallPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsCertificateInput")
    def tls_certificate_input(self) -> typing.Optional["FirewallPolicyTlsCertificate"]:
        return typing.cast(typing.Optional["FirewallPolicyTlsCertificate"], jsii.get(self, "tlsCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="autoLearnPrivateRangesEnabled")
    def auto_learn_private_ranges_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoLearnPrivateRangesEnabled"))

    @auto_learn_private_ranges_enabled.setter
    def auto_learn_private_ranges_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c1a0bd6522b82dbeb38bdf7f2071756093d676a0752fe7337fb7039853810a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoLearnPrivateRangesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="basePolicyId")
    def base_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basePolicyId"))

    @base_policy_id.setter
    def base_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6079777f07a9a13dcadd808117da9451ce3418171d530c7eb9b82a6039963be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basePolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab70562142c6dfd5199aeb1510f6812e44e62f17f1686757c30a7e594dfcc67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d79c130ba1291c262e02a2a44e143d1bd882d184360b9075fa4a2353de6e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cad2a4ee2bc0524213493e0968b8b59786e4aab41441a0f11e8b39eed190351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpRanges")
    def private_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateIpRanges"))

    @private_ip_ranges.setter
    def private_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39e1e146541c2a3039004b33860fc4f81e3cde442b30c0a0a162de7d4c252c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ce5f2de8bd518606fd19dec07647e96ef72fa474b055075b80e56cd2eb85c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4728786bf923ae3f345633739f02687aa2b125d39321f5db26a7b91ad0a7c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlRedirectAllowed")
    def sql_redirect_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sqlRedirectAllowed"))

    @sql_redirect_allowed.setter
    def sql_redirect_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c42885f4f996c8614d0506ea512c50528161d20246009fbfca738a4a670c732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlRedirectAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e1b7f79349b0ae49eaa5c727ccb9571b5f4a6040402bd5a477aa025373b834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threatIntelligenceMode")
    def threat_intelligence_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "threatIntelligenceMode"))

    @threat_intelligence_mode.setter
    def threat_intelligence_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244fecbf8ee2c77bf98589361e1eb0ae30c8932e8525627365b2b003a2a332ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threatIntelligenceMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "auto_learn_private_ranges_enabled": "autoLearnPrivateRangesEnabled",
        "base_policy_id": "basePolicyId",
        "dns": "dns",
        "explicit_proxy": "explicitProxy",
        "id": "id",
        "identity": "identity",
        "insights": "insights",
        "intrusion_detection": "intrusionDetection",
        "private_ip_ranges": "privateIpRanges",
        "sku": "sku",
        "sql_redirect_allowed": "sqlRedirectAllowed",
        "tags": "tags",
        "threat_intelligence_allowlist": "threatIntelligenceAllowlist",
        "threat_intelligence_mode": "threatIntelligenceMode",
        "timeouts": "timeouts",
        "tls_certificate": "tlsCertificate",
    },
)
class FirewallPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        auto_learn_private_ranges_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        base_policy_id: typing.Optional[builtins.str] = None,
        dns: typing.Optional[typing.Union["FirewallPolicyDns", typing.Dict[builtins.str, typing.Any]]] = None,
        explicit_proxy: typing.Optional[typing.Union["FirewallPolicyExplicitProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["FirewallPolicyIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        insights: typing.Optional[typing.Union["FirewallPolicyInsights", typing.Dict[builtins.str, typing.Any]]] = None,
        intrusion_detection: typing.Optional[typing.Union["FirewallPolicyIntrusionDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        private_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        sku: typing.Optional[builtins.str] = None,
        sql_redirect_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        threat_intelligence_allowlist: typing.Optional[typing.Union["FirewallPolicyThreatIntelligenceAllowlistStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        threat_intelligence_mode: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["FirewallPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_certificate: typing.Optional[typing.Union["FirewallPolicyTlsCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#location FirewallPolicy#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#name FirewallPolicy#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#resource_group_name FirewallPolicy#resource_group_name}.
        :param auto_learn_private_ranges_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#auto_learn_private_ranges_enabled FirewallPolicy#auto_learn_private_ranges_enabled}.
        :param base_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#base_policy_id FirewallPolicy#base_policy_id}.
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#dns FirewallPolicy#dns}
        :param explicit_proxy: explicit_proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#explicit_proxy FirewallPolicy#explicit_proxy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#id FirewallPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#identity FirewallPolicy#identity}
        :param insights: insights block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#insights FirewallPolicy#insights}
        :param intrusion_detection: intrusion_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#intrusion_detection FirewallPolicy#intrusion_detection}
        :param private_ip_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#private_ip_ranges FirewallPolicy#private_ip_ranges}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#sku FirewallPolicy#sku}.
        :param sql_redirect_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#sql_redirect_allowed FirewallPolicy#sql_redirect_allowed}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#tags FirewallPolicy#tags}.
        :param threat_intelligence_allowlist: threat_intelligence_allowlist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#threat_intelligence_allowlist FirewallPolicy#threat_intelligence_allowlist}
        :param threat_intelligence_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#threat_intelligence_mode FirewallPolicy#threat_intelligence_mode}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#timeouts FirewallPolicy#timeouts}
        :param tls_certificate: tls_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#tls_certificate FirewallPolicy#tls_certificate}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dns, dict):
            dns = FirewallPolicyDns(**dns)
        if isinstance(explicit_proxy, dict):
            explicit_proxy = FirewallPolicyExplicitProxy(**explicit_proxy)
        if isinstance(identity, dict):
            identity = FirewallPolicyIdentity(**identity)
        if isinstance(insights, dict):
            insights = FirewallPolicyInsights(**insights)
        if isinstance(intrusion_detection, dict):
            intrusion_detection = FirewallPolicyIntrusionDetection(**intrusion_detection)
        if isinstance(threat_intelligence_allowlist, dict):
            threat_intelligence_allowlist = FirewallPolicyThreatIntelligenceAllowlistStruct(**threat_intelligence_allowlist)
        if isinstance(timeouts, dict):
            timeouts = FirewallPolicyTimeouts(**timeouts)
        if isinstance(tls_certificate, dict):
            tls_certificate = FirewallPolicyTlsCertificate(**tls_certificate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4214aca0a3fe6099b47839bebed2ea362590bce54ccb0eab2ead18f9c0b570)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument auto_learn_private_ranges_enabled", value=auto_learn_private_ranges_enabled, expected_type=type_hints["auto_learn_private_ranges_enabled"])
            check_type(argname="argument base_policy_id", value=base_policy_id, expected_type=type_hints["base_policy_id"])
            check_type(argname="argument dns", value=dns, expected_type=type_hints["dns"])
            check_type(argname="argument explicit_proxy", value=explicit_proxy, expected_type=type_hints["explicit_proxy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument insights", value=insights, expected_type=type_hints["insights"])
            check_type(argname="argument intrusion_detection", value=intrusion_detection, expected_type=type_hints["intrusion_detection"])
            check_type(argname="argument private_ip_ranges", value=private_ip_ranges, expected_type=type_hints["private_ip_ranges"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument sql_redirect_allowed", value=sql_redirect_allowed, expected_type=type_hints["sql_redirect_allowed"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument threat_intelligence_allowlist", value=threat_intelligence_allowlist, expected_type=type_hints["threat_intelligence_allowlist"])
            check_type(argname="argument threat_intelligence_mode", value=threat_intelligence_mode, expected_type=type_hints["threat_intelligence_mode"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tls_certificate", value=tls_certificate, expected_type=type_hints["tls_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if auto_learn_private_ranges_enabled is not None:
            self._values["auto_learn_private_ranges_enabled"] = auto_learn_private_ranges_enabled
        if base_policy_id is not None:
            self._values["base_policy_id"] = base_policy_id
        if dns is not None:
            self._values["dns"] = dns
        if explicit_proxy is not None:
            self._values["explicit_proxy"] = explicit_proxy
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if insights is not None:
            self._values["insights"] = insights
        if intrusion_detection is not None:
            self._values["intrusion_detection"] = intrusion_detection
        if private_ip_ranges is not None:
            self._values["private_ip_ranges"] = private_ip_ranges
        if sku is not None:
            self._values["sku"] = sku
        if sql_redirect_allowed is not None:
            self._values["sql_redirect_allowed"] = sql_redirect_allowed
        if tags is not None:
            self._values["tags"] = tags
        if threat_intelligence_allowlist is not None:
            self._values["threat_intelligence_allowlist"] = threat_intelligence_allowlist
        if threat_intelligence_mode is not None:
            self._values["threat_intelligence_mode"] = threat_intelligence_mode
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tls_certificate is not None:
            self._values["tls_certificate"] = tls_certificate

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#location FirewallPolicy#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#name FirewallPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#resource_group_name FirewallPolicy#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_learn_private_ranges_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#auto_learn_private_ranges_enabled FirewallPolicy#auto_learn_private_ranges_enabled}.'''
        result = self._values.get("auto_learn_private_ranges_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def base_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#base_policy_id FirewallPolicy#base_policy_id}.'''
        result = self._values.get("base_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns(self) -> typing.Optional["FirewallPolicyDns"]:
        '''dns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#dns FirewallPolicy#dns}
        '''
        result = self._values.get("dns")
        return typing.cast(typing.Optional["FirewallPolicyDns"], result)

    @builtins.property
    def explicit_proxy(self) -> typing.Optional["FirewallPolicyExplicitProxy"]:
        '''explicit_proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#explicit_proxy FirewallPolicy#explicit_proxy}
        '''
        result = self._values.get("explicit_proxy")
        return typing.cast(typing.Optional["FirewallPolicyExplicitProxy"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#id FirewallPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["FirewallPolicyIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#identity FirewallPolicy#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["FirewallPolicyIdentity"], result)

    @builtins.property
    def insights(self) -> typing.Optional["FirewallPolicyInsights"]:
        '''insights block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#insights FirewallPolicy#insights}
        '''
        result = self._values.get("insights")
        return typing.cast(typing.Optional["FirewallPolicyInsights"], result)

    @builtins.property
    def intrusion_detection(
        self,
    ) -> typing.Optional["FirewallPolicyIntrusionDetection"]:
        '''intrusion_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#intrusion_detection FirewallPolicy#intrusion_detection}
        '''
        result = self._values.get("intrusion_detection")
        return typing.cast(typing.Optional["FirewallPolicyIntrusionDetection"], result)

    @builtins.property
    def private_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#private_ip_ranges FirewallPolicy#private_ip_ranges}.'''
        result = self._values.get("private_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#sku FirewallPolicy#sku}.'''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_redirect_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#sql_redirect_allowed FirewallPolicy#sql_redirect_allowed}.'''
        result = self._values.get("sql_redirect_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#tags FirewallPolicy#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def threat_intelligence_allowlist(
        self,
    ) -> typing.Optional["FirewallPolicyThreatIntelligenceAllowlistStruct"]:
        '''threat_intelligence_allowlist block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#threat_intelligence_allowlist FirewallPolicy#threat_intelligence_allowlist}
        '''
        result = self._values.get("threat_intelligence_allowlist")
        return typing.cast(typing.Optional["FirewallPolicyThreatIntelligenceAllowlistStruct"], result)

    @builtins.property
    def threat_intelligence_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#threat_intelligence_mode FirewallPolicy#threat_intelligence_mode}.'''
        result = self._values.get("threat_intelligence_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FirewallPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#timeouts FirewallPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FirewallPolicyTimeouts"], result)

    @builtins.property
    def tls_certificate(self) -> typing.Optional["FirewallPolicyTlsCertificate"]:
        '''tls_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#tls_certificate FirewallPolicy#tls_certificate}
        '''
        result = self._values.get("tls_certificate")
        return typing.cast(typing.Optional["FirewallPolicyTlsCertificate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyDns",
    jsii_struct_bases=[],
    name_mapping={"proxy_enabled": "proxyEnabled", "servers": "servers"},
)
class FirewallPolicyDns:
    def __init__(
        self,
        *,
        proxy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param proxy_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#proxy_enabled FirewallPolicy#proxy_enabled}.
        :param servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#servers FirewallPolicy#servers}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6274ca3d14f0cafd9f5a178aa4593dd2387c473308012ac8a21ec3f59536ca3b)
            check_type(argname="argument proxy_enabled", value=proxy_enabled, expected_type=type_hints["proxy_enabled"])
            check_type(argname="argument servers", value=servers, expected_type=type_hints["servers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if proxy_enabled is not None:
            self._values["proxy_enabled"] = proxy_enabled
        if servers is not None:
            self._values["servers"] = servers

    @builtins.property
    def proxy_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#proxy_enabled FirewallPolicy#proxy_enabled}.'''
        result = self._values.get("proxy_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#servers FirewallPolicy#servers}.'''
        result = self._values.get("servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyDns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyDnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyDnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3208be2624c49814160a7ca2d55234e7075d7fa675225c32aec2629ea06ed2e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProxyEnabled")
    def reset_proxy_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyEnabled", []))

    @jsii.member(jsii_name="resetServers")
    def reset_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServers", []))

    @builtins.property
    @jsii.member(jsii_name="proxyEnabledInput")
    def proxy_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "proxyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="serversInput")
    def servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serversInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyEnabled")
    def proxy_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "proxyEnabled"))

    @proxy_enabled.setter
    def proxy_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d8075a192afdd62d4c3beb70c162991e0ba83d00ff7c37a4c531b9ba5a5f11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servers")
    def servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "servers"))

    @servers.setter
    def servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a26eaa4a24cfc36e2fefcf43c716d670c8c3b338d94778d3d6bb6175ed2769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirewallPolicyDns]:
        return typing.cast(typing.Optional[FirewallPolicyDns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FirewallPolicyDns]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff07d25e4e0aec57ef4df88ebf98f85a29a7b74a5413a188fb1cde22aa45b988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyExplicitProxy",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "enable_pac_file": "enablePacFile",
        "http_port": "httpPort",
        "https_port": "httpsPort",
        "pac_file": "pacFile",
        "pac_file_port": "pacFilePort",
    },
)
class FirewallPolicyExplicitProxy:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_pac_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        pac_file: typing.Optional[builtins.str] = None,
        pac_file_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#enabled FirewallPolicy#enabled}.
        :param enable_pac_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#enable_pac_file FirewallPolicy#enable_pac_file}.
        :param http_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#http_port FirewallPolicy#http_port}.
        :param https_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#https_port FirewallPolicy#https_port}.
        :param pac_file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#pac_file FirewallPolicy#pac_file}.
        :param pac_file_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#pac_file_port FirewallPolicy#pac_file_port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915ddfd751cb8a1b4cc61a28cdd9b60db26519f9eae7464a17c9ecde7978944a)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_pac_file", value=enable_pac_file, expected_type=type_hints["enable_pac_file"])
            check_type(argname="argument http_port", value=http_port, expected_type=type_hints["http_port"])
            check_type(argname="argument https_port", value=https_port, expected_type=type_hints["https_port"])
            check_type(argname="argument pac_file", value=pac_file, expected_type=type_hints["pac_file"])
            check_type(argname="argument pac_file_port", value=pac_file_port, expected_type=type_hints["pac_file_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_pac_file is not None:
            self._values["enable_pac_file"] = enable_pac_file
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port
        if pac_file is not None:
            self._values["pac_file"] = pac_file
        if pac_file_port is not None:
            self._values["pac_file_port"] = pac_file_port

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#enabled FirewallPolicy#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_pac_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#enable_pac_file FirewallPolicy#enable_pac_file}.'''
        result = self._values.get("enable_pac_file")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#http_port FirewallPolicy#http_port}.'''
        result = self._values.get("http_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#https_port FirewallPolicy#https_port}.'''
        result = self._values.get("https_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pac_file(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#pac_file FirewallPolicy#pac_file}.'''
        result = self._values.get("pac_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pac_file_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#pac_file_port FirewallPolicy#pac_file_port}.'''
        result = self._values.get("pac_file_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyExplicitProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyExplicitProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyExplicitProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d720be20ec9a86107314253105507030f03edac2ed0e902a45090291a920234)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnablePacFile")
    def reset_enable_pac_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePacFile", []))

    @jsii.member(jsii_name="resetHttpPort")
    def reset_http_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpPort", []))

    @jsii.member(jsii_name="resetHttpsPort")
    def reset_https_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsPort", []))

    @jsii.member(jsii_name="resetPacFile")
    def reset_pac_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPacFile", []))

    @jsii.member(jsii_name="resetPacFilePort")
    def reset_pac_file_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPacFilePort", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePacFileInput")
    def enable_pac_file_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePacFileInput"))

    @builtins.property
    @jsii.member(jsii_name="httpPortInput")
    def http_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpPortInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsPortInput")
    def https_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpsPortInput"))

    @builtins.property
    @jsii.member(jsii_name="pacFileInput")
    def pac_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pacFileInput"))

    @builtins.property
    @jsii.member(jsii_name="pacFilePortInput")
    def pac_file_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pacFilePortInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85078d4f4283221734255784dc555af6737326b82b02053c9ab190497e61c1ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePacFile")
    def enable_pac_file(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePacFile"))

    @enable_pac_file.setter
    def enable_pac_file(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd77e25657f8cb4a1c0322f30eb5970eb8af85fa14d9d32099928041dbc4c7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePacFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpPort")
    def http_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpPort"))

    @http_port.setter
    def http_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae459d0449e22220e586ffbca67a5dc762a10d27db2df126481b25a72924063b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsPort")
    def https_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpsPort"))

    @https_port.setter
    def https_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0842a1daf762cafe10dcca858d52a283bd48c6cb6fda2cae2dce8dddb3fe3a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pacFile")
    def pac_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pacFile"))

    @pac_file.setter
    def pac_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe28bcf5101c11b355c9b62e1ec2f985a9b6a54652d463d9fb9d29f5ce3b3430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pacFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pacFilePort")
    def pac_file_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pacFilePort"))

    @pac_file_port.setter
    def pac_file_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4f924b75ecf3841208a4a10ef6fdc06613c5bb487f0a28aff84ce3597fbc45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pacFilePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirewallPolicyExplicitProxy]:
        return typing.cast(typing.Optional[FirewallPolicyExplicitProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirewallPolicyExplicitProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57caaae5cb92fb8dccde4839ddc08e49f91d99bc96197d3f1995af11d8090fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class FirewallPolicyIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#type FirewallPolicy#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#identity_ids FirewallPolicy#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f08b51b31e8991f0d405c0ab1deda9b24abb1d76454717c7b2e7cc5320132d)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#type FirewallPolicy#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#identity_ids FirewallPolicy#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bfb4301834e295b2c7a83316331d93e1a89a08a9ec1cfc1ef09014043fb1872)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f2f043537e54e29458f75d3074eddc0c4bf3be17b1fd4642910bfb24032196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3863c7dbe99bf7b2f2856928c84b023eb531752b10bdc0433f2d58ae1b5585f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirewallPolicyIdentity]:
        return typing.cast(typing.Optional[FirewallPolicyIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FirewallPolicyIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a701b8779b0bcb9d5588ae2844e83e7d826b79dc4502ccb67f92f5a22c1ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyInsights",
    jsii_struct_bases=[],
    name_mapping={
        "default_log_analytics_workspace_id": "defaultLogAnalyticsWorkspaceId",
        "enabled": "enabled",
        "log_analytics_workspace": "logAnalyticsWorkspace",
        "retention_in_days": "retentionInDays",
    },
)
class FirewallPolicyInsights:
    def __init__(
        self,
        *,
        default_log_analytics_workspace_id: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_analytics_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirewallPolicyInsightsLogAnalyticsWorkspace", typing.Dict[builtins.str, typing.Any]]]]] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param default_log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#default_log_analytics_workspace_id FirewallPolicy#default_log_analytics_workspace_id}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#enabled FirewallPolicy#enabled}.
        :param log_analytics_workspace: log_analytics_workspace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#log_analytics_workspace FirewallPolicy#log_analytics_workspace}
        :param retention_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#retention_in_days FirewallPolicy#retention_in_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f192b7924ad221af543fd486d8e439beb428902b292269acb376ac116b8712)
            check_type(argname="argument default_log_analytics_workspace_id", value=default_log_analytics_workspace_id, expected_type=type_hints["default_log_analytics_workspace_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_analytics_workspace", value=log_analytics_workspace, expected_type=type_hints["log_analytics_workspace"])
            check_type(argname="argument retention_in_days", value=retention_in_days, expected_type=type_hints["retention_in_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_log_analytics_workspace_id": default_log_analytics_workspace_id,
            "enabled": enabled,
        }
        if log_analytics_workspace is not None:
            self._values["log_analytics_workspace"] = log_analytics_workspace
        if retention_in_days is not None:
            self._values["retention_in_days"] = retention_in_days

    @builtins.property
    def default_log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#default_log_analytics_workspace_id FirewallPolicy#default_log_analytics_workspace_id}.'''
        result = self._values.get("default_log_analytics_workspace_id")
        assert result is not None, "Required property 'default_log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#enabled FirewallPolicy#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_analytics_workspace(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyInsightsLogAnalyticsWorkspace"]]]:
        '''log_analytics_workspace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#log_analytics_workspace FirewallPolicy#log_analytics_workspace}
        '''
        result = self._values.get("log_analytics_workspace")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyInsightsLogAnalyticsWorkspace"]]], result)

    @builtins.property
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#retention_in_days FirewallPolicy#retention_in_days}.'''
        result = self._values.get("retention_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyInsights(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyInsightsLogAnalyticsWorkspace",
    jsii_struct_bases=[],
    name_mapping={"firewall_location": "firewallLocation", "id": "id"},
)
class FirewallPolicyInsightsLogAnalyticsWorkspace:
    def __init__(self, *, firewall_location: builtins.str, id: builtins.str) -> None:
        '''
        :param firewall_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#firewall_location FirewallPolicy#firewall_location}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#id FirewallPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2cddac0de5522459bb6cd4e11d7b1a744fce0ea22937321b5368f3e8d83f5ac)
            check_type(argname="argument firewall_location", value=firewall_location, expected_type=type_hints["firewall_location"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firewall_location": firewall_location,
            "id": id,
        }

    @builtins.property
    def firewall_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#firewall_location FirewallPolicy#firewall_location}.'''
        result = self._values.get("firewall_location")
        assert result is not None, "Required property 'firewall_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#id FirewallPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyInsightsLogAnalyticsWorkspace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyInsightsLogAnalyticsWorkspaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyInsightsLogAnalyticsWorkspaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8a509a6d0055b58e6c6738a85417998aee1cbc42d452c4165582ca54c1f3c41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirewallPolicyInsightsLogAnalyticsWorkspaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d42315165867d0d2758141d91c71b66f992d5e981536ef9499d4964152255a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirewallPolicyInsightsLogAnalyticsWorkspaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b8e99b30e97c8788158e9bbce5c1b79443dce92721861712d7fbe752a50ad9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0ced3ece871d6e0452205870ba3965d7b4952a6f0334bfdebb3d0f7107b3fb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9fd170196ceff400b0755c0554669f16796594c37ec96cf499040aabd52d0f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyInsightsLogAnalyticsWorkspace]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyInsightsLogAnalyticsWorkspace]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyInsightsLogAnalyticsWorkspace]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde4691dc74c27b65e410807bff45aa18b5eb8102307faea0e81b527f1c9001f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirewallPolicyInsightsLogAnalyticsWorkspaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyInsightsLogAnalyticsWorkspaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78b68cdf02994e0a384723812a4f443d65d36f46a5d083ba6f50412563176307)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="firewallLocationInput")
    def firewall_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallLocation")
    def firewall_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallLocation"))

    @firewall_location.setter
    def firewall_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bab1b4f2b9a47960a583bd19e69ec5aca3ed69eaa654132fd3027e7c6d29119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a966bfb32f31feffae9391c23237958990505091f7828c8c99e722fbed233a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyInsightsLogAnalyticsWorkspace]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyInsightsLogAnalyticsWorkspace]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyInsightsLogAnalyticsWorkspace]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0387b8c3ce208b6586721f829cb58fa5ba446363f14747068fe754eb213488c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirewallPolicyInsightsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyInsightsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dfb7162f96b871c764980e2a4b3da3d2fa8e2a0e53e22c08a926ec4158db8d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLogAnalyticsWorkspace")
    def put_log_analytics_workspace(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirewallPolicyInsightsLogAnalyticsWorkspace, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1023bde0bcb075a531bac6713737a0230b3754a347346f38a3545302e3c31d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogAnalyticsWorkspace", [value]))

    @jsii.member(jsii_name="resetLogAnalyticsWorkspace")
    def reset_log_analytics_workspace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsWorkspace", []))

    @jsii.member(jsii_name="resetRetentionInDays")
    def reset_retention_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionInDays", []))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspace")
    def log_analytics_workspace(
        self,
    ) -> FirewallPolicyInsightsLogAnalyticsWorkspaceList:
        return typing.cast(FirewallPolicyInsightsLogAnalyticsWorkspaceList, jsii.get(self, "logAnalyticsWorkspace"))

    @builtins.property
    @jsii.member(jsii_name="defaultLogAnalyticsWorkspaceIdInput")
    def default_log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLogAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceInput")
    def log_analytics_workspace_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyInsightsLogAnalyticsWorkspace]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyInsightsLogAnalyticsWorkspace]]], jsii.get(self, "logAnalyticsWorkspaceInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionInDaysInput")
    def retention_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLogAnalyticsWorkspaceId")
    def default_log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLogAnalyticsWorkspaceId"))

    @default_log_analytics_workspace_id.setter
    def default_log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ecdb265b3a3f2dc8dde12ca82a50a60e15072b6eb8aed33e3a727d29c2aaf1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLogAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795eaf52a3cad7bb02b279ddabed6ee03d167a8fe286dfe61a2a753cebe66e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionInDays")
    def retention_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionInDays"))

    @retention_in_days.setter
    def retention_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef5c32c576794937b63ffcf6689c9ed257bae8527da634a8f75253e8195293e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirewallPolicyInsights]:
        return typing.cast(typing.Optional[FirewallPolicyInsights], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FirewallPolicyInsights]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f897b01d3d6a3c561e7f17633c0a729e02508a3885d4648258c751ffea7137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIntrusionDetection",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "private_ranges": "privateRanges",
        "signature_overrides": "signatureOverrides",
        "traffic_bypass": "trafficBypass",
    },
)
class FirewallPolicyIntrusionDetection:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        private_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        signature_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirewallPolicyIntrusionDetectionSignatureOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        traffic_bypass: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirewallPolicyIntrusionDetectionTrafficBypass", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#mode FirewallPolicy#mode}.
        :param private_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#private_ranges FirewallPolicy#private_ranges}.
        :param signature_overrides: signature_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#signature_overrides FirewallPolicy#signature_overrides}
        :param traffic_bypass: traffic_bypass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#traffic_bypass FirewallPolicy#traffic_bypass}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f3d5a771fa9830b444599be942d50c5b9c2a5bbd828fbadb728d347df93b09)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument private_ranges", value=private_ranges, expected_type=type_hints["private_ranges"])
            check_type(argname="argument signature_overrides", value=signature_overrides, expected_type=type_hints["signature_overrides"])
            check_type(argname="argument traffic_bypass", value=traffic_bypass, expected_type=type_hints["traffic_bypass"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if private_ranges is not None:
            self._values["private_ranges"] = private_ranges
        if signature_overrides is not None:
            self._values["signature_overrides"] = signature_overrides
        if traffic_bypass is not None:
            self._values["traffic_bypass"] = traffic_bypass

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#mode FirewallPolicy#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#private_ranges FirewallPolicy#private_ranges}.'''
        result = self._values.get("private_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def signature_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyIntrusionDetectionSignatureOverrides"]]]:
        '''signature_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#signature_overrides FirewallPolicy#signature_overrides}
        '''
        result = self._values.get("signature_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyIntrusionDetectionSignatureOverrides"]]], result)

    @builtins.property
    def traffic_bypass(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyIntrusionDetectionTrafficBypass"]]]:
        '''traffic_bypass block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#traffic_bypass FirewallPolicy#traffic_bypass}
        '''
        result = self._values.get("traffic_bypass")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyIntrusionDetectionTrafficBypass"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyIntrusionDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyIntrusionDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIntrusionDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dab2b3850364e2ad9ef7856ef673575b59eeace46f523fba95e108914df066e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSignatureOverrides")
    def put_signature_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirewallPolicyIntrusionDetectionSignatureOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8dd0ff43387f352b9000e13afe4f0e6da406ab7054aa3ed94683e6bf3f92301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSignatureOverrides", [value]))

    @jsii.member(jsii_name="putTrafficBypass")
    def put_traffic_bypass(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirewallPolicyIntrusionDetectionTrafficBypass", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ab181c36267e4c9fb5f1aea58d60a86329c05bed8c0df4f81564d194e261a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrafficBypass", [value]))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetPrivateRanges")
    def reset_private_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateRanges", []))

    @jsii.member(jsii_name="resetSignatureOverrides")
    def reset_signature_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignatureOverrides", []))

    @jsii.member(jsii_name="resetTrafficBypass")
    def reset_traffic_bypass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficBypass", []))

    @builtins.property
    @jsii.member(jsii_name="signatureOverrides")
    def signature_overrides(
        self,
    ) -> "FirewallPolicyIntrusionDetectionSignatureOverridesList":
        return typing.cast("FirewallPolicyIntrusionDetectionSignatureOverridesList", jsii.get(self, "signatureOverrides"))

    @builtins.property
    @jsii.member(jsii_name="trafficBypass")
    def traffic_bypass(self) -> "FirewallPolicyIntrusionDetectionTrafficBypassList":
        return typing.cast("FirewallPolicyIntrusionDetectionTrafficBypassList", jsii.get(self, "trafficBypass"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="privateRangesInput")
    def private_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "privateRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="signatureOverridesInput")
    def signature_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyIntrusionDetectionSignatureOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyIntrusionDetectionSignatureOverrides"]]], jsii.get(self, "signatureOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficBypassInput")
    def traffic_bypass_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyIntrusionDetectionTrafficBypass"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirewallPolicyIntrusionDetectionTrafficBypass"]]], jsii.get(self, "trafficBypassInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468e4406563916bb4758ee41ce1a0872ebb853dca32041ff523c575d635641d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateRanges")
    def private_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateRanges"))

    @private_ranges.setter
    def private_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4445b7a52392dbb7cc547c92d6cae3ba1deb545fcba02db6097be261bbb31f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirewallPolicyIntrusionDetection]:
        return typing.cast(typing.Optional[FirewallPolicyIntrusionDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirewallPolicyIntrusionDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c92326ab88a073e717f0bef895d6abc001b15c8de128f5a7cb6b6d6f763adab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIntrusionDetectionSignatureOverrides",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "state": "state"},
)
class FirewallPolicyIntrusionDetectionSignatureOverrides:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#id FirewallPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#state FirewallPolicy#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08f9491697c42a9d84c5643f220013f2ad75d888405ad1bd66f623d0cd60948)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#id FirewallPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#state FirewallPolicy#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyIntrusionDetectionSignatureOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyIntrusionDetectionSignatureOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIntrusionDetectionSignatureOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a5e6144edfe4ca040d0849a875ebbfe8d29c05fe3b5ea7bbf7a849700e78755)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirewallPolicyIntrusionDetectionSignatureOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ebfa6ed0c9e52aeead2d858f3d0909ca51b99d3d716612d30d9dea36111eb6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirewallPolicyIntrusionDetectionSignatureOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97fc9845b64579613feb87acc3730e460dde47716976de9ee13a77cc807f056c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d75013945504067ad7ee4315af6deb96f2a8929ac316e7e952678215952d6ed6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f38da8d67b938161ec81bf567c6f0aa9bff630f7af088f9e6c045ef0796ba1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyIntrusionDetectionSignatureOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyIntrusionDetectionSignatureOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyIntrusionDetectionSignatureOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b1d0f8587e9580ae5509d966525162a420d21d7ba361f845f92db870e91c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirewallPolicyIntrusionDetectionSignatureOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIntrusionDetectionSignatureOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c8e383626b7db0cd29871b58598de471aa5e3f81e77ec7793d6ba360db814a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b0aa6c21153202ee66ee13302f41a905d3eeb1264e4689823993e3a7820d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d904d5f46998e16bab7e27611b5ef6376f4b0587d27203c6cf45885127c8d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyIntrusionDetectionSignatureOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyIntrusionDetectionSignatureOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyIntrusionDetectionSignatureOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed0a7fdeb4ee876fde7fa1c4c96f5dcd7cef9b86b13b79567a3bd82fcbf7a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIntrusionDetectionTrafficBypass",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "protocol": "protocol",
        "description": "description",
        "destination_addresses": "destinationAddresses",
        "destination_ip_groups": "destinationIpGroups",
        "destination_ports": "destinationPorts",
        "source_addresses": "sourceAddresses",
        "source_ip_groups": "sourceIpGroups",
    },
)
class FirewallPolicyIntrusionDetectionTrafficBypass:
    def __init__(
        self,
        *,
        name: builtins.str,
        protocol: builtins.str,
        description: typing.Optional[builtins.str] = None,
        destination_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination_ip_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#name FirewallPolicy#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#protocol FirewallPolicy#protocol}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#description FirewallPolicy#description}.
        :param destination_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#destination_addresses FirewallPolicy#destination_addresses}.
        :param destination_ip_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#destination_ip_groups FirewallPolicy#destination_ip_groups}.
        :param destination_ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#destination_ports FirewallPolicy#destination_ports}.
        :param source_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#source_addresses FirewallPolicy#source_addresses}.
        :param source_ip_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#source_ip_groups FirewallPolicy#source_ip_groups}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf86781917a240e35c5efd532139e67cd2b40e8cbf929f3c4efade9ebcc92796)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_addresses", value=destination_addresses, expected_type=type_hints["destination_addresses"])
            check_type(argname="argument destination_ip_groups", value=destination_ip_groups, expected_type=type_hints["destination_ip_groups"])
            check_type(argname="argument destination_ports", value=destination_ports, expected_type=type_hints["destination_ports"])
            check_type(argname="argument source_addresses", value=source_addresses, expected_type=type_hints["source_addresses"])
            check_type(argname="argument source_ip_groups", value=source_ip_groups, expected_type=type_hints["source_ip_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "protocol": protocol,
        }
        if description is not None:
            self._values["description"] = description
        if destination_addresses is not None:
            self._values["destination_addresses"] = destination_addresses
        if destination_ip_groups is not None:
            self._values["destination_ip_groups"] = destination_ip_groups
        if destination_ports is not None:
            self._values["destination_ports"] = destination_ports
        if source_addresses is not None:
            self._values["source_addresses"] = source_addresses
        if source_ip_groups is not None:
            self._values["source_ip_groups"] = source_ip_groups

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#name FirewallPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#protocol FirewallPolicy#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#description FirewallPolicy#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#destination_addresses FirewallPolicy#destination_addresses}.'''
        result = self._values.get("destination_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def destination_ip_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#destination_ip_groups FirewallPolicy#destination_ip_groups}.'''
        result = self._values.get("destination_ip_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def destination_ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#destination_ports FirewallPolicy#destination_ports}.'''
        result = self._values.get("destination_ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#source_addresses FirewallPolicy#source_addresses}.'''
        result = self._values.get("source_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_ip_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#source_ip_groups FirewallPolicy#source_ip_groups}.'''
        result = self._values.get("source_ip_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyIntrusionDetectionTrafficBypass(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyIntrusionDetectionTrafficBypassList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIntrusionDetectionTrafficBypassList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94b2f87ee23d1bdcb3b9f21bb789980fef2faa55baf919703fc2fea20c93f597)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirewallPolicyIntrusionDetectionTrafficBypassOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a484ea2c63aab565aa8af38bfc9a4b64999d6b37ef5d34a877662e5ec14577)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirewallPolicyIntrusionDetectionTrafficBypassOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__707e0e1d1195eb9955255fd9da9b3beffdbb940d1a14b738109913de8e88eb62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f66b226276ce242ed72db5820fda4e3e6dba37acbd5a84f953f97b45e40c2494)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bca4fddafd177cd1271428e15a6083adf7476369ad4daf9465ac6c9c5601a05c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyIntrusionDetectionTrafficBypass]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyIntrusionDetectionTrafficBypass]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyIntrusionDetectionTrafficBypass]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c09ae7f01d90dc7f6aec581c54b8c2edda3b492cc7949b76d1c162a51674c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirewallPolicyIntrusionDetectionTrafficBypassOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyIntrusionDetectionTrafficBypassOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__683b40c828b96e90318b25e7674b18f2e8f25849a858346d8f66ced611e2744d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDestinationAddresses")
    def reset_destination_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationAddresses", []))

    @jsii.member(jsii_name="resetDestinationIpGroups")
    def reset_destination_ip_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationIpGroups", []))

    @jsii.member(jsii_name="resetDestinationPorts")
    def reset_destination_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationPorts", []))

    @jsii.member(jsii_name="resetSourceAddresses")
    def reset_source_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceAddresses", []))

    @jsii.member(jsii_name="resetSourceIpGroups")
    def reset_source_ip_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceIpGroups", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationAddressesInput")
    def destination_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationIpGroupsInput")
    def destination_ip_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationIpGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPortsInput")
    def destination_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceAddressesInput")
    def source_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIpGroupsInput")
    def source_ip_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceIpGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36dbc7fdba58bf7defc692866605f8d2ae31302af1b09d345be5b65e2e404ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationAddresses")
    def destination_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationAddresses"))

    @destination_addresses.setter
    def destination_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a2ba176bb0c29a2b1f9a3a94c5eb954d3298a7c80c221fca4e83d2c26745dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationIpGroups")
    def destination_ip_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationIpGroups"))

    @destination_ip_groups.setter
    def destination_ip_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125b4909f8024f309d2804c61f34266d69ddcebf6c39e6c030527ce519edaddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationIpGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationPorts")
    def destination_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationPorts"))

    @destination_ports.setter
    def destination_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9af4f679a51fa226c6b1e38ba76a1c9116d78f3d05f5337334394949e30e401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f974c3f2dfb4dd27dc7b987a94c1c6c8ee8b32ea6bb2c81a0d2168e298006e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101f8a6cc4cf69ef1265ac45dc152074fcebe73a78c67d4fb61b7fe872399555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceAddresses")
    def source_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceAddresses"))

    @source_addresses.setter
    def source_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d13f558236c6be77e66186b9d72606e0c7f315268c4e3c938a5bc884a49f788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceIpGroups")
    def source_ip_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceIpGroups"))

    @source_ip_groups.setter
    def source_ip_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e6690bed4791633709fe4acdb7329f66dc78d84d5e8ae6ed5972fd9ac10c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIpGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyIntrusionDetectionTrafficBypass]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyIntrusionDetectionTrafficBypass]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyIntrusionDetectionTrafficBypass]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3932785105a6a7b12925a3420ddefda34ccb5b7d3178a1af8eef6b50a2fd07e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyThreatIntelligenceAllowlistStruct",
    jsii_struct_bases=[],
    name_mapping={"fqdns": "fqdns", "ip_addresses": "ipAddresses"},
)
class FirewallPolicyThreatIntelligenceAllowlistStruct:
    def __init__(
        self,
        *,
        fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param fqdns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#fqdns FirewallPolicy#fqdns}.
        :param ip_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#ip_addresses FirewallPolicy#ip_addresses}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae85f2896b303ff4feb10528b5ec91181c2f244bf1133ffbdccfdbad64c96e26)
            check_type(argname="argument fqdns", value=fqdns, expected_type=type_hints["fqdns"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fqdns is not None:
            self._values["fqdns"] = fqdns
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses

    @builtins.property
    def fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#fqdns FirewallPolicy#fqdns}.'''
        result = self._values.get("fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#ip_addresses FirewallPolicy#ip_addresses}.'''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyThreatIntelligenceAllowlistStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyThreatIntelligenceAllowlistStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyThreatIntelligenceAllowlistStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97097e971fd608dc011ed87329111925141865d9b6668663837fc1cb47f21096)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFqdns")
    def reset_fqdns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFqdns", []))

    @jsii.member(jsii_name="resetIpAddresses")
    def reset_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddresses", []))

    @builtins.property
    @jsii.member(jsii_name="fqdnsInput")
    def fqdns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fqdnsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressesInput")
    def ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdns")
    def fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fqdns"))

    @fqdns.setter
    def fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71904c88c891129597740f39fa268303194205f7d60dccab09988670d5e42635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea06c1738cf4b9cc19e5c2fa24a1b480397b156e47cbf002e33bc2a2d077c902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirewallPolicyThreatIntelligenceAllowlistStruct]:
        return typing.cast(typing.Optional[FirewallPolicyThreatIntelligenceAllowlistStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirewallPolicyThreatIntelligenceAllowlistStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d373099ac4f879858dbbb3809541c6cce345564409e9713c05401364c7aabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class FirewallPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#create FirewallPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#delete FirewallPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#read FirewallPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#update FirewallPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56d3f3749a2ab7e352a9e812a8b3f4b5b4dd88e1ed2d063104fc834925da85b)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#create FirewallPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#delete FirewallPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#read FirewallPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#update FirewallPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dedc87024d65f03964c7ff5cbb845b9cfa12fe689c049cd6a0158e23a615744a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1a55dfe77d3bf24c1e9ea4708174e4680127cbbf69a6214652e6629694fdc20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b359ed5916cb7cd2df6b9ae3c425876aaa054d73fce0fa9806b69a214f38919b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42636a6b8dd1fe65a5755546793640e0af84e33a6bd9f6b857d2b0a57930cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812fb3fa74ed7c51ca1dcb7d03de04a0db84026fdfd9e3de0527f85e5c01b18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd6bffeb1ff6426a2520ba176f72c14ce4374502432ef7129d3c2d119ae7edea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyTlsCertificate",
    jsii_struct_bases=[],
    name_mapping={"key_vault_secret_id": "keyVaultSecretId", "name": "name"},
)
class FirewallPolicyTlsCertificate:
    def __init__(
        self,
        *,
        key_vault_secret_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param key_vault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#key_vault_secret_id FirewallPolicy#key_vault_secret_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#name FirewallPolicy#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d663d173b8230bbd3cc632c6b37a09d567512037870905363a0da79a731c2b0c)
            check_type(argname="argument key_vault_secret_id", value=key_vault_secret_id, expected_type=type_hints["key_vault_secret_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_vault_secret_id": key_vault_secret_id,
            "name": name,
        }

    @builtins.property
    def key_vault_secret_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#key_vault_secret_id FirewallPolicy#key_vault_secret_id}.'''
        result = self._values.get("key_vault_secret_id")
        assert result is not None, "Required property 'key_vault_secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/firewall_policy#name FirewallPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallPolicyTlsCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallPolicyTlsCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.firewallPolicy.FirewallPolicyTlsCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd1890df9e5300610238c47874fc749f1360377d5d64d45dcbd8529adf85642c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretIdInput")
    def key_vault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretId")
    def key_vault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultSecretId"))

    @key_vault_secret_id.setter
    def key_vault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5ecca41a79978ec3a19ac7088919a67a39e0daa8930173eedb9de7f64ba4cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d157a654119baf6bea97c6802f1ca1b8832bdcf2771d2db4b0f9305d827b99e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirewallPolicyTlsCertificate]:
        return typing.cast(typing.Optional[FirewallPolicyTlsCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirewallPolicyTlsCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397f991e5c5ea74e41d91ccac7343a6b34c346398dbb355b5fc6d95551de9c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FirewallPolicy",
    "FirewallPolicyConfig",
    "FirewallPolicyDns",
    "FirewallPolicyDnsOutputReference",
    "FirewallPolicyExplicitProxy",
    "FirewallPolicyExplicitProxyOutputReference",
    "FirewallPolicyIdentity",
    "FirewallPolicyIdentityOutputReference",
    "FirewallPolicyInsights",
    "FirewallPolicyInsightsLogAnalyticsWorkspace",
    "FirewallPolicyInsightsLogAnalyticsWorkspaceList",
    "FirewallPolicyInsightsLogAnalyticsWorkspaceOutputReference",
    "FirewallPolicyInsightsOutputReference",
    "FirewallPolicyIntrusionDetection",
    "FirewallPolicyIntrusionDetectionOutputReference",
    "FirewallPolicyIntrusionDetectionSignatureOverrides",
    "FirewallPolicyIntrusionDetectionSignatureOverridesList",
    "FirewallPolicyIntrusionDetectionSignatureOverridesOutputReference",
    "FirewallPolicyIntrusionDetectionTrafficBypass",
    "FirewallPolicyIntrusionDetectionTrafficBypassList",
    "FirewallPolicyIntrusionDetectionTrafficBypassOutputReference",
    "FirewallPolicyThreatIntelligenceAllowlistStruct",
    "FirewallPolicyThreatIntelligenceAllowlistStructOutputReference",
    "FirewallPolicyTimeouts",
    "FirewallPolicyTimeoutsOutputReference",
    "FirewallPolicyTlsCertificate",
    "FirewallPolicyTlsCertificateOutputReference",
]

publication.publish()

def _typecheckingstub__019c06c2a343ec961e5f9c63ef1b04cb321fc4369a208a1bb8b370a1e2bedc22(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    auto_learn_private_ranges_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    base_policy_id: typing.Optional[builtins.str] = None,
    dns: typing.Optional[typing.Union[FirewallPolicyDns, typing.Dict[builtins.str, typing.Any]]] = None,
    explicit_proxy: typing.Optional[typing.Union[FirewallPolicyExplicitProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[FirewallPolicyIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    insights: typing.Optional[typing.Union[FirewallPolicyInsights, typing.Dict[builtins.str, typing.Any]]] = None,
    intrusion_detection: typing.Optional[typing.Union[FirewallPolicyIntrusionDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    private_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    sku: typing.Optional[builtins.str] = None,
    sql_redirect_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    threat_intelligence_allowlist: typing.Optional[typing.Union[FirewallPolicyThreatIntelligenceAllowlistStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    threat_intelligence_mode: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[FirewallPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_certificate: typing.Optional[typing.Union[FirewallPolicyTlsCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__aa2b555550016130bd89aa9ea4a4925638d7b646d20671b6165240ce565e1890(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c1a0bd6522b82dbeb38bdf7f2071756093d676a0752fe7337fb7039853810a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6079777f07a9a13dcadd808117da9451ce3418171d530c7eb9b82a6039963be7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab70562142c6dfd5199aeb1510f6812e44e62f17f1686757c30a7e594dfcc67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d79c130ba1291c262e02a2a44e143d1bd882d184360b9075fa4a2353de6e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cad2a4ee2bc0524213493e0968b8b59786e4aab41441a0f11e8b39eed190351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39e1e146541c2a3039004b33860fc4f81e3cde442b30c0a0a162de7d4c252c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ce5f2de8bd518606fd19dec07647e96ef72fa474b055075b80e56cd2eb85c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4728786bf923ae3f345633739f02687aa2b125d39321f5db26a7b91ad0a7c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c42885f4f996c8614d0506ea512c50528161d20246009fbfca738a4a670c732(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e1b7f79349b0ae49eaa5c727ccb9571b5f4a6040402bd5a477aa025373b834(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244fecbf8ee2c77bf98589361e1eb0ae30c8932e8525627365b2b003a2a332ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4214aca0a3fe6099b47839bebed2ea362590bce54ccb0eab2ead18f9c0b570(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    auto_learn_private_ranges_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    base_policy_id: typing.Optional[builtins.str] = None,
    dns: typing.Optional[typing.Union[FirewallPolicyDns, typing.Dict[builtins.str, typing.Any]]] = None,
    explicit_proxy: typing.Optional[typing.Union[FirewallPolicyExplicitProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[FirewallPolicyIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    insights: typing.Optional[typing.Union[FirewallPolicyInsights, typing.Dict[builtins.str, typing.Any]]] = None,
    intrusion_detection: typing.Optional[typing.Union[FirewallPolicyIntrusionDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    private_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    sku: typing.Optional[builtins.str] = None,
    sql_redirect_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    threat_intelligence_allowlist: typing.Optional[typing.Union[FirewallPolicyThreatIntelligenceAllowlistStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    threat_intelligence_mode: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[FirewallPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_certificate: typing.Optional[typing.Union[FirewallPolicyTlsCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6274ca3d14f0cafd9f5a178aa4593dd2387c473308012ac8a21ec3f59536ca3b(
    *,
    proxy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    servers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3208be2624c49814160a7ca2d55234e7075d7fa675225c32aec2629ea06ed2e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d8075a192afdd62d4c3beb70c162991e0ba83d00ff7c37a4c531b9ba5a5f11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a26eaa4a24cfc36e2fefcf43c716d670c8c3b338d94778d3d6bb6175ed2769(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff07d25e4e0aec57ef4df88ebf98f85a29a7b74a5413a188fb1cde22aa45b988(
    value: typing.Optional[FirewallPolicyDns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915ddfd751cb8a1b4cc61a28cdd9b60db26519f9eae7464a17c9ecde7978944a(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_pac_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_port: typing.Optional[jsii.Number] = None,
    https_port: typing.Optional[jsii.Number] = None,
    pac_file: typing.Optional[builtins.str] = None,
    pac_file_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d720be20ec9a86107314253105507030f03edac2ed0e902a45090291a920234(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85078d4f4283221734255784dc555af6737326b82b02053c9ab190497e61c1ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd77e25657f8cb4a1c0322f30eb5970eb8af85fa14d9d32099928041dbc4c7bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae459d0449e22220e586ffbca67a5dc762a10d27db2df126481b25a72924063b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0842a1daf762cafe10dcca858d52a283bd48c6cb6fda2cae2dce8dddb3fe3a9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe28bcf5101c11b355c9b62e1ec2f985a9b6a54652d463d9fb9d29f5ce3b3430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4f924b75ecf3841208a4a10ef6fdc06613c5bb487f0a28aff84ce3597fbc45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57caaae5cb92fb8dccde4839ddc08e49f91d99bc96197d3f1995af11d8090fa(
    value: typing.Optional[FirewallPolicyExplicitProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f08b51b31e8991f0d405c0ab1deda9b24abb1d76454717c7b2e7cc5320132d(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfb4301834e295b2c7a83316331d93e1a89a08a9ec1cfc1ef09014043fb1872(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f2f043537e54e29458f75d3074eddc0c4bf3be17b1fd4642910bfb24032196(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3863c7dbe99bf7b2f2856928c84b023eb531752b10bdc0433f2d58ae1b5585f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a701b8779b0bcb9d5588ae2844e83e7d826b79dc4502ccb67f92f5a22c1ef2(
    value: typing.Optional[FirewallPolicyIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f192b7924ad221af543fd486d8e439beb428902b292269acb376ac116b8712(
    *,
    default_log_analytics_workspace_id: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_analytics_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirewallPolicyInsightsLogAnalyticsWorkspace, typing.Dict[builtins.str, typing.Any]]]]] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2cddac0de5522459bb6cd4e11d7b1a744fce0ea22937321b5368f3e8d83f5ac(
    *,
    firewall_location: builtins.str,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a509a6d0055b58e6c6738a85417998aee1cbc42d452c4165582ca54c1f3c41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d42315165867d0d2758141d91c71b66f992d5e981536ef9499d4964152255a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b8e99b30e97c8788158e9bbce5c1b79443dce92721861712d7fbe752a50ad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ced3ece871d6e0452205870ba3965d7b4952a6f0334bfdebb3d0f7107b3fb1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fd170196ceff400b0755c0554669f16796594c37ec96cf499040aabd52d0f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde4691dc74c27b65e410807bff45aa18b5eb8102307faea0e81b527f1c9001f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyInsightsLogAnalyticsWorkspace]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b68cdf02994e0a384723812a4f443d65d36f46a5d083ba6f50412563176307(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bab1b4f2b9a47960a583bd19e69ec5aca3ed69eaa654132fd3027e7c6d29119(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a966bfb32f31feffae9391c23237958990505091f7828c8c99e722fbed233a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0387b8c3ce208b6586721f829cb58fa5ba446363f14747068fe754eb213488c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyInsightsLogAnalyticsWorkspace]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfb7162f96b871c764980e2a4b3da3d2fa8e2a0e53e22c08a926ec4158db8d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1023bde0bcb075a531bac6713737a0230b3754a347346f38a3545302e3c31d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirewallPolicyInsightsLogAnalyticsWorkspace, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecdb265b3a3f2dc8dde12ca82a50a60e15072b6eb8aed33e3a727d29c2aaf1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795eaf52a3cad7bb02b279ddabed6ee03d167a8fe286dfe61a2a753cebe66e00(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef5c32c576794937b63ffcf6689c9ed257bae8527da634a8f75253e8195293e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f897b01d3d6a3c561e7f17633c0a729e02508a3885d4648258c751ffea7137(
    value: typing.Optional[FirewallPolicyInsights],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f3d5a771fa9830b444599be942d50c5b9c2a5bbd828fbadb728d347df93b09(
    *,
    mode: typing.Optional[builtins.str] = None,
    private_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    signature_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirewallPolicyIntrusionDetectionSignatureOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    traffic_bypass: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirewallPolicyIntrusionDetectionTrafficBypass, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dab2b3850364e2ad9ef7856ef673575b59eeace46f523fba95e108914df066e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8dd0ff43387f352b9000e13afe4f0e6da406ab7054aa3ed94683e6bf3f92301(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirewallPolicyIntrusionDetectionSignatureOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ab181c36267e4c9fb5f1aea58d60a86329c05bed8c0df4f81564d194e261a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirewallPolicyIntrusionDetectionTrafficBypass, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468e4406563916bb4758ee41ce1a0872ebb853dca32041ff523c575d635641d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4445b7a52392dbb7cc547c92d6cae3ba1deb545fcba02db6097be261bbb31f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c92326ab88a073e717f0bef895d6abc001b15c8de128f5a7cb6b6d6f763adab(
    value: typing.Optional[FirewallPolicyIntrusionDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08f9491697c42a9d84c5643f220013f2ad75d888405ad1bd66f623d0cd60948(
    *,
    id: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5e6144edfe4ca040d0849a875ebbfe8d29c05fe3b5ea7bbf7a849700e78755(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ebfa6ed0c9e52aeead2d858f3d0909ca51b99d3d716612d30d9dea36111eb6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97fc9845b64579613feb87acc3730e460dde47716976de9ee13a77cc807f056c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75013945504067ad7ee4315af6deb96f2a8929ac316e7e952678215952d6ed6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f38da8d67b938161ec81bf567c6f0aa9bff630f7af088f9e6c045ef0796ba1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b1d0f8587e9580ae5509d966525162a420d21d7ba361f845f92db870e91c91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyIntrusionDetectionSignatureOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c8e383626b7db0cd29871b58598de471aa5e3f81e77ec7793d6ba360db814a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b0aa6c21153202ee66ee13302f41a905d3eeb1264e4689823993e3a7820d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d904d5f46998e16bab7e27611b5ef6376f4b0587d27203c6cf45885127c8d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed0a7fdeb4ee876fde7fa1c4c96f5dcd7cef9b86b13b79567a3bd82fcbf7a8a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyIntrusionDetectionSignatureOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf86781917a240e35c5efd532139e67cd2b40e8cbf929f3c4efade9ebcc92796(
    *,
    name: builtins.str,
    protocol: builtins.str,
    description: typing.Optional[builtins.str] = None,
    destination_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination_ip_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b2f87ee23d1bdcb3b9f21bb789980fef2faa55baf919703fc2fea20c93f597(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a484ea2c63aab565aa8af38bfc9a4b64999d6b37ef5d34a877662e5ec14577(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707e0e1d1195eb9955255fd9da9b3beffdbb940d1a14b738109913de8e88eb62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66b226276ce242ed72db5820fda4e3e6dba37acbd5a84f953f97b45e40c2494(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca4fddafd177cd1271428e15a6083adf7476369ad4daf9465ac6c9c5601a05c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c09ae7f01d90dc7f6aec581c54b8c2edda3b492cc7949b76d1c162a51674c51(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirewallPolicyIntrusionDetectionTrafficBypass]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683b40c828b96e90318b25e7674b18f2e8f25849a858346d8f66ced611e2744d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36dbc7fdba58bf7defc692866605f8d2ae31302af1b09d345be5b65e2e404ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a2ba176bb0c29a2b1f9a3a94c5eb954d3298a7c80c221fca4e83d2c26745dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125b4909f8024f309d2804c61f34266d69ddcebf6c39e6c030527ce519edaddb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9af4f679a51fa226c6b1e38ba76a1c9116d78f3d05f5337334394949e30e401(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f974c3f2dfb4dd27dc7b987a94c1c6c8ee8b32ea6bb2c81a0d2168e298006e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101f8a6cc4cf69ef1265ac45dc152074fcebe73a78c67d4fb61b7fe872399555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d13f558236c6be77e66186b9d72606e0c7f315268c4e3c938a5bc884a49f788(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e6690bed4791633709fe4acdb7329f66dc78d84d5e8ae6ed5972fd9ac10c44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3932785105a6a7b12925a3420ddefda34ccb5b7d3178a1af8eef6b50a2fd07e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyIntrusionDetectionTrafficBypass]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae85f2896b303ff4feb10528b5ec91181c2f244bf1133ffbdccfdbad64c96e26(
    *,
    fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97097e971fd608dc011ed87329111925141865d9b6668663837fc1cb47f21096(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71904c88c891129597740f39fa268303194205f7d60dccab09988670d5e42635(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea06c1738cf4b9cc19e5c2fa24a1b480397b156e47cbf002e33bc2a2d077c902(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d373099ac4f879858dbbb3809541c6cce345564409e9713c05401364c7aabf(
    value: typing.Optional[FirewallPolicyThreatIntelligenceAllowlistStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56d3f3749a2ab7e352a9e812a8b3f4b5b4dd88e1ed2d063104fc834925da85b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dedc87024d65f03964c7ff5cbb845b9cfa12fe689c049cd6a0158e23a615744a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a55dfe77d3bf24c1e9ea4708174e4680127cbbf69a6214652e6629694fdc20d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b359ed5916cb7cd2df6b9ae3c425876aaa054d73fce0fa9806b69a214f38919b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42636a6b8dd1fe65a5755546793640e0af84e33a6bd9f6b857d2b0a57930cb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812fb3fa74ed7c51ca1dcb7d03de04a0db84026fdfd9e3de0527f85e5c01b18e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6bffeb1ff6426a2520ba176f72c14ce4374502432ef7129d3c2d119ae7edea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirewallPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d663d173b8230bbd3cc632c6b37a09d567512037870905363a0da79a731c2b0c(
    *,
    key_vault_secret_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1890df9e5300610238c47874fc749f1360377d5d64d45dcbd8529adf85642c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5ecca41a79978ec3a19ac7088919a67a39e0daa8930173eedb9de7f64ba4cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d157a654119baf6bea97c6802f1ca1b8832bdcf2771d2db4b0f9305d827b99e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397f991e5c5ea74e41d91ccac7343a6b34c346398dbb355b5fc6d95551de9c19(
    value: typing.Optional[FirewallPolicyTlsCertificate],
) -> None:
    """Type checking stubs"""
    pass
