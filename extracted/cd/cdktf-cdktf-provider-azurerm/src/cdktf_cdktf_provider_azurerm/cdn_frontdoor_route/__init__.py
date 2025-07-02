r'''
# `azurerm_cdn_frontdoor_route`

Refer to the Terraform Registry for docs: [`azurerm_cdn_frontdoor_route`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route).
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


class CdnFrontdoorRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRoute.CdnFrontdoorRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route azurerm_cdn_frontdoor_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cdn_frontdoor_endpoint_id: builtins.str,
        cdn_frontdoor_origin_group_id: builtins.str,
        cdn_frontdoor_origin_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        patterns_to_match: typing.Sequence[builtins.str],
        supported_protocols: typing.Sequence[builtins.str],
        cache: typing.Optional[typing.Union["CdnFrontdoorRouteCache", typing.Dict[builtins.str, typing.Any]]] = None,
        cdn_frontdoor_custom_domain_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdn_frontdoor_origin_path: typing.Optional[builtins.str] = None,
        cdn_frontdoor_rule_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarding_protocol: typing.Optional[builtins.str] = None,
        https_redirect_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        link_to_default_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["CdnFrontdoorRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route azurerm_cdn_frontdoor_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cdn_frontdoor_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_endpoint_id CdnFrontdoorRoute#cdn_frontdoor_endpoint_id}.
        :param cdn_frontdoor_origin_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_origin_group_id CdnFrontdoorRoute#cdn_frontdoor_origin_group_id}.
        :param cdn_frontdoor_origin_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_origin_ids CdnFrontdoorRoute#cdn_frontdoor_origin_ids}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#name CdnFrontdoorRoute#name}.
        :param patterns_to_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#patterns_to_match CdnFrontdoorRoute#patterns_to_match}.
        :param supported_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#supported_protocols CdnFrontdoorRoute#supported_protocols}.
        :param cache: cache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cache CdnFrontdoorRoute#cache}
        :param cdn_frontdoor_custom_domain_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_custom_domain_ids CdnFrontdoorRoute#cdn_frontdoor_custom_domain_ids}.
        :param cdn_frontdoor_origin_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_origin_path CdnFrontdoorRoute#cdn_frontdoor_origin_path}.
        :param cdn_frontdoor_rule_set_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_rule_set_ids CdnFrontdoorRoute#cdn_frontdoor_rule_set_ids}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#enabled CdnFrontdoorRoute#enabled}.
        :param forwarding_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#forwarding_protocol CdnFrontdoorRoute#forwarding_protocol}.
        :param https_redirect_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#https_redirect_enabled CdnFrontdoorRoute#https_redirect_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#id CdnFrontdoorRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param link_to_default_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#link_to_default_domain CdnFrontdoorRoute#link_to_default_domain}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#timeouts CdnFrontdoorRoute#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c790a28f1384a537d25f2b82ab4e71c818643cc993c9f68caba9b7ccf4c627)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CdnFrontdoorRouteConfig(
            cdn_frontdoor_endpoint_id=cdn_frontdoor_endpoint_id,
            cdn_frontdoor_origin_group_id=cdn_frontdoor_origin_group_id,
            cdn_frontdoor_origin_ids=cdn_frontdoor_origin_ids,
            name=name,
            patterns_to_match=patterns_to_match,
            supported_protocols=supported_protocols,
            cache=cache,
            cdn_frontdoor_custom_domain_ids=cdn_frontdoor_custom_domain_ids,
            cdn_frontdoor_origin_path=cdn_frontdoor_origin_path,
            cdn_frontdoor_rule_set_ids=cdn_frontdoor_rule_set_ids,
            enabled=enabled,
            forwarding_protocol=forwarding_protocol,
            https_redirect_enabled=https_redirect_enabled,
            id=id,
            link_to_default_domain=link_to_default_domain,
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
        '''Generates CDKTF code for importing a CdnFrontdoorRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CdnFrontdoorRoute to import.
        :param import_from_id: The id of the existing CdnFrontdoorRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CdnFrontdoorRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8e8c9a4c55d4926a70c073abb5e7c240f78a629077992860f9d22d6c6b222c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCache")
    def put_cache(
        self,
        *,
        compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        content_types_to_compress: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_caching_behavior: typing.Optional[builtins.str] = None,
        query_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param compression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#compression_enabled CdnFrontdoorRoute#compression_enabled}.
        :param content_types_to_compress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#content_types_to_compress CdnFrontdoorRoute#content_types_to_compress}.
        :param query_string_caching_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#query_string_caching_behavior CdnFrontdoorRoute#query_string_caching_behavior}.
        :param query_strings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#query_strings CdnFrontdoorRoute#query_strings}.
        '''
        value = CdnFrontdoorRouteCache(
            compression_enabled=compression_enabled,
            content_types_to_compress=content_types_to_compress,
            query_string_caching_behavior=query_string_caching_behavior,
            query_strings=query_strings,
        )

        return typing.cast(None, jsii.invoke(self, "putCache", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#create CdnFrontdoorRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#delete CdnFrontdoorRoute#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#read CdnFrontdoorRoute#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#update CdnFrontdoorRoute#update}.
        '''
        value = CdnFrontdoorRouteTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCache")
    def reset_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCache", []))

    @jsii.member(jsii_name="resetCdnFrontdoorCustomDomainIds")
    def reset_cdn_frontdoor_custom_domain_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnFrontdoorCustomDomainIds", []))

    @jsii.member(jsii_name="resetCdnFrontdoorOriginPath")
    def reset_cdn_frontdoor_origin_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnFrontdoorOriginPath", []))

    @jsii.member(jsii_name="resetCdnFrontdoorRuleSetIds")
    def reset_cdn_frontdoor_rule_set_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnFrontdoorRuleSetIds", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetForwardingProtocol")
    def reset_forwarding_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardingProtocol", []))

    @jsii.member(jsii_name="resetHttpsRedirectEnabled")
    def reset_https_redirect_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsRedirectEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLinkToDefaultDomain")
    def reset_link_to_default_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkToDefaultDomain", []))

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
    @jsii.member(jsii_name="cache")
    def cache(self) -> "CdnFrontdoorRouteCacheOutputReference":
        return typing.cast("CdnFrontdoorRouteCacheOutputReference", jsii.get(self, "cache"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CdnFrontdoorRouteTimeoutsOutputReference":
        return typing.cast("CdnFrontdoorRouteTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cacheInput")
    def cache_input(self) -> typing.Optional["CdnFrontdoorRouteCache"]:
        return typing.cast(typing.Optional["CdnFrontdoorRouteCache"], jsii.get(self, "cacheInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorCustomDomainIdsInput")
    def cdn_frontdoor_custom_domain_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cdnFrontdoorCustomDomainIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorEndpointIdInput")
    def cdn_frontdoor_endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnFrontdoorEndpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorOriginGroupIdInput")
    def cdn_frontdoor_origin_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnFrontdoorOriginGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorOriginIdsInput")
    def cdn_frontdoor_origin_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cdnFrontdoorOriginIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorOriginPathInput")
    def cdn_frontdoor_origin_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnFrontdoorOriginPathInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorRuleSetIdsInput")
    def cdn_frontdoor_rule_set_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cdnFrontdoorRuleSetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingProtocolInput")
    def forwarding_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardingProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsRedirectEnabledInput")
    def https_redirect_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpsRedirectEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linkToDefaultDomainInput")
    def link_to_default_domain_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "linkToDefaultDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="patternsToMatchInput")
    def patterns_to_match_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "patternsToMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="supportedProtocolsInput")
    def supported_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "supportedProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CdnFrontdoorRouteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CdnFrontdoorRouteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorCustomDomainIds")
    def cdn_frontdoor_custom_domain_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cdnFrontdoorCustomDomainIds"))

    @cdn_frontdoor_custom_domain_ids.setter
    def cdn_frontdoor_custom_domain_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d675792cf70f90b469e2c23e728d59c20d9e9728e3f71f429313db941de356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorCustomDomainIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorEndpointId")
    def cdn_frontdoor_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnFrontdoorEndpointId"))

    @cdn_frontdoor_endpoint_id.setter
    def cdn_frontdoor_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3e934a711669a5d6a54e9e7ece44d133f41e8b271d455f9dd9b5fcbf8be4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorOriginGroupId")
    def cdn_frontdoor_origin_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnFrontdoorOriginGroupId"))

    @cdn_frontdoor_origin_group_id.setter
    def cdn_frontdoor_origin_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513fecc8d010559ee4e3b1eb9b2baabf31b48c359856b7c53f707933b9b907d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorOriginGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorOriginIds")
    def cdn_frontdoor_origin_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cdnFrontdoorOriginIds"))

    @cdn_frontdoor_origin_ids.setter
    def cdn_frontdoor_origin_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b663027eb674002358f714c7f95f679c202d9388b4469bdf2fd38764065eb8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorOriginIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorOriginPath")
    def cdn_frontdoor_origin_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnFrontdoorOriginPath"))

    @cdn_frontdoor_origin_path.setter
    def cdn_frontdoor_origin_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c222b26cfebb3ae5f451db8cd79645f011b3154e0c7c521d0a8441b130fd55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorOriginPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorRuleSetIds")
    def cdn_frontdoor_rule_set_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cdnFrontdoorRuleSetIds"))

    @cdn_frontdoor_rule_set_ids.setter
    def cdn_frontdoor_rule_set_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe509098242c19a364ab3ac00f3b5797118421ff64e343c927dbd52b252c150a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorRuleSetIds", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__8592dba2a41b6ea9965a86a2071f9b8d3414324c636b8a287d58fa8bcbbe97d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingProtocol")
    def forwarding_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingProtocol"))

    @forwarding_protocol.setter
    def forwarding_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f265c751b75b2372707bb12bd040d8e4ee4d86d4fdc17721248060f8175b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsRedirectEnabled")
    def https_redirect_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpsRedirectEnabled"))

    @https_redirect_enabled.setter
    def https_redirect_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b8e5526744a154c41b29e87ead51878e1f5652d301c0969e4ca2b0a404daef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsRedirectEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746f6576dfe86a8cbcee85c67b9e42ec5d3409b75639087292566bf95c52109f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkToDefaultDomain")
    def link_to_default_domain(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "linkToDefaultDomain"))

    @link_to_default_domain.setter
    def link_to_default_domain(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a294c54093d2fb65b6616a9a323a9d93a1f6ceee6475b066db052b634bf8936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkToDefaultDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14993c1432d388ec75226ba68d6d7c744ff6d8e392f797e602c21d56dec011c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternsToMatch")
    def patterns_to_match(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "patternsToMatch"))

    @patterns_to_match.setter
    def patterns_to_match(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c415499645e7504656f521c81688ecff08c6da4f0d3126ac38703fffa1b2368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patternsToMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportedProtocols")
    def supported_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedProtocols"))

    @supported_protocols.setter
    def supported_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2daf99fd066fe312e4084c33c1bb6772bc8a1419c5ce22833a14796e944f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedProtocols", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRoute.CdnFrontdoorRouteCache",
    jsii_struct_bases=[],
    name_mapping={
        "compression_enabled": "compressionEnabled",
        "content_types_to_compress": "contentTypesToCompress",
        "query_string_caching_behavior": "queryStringCachingBehavior",
        "query_strings": "queryStrings",
    },
)
class CdnFrontdoorRouteCache:
    def __init__(
        self,
        *,
        compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        content_types_to_compress: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_caching_behavior: typing.Optional[builtins.str] = None,
        query_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param compression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#compression_enabled CdnFrontdoorRoute#compression_enabled}.
        :param content_types_to_compress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#content_types_to_compress CdnFrontdoorRoute#content_types_to_compress}.
        :param query_string_caching_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#query_string_caching_behavior CdnFrontdoorRoute#query_string_caching_behavior}.
        :param query_strings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#query_strings CdnFrontdoorRoute#query_strings}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91c5e6fb9ced10f5cfeb4e055ac8e94aed28bcf31905d665e0afd58e44163b4)
            check_type(argname="argument compression_enabled", value=compression_enabled, expected_type=type_hints["compression_enabled"])
            check_type(argname="argument content_types_to_compress", value=content_types_to_compress, expected_type=type_hints["content_types_to_compress"])
            check_type(argname="argument query_string_caching_behavior", value=query_string_caching_behavior, expected_type=type_hints["query_string_caching_behavior"])
            check_type(argname="argument query_strings", value=query_strings, expected_type=type_hints["query_strings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compression_enabled is not None:
            self._values["compression_enabled"] = compression_enabled
        if content_types_to_compress is not None:
            self._values["content_types_to_compress"] = content_types_to_compress
        if query_string_caching_behavior is not None:
            self._values["query_string_caching_behavior"] = query_string_caching_behavior
        if query_strings is not None:
            self._values["query_strings"] = query_strings

    @builtins.property
    def compression_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#compression_enabled CdnFrontdoorRoute#compression_enabled}.'''
        result = self._values.get("compression_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def content_types_to_compress(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#content_types_to_compress CdnFrontdoorRoute#content_types_to_compress}.'''
        result = self._values.get("content_types_to_compress")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_caching_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#query_string_caching_behavior CdnFrontdoorRoute#query_string_caching_behavior}.'''
        result = self._values.get("query_string_caching_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_strings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#query_strings CdnFrontdoorRoute#query_strings}.'''
        result = self._values.get("query_strings")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRouteCache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRouteCacheOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRoute.CdnFrontdoorRouteCacheOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5343c04e4439d57edba7ea561d91c683da89655a48b195ea0ad579c1fa22a360)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCompressionEnabled")
    def reset_compression_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionEnabled", []))

    @jsii.member(jsii_name="resetContentTypesToCompress")
    def reset_content_types_to_compress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentTypesToCompress", []))

    @jsii.member(jsii_name="resetQueryStringCachingBehavior")
    def reset_query_string_caching_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringCachingBehavior", []))

    @jsii.member(jsii_name="resetQueryStrings")
    def reset_query_strings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStrings", []))

    @builtins.property
    @jsii.member(jsii_name="compressionEnabledInput")
    def compression_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "compressionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypesToCompressInput")
    def content_types_to_compress_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contentTypesToCompressInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringCachingBehaviorInput")
    def query_string_caching_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryStringCachingBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringsInput")
    def query_strings_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryStringsInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionEnabled")
    def compression_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "compressionEnabled"))

    @compression_enabled.setter
    def compression_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad0c866976d529f06ed54072ddb44dc66c63479e79d929cbfd3a883ba459f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentTypesToCompress")
    def content_types_to_compress(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contentTypesToCompress"))

    @content_types_to_compress.setter
    def content_types_to_compress(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d293e56d183c62e3e5d1cf5426411496f6dfebd80f89e8251572f889fdfe12a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentTypesToCompress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringCachingBehavior")
    def query_string_caching_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryStringCachingBehavior"))

    @query_string_caching_behavior.setter
    def query_string_caching_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56d8245e67e722f74bcee9a82a2391e95bd94b422085edbd06d768bd0ba28ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringCachingBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStrings")
    def query_strings(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStrings"))

    @query_strings.setter
    def query_strings(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b63c80e51bbba50311dd49b6234655e258dc03fcb042574888be21e8d3538f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStrings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CdnFrontdoorRouteCache]:
        return typing.cast(typing.Optional[CdnFrontdoorRouteCache], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CdnFrontdoorRouteCache]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f989fdceb3a484ff1fc797a398ab070e0c620d06e6c3560bdf7d6c980f85ba45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRoute.CdnFrontdoorRouteConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cdn_frontdoor_endpoint_id": "cdnFrontdoorEndpointId",
        "cdn_frontdoor_origin_group_id": "cdnFrontdoorOriginGroupId",
        "cdn_frontdoor_origin_ids": "cdnFrontdoorOriginIds",
        "name": "name",
        "patterns_to_match": "patternsToMatch",
        "supported_protocols": "supportedProtocols",
        "cache": "cache",
        "cdn_frontdoor_custom_domain_ids": "cdnFrontdoorCustomDomainIds",
        "cdn_frontdoor_origin_path": "cdnFrontdoorOriginPath",
        "cdn_frontdoor_rule_set_ids": "cdnFrontdoorRuleSetIds",
        "enabled": "enabled",
        "forwarding_protocol": "forwardingProtocol",
        "https_redirect_enabled": "httpsRedirectEnabled",
        "id": "id",
        "link_to_default_domain": "linkToDefaultDomain",
        "timeouts": "timeouts",
    },
)
class CdnFrontdoorRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cdn_frontdoor_endpoint_id: builtins.str,
        cdn_frontdoor_origin_group_id: builtins.str,
        cdn_frontdoor_origin_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        patterns_to_match: typing.Sequence[builtins.str],
        supported_protocols: typing.Sequence[builtins.str],
        cache: typing.Optional[typing.Union[CdnFrontdoorRouteCache, typing.Dict[builtins.str, typing.Any]]] = None,
        cdn_frontdoor_custom_domain_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdn_frontdoor_origin_path: typing.Optional[builtins.str] = None,
        cdn_frontdoor_rule_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarding_protocol: typing.Optional[builtins.str] = None,
        https_redirect_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        link_to_default_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["CdnFrontdoorRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cdn_frontdoor_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_endpoint_id CdnFrontdoorRoute#cdn_frontdoor_endpoint_id}.
        :param cdn_frontdoor_origin_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_origin_group_id CdnFrontdoorRoute#cdn_frontdoor_origin_group_id}.
        :param cdn_frontdoor_origin_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_origin_ids CdnFrontdoorRoute#cdn_frontdoor_origin_ids}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#name CdnFrontdoorRoute#name}.
        :param patterns_to_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#patterns_to_match CdnFrontdoorRoute#patterns_to_match}.
        :param supported_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#supported_protocols CdnFrontdoorRoute#supported_protocols}.
        :param cache: cache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cache CdnFrontdoorRoute#cache}
        :param cdn_frontdoor_custom_domain_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_custom_domain_ids CdnFrontdoorRoute#cdn_frontdoor_custom_domain_ids}.
        :param cdn_frontdoor_origin_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_origin_path CdnFrontdoorRoute#cdn_frontdoor_origin_path}.
        :param cdn_frontdoor_rule_set_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_rule_set_ids CdnFrontdoorRoute#cdn_frontdoor_rule_set_ids}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#enabled CdnFrontdoorRoute#enabled}.
        :param forwarding_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#forwarding_protocol CdnFrontdoorRoute#forwarding_protocol}.
        :param https_redirect_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#https_redirect_enabled CdnFrontdoorRoute#https_redirect_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#id CdnFrontdoorRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param link_to_default_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#link_to_default_domain CdnFrontdoorRoute#link_to_default_domain}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#timeouts CdnFrontdoorRoute#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cache, dict):
            cache = CdnFrontdoorRouteCache(**cache)
        if isinstance(timeouts, dict):
            timeouts = CdnFrontdoorRouteTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6abf4633fe1c1f3ff6d54ee354c99416eeb678db42290c16004052c5f62717c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cdn_frontdoor_endpoint_id", value=cdn_frontdoor_endpoint_id, expected_type=type_hints["cdn_frontdoor_endpoint_id"])
            check_type(argname="argument cdn_frontdoor_origin_group_id", value=cdn_frontdoor_origin_group_id, expected_type=type_hints["cdn_frontdoor_origin_group_id"])
            check_type(argname="argument cdn_frontdoor_origin_ids", value=cdn_frontdoor_origin_ids, expected_type=type_hints["cdn_frontdoor_origin_ids"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument patterns_to_match", value=patterns_to_match, expected_type=type_hints["patterns_to_match"])
            check_type(argname="argument supported_protocols", value=supported_protocols, expected_type=type_hints["supported_protocols"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument cdn_frontdoor_custom_domain_ids", value=cdn_frontdoor_custom_domain_ids, expected_type=type_hints["cdn_frontdoor_custom_domain_ids"])
            check_type(argname="argument cdn_frontdoor_origin_path", value=cdn_frontdoor_origin_path, expected_type=type_hints["cdn_frontdoor_origin_path"])
            check_type(argname="argument cdn_frontdoor_rule_set_ids", value=cdn_frontdoor_rule_set_ids, expected_type=type_hints["cdn_frontdoor_rule_set_ids"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument forwarding_protocol", value=forwarding_protocol, expected_type=type_hints["forwarding_protocol"])
            check_type(argname="argument https_redirect_enabled", value=https_redirect_enabled, expected_type=type_hints["https_redirect_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument link_to_default_domain", value=link_to_default_domain, expected_type=type_hints["link_to_default_domain"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cdn_frontdoor_endpoint_id": cdn_frontdoor_endpoint_id,
            "cdn_frontdoor_origin_group_id": cdn_frontdoor_origin_group_id,
            "cdn_frontdoor_origin_ids": cdn_frontdoor_origin_ids,
            "name": name,
            "patterns_to_match": patterns_to_match,
            "supported_protocols": supported_protocols,
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
        if cache is not None:
            self._values["cache"] = cache
        if cdn_frontdoor_custom_domain_ids is not None:
            self._values["cdn_frontdoor_custom_domain_ids"] = cdn_frontdoor_custom_domain_ids
        if cdn_frontdoor_origin_path is not None:
            self._values["cdn_frontdoor_origin_path"] = cdn_frontdoor_origin_path
        if cdn_frontdoor_rule_set_ids is not None:
            self._values["cdn_frontdoor_rule_set_ids"] = cdn_frontdoor_rule_set_ids
        if enabled is not None:
            self._values["enabled"] = enabled
        if forwarding_protocol is not None:
            self._values["forwarding_protocol"] = forwarding_protocol
        if https_redirect_enabled is not None:
            self._values["https_redirect_enabled"] = https_redirect_enabled
        if id is not None:
            self._values["id"] = id
        if link_to_default_domain is not None:
            self._values["link_to_default_domain"] = link_to_default_domain
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
    def cdn_frontdoor_endpoint_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_endpoint_id CdnFrontdoorRoute#cdn_frontdoor_endpoint_id}.'''
        result = self._values.get("cdn_frontdoor_endpoint_id")
        assert result is not None, "Required property 'cdn_frontdoor_endpoint_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cdn_frontdoor_origin_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_origin_group_id CdnFrontdoorRoute#cdn_frontdoor_origin_group_id}.'''
        result = self._values.get("cdn_frontdoor_origin_group_id")
        assert result is not None, "Required property 'cdn_frontdoor_origin_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cdn_frontdoor_origin_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_origin_ids CdnFrontdoorRoute#cdn_frontdoor_origin_ids}.'''
        result = self._values.get("cdn_frontdoor_origin_ids")
        assert result is not None, "Required property 'cdn_frontdoor_origin_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#name CdnFrontdoorRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def patterns_to_match(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#patterns_to_match CdnFrontdoorRoute#patterns_to_match}.'''
        result = self._values.get("patterns_to_match")
        assert result is not None, "Required property 'patterns_to_match' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def supported_protocols(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#supported_protocols CdnFrontdoorRoute#supported_protocols}.'''
        result = self._values.get("supported_protocols")
        assert result is not None, "Required property 'supported_protocols' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cache(self) -> typing.Optional[CdnFrontdoorRouteCache]:
        '''cache block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cache CdnFrontdoorRoute#cache}
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[CdnFrontdoorRouteCache], result)

    @builtins.property
    def cdn_frontdoor_custom_domain_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_custom_domain_ids CdnFrontdoorRoute#cdn_frontdoor_custom_domain_ids}.'''
        result = self._values.get("cdn_frontdoor_custom_domain_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdn_frontdoor_origin_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_origin_path CdnFrontdoorRoute#cdn_frontdoor_origin_path}.'''
        result = self._values.get("cdn_frontdoor_origin_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdn_frontdoor_rule_set_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#cdn_frontdoor_rule_set_ids CdnFrontdoorRoute#cdn_frontdoor_rule_set_ids}.'''
        result = self._values.get("cdn_frontdoor_rule_set_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#enabled CdnFrontdoorRoute#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forwarding_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#forwarding_protocol CdnFrontdoorRoute#forwarding_protocol}.'''
        result = self._values.get("forwarding_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_redirect_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#https_redirect_enabled CdnFrontdoorRoute#https_redirect_enabled}.'''
        result = self._values.get("https_redirect_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#id CdnFrontdoorRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_to_default_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#link_to_default_domain CdnFrontdoorRoute#link_to_default_domain}.'''
        result = self._values.get("link_to_default_domain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CdnFrontdoorRouteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#timeouts CdnFrontdoorRoute#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CdnFrontdoorRouteTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRoute.CdnFrontdoorRouteTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class CdnFrontdoorRouteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#create CdnFrontdoorRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#delete CdnFrontdoorRoute#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#read CdnFrontdoorRoute#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#update CdnFrontdoorRoute#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3e8c1b4a07ab26e24550f52e5676b5db8ba10f1a460d8b216fd1aeb5d2ac07)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#create CdnFrontdoorRoute#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#delete CdnFrontdoorRoute#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#read CdnFrontdoorRoute#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_route#update CdnFrontdoorRoute#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRouteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRouteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRoute.CdnFrontdoorRouteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f005470e0b0ab02e9532e052a28c2a7fa941dfeac829dbbeb9ad34af37f5f25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f6eb59225853d504cd226a72e284dbb25f8a6c506c9c8bc23500ca6d546a486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67fab45f164aa467f7fcc919148760fe12f2a8fa7044091470178cdeaf4a5a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48034d6dbc7c660a686bb34774f90591ae6319645e961d94c5224ebef98e3756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968928b23d5d0c922a66747f162b115058d33375ff6b7ed3e07010b1fa7b7134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRouteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRouteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRouteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26f5d48b38bcc028623a1f8047feec8bd012c7a0074be522668eef6e4f5a009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CdnFrontdoorRoute",
    "CdnFrontdoorRouteCache",
    "CdnFrontdoorRouteCacheOutputReference",
    "CdnFrontdoorRouteConfig",
    "CdnFrontdoorRouteTimeouts",
    "CdnFrontdoorRouteTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__55c790a28f1384a537d25f2b82ab4e71c818643cc993c9f68caba9b7ccf4c627(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cdn_frontdoor_endpoint_id: builtins.str,
    cdn_frontdoor_origin_group_id: builtins.str,
    cdn_frontdoor_origin_ids: typing.Sequence[builtins.str],
    name: builtins.str,
    patterns_to_match: typing.Sequence[builtins.str],
    supported_protocols: typing.Sequence[builtins.str],
    cache: typing.Optional[typing.Union[CdnFrontdoorRouteCache, typing.Dict[builtins.str, typing.Any]]] = None,
    cdn_frontdoor_custom_domain_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdn_frontdoor_origin_path: typing.Optional[builtins.str] = None,
    cdn_frontdoor_rule_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarding_protocol: typing.Optional[builtins.str] = None,
    https_redirect_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    link_to_default_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[CdnFrontdoorRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2c8e8c9a4c55d4926a70c073abb5e7c240f78a629077992860f9d22d6c6b222c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d675792cf70f90b469e2c23e728d59c20d9e9728e3f71f429313db941de356(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3e934a711669a5d6a54e9e7ece44d133f41e8b271d455f9dd9b5fcbf8be4d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513fecc8d010559ee4e3b1eb9b2baabf31b48c359856b7c53f707933b9b907d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b663027eb674002358f714c7f95f679c202d9388b4469bdf2fd38764065eb8f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c222b26cfebb3ae5f451db8cd79645f011b3154e0c7c521d0a8441b130fd55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe509098242c19a364ab3ac00f3b5797118421ff64e343c927dbd52b252c150a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8592dba2a41b6ea9965a86a2071f9b8d3414324c636b8a287d58fa8bcbbe97d5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f265c751b75b2372707bb12bd040d8e4ee4d86d4fdc17721248060f8175b5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b8e5526744a154c41b29e87ead51878e1f5652d301c0969e4ca2b0a404daef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746f6576dfe86a8cbcee85c67b9e42ec5d3409b75639087292566bf95c52109f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a294c54093d2fb65b6616a9a323a9d93a1f6ceee6475b066db052b634bf8936(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14993c1432d388ec75226ba68d6d7c744ff6d8e392f797e602c21d56dec011c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c415499645e7504656f521c81688ecff08c6da4f0d3126ac38703fffa1b2368(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2daf99fd066fe312e4084c33c1bb6772bc8a1419c5ce22833a14796e944f19(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91c5e6fb9ced10f5cfeb4e055ac8e94aed28bcf31905d665e0afd58e44163b4(
    *,
    compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    content_types_to_compress: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_caching_behavior: typing.Optional[builtins.str] = None,
    query_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5343c04e4439d57edba7ea561d91c683da89655a48b195ea0ad579c1fa22a360(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad0c866976d529f06ed54072ddb44dc66c63479e79d929cbfd3a883ba459f7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d293e56d183c62e3e5d1cf5426411496f6dfebd80f89e8251572f889fdfe12a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56d8245e67e722f74bcee9a82a2391e95bd94b422085edbd06d768bd0ba28ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b63c80e51bbba50311dd49b6234655e258dc03fcb042574888be21e8d3538f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f989fdceb3a484ff1fc797a398ab070e0c620d06e6c3560bdf7d6c980f85ba45(
    value: typing.Optional[CdnFrontdoorRouteCache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6abf4633fe1c1f3ff6d54ee354c99416eeb678db42290c16004052c5f62717c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_frontdoor_endpoint_id: builtins.str,
    cdn_frontdoor_origin_group_id: builtins.str,
    cdn_frontdoor_origin_ids: typing.Sequence[builtins.str],
    name: builtins.str,
    patterns_to_match: typing.Sequence[builtins.str],
    supported_protocols: typing.Sequence[builtins.str],
    cache: typing.Optional[typing.Union[CdnFrontdoorRouteCache, typing.Dict[builtins.str, typing.Any]]] = None,
    cdn_frontdoor_custom_domain_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdn_frontdoor_origin_path: typing.Optional[builtins.str] = None,
    cdn_frontdoor_rule_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarding_protocol: typing.Optional[builtins.str] = None,
    https_redirect_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    link_to_default_domain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[CdnFrontdoorRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3e8c1b4a07ab26e24550f52e5676b5db8ba10f1a460d8b216fd1aeb5d2ac07(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f005470e0b0ab02e9532e052a28c2a7fa941dfeac829dbbeb9ad34af37f5f25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6eb59225853d504cd226a72e284dbb25f8a6c506c9c8bc23500ca6d546a486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fab45f164aa467f7fcc919148760fe12f2a8fa7044091470178cdeaf4a5a04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48034d6dbc7c660a686bb34774f90591ae6319645e961d94c5224ebef98e3756(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968928b23d5d0c922a66747f162b115058d33375ff6b7ed3e07010b1fa7b7134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26f5d48b38bcc028623a1f8047feec8bd012c7a0074be522668eef6e4f5a009(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRouteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
