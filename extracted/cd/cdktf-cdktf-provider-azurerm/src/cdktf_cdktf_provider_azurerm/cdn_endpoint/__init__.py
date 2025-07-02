r'''
# `azurerm_cdn_endpoint`

Refer to the Terraform Registry for docs: [`azurerm_cdn_endpoint`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint).
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


class CdnEndpoint(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpoint",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint azurerm_cdn_endpoint}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        origin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointOrigin", typing.Dict[builtins.str, typing.Any]]]],
        profile_name: builtins.str,
        resource_group_name: builtins.str,
        content_types_to_compress: typing.Optional[typing.Sequence[builtins.str]] = None,
        delivery_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        geo_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointGeoFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        global_delivery_rule: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRule", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_http_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_https_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optimization_type: typing.Optional[builtins.str] = None,
        origin_host_header: typing.Optional[builtins.str] = None,
        origin_path: typing.Optional[builtins.str] = None,
        probe_path: typing.Optional[builtins.str] = None,
        querystring_caching_behaviour: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CdnEndpointTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint azurerm_cdn_endpoint} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#location CdnEndpoint#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#origin CdnEndpoint#origin}
        :param profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#profile_name CdnEndpoint#profile_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#resource_group_name CdnEndpoint#resource_group_name}.
        :param content_types_to_compress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#content_types_to_compress CdnEndpoint#content_types_to_compress}.
        :param delivery_rule: delivery_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#delivery_rule CdnEndpoint#delivery_rule}
        :param geo_filter: geo_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#geo_filter CdnEndpoint#geo_filter}
        :param global_delivery_rule: global_delivery_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#global_delivery_rule CdnEndpoint#global_delivery_rule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#id CdnEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_compression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#is_compression_enabled CdnEndpoint#is_compression_enabled}.
        :param is_http_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#is_http_allowed CdnEndpoint#is_http_allowed}.
        :param is_https_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#is_https_allowed CdnEndpoint#is_https_allowed}.
        :param optimization_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#optimization_type CdnEndpoint#optimization_type}.
        :param origin_host_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#origin_host_header CdnEndpoint#origin_host_header}.
        :param origin_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#origin_path CdnEndpoint#origin_path}.
        :param probe_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#probe_path CdnEndpoint#probe_path}.
        :param querystring_caching_behaviour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#querystring_caching_behaviour CdnEndpoint#querystring_caching_behaviour}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#tags CdnEndpoint#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#timeouts CdnEndpoint#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41c2d9eecef2adb957d716684a1e81a0f737215b6b3e8a31b2a22ab950730b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CdnEndpointConfig(
            location=location,
            name=name,
            origin=origin,
            profile_name=profile_name,
            resource_group_name=resource_group_name,
            content_types_to_compress=content_types_to_compress,
            delivery_rule=delivery_rule,
            geo_filter=geo_filter,
            global_delivery_rule=global_delivery_rule,
            id=id,
            is_compression_enabled=is_compression_enabled,
            is_http_allowed=is_http_allowed,
            is_https_allowed=is_https_allowed,
            optimization_type=optimization_type,
            origin_host_header=origin_host_header,
            origin_path=origin_path,
            probe_path=probe_path,
            querystring_caching_behaviour=querystring_caching_behaviour,
            tags=tags,
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
        '''Generates CDKTF code for importing a CdnEndpoint resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CdnEndpoint to import.
        :param import_from_id: The id of the existing CdnEndpoint that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CdnEndpoint to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7952d8d675ba5cd1abab69fe4ce83542bf60ead9a15af86c6996539b12966071)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeliveryRule")
    def put_delivery_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57aec5012d6dbe5400fa4e8262b356813a21fcbed0eceaec6e9f121518ae8211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeliveryRule", [value]))

    @jsii.member(jsii_name="putGeoFilter")
    def put_geo_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointGeoFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804bc0a095d9b1aeb765b2665bf4367e610184b904098930e4bf69ab883efec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGeoFilter", [value]))

    @jsii.member(jsii_name="putGlobalDeliveryRule")
    def put_global_delivery_rule(
        self,
        *,
        cache_expiration_action: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRuleCacheExpirationAction", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_key_query_string_action: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction", typing.Dict[builtins.str, typing.Any]]] = None,
        modify_request_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        modify_response_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_redirect_action: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRuleUrlRedirectAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite_action: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRuleUrlRewriteAction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cache_expiration_action: cache_expiration_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_expiration_action CdnEndpoint#cache_expiration_action}
        :param cache_key_query_string_action: cache_key_query_string_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_key_query_string_action CdnEndpoint#cache_key_query_string_action}
        :param modify_request_header_action: modify_request_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_request_header_action CdnEndpoint#modify_request_header_action}
        :param modify_response_header_action: modify_response_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_response_header_action CdnEndpoint#modify_response_header_action}
        :param url_redirect_action: url_redirect_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_redirect_action CdnEndpoint#url_redirect_action}
        :param url_rewrite_action: url_rewrite_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_rewrite_action CdnEndpoint#url_rewrite_action}
        '''
        value = CdnEndpointGlobalDeliveryRule(
            cache_expiration_action=cache_expiration_action,
            cache_key_query_string_action=cache_key_query_string_action,
            modify_request_header_action=modify_request_header_action,
            modify_response_header_action=modify_response_header_action,
            url_redirect_action=url_redirect_action,
            url_rewrite_action=url_rewrite_action,
        )

        return typing.cast(None, jsii.invoke(self, "putGlobalDeliveryRule", [value]))

    @jsii.member(jsii_name="putOrigin")
    def put_origin(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointOrigin", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8956c542b5000dc5847b7f0cc138631cc25f92cac2d9b330ed832e50d9adecc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOrigin", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#create CdnEndpoint#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#delete CdnEndpoint#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#read CdnEndpoint#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#update CdnEndpoint#update}.
        '''
        value = CdnEndpointTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetContentTypesToCompress")
    def reset_content_types_to_compress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentTypesToCompress", []))

    @jsii.member(jsii_name="resetDeliveryRule")
    def reset_delivery_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliveryRule", []))

    @jsii.member(jsii_name="resetGeoFilter")
    def reset_geo_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoFilter", []))

    @jsii.member(jsii_name="resetGlobalDeliveryRule")
    def reset_global_delivery_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobalDeliveryRule", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsCompressionEnabled")
    def reset_is_compression_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCompressionEnabled", []))

    @jsii.member(jsii_name="resetIsHttpAllowed")
    def reset_is_http_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsHttpAllowed", []))

    @jsii.member(jsii_name="resetIsHttpsAllowed")
    def reset_is_https_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsHttpsAllowed", []))

    @jsii.member(jsii_name="resetOptimizationType")
    def reset_optimization_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptimizationType", []))

    @jsii.member(jsii_name="resetOriginHostHeader")
    def reset_origin_host_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginHostHeader", []))

    @jsii.member(jsii_name="resetOriginPath")
    def reset_origin_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginPath", []))

    @jsii.member(jsii_name="resetProbePath")
    def reset_probe_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProbePath", []))

    @jsii.member(jsii_name="resetQuerystringCachingBehaviour")
    def reset_querystring_caching_behaviour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuerystringCachingBehaviour", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="deliveryRule")
    def delivery_rule(self) -> "CdnEndpointDeliveryRuleList":
        return typing.cast("CdnEndpointDeliveryRuleList", jsii.get(self, "deliveryRule"))

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="geoFilter")
    def geo_filter(self) -> "CdnEndpointGeoFilterList":
        return typing.cast("CdnEndpointGeoFilterList", jsii.get(self, "geoFilter"))

    @builtins.property
    @jsii.member(jsii_name="globalDeliveryRule")
    def global_delivery_rule(self) -> "CdnEndpointGlobalDeliveryRuleOutputReference":
        return typing.cast("CdnEndpointGlobalDeliveryRuleOutputReference", jsii.get(self, "globalDeliveryRule"))

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> "CdnEndpointOriginList":
        return typing.cast("CdnEndpointOriginList", jsii.get(self, "origin"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CdnEndpointTimeoutsOutputReference":
        return typing.cast("CdnEndpointTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="contentTypesToCompressInput")
    def content_types_to_compress_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contentTypesToCompressInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryRuleInput")
    def delivery_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRule"]]], jsii.get(self, "deliveryRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="geoFilterInput")
    def geo_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointGeoFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointGeoFilter"]]], jsii.get(self, "geoFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="globalDeliveryRuleInput")
    def global_delivery_rule_input(
        self,
    ) -> typing.Optional["CdnEndpointGlobalDeliveryRule"]:
        return typing.cast(typing.Optional["CdnEndpointGlobalDeliveryRule"], jsii.get(self, "globalDeliveryRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isCompressionEnabledInput")
    def is_compression_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCompressionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isHttpAllowedInput")
    def is_http_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isHttpAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="isHttpsAllowedInput")
    def is_https_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isHttpsAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizationTypeInput")
    def optimization_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "optimizationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="originHostHeaderInput")
    def origin_host_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originHostHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointOrigin"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointOrigin"]]], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="originPathInput")
    def origin_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originPathInput"))

    @builtins.property
    @jsii.member(jsii_name="probePathInput")
    def probe_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "probePathInput"))

    @builtins.property
    @jsii.member(jsii_name="profileNameInput")
    def profile_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="querystringCachingBehaviourInput")
    def querystring_caching_behaviour_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "querystringCachingBehaviourInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CdnEndpointTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CdnEndpointTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypesToCompress")
    def content_types_to_compress(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contentTypesToCompress"))

    @content_types_to_compress.setter
    def content_types_to_compress(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240e0c2d7a9eda8243d3716ecba1039f6ab2e3af8b3bfc7f33c51b08e2c271b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentTypesToCompress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e348b2fa0bca891ee6165acbccafb087b2cdb5e06297dc6ec3364a1473cc096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isCompressionEnabled")
    def is_compression_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCompressionEnabled"))

    @is_compression_enabled.setter
    def is_compression_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627aa8745ea9a7aea1241ad3762c591b3a53cfae92c866a7079eaf6fac123c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCompressionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isHttpAllowed")
    def is_http_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isHttpAllowed"))

    @is_http_allowed.setter
    def is_http_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7737f2c8134459307ce6a83afc62674bbdb45d2bd47ce256d4fc1195db551f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isHttpAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isHttpsAllowed")
    def is_https_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isHttpsAllowed"))

    @is_https_allowed.setter
    def is_https_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4109f0b7c9ad24c1e7f9b22623f664b95095e3cfa4bfdbf014a11e6dfd1fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isHttpsAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d32e4f6ca559e8fd4b5415a523d4e089b39e0b14d62624b47f187a12bbc445f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d530f575d0c141aeb8d1e1abe4a29ceb7ce26c22de50b756178dd99524d5172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optimizationType")
    def optimization_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "optimizationType"))

    @optimization_type.setter
    def optimization_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6de932f4e1c4dfd3f203c7d8b28200e8512c85fd9214ec914e6ef8ea7aff7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optimizationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originHostHeader")
    def origin_host_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originHostHeader"))

    @origin_host_header.setter
    def origin_host_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1e4670cc41fc846c6759161686f587598ae1979c38b019182f2d9d1eefdeba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originHostHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originPath")
    def origin_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originPath"))

    @origin_path.setter
    def origin_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d92ec09ce1dbce7d8cf1c24ad44ae4c8d9c268984c088d0cbe0523338c3fbf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="probePath")
    def probe_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "probePath"))

    @probe_path.setter
    def probe_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e72c7b34cac83dc30cc9be0ebf2eba79d760b8b66cea3ec0696086fee1fba78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "probePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileName")
    def profile_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profileName"))

    @profile_name.setter
    def profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d0fabd539fa28fbbd76227329510d282242feef7e9853ca039b104fd91affd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="querystringCachingBehaviour")
    def querystring_caching_behaviour(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "querystringCachingBehaviour"))

    @querystring_caching_behaviour.setter
    def querystring_caching_behaviour(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4200cef2d16aff8c8775e52cbfa15c3555349f88505f686cb11daa853dc1d14d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "querystringCachingBehaviour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e27b299c3ffa1fafcad95f6f17a2e6c48ee0745a47b9674097145fc4ba720be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd920a73169ed10c759858fad3ceb6650f47b9fa3ffde7e8aed795ed6883d066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointConfig",
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
        "origin": "origin",
        "profile_name": "profileName",
        "resource_group_name": "resourceGroupName",
        "content_types_to_compress": "contentTypesToCompress",
        "delivery_rule": "deliveryRule",
        "geo_filter": "geoFilter",
        "global_delivery_rule": "globalDeliveryRule",
        "id": "id",
        "is_compression_enabled": "isCompressionEnabled",
        "is_http_allowed": "isHttpAllowed",
        "is_https_allowed": "isHttpsAllowed",
        "optimization_type": "optimizationType",
        "origin_host_header": "originHostHeader",
        "origin_path": "originPath",
        "probe_path": "probePath",
        "querystring_caching_behaviour": "querystringCachingBehaviour",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class CdnEndpointConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        origin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointOrigin", typing.Dict[builtins.str, typing.Any]]]],
        profile_name: builtins.str,
        resource_group_name: builtins.str,
        content_types_to_compress: typing.Optional[typing.Sequence[builtins.str]] = None,
        delivery_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        geo_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointGeoFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        global_delivery_rule: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRule", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_http_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_https_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optimization_type: typing.Optional[builtins.str] = None,
        origin_host_header: typing.Optional[builtins.str] = None,
        origin_path: typing.Optional[builtins.str] = None,
        probe_path: typing.Optional[builtins.str] = None,
        querystring_caching_behaviour: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CdnEndpointTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#location CdnEndpoint#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#origin CdnEndpoint#origin}
        :param profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#profile_name CdnEndpoint#profile_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#resource_group_name CdnEndpoint#resource_group_name}.
        :param content_types_to_compress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#content_types_to_compress CdnEndpoint#content_types_to_compress}.
        :param delivery_rule: delivery_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#delivery_rule CdnEndpoint#delivery_rule}
        :param geo_filter: geo_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#geo_filter CdnEndpoint#geo_filter}
        :param global_delivery_rule: global_delivery_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#global_delivery_rule CdnEndpoint#global_delivery_rule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#id CdnEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_compression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#is_compression_enabled CdnEndpoint#is_compression_enabled}.
        :param is_http_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#is_http_allowed CdnEndpoint#is_http_allowed}.
        :param is_https_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#is_https_allowed CdnEndpoint#is_https_allowed}.
        :param optimization_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#optimization_type CdnEndpoint#optimization_type}.
        :param origin_host_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#origin_host_header CdnEndpoint#origin_host_header}.
        :param origin_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#origin_path CdnEndpoint#origin_path}.
        :param probe_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#probe_path CdnEndpoint#probe_path}.
        :param querystring_caching_behaviour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#querystring_caching_behaviour CdnEndpoint#querystring_caching_behaviour}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#tags CdnEndpoint#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#timeouts CdnEndpoint#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(global_delivery_rule, dict):
            global_delivery_rule = CdnEndpointGlobalDeliveryRule(**global_delivery_rule)
        if isinstance(timeouts, dict):
            timeouts = CdnEndpointTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93648e532e4f915746f2f1e83d7ef07640d2221eb87a17b5f7a71eec21073ece)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument profile_name", value=profile_name, expected_type=type_hints["profile_name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument content_types_to_compress", value=content_types_to_compress, expected_type=type_hints["content_types_to_compress"])
            check_type(argname="argument delivery_rule", value=delivery_rule, expected_type=type_hints["delivery_rule"])
            check_type(argname="argument geo_filter", value=geo_filter, expected_type=type_hints["geo_filter"])
            check_type(argname="argument global_delivery_rule", value=global_delivery_rule, expected_type=type_hints["global_delivery_rule"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_compression_enabled", value=is_compression_enabled, expected_type=type_hints["is_compression_enabled"])
            check_type(argname="argument is_http_allowed", value=is_http_allowed, expected_type=type_hints["is_http_allowed"])
            check_type(argname="argument is_https_allowed", value=is_https_allowed, expected_type=type_hints["is_https_allowed"])
            check_type(argname="argument optimization_type", value=optimization_type, expected_type=type_hints["optimization_type"])
            check_type(argname="argument origin_host_header", value=origin_host_header, expected_type=type_hints["origin_host_header"])
            check_type(argname="argument origin_path", value=origin_path, expected_type=type_hints["origin_path"])
            check_type(argname="argument probe_path", value=probe_path, expected_type=type_hints["probe_path"])
            check_type(argname="argument querystring_caching_behaviour", value=querystring_caching_behaviour, expected_type=type_hints["querystring_caching_behaviour"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "origin": origin,
            "profile_name": profile_name,
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
        if content_types_to_compress is not None:
            self._values["content_types_to_compress"] = content_types_to_compress
        if delivery_rule is not None:
            self._values["delivery_rule"] = delivery_rule
        if geo_filter is not None:
            self._values["geo_filter"] = geo_filter
        if global_delivery_rule is not None:
            self._values["global_delivery_rule"] = global_delivery_rule
        if id is not None:
            self._values["id"] = id
        if is_compression_enabled is not None:
            self._values["is_compression_enabled"] = is_compression_enabled
        if is_http_allowed is not None:
            self._values["is_http_allowed"] = is_http_allowed
        if is_https_allowed is not None:
            self._values["is_https_allowed"] = is_https_allowed
        if optimization_type is not None:
            self._values["optimization_type"] = optimization_type
        if origin_host_header is not None:
            self._values["origin_host_header"] = origin_host_header
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if probe_path is not None:
            self._values["probe_path"] = probe_path
        if querystring_caching_behaviour is not None:
            self._values["querystring_caching_behaviour"] = querystring_caching_behaviour
        if tags is not None:
            self._values["tags"] = tags
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#location CdnEndpoint#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointOrigin"]]:
        '''origin block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#origin CdnEndpoint#origin}
        '''
        result = self._values.get("origin")
        assert result is not None, "Required property 'origin' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointOrigin"]], result)

    @builtins.property
    def profile_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#profile_name CdnEndpoint#profile_name}.'''
        result = self._values.get("profile_name")
        assert result is not None, "Required property 'profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#resource_group_name CdnEndpoint#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_types_to_compress(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#content_types_to_compress CdnEndpoint#content_types_to_compress}.'''
        result = self._values.get("content_types_to_compress")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def delivery_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRule"]]]:
        '''delivery_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#delivery_rule CdnEndpoint#delivery_rule}
        '''
        result = self._values.get("delivery_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRule"]]], result)

    @builtins.property
    def geo_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointGeoFilter"]]]:
        '''geo_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#geo_filter CdnEndpoint#geo_filter}
        '''
        result = self._values.get("geo_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointGeoFilter"]]], result)

    @builtins.property
    def global_delivery_rule(self) -> typing.Optional["CdnEndpointGlobalDeliveryRule"]:
        '''global_delivery_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#global_delivery_rule CdnEndpoint#global_delivery_rule}
        '''
        result = self._values.get("global_delivery_rule")
        return typing.cast(typing.Optional["CdnEndpointGlobalDeliveryRule"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#id CdnEndpoint#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_compression_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#is_compression_enabled CdnEndpoint#is_compression_enabled}.'''
        result = self._values.get("is_compression_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_http_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#is_http_allowed CdnEndpoint#is_http_allowed}.'''
        result = self._values.get("is_http_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_https_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#is_https_allowed CdnEndpoint#is_https_allowed}.'''
        result = self._values.get("is_https_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def optimization_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#optimization_type CdnEndpoint#optimization_type}.'''
        result = self._values.get("optimization_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_host_header(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#origin_host_header CdnEndpoint#origin_host_header}.'''
        result = self._values.get("origin_host_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#origin_path CdnEndpoint#origin_path}.'''
        result = self._values.get("origin_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def probe_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#probe_path CdnEndpoint#probe_path}.'''
        result = self._values.get("probe_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def querystring_caching_behaviour(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#querystring_caching_behaviour CdnEndpoint#querystring_caching_behaviour}.'''
        result = self._values.get("querystring_caching_behaviour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#tags CdnEndpoint#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CdnEndpointTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#timeouts CdnEndpoint#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CdnEndpointTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRule",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "order": "order",
        "cache_expiration_action": "cacheExpirationAction",
        "cache_key_query_string_action": "cacheKeyQueryStringAction",
        "cookies_condition": "cookiesCondition",
        "device_condition": "deviceCondition",
        "http_version_condition": "httpVersionCondition",
        "modify_request_header_action": "modifyRequestHeaderAction",
        "modify_response_header_action": "modifyResponseHeaderAction",
        "post_arg_condition": "postArgCondition",
        "query_string_condition": "queryStringCondition",
        "remote_address_condition": "remoteAddressCondition",
        "request_body_condition": "requestBodyCondition",
        "request_header_condition": "requestHeaderCondition",
        "request_method_condition": "requestMethodCondition",
        "request_scheme_condition": "requestSchemeCondition",
        "request_uri_condition": "requestUriCondition",
        "url_file_extension_condition": "urlFileExtensionCondition",
        "url_file_name_condition": "urlFileNameCondition",
        "url_path_condition": "urlPathCondition",
        "url_redirect_action": "urlRedirectAction",
        "url_rewrite_action": "urlRewriteAction",
    },
)
class CdnEndpointDeliveryRule:
    def __init__(
        self,
        *,
        name: builtins.str,
        order: jsii.Number,
        cache_expiration_action: typing.Optional[typing.Union["CdnEndpointDeliveryRuleCacheExpirationAction", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_key_query_string_action: typing.Optional[typing.Union["CdnEndpointDeliveryRuleCacheKeyQueryStringAction", typing.Dict[builtins.str, typing.Any]]] = None,
        cookies_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleCookiesCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        device_condition: typing.Optional[typing.Union["CdnEndpointDeliveryRuleDeviceCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        http_version_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleHttpVersionCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        modify_request_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleModifyRequestHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        modify_response_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleModifyResponseHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_arg_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRulePostArgCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_string_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleQueryStringCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        remote_address_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleRemoteAddressCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_body_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleRequestBodyCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleRequestHeaderCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_method_condition: typing.Optional[typing.Union["CdnEndpointDeliveryRuleRequestMethodCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        request_scheme_condition: typing.Optional[typing.Union["CdnEndpointDeliveryRuleRequestSchemeCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        request_uri_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleRequestUriCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_file_extension_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleUrlFileExtensionCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_file_name_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleUrlFileNameCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_path_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleUrlPathCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_redirect_action: typing.Optional[typing.Union["CdnEndpointDeliveryRuleUrlRedirectAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite_action: typing.Optional[typing.Union["CdnEndpointDeliveryRuleUrlRewriteAction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.
        :param order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#order CdnEndpoint#order}.
        :param cache_expiration_action: cache_expiration_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_expiration_action CdnEndpoint#cache_expiration_action}
        :param cache_key_query_string_action: cache_key_query_string_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_key_query_string_action CdnEndpoint#cache_key_query_string_action}
        :param cookies_condition: cookies_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cookies_condition CdnEndpoint#cookies_condition}
        :param device_condition: device_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#device_condition CdnEndpoint#device_condition}
        :param http_version_condition: http_version_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#http_version_condition CdnEndpoint#http_version_condition}
        :param modify_request_header_action: modify_request_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_request_header_action CdnEndpoint#modify_request_header_action}
        :param modify_response_header_action: modify_response_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_response_header_action CdnEndpoint#modify_response_header_action}
        :param post_arg_condition: post_arg_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#post_arg_condition CdnEndpoint#post_arg_condition}
        :param query_string_condition: query_string_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#query_string_condition CdnEndpoint#query_string_condition}
        :param remote_address_condition: remote_address_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#remote_address_condition CdnEndpoint#remote_address_condition}
        :param request_body_condition: request_body_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_body_condition CdnEndpoint#request_body_condition}
        :param request_header_condition: request_header_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_header_condition CdnEndpoint#request_header_condition}
        :param request_method_condition: request_method_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_method_condition CdnEndpoint#request_method_condition}
        :param request_scheme_condition: request_scheme_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_scheme_condition CdnEndpoint#request_scheme_condition}
        :param request_uri_condition: request_uri_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_uri_condition CdnEndpoint#request_uri_condition}
        :param url_file_extension_condition: url_file_extension_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_file_extension_condition CdnEndpoint#url_file_extension_condition}
        :param url_file_name_condition: url_file_name_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_file_name_condition CdnEndpoint#url_file_name_condition}
        :param url_path_condition: url_path_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_path_condition CdnEndpoint#url_path_condition}
        :param url_redirect_action: url_redirect_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_redirect_action CdnEndpoint#url_redirect_action}
        :param url_rewrite_action: url_rewrite_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_rewrite_action CdnEndpoint#url_rewrite_action}
        '''
        if isinstance(cache_expiration_action, dict):
            cache_expiration_action = CdnEndpointDeliveryRuleCacheExpirationAction(**cache_expiration_action)
        if isinstance(cache_key_query_string_action, dict):
            cache_key_query_string_action = CdnEndpointDeliveryRuleCacheKeyQueryStringAction(**cache_key_query_string_action)
        if isinstance(device_condition, dict):
            device_condition = CdnEndpointDeliveryRuleDeviceCondition(**device_condition)
        if isinstance(request_method_condition, dict):
            request_method_condition = CdnEndpointDeliveryRuleRequestMethodCondition(**request_method_condition)
        if isinstance(request_scheme_condition, dict):
            request_scheme_condition = CdnEndpointDeliveryRuleRequestSchemeCondition(**request_scheme_condition)
        if isinstance(url_redirect_action, dict):
            url_redirect_action = CdnEndpointDeliveryRuleUrlRedirectAction(**url_redirect_action)
        if isinstance(url_rewrite_action, dict):
            url_rewrite_action = CdnEndpointDeliveryRuleUrlRewriteAction(**url_rewrite_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba369dedcc5cdb7753a7d88222484c3bda996c7a9a123203eddca7a0ff83d124)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument cache_expiration_action", value=cache_expiration_action, expected_type=type_hints["cache_expiration_action"])
            check_type(argname="argument cache_key_query_string_action", value=cache_key_query_string_action, expected_type=type_hints["cache_key_query_string_action"])
            check_type(argname="argument cookies_condition", value=cookies_condition, expected_type=type_hints["cookies_condition"])
            check_type(argname="argument device_condition", value=device_condition, expected_type=type_hints["device_condition"])
            check_type(argname="argument http_version_condition", value=http_version_condition, expected_type=type_hints["http_version_condition"])
            check_type(argname="argument modify_request_header_action", value=modify_request_header_action, expected_type=type_hints["modify_request_header_action"])
            check_type(argname="argument modify_response_header_action", value=modify_response_header_action, expected_type=type_hints["modify_response_header_action"])
            check_type(argname="argument post_arg_condition", value=post_arg_condition, expected_type=type_hints["post_arg_condition"])
            check_type(argname="argument query_string_condition", value=query_string_condition, expected_type=type_hints["query_string_condition"])
            check_type(argname="argument remote_address_condition", value=remote_address_condition, expected_type=type_hints["remote_address_condition"])
            check_type(argname="argument request_body_condition", value=request_body_condition, expected_type=type_hints["request_body_condition"])
            check_type(argname="argument request_header_condition", value=request_header_condition, expected_type=type_hints["request_header_condition"])
            check_type(argname="argument request_method_condition", value=request_method_condition, expected_type=type_hints["request_method_condition"])
            check_type(argname="argument request_scheme_condition", value=request_scheme_condition, expected_type=type_hints["request_scheme_condition"])
            check_type(argname="argument request_uri_condition", value=request_uri_condition, expected_type=type_hints["request_uri_condition"])
            check_type(argname="argument url_file_extension_condition", value=url_file_extension_condition, expected_type=type_hints["url_file_extension_condition"])
            check_type(argname="argument url_file_name_condition", value=url_file_name_condition, expected_type=type_hints["url_file_name_condition"])
            check_type(argname="argument url_path_condition", value=url_path_condition, expected_type=type_hints["url_path_condition"])
            check_type(argname="argument url_redirect_action", value=url_redirect_action, expected_type=type_hints["url_redirect_action"])
            check_type(argname="argument url_rewrite_action", value=url_rewrite_action, expected_type=type_hints["url_rewrite_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "order": order,
        }
        if cache_expiration_action is not None:
            self._values["cache_expiration_action"] = cache_expiration_action
        if cache_key_query_string_action is not None:
            self._values["cache_key_query_string_action"] = cache_key_query_string_action
        if cookies_condition is not None:
            self._values["cookies_condition"] = cookies_condition
        if device_condition is not None:
            self._values["device_condition"] = device_condition
        if http_version_condition is not None:
            self._values["http_version_condition"] = http_version_condition
        if modify_request_header_action is not None:
            self._values["modify_request_header_action"] = modify_request_header_action
        if modify_response_header_action is not None:
            self._values["modify_response_header_action"] = modify_response_header_action
        if post_arg_condition is not None:
            self._values["post_arg_condition"] = post_arg_condition
        if query_string_condition is not None:
            self._values["query_string_condition"] = query_string_condition
        if remote_address_condition is not None:
            self._values["remote_address_condition"] = remote_address_condition
        if request_body_condition is not None:
            self._values["request_body_condition"] = request_body_condition
        if request_header_condition is not None:
            self._values["request_header_condition"] = request_header_condition
        if request_method_condition is not None:
            self._values["request_method_condition"] = request_method_condition
        if request_scheme_condition is not None:
            self._values["request_scheme_condition"] = request_scheme_condition
        if request_uri_condition is not None:
            self._values["request_uri_condition"] = request_uri_condition
        if url_file_extension_condition is not None:
            self._values["url_file_extension_condition"] = url_file_extension_condition
        if url_file_name_condition is not None:
            self._values["url_file_name_condition"] = url_file_name_condition
        if url_path_condition is not None:
            self._values["url_path_condition"] = url_path_condition
        if url_redirect_action is not None:
            self._values["url_redirect_action"] = url_redirect_action
        if url_rewrite_action is not None:
            self._values["url_rewrite_action"] = url_rewrite_action

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def order(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#order CdnEndpoint#order}.'''
        result = self._values.get("order")
        assert result is not None, "Required property 'order' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cache_expiration_action(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleCacheExpirationAction"]:
        '''cache_expiration_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_expiration_action CdnEndpoint#cache_expiration_action}
        '''
        result = self._values.get("cache_expiration_action")
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleCacheExpirationAction"], result)

    @builtins.property
    def cache_key_query_string_action(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleCacheKeyQueryStringAction"]:
        '''cache_key_query_string_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_key_query_string_action CdnEndpoint#cache_key_query_string_action}
        '''
        result = self._values.get("cache_key_query_string_action")
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleCacheKeyQueryStringAction"], result)

    @builtins.property
    def cookies_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleCookiesCondition"]]]:
        '''cookies_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cookies_condition CdnEndpoint#cookies_condition}
        '''
        result = self._values.get("cookies_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleCookiesCondition"]]], result)

    @builtins.property
    def device_condition(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleDeviceCondition"]:
        '''device_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#device_condition CdnEndpoint#device_condition}
        '''
        result = self._values.get("device_condition")
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleDeviceCondition"], result)

    @builtins.property
    def http_version_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleHttpVersionCondition"]]]:
        '''http_version_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#http_version_condition CdnEndpoint#http_version_condition}
        '''
        result = self._values.get("http_version_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleHttpVersionCondition"]]], result)

    @builtins.property
    def modify_request_header_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleModifyRequestHeaderAction"]]]:
        '''modify_request_header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_request_header_action CdnEndpoint#modify_request_header_action}
        '''
        result = self._values.get("modify_request_header_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleModifyRequestHeaderAction"]]], result)

    @builtins.property
    def modify_response_header_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleModifyResponseHeaderAction"]]]:
        '''modify_response_header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_response_header_action CdnEndpoint#modify_response_header_action}
        '''
        result = self._values.get("modify_response_header_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleModifyResponseHeaderAction"]]], result)

    @builtins.property
    def post_arg_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRulePostArgCondition"]]]:
        '''post_arg_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#post_arg_condition CdnEndpoint#post_arg_condition}
        '''
        result = self._values.get("post_arg_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRulePostArgCondition"]]], result)

    @builtins.property
    def query_string_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleQueryStringCondition"]]]:
        '''query_string_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#query_string_condition CdnEndpoint#query_string_condition}
        '''
        result = self._values.get("query_string_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleQueryStringCondition"]]], result)

    @builtins.property
    def remote_address_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRemoteAddressCondition"]]]:
        '''remote_address_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#remote_address_condition CdnEndpoint#remote_address_condition}
        '''
        result = self._values.get("remote_address_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRemoteAddressCondition"]]], result)

    @builtins.property
    def request_body_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestBodyCondition"]]]:
        '''request_body_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_body_condition CdnEndpoint#request_body_condition}
        '''
        result = self._values.get("request_body_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestBodyCondition"]]], result)

    @builtins.property
    def request_header_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestHeaderCondition"]]]:
        '''request_header_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_header_condition CdnEndpoint#request_header_condition}
        '''
        result = self._values.get("request_header_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestHeaderCondition"]]], result)

    @builtins.property
    def request_method_condition(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleRequestMethodCondition"]:
        '''request_method_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_method_condition CdnEndpoint#request_method_condition}
        '''
        result = self._values.get("request_method_condition")
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleRequestMethodCondition"], result)

    @builtins.property
    def request_scheme_condition(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleRequestSchemeCondition"]:
        '''request_scheme_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_scheme_condition CdnEndpoint#request_scheme_condition}
        '''
        result = self._values.get("request_scheme_condition")
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleRequestSchemeCondition"], result)

    @builtins.property
    def request_uri_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestUriCondition"]]]:
        '''request_uri_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#request_uri_condition CdnEndpoint#request_uri_condition}
        '''
        result = self._values.get("request_uri_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestUriCondition"]]], result)

    @builtins.property
    def url_file_extension_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlFileExtensionCondition"]]]:
        '''url_file_extension_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_file_extension_condition CdnEndpoint#url_file_extension_condition}
        '''
        result = self._values.get("url_file_extension_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlFileExtensionCondition"]]], result)

    @builtins.property
    def url_file_name_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlFileNameCondition"]]]:
        '''url_file_name_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_file_name_condition CdnEndpoint#url_file_name_condition}
        '''
        result = self._values.get("url_file_name_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlFileNameCondition"]]], result)

    @builtins.property
    def url_path_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlPathCondition"]]]:
        '''url_path_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_path_condition CdnEndpoint#url_path_condition}
        '''
        result = self._values.get("url_path_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlPathCondition"]]], result)

    @builtins.property
    def url_redirect_action(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleUrlRedirectAction"]:
        '''url_redirect_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_redirect_action CdnEndpoint#url_redirect_action}
        '''
        result = self._values.get("url_redirect_action")
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleUrlRedirectAction"], result)

    @builtins.property
    def url_rewrite_action(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleUrlRewriteAction"]:
        '''url_rewrite_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_rewrite_action CdnEndpoint#url_rewrite_action}
        '''
        result = self._values.get("url_rewrite_action")
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleUrlRewriteAction"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleCacheExpirationAction",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior", "duration": "duration"},
)
class CdnEndpointDeliveryRuleCacheExpirationAction:
    def __init__(
        self,
        *,
        behavior: builtins.str,
        duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#duration CdnEndpoint#duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19bce8b7e4b2b2a7df235f531dc44a4bd89855cfdf77a5192e52430252ca67f5)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
        }
        if duration is not None:
            self._values["duration"] = duration

    @builtins.property
    def behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.'''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#duration CdnEndpoint#duration}.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleCacheExpirationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleCacheExpirationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleCacheExpirationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eb15238a79d26db31496352704c1f57470354b4128b39dfc5cc10865e408487)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcb7eb2058bb49c974ef18c02761401af0a9d0af34070ef54af86a7e80b38e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d9d443092d6f6e34434f2ac766b614c1e0739fb24118732c67e5eb5f8f5f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointDeliveryRuleCacheExpirationAction]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleCacheExpirationAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointDeliveryRuleCacheExpirationAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2824998b31fdcddf3338f3b07fabdcda339324bfc00df1c095e83fe5c720036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleCacheKeyQueryStringAction",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior", "parameters": "parameters"},
)
class CdnEndpointDeliveryRuleCacheKeyQueryStringAction:
    def __init__(
        self,
        *,
        behavior: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#parameters CdnEndpoint#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c025233fbe4c8d443f80fb098acaf3b827ea2e299bc917082fb8457bb0cebc8)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.'''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#parameters CdnEndpoint#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleCacheKeyQueryStringAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleCacheKeyQueryStringActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleCacheKeyQueryStringActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb945e8901d392f13e29b1c1849aedf61a0b9b64de6d6afc0a2a563522b63ac6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3646fc21419cb02c14cfcd6e85183723c5504713abb0ba3777f43dc002dd8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae7eb22899fa27541a3bb8ef950868121de0060c8e75a10d17a07ec625b97322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointDeliveryRuleCacheKeyQueryStringAction]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleCacheKeyQueryStringAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointDeliveryRuleCacheKeyQueryStringAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3613bae0300f6aa2c617da8aeb37f6f979028b34c945ea4ee0e6dc979c0c1ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleCookiesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "selector": "selector",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnEndpointDeliveryRuleCookiesCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        selector: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param selector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#selector CdnEndpoint#selector}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf2372e11692f1e741a996622cb87f256e5242e26ace19798dd6b6164911f74)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "selector": selector,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#selector CdnEndpoint#selector}.'''
        result = self._values.get("selector")
        assert result is not None, "Required property 'selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleCookiesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleCookiesConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleCookiesConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1648fd0d60756e7750cf3e97d55e9932e026dfe3cf288e5b6357fa5ec2be02b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleCookiesConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2ad295e8312cb413c6cb0f6c8f97af3fbf3ffd795d6bff37d90c00242517ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleCookiesConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857a072de97f5480b7e5f2419c96b460537a4f31188436fe5e622d33952eb641)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfdb0d1c8646edcdf93a254e7e89648ab787560526937711f35ba4bbd2b4a9a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eb18387a724256475893f6bb513ddb4b6d981deca3da698ef0cb27385ea7a2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleCookiesCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleCookiesCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleCookiesCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0eca0a9addce5aa31cfa2dbc421b1e2d031c3380ed4f991333d50216d8cf944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleCookiesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleCookiesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d94672315bee5ed55b92c142c25efa1830f65c1b1929da334ba7510a2b4e028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac07b0eeb930c4f9b5ba3ad3bcbd18d683599e7fe1e43a473d6380561215491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147dac30d9b8e7720751a863e68e58825182a6cc1de2bfca510b48bdcfa60185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68c3e4c425342446f11ff75c1f506228df60243d742baf2e00837cb409b413f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c0791565d1e6cacea335b9a543aea3d015b8c85b1f76c147fe83f9c0f2203a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f522bbcb28bea4c99abaadedcbf63b9bc4ab40fa2f0100ae633250ec8d36a539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleCookiesCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleCookiesCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleCookiesCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe515a4abd216398604d4c39acc294d2fb1aa107b04f73796e920b5ac8a5eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleDeviceCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnEndpointDeliveryRuleDeviceCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818535170437e567ee8a7fd38ad8d5f56963a51ca5d71a63a9689e52dfad1dd1)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_values": match_values,
        }
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def match_values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleDeviceCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleDeviceConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleDeviceConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__937d5188c586d44526208f903d7ce5b0b9813da90f1c59b3d543cd1857ca51c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ef0528c80c68b0cba270409bf763321873c03bc8313f0032f18384cc156ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a36739e60eeb3906ab0c5c32b4e5e689b2ef9eb9f2c2ad81cd4112fd9e308b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87b45d84425b4ee02a6fd57aeadcce074e7ebc9b0cc23d6e6e4ceedaeb96033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CdnEndpointDeliveryRuleDeviceCondition]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleDeviceCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointDeliveryRuleDeviceCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6841db00878f23cd4ffdc12e52959c4366e858fb861fb24f808f46bebb6e9e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleHttpVersionCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnEndpointDeliveryRuleHttpVersionCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a5a5db1db80efdfbdc2e6ad7f1c0f09f1c7a904566dd6da94ef281a19ff3b3)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_values": match_values,
        }
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def match_values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleHttpVersionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleHttpVersionConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleHttpVersionConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f16c35da45ca0c6cbab0888c934181e1fc704a07027a678fc068b041545d6f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleHttpVersionConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008f9dcdfb9eb45f49ace89196d2a861361bc7ff6dfa75bd6abf6f8d48992991)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleHttpVersionConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c83b0bd476bef9d3778ba46aaca32d22ee6ed3b62576a934f6c868aa5aa8e9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4c1fed4072da2ab1181c0657f9a58213bb46aa79a307fd85935186887f1b64b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77bb6cab06b969a2e1cba3ece8983e996fcd4626f4c8fd4fb282e86d4ed396ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleHttpVersionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleHttpVersionCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleHttpVersionCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa623fbff112fdf75a13b44bdce15a66b7a19c7efe3c74bc152c00e6915cc933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleHttpVersionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleHttpVersionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__319e8f365d13927fa6ae5a14575404194619de2ecc237bc9d749d3549b60d280)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7683076264f24c424e9ddd2306d5d08fdccd665fd742693f6012701baa8c82b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645609687213e9d0bdfc163cdaa7b3f5edc938b15be2b74a8da245910f76e584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c3bfed28f1bcdaf57776e68b66ade63ca2ba42e0c389c8598bed0859e187c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleHttpVersionCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleHttpVersionCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleHttpVersionCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd717137f2ca44071e318548ef6e9e11b402e9bff8800c06320c76f52a487c08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8810f8f6bd590c248dafbcef8276df5f76ffdf8f2db1b6c1c7d5db847de6d21a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CdnEndpointDeliveryRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f41f9cece676e224623438c8d97cb38f78e44be86447746bba7857688186a53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9ea715e03b48aad94d6e838d3c75fe803239588736c8ac035ac1a8e37be6a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a54abb99d260ef4dfd43594a01e0746168ea8a9409c5db6eb6c509924be4e156)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57137c6fbdba3faec60f07c31dc1d43c2c5d0a2610fac8d48a5ea89ca74783a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af739ef6881d64014dc3a2156c8dcccadebd28c51a90e34ffac04a1fd7059557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleModifyRequestHeaderAction",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name", "value": "value"},
)
class CdnEndpointDeliveryRuleModifyRequestHeaderAction:
    def __init__(
        self,
        *,
        action: builtins.str,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#value CdnEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c8d6b6ccae17e80855ef445a8bedc4d94d8b168b255e33db689832a321ff36)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#value CdnEndpoint#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleModifyRequestHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleModifyRequestHeaderActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleModifyRequestHeaderActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fca17a6764d2affb6e3d94e0a96fabddae9e7b0c9ccc61e4159922bf282813a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleModifyRequestHeaderActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f248b6e53288745143f07d957b8c0b8a56ff774cfc53e81951052dd155061e2a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleModifyRequestHeaderActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214977410bf2b051389aad3ad8d2f9ba89049fdfddd6eb2853d2e0b2b3d810be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57538bfd408d63279c5a05211d742cef75d707e9beb11f7b361d801c4e2351e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5e9303d2764f12bf40ddafd43880a078e971f671f865dcb95cc99f839a01740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyRequestHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyRequestHeaderAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyRequestHeaderAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a548c62c5843b12bdaf0d111083fc9a157bde9ac1303154da82e9057fe786a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleModifyRequestHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleModifyRequestHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc19704d9adb530d2de247130b7ba0b11b2bbe0801380b0bdd3ee8289f8584f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7560b6a61b3990521c9131e87a031b147528ce8eab5a88b96ae58018747c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54fcaed5fe31ed233824774c8985fb81f10ab31a3858d13d91008cab01d853a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac143232a31d91e9dea110b575cdb83d9438594453edb8080c757c502ec34ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleModifyRequestHeaderAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleModifyRequestHeaderAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleModifyRequestHeaderAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696759835dc0d8a32ce99df67496b42ebf1d14afbd2f5482bf2c61f40077a63b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleModifyResponseHeaderAction",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name", "value": "value"},
)
class CdnEndpointDeliveryRuleModifyResponseHeaderAction:
    def __init__(
        self,
        *,
        action: builtins.str,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#value CdnEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a0dc236b6b588ba24aca9249964f5ceb2fdc50d3d09659a4cde22712ded26c)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#value CdnEndpoint#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleModifyResponseHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleModifyResponseHeaderActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleModifyResponseHeaderActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2842fae04589874c86aecf8bfdf70af4f2abba93d86673a259f15ac57bb93488)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleModifyResponseHeaderActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a473256200b9b6ae51dbec53b44f3413025be53036316e162415fba61ecde07)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleModifyResponseHeaderActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d991300d8c1447d0c82d83a288e2803f28d3b0366a1dca29fa7dbbc8d0570724)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48e211a3a3774c9d1c0eb6a85a71fb512d40cd67ed90c0d0883cc5dc1b2cd2ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93e3b235b62437dca56183f119bcc3ce2f501dd1e2db372dd351a7cbb43fa5b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyResponseHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyResponseHeaderAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyResponseHeaderAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1529f72fd32ba921e2388933fbecb5b236e9d9fd942470ee4c1ae3b54716ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleModifyResponseHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleModifyResponseHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b67fa65b4cc14315c4c6ed9a28ea1d91d6315dc7e36842914954a956c51299c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0cfffedd91a03eeba2af35a5b89e54a6e9e4852e300ca88ab748e14b8740ce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69f500f5e79d6ad67de524fe2daed9a87ae13c7476390803136e7eb74e8b50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52926d6033b845d94b55a361c715d3ee94b2766981593dbe5f82ce9cc949728b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleModifyResponseHeaderAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleModifyResponseHeaderAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleModifyResponseHeaderAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0d846ad533acb444e2c44ab0f18803e709198e0c8c0223b14b23498003f12a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f79becfc080681af33c3d8a68c42d9b20f5f1bf9c2176f5a21fd3a202c9414bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCacheExpirationAction")
    def put_cache_expiration_action(
        self,
        *,
        behavior: builtins.str,
        duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#duration CdnEndpoint#duration}.
        '''
        value = CdnEndpointDeliveryRuleCacheExpirationAction(
            behavior=behavior, duration=duration
        )

        return typing.cast(None, jsii.invoke(self, "putCacheExpirationAction", [value]))

    @jsii.member(jsii_name="putCacheKeyQueryStringAction")
    def put_cache_key_query_string_action(
        self,
        *,
        behavior: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#parameters CdnEndpoint#parameters}.
        '''
        value = CdnEndpointDeliveryRuleCacheKeyQueryStringAction(
            behavior=behavior, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putCacheKeyQueryStringAction", [value]))

    @jsii.member(jsii_name="putCookiesCondition")
    def put_cookies_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleCookiesCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3144f1b90150da7cf6fd30ad07ec0451e9256aa7be757acab4d2ad8795ffc21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCookiesCondition", [value]))

    @jsii.member(jsii_name="putDeviceCondition")
    def put_device_condition(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        '''
        value = CdnEndpointDeliveryRuleDeviceCondition(
            match_values=match_values,
            negate_condition=negate_condition,
            operator=operator,
        )

        return typing.cast(None, jsii.invoke(self, "putDeviceCondition", [value]))

    @jsii.member(jsii_name="putHttpVersionCondition")
    def put_http_version_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleHttpVersionCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ccfc92eb43e6c212e2d1a1d2fe20bfbdb4f4c764908eeea33abf1ba04e21f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpVersionCondition", [value]))

    @jsii.member(jsii_name="putModifyRequestHeaderAction")
    def put_modify_request_header_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleModifyRequestHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54d2ed0df78b5b7caf50d221d47047a99e5f5df1ef5c500fe770ea0eed2b76c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putModifyRequestHeaderAction", [value]))

    @jsii.member(jsii_name="putModifyResponseHeaderAction")
    def put_modify_response_header_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleModifyResponseHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e009d1027cf58c341b86cc5fdee0e0ec666ea68fb3ef108a18436914bc2f87ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putModifyResponseHeaderAction", [value]))

    @jsii.member(jsii_name="putPostArgCondition")
    def put_post_arg_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRulePostArgCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58edef75f7e8721a65377bb6b2becd15f1c53ad3f465028cbd4a20332d1e668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostArgCondition", [value]))

    @jsii.member(jsii_name="putQueryStringCondition")
    def put_query_string_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleQueryStringCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1748e8bd31a05f249d6bf383495ceaba7c9a2a970a535e9aec9e16db77e06980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryStringCondition", [value]))

    @jsii.member(jsii_name="putRemoteAddressCondition")
    def put_remote_address_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleRemoteAddressCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc8291452e93c84cf8900c37987f27f9fc3a028fcf46c1c188d1c22fc0ea2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRemoteAddressCondition", [value]))

    @jsii.member(jsii_name="putRequestBodyCondition")
    def put_request_body_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleRequestBodyCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37d13a437659f60a011439c2245e1c76fbc2d6b292a457b5b8ee92419946cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestBodyCondition", [value]))

    @jsii.member(jsii_name="putRequestHeaderCondition")
    def put_request_header_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleRequestHeaderCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279b0dde1c1044495e4372e422cacd7001f8fc7b30a06460115baa6fe9f3749c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaderCondition", [value]))

    @jsii.member(jsii_name="putRequestMethodCondition")
    def put_request_method_condition(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        '''
        value = CdnEndpointDeliveryRuleRequestMethodCondition(
            match_values=match_values,
            negate_condition=negate_condition,
            operator=operator,
        )

        return typing.cast(None, jsii.invoke(self, "putRequestMethodCondition", [value]))

    @jsii.member(jsii_name="putRequestSchemeCondition")
    def put_request_scheme_condition(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        '''
        value = CdnEndpointDeliveryRuleRequestSchemeCondition(
            match_values=match_values,
            negate_condition=negate_condition,
            operator=operator,
        )

        return typing.cast(None, jsii.invoke(self, "putRequestSchemeCondition", [value]))

    @jsii.member(jsii_name="putRequestUriCondition")
    def put_request_uri_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleRequestUriCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be862f03e042c57360d447d38ebd8962ff2fd81c9e2c9fa7e93672606dbbb2f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestUriCondition", [value]))

    @jsii.member(jsii_name="putUrlFileExtensionCondition")
    def put_url_file_extension_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleUrlFileExtensionCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3cb0ada5494367d0c874827928513fe1fe81dabcf5142c67f10344e553e5da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrlFileExtensionCondition", [value]))

    @jsii.member(jsii_name="putUrlFileNameCondition")
    def put_url_file_name_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleUrlFileNameCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc91802e1fc180dcef2236d9e968a3eb1307eac27970e90acec7080150cf4b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrlFileNameCondition", [value]))

    @jsii.member(jsii_name="putUrlPathCondition")
    def put_url_path_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointDeliveryRuleUrlPathCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681906a64d67fcc0eb7c81fbfedeabfe5aac4e90161bbf5781038d2e05a1fb33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrlPathCondition", [value]))

    @jsii.member(jsii_name="putUrlRedirectAction")
    def put_url_redirect_action(
        self,
        *,
        redirect_type: builtins.str,
        fragment: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param redirect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#redirect_type CdnEndpoint#redirect_type}.
        :param fragment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#fragment CdnEndpoint#fragment}.
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#hostname CdnEndpoint#hostname}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#path CdnEndpoint#path}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#protocol CdnEndpoint#protocol}.
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#query_string CdnEndpoint#query_string}.
        '''
        value = CdnEndpointDeliveryRuleUrlRedirectAction(
            redirect_type=redirect_type,
            fragment=fragment,
            hostname=hostname,
            path=path,
            protocol=protocol,
            query_string=query_string,
        )

        return typing.cast(None, jsii.invoke(self, "putUrlRedirectAction", [value]))

    @jsii.member(jsii_name="putUrlRewriteAction")
    def put_url_rewrite_action(
        self,
        *,
        destination: builtins.str,
        source_pattern: builtins.str,
        preserve_unmatched_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#destination CdnEndpoint#destination}.
        :param source_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#source_pattern CdnEndpoint#source_pattern}.
        :param preserve_unmatched_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#preserve_unmatched_path CdnEndpoint#preserve_unmatched_path}.
        '''
        value = CdnEndpointDeliveryRuleUrlRewriteAction(
            destination=destination,
            source_pattern=source_pattern,
            preserve_unmatched_path=preserve_unmatched_path,
        )

        return typing.cast(None, jsii.invoke(self, "putUrlRewriteAction", [value]))

    @jsii.member(jsii_name="resetCacheExpirationAction")
    def reset_cache_expiration_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheExpirationAction", []))

    @jsii.member(jsii_name="resetCacheKeyQueryStringAction")
    def reset_cache_key_query_string_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheKeyQueryStringAction", []))

    @jsii.member(jsii_name="resetCookiesCondition")
    def reset_cookies_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookiesCondition", []))

    @jsii.member(jsii_name="resetDeviceCondition")
    def reset_device_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceCondition", []))

    @jsii.member(jsii_name="resetHttpVersionCondition")
    def reset_http_version_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpVersionCondition", []))

    @jsii.member(jsii_name="resetModifyRequestHeaderAction")
    def reset_modify_request_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModifyRequestHeaderAction", []))

    @jsii.member(jsii_name="resetModifyResponseHeaderAction")
    def reset_modify_response_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModifyResponseHeaderAction", []))

    @jsii.member(jsii_name="resetPostArgCondition")
    def reset_post_arg_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostArgCondition", []))

    @jsii.member(jsii_name="resetQueryStringCondition")
    def reset_query_string_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringCondition", []))

    @jsii.member(jsii_name="resetRemoteAddressCondition")
    def reset_remote_address_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteAddressCondition", []))

    @jsii.member(jsii_name="resetRequestBodyCondition")
    def reset_request_body_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBodyCondition", []))

    @jsii.member(jsii_name="resetRequestHeaderCondition")
    def reset_request_header_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaderCondition", []))

    @jsii.member(jsii_name="resetRequestMethodCondition")
    def reset_request_method_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestMethodCondition", []))

    @jsii.member(jsii_name="resetRequestSchemeCondition")
    def reset_request_scheme_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestSchemeCondition", []))

    @jsii.member(jsii_name="resetRequestUriCondition")
    def reset_request_uri_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestUriCondition", []))

    @jsii.member(jsii_name="resetUrlFileExtensionCondition")
    def reset_url_file_extension_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlFileExtensionCondition", []))

    @jsii.member(jsii_name="resetUrlFileNameCondition")
    def reset_url_file_name_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlFileNameCondition", []))

    @jsii.member(jsii_name="resetUrlPathCondition")
    def reset_url_path_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlPathCondition", []))

    @jsii.member(jsii_name="resetUrlRedirectAction")
    def reset_url_redirect_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRedirectAction", []))

    @jsii.member(jsii_name="resetUrlRewriteAction")
    def reset_url_rewrite_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRewriteAction", []))

    @builtins.property
    @jsii.member(jsii_name="cacheExpirationAction")
    def cache_expiration_action(
        self,
    ) -> CdnEndpointDeliveryRuleCacheExpirationActionOutputReference:
        return typing.cast(CdnEndpointDeliveryRuleCacheExpirationActionOutputReference, jsii.get(self, "cacheExpirationAction"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyQueryStringAction")
    def cache_key_query_string_action(
        self,
    ) -> CdnEndpointDeliveryRuleCacheKeyQueryStringActionOutputReference:
        return typing.cast(CdnEndpointDeliveryRuleCacheKeyQueryStringActionOutputReference, jsii.get(self, "cacheKeyQueryStringAction"))

    @builtins.property
    @jsii.member(jsii_name="cookiesCondition")
    def cookies_condition(self) -> CdnEndpointDeliveryRuleCookiesConditionList:
        return typing.cast(CdnEndpointDeliveryRuleCookiesConditionList, jsii.get(self, "cookiesCondition"))

    @builtins.property
    @jsii.member(jsii_name="deviceCondition")
    def device_condition(self) -> CdnEndpointDeliveryRuleDeviceConditionOutputReference:
        return typing.cast(CdnEndpointDeliveryRuleDeviceConditionOutputReference, jsii.get(self, "deviceCondition"))

    @builtins.property
    @jsii.member(jsii_name="httpVersionCondition")
    def http_version_condition(self) -> CdnEndpointDeliveryRuleHttpVersionConditionList:
        return typing.cast(CdnEndpointDeliveryRuleHttpVersionConditionList, jsii.get(self, "httpVersionCondition"))

    @builtins.property
    @jsii.member(jsii_name="modifyRequestHeaderAction")
    def modify_request_header_action(
        self,
    ) -> CdnEndpointDeliveryRuleModifyRequestHeaderActionList:
        return typing.cast(CdnEndpointDeliveryRuleModifyRequestHeaderActionList, jsii.get(self, "modifyRequestHeaderAction"))

    @builtins.property
    @jsii.member(jsii_name="modifyResponseHeaderAction")
    def modify_response_header_action(
        self,
    ) -> CdnEndpointDeliveryRuleModifyResponseHeaderActionList:
        return typing.cast(CdnEndpointDeliveryRuleModifyResponseHeaderActionList, jsii.get(self, "modifyResponseHeaderAction"))

    @builtins.property
    @jsii.member(jsii_name="postArgCondition")
    def post_arg_condition(self) -> "CdnEndpointDeliveryRulePostArgConditionList":
        return typing.cast("CdnEndpointDeliveryRulePostArgConditionList", jsii.get(self, "postArgCondition"))

    @builtins.property
    @jsii.member(jsii_name="queryStringCondition")
    def query_string_condition(
        self,
    ) -> "CdnEndpointDeliveryRuleQueryStringConditionList":
        return typing.cast("CdnEndpointDeliveryRuleQueryStringConditionList", jsii.get(self, "queryStringCondition"))

    @builtins.property
    @jsii.member(jsii_name="remoteAddressCondition")
    def remote_address_condition(
        self,
    ) -> "CdnEndpointDeliveryRuleRemoteAddressConditionList":
        return typing.cast("CdnEndpointDeliveryRuleRemoteAddressConditionList", jsii.get(self, "remoteAddressCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyCondition")
    def request_body_condition(
        self,
    ) -> "CdnEndpointDeliveryRuleRequestBodyConditionList":
        return typing.cast("CdnEndpointDeliveryRuleRequestBodyConditionList", jsii.get(self, "requestBodyCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderCondition")
    def request_header_condition(
        self,
    ) -> "CdnEndpointDeliveryRuleRequestHeaderConditionList":
        return typing.cast("CdnEndpointDeliveryRuleRequestHeaderConditionList", jsii.get(self, "requestHeaderCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestMethodCondition")
    def request_method_condition(
        self,
    ) -> "CdnEndpointDeliveryRuleRequestMethodConditionOutputReference":
        return typing.cast("CdnEndpointDeliveryRuleRequestMethodConditionOutputReference", jsii.get(self, "requestMethodCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestSchemeCondition")
    def request_scheme_condition(
        self,
    ) -> "CdnEndpointDeliveryRuleRequestSchemeConditionOutputReference":
        return typing.cast("CdnEndpointDeliveryRuleRequestSchemeConditionOutputReference", jsii.get(self, "requestSchemeCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestUriCondition")
    def request_uri_condition(self) -> "CdnEndpointDeliveryRuleRequestUriConditionList":
        return typing.cast("CdnEndpointDeliveryRuleRequestUriConditionList", jsii.get(self, "requestUriCondition"))

    @builtins.property
    @jsii.member(jsii_name="urlFileExtensionCondition")
    def url_file_extension_condition(
        self,
    ) -> "CdnEndpointDeliveryRuleUrlFileExtensionConditionList":
        return typing.cast("CdnEndpointDeliveryRuleUrlFileExtensionConditionList", jsii.get(self, "urlFileExtensionCondition"))

    @builtins.property
    @jsii.member(jsii_name="urlFileNameCondition")
    def url_file_name_condition(
        self,
    ) -> "CdnEndpointDeliveryRuleUrlFileNameConditionList":
        return typing.cast("CdnEndpointDeliveryRuleUrlFileNameConditionList", jsii.get(self, "urlFileNameCondition"))

    @builtins.property
    @jsii.member(jsii_name="urlPathCondition")
    def url_path_condition(self) -> "CdnEndpointDeliveryRuleUrlPathConditionList":
        return typing.cast("CdnEndpointDeliveryRuleUrlPathConditionList", jsii.get(self, "urlPathCondition"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirectAction")
    def url_redirect_action(
        self,
    ) -> "CdnEndpointDeliveryRuleUrlRedirectActionOutputReference":
        return typing.cast("CdnEndpointDeliveryRuleUrlRedirectActionOutputReference", jsii.get(self, "urlRedirectAction"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteAction")
    def url_rewrite_action(
        self,
    ) -> "CdnEndpointDeliveryRuleUrlRewriteActionOutputReference":
        return typing.cast("CdnEndpointDeliveryRuleUrlRewriteActionOutputReference", jsii.get(self, "urlRewriteAction"))

    @builtins.property
    @jsii.member(jsii_name="cacheExpirationActionInput")
    def cache_expiration_action_input(
        self,
    ) -> typing.Optional[CdnEndpointDeliveryRuleCacheExpirationAction]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleCacheExpirationAction], jsii.get(self, "cacheExpirationActionInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyQueryStringActionInput")
    def cache_key_query_string_action_input(
        self,
    ) -> typing.Optional[CdnEndpointDeliveryRuleCacheKeyQueryStringAction]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleCacheKeyQueryStringAction], jsii.get(self, "cacheKeyQueryStringActionInput"))

    @builtins.property
    @jsii.member(jsii_name="cookiesConditionInput")
    def cookies_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleCookiesCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleCookiesCondition]]], jsii.get(self, "cookiesConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceConditionInput")
    def device_condition_input(
        self,
    ) -> typing.Optional[CdnEndpointDeliveryRuleDeviceCondition]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleDeviceCondition], jsii.get(self, "deviceConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpVersionConditionInput")
    def http_version_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleHttpVersionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleHttpVersionCondition]]], jsii.get(self, "httpVersionConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="modifyRequestHeaderActionInput")
    def modify_request_header_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyRequestHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyRequestHeaderAction]]], jsii.get(self, "modifyRequestHeaderActionInput"))

    @builtins.property
    @jsii.member(jsii_name="modifyResponseHeaderActionInput")
    def modify_response_header_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyResponseHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyResponseHeaderAction]]], jsii.get(self, "modifyResponseHeaderActionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="postArgConditionInput")
    def post_arg_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRulePostArgCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRulePostArgCondition"]]], jsii.get(self, "postArgConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringConditionInput")
    def query_string_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleQueryStringCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleQueryStringCondition"]]], jsii.get(self, "queryStringConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteAddressConditionInput")
    def remote_address_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRemoteAddressCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRemoteAddressCondition"]]], jsii.get(self, "remoteAddressConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyConditionInput")
    def request_body_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestBodyCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestBodyCondition"]]], jsii.get(self, "requestBodyConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderConditionInput")
    def request_header_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestHeaderCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestHeaderCondition"]]], jsii.get(self, "requestHeaderConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestMethodConditionInput")
    def request_method_condition_input(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleRequestMethodCondition"]:
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleRequestMethodCondition"], jsii.get(self, "requestMethodConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestSchemeConditionInput")
    def request_scheme_condition_input(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleRequestSchemeCondition"]:
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleRequestSchemeCondition"], jsii.get(self, "requestSchemeConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriConditionInput")
    def request_uri_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestUriCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleRequestUriCondition"]]], jsii.get(self, "requestUriConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlFileExtensionConditionInput")
    def url_file_extension_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlFileExtensionCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlFileExtensionCondition"]]], jsii.get(self, "urlFileExtensionConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlFileNameConditionInput")
    def url_file_name_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlFileNameCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlFileNameCondition"]]], jsii.get(self, "urlFileNameConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlPathConditionInput")
    def url_path_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlPathCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointDeliveryRuleUrlPathCondition"]]], jsii.get(self, "urlPathConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirectActionInput")
    def url_redirect_action_input(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleUrlRedirectAction"]:
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleUrlRedirectAction"], jsii.get(self, "urlRedirectActionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteActionInput")
    def url_rewrite_action_input(
        self,
    ) -> typing.Optional["CdnEndpointDeliveryRuleUrlRewriteAction"]:
        return typing.cast(typing.Optional["CdnEndpointDeliveryRuleUrlRewriteAction"], jsii.get(self, "urlRewriteActionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05157d1ee024a4021308772ce13740fbb1eb7018c61a6de26d2080cf49ca0896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "order"))

    @order.setter
    def order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddd5c03f705bf7a348aa3be86bb561fdcc4e42081ee56948b0977191b17ba89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8905aebd65ef0e74df962f16096edcb4a26b77eb29fe64fdbc5517757ad3c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRulePostArgCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "selector": "selector",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnEndpointDeliveryRulePostArgCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        selector: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param selector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#selector CdnEndpoint#selector}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a922fa5e3499db75cb1692240aee610ca2e5a3499fe4fa8befa572d8c727cb)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "selector": selector,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#selector CdnEndpoint#selector}.'''
        result = self._values.get("selector")
        assert result is not None, "Required property 'selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRulePostArgCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRulePostArgConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRulePostArgConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9af103a721aaae92811f0953a9be7ffefc4fdd6f3374458bbb61ec937a5b0d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRulePostArgConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90cc384682f37067486ed437cd7c367b39bbd7a7107360dc27b76937d8f5f99a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRulePostArgConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12e2c6e09a91ddea0035b4afca5bd3ddb9ae9d626095051e43e4a84580877af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21174c63b89d62c9a0eb58ad261e653aa8648e8e4ee3a47693dfae1172cb5116)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e4d0e2325bb14371a014a1ae2458f393eb659076c900afd51bc106b0140f5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRulePostArgCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRulePostArgCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRulePostArgCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e8c6a12a33d55664c6d401e3d0f6fa0c277cf8d588fdd025433d334326efa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRulePostArgConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRulePostArgConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1661deab8afbb0567395f9946110bccf520c16141842fcc021187df921e723ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d67019e8e079aa50d3bf4d026ad94c9b91c24ec97a465c4cd5f699536fc1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef1e478b5dad3ab0e8b34707f876916a932567849f7986250ac44a8ceaf7ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3773fff9451ef55f7979548a127256fabf527076b439f36f6a856d732bbfa408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d1b26bda01210a32cba81593802c769c201199696161dc32f476829c68a430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3a7858093ecc9c9afab80b15164bb5d2d3b3eb5ca4eccbbe4cd8b18c46b933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRulePostArgCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRulePostArgCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRulePostArgCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__932f67e1c6cdf536c22046a9f1bfb213cbc45f42b85785dc4f75a2fdf9b4f56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleQueryStringCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnEndpointDeliveryRuleQueryStringCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ab3bf66c80aaf836df029adc4b59bad5d30b16156a8f205c91083dce5894e1)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleQueryStringCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleQueryStringConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleQueryStringConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90516b85748f92ef391bdb0a4429aafbd2db106d1805c8259d632845a5164e72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleQueryStringConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b754fafdf207dd34c4c86fe527f856b81da98f89b3007945d1588a429b82ae1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleQueryStringConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1beb535d31995aaa2ace84078585de327bd101f51b1e5b0fc191fa31565e2792)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31aeda6f16fc0fbcd804b57ba3dac09c50e5f1893fb40942df87b4d2f707d51d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a871558091dfd4b47e6644cbe255d6991cde526faceff5950be963cd043ad291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleQueryStringCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleQueryStringCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleQueryStringCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87efd3dfab29e5518ef9d0769f60e392fe4cf0d0667f469e2ea50f08aaed662e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleQueryStringConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleQueryStringConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__028a4b31d9e4f1a8cf9ca476d6d1d3af7966a2504813466c40db3a21a844ae84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7d288ff79dd0eccdde12a4c33517968dd60e3566f1d44a31297b30badc1df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e693f5f1158712739ec8e4dd991c35ce4d2d085cc078b57f545e9821becf8be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9900b19a708eb341387b5fc8841df4481e187e980346cdf636137db4292e0a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a02f4a044d859c87187fffbf8fabe008b867ce6973f0bc5d4d50c2e8004d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleQueryStringCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleQueryStringCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleQueryStringCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebc95156f9e55a48b44d5bc3df007da01e2f86e7a98d09b9f1ceedab411c189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRemoteAddressCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
    },
)
class CdnEndpointDeliveryRuleRemoteAddressCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138e33eab1a3b5cda90ec33cad5c684da6ce2975dad58d056de2e8aa22fbb798)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleRemoteAddressCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleRemoteAddressConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRemoteAddressConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__759a44d67f4db72d540948a4f9b6b300d4ba965d43ad9ff74d02588dadeaadf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleRemoteAddressConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9101f3597fef2011883c046bd9fd64c7747f0d910a3ec7743c0e1b32f17053)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleRemoteAddressConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f96ddbdab071bff0599470d3ca7157ce1e113a942a3b950e441f058da65d0af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b91dd2cdcf77af3633db9eca89ff23da6a1aff35ef348dc6270eafe9c6a1d81a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c60ee39d5cc629710e15e9e4af29b778b811e8360b35497675d91fd19b76e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRemoteAddressCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRemoteAddressCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRemoteAddressCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2bdb7fb8fee690ca55c12484c5b48a2cc4554d576cb9be0930594251f06dc2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleRemoteAddressConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRemoteAddressConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a56efa392fba409a41a3175f809f56bf5f7805040c8adb42e0b6ca9a0e01b75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74cb12205985d05e40452634a5a8564151c66816ddf35e7212cd9e7869db58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2762bd372c76715b7380446d09efd793953023b37f773c0b2202447bfd530a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631c19cbeb1ac20bb2f0eb8d55b70d41d394df5e68a39b4ce0801682aad2da98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRemoteAddressCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRemoteAddressCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRemoteAddressCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e910f5f8d1c74fdc3fad92e5f4ad96195bfad652af5078c65afef4f5303a6e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestBodyCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnEndpointDeliveryRuleRequestBodyCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c6d4947d23c8b709b12c3f502240871d557acc73f881cf0a9ced3579eab3d8d)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleRequestBodyCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleRequestBodyConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestBodyConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50367a5e47f99be66896802637807718e9c2baecc037c19064ba6a0c8c78c520)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleRequestBodyConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa92dab5309ea58c99ecbccb9f4de72dd160892ce68c6acb6db5102224ed1b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleRequestBodyConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675b793483a39c6ea3c6e1a0a8fa630d037b71d84eb7c802f374bbd3c4364e7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da210c589d4566bd55af59bb3b0a005fedd5c93f1aea72c6683ca6fdde4b487e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dd30e250f42f3916a29759469ec159dfa37eced51090a7860cdafdc65f15461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestBodyCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestBodyCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestBodyCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bcb20e7c2b56d3572a595ebe227e4873e72d4fa88502a2282ce958cccc2fdf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleRequestBodyConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestBodyConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9833dc9986c7c0b25f9bc8acb0960ac52c17a78aa5073a17c5b144c885502fe7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e14fbff77d4e66d34bdeb0e6a6d57edc4f1dda27c1927f7194a0c1ae1b00ecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5f39442800e2ee52a0800207aef6ca5d655b42729a319468084de2d9979776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca966577f2c19f652136d1cc30f4932b8defb0994a9889f277a8577c2a6b402e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb8d7ed3e96b27fdd8e00de604d739c25a422004b6c1590e685cde18aa8af35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestBodyCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestBodyCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestBodyCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4936ba9051bb0ce88ab9c6c84c553271b9dee4ed0e82cca5658a0763eeb967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestHeaderCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "selector": "selector",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnEndpointDeliveryRuleRequestHeaderCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        selector: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param selector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#selector CdnEndpoint#selector}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5d6836fee5f078e531f7d463a678cfeeb21c9824502eef2c950b3bd0441b46)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "selector": selector,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#selector CdnEndpoint#selector}.'''
        result = self._values.get("selector")
        assert result is not None, "Required property 'selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleRequestHeaderCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleRequestHeaderConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestHeaderConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35eb6bd24ddfd60517240c539335d78e0c99b61ebeb1b08d169bd3cb66a3e413)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleRequestHeaderConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039dd869bf82924319841d0a1d9d9d676892a30555f93f13ede1added23f7704)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleRequestHeaderConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de340a044e4478bb1e73ac880000306427252e232e17194d4da61b3ea689225e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf89e0e3076fe39038182c4e671264e81330e0753adb0364a74b4d4f0ddcaa69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__620ac5389794c6a6946a0b7ea9e91d596426ca47505524c638328f0d7bf5c798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestHeaderCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestHeaderCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestHeaderCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ceb8013f87ec294e1bb27a55bfcd8d911b5396ca338d33761204587bb82ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleRequestHeaderConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestHeaderConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b652e5a3ae16234b96aab6ee0d1f29c314a228df28c72eaa4f33c5afbdf724f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df41f65acd0537bc3e3eb26d5f79279991e13417f5533e73497f605b78999ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0cd1950708c9ac0a1c569961e4042006f4b36cc8793e1457a1f69032a3d2708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6a2c85fe55ca530821d7996073f09a3a1326da8604c4ca5d9d46f7daec3281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef54d71733b55f0ed084f1d9df421b49a6e185b3e2a32f12dbd0c4e90275c846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e0ce2744729ae396725a1a2245330b8d355ca1bdc91701a7982c3d94792052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestHeaderCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestHeaderCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestHeaderCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df5ff9b1aad509da5ae5f44744c7db5ce746b9a25ff0438a77f8113ec467d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestMethodCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnEndpointDeliveryRuleRequestMethodCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c515ef3e210f4a6b5a57a8fd428f556e2a9f1fb22509e612506d966429ef5d)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_values": match_values,
        }
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def match_values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleRequestMethodCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleRequestMethodConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestMethodConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7695eb0ed2c7fd474e5a4539f37b5ad2f9fa7e3f8c4e55fd937869e1dd3f0812)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ca37fade34c26a261db88e69c235d1eebba0110c38dee9d4e18c2a76a5e0bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4829ed338398958df5cf13fcc08769943067c86813de30d20b6597bed4166cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4fb14cf44aa732c8d288c8cce45104daecbceaefd6a6966af16fb54748abb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointDeliveryRuleRequestMethodCondition]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleRequestMethodCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointDeliveryRuleRequestMethodCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88951c2f16d6c0d9abe960327805afaf29756de29f645cf58896937e7148774e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestSchemeCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnEndpointDeliveryRuleRequestSchemeCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa7a2b972eefa4ae63dd0bf66f7baacb8376dc936730865601aa25377aa32ca)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_values": match_values,
        }
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def match_values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleRequestSchemeCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleRequestSchemeConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestSchemeConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce3023ddc4ff0bddb71ef774d1a1733ae549545605e57451ca4a9a89e23d0010)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a89f15e70f4a99816d432639c8ad74af9e2357ee08dbacf6741c2f867a08de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc1cde2e4de0c560fcc06f6a0e09154371cc6b099ec02a1d72506d275eb6a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68247188ba5d7f8c3b32ebea62ecf3aaf11914f9d309869463bfc38bf2891624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointDeliveryRuleRequestSchemeCondition]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleRequestSchemeCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointDeliveryRuleRequestSchemeCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2843b8567634346b82e05169371ac2843104d2f5dadc9c56d6698698bdae67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestUriCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnEndpointDeliveryRuleRequestUriCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae428c59678975c18d7a3275a171de68e30084dc80d6d0fa31e248bb8095860)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleRequestUriCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleRequestUriConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestUriConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee4f620d82036b02891f18af4c7974a0b38e6887942147d2eac5d80948a34738)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleRequestUriConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f022988f5f72b456f786bee06ad5c05129e5e508f4e35b159d9377d6934efa2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleRequestUriConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb96d1af24091788d7aff513162d0b6772de5697d28a532d633dc731702e3b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3509bf2f7053d2fc87797094851b60e8f7e7cc06d866a767ec750c9e53e20a6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34470b0a7790a63b7a1f7b8bd022f436d1ecb5ed9a7f777841620cf485de0c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestUriCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestUriCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestUriCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe747b01c03cc9c339291313f10200618e7337fb28fe5ca086a56ab7b873523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleRequestUriConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleRequestUriConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de49e6ad781248398cff88e60edb5fa348715afb56ff2485dddc22e5445fe7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab50ff2276efffaa3f8f29be66256a806713868c8dd7b811ec5bade62d049f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d05596c4ec1f59286748ca08bb4a1e5ef56d469b575f795cfe63e5675c044d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3beef8b228930f0bce276fb23121835be0e9dbd8df0850287af603d47f3b1836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29c2f3ddeaef2d320f300c992874d8f2c8bb220f40169c3df6969d0532aafb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestUriCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestUriCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestUriCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3883da5dfa6919a2d16a922168217c11c95e6d3eee5570d501dbe4229ab6948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlFileExtensionCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnEndpointDeliveryRuleUrlFileExtensionCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703634b12940042e8c57de7eefcf646011e0df25d54d2f4d04dd733fd70a6584)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleUrlFileExtensionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleUrlFileExtensionConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlFileExtensionConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__213655506bc53f124d348b28bb6a04f24989f5d85c43721cc2af4a14fe9c70fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleUrlFileExtensionConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088a2853d5b7d035f71edfed5ba238f7619c01d4d87953ed718609758de728f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleUrlFileExtensionConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6898a8bd7ecbcbe1b154d1a168102c71fcddff41743fa0b425121ef09a17d494)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a346762dd5f5ca4e5dd8d69354a92583eec69a654afe6735362c67526b618a8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c3c2fbcc96126afa30aa3950f8cb10be59bb51d557552f61eebaf29ea6d7405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlFileExtensionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlFileExtensionCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlFileExtensionCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6c4652b6cbf92e876447d749690adb218d7e8b8f6de55f2160e4b3deb782b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleUrlFileExtensionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlFileExtensionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f75643dcab8df8ee8692210a49fc9913f21f013383d5f8cf72deefe681e36ebb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce861f661fa669e5702c3877a2470a7e62862fd92f9b858c3ded926b1b0c69dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc59cba7c78b92a56f39caba469ffafe15a5404e15a1a57d53a0a8f8d9d174ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7729fadab51c552615c7c6666aaab3c102454e1d6c21d07bb33aeb071dc213cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec7a169ff41806d1404195040d25688634a17c8b817603c62a34292c55ddaea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlFileExtensionCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlFileExtensionCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlFileExtensionCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0f9e64db2d8369fa39ba4cd0605647e27a5de24b09bfa800926d71dcea33ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlFileNameCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnEndpointDeliveryRuleUrlFileNameCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faaee70ffb1b6f95e78503936d73976f50923635a62c789e692c4c7024dc1b37)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleUrlFileNameCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleUrlFileNameConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlFileNameConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f869c658e888cc3c2e68de8db91f0a38f73fa9434a062a3ae6388a691ef09d95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleUrlFileNameConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf6143e920ae701228483dd5c9f928adf58a8508647bbe3ee8b8250a76027ae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleUrlFileNameConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e5bc3223bdacc41b5927370568140eec1385d569df551958624f08a8d08c23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa4311ed0c656b1605c7a169a26ec11584794e4b880655793d97262d7254e8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c930d68ceb31ce1a79f9e6177c3fa22033c65c16c1a352c8f370175618c9e46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlFileNameCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlFileNameCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlFileNameCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4267a289a049b3904cdd18e8bbadf9cba9d3d67dc371c8778aff9a1ab5102178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleUrlFileNameConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlFileNameConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__098a57d5d49d9b15149096dc481cb1200352363630981c5110f95fb4c79029f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19a298d25956894a30dbd7bf304ed6c5c0a6aaaf481d468114afd121e719acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8db53940e3441c141722060c39a5572bbbb99ac76cd101cf1f9f9be372e7935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9939b040ffdfd29bfe757365befed04c7a63bd0a7a3632dfda863f102b47cf87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b65d361ec9efae4c44cc39726a3219cfc34ab39eb8d946d97061f26e65d6bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlFileNameCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlFileNameCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlFileNameCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba75cb86ba2fbe0ca4e82b3cf1192445a3deaf54114c75dad8f31a17b16f8386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlPathCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnEndpointDeliveryRuleUrlPathCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7509a1d01039b8a13f3411425015bd7afc2cf9440b2913a01f2740de0b4df7b9)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#operator CdnEndpoint#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#match_values CdnEndpoint#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#negate_condition CdnEndpoint#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#transforms CdnEndpoint#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleUrlPathCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleUrlPathConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlPathConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3af1a0116e4423c73639a02717839d1ef8200d3c55e5817a87b3bfb7e1d7110b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointDeliveryRuleUrlPathConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc942175f86b258d65107da5d391dd999973ec94d51c57944bee88394e019e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointDeliveryRuleUrlPathConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45dbb9eb5a7f66e10d45466af89630260a88f42528bf5d2cce6c299d41d3f11a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c6b8214377c190155ef2fbc4902f099d48cce60588dde81b393d0c106617030)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85a44b8368eb4f8e1c1252ceaf26bad713a07a6a23e0b1ab69033fb9edf97fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlPathCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlPathCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlPathCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b05412794a9e64d0605fc41c5c2e152a9ecb676bc12e765d63a2881f9edd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointDeliveryRuleUrlPathConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlPathConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f65b3cfdfcd477aa791a51ba4c11360b5c1064fae2808d2889627e834a7fab01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchValues")
    def reset_match_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchValues", []))

    @jsii.member(jsii_name="resetNegateCondition")
    def reset_negate_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateCondition", []))

    @jsii.member(jsii_name="resetTransforms")
    def reset_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="matchValuesInput")
    def match_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="negateConditionInput")
    def negate_condition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="transformsInput")
    def transforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transformsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8def3e35df960dd3017f7b644861c3d7d0d276688fdf8d4f808af5cff42ce605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateCondition")
    def negate_condition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateCondition"))

    @negate_condition.setter
    def negate_condition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0942137d344270d04d32bae54da6171268ea434e80f0811a10ac076d91be6e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975e40fd4d4b530da1ba01d6d8dd237dd9548a5f8dea3d4ab29e498c4e17a532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0755e331cf16937f8ddf3702e330b79cb0d4d3632de74184dffb32aad82fba5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlPathCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlPathCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlPathCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bbdb8d1cbe0bae786dc7320c163098687a285c9b6e76d986f62bbdf2991da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlRedirectAction",
    jsii_struct_bases=[],
    name_mapping={
        "redirect_type": "redirectType",
        "fragment": "fragment",
        "hostname": "hostname",
        "path": "path",
        "protocol": "protocol",
        "query_string": "queryString",
    },
)
class CdnEndpointDeliveryRuleUrlRedirectAction:
    def __init__(
        self,
        *,
        redirect_type: builtins.str,
        fragment: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param redirect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#redirect_type CdnEndpoint#redirect_type}.
        :param fragment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#fragment CdnEndpoint#fragment}.
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#hostname CdnEndpoint#hostname}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#path CdnEndpoint#path}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#protocol CdnEndpoint#protocol}.
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#query_string CdnEndpoint#query_string}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a744d7a12d76e6bc98858ac792617004f8b93ff01c6b01ef381bf0d1187fd1)
            check_type(argname="argument redirect_type", value=redirect_type, expected_type=type_hints["redirect_type"])
            check_type(argname="argument fragment", value=fragment, expected_type=type_hints["fragment"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "redirect_type": redirect_type,
        }
        if fragment is not None:
            self._values["fragment"] = fragment
        if hostname is not None:
            self._values["hostname"] = hostname
        if path is not None:
            self._values["path"] = path
        if protocol is not None:
            self._values["protocol"] = protocol
        if query_string is not None:
            self._values["query_string"] = query_string

    @builtins.property
    def redirect_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#redirect_type CdnEndpoint#redirect_type}.'''
        result = self._values.get("redirect_type")
        assert result is not None, "Required property 'redirect_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fragment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#fragment CdnEndpoint#fragment}.'''
        result = self._values.get("fragment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#hostname CdnEndpoint#hostname}.'''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#path CdnEndpoint#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#protocol CdnEndpoint#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#query_string CdnEndpoint#query_string}.'''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleUrlRedirectAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleUrlRedirectActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlRedirectActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d053cc446821472782e0facd81431484bac65048ba9c7adfb9a17d1ceac1e9a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFragment")
    def reset_fragment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFragment", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetQueryString")
    def reset_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryString", []))

    @builtins.property
    @jsii.member(jsii_name="fragmentInput")
    def fragment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fragmentInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectTypeInput")
    def redirect_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="fragment")
    def fragment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fragment"))

    @fragment.setter
    def fragment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11cf6240ead0845c2ce7efd32082d32806589e1eb3c09548cc5aa6a5aaec9c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fragment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b05d50e373e46cbfb41d00048293785cee3e55c59367d3baf601f4516fd2d08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2733cf7e5b6f13f38d2471d9ff7c5c7ad0f8c51e324c46e616f2f9311899eb55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4437102054b66f5f48b6e8e6d395cc520bb8eb40a327c3c67e52742a8b1d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0835c3ed96d70bb0bde4125ff0ff2490aceabd3c99d1c92e2645971623e3a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectType")
    def redirect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectType"))

    @redirect_type.setter
    def redirect_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77919cc814073d38eeddc0057e4fdc795adbfdcbd6603de6a9961796bbd3652c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointDeliveryRuleUrlRedirectAction]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleUrlRedirectAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointDeliveryRuleUrlRedirectAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e238c491e766f69d6f192803ef654cae0c0a4f268b00265dc110acc8fbd666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlRewriteAction",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "source_pattern": "sourcePattern",
        "preserve_unmatched_path": "preserveUnmatchedPath",
    },
)
class CdnEndpointDeliveryRuleUrlRewriteAction:
    def __init__(
        self,
        *,
        destination: builtins.str,
        source_pattern: builtins.str,
        preserve_unmatched_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#destination CdnEndpoint#destination}.
        :param source_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#source_pattern CdnEndpoint#source_pattern}.
        :param preserve_unmatched_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#preserve_unmatched_path CdnEndpoint#preserve_unmatched_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9f64919e97d1884529a47a04f6aed55d24396c6c0053adabb72c7b2cc16fe4)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument source_pattern", value=source_pattern, expected_type=type_hints["source_pattern"])
            check_type(argname="argument preserve_unmatched_path", value=preserve_unmatched_path, expected_type=type_hints["preserve_unmatched_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "source_pattern": source_pattern,
        }
        if preserve_unmatched_path is not None:
            self._values["preserve_unmatched_path"] = preserve_unmatched_path

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#destination CdnEndpoint#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#source_pattern CdnEndpoint#source_pattern}.'''
        result = self._values.get("source_pattern")
        assert result is not None, "Required property 'source_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preserve_unmatched_path(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#preserve_unmatched_path CdnEndpoint#preserve_unmatched_path}.'''
        result = self._values.get("preserve_unmatched_path")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointDeliveryRuleUrlRewriteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointDeliveryRuleUrlRewriteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointDeliveryRuleUrlRewriteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__510ce431ce7d88aab45fd466346a19f622eb9d9309f90e3d3c088177b147c623)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPreserveUnmatchedPath")
    def reset_preserve_unmatched_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveUnmatchedPath", []))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveUnmatchedPathInput")
    def preserve_unmatched_path_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveUnmatchedPathInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePatternInput")
    def source_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourcePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c08c4a543ed8077ef1601c9f0ae4dd07ca6e71e65d45ea785b7f7e9434ae40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preserveUnmatchedPath")
    def preserve_unmatched_path(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveUnmatchedPath"))

    @preserve_unmatched_path.setter
    def preserve_unmatched_path(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ff673c306d564f34d3ebde364921778e3b636fef38e34518f2203b98c84683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveUnmatchedPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePattern")
    def source_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcePattern"))

    @source_pattern.setter
    def source_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8645fa3bf15cbcaeeb9b811ff31743d2f6d13d3bf2e5c3ff3ba5040fcbcdafef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointDeliveryRuleUrlRewriteAction]:
        return typing.cast(typing.Optional[CdnEndpointDeliveryRuleUrlRewriteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointDeliveryRuleUrlRewriteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0c9d0d59b76cc87a2dac736086afe77f7f12f7586f371a2d5f907fd8076e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGeoFilter",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "country_codes": "countryCodes",
        "relative_path": "relativePath",
    },
)
class CdnEndpointGeoFilter:
    def __init__(
        self,
        *,
        action: builtins.str,
        country_codes: typing.Sequence[builtins.str],
        relative_path: builtins.str,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.
        :param country_codes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#country_codes CdnEndpoint#country_codes}.
        :param relative_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#relative_path CdnEndpoint#relative_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835122195e697e8caf7643c81deb8d14372657458cf463f5bfcc3ec35f7495e3)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument country_codes", value=country_codes, expected_type=type_hints["country_codes"])
            check_type(argname="argument relative_path", value=relative_path, expected_type=type_hints["relative_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "country_codes": country_codes,
            "relative_path": relative_path,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def country_codes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#country_codes CdnEndpoint#country_codes}.'''
        result = self._values.get("country_codes")
        assert result is not None, "Required property 'country_codes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def relative_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#relative_path CdnEndpoint#relative_path}.'''
        result = self._values.get("relative_path")
        assert result is not None, "Required property 'relative_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointGeoFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointGeoFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGeoFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10b11f551e1011d84d4f48d5199b2de033119fb952e8afeba75ca7388e1f1750)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CdnEndpointGeoFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fa5965613683eedd71142c4cdd1de20aa246d5542f3c767dbca47a1002e554)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointGeoFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c14cceec828fd4201abdf0a75e2742e213b4a4bfcdf38e580227318537f5ea8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d120b7b14abb8ae4ddb332196186af8bbf32470c5c98290f8851fa45c9b65d1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c480800085be276d8723046e54922e074205c7a2f48fb50e3e4a188bacc357c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGeoFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGeoFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGeoFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b256cb3b672aa1b166b4eaaa1e4c4ab7290f4d2fd9e90f3d88e2577e05148e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointGeoFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGeoFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d938799433166b985efa8699691c53177d8af68cb89c240b3e36385f24657539)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCodesInput")
    def country_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "countryCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="relativePathInput")
    def relative_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relativePathInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281bd2def29809b77b4bfec438ccc8797cdd2ad04971793d5eee2ac585b56e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCodes")
    def country_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "countryCodes"))

    @country_codes.setter
    def country_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72018966008ac2e50389fe719e9d7f4e1010cabe34ccbe2e6f8efabc99d45566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativePath")
    def relative_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relativePath"))

    @relative_path.setter
    def relative_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a1c704b5d6ad69413d04505da818e5a35ced36e849c2bdd15539b25acfef38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGeoFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGeoFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGeoFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdebf0471d3cb1531e2514fa2a1f9a5613e1befcefe3375db1ddedce0d2aaa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRule",
    jsii_struct_bases=[],
    name_mapping={
        "cache_expiration_action": "cacheExpirationAction",
        "cache_key_query_string_action": "cacheKeyQueryStringAction",
        "modify_request_header_action": "modifyRequestHeaderAction",
        "modify_response_header_action": "modifyResponseHeaderAction",
        "url_redirect_action": "urlRedirectAction",
        "url_rewrite_action": "urlRewriteAction",
    },
)
class CdnEndpointGlobalDeliveryRule:
    def __init__(
        self,
        *,
        cache_expiration_action: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRuleCacheExpirationAction", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_key_query_string_action: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction", typing.Dict[builtins.str, typing.Any]]] = None,
        modify_request_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        modify_response_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_redirect_action: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRuleUrlRedirectAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite_action: typing.Optional[typing.Union["CdnEndpointGlobalDeliveryRuleUrlRewriteAction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cache_expiration_action: cache_expiration_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_expiration_action CdnEndpoint#cache_expiration_action}
        :param cache_key_query_string_action: cache_key_query_string_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_key_query_string_action CdnEndpoint#cache_key_query_string_action}
        :param modify_request_header_action: modify_request_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_request_header_action CdnEndpoint#modify_request_header_action}
        :param modify_response_header_action: modify_response_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_response_header_action CdnEndpoint#modify_response_header_action}
        :param url_redirect_action: url_redirect_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_redirect_action CdnEndpoint#url_redirect_action}
        :param url_rewrite_action: url_rewrite_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_rewrite_action CdnEndpoint#url_rewrite_action}
        '''
        if isinstance(cache_expiration_action, dict):
            cache_expiration_action = CdnEndpointGlobalDeliveryRuleCacheExpirationAction(**cache_expiration_action)
        if isinstance(cache_key_query_string_action, dict):
            cache_key_query_string_action = CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction(**cache_key_query_string_action)
        if isinstance(url_redirect_action, dict):
            url_redirect_action = CdnEndpointGlobalDeliveryRuleUrlRedirectAction(**url_redirect_action)
        if isinstance(url_rewrite_action, dict):
            url_rewrite_action = CdnEndpointGlobalDeliveryRuleUrlRewriteAction(**url_rewrite_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55057b4639eea2d0764e80191a38de934c342c9b002460ee58aab4b822118b90)
            check_type(argname="argument cache_expiration_action", value=cache_expiration_action, expected_type=type_hints["cache_expiration_action"])
            check_type(argname="argument cache_key_query_string_action", value=cache_key_query_string_action, expected_type=type_hints["cache_key_query_string_action"])
            check_type(argname="argument modify_request_header_action", value=modify_request_header_action, expected_type=type_hints["modify_request_header_action"])
            check_type(argname="argument modify_response_header_action", value=modify_response_header_action, expected_type=type_hints["modify_response_header_action"])
            check_type(argname="argument url_redirect_action", value=url_redirect_action, expected_type=type_hints["url_redirect_action"])
            check_type(argname="argument url_rewrite_action", value=url_rewrite_action, expected_type=type_hints["url_rewrite_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_expiration_action is not None:
            self._values["cache_expiration_action"] = cache_expiration_action
        if cache_key_query_string_action is not None:
            self._values["cache_key_query_string_action"] = cache_key_query_string_action
        if modify_request_header_action is not None:
            self._values["modify_request_header_action"] = modify_request_header_action
        if modify_response_header_action is not None:
            self._values["modify_response_header_action"] = modify_response_header_action
        if url_redirect_action is not None:
            self._values["url_redirect_action"] = url_redirect_action
        if url_rewrite_action is not None:
            self._values["url_rewrite_action"] = url_rewrite_action

    @builtins.property
    def cache_expiration_action(
        self,
    ) -> typing.Optional["CdnEndpointGlobalDeliveryRuleCacheExpirationAction"]:
        '''cache_expiration_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_expiration_action CdnEndpoint#cache_expiration_action}
        '''
        result = self._values.get("cache_expiration_action")
        return typing.cast(typing.Optional["CdnEndpointGlobalDeliveryRuleCacheExpirationAction"], result)

    @builtins.property
    def cache_key_query_string_action(
        self,
    ) -> typing.Optional["CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction"]:
        '''cache_key_query_string_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#cache_key_query_string_action CdnEndpoint#cache_key_query_string_action}
        '''
        result = self._values.get("cache_key_query_string_action")
        return typing.cast(typing.Optional["CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction"], result)

    @builtins.property
    def modify_request_header_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction"]]]:
        '''modify_request_header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_request_header_action CdnEndpoint#modify_request_header_action}
        '''
        result = self._values.get("modify_request_header_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction"]]], result)

    @builtins.property
    def modify_response_header_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction"]]]:
        '''modify_response_header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#modify_response_header_action CdnEndpoint#modify_response_header_action}
        '''
        result = self._values.get("modify_response_header_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction"]]], result)

    @builtins.property
    def url_redirect_action(
        self,
    ) -> typing.Optional["CdnEndpointGlobalDeliveryRuleUrlRedirectAction"]:
        '''url_redirect_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_redirect_action CdnEndpoint#url_redirect_action}
        '''
        result = self._values.get("url_redirect_action")
        return typing.cast(typing.Optional["CdnEndpointGlobalDeliveryRuleUrlRedirectAction"], result)

    @builtins.property
    def url_rewrite_action(
        self,
    ) -> typing.Optional["CdnEndpointGlobalDeliveryRuleUrlRewriteAction"]:
        '''url_rewrite_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#url_rewrite_action CdnEndpoint#url_rewrite_action}
        '''
        result = self._values.get("url_rewrite_action")
        return typing.cast(typing.Optional["CdnEndpointGlobalDeliveryRuleUrlRewriteAction"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointGlobalDeliveryRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleCacheExpirationAction",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior", "duration": "duration"},
)
class CdnEndpointGlobalDeliveryRuleCacheExpirationAction:
    def __init__(
        self,
        *,
        behavior: builtins.str,
        duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#duration CdnEndpoint#duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad8609cc1c491888a7bce9e7f842bbe358d78b910956c8ddee0ae1b25e7b9df)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
        }
        if duration is not None:
            self._values["duration"] = duration

    @builtins.property
    def behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.'''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#duration CdnEndpoint#duration}.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointGlobalDeliveryRuleCacheExpirationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointGlobalDeliveryRuleCacheExpirationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleCacheExpirationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be1b34cb0956d407873ab643d6fd46a88a47e91cd5617df93b5ce0b0a87eea94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ccbd3d94d5e8b35ce0badeff82ea148f52cca6db341510253d6c78caa1cd521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb10f3bcdd8f399b3937d2de5ad0a6bfa505f0f408eacaa4b2a93b3ef0583f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointGlobalDeliveryRuleCacheExpirationAction]:
        return typing.cast(typing.Optional[CdnEndpointGlobalDeliveryRuleCacheExpirationAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointGlobalDeliveryRuleCacheExpirationAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5d5ffdf77725644396954959232ee38adc33945c7f6158f2b10ba1323ab27f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior", "parameters": "parameters"},
)
class CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction:
    def __init__(
        self,
        *,
        behavior: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#parameters CdnEndpoint#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09293d84162fabad8033c719dd977bdd0ec690421959e98ba209c8f88d34e60e)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.'''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#parameters CdnEndpoint#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e563768fcd953c2b34dfc56d9ccefb9b6c94e91dd7409201b537336b91f554d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50725fd0740074008537c19912ab749912ec604cc8ddea8e1c8766791dce213b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58f5491baf76bded28b9e9d906ca4a9b6d4408ffa19d58aa81247ebb11109ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction]:
        return typing.cast(typing.Optional[CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93b94db4f26ab129fc3382adbeb1dc9a8e4632a78667afaec1d93c304cbb051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name", "value": "value"},
)
class CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction:
    def __init__(
        self,
        *,
        action: builtins.str,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#value CdnEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0ccc682a89ad629523bbadca36d1969792653eb9f86757575e610d4316432a)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#value CdnEndpoint#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3a1bedae1c809f7c0a280e436f00a1302bbcf9ebd64559966e7f144332b9061)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea33517b3fb783f8f0029809dbd7a1726c983a010f6231a4fb5d327ecff8f1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428e2c6717b20b85531d74c10432f8a7f1f9286e301f818895d134d363053ec1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4f0cb1ca4c3a279e5c627421d019e5eb9370dae54d09d0874abb7efdb50d19b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12525bf4288194ba240dda229278a1d0d45a071637b849ac495dcf0069ddf795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63ae7e19b6ecd369734e520e43822cf6c38c60c59d68e0112baefd2cdbcd769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abbd43188c09520fd703786e649bb89b1a500ead11aa07bd5e1eca806eebc325)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c75ea75effed7fefda1adfc9d463e6afd567e7a4cca62c502730bb7979156c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552fb8dca8c051799aca78fca8dbbf1c393280c4e48c78c816d7b6f7c3e95877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0248c234344d9fb24d421c65e9472d231433a9177254a4fc99ff4254240dc80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9574a7f7178f267d25b158d9b5311b392b590e31c2fb174029f8a0647907b272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name", "value": "value"},
)
class CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction:
    def __init__(
        self,
        *,
        action: builtins.str,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#value CdnEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43215636beb1a77449a41e4f012eaf4b5c20108806a362c0bd114cc6879e6ba0)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#action CdnEndpoint#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#value CdnEndpoint#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92f89bf80227577f22a96cf62b6d93cd308383ce2a3cb090a0aaf4675e74dcba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611de4791828c918a0219d34ee9d439aab1f3ac90f7716297c7f7c354898c346)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ec607f9197a4601a2a2a43e848072839f96021ee7b1d7ba46fb57843ae7b55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__886bddf2094f35a081dc994d709090a301cda913e5e067a4eded91ddb109f332)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8fa730100159455612679da4fd91cc01735c0b468f81e9e9a464aede17572b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b005ac6040c931d59750fa6dca3640b05c497bce8491149991cfd70ed4961384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fd1a3264a506a2c8e299e60968e3e704d322dd5841e20a523384aceab2f6a9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab094bb585bd865530f663ae4b6935674ad62516d60a6e8acf2953566a5be25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a126dc38251876d788c5a00086ddf0656ad5cab8377397c933d64189985292fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df31b36fd67149725c21655a39a9edbb22613bd5f65bae00d669c0741e091523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0a116aa07aca8c89ecc7f6b6893bbdf5c4d4486dbdd9cb95021f0aa94c1411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointGlobalDeliveryRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b40f283fa4e1bc51a7a827d1f73a4e51c4af2133063d9a06f4c4a19511e19a90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCacheExpirationAction")
    def put_cache_expiration_action(
        self,
        *,
        behavior: builtins.str,
        duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#duration CdnEndpoint#duration}.
        '''
        value = CdnEndpointGlobalDeliveryRuleCacheExpirationAction(
            behavior=behavior, duration=duration
        )

        return typing.cast(None, jsii.invoke(self, "putCacheExpirationAction", [value]))

    @jsii.member(jsii_name="putCacheKeyQueryStringAction")
    def put_cache_key_query_string_action(
        self,
        *,
        behavior: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#behavior CdnEndpoint#behavior}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#parameters CdnEndpoint#parameters}.
        '''
        value = CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction(
            behavior=behavior, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putCacheKeyQueryStringAction", [value]))

    @jsii.member(jsii_name="putModifyRequestHeaderAction")
    def put_modify_request_header_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9365c561dac0fc3ffd4e816a7f525d03bc72083fc3e8ece2e72cfdcff9d383fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putModifyRequestHeaderAction", [value]))

    @jsii.member(jsii_name="putModifyResponseHeaderAction")
    def put_modify_response_header_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b28736669370383edb4f5ec8f33b88d84593ebd1e6eb7d0cc3768f8b12ff2a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putModifyResponseHeaderAction", [value]))

    @jsii.member(jsii_name="putUrlRedirectAction")
    def put_url_redirect_action(
        self,
        *,
        redirect_type: builtins.str,
        fragment: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param redirect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#redirect_type CdnEndpoint#redirect_type}.
        :param fragment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#fragment CdnEndpoint#fragment}.
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#hostname CdnEndpoint#hostname}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#path CdnEndpoint#path}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#protocol CdnEndpoint#protocol}.
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#query_string CdnEndpoint#query_string}.
        '''
        value = CdnEndpointGlobalDeliveryRuleUrlRedirectAction(
            redirect_type=redirect_type,
            fragment=fragment,
            hostname=hostname,
            path=path,
            protocol=protocol,
            query_string=query_string,
        )

        return typing.cast(None, jsii.invoke(self, "putUrlRedirectAction", [value]))

    @jsii.member(jsii_name="putUrlRewriteAction")
    def put_url_rewrite_action(
        self,
        *,
        destination: builtins.str,
        source_pattern: builtins.str,
        preserve_unmatched_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#destination CdnEndpoint#destination}.
        :param source_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#source_pattern CdnEndpoint#source_pattern}.
        :param preserve_unmatched_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#preserve_unmatched_path CdnEndpoint#preserve_unmatched_path}.
        '''
        value = CdnEndpointGlobalDeliveryRuleUrlRewriteAction(
            destination=destination,
            source_pattern=source_pattern,
            preserve_unmatched_path=preserve_unmatched_path,
        )

        return typing.cast(None, jsii.invoke(self, "putUrlRewriteAction", [value]))

    @jsii.member(jsii_name="resetCacheExpirationAction")
    def reset_cache_expiration_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheExpirationAction", []))

    @jsii.member(jsii_name="resetCacheKeyQueryStringAction")
    def reset_cache_key_query_string_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheKeyQueryStringAction", []))

    @jsii.member(jsii_name="resetModifyRequestHeaderAction")
    def reset_modify_request_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModifyRequestHeaderAction", []))

    @jsii.member(jsii_name="resetModifyResponseHeaderAction")
    def reset_modify_response_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModifyResponseHeaderAction", []))

    @jsii.member(jsii_name="resetUrlRedirectAction")
    def reset_url_redirect_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRedirectAction", []))

    @jsii.member(jsii_name="resetUrlRewriteAction")
    def reset_url_rewrite_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRewriteAction", []))

    @builtins.property
    @jsii.member(jsii_name="cacheExpirationAction")
    def cache_expiration_action(
        self,
    ) -> CdnEndpointGlobalDeliveryRuleCacheExpirationActionOutputReference:
        return typing.cast(CdnEndpointGlobalDeliveryRuleCacheExpirationActionOutputReference, jsii.get(self, "cacheExpirationAction"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyQueryStringAction")
    def cache_key_query_string_action(
        self,
    ) -> CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringActionOutputReference:
        return typing.cast(CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringActionOutputReference, jsii.get(self, "cacheKeyQueryStringAction"))

    @builtins.property
    @jsii.member(jsii_name="modifyRequestHeaderAction")
    def modify_request_header_action(
        self,
    ) -> CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionList:
        return typing.cast(CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionList, jsii.get(self, "modifyRequestHeaderAction"))

    @builtins.property
    @jsii.member(jsii_name="modifyResponseHeaderAction")
    def modify_response_header_action(
        self,
    ) -> CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionList:
        return typing.cast(CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionList, jsii.get(self, "modifyResponseHeaderAction"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirectAction")
    def url_redirect_action(
        self,
    ) -> "CdnEndpointGlobalDeliveryRuleUrlRedirectActionOutputReference":
        return typing.cast("CdnEndpointGlobalDeliveryRuleUrlRedirectActionOutputReference", jsii.get(self, "urlRedirectAction"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteAction")
    def url_rewrite_action(
        self,
    ) -> "CdnEndpointGlobalDeliveryRuleUrlRewriteActionOutputReference":
        return typing.cast("CdnEndpointGlobalDeliveryRuleUrlRewriteActionOutputReference", jsii.get(self, "urlRewriteAction"))

    @builtins.property
    @jsii.member(jsii_name="cacheExpirationActionInput")
    def cache_expiration_action_input(
        self,
    ) -> typing.Optional[CdnEndpointGlobalDeliveryRuleCacheExpirationAction]:
        return typing.cast(typing.Optional[CdnEndpointGlobalDeliveryRuleCacheExpirationAction], jsii.get(self, "cacheExpirationActionInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyQueryStringActionInput")
    def cache_key_query_string_action_input(
        self,
    ) -> typing.Optional[CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction]:
        return typing.cast(typing.Optional[CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction], jsii.get(self, "cacheKeyQueryStringActionInput"))

    @builtins.property
    @jsii.member(jsii_name="modifyRequestHeaderActionInput")
    def modify_request_header_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]]], jsii.get(self, "modifyRequestHeaderActionInput"))

    @builtins.property
    @jsii.member(jsii_name="modifyResponseHeaderActionInput")
    def modify_response_header_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]]], jsii.get(self, "modifyResponseHeaderActionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirectActionInput")
    def url_redirect_action_input(
        self,
    ) -> typing.Optional["CdnEndpointGlobalDeliveryRuleUrlRedirectAction"]:
        return typing.cast(typing.Optional["CdnEndpointGlobalDeliveryRuleUrlRedirectAction"], jsii.get(self, "urlRedirectActionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteActionInput")
    def url_rewrite_action_input(
        self,
    ) -> typing.Optional["CdnEndpointGlobalDeliveryRuleUrlRewriteAction"]:
        return typing.cast(typing.Optional["CdnEndpointGlobalDeliveryRuleUrlRewriteAction"], jsii.get(self, "urlRewriteActionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CdnEndpointGlobalDeliveryRule]:
        return typing.cast(typing.Optional[CdnEndpointGlobalDeliveryRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointGlobalDeliveryRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbeec77ac4d0a796ecdc79e7002e6d4c1e6cbd560630a82e77625c8e87955da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleUrlRedirectAction",
    jsii_struct_bases=[],
    name_mapping={
        "redirect_type": "redirectType",
        "fragment": "fragment",
        "hostname": "hostname",
        "path": "path",
        "protocol": "protocol",
        "query_string": "queryString",
    },
)
class CdnEndpointGlobalDeliveryRuleUrlRedirectAction:
    def __init__(
        self,
        *,
        redirect_type: builtins.str,
        fragment: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param redirect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#redirect_type CdnEndpoint#redirect_type}.
        :param fragment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#fragment CdnEndpoint#fragment}.
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#hostname CdnEndpoint#hostname}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#path CdnEndpoint#path}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#protocol CdnEndpoint#protocol}.
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#query_string CdnEndpoint#query_string}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266be95137650349fc0fba1620d556d515a51a3997877181d1597fd6faf3da8f)
            check_type(argname="argument redirect_type", value=redirect_type, expected_type=type_hints["redirect_type"])
            check_type(argname="argument fragment", value=fragment, expected_type=type_hints["fragment"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "redirect_type": redirect_type,
        }
        if fragment is not None:
            self._values["fragment"] = fragment
        if hostname is not None:
            self._values["hostname"] = hostname
        if path is not None:
            self._values["path"] = path
        if protocol is not None:
            self._values["protocol"] = protocol
        if query_string is not None:
            self._values["query_string"] = query_string

    @builtins.property
    def redirect_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#redirect_type CdnEndpoint#redirect_type}.'''
        result = self._values.get("redirect_type")
        assert result is not None, "Required property 'redirect_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fragment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#fragment CdnEndpoint#fragment}.'''
        result = self._values.get("fragment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#hostname CdnEndpoint#hostname}.'''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#path CdnEndpoint#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#protocol CdnEndpoint#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#query_string CdnEndpoint#query_string}.'''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointGlobalDeliveryRuleUrlRedirectAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointGlobalDeliveryRuleUrlRedirectActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleUrlRedirectActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bd3ad04a01cc6439e382e513f6547806516a41e6010a535ff0ee2189e4fe0bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFragment")
    def reset_fragment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFragment", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetQueryString")
    def reset_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryString", []))

    @builtins.property
    @jsii.member(jsii_name="fragmentInput")
    def fragment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fragmentInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectTypeInput")
    def redirect_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="fragment")
    def fragment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fragment"))

    @fragment.setter
    def fragment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5cd50735f24f419297d23a05bc73c6324c31ab8256a1d02608930af204531b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fragment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5310d9c8e901c564331d7606e70d6f669975ad6140f52e0f3bf6845019cb8023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a66cb687d22f05b891bab107e9251300ce543dc8933b673a484827d93b17ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f296bd81ff32ebd752cd9d0ed4b42a7906740bcb7362f9bad6e5151dff8904f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b6ea122a1d260173fe50427625ca2e4d4c4abe1bbace2bc7e0b245e5ae41d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectType")
    def redirect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectType"))

    @redirect_type.setter
    def redirect_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e07260e97a24d54ab3f24d447ded4dbb4658663e5441cb7996f17f6d9c7aee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointGlobalDeliveryRuleUrlRedirectAction]:
        return typing.cast(typing.Optional[CdnEndpointGlobalDeliveryRuleUrlRedirectAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointGlobalDeliveryRuleUrlRedirectAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5704eee50bd362b39954a1628501d60cad117e896e3fc6a9c40e4326f16fea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleUrlRewriteAction",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "source_pattern": "sourcePattern",
        "preserve_unmatched_path": "preserveUnmatchedPath",
    },
)
class CdnEndpointGlobalDeliveryRuleUrlRewriteAction:
    def __init__(
        self,
        *,
        destination: builtins.str,
        source_pattern: builtins.str,
        preserve_unmatched_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#destination CdnEndpoint#destination}.
        :param source_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#source_pattern CdnEndpoint#source_pattern}.
        :param preserve_unmatched_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#preserve_unmatched_path CdnEndpoint#preserve_unmatched_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67829debe997502b2cfe991a043b0d92078543a059910f0d52108588915482f6)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument source_pattern", value=source_pattern, expected_type=type_hints["source_pattern"])
            check_type(argname="argument preserve_unmatched_path", value=preserve_unmatched_path, expected_type=type_hints["preserve_unmatched_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "source_pattern": source_pattern,
        }
        if preserve_unmatched_path is not None:
            self._values["preserve_unmatched_path"] = preserve_unmatched_path

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#destination CdnEndpoint#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#source_pattern CdnEndpoint#source_pattern}.'''
        result = self._values.get("source_pattern")
        assert result is not None, "Required property 'source_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preserve_unmatched_path(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#preserve_unmatched_path CdnEndpoint#preserve_unmatched_path}.'''
        result = self._values.get("preserve_unmatched_path")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointGlobalDeliveryRuleUrlRewriteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointGlobalDeliveryRuleUrlRewriteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointGlobalDeliveryRuleUrlRewriteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8d9b58b048280983c5c6e66c21567b48387a80763c2655dbeb286957b4572a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPreserveUnmatchedPath")
    def reset_preserve_unmatched_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveUnmatchedPath", []))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveUnmatchedPathInput")
    def preserve_unmatched_path_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveUnmatchedPathInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePatternInput")
    def source_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourcePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50cea72ef6acae6aa7368e4dcfd35a7292ee300de26d1f9faa4267f7fabbe6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preserveUnmatchedPath")
    def preserve_unmatched_path(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveUnmatchedPath"))

    @preserve_unmatched_path.setter
    def preserve_unmatched_path(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c27e1dc36ecdc5bb4bf44039724182d106c196391a21c024e66b98a91c72f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveUnmatchedPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePattern")
    def source_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcePattern"))

    @source_pattern.setter
    def source_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22278ae8eb5791eb9182ba13dbca7688a7ef22f863fca48d49fa19e46483e1fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnEndpointGlobalDeliveryRuleUrlRewriteAction]:
        return typing.cast(typing.Optional[CdnEndpointGlobalDeliveryRuleUrlRewriteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnEndpointGlobalDeliveryRuleUrlRewriteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aaa799c9891291c8cda24adf210bb7fb46622976be86556bf33ff355d49a60c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointOrigin",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "name": "name",
        "http_port": "httpPort",
        "https_port": "httpsPort",
    },
)
class CdnEndpointOrigin:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        name: builtins.str,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#host_name CdnEndpoint#host_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.
        :param http_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#http_port CdnEndpoint#http_port}.
        :param https_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#https_port CdnEndpoint#https_port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4b1c0dbdcee7a2b737569e0828916451459f0c3267780c6eb527073cf1d468)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument http_port", value=http_port, expected_type=type_hints["http_port"])
            check_type(argname="argument https_port", value=https_port, expected_type=type_hints["https_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
            "name": name,
        }
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#host_name CdnEndpoint#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#name CdnEndpoint#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#http_port CdnEndpoint#http_port}.'''
        result = self._values.get("http_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#https_port CdnEndpoint#https_port}.'''
        result = self._values.get("https_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointOrigin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointOriginList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointOriginList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15e14e661de661804f3ea7989c88e7afadb380655450996bda08c59f6a33e7db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CdnEndpointOriginOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f7bff08bf41feae46deda8535e8fe26cdb7b43cee107a02f9f421bee7217f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnEndpointOriginOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e610a35de73ca1ae2efb15bf159e5dd17e6c949bfdc7e3bb7c7cb4305ef5425e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16397b0713829163408a4ac63a92b46ad0fe64a9183ac726736bc8c1d52adcda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b31e5d9bf832915a68ec309d63f57667138fb858bd1527c136b458324fe197b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointOrigin]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointOrigin]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointOrigin]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ca7d8db7e1e58b9223c50b97fb7eac0146d29abeb47f0c9baff3ca3b366ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnEndpointOriginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointOriginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5fca5d9197567f011280889133972e663f6529e2c05112dbd59e8c7812d8338)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHttpPort")
    def reset_http_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpPort", []))

    @jsii.member(jsii_name="resetHttpsPort")
    def reset_https_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsPort", []))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="httpPortInput")
    def http_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpPortInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsPortInput")
    def https_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpsPortInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727035bf6d8721a0c467a3dd7a816012dd6fcbca11929aa1ed8ff8ae4378bd90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpPort")
    def http_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpPort"))

    @http_port.setter
    def http_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfef61f3faf72ff2d5f572cb1ae3742389b4757e8dbd7ff18f937d1cdccbcfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsPort")
    def https_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpsPort"))

    @https_port.setter
    def https_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9936402f6d094daf71a486f14f8bd213e4953146551e88626851cb6cc60c2573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817ad04939d8c60f9a1bf69133f8d2e21e2d695afbadfbc154fb0a908fb68d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointOrigin]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointOrigin]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointOrigin]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102a808f51857d08491febe2ae4b22467c50d31a68ddbba98e486c805f86c8d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class CdnEndpointTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#create CdnEndpoint#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#delete CdnEndpoint#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#read CdnEndpoint#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#update CdnEndpoint#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4894374ca5afdb8aeb2b58f2af2fea8daab45ff0bbe4835f09f353aa58263de8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#create CdnEndpoint#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#delete CdnEndpoint#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#read CdnEndpoint#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_endpoint#update CdnEndpoint#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnEndpointTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnEndpointTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnEndpoint.CdnEndpointTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69360c439e86d1666428f77d416205eb7b264da3697bf5f5e7608f65185bf952)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc93b60f3bd926d5bc78f8fe3efb8c9ba03b4eadac624d76606f8b7a7e076109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300329fd613ce81794eb78f1036717a03e0ed79936bc892fce8311ce5fb0a67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883b4b898de52a133d796c3d45b3cab4d12d9d89c612e3d7fdbc8d580b519069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ccc03df3718f5db3bfd08741ee9cb1a075705bc66e42b58d507761d142e885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1a3d6fc86a503892214757e93529f4ac2f209b95599fc1395116fb2e0a728c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CdnEndpoint",
    "CdnEndpointConfig",
    "CdnEndpointDeliveryRule",
    "CdnEndpointDeliveryRuleCacheExpirationAction",
    "CdnEndpointDeliveryRuleCacheExpirationActionOutputReference",
    "CdnEndpointDeliveryRuleCacheKeyQueryStringAction",
    "CdnEndpointDeliveryRuleCacheKeyQueryStringActionOutputReference",
    "CdnEndpointDeliveryRuleCookiesCondition",
    "CdnEndpointDeliveryRuleCookiesConditionList",
    "CdnEndpointDeliveryRuleCookiesConditionOutputReference",
    "CdnEndpointDeliveryRuleDeviceCondition",
    "CdnEndpointDeliveryRuleDeviceConditionOutputReference",
    "CdnEndpointDeliveryRuleHttpVersionCondition",
    "CdnEndpointDeliveryRuleHttpVersionConditionList",
    "CdnEndpointDeliveryRuleHttpVersionConditionOutputReference",
    "CdnEndpointDeliveryRuleList",
    "CdnEndpointDeliveryRuleModifyRequestHeaderAction",
    "CdnEndpointDeliveryRuleModifyRequestHeaderActionList",
    "CdnEndpointDeliveryRuleModifyRequestHeaderActionOutputReference",
    "CdnEndpointDeliveryRuleModifyResponseHeaderAction",
    "CdnEndpointDeliveryRuleModifyResponseHeaderActionList",
    "CdnEndpointDeliveryRuleModifyResponseHeaderActionOutputReference",
    "CdnEndpointDeliveryRuleOutputReference",
    "CdnEndpointDeliveryRulePostArgCondition",
    "CdnEndpointDeliveryRulePostArgConditionList",
    "CdnEndpointDeliveryRulePostArgConditionOutputReference",
    "CdnEndpointDeliveryRuleQueryStringCondition",
    "CdnEndpointDeliveryRuleQueryStringConditionList",
    "CdnEndpointDeliveryRuleQueryStringConditionOutputReference",
    "CdnEndpointDeliveryRuleRemoteAddressCondition",
    "CdnEndpointDeliveryRuleRemoteAddressConditionList",
    "CdnEndpointDeliveryRuleRemoteAddressConditionOutputReference",
    "CdnEndpointDeliveryRuleRequestBodyCondition",
    "CdnEndpointDeliveryRuleRequestBodyConditionList",
    "CdnEndpointDeliveryRuleRequestBodyConditionOutputReference",
    "CdnEndpointDeliveryRuleRequestHeaderCondition",
    "CdnEndpointDeliveryRuleRequestHeaderConditionList",
    "CdnEndpointDeliveryRuleRequestHeaderConditionOutputReference",
    "CdnEndpointDeliveryRuleRequestMethodCondition",
    "CdnEndpointDeliveryRuleRequestMethodConditionOutputReference",
    "CdnEndpointDeliveryRuleRequestSchemeCondition",
    "CdnEndpointDeliveryRuleRequestSchemeConditionOutputReference",
    "CdnEndpointDeliveryRuleRequestUriCondition",
    "CdnEndpointDeliveryRuleRequestUriConditionList",
    "CdnEndpointDeliveryRuleRequestUriConditionOutputReference",
    "CdnEndpointDeliveryRuleUrlFileExtensionCondition",
    "CdnEndpointDeliveryRuleUrlFileExtensionConditionList",
    "CdnEndpointDeliveryRuleUrlFileExtensionConditionOutputReference",
    "CdnEndpointDeliveryRuleUrlFileNameCondition",
    "CdnEndpointDeliveryRuleUrlFileNameConditionList",
    "CdnEndpointDeliveryRuleUrlFileNameConditionOutputReference",
    "CdnEndpointDeliveryRuleUrlPathCondition",
    "CdnEndpointDeliveryRuleUrlPathConditionList",
    "CdnEndpointDeliveryRuleUrlPathConditionOutputReference",
    "CdnEndpointDeliveryRuleUrlRedirectAction",
    "CdnEndpointDeliveryRuleUrlRedirectActionOutputReference",
    "CdnEndpointDeliveryRuleUrlRewriteAction",
    "CdnEndpointDeliveryRuleUrlRewriteActionOutputReference",
    "CdnEndpointGeoFilter",
    "CdnEndpointGeoFilterList",
    "CdnEndpointGeoFilterOutputReference",
    "CdnEndpointGlobalDeliveryRule",
    "CdnEndpointGlobalDeliveryRuleCacheExpirationAction",
    "CdnEndpointGlobalDeliveryRuleCacheExpirationActionOutputReference",
    "CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction",
    "CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringActionOutputReference",
    "CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction",
    "CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionList",
    "CdnEndpointGlobalDeliveryRuleModifyRequestHeaderActionOutputReference",
    "CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction",
    "CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionList",
    "CdnEndpointGlobalDeliveryRuleModifyResponseHeaderActionOutputReference",
    "CdnEndpointGlobalDeliveryRuleOutputReference",
    "CdnEndpointGlobalDeliveryRuleUrlRedirectAction",
    "CdnEndpointGlobalDeliveryRuleUrlRedirectActionOutputReference",
    "CdnEndpointGlobalDeliveryRuleUrlRewriteAction",
    "CdnEndpointGlobalDeliveryRuleUrlRewriteActionOutputReference",
    "CdnEndpointOrigin",
    "CdnEndpointOriginList",
    "CdnEndpointOriginOutputReference",
    "CdnEndpointTimeouts",
    "CdnEndpointTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b41c2d9eecef2adb957d716684a1e81a0f737215b6b3e8a31b2a22ab950730b7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    origin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointOrigin, typing.Dict[builtins.str, typing.Any]]]],
    profile_name: builtins.str,
    resource_group_name: builtins.str,
    content_types_to_compress: typing.Optional[typing.Sequence[builtins.str]] = None,
    delivery_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    geo_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointGeoFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    global_delivery_rule: typing.Optional[typing.Union[CdnEndpointGlobalDeliveryRule, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_http_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_https_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optimization_type: typing.Optional[builtins.str] = None,
    origin_host_header: typing.Optional[builtins.str] = None,
    origin_path: typing.Optional[builtins.str] = None,
    probe_path: typing.Optional[builtins.str] = None,
    querystring_caching_behaviour: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CdnEndpointTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7952d8d675ba5cd1abab69fe4ce83542bf60ead9a15af86c6996539b12966071(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57aec5012d6dbe5400fa4e8262b356813a21fcbed0eceaec6e9f121518ae8211(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804bc0a095d9b1aeb765b2665bf4367e610184b904098930e4bf69ab883efec3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointGeoFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8956c542b5000dc5847b7f0cc138631cc25f92cac2d9b330ed832e50d9adecc1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointOrigin, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240e0c2d7a9eda8243d3716ecba1039f6ab2e3af8b3bfc7f33c51b08e2c271b6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e348b2fa0bca891ee6165acbccafb087b2cdb5e06297dc6ec3364a1473cc096(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627aa8745ea9a7aea1241ad3762c591b3a53cfae92c866a7079eaf6fac123c57(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7737f2c8134459307ce6a83afc62674bbdb45d2bd47ce256d4fc1195db551f18(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4109f0b7c9ad24c1e7f9b22623f664b95095e3cfa4bfdbf014a11e6dfd1fd1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d32e4f6ca559e8fd4b5415a523d4e089b39e0b14d62624b47f187a12bbc445f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d530f575d0c141aeb8d1e1abe4a29ceb7ce26c22de50b756178dd99524d5172(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6de932f4e1c4dfd3f203c7d8b28200e8512c85fd9214ec914e6ef8ea7aff7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1e4670cc41fc846c6759161686f587598ae1979c38b019182f2d9d1eefdeba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d92ec09ce1dbce7d8cf1c24ad44ae4c8d9c268984c088d0cbe0523338c3fbf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e72c7b34cac83dc30cc9be0ebf2eba79d760b8b66cea3ec0696086fee1fba78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d0fabd539fa28fbbd76227329510d282242feef7e9853ca039b104fd91affd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4200cef2d16aff8c8775e52cbfa15c3555349f88505f686cb11daa853dc1d14d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e27b299c3ffa1fafcad95f6f17a2e6c48ee0745a47b9674097145fc4ba720be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd920a73169ed10c759858fad3ceb6650f47b9fa3ffde7e8aed795ed6883d066(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93648e532e4f915746f2f1e83d7ef07640d2221eb87a17b5f7a71eec21073ece(
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
    origin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointOrigin, typing.Dict[builtins.str, typing.Any]]]],
    profile_name: builtins.str,
    resource_group_name: builtins.str,
    content_types_to_compress: typing.Optional[typing.Sequence[builtins.str]] = None,
    delivery_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    geo_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointGeoFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    global_delivery_rule: typing.Optional[typing.Union[CdnEndpointGlobalDeliveryRule, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_http_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_https_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optimization_type: typing.Optional[builtins.str] = None,
    origin_host_header: typing.Optional[builtins.str] = None,
    origin_path: typing.Optional[builtins.str] = None,
    probe_path: typing.Optional[builtins.str] = None,
    querystring_caching_behaviour: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CdnEndpointTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba369dedcc5cdb7753a7d88222484c3bda996c7a9a123203eddca7a0ff83d124(
    *,
    name: builtins.str,
    order: jsii.Number,
    cache_expiration_action: typing.Optional[typing.Union[CdnEndpointDeliveryRuleCacheExpirationAction, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_key_query_string_action: typing.Optional[typing.Union[CdnEndpointDeliveryRuleCacheKeyQueryStringAction, typing.Dict[builtins.str, typing.Any]]] = None,
    cookies_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleCookiesCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    device_condition: typing.Optional[typing.Union[CdnEndpointDeliveryRuleDeviceCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    http_version_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleHttpVersionCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    modify_request_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleModifyRequestHeaderAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    modify_response_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleModifyResponseHeaderAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    post_arg_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRulePostArgCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_string_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleQueryStringCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    remote_address_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleRemoteAddressCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_body_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleRequestBodyCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleRequestHeaderCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_method_condition: typing.Optional[typing.Union[CdnEndpointDeliveryRuleRequestMethodCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    request_scheme_condition: typing.Optional[typing.Union[CdnEndpointDeliveryRuleRequestSchemeCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    request_uri_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleRequestUriCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_file_extension_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleUrlFileExtensionCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_file_name_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleUrlFileNameCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_path_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleUrlPathCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_redirect_action: typing.Optional[typing.Union[CdnEndpointDeliveryRuleUrlRedirectAction, typing.Dict[builtins.str, typing.Any]]] = None,
    url_rewrite_action: typing.Optional[typing.Union[CdnEndpointDeliveryRuleUrlRewriteAction, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bce8b7e4b2b2a7df235f531dc44a4bd89855cfdf77a5192e52430252ca67f5(
    *,
    behavior: builtins.str,
    duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb15238a79d26db31496352704c1f57470354b4128b39dfc5cc10865e408487(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcb7eb2058bb49c974ef18c02761401af0a9d0af34070ef54af86a7e80b38e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d9d443092d6f6e34434f2ac766b614c1e0739fb24118732c67e5eb5f8f5f41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2824998b31fdcddf3338f3b07fabdcda339324bfc00df1c095e83fe5c720036(
    value: typing.Optional[CdnEndpointDeliveryRuleCacheExpirationAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c025233fbe4c8d443f80fb098acaf3b827ea2e299bc917082fb8457bb0cebc8(
    *,
    behavior: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb945e8901d392f13e29b1c1849aedf61a0b9b64de6d6afc0a2a563522b63ac6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3646fc21419cb02c14cfcd6e85183723c5504713abb0ba3777f43dc002dd8a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7eb22899fa27541a3bb8ef950868121de0060c8e75a10d17a07ec625b97322(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3613bae0300f6aa2c617da8aeb37f6f979028b34c945ea4ee0e6dc979c0c1ef7(
    value: typing.Optional[CdnEndpointDeliveryRuleCacheKeyQueryStringAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf2372e11692f1e741a996622cb87f256e5242e26ace19798dd6b6164911f74(
    *,
    operator: builtins.str,
    selector: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1648fd0d60756e7750cf3e97d55e9932e026dfe3cf288e5b6357fa5ec2be02b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2ad295e8312cb413c6cb0f6c8f97af3fbf3ffd795d6bff37d90c00242517ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857a072de97f5480b7e5f2419c96b460537a4f31188436fe5e622d33952eb641(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfdb0d1c8646edcdf93a254e7e89648ab787560526937711f35ba4bbd2b4a9a6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb18387a724256475893f6bb513ddb4b6d981deca3da698ef0cb27385ea7a2e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0eca0a9addce5aa31cfa2dbc421b1e2d031c3380ed4f991333d50216d8cf944(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleCookiesCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d94672315bee5ed55b92c142c25efa1830f65c1b1929da334ba7510a2b4e028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac07b0eeb930c4f9b5ba3ad3bcbd18d683599e7fe1e43a473d6380561215491(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147dac30d9b8e7720751a863e68e58825182a6cc1de2bfca510b48bdcfa60185(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68c3e4c425342446f11ff75c1f506228df60243d742baf2e00837cb409b413f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c0791565d1e6cacea335b9a543aea3d015b8c85b1f76c147fe83f9c0f2203a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f522bbcb28bea4c99abaadedcbf63b9bc4ab40fa2f0100ae633250ec8d36a539(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe515a4abd216398604d4c39acc294d2fb1aa107b04f73796e920b5ac8a5eb8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleCookiesCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818535170437e567ee8a7fd38ad8d5f56963a51ca5d71a63a9689e52dfad1dd1(
    *,
    match_values: typing.Sequence[builtins.str],
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937d5188c586d44526208f903d7ce5b0b9813da90f1c59b3d543cd1857ca51c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ef0528c80c68b0cba270409bf763321873c03bc8313f0032f18384cc156ca9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a36739e60eeb3906ab0c5c32b4e5e689b2ef9eb9f2c2ad81cd4112fd9e308b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87b45d84425b4ee02a6fd57aeadcce074e7ebc9b0cc23d6e6e4ceedaeb96033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6841db00878f23cd4ffdc12e52959c4366e858fb861fb24f808f46bebb6e9e39(
    value: typing.Optional[CdnEndpointDeliveryRuleDeviceCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a5a5db1db80efdfbdc2e6ad7f1c0f09f1c7a904566dd6da94ef281a19ff3b3(
    *,
    match_values: typing.Sequence[builtins.str],
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f16c35da45ca0c6cbab0888c934181e1fc704a07027a678fc068b041545d6f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008f9dcdfb9eb45f49ace89196d2a861361bc7ff6dfa75bd6abf6f8d48992991(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c83b0bd476bef9d3778ba46aaca32d22ee6ed3b62576a934f6c868aa5aa8e9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c1fed4072da2ab1181c0657f9a58213bb46aa79a307fd85935186887f1b64b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bb6cab06b969a2e1cba3ece8983e996fcd4626f4c8fd4fb282e86d4ed396ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa623fbff112fdf75a13b44bdce15a66b7a19c7efe3c74bc152c00e6915cc933(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleHttpVersionCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319e8f365d13927fa6ae5a14575404194619de2ecc237bc9d749d3549b60d280(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7683076264f24c424e9ddd2306d5d08fdccd665fd742693f6012701baa8c82b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645609687213e9d0bdfc163cdaa7b3f5edc938b15be2b74a8da245910f76e584(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c3bfed28f1bcdaf57776e68b66ade63ca2ba42e0c389c8598bed0859e187c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd717137f2ca44071e318548ef6e9e11b402e9bff8800c06320c76f52a487c08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleHttpVersionCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8810f8f6bd590c248dafbcef8276df5f76ffdf8f2db1b6c1c7d5db847de6d21a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f41f9cece676e224623438c8d97cb38f78e44be86447746bba7857688186a53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9ea715e03b48aad94d6e838d3c75fe803239588736c8ac035ac1a8e37be6a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54abb99d260ef4dfd43594a01e0746168ea8a9409c5db6eb6c509924be4e156(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57137c6fbdba3faec60f07c31dc1d43c2c5d0a2610fac8d48a5ea89ca74783a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af739ef6881d64014dc3a2156c8dcccadebd28c51a90e34ffac04a1fd7059557(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c8d6b6ccae17e80855ef445a8bedc4d94d8b168b255e33db689832a321ff36(
    *,
    action: builtins.str,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca17a6764d2affb6e3d94e0a96fabddae9e7b0c9ccc61e4159922bf282813a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f248b6e53288745143f07d957b8c0b8a56ff774cfc53e81951052dd155061e2a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214977410bf2b051389aad3ad8d2f9ba89049fdfddd6eb2853d2e0b2b3d810be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57538bfd408d63279c5a05211d742cef75d707e9beb11f7b361d801c4e2351e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e9303d2764f12bf40ddafd43880a078e971f671f865dcb95cc99f839a01740(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a548c62c5843b12bdaf0d111083fc9a157bde9ac1303154da82e9057fe786a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyRequestHeaderAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc19704d9adb530d2de247130b7ba0b11b2bbe0801380b0bdd3ee8289f8584f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7560b6a61b3990521c9131e87a031b147528ce8eab5a88b96ae58018747c1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54fcaed5fe31ed233824774c8985fb81f10ab31a3858d13d91008cab01d853a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac143232a31d91e9dea110b575cdb83d9438594453edb8080c757c502ec34ee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696759835dc0d8a32ce99df67496b42ebf1d14afbd2f5482bf2c61f40077a63b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleModifyRequestHeaderAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a0dc236b6b588ba24aca9249964f5ceb2fdc50d3d09659a4cde22712ded26c(
    *,
    action: builtins.str,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2842fae04589874c86aecf8bfdf70af4f2abba93d86673a259f15ac57bb93488(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a473256200b9b6ae51dbec53b44f3413025be53036316e162415fba61ecde07(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d991300d8c1447d0c82d83a288e2803f28d3b0366a1dca29fa7dbbc8d0570724(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e211a3a3774c9d1c0eb6a85a71fb512d40cd67ed90c0d0883cc5dc1b2cd2ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e3b235b62437dca56183f119bcc3ce2f501dd1e2db372dd351a7cbb43fa5b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1529f72fd32ba921e2388933fbecb5b236e9d9fd942470ee4c1ae3b54716ab2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleModifyResponseHeaderAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67fa65b4cc14315c4c6ed9a28ea1d91d6315dc7e36842914954a956c51299c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0cfffedd91a03eeba2af35a5b89e54a6e9e4852e300ca88ab748e14b8740ce1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69f500f5e79d6ad67de524fe2daed9a87ae13c7476390803136e7eb74e8b50a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52926d6033b845d94b55a361c715d3ee94b2766981593dbe5f82ce9cc949728b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0d846ad533acb444e2c44ab0f18803e709198e0c8c0223b14b23498003f12a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleModifyResponseHeaderAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79becfc080681af33c3d8a68c42d9b20f5f1bf9c2176f5a21fd3a202c9414bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3144f1b90150da7cf6fd30ad07ec0451e9256aa7be757acab4d2ad8795ffc21(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleCookiesCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccfc92eb43e6c212e2d1a1d2fe20bfbdb4f4c764908eeea33abf1ba04e21f51(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleHttpVersionCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54d2ed0df78b5b7caf50d221d47047a99e5f5df1ef5c500fe770ea0eed2b76c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleModifyRequestHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e009d1027cf58c341b86cc5fdee0e0ec666ea68fb3ef108a18436914bc2f87ec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleModifyResponseHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58edef75f7e8721a65377bb6b2becd15f1c53ad3f465028cbd4a20332d1e668(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRulePostArgCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1748e8bd31a05f249d6bf383495ceaba7c9a2a970a535e9aec9e16db77e06980(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleQueryStringCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc8291452e93c84cf8900c37987f27f9fc3a028fcf46c1c188d1c22fc0ea2ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleRemoteAddressCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37d13a437659f60a011439c2245e1c76fbc2d6b292a457b5b8ee92419946cd0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleRequestBodyCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279b0dde1c1044495e4372e422cacd7001f8fc7b30a06460115baa6fe9f3749c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleRequestHeaderCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be862f03e042c57360d447d38ebd8962ff2fd81c9e2c9fa7e93672606dbbb2f0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleRequestUriCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3cb0ada5494367d0c874827928513fe1fe81dabcf5142c67f10344e553e5da1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleUrlFileExtensionCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc91802e1fc180dcef2236d9e968a3eb1307eac27970e90acec7080150cf4b5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleUrlFileNameCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681906a64d67fcc0eb7c81fbfedeabfe5aac4e90161bbf5781038d2e05a1fb33(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointDeliveryRuleUrlPathCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05157d1ee024a4021308772ce13740fbb1eb7018c61a6de26d2080cf49ca0896(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ddd5c03f705bf7a348aa3be86bb561fdcc4e42081ee56948b0977191b17ba89(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8905aebd65ef0e74df962f16096edcb4a26b77eb29fe64fdbc5517757ad3c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a922fa5e3499db75cb1692240aee610ca2e5a3499fe4fa8befa572d8c727cb(
    *,
    operator: builtins.str,
    selector: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9af103a721aaae92811f0953a9be7ffefc4fdd6f3374458bbb61ec937a5b0d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90cc384682f37067486ed437cd7c367b39bbd7a7107360dc27b76937d8f5f99a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12e2c6e09a91ddea0035b4afca5bd3ddb9ae9d626095051e43e4a84580877af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21174c63b89d62c9a0eb58ad261e653aa8648e8e4ee3a47693dfae1172cb5116(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4d0e2325bb14371a014a1ae2458f393eb659076c900afd51bc106b0140f5bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e8c6a12a33d55664c6d401e3d0f6fa0c277cf8d588fdd025433d334326efa1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRulePostArgCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1661deab8afbb0567395f9946110bccf520c16141842fcc021187df921e723ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d67019e8e079aa50d3bf4d026ad94c9b91c24ec97a465c4cd5f699536fc1f5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef1e478b5dad3ab0e8b34707f876916a932567849f7986250ac44a8ceaf7ef4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3773fff9451ef55f7979548a127256fabf527076b439f36f6a856d732bbfa408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d1b26bda01210a32cba81593802c769c201199696161dc32f476829c68a430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3a7858093ecc9c9afab80b15164bb5d2d3b3eb5ca4eccbbe4cd8b18c46b933(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__932f67e1c6cdf536c22046a9f1bfb213cbc45f42b85785dc4f75a2fdf9b4f56f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRulePostArgCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ab3bf66c80aaf836df029adc4b59bad5d30b16156a8f205c91083dce5894e1(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90516b85748f92ef391bdb0a4429aafbd2db106d1805c8259d632845a5164e72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b754fafdf207dd34c4c86fe527f856b81da98f89b3007945d1588a429b82ae1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1beb535d31995aaa2ace84078585de327bd101f51b1e5b0fc191fa31565e2792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31aeda6f16fc0fbcd804b57ba3dac09c50e5f1893fb40942df87b4d2f707d51d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a871558091dfd4b47e6644cbe255d6991cde526faceff5950be963cd043ad291(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87efd3dfab29e5518ef9d0769f60e392fe4cf0d0667f469e2ea50f08aaed662e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleQueryStringCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028a4b31d9e4f1a8cf9ca476d6d1d3af7966a2504813466c40db3a21a844ae84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7d288ff79dd0eccdde12a4c33517968dd60e3566f1d44a31297b30badc1df1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e693f5f1158712739ec8e4dd991c35ce4d2d085cc078b57f545e9821becf8be6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9900b19a708eb341387b5fc8841df4481e187e980346cdf636137db4292e0a3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a02f4a044d859c87187fffbf8fabe008b867ce6973f0bc5d4d50c2e8004d86(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebc95156f9e55a48b44d5bc3df007da01e2f86e7a98d09b9f1ceedab411c189(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleQueryStringCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138e33eab1a3b5cda90ec33cad5c684da6ce2975dad58d056de2e8aa22fbb798(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759a44d67f4db72d540948a4f9b6b300d4ba965d43ad9ff74d02588dadeaadf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9101f3597fef2011883c046bd9fd64c7747f0d910a3ec7743c0e1b32f17053(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f96ddbdab071bff0599470d3ca7157ce1e113a942a3b950e441f058da65d0af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91dd2cdcf77af3633db9eca89ff23da6a1aff35ef348dc6270eafe9c6a1d81a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c60ee39d5cc629710e15e9e4af29b778b811e8360b35497675d91fd19b76e15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2bdb7fb8fee690ca55c12484c5b48a2cc4554d576cb9be0930594251f06dc2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRemoteAddressCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a56efa392fba409a41a3175f809f56bf5f7805040c8adb42e0b6ca9a0e01b75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74cb12205985d05e40452634a5a8564151c66816ddf35e7212cd9e7869db58d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2762bd372c76715b7380446d09efd793953023b37f773c0b2202447bfd530a1a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631c19cbeb1ac20bb2f0eb8d55b70d41d394df5e68a39b4ce0801682aad2da98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e910f5f8d1c74fdc3fad92e5f4ad96195bfad652af5078c65afef4f5303a6e00(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRemoteAddressCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6d4947d23c8b709b12c3f502240871d557acc73f881cf0a9ced3579eab3d8d(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50367a5e47f99be66896802637807718e9c2baecc037c19064ba6a0c8c78c520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa92dab5309ea58c99ecbccb9f4de72dd160892ce68c6acb6db5102224ed1b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675b793483a39c6ea3c6e1a0a8fa630d037b71d84eb7c802f374bbd3c4364e7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da210c589d4566bd55af59bb3b0a005fedd5c93f1aea72c6683ca6fdde4b487e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd30e250f42f3916a29759469ec159dfa37eced51090a7860cdafdc65f15461(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bcb20e7c2b56d3572a595ebe227e4873e72d4fa88502a2282ce958cccc2fdf9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestBodyCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9833dc9986c7c0b25f9bc8acb0960ac52c17a78aa5073a17c5b144c885502fe7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e14fbff77d4e66d34bdeb0e6a6d57edc4f1dda27c1927f7194a0c1ae1b00ecc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5f39442800e2ee52a0800207aef6ca5d655b42729a319468084de2d9979776(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca966577f2c19f652136d1cc30f4932b8defb0994a9889f277a8577c2a6b402e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb8d7ed3e96b27fdd8e00de604d739c25a422004b6c1590e685cde18aa8af35(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4936ba9051bb0ce88ab9c6c84c553271b9dee4ed0e82cca5658a0763eeb967(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestBodyCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5d6836fee5f078e531f7d463a678cfeeb21c9824502eef2c950b3bd0441b46(
    *,
    operator: builtins.str,
    selector: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35eb6bd24ddfd60517240c539335d78e0c99b61ebeb1b08d169bd3cb66a3e413(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039dd869bf82924319841d0a1d9d9d676892a30555f93f13ede1added23f7704(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de340a044e4478bb1e73ac880000306427252e232e17194d4da61b3ea689225e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf89e0e3076fe39038182c4e671264e81330e0753adb0364a74b4d4f0ddcaa69(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620ac5389794c6a6946a0b7ea9e91d596426ca47505524c638328f0d7bf5c798(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ceb8013f87ec294e1bb27a55bfcd8d911b5396ca338d33761204587bb82ad1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestHeaderCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b652e5a3ae16234b96aab6ee0d1f29c314a228df28c72eaa4f33c5afbdf724f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df41f65acd0537bc3e3eb26d5f79279991e13417f5533e73497f605b78999ee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0cd1950708c9ac0a1c569961e4042006f4b36cc8793e1457a1f69032a3d2708(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6a2c85fe55ca530821d7996073f09a3a1326da8604c4ca5d9d46f7daec3281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef54d71733b55f0ed084f1d9df421b49a6e185b3e2a32f12dbd0c4e90275c846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e0ce2744729ae396725a1a2245330b8d355ca1bdc91701a7982c3d94792052(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df5ff9b1aad509da5ae5f44744c7db5ce746b9a25ff0438a77f8113ec467d01(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestHeaderCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c515ef3e210f4a6b5a57a8fd428f556e2a9f1fb22509e612506d966429ef5d(
    *,
    match_values: typing.Sequence[builtins.str],
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7695eb0ed2c7fd474e5a4539f37b5ad2f9fa7e3f8c4e55fd937869e1dd3f0812(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ca37fade34c26a261db88e69c235d1eebba0110c38dee9d4e18c2a76a5e0bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4829ed338398958df5cf13fcc08769943067c86813de30d20b6597bed4166cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4fb14cf44aa732c8d288c8cce45104daecbceaefd6a6966af16fb54748abb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88951c2f16d6c0d9abe960327805afaf29756de29f645cf58896937e7148774e(
    value: typing.Optional[CdnEndpointDeliveryRuleRequestMethodCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa7a2b972eefa4ae63dd0bf66f7baacb8376dc936730865601aa25377aa32ca(
    *,
    match_values: typing.Sequence[builtins.str],
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3023ddc4ff0bddb71ef774d1a1733ae549545605e57451ca4a9a89e23d0010(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a89f15e70f4a99816d432639c8ad74af9e2357ee08dbacf6741c2f867a08de4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc1cde2e4de0c560fcc06f6a0e09154371cc6b099ec02a1d72506d275eb6a83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68247188ba5d7f8c3b32ebea62ecf3aaf11914f9d309869463bfc38bf2891624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2843b8567634346b82e05169371ac2843104d2f5dadc9c56d6698698bdae67a(
    value: typing.Optional[CdnEndpointDeliveryRuleRequestSchemeCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae428c59678975c18d7a3275a171de68e30084dc80d6d0fa31e248bb8095860(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4f620d82036b02891f18af4c7974a0b38e6887942147d2eac5d80948a34738(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f022988f5f72b456f786bee06ad5c05129e5e508f4e35b159d9377d6934efa2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb96d1af24091788d7aff513162d0b6772de5697d28a532d633dc731702e3b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3509bf2f7053d2fc87797094851b60e8f7e7cc06d866a767ec750c9e53e20a6a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34470b0a7790a63b7a1f7b8bd022f436d1ecb5ed9a7f777841620cf485de0c1e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe747b01c03cc9c339291313f10200618e7337fb28fe5ca086a56ab7b873523(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleRequestUriCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de49e6ad781248398cff88e60edb5fa348715afb56ff2485dddc22e5445fe7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab50ff2276efffaa3f8f29be66256a806713868c8dd7b811ec5bade62d049f9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d05596c4ec1f59286748ca08bb4a1e5ef56d469b575f795cfe63e5675c044d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3beef8b228930f0bce276fb23121835be0e9dbd8df0850287af603d47f3b1836(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29c2f3ddeaef2d320f300c992874d8f2c8bb220f40169c3df6969d0532aafb4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3883da5dfa6919a2d16a922168217c11c95e6d3eee5570d501dbe4229ab6948(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleRequestUriCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703634b12940042e8c57de7eefcf646011e0df25d54d2f4d04dd733fd70a6584(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__213655506bc53f124d348b28bb6a04f24989f5d85c43721cc2af4a14fe9c70fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088a2853d5b7d035f71edfed5ba238f7619c01d4d87953ed718609758de728f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6898a8bd7ecbcbe1b154d1a168102c71fcddff41743fa0b425121ef09a17d494(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a346762dd5f5ca4e5dd8d69354a92583eec69a654afe6735362c67526b618a8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3c2fbcc96126afa30aa3950f8cb10be59bb51d557552f61eebaf29ea6d7405(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6c4652b6cbf92e876447d749690adb218d7e8b8f6de55f2160e4b3deb782b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlFileExtensionCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75643dcab8df8ee8692210a49fc9913f21f013383d5f8cf72deefe681e36ebb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce861f661fa669e5702c3877a2470a7e62862fd92f9b858c3ded926b1b0c69dd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc59cba7c78b92a56f39caba469ffafe15a5404e15a1a57d53a0a8f8d9d174ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7729fadab51c552615c7c6666aaab3c102454e1d6c21d07bb33aeb071dc213cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7a169ff41806d1404195040d25688634a17c8b817603c62a34292c55ddaea1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f9e64db2d8369fa39ba4cd0605647e27a5de24b09bfa800926d71dcea33ebc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlFileExtensionCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faaee70ffb1b6f95e78503936d73976f50923635a62c789e692c4c7024dc1b37(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f869c658e888cc3c2e68de8db91f0a38f73fa9434a062a3ae6388a691ef09d95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf6143e920ae701228483dd5c9f928adf58a8508647bbe3ee8b8250a76027ae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e5bc3223bdacc41b5927370568140eec1385d569df551958624f08a8d08c23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa4311ed0c656b1605c7a169a26ec11584794e4b880655793d97262d7254e8c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c930d68ceb31ce1a79f9e6177c3fa22033c65c16c1a352c8f370175618c9e46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4267a289a049b3904cdd18e8bbadf9cba9d3d67dc371c8778aff9a1ab5102178(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlFileNameCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098a57d5d49d9b15149096dc481cb1200352363630981c5110f95fb4c79029f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19a298d25956894a30dbd7bf304ed6c5c0a6aaaf481d468114afd121e719acd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8db53940e3441c141722060c39a5572bbbb99ac76cd101cf1f9f9be372e7935(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9939b040ffdfd29bfe757365befed04c7a63bd0a7a3632dfda863f102b47cf87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b65d361ec9efae4c44cc39726a3219cfc34ab39eb8d946d97061f26e65d6bcd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba75cb86ba2fbe0ca4e82b3cf1192445a3deaf54114c75dad8f31a17b16f8386(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlFileNameCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7509a1d01039b8a13f3411425015bd7afc2cf9440b2913a01f2740de0b4df7b9(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af1a0116e4423c73639a02717839d1ef8200d3c55e5817a87b3bfb7e1d7110b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc942175f86b258d65107da5d391dd999973ec94d51c57944bee88394e019e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dbb9eb5a7f66e10d45466af89630260a88f42528bf5d2cce6c299d41d3f11a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6b8214377c190155ef2fbc4902f099d48cce60588dde81b393d0c106617030(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a44b8368eb4f8e1c1252ceaf26bad713a07a6a23e0b1ab69033fb9edf97fcd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b05412794a9e64d0605fc41c5c2e152a9ecb676bc12e765d63a2881f9edd31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointDeliveryRuleUrlPathCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65b3cfdfcd477aa791a51ba4c11360b5c1064fae2808d2889627e834a7fab01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8def3e35df960dd3017f7b644861c3d7d0d276688fdf8d4f808af5cff42ce605(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0942137d344270d04d32bae54da6171268ea434e80f0811a10ac076d91be6e6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975e40fd4d4b530da1ba01d6d8dd237dd9548a5f8dea3d4ab29e498c4e17a532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0755e331cf16937f8ddf3702e330b79cb0d4d3632de74184dffb32aad82fba5d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bbdb8d1cbe0bae786dc7320c163098687a285c9b6e76d986f62bbdf2991da9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointDeliveryRuleUrlPathCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a744d7a12d76e6bc98858ac792617004f8b93ff01c6b01ef381bf0d1187fd1(
    *,
    redirect_type: builtins.str,
    fragment: typing.Optional[builtins.str] = None,
    hostname: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    query_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d053cc446821472782e0facd81431484bac65048ba9c7adfb9a17d1ceac1e9a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11cf6240ead0845c2ce7efd32082d32806589e1eb3c09548cc5aa6a5aaec9c2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b05d50e373e46cbfb41d00048293785cee3e55c59367d3baf601f4516fd2d08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2733cf7e5b6f13f38d2471d9ff7c5c7ad0f8c51e324c46e616f2f9311899eb55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4437102054b66f5f48b6e8e6d395cc520bb8eb40a327c3c67e52742a8b1d09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0835c3ed96d70bb0bde4125ff0ff2490aceabd3c99d1c92e2645971623e3a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77919cc814073d38eeddc0057e4fdc795adbfdcbd6603de6a9961796bbd3652c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e238c491e766f69d6f192803ef654cae0c0a4f268b00265dc110acc8fbd666(
    value: typing.Optional[CdnEndpointDeliveryRuleUrlRedirectAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9f64919e97d1884529a47a04f6aed55d24396c6c0053adabb72c7b2cc16fe4(
    *,
    destination: builtins.str,
    source_pattern: builtins.str,
    preserve_unmatched_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510ce431ce7d88aab45fd466346a19f622eb9d9309f90e3d3c088177b147c623(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c08c4a543ed8077ef1601c9f0ae4dd07ca6e71e65d45ea785b7f7e9434ae40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ff673c306d564f34d3ebde364921778e3b636fef38e34518f2203b98c84683(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8645fa3bf15cbcaeeb9b811ff31743d2f6d13d3bf2e5c3ff3ba5040fcbcdafef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0c9d0d59b76cc87a2dac736086afe77f7f12f7586f371a2d5f907fd8076e4b(
    value: typing.Optional[CdnEndpointDeliveryRuleUrlRewriteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835122195e697e8caf7643c81deb8d14372657458cf463f5bfcc3ec35f7495e3(
    *,
    action: builtins.str,
    country_codes: typing.Sequence[builtins.str],
    relative_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b11f551e1011d84d4f48d5199b2de033119fb952e8afeba75ca7388e1f1750(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fa5965613683eedd71142c4cdd1de20aa246d5542f3c767dbca47a1002e554(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c14cceec828fd4201abdf0a75e2742e213b4a4bfcdf38e580227318537f5ea8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d120b7b14abb8ae4ddb332196186af8bbf32470c5c98290f8851fa45c9b65d1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c480800085be276d8723046e54922e074205c7a2f48fb50e3e4a188bacc357c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b256cb3b672aa1b166b4eaaa1e4c4ab7290f4d2fd9e90f3d88e2577e05148e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGeoFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d938799433166b985efa8699691c53177d8af68cb89c240b3e36385f24657539(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281bd2def29809b77b4bfec438ccc8797cdd2ad04971793d5eee2ac585b56e70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72018966008ac2e50389fe719e9d7f4e1010cabe34ccbe2e6f8efabc99d45566(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a1c704b5d6ad69413d04505da818e5a35ced36e849c2bdd15539b25acfef38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdebf0471d3cb1531e2514fa2a1f9a5613e1befcefe3375db1ddedce0d2aaa4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGeoFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55057b4639eea2d0764e80191a38de934c342c9b002460ee58aab4b822118b90(
    *,
    cache_expiration_action: typing.Optional[typing.Union[CdnEndpointGlobalDeliveryRuleCacheExpirationAction, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_key_query_string_action: typing.Optional[typing.Union[CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction, typing.Dict[builtins.str, typing.Any]]] = None,
    modify_request_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    modify_response_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_redirect_action: typing.Optional[typing.Union[CdnEndpointGlobalDeliveryRuleUrlRedirectAction, typing.Dict[builtins.str, typing.Any]]] = None,
    url_rewrite_action: typing.Optional[typing.Union[CdnEndpointGlobalDeliveryRuleUrlRewriteAction, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad8609cc1c491888a7bce9e7f842bbe358d78b910956c8ddee0ae1b25e7b9df(
    *,
    behavior: builtins.str,
    duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1b34cb0956d407873ab643d6fd46a88a47e91cd5617df93b5ce0b0a87eea94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ccbd3d94d5e8b35ce0badeff82ea148f52cca6db341510253d6c78caa1cd521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb10f3bcdd8f399b3937d2de5ad0a6bfa505f0f408eacaa4b2a93b3ef0583f9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5d5ffdf77725644396954959232ee38adc33945c7f6158f2b10ba1323ab27f(
    value: typing.Optional[CdnEndpointGlobalDeliveryRuleCacheExpirationAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09293d84162fabad8033c719dd977bdd0ec690421959e98ba209c8f88d34e60e(
    *,
    behavior: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e563768fcd953c2b34dfc56d9ccefb9b6c94e91dd7409201b537336b91f554d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50725fd0740074008537c19912ab749912ec604cc8ddea8e1c8766791dce213b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58f5491baf76bded28b9e9d906ca4a9b6d4408ffa19d58aa81247ebb11109ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93b94db4f26ab129fc3382adbeb1dc9a8e4632a78667afaec1d93c304cbb051(
    value: typing.Optional[CdnEndpointGlobalDeliveryRuleCacheKeyQueryStringAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0ccc682a89ad629523bbadca36d1969792653eb9f86757575e610d4316432a(
    *,
    action: builtins.str,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a1bedae1c809f7c0a280e436f00a1302bbcf9ebd64559966e7f144332b9061(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea33517b3fb783f8f0029809dbd7a1726c983a010f6231a4fb5d327ecff8f1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428e2c6717b20b85531d74c10432f8a7f1f9286e301f818895d134d363053ec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f0cb1ca4c3a279e5c627421d019e5eb9370dae54d09d0874abb7efdb50d19b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12525bf4288194ba240dda229278a1d0d45a071637b849ac495dcf0069ddf795(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63ae7e19b6ecd369734e520e43822cf6c38c60c59d68e0112baefd2cdbcd769(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbd43188c09520fd703786e649bb89b1a500ead11aa07bd5e1eca806eebc325(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c75ea75effed7fefda1adfc9d463e6afd567e7a4cca62c502730bb7979156c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552fb8dca8c051799aca78fca8dbbf1c393280c4e48c78c816d7b6f7c3e95877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0248c234344d9fb24d421c65e9472d231433a9177254a4fc99ff4254240dc80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9574a7f7178f267d25b158d9b5311b392b590e31c2fb174029f8a0647907b272(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43215636beb1a77449a41e4f012eaf4b5c20108806a362c0bd114cc6879e6ba0(
    *,
    action: builtins.str,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f89bf80227577f22a96cf62b6d93cd308383ce2a3cb090a0aaf4675e74dcba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611de4791828c918a0219d34ee9d439aab1f3ac90f7716297c7f7c354898c346(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ec607f9197a4601a2a2a43e848072839f96021ee7b1d7ba46fb57843ae7b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886bddf2094f35a081dc994d709090a301cda913e5e067a4eded91ddb109f332(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fa730100159455612679da4fd91cc01735c0b468f81e9e9a464aede17572b7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b005ac6040c931d59750fa6dca3640b05c497bce8491149991cfd70ed4961384(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd1a3264a506a2c8e299e60968e3e704d322dd5841e20a523384aceab2f6a9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab094bb585bd865530f663ae4b6935674ad62516d60a6e8acf2953566a5be25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a126dc38251876d788c5a00086ddf0656ad5cab8377397c933d64189985292fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df31b36fd67149725c21655a39a9edbb22613bd5f65bae00d669c0741e091523(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0a116aa07aca8c89ecc7f6b6893bbdf5c4d4486dbdd9cb95021f0aa94c1411(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40f283fa4e1bc51a7a827d1f73a4e51c4af2133063d9a06f4c4a19511e19a90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9365c561dac0fc3ffd4e816a7f525d03bc72083fc3e8ece2e72cfdcff9d383fb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointGlobalDeliveryRuleModifyRequestHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b28736669370383edb4f5ec8f33b88d84593ebd1e6eb7d0cc3768f8b12ff2a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnEndpointGlobalDeliveryRuleModifyResponseHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbeec77ac4d0a796ecdc79e7002e6d4c1e6cbd560630a82e77625c8e87955da7(
    value: typing.Optional[CdnEndpointGlobalDeliveryRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266be95137650349fc0fba1620d556d515a51a3997877181d1597fd6faf3da8f(
    *,
    redirect_type: builtins.str,
    fragment: typing.Optional[builtins.str] = None,
    hostname: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    query_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd3ad04a01cc6439e382e513f6547806516a41e6010a535ff0ee2189e4fe0bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5cd50735f24f419297d23a05bc73c6324c31ab8256a1d02608930af204531b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5310d9c8e901c564331d7606e70d6f669975ad6140f52e0f3bf6845019cb8023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a66cb687d22f05b891bab107e9251300ce543dc8933b673a484827d93b17ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f296bd81ff32ebd752cd9d0ed4b42a7906740bcb7362f9bad6e5151dff8904f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b6ea122a1d260173fe50427625ca2e4d4c4abe1bbace2bc7e0b245e5ae41d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e07260e97a24d54ab3f24d447ded4dbb4658663e5441cb7996f17f6d9c7aee9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5704eee50bd362b39954a1628501d60cad117e896e3fc6a9c40e4326f16fea1(
    value: typing.Optional[CdnEndpointGlobalDeliveryRuleUrlRedirectAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67829debe997502b2cfe991a043b0d92078543a059910f0d52108588915482f6(
    *,
    destination: builtins.str,
    source_pattern: builtins.str,
    preserve_unmatched_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d9b58b048280983c5c6e66c21567b48387a80763c2655dbeb286957b4572a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50cea72ef6acae6aa7368e4dcfd35a7292ee300de26d1f9faa4267f7fabbe6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c27e1dc36ecdc5bb4bf44039724182d106c196391a21c024e66b98a91c72f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22278ae8eb5791eb9182ba13dbca7688a7ef22f863fca48d49fa19e46483e1fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aaa799c9891291c8cda24adf210bb7fb46622976be86556bf33ff355d49a60c(
    value: typing.Optional[CdnEndpointGlobalDeliveryRuleUrlRewriteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4b1c0dbdcee7a2b737569e0828916451459f0c3267780c6eb527073cf1d468(
    *,
    host_name: builtins.str,
    name: builtins.str,
    http_port: typing.Optional[jsii.Number] = None,
    https_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e14e661de661804f3ea7989c88e7afadb380655450996bda08c59f6a33e7db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f7bff08bf41feae46deda8535e8fe26cdb7b43cee107a02f9f421bee7217f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e610a35de73ca1ae2efb15bf159e5dd17e6c949bfdc7e3bb7c7cb4305ef5425e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16397b0713829163408a4ac63a92b46ad0fe64a9183ac726736bc8c1d52adcda(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b31e5d9bf832915a68ec309d63f57667138fb858bd1527c136b458324fe197b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ca7d8db7e1e58b9223c50b97fb7eac0146d29abeb47f0c9baff3ca3b366ab0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnEndpointOrigin]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fca5d9197567f011280889133972e663f6529e2c05112dbd59e8c7812d8338(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727035bf6d8721a0c467a3dd7a816012dd6fcbca11929aa1ed8ff8ae4378bd90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfef61f3faf72ff2d5f572cb1ae3742389b4757e8dbd7ff18f937d1cdccbcfc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9936402f6d094daf71a486f14f8bd213e4953146551e88626851cb6cc60c2573(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817ad04939d8c60f9a1bf69133f8d2e21e2d695afbadfbc154fb0a908fb68d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102a808f51857d08491febe2ae4b22467c50d31a68ddbba98e486c805f86c8d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointOrigin]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4894374ca5afdb8aeb2b58f2af2fea8daab45ff0bbe4835f09f353aa58263de8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69360c439e86d1666428f77d416205eb7b264da3697bf5f5e7608f65185bf952(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc93b60f3bd926d5bc78f8fe3efb8c9ba03b4eadac624d76606f8b7a7e076109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300329fd613ce81794eb78f1036717a03e0ed79936bc892fce8311ce5fb0a67b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883b4b898de52a133d796c3d45b3cab4d12d9d89c612e3d7fdbc8d580b519069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ccc03df3718f5db3bfd08741ee9cb1a075705bc66e42b58d507761d142e885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1a3d6fc86a503892214757e93529f4ac2f209b95599fc1395116fb2e0a728c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnEndpointTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
