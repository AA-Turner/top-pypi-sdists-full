r'''
# `azurerm_frontdoor`

Refer to the Terraform Registry for docs: [`azurerm_frontdoor`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor).
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


class Frontdoor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.Frontdoor",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor azurerm_frontdoor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backend_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorBackendPool", typing.Dict[builtins.str, typing.Any]]]],
        backend_pool_health_probe: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorBackendPoolHealthProbe", typing.Dict[builtins.str, typing.Any]]]],
        backend_pool_load_balancing: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorBackendPoolLoadBalancing", typing.Dict[builtins.str, typing.Any]]]],
        frontend_endpoint: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorFrontendEndpoint", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        resource_group_name: builtins.str,
        routing_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorRoutingRule", typing.Dict[builtins.str, typing.Any]]]],
        backend_pool_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorBackendPoolSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FrontdoorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor azurerm_frontdoor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backend_pool: backend_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool Frontdoor#backend_pool}
        :param backend_pool_health_probe: backend_pool_health_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_health_probe Frontdoor#backend_pool_health_probe}
        :param backend_pool_load_balancing: backend_pool_load_balancing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_load_balancing Frontdoor#backend_pool_load_balancing}
        :param frontend_endpoint: frontend_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#frontend_endpoint Frontdoor#frontend_endpoint}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#resource_group_name Frontdoor#resource_group_name}.
        :param routing_rule: routing_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#routing_rule Frontdoor#routing_rule}
        :param backend_pool_settings: backend_pool_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_settings Frontdoor#backend_pool_settings}
        :param friendly_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#friendly_name Frontdoor#friendly_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#id Frontdoor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#load_balancer_enabled Frontdoor#load_balancer_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#tags Frontdoor#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#timeouts Frontdoor#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a46a4c768d7d352f48a58e20c790a039105b2ebcea19b38ef28eddb40b78000)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FrontdoorConfig(
            backend_pool=backend_pool,
            backend_pool_health_probe=backend_pool_health_probe,
            backend_pool_load_balancing=backend_pool_load_balancing,
            frontend_endpoint=frontend_endpoint,
            name=name,
            resource_group_name=resource_group_name,
            routing_rule=routing_rule,
            backend_pool_settings=backend_pool_settings,
            friendly_name=friendly_name,
            id=id,
            load_balancer_enabled=load_balancer_enabled,
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
        '''Generates CDKTF code for importing a Frontdoor resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Frontdoor to import.
        :param import_from_id: The id of the existing Frontdoor that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Frontdoor to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85964357cb6603d1cb4f53fb91e77f01af1d69507fb5b08849494579543acce5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackendPool")
    def put_backend_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorBackendPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1eff61cbef45749cd63732a92dbde3378721b1894fcc4f68381cf9cca119a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendPool", [value]))

    @jsii.member(jsii_name="putBackendPoolHealthProbe")
    def put_backend_pool_health_probe(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorBackendPoolHealthProbe", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6629a5c50038f2d0fcaf8e2249b3cef16cff8bbae9ae0115bb028403abcfcf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendPoolHealthProbe", [value]))

    @jsii.member(jsii_name="putBackendPoolLoadBalancing")
    def put_backend_pool_load_balancing(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorBackendPoolLoadBalancing", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756f5c9f505528e020df5c9c2d0c2aae58b2e38ce5989bffbc0219e06f6e7f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendPoolLoadBalancing", [value]))

    @jsii.member(jsii_name="putBackendPoolSettings")
    def put_backend_pool_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorBackendPoolSettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598c843a081037685d799399f92826beb3eeea12f6a085b446808a437e285dff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendPoolSettings", [value]))

    @jsii.member(jsii_name="putFrontendEndpoint")
    def put_frontend_endpoint(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorFrontendEndpoint", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c8a97d7b73716eaa60f85aad9400f5aab9b2e364f97e6c6406e173247af05c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFrontendEndpoint", [value]))

    @jsii.member(jsii_name="putRoutingRule")
    def put_routing_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorRoutingRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17871732e50df8f12ce1709c8ed30a234b415887acd9a942458765452fbfc40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRoutingRule", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#create Frontdoor#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#delete Frontdoor#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#read Frontdoor#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#update Frontdoor#update}.
        '''
        value = FrontdoorTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackendPoolSettings")
    def reset_backend_pool_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendPoolSettings", []))

    @jsii.member(jsii_name="resetFriendlyName")
    def reset_friendly_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFriendlyName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoadBalancerEnabled")
    def reset_load_balancer_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerEnabled", []))

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
    @jsii.member(jsii_name="backendPool")
    def backend_pool(self) -> "FrontdoorBackendPoolList":
        return typing.cast("FrontdoorBackendPoolList", jsii.get(self, "backendPool"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolHealthProbe")
    def backend_pool_health_probe(self) -> "FrontdoorBackendPoolHealthProbeList":
        return typing.cast("FrontdoorBackendPoolHealthProbeList", jsii.get(self, "backendPoolHealthProbe"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolHealthProbes")
    def backend_pool_health_probes(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "backendPoolHealthProbes"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolLoadBalancing")
    def backend_pool_load_balancing(self) -> "FrontdoorBackendPoolLoadBalancingList":
        return typing.cast("FrontdoorBackendPoolLoadBalancingList", jsii.get(self, "backendPoolLoadBalancing"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolLoadBalancingSettings")
    def backend_pool_load_balancing_settings(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "backendPoolLoadBalancingSettings"))

    @builtins.property
    @jsii.member(jsii_name="backendPools")
    def backend_pools(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "backendPools"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolSettings")
    def backend_pool_settings(self) -> "FrontdoorBackendPoolSettingsList":
        return typing.cast("FrontdoorBackendPoolSettingsList", jsii.get(self, "backendPoolSettings"))

    @builtins.property
    @jsii.member(jsii_name="cname")
    def cname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cname"))

    @builtins.property
    @jsii.member(jsii_name="explicitResourceOrder")
    def explicit_resource_order(self) -> "FrontdoorExplicitResourceOrderList":
        return typing.cast("FrontdoorExplicitResourceOrderList", jsii.get(self, "explicitResourceOrder"))

    @builtins.property
    @jsii.member(jsii_name="frontendEndpoint")
    def frontend_endpoint(self) -> "FrontdoorFrontendEndpointList":
        return typing.cast("FrontdoorFrontendEndpointList", jsii.get(self, "frontendEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="frontendEndpoints")
    def frontend_endpoints(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "frontendEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="headerFrontdoorId")
    def header_frontdoor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerFrontdoorId"))

    @builtins.property
    @jsii.member(jsii_name="routingRule")
    def routing_rule(self) -> "FrontdoorRoutingRuleList":
        return typing.cast("FrontdoorRoutingRuleList", jsii.get(self, "routingRule"))

    @builtins.property
    @jsii.member(jsii_name="routingRules")
    def routing_rules(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "routingRules"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FrontdoorTimeoutsOutputReference":
        return typing.cast("FrontdoorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolHealthProbeInput")
    def backend_pool_health_probe_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPoolHealthProbe"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPoolHealthProbe"]]], jsii.get(self, "backendPoolHealthProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolInput")
    def backend_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPool"]]], jsii.get(self, "backendPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolLoadBalancingInput")
    def backend_pool_load_balancing_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPoolLoadBalancing"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPoolLoadBalancing"]]], jsii.get(self, "backendPoolLoadBalancingInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolSettingsInput")
    def backend_pool_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPoolSettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPoolSettings"]]], jsii.get(self, "backendPoolSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyNameInput")
    def friendly_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "friendlyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendEndpointInput")
    def frontend_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorFrontendEndpoint"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorFrontendEndpoint"]]], jsii.get(self, "frontendEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerEnabledInput")
    def load_balancer_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loadBalancerEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingRuleInput")
    def routing_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorRoutingRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorRoutingRule"]]], jsii.get(self, "routingRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FrontdoorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FrontdoorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d0ed82978f44c8d7a55aa0372676965040429c892bc2bc848c1e89630f8dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79241666a4e309960194d9cdd851b68e76aa8c609f2fed8f48d7718f6faa886e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerEnabled")
    def load_balancer_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "loadBalancerEnabled"))

    @load_balancer_enabled.setter
    def load_balancer_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3983be6fba5d8011fbf697132730a191b79e4babf65940f0cf5f33f535e123ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daee6c36c49c347a07e969b81becf56c73333d84fe841fb97807ae0e8a8d3ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86bd579afd046ef02f26bb74054bd40c70fde424267732b5f61be941e8edd82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776865e51568e769641924d415622417c534296a6cbf871e6750ea2df9807aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPool",
    jsii_struct_bases=[],
    name_mapping={
        "backend": "backend",
        "health_probe_name": "healthProbeName",
        "load_balancing_name": "loadBalancingName",
        "name": "name",
    },
)
class FrontdoorBackendPool:
    def __init__(
        self,
        *,
        backend: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorBackendPoolBackend", typing.Dict[builtins.str, typing.Any]]]],
        health_probe_name: builtins.str,
        load_balancing_name: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend Frontdoor#backend}
        :param health_probe_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#health_probe_name Frontdoor#health_probe_name}.
        :param load_balancing_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#load_balancing_name Frontdoor#load_balancing_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f359faac6f4f23f294e49156f555fae1614f3c448e705b813f0ea8f4661856)
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument health_probe_name", value=health_probe_name, expected_type=type_hints["health_probe_name"])
            check_type(argname="argument load_balancing_name", value=load_balancing_name, expected_type=type_hints["load_balancing_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend": backend,
            "health_probe_name": health_probe_name,
            "load_balancing_name": load_balancing_name,
            "name": name,
        }

    @builtins.property
    def backend(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPoolBackend"]]:
        '''backend block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend Frontdoor#backend}
        '''
        result = self._values.get("backend")
        assert result is not None, "Required property 'backend' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorBackendPoolBackend"]], result)

    @builtins.property
    def health_probe_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#health_probe_name Frontdoor#health_probe_name}.'''
        result = self._values.get("health_probe_name")
        assert result is not None, "Required property 'health_probe_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancing_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#load_balancing_name Frontdoor#load_balancing_name}.'''
        result = self._values.get("load_balancing_name")
        assert result is not None, "Required property 'load_balancing_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorBackendPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolBackend",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "host_header": "hostHeader",
        "http_port": "httpPort",
        "https_port": "httpsPort",
        "enabled": "enabled",
        "priority": "priority",
        "weight": "weight",
    },
)
class FrontdoorBackendPoolBackend:
    def __init__(
        self,
        *,
        address: builtins.str,
        host_header: builtins.str,
        http_port: jsii.Number,
        https_port: jsii.Number,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        priority: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#address Frontdoor#address}.
        :param host_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#host_header Frontdoor#host_header}.
        :param http_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#http_port Frontdoor#http_port}.
        :param https_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#https_port Frontdoor#https_port}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#enabled Frontdoor#enabled}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#priority Frontdoor#priority}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#weight Frontdoor#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a6389a3f63ef4d2d3cd3366bab752dce980875089b4fa1afab228e5d50450c)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument host_header", value=host_header, expected_type=type_hints["host_header"])
            check_type(argname="argument http_port", value=http_port, expected_type=type_hints["http_port"])
            check_type(argname="argument https_port", value=https_port, expected_type=type_hints["https_port"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "host_header": host_header,
            "http_port": http_port,
            "https_port": https_port,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if priority is not None:
            self._values["priority"] = priority
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#address Frontdoor#address}.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_header(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#host_header Frontdoor#host_header}.'''
        result = self._values.get("host_header")
        assert result is not None, "Required property 'host_header' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#http_port Frontdoor#http_port}.'''
        result = self._values.get("http_port")
        assert result is not None, "Required property 'http_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def https_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#https_port Frontdoor#https_port}.'''
        result = self._values.get("https_port")
        assert result is not None, "Required property 'https_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#enabled Frontdoor#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#priority Frontdoor#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#weight Frontdoor#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorBackendPoolBackend(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorBackendPoolBackendList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolBackendList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8dccf7ec87f75ac9fd875fc2e31661dcff14219400337038ece63f46488d56f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FrontdoorBackendPoolBackendOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ff8807cb2f51b404027637c00ddb8ddfbd23b80a6e0dc5d3b72e76054d1757)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FrontdoorBackendPoolBackendOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8425ca3a3836056070b0b30237b7235ffe3097bef827e5ce5f75df20bbb1c099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab558ad75339dc4a18f2ef3f68168fe61e3007737e7555e1983bf645f7192265)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff9308cb9048f027a2e99cb457d800d2d15558221fce4ccaaf5720a3a0670dc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolBackend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolBackend]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolBackend]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d358ebfb1da0ee263c9fd576f451528a575e3d30bea017dc80fdc2a7bdd4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FrontdoorBackendPoolBackendOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolBackendOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef288145a14641832ce04e594fab32e910f46ce7ee3e045f8d4095b12ca3f9a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostHeaderInput")
    def host_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="httpPortInput")
    def http_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpPortInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsPortInput")
    def https_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpsPortInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c32efb13b1263b799a2936daa78d0dd4fbd3ed4b103996bcbeed23ecc1f3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__5bac2acb6c9cc85015cb70cdd1a138750d84d0f0f716edc2abed9f11d70bae34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostHeader")
    def host_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostHeader"))

    @host_header.setter
    def host_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91906bcf3ee823215d6ab9109ee1322c54315cbe019b47e4c05535ad885e407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpPort")
    def http_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpPort"))

    @http_port.setter
    def http_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d646ef7ad1ce05bc54032159a0ee52f4a186abad71f151645e299c48f7affa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsPort")
    def https_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpsPort"))

    @https_port.setter
    def https_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02aaa1e8e22c969627e92678b8f47bfe3c735293d2ed1aec11c9bacf02da239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c66a8cd9303f9a5ff63d0b15cd504af72da41e838bec9ab3ba26ca7fc2f497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597770b5a7458868c9e407a477492302c0f1ad85267dd4b8bcce5c4210000326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolBackend]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolBackend]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolBackend]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb1dc211010f981a5be54b841f0f12d1e486f47d6132401155b336c789abb75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolHealthProbe",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "enabled": "enabled",
        "interval_in_seconds": "intervalInSeconds",
        "path": "path",
        "probe_method": "probeMethod",
        "protocol": "protocol",
    },
)
class FrontdoorBackendPoolHealthProbe:
    def __init__(
        self,
        *,
        name: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        interval_in_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        probe_method: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#enabled Frontdoor#enabled}.
        :param interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#interval_in_seconds Frontdoor#interval_in_seconds}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#path Frontdoor#path}.
        :param probe_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#probe_method Frontdoor#probe_method}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#protocol Frontdoor#protocol}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14442537f84e99e674c278d7d638509418e4e7400592a2d74baeb650e8708028)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument interval_in_seconds", value=interval_in_seconds, expected_type=type_hints["interval_in_seconds"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument probe_method", value=probe_method, expected_type=type_hints["probe_method"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if interval_in_seconds is not None:
            self._values["interval_in_seconds"] = interval_in_seconds
        if path is not None:
            self._values["path"] = path
        if probe_method is not None:
            self._values["probe_method"] = probe_method
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#enabled Frontdoor#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#interval_in_seconds Frontdoor#interval_in_seconds}.'''
        result = self._values.get("interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#path Frontdoor#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def probe_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#probe_method Frontdoor#probe_method}.'''
        result = self._values.get("probe_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#protocol Frontdoor#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorBackendPoolHealthProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorBackendPoolHealthProbeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolHealthProbeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea7668bb1d52a2f2d27b703d7753d368ff52ccd3f43fd76953c533e507225772)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FrontdoorBackendPoolHealthProbeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e1d2badce026d9543e35c311e1acac6f8f5ba278ccb7aef3e922d7f5d662f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FrontdoorBackendPoolHealthProbeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920df4986d716b737467568a68fe7e8aefa601e59b22c1164960cfb65d00d97c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed9a815423a137e69eb3129386c431da4bf96efb0444017a91c21d529a292a8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8858a65b4452d0c825a2a6e2a72ebccecc46b9d8557915585340095312848f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolHealthProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolHealthProbe]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolHealthProbe]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1978f9dbf0abaefa54c2e33300f72e006ec572b3d114066c7e1c8760acde7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FrontdoorBackendPoolHealthProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolHealthProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54a9b5ba01bee655ba03c99bf190812c0c95c5200a18828f0f9236d178464792)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetIntervalInSeconds")
    def reset_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalInSeconds", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetProbeMethod")
    def reset_probe_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProbeMethod", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInSecondsInput")
    def interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="probeMethodInput")
    def probe_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "probeMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bef63d36858f8efb683360d2bbba3f13e4ed7b33594fc5dde0bfc6d353099091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalInSeconds")
    def interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalInSeconds"))

    @interval_in_seconds.setter
    def interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c09fa5e53564015de2a2f6fa47fa0f99abf1a455c4207000a3ddfb7ab2dc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dafb6e94380cb6259bbda9c57503b16d7ac5f13263b39922d103b48d8174599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5759da6623c2b1823430187ffcbf9709e2c7b5864d91e51b91adebeef66d3963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="probeMethod")
    def probe_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "probeMethod"))

    @probe_method.setter
    def probe_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b050dd08ca6e3563dd96c863b7d7e0a71185bcb9c19617b64e13494afe67642b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "probeMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22ebb5fd8fb271e55ac90ef5575d45c5147934eb5e92a1eb7a5ceef573f28bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolHealthProbe]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolHealthProbe]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolHealthProbe]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b2e26e5aa89b2b62ac63cf4664ec05529585672ab556e860f07264102979de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FrontdoorBackendPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e25378fd2b0c884e5e5ecf31a2134b07b622fe09929a649417ae1d16125d9dcd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FrontdoorBackendPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135d529e45e2e9f45e6dcafc6129e9ff7a7e2c3df8d3bd2a3e26ae0e5faedd9f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FrontdoorBackendPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba9b87892a5fffc80fc224e83d3439990a1a752b44df4597ba137d1ae7ae4f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c7df4ee27ce0710e5f84bca114b8afa50763ef97c4a796f5df4a270bedcad80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72ee8e18e16b05915b0d63ea0d3dbb48b7f20a0ca092dc03bb9e7e205af3b6a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c905f0f26ce72c5ef541b98e15d236707716a319ec2a8d8f3b38f69f8fd23483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolLoadBalancing",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "additional_latency_milliseconds": "additionalLatencyMilliseconds",
        "sample_size": "sampleSize",
        "successful_samples_required": "successfulSamplesRequired",
    },
)
class FrontdoorBackendPoolLoadBalancing:
    def __init__(
        self,
        *,
        name: builtins.str,
        additional_latency_milliseconds: typing.Optional[jsii.Number] = None,
        sample_size: typing.Optional[jsii.Number] = None,
        successful_samples_required: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.
        :param additional_latency_milliseconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#additional_latency_milliseconds Frontdoor#additional_latency_milliseconds}.
        :param sample_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#sample_size Frontdoor#sample_size}.
        :param successful_samples_required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#successful_samples_required Frontdoor#successful_samples_required}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21ce34d73db8856151da0982afbedcfac3411b4d0c96aacb475bf331fccd9be)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument additional_latency_milliseconds", value=additional_latency_milliseconds, expected_type=type_hints["additional_latency_milliseconds"])
            check_type(argname="argument sample_size", value=sample_size, expected_type=type_hints["sample_size"])
            check_type(argname="argument successful_samples_required", value=successful_samples_required, expected_type=type_hints["successful_samples_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if additional_latency_milliseconds is not None:
            self._values["additional_latency_milliseconds"] = additional_latency_milliseconds
        if sample_size is not None:
            self._values["sample_size"] = sample_size
        if successful_samples_required is not None:
            self._values["successful_samples_required"] = successful_samples_required

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_latency_milliseconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#additional_latency_milliseconds Frontdoor#additional_latency_milliseconds}.'''
        result = self._values.get("additional_latency_milliseconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sample_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#sample_size Frontdoor#sample_size}.'''
        result = self._values.get("sample_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def successful_samples_required(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#successful_samples_required Frontdoor#successful_samples_required}.'''
        result = self._values.get("successful_samples_required")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorBackendPoolLoadBalancing(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorBackendPoolLoadBalancingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolLoadBalancingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__142ea549aaf0e4fb427dab1ba5798594e1d313c86083cf556c062ec4a08304b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FrontdoorBackendPoolLoadBalancingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeacc38f589504952a8459516788b8dd25814d86db03b746ae8b9b8badcc8e5d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FrontdoorBackendPoolLoadBalancingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5defd5389f38ba12df9c163cb8759915e917c0c850af42d2692078fc3de55a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a944bc37b26f6c65b66466ae4280ef93466b2738b42b545aa1a1c3f13e12de48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0480145695cd71ce4e95d52e5b083d81d55b8f66db7e4b6a46b1ea82be3e5723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolLoadBalancing]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolLoadBalancing]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolLoadBalancing]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61063313f4286fdc71459a9cca4df296ffe412537364cb9eda2799d8db74f1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FrontdoorBackendPoolLoadBalancingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolLoadBalancingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ca1e515448459faae6b42f81f83d046c6dab62f8624c904dcef76044d94f3af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAdditionalLatencyMilliseconds")
    def reset_additional_latency_milliseconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalLatencyMilliseconds", []))

    @jsii.member(jsii_name="resetSampleSize")
    def reset_sample_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleSize", []))

    @jsii.member(jsii_name="resetSuccessfulSamplesRequired")
    def reset_successful_samples_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessfulSamplesRequired", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="additionalLatencyMillisecondsInput")
    def additional_latency_milliseconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "additionalLatencyMillisecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleSizeInput")
    def sample_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="successfulSamplesRequiredInput")
    def successful_samples_required_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successfulSamplesRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalLatencyMilliseconds")
    def additional_latency_milliseconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "additionalLatencyMilliseconds"))

    @additional_latency_milliseconds.setter
    def additional_latency_milliseconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59194fb5a3d0d5f037b0866b2733a7f4a92a2f2cef62b76f3bdbfd8970df471a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalLatencyMilliseconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b73e9246ba258802b3f632b18afa27b55a8e608f604ed7ba710175fba193f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleSize")
    def sample_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleSize"))

    @sample_size.setter
    def sample_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0cebbec834b839450385b7c2719e43b994a3261ba431f0391f87366b18dbb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successfulSamplesRequired")
    def successful_samples_required(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successfulSamplesRequired"))

    @successful_samples_required.setter
    def successful_samples_required(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1810c2dcdeff67c2719e255a6438b391ee78182b22b41b56fe022a97192626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successfulSamplesRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolLoadBalancing]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolLoadBalancing]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolLoadBalancing]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640c857257ac05f8620fad9ea036f9230a5fb2fe4e30240daaf4b15b44b61fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FrontdoorBackendPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6733d85131963692c4175ea4c0f4ee7776a6c1e979b699802108a5ab8b4b6432)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBackend")
    def put_backend(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolBackend, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0deca5aef016df454873c54d23a24db52b563bb5b9e2ea3406ba68d2ca0862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackend", [value]))

    @builtins.property
    @jsii.member(jsii_name="backend")
    def backend(self) -> FrontdoorBackendPoolBackendList:
        return typing.cast(FrontdoorBackendPoolBackendList, jsii.get(self, "backend"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolBackend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolBackend]]], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="healthProbeNameInput")
    def health_probe_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthProbeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingNameInput")
    def load_balancing_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="healthProbeName")
    def health_probe_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthProbeName"))

    @health_probe_name.setter
    def health_probe_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6eb25bdde5111ac010cecbd3a3c889518f7308b2806390993d0c4607b41385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthProbeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingName")
    def load_balancing_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingName"))

    @load_balancing_name.setter
    def load_balancing_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1af780c1c38164ca26dd14100099c8fcd7e743819d908f1ba38b3dc86f6da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b8bbd2f5439bff30ed8b43b6ce57b4aec72c04b5663ce9466aa28062771b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb17c82482ee339664006f57f8ac7a6c624a0cddd8154f178060b3d413b9e104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enforce_backend_pools_certificate_name_check": "enforceBackendPoolsCertificateNameCheck",
        "backend_pools_send_receive_timeout_seconds": "backendPoolsSendReceiveTimeoutSeconds",
    },
)
class FrontdoorBackendPoolSettings:
    def __init__(
        self,
        *,
        enforce_backend_pools_certificate_name_check: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        backend_pools_send_receive_timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enforce_backend_pools_certificate_name_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#enforce_backend_pools_certificate_name_check Frontdoor#enforce_backend_pools_certificate_name_check}.
        :param backend_pools_send_receive_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pools_send_receive_timeout_seconds Frontdoor#backend_pools_send_receive_timeout_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042ac0f3f31e16f9a716a856c2f097d2d9e30d6c5fd77f7e2400305f776655c4)
            check_type(argname="argument enforce_backend_pools_certificate_name_check", value=enforce_backend_pools_certificate_name_check, expected_type=type_hints["enforce_backend_pools_certificate_name_check"])
            check_type(argname="argument backend_pools_send_receive_timeout_seconds", value=backend_pools_send_receive_timeout_seconds, expected_type=type_hints["backend_pools_send_receive_timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enforce_backend_pools_certificate_name_check": enforce_backend_pools_certificate_name_check,
        }
        if backend_pools_send_receive_timeout_seconds is not None:
            self._values["backend_pools_send_receive_timeout_seconds"] = backend_pools_send_receive_timeout_seconds

    @builtins.property
    def enforce_backend_pools_certificate_name_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#enforce_backend_pools_certificate_name_check Frontdoor#enforce_backend_pools_certificate_name_check}.'''
        result = self._values.get("enforce_backend_pools_certificate_name_check")
        assert result is not None, "Required property 'enforce_backend_pools_certificate_name_check' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def backend_pools_send_receive_timeout_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pools_send_receive_timeout_seconds Frontdoor#backend_pools_send_receive_timeout_seconds}.'''
        result = self._values.get("backend_pools_send_receive_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorBackendPoolSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorBackendPoolSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__326414ea10b6cc19d6761adbf796b71ae51aca48995301f210799b93071e3565)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FrontdoorBackendPoolSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4b9c13d375ecf5d9f8fb30b33d3213fbeb79049d29a732636bdd7b0e61dcb1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FrontdoorBackendPoolSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f9b45f5d104e0a035a6313ef89933d4b66879aeace4f52d6966e7bb9b884cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d62584135bd0a35bc53507da87c08aa2b73a2f7c35b27b37b9eacc798deccc22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1b2acbdb128249cd64a4339ee23e8495fad59c118e8b97e5bb25d7cefe19457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e12abb5b6f2d0c73fcdad552eaa9207d6073425f592cc08ecd71823cae681fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FrontdoorBackendPoolSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorBackendPoolSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10c6925bc39727679e139d40e8718f513d6c6160471c230a7b8027a0c485c861)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackendPoolsSendReceiveTimeoutSeconds")
    def reset_backend_pools_send_receive_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendPoolsSendReceiveTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="backendPoolsSendReceiveTimeoutSecondsInput")
    def backend_pools_send_receive_timeout_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backendPoolsSendReceiveTimeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceBackendPoolsCertificateNameCheckInput")
    def enforce_backend_pools_certificate_name_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceBackendPoolsCertificateNameCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolsSendReceiveTimeoutSeconds")
    def backend_pools_send_receive_timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backendPoolsSendReceiveTimeoutSeconds"))

    @backend_pools_send_receive_timeout_seconds.setter
    def backend_pools_send_receive_timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec91440604f610357e659f60225168133e53d5058fe643e6dc56c1f74ed034e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendPoolsSendReceiveTimeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceBackendPoolsCertificateNameCheck")
    def enforce_backend_pools_certificate_name_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforceBackendPoolsCertificateNameCheck"))

    @enforce_backend_pools_certificate_name_check.setter
    def enforce_backend_pools_certificate_name_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e5a7f04119309149dfabb818e69bde2206ca89888089c5f0e10fc4ccce4430a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceBackendPoolsCertificateNameCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d775feca8e323c2d8f3cc02894ab1826528a4170f09b513b5afa7b50c971d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backend_pool": "backendPool",
        "backend_pool_health_probe": "backendPoolHealthProbe",
        "backend_pool_load_balancing": "backendPoolLoadBalancing",
        "frontend_endpoint": "frontendEndpoint",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "routing_rule": "routingRule",
        "backend_pool_settings": "backendPoolSettings",
        "friendly_name": "friendlyName",
        "id": "id",
        "load_balancer_enabled": "loadBalancerEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class FrontdoorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backend_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPool, typing.Dict[builtins.str, typing.Any]]]],
        backend_pool_health_probe: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolHealthProbe, typing.Dict[builtins.str, typing.Any]]]],
        backend_pool_load_balancing: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolLoadBalancing, typing.Dict[builtins.str, typing.Any]]]],
        frontend_endpoint: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorFrontendEndpoint", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        resource_group_name: builtins.str,
        routing_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FrontdoorRoutingRule", typing.Dict[builtins.str, typing.Any]]]],
        backend_pool_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FrontdoorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backend_pool: backend_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool Frontdoor#backend_pool}
        :param backend_pool_health_probe: backend_pool_health_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_health_probe Frontdoor#backend_pool_health_probe}
        :param backend_pool_load_balancing: backend_pool_load_balancing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_load_balancing Frontdoor#backend_pool_load_balancing}
        :param frontend_endpoint: frontend_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#frontend_endpoint Frontdoor#frontend_endpoint}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#resource_group_name Frontdoor#resource_group_name}.
        :param routing_rule: routing_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#routing_rule Frontdoor#routing_rule}
        :param backend_pool_settings: backend_pool_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_settings Frontdoor#backend_pool_settings}
        :param friendly_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#friendly_name Frontdoor#friendly_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#id Frontdoor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#load_balancer_enabled Frontdoor#load_balancer_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#tags Frontdoor#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#timeouts Frontdoor#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = FrontdoorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d11f5516722bb193798b2863c342812738cb46253aff2415f1c0806d27a399f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backend_pool", value=backend_pool, expected_type=type_hints["backend_pool"])
            check_type(argname="argument backend_pool_health_probe", value=backend_pool_health_probe, expected_type=type_hints["backend_pool_health_probe"])
            check_type(argname="argument backend_pool_load_balancing", value=backend_pool_load_balancing, expected_type=type_hints["backend_pool_load_balancing"])
            check_type(argname="argument frontend_endpoint", value=frontend_endpoint, expected_type=type_hints["frontend_endpoint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument routing_rule", value=routing_rule, expected_type=type_hints["routing_rule"])
            check_type(argname="argument backend_pool_settings", value=backend_pool_settings, expected_type=type_hints["backend_pool_settings"])
            check_type(argname="argument friendly_name", value=friendly_name, expected_type=type_hints["friendly_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument load_balancer_enabled", value=load_balancer_enabled, expected_type=type_hints["load_balancer_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend_pool": backend_pool,
            "backend_pool_health_probe": backend_pool_health_probe,
            "backend_pool_load_balancing": backend_pool_load_balancing,
            "frontend_endpoint": frontend_endpoint,
            "name": name,
            "resource_group_name": resource_group_name,
            "routing_rule": routing_rule,
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
        if backend_pool_settings is not None:
            self._values["backend_pool_settings"] = backend_pool_settings
        if friendly_name is not None:
            self._values["friendly_name"] = friendly_name
        if id is not None:
            self._values["id"] = id
        if load_balancer_enabled is not None:
            self._values["load_balancer_enabled"] = load_balancer_enabled
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
    def backend_pool(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPool]]:
        '''backend_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool Frontdoor#backend_pool}
        '''
        result = self._values.get("backend_pool")
        assert result is not None, "Required property 'backend_pool' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPool]], result)

    @builtins.property
    def backend_pool_health_probe(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolHealthProbe]]:
        '''backend_pool_health_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_health_probe Frontdoor#backend_pool_health_probe}
        '''
        result = self._values.get("backend_pool_health_probe")
        assert result is not None, "Required property 'backend_pool_health_probe' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolHealthProbe]], result)

    @builtins.property
    def backend_pool_load_balancing(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolLoadBalancing]]:
        '''backend_pool_load_balancing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_load_balancing Frontdoor#backend_pool_load_balancing}
        '''
        result = self._values.get("backend_pool_load_balancing")
        assert result is not None, "Required property 'backend_pool_load_balancing' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolLoadBalancing]], result)

    @builtins.property
    def frontend_endpoint(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorFrontendEndpoint"]]:
        '''frontend_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#frontend_endpoint Frontdoor#frontend_endpoint}
        '''
        result = self._values.get("frontend_endpoint")
        assert result is not None, "Required property 'frontend_endpoint' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorFrontendEndpoint"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#resource_group_name Frontdoor#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routing_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorRoutingRule"]]:
        '''routing_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#routing_rule Frontdoor#routing_rule}
        '''
        result = self._values.get("routing_rule")
        assert result is not None, "Required property 'routing_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FrontdoorRoutingRule"]], result)

    @builtins.property
    def backend_pool_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolSettings]]]:
        '''backend_pool_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_settings Frontdoor#backend_pool_settings}
        '''
        result = self._values.get("backend_pool_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolSettings]]], result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#friendly_name Frontdoor#friendly_name}.'''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#id Frontdoor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#load_balancer_enabled Frontdoor#load_balancer_enabled}.'''
        result = self._values.get("load_balancer_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#tags Frontdoor#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FrontdoorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#timeouts Frontdoor#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FrontdoorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorExplicitResourceOrder",
    jsii_struct_bases=[],
    name_mapping={},
)
class FrontdoorExplicitResourceOrder:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorExplicitResourceOrder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorExplicitResourceOrderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorExplicitResourceOrderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__510ce3702f062e5774b4b683bb50bfca8118105647b8b6234820a0b172768d9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FrontdoorExplicitResourceOrderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16800623fe81ca7e72879c4e63707a3691d16bdcd434f64d8cff40106409a9ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FrontdoorExplicitResourceOrderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67eb9c21444b331d1015e2119ef70ff390601d13b4ff712726a63cefe83da9d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4276c3d75f4bff4dbb9228b68a6450a0562c94de9f93bccfb2a917c45efa4e35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30604151c8ae585f2b618921fc60366c99887159fb5c8642d679a43d55e73cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FrontdoorExplicitResourceOrderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorExplicitResourceOrderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04c8905fef552043199714f17d3f1d5e33644bfde32b6ff74ed9115bfad5e415)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="backendPoolHealthProbeIds")
    def backend_pool_health_probe_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backendPoolHealthProbeIds"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolIds")
    def backend_pool_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backendPoolIds"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolLoadBalancingIds")
    def backend_pool_load_balancing_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backendPoolLoadBalancingIds"))

    @builtins.property
    @jsii.member(jsii_name="frontendEndpointIds")
    def frontend_endpoint_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "frontendEndpointIds"))

    @builtins.property
    @jsii.member(jsii_name="routingRuleIds")
    def routing_rule_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "routingRuleIds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FrontdoorExplicitResourceOrder]:
        return typing.cast(typing.Optional[FrontdoorExplicitResourceOrder], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FrontdoorExplicitResourceOrder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7eb2754715dcebe3d68a15a69fe651d441aaee32c95a4fe86810f31f5cedb1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorFrontendEndpoint",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "name": "name",
        "session_affinity_enabled": "sessionAffinityEnabled",
        "session_affinity_ttl_seconds": "sessionAffinityTtlSeconds",
        "web_application_firewall_policy_link_id": "webApplicationFirewallPolicyLinkId",
    },
)
class FrontdoorFrontendEndpoint:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        name: builtins.str,
        session_affinity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_affinity_ttl_seconds: typing.Optional[jsii.Number] = None,
        web_application_firewall_policy_link_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#host_name Frontdoor#host_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.
        :param session_affinity_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#session_affinity_enabled Frontdoor#session_affinity_enabled}.
        :param session_affinity_ttl_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#session_affinity_ttl_seconds Frontdoor#session_affinity_ttl_seconds}.
        :param web_application_firewall_policy_link_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#web_application_firewall_policy_link_id Frontdoor#web_application_firewall_policy_link_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abd6b38593b789b6c46708803c3bbb9e6653f42e75778a8573a26d05327f3ad)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument session_affinity_enabled", value=session_affinity_enabled, expected_type=type_hints["session_affinity_enabled"])
            check_type(argname="argument session_affinity_ttl_seconds", value=session_affinity_ttl_seconds, expected_type=type_hints["session_affinity_ttl_seconds"])
            check_type(argname="argument web_application_firewall_policy_link_id", value=web_application_firewall_policy_link_id, expected_type=type_hints["web_application_firewall_policy_link_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
            "name": name,
        }
        if session_affinity_enabled is not None:
            self._values["session_affinity_enabled"] = session_affinity_enabled
        if session_affinity_ttl_seconds is not None:
            self._values["session_affinity_ttl_seconds"] = session_affinity_ttl_seconds
        if web_application_firewall_policy_link_id is not None:
            self._values["web_application_firewall_policy_link_id"] = web_application_firewall_policy_link_id

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#host_name Frontdoor#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_affinity_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#session_affinity_enabled Frontdoor#session_affinity_enabled}.'''
        result = self._values.get("session_affinity_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_affinity_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#session_affinity_ttl_seconds Frontdoor#session_affinity_ttl_seconds}.'''
        result = self._values.get("session_affinity_ttl_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def web_application_firewall_policy_link_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#web_application_firewall_policy_link_id Frontdoor#web_application_firewall_policy_link_id}.'''
        result = self._values.get("web_application_firewall_policy_link_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorFrontendEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorFrontendEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorFrontendEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b46bbc80dfeeba610b7563a39dd54c9f97361a471cf929478649ddc6930e03bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FrontdoorFrontendEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f234e23ddc50b3b25533f2a99435c8689112095b1ca0e1b6a536240e9f9bd20a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FrontdoorFrontendEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e3f3d654a35ec2388cb644eec9c136dbc467b46de7e434f5e82be510b10a63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__493533be24943b5b4e955c3322ecf727e92069abd65f52dd897d6afd6589962e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c889b74a1bf17eff03b235b7ced2230a11730586f6f95f29c6d89d77a4ce1361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorFrontendEndpoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorFrontendEndpoint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorFrontendEndpoint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da55069c63644546a335f4e5be6e21153331fe08f7f77eb9f37522cc5bdc06fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FrontdoorFrontendEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorFrontendEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e78bed75875a40be4e91ef0502bb9b39a86fa025f6a728f53e91194adee1008)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSessionAffinityEnabled")
    def reset_session_affinity_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinityEnabled", []))

    @jsii.member(jsii_name="resetSessionAffinityTtlSeconds")
    def reset_session_affinity_ttl_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinityTtlSeconds", []))

    @jsii.member(jsii_name="resetWebApplicationFirewallPolicyLinkId")
    def reset_web_application_firewall_policy_link_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebApplicationFirewallPolicyLinkId", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityEnabledInput")
    def session_affinity_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sessionAffinityEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityTtlSecondsInput")
    def session_affinity_ttl_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionAffinityTtlSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="webApplicationFirewallPolicyLinkIdInput")
    def web_application_firewall_policy_link_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webApplicationFirewallPolicyLinkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f5e9ae6540d0d5e5bc4abc7dc0f61cf85a1575ff6fac0ec4bcc59c469294fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b1f0bb8893b1b6f2b23b7956abb53ecc29d615648d10c2ee277e6f79fcf5a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityEnabled")
    def session_affinity_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sessionAffinityEnabled"))

    @session_affinity_enabled.setter
    def session_affinity_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fbab8676c5870293008b26a607f08a2de5c7eeb9eb3531752e3ba873a642fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinityEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityTtlSeconds")
    def session_affinity_ttl_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionAffinityTtlSeconds"))

    @session_affinity_ttl_seconds.setter
    def session_affinity_ttl_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fc738f1f5643b56e28bc130d04317e44f0ca8f1fd50afcfdce14d729c3582f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinityTtlSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webApplicationFirewallPolicyLinkId")
    def web_application_firewall_policy_link_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webApplicationFirewallPolicyLinkId"))

    @web_application_firewall_policy_link_id.setter
    def web_application_firewall_policy_link_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604d54a2c0a01793bcaf3e25cdbce274aa6d7395d699b28ba191b3dc1caa8cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webApplicationFirewallPolicyLinkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorFrontendEndpoint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorFrontendEndpoint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorFrontendEndpoint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d037381a512e8aa8cbc551cf1dabf35547161cec111dcd55407dc8c654132e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorRoutingRule",
    jsii_struct_bases=[],
    name_mapping={
        "accepted_protocols": "acceptedProtocols",
        "frontend_endpoints": "frontendEndpoints",
        "name": "name",
        "patterns_to_match": "patternsToMatch",
        "enabled": "enabled",
        "forwarding_configuration": "forwardingConfiguration",
        "redirect_configuration": "redirectConfiguration",
    },
)
class FrontdoorRoutingRule:
    def __init__(
        self,
        *,
        accepted_protocols: typing.Sequence[builtins.str],
        frontend_endpoints: typing.Sequence[builtins.str],
        name: builtins.str,
        patterns_to_match: typing.Sequence[builtins.str],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarding_configuration: typing.Optional[typing.Union["FrontdoorRoutingRuleForwardingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect_configuration: typing.Optional[typing.Union["FrontdoorRoutingRuleRedirectConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param accepted_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#accepted_protocols Frontdoor#accepted_protocols}.
        :param frontend_endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#frontend_endpoints Frontdoor#frontend_endpoints}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.
        :param patterns_to_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#patterns_to_match Frontdoor#patterns_to_match}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#enabled Frontdoor#enabled}.
        :param forwarding_configuration: forwarding_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#forwarding_configuration Frontdoor#forwarding_configuration}
        :param redirect_configuration: redirect_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#redirect_configuration Frontdoor#redirect_configuration}
        '''
        if isinstance(forwarding_configuration, dict):
            forwarding_configuration = FrontdoorRoutingRuleForwardingConfiguration(**forwarding_configuration)
        if isinstance(redirect_configuration, dict):
            redirect_configuration = FrontdoorRoutingRuleRedirectConfiguration(**redirect_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d247fdfeb116cecde593bdf26fed2ce174a87874030d4952a0e21e0a464a8c38)
            check_type(argname="argument accepted_protocols", value=accepted_protocols, expected_type=type_hints["accepted_protocols"])
            check_type(argname="argument frontend_endpoints", value=frontend_endpoints, expected_type=type_hints["frontend_endpoints"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument patterns_to_match", value=patterns_to_match, expected_type=type_hints["patterns_to_match"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument forwarding_configuration", value=forwarding_configuration, expected_type=type_hints["forwarding_configuration"])
            check_type(argname="argument redirect_configuration", value=redirect_configuration, expected_type=type_hints["redirect_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accepted_protocols": accepted_protocols,
            "frontend_endpoints": frontend_endpoints,
            "name": name,
            "patterns_to_match": patterns_to_match,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if forwarding_configuration is not None:
            self._values["forwarding_configuration"] = forwarding_configuration
        if redirect_configuration is not None:
            self._values["redirect_configuration"] = redirect_configuration

    @builtins.property
    def accepted_protocols(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#accepted_protocols Frontdoor#accepted_protocols}.'''
        result = self._values.get("accepted_protocols")
        assert result is not None, "Required property 'accepted_protocols' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def frontend_endpoints(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#frontend_endpoints Frontdoor#frontend_endpoints}.'''
        result = self._values.get("frontend_endpoints")
        assert result is not None, "Required property 'frontend_endpoints' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#name Frontdoor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def patterns_to_match(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#patterns_to_match Frontdoor#patterns_to_match}.'''
        result = self._values.get("patterns_to_match")
        assert result is not None, "Required property 'patterns_to_match' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#enabled Frontdoor#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forwarding_configuration(
        self,
    ) -> typing.Optional["FrontdoorRoutingRuleForwardingConfiguration"]:
        '''forwarding_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#forwarding_configuration Frontdoor#forwarding_configuration}
        '''
        result = self._values.get("forwarding_configuration")
        return typing.cast(typing.Optional["FrontdoorRoutingRuleForwardingConfiguration"], result)

    @builtins.property
    def redirect_configuration(
        self,
    ) -> typing.Optional["FrontdoorRoutingRuleRedirectConfiguration"]:
        '''redirect_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#redirect_configuration Frontdoor#redirect_configuration}
        '''
        result = self._values.get("redirect_configuration")
        return typing.cast(typing.Optional["FrontdoorRoutingRuleRedirectConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorRoutingRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorRoutingRuleForwardingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "backend_pool_name": "backendPoolName",
        "cache_duration": "cacheDuration",
        "cache_enabled": "cacheEnabled",
        "cache_query_parameters": "cacheQueryParameters",
        "cache_query_parameter_strip_directive": "cacheQueryParameterStripDirective",
        "cache_use_dynamic_compression": "cacheUseDynamicCompression",
        "custom_forwarding_path": "customForwardingPath",
        "forwarding_protocol": "forwardingProtocol",
    },
)
class FrontdoorRoutingRuleForwardingConfiguration:
    def __init__(
        self,
        *,
        backend_pool_name: builtins.str,
        cache_duration: typing.Optional[builtins.str] = None,
        cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cache_query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_query_parameter_strip_directive: typing.Optional[builtins.str] = None,
        cache_use_dynamic_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_forwarding_path: typing.Optional[builtins.str] = None,
        forwarding_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_name Frontdoor#backend_pool_name}.
        :param cache_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_duration Frontdoor#cache_duration}.
        :param cache_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_enabled Frontdoor#cache_enabled}.
        :param cache_query_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_query_parameters Frontdoor#cache_query_parameters}.
        :param cache_query_parameter_strip_directive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_query_parameter_strip_directive Frontdoor#cache_query_parameter_strip_directive}.
        :param cache_use_dynamic_compression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_use_dynamic_compression Frontdoor#cache_use_dynamic_compression}.
        :param custom_forwarding_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_forwarding_path Frontdoor#custom_forwarding_path}.
        :param forwarding_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#forwarding_protocol Frontdoor#forwarding_protocol}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b693881f445f86d4d4f86f49c9fa47bdd385d4b0c90652d137e3a3b66627308c)
            check_type(argname="argument backend_pool_name", value=backend_pool_name, expected_type=type_hints["backend_pool_name"])
            check_type(argname="argument cache_duration", value=cache_duration, expected_type=type_hints["cache_duration"])
            check_type(argname="argument cache_enabled", value=cache_enabled, expected_type=type_hints["cache_enabled"])
            check_type(argname="argument cache_query_parameters", value=cache_query_parameters, expected_type=type_hints["cache_query_parameters"])
            check_type(argname="argument cache_query_parameter_strip_directive", value=cache_query_parameter_strip_directive, expected_type=type_hints["cache_query_parameter_strip_directive"])
            check_type(argname="argument cache_use_dynamic_compression", value=cache_use_dynamic_compression, expected_type=type_hints["cache_use_dynamic_compression"])
            check_type(argname="argument custom_forwarding_path", value=custom_forwarding_path, expected_type=type_hints["custom_forwarding_path"])
            check_type(argname="argument forwarding_protocol", value=forwarding_protocol, expected_type=type_hints["forwarding_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend_pool_name": backend_pool_name,
        }
        if cache_duration is not None:
            self._values["cache_duration"] = cache_duration
        if cache_enabled is not None:
            self._values["cache_enabled"] = cache_enabled
        if cache_query_parameters is not None:
            self._values["cache_query_parameters"] = cache_query_parameters
        if cache_query_parameter_strip_directive is not None:
            self._values["cache_query_parameter_strip_directive"] = cache_query_parameter_strip_directive
        if cache_use_dynamic_compression is not None:
            self._values["cache_use_dynamic_compression"] = cache_use_dynamic_compression
        if custom_forwarding_path is not None:
            self._values["custom_forwarding_path"] = custom_forwarding_path
        if forwarding_protocol is not None:
            self._values["forwarding_protocol"] = forwarding_protocol

    @builtins.property
    def backend_pool_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_name Frontdoor#backend_pool_name}.'''
        result = self._values.get("backend_pool_name")
        assert result is not None, "Required property 'backend_pool_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cache_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_duration Frontdoor#cache_duration}.'''
        result = self._values.get("cache_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_enabled Frontdoor#cache_enabled}.'''
        result = self._values.get("cache_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cache_query_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_query_parameters Frontdoor#cache_query_parameters}.'''
        result = self._values.get("cache_query_parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_query_parameter_strip_directive(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_query_parameter_strip_directive Frontdoor#cache_query_parameter_strip_directive}.'''
        result = self._values.get("cache_query_parameter_strip_directive")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_use_dynamic_compression(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_use_dynamic_compression Frontdoor#cache_use_dynamic_compression}.'''
        result = self._values.get("cache_use_dynamic_compression")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_forwarding_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_forwarding_path Frontdoor#custom_forwarding_path}.'''
        result = self._values.get("custom_forwarding_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forwarding_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#forwarding_protocol Frontdoor#forwarding_protocol}.'''
        result = self._values.get("forwarding_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorRoutingRuleForwardingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorRoutingRuleForwardingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorRoutingRuleForwardingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96838071c367ab04ab5f4a371937b614034c8f3b84e46a952095c715a8b004ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCacheDuration")
    def reset_cache_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheDuration", []))

    @jsii.member(jsii_name="resetCacheEnabled")
    def reset_cache_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheEnabled", []))

    @jsii.member(jsii_name="resetCacheQueryParameters")
    def reset_cache_query_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheQueryParameters", []))

    @jsii.member(jsii_name="resetCacheQueryParameterStripDirective")
    def reset_cache_query_parameter_strip_directive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheQueryParameterStripDirective", []))

    @jsii.member(jsii_name="resetCacheUseDynamicCompression")
    def reset_cache_use_dynamic_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheUseDynamicCompression", []))

    @jsii.member(jsii_name="resetCustomForwardingPath")
    def reset_custom_forwarding_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomForwardingPath", []))

    @jsii.member(jsii_name="resetForwardingProtocol")
    def reset_forwarding_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardingProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="backendPoolNameInput")
    def backend_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheDurationInput")
    def cache_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheEnabledInput")
    def cache_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cacheEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheQueryParametersInput")
    def cache_query_parameters_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cacheQueryParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheQueryParameterStripDirectiveInput")
    def cache_query_parameter_strip_directive_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheQueryParameterStripDirectiveInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheUseDynamicCompressionInput")
    def cache_use_dynamic_compression_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cacheUseDynamicCompressionInput"))

    @builtins.property
    @jsii.member(jsii_name="customForwardingPathInput")
    def custom_forwarding_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customForwardingPathInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingProtocolInput")
    def forwarding_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardingProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolName")
    def backend_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendPoolName"))

    @backend_pool_name.setter
    def backend_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5fc340206852f630f6879b81408b39b1bdba16e88e36301363600a48a22fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheDuration")
    def cache_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheDuration"))

    @cache_duration.setter
    def cache_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e50ef31f6648f85ad0beea8074c264397b364175ac99cf2a32b68471e43f3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheEnabled")
    def cache_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cacheEnabled"))

    @cache_enabled.setter
    def cache_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636d232e37d405568fdfadf371eeda7546ffe5a43a23f09c08ac9894ebc9e28a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheQueryParameters")
    def cache_query_parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cacheQueryParameters"))

    @cache_query_parameters.setter
    def cache_query_parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6496606f2cb415126b29a384d09d6f0714f8e38d27a96a660446e35f360bfd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheQueryParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheQueryParameterStripDirective")
    def cache_query_parameter_strip_directive(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheQueryParameterStripDirective"))

    @cache_query_parameter_strip_directive.setter
    def cache_query_parameter_strip_directive(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fb01975cb7cfe0573d3a3308ec9b35eb60665f09477169d40552418c343bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheQueryParameterStripDirective", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheUseDynamicCompression")
    def cache_use_dynamic_compression(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cacheUseDynamicCompression"))

    @cache_use_dynamic_compression.setter
    def cache_use_dynamic_compression(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718a8a5289311064d4410851d941c1ea9f1652e0f89e91a4215273be6d32011b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheUseDynamicCompression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customForwardingPath")
    def custom_forwarding_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customForwardingPath"))

    @custom_forwarding_path.setter
    def custom_forwarding_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b451098c7c05ada64ca627f925881e48b2da955b5b8f1702ecb7e19f8a2823b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customForwardingPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingProtocol")
    def forwarding_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingProtocol"))

    @forwarding_protocol.setter
    def forwarding_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9817fb46827c4497203a84c4351ef815d9d183aa5a7503c2763149b0137ef075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FrontdoorRoutingRuleForwardingConfiguration]:
        return typing.cast(typing.Optional[FrontdoorRoutingRuleForwardingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FrontdoorRoutingRuleForwardingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df02452aa99caa8b8d1cdda1e877ff1c44c8cc96c34fb7a8cf90ae07dabf396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FrontdoorRoutingRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorRoutingRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1906be6682c60e871b94ce16a3d75cbea922f8c487a1feb71211883a049d470)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FrontdoorRoutingRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99df99aaec782854295ffa6ecd2e6b4885a95f390636bf603107f438e7d677c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FrontdoorRoutingRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4121f3f65e7be94cb1a440b57c27f4f83edcaf1e2e51c2d1d13524e0ed77ce18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d57b4a1ed203db703199c1651d681e037b2f2c6819b99e4d6766829011eae69e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__455d5346066b74c9abdc416a680ea891cf1a533a87f52b5958f0ea23440a9998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorRoutingRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorRoutingRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorRoutingRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4550775b90de4efe323128170d2eecc7332d02fda025a21eacece6a9f0ddec70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FrontdoorRoutingRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorRoutingRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__696b47c062ca32078ac13a29bcd6732efa92187e0d169701db427583f3e4ef3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putForwardingConfiguration")
    def put_forwarding_configuration(
        self,
        *,
        backend_pool_name: builtins.str,
        cache_duration: typing.Optional[builtins.str] = None,
        cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cache_query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_query_parameter_strip_directive: typing.Optional[builtins.str] = None,
        cache_use_dynamic_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_forwarding_path: typing.Optional[builtins.str] = None,
        forwarding_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#backend_pool_name Frontdoor#backend_pool_name}.
        :param cache_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_duration Frontdoor#cache_duration}.
        :param cache_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_enabled Frontdoor#cache_enabled}.
        :param cache_query_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_query_parameters Frontdoor#cache_query_parameters}.
        :param cache_query_parameter_strip_directive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_query_parameter_strip_directive Frontdoor#cache_query_parameter_strip_directive}.
        :param cache_use_dynamic_compression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#cache_use_dynamic_compression Frontdoor#cache_use_dynamic_compression}.
        :param custom_forwarding_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_forwarding_path Frontdoor#custom_forwarding_path}.
        :param forwarding_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#forwarding_protocol Frontdoor#forwarding_protocol}.
        '''
        value = FrontdoorRoutingRuleForwardingConfiguration(
            backend_pool_name=backend_pool_name,
            cache_duration=cache_duration,
            cache_enabled=cache_enabled,
            cache_query_parameters=cache_query_parameters,
            cache_query_parameter_strip_directive=cache_query_parameter_strip_directive,
            cache_use_dynamic_compression=cache_use_dynamic_compression,
            custom_forwarding_path=custom_forwarding_path,
            forwarding_protocol=forwarding_protocol,
        )

        return typing.cast(None, jsii.invoke(self, "putForwardingConfiguration", [value]))

    @jsii.member(jsii_name="putRedirectConfiguration")
    def put_redirect_configuration(
        self,
        *,
        redirect_protocol: builtins.str,
        redirect_type: builtins.str,
        custom_fragment: typing.Optional[builtins.str] = None,
        custom_host: typing.Optional[builtins.str] = None,
        custom_path: typing.Optional[builtins.str] = None,
        custom_query_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param redirect_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#redirect_protocol Frontdoor#redirect_protocol}.
        :param redirect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#redirect_type Frontdoor#redirect_type}.
        :param custom_fragment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_fragment Frontdoor#custom_fragment}.
        :param custom_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_host Frontdoor#custom_host}.
        :param custom_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_path Frontdoor#custom_path}.
        :param custom_query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_query_string Frontdoor#custom_query_string}.
        '''
        value = FrontdoorRoutingRuleRedirectConfiguration(
            redirect_protocol=redirect_protocol,
            redirect_type=redirect_type,
            custom_fragment=custom_fragment,
            custom_host=custom_host,
            custom_path=custom_path,
            custom_query_string=custom_query_string,
        )

        return typing.cast(None, jsii.invoke(self, "putRedirectConfiguration", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetForwardingConfiguration")
    def reset_forwarding_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardingConfiguration", []))

    @jsii.member(jsii_name="resetRedirectConfiguration")
    def reset_redirect_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="forwardingConfiguration")
    def forwarding_configuration(
        self,
    ) -> FrontdoorRoutingRuleForwardingConfigurationOutputReference:
        return typing.cast(FrontdoorRoutingRuleForwardingConfigurationOutputReference, jsii.get(self, "forwardingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="redirectConfiguration")
    def redirect_configuration(
        self,
    ) -> "FrontdoorRoutingRuleRedirectConfigurationOutputReference":
        return typing.cast("FrontdoorRoutingRuleRedirectConfigurationOutputReference", jsii.get(self, "redirectConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="acceptedProtocolsInput")
    def accepted_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "acceptedProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingConfigurationInput")
    def forwarding_configuration_input(
        self,
    ) -> typing.Optional[FrontdoorRoutingRuleForwardingConfiguration]:
        return typing.cast(typing.Optional[FrontdoorRoutingRuleForwardingConfiguration], jsii.get(self, "forwardingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendEndpointsInput")
    def frontend_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "frontendEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="patternsToMatchInput")
    def patterns_to_match_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "patternsToMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectConfigurationInput")
    def redirect_configuration_input(
        self,
    ) -> typing.Optional["FrontdoorRoutingRuleRedirectConfiguration"]:
        return typing.cast(typing.Optional["FrontdoorRoutingRuleRedirectConfiguration"], jsii.get(self, "redirectConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="acceptedProtocols")
    def accepted_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "acceptedProtocols"))

    @accepted_protocols.setter
    def accepted_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd8731efc39ace697b83731770c66b1ffa6360d7252c9ad8a28c23c20426f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptedProtocols", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__701d1376444ce88020fcc7975c065e34e8f6831173ad4ee16d2934e3bb948da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendEndpoints")
    def frontend_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "frontendEndpoints"))

    @frontend_endpoints.setter
    def frontend_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5ef21f177b50bb3771036fc8ebe4fe502141840048206c0fd458d3a41618a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c01e770893f8af8540626f0bb2ea9e3b9d880708b1c9d4a4ecf444963a61d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternsToMatch")
    def patterns_to_match(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "patternsToMatch"))

    @patterns_to_match.setter
    def patterns_to_match(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b846359a78a8819bd1aec53636eac2a113dbdc016e000b795d002c08c614bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patternsToMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorRoutingRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorRoutingRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorRoutingRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1c450c5e71aa98153094b586dcba15d01adacb4e19556ec5481a2cc2a94360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorRoutingRuleRedirectConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "redirect_protocol": "redirectProtocol",
        "redirect_type": "redirectType",
        "custom_fragment": "customFragment",
        "custom_host": "customHost",
        "custom_path": "customPath",
        "custom_query_string": "customQueryString",
    },
)
class FrontdoorRoutingRuleRedirectConfiguration:
    def __init__(
        self,
        *,
        redirect_protocol: builtins.str,
        redirect_type: builtins.str,
        custom_fragment: typing.Optional[builtins.str] = None,
        custom_host: typing.Optional[builtins.str] = None,
        custom_path: typing.Optional[builtins.str] = None,
        custom_query_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param redirect_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#redirect_protocol Frontdoor#redirect_protocol}.
        :param redirect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#redirect_type Frontdoor#redirect_type}.
        :param custom_fragment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_fragment Frontdoor#custom_fragment}.
        :param custom_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_host Frontdoor#custom_host}.
        :param custom_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_path Frontdoor#custom_path}.
        :param custom_query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_query_string Frontdoor#custom_query_string}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f449a4c4d2636dfa8dd2499a00a2bef63af21a467fe30d2472f7f3ddd72e4eac)
            check_type(argname="argument redirect_protocol", value=redirect_protocol, expected_type=type_hints["redirect_protocol"])
            check_type(argname="argument redirect_type", value=redirect_type, expected_type=type_hints["redirect_type"])
            check_type(argname="argument custom_fragment", value=custom_fragment, expected_type=type_hints["custom_fragment"])
            check_type(argname="argument custom_host", value=custom_host, expected_type=type_hints["custom_host"])
            check_type(argname="argument custom_path", value=custom_path, expected_type=type_hints["custom_path"])
            check_type(argname="argument custom_query_string", value=custom_query_string, expected_type=type_hints["custom_query_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "redirect_protocol": redirect_protocol,
            "redirect_type": redirect_type,
        }
        if custom_fragment is not None:
            self._values["custom_fragment"] = custom_fragment
        if custom_host is not None:
            self._values["custom_host"] = custom_host
        if custom_path is not None:
            self._values["custom_path"] = custom_path
        if custom_query_string is not None:
            self._values["custom_query_string"] = custom_query_string

    @builtins.property
    def redirect_protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#redirect_protocol Frontdoor#redirect_protocol}.'''
        result = self._values.get("redirect_protocol")
        assert result is not None, "Required property 'redirect_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def redirect_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#redirect_type Frontdoor#redirect_type}.'''
        result = self._values.get("redirect_type")
        assert result is not None, "Required property 'redirect_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_fragment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_fragment Frontdoor#custom_fragment}.'''
        result = self._values.get("custom_fragment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_host Frontdoor#custom_host}.'''
        result = self._values.get("custom_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_path Frontdoor#custom_path}.'''
        result = self._values.get("custom_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_query_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#custom_query_string Frontdoor#custom_query_string}.'''
        result = self._values.get("custom_query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorRoutingRuleRedirectConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorRoutingRuleRedirectConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorRoutingRuleRedirectConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e3316bb683e2ce53cfcdc60b29cb4ae8c3537cabe0c2bd54b9585b140e4a70e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomFragment")
    def reset_custom_fragment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomFragment", []))

    @jsii.member(jsii_name="resetCustomHost")
    def reset_custom_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomHost", []))

    @jsii.member(jsii_name="resetCustomPath")
    def reset_custom_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPath", []))

    @jsii.member(jsii_name="resetCustomQueryString")
    def reset_custom_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomQueryString", []))

    @builtins.property
    @jsii.member(jsii_name="customFragmentInput")
    def custom_fragment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customFragmentInput"))

    @builtins.property
    @jsii.member(jsii_name="customHostInput")
    def custom_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customHostInput"))

    @builtins.property
    @jsii.member(jsii_name="customPathInput")
    def custom_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customPathInput"))

    @builtins.property
    @jsii.member(jsii_name="customQueryStringInput")
    def custom_query_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customQueryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectProtocolInput")
    def redirect_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectTypeInput")
    def redirect_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customFragment")
    def custom_fragment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customFragment"))

    @custom_fragment.setter
    def custom_fragment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4853a41c528bfcfa0e124651e58ae0fad934f5b3cbb8526261421980eccd60c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customFragment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customHost")
    def custom_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customHost"))

    @custom_host.setter
    def custom_host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8f08a21680f3331e314b7756946525ad1856b1cc496e425cdc3268895d0175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPath")
    def custom_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customPath"))

    @custom_path.setter
    def custom_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6973bb1bbff1a0055654895c21aa5ef99e0c16ee96debd01d0a1d75cc16429d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customQueryString")
    def custom_query_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customQueryString"))

    @custom_query_string.setter
    def custom_query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d8344fd9c05ab24c33ee66fbbb11982f6b793b54abfa08082a13736b3325c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customQueryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectProtocol")
    def redirect_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectProtocol"))

    @redirect_protocol.setter
    def redirect_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1bf3e6f4123092c3f42ee5fc452356f90a9ffb2e60dc0e45b967a1236e3d1b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectType")
    def redirect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectType"))

    @redirect_type.setter
    def redirect_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d3776edbae4db6650ac23da14a770a8b1cf7c3b5a236fa50b116ab17b65d8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FrontdoorRoutingRuleRedirectConfiguration]:
        return typing.cast(typing.Optional[FrontdoorRoutingRuleRedirectConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FrontdoorRoutingRuleRedirectConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a023943a09c76e657b4a1dc2290203db1e42f5cbda8726e4989fe114dc7b269b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class FrontdoorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#create Frontdoor#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#delete Frontdoor#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#read Frontdoor#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#update Frontdoor#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b04eafe27090d8db51d586a509c36e7216b0c91c6f56d166506b8e83bed62d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#create Frontdoor#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#delete Frontdoor#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#read Frontdoor#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor#update Frontdoor#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoor.FrontdoorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a584200a3458a215cbf271f4e554339e9605860f5d8b48ba40925a8371905fc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd7aa9a12bbbf4ffb8f5b0f7e612e76a7ee5d70506bfbf46871f2e666040c3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9387cac33d7b65410e7b6018ce152522ae63c05a7be4e44b47ded99abb23615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb8bed73bae47a96c47f0fd52e1e9b79d2fdc921b16cc40756ad12a756f840a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec26de00ae3fc9e93c01f41ef99b53cc156882e90e4bfc38dfe2556084e522a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ff47a7f6b459315f31345c1d3055e2f5101ea8ebf3765f1d637766c1883669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Frontdoor",
    "FrontdoorBackendPool",
    "FrontdoorBackendPoolBackend",
    "FrontdoorBackendPoolBackendList",
    "FrontdoorBackendPoolBackendOutputReference",
    "FrontdoorBackendPoolHealthProbe",
    "FrontdoorBackendPoolHealthProbeList",
    "FrontdoorBackendPoolHealthProbeOutputReference",
    "FrontdoorBackendPoolList",
    "FrontdoorBackendPoolLoadBalancing",
    "FrontdoorBackendPoolLoadBalancingList",
    "FrontdoorBackendPoolLoadBalancingOutputReference",
    "FrontdoorBackendPoolOutputReference",
    "FrontdoorBackendPoolSettings",
    "FrontdoorBackendPoolSettingsList",
    "FrontdoorBackendPoolSettingsOutputReference",
    "FrontdoorConfig",
    "FrontdoorExplicitResourceOrder",
    "FrontdoorExplicitResourceOrderList",
    "FrontdoorExplicitResourceOrderOutputReference",
    "FrontdoorFrontendEndpoint",
    "FrontdoorFrontendEndpointList",
    "FrontdoorFrontendEndpointOutputReference",
    "FrontdoorRoutingRule",
    "FrontdoorRoutingRuleForwardingConfiguration",
    "FrontdoorRoutingRuleForwardingConfigurationOutputReference",
    "FrontdoorRoutingRuleList",
    "FrontdoorRoutingRuleOutputReference",
    "FrontdoorRoutingRuleRedirectConfiguration",
    "FrontdoorRoutingRuleRedirectConfigurationOutputReference",
    "FrontdoorTimeouts",
    "FrontdoorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3a46a4c768d7d352f48a58e20c790a039105b2ebcea19b38ef28eddb40b78000(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backend_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPool, typing.Dict[builtins.str, typing.Any]]]],
    backend_pool_health_probe: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolHealthProbe, typing.Dict[builtins.str, typing.Any]]]],
    backend_pool_load_balancing: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolLoadBalancing, typing.Dict[builtins.str, typing.Any]]]],
    frontend_endpoint: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorFrontendEndpoint, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    resource_group_name: builtins.str,
    routing_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorRoutingRule, typing.Dict[builtins.str, typing.Any]]]],
    backend_pool_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FrontdoorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__85964357cb6603d1cb4f53fb91e77f01af1d69507fb5b08849494579543acce5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1eff61cbef45749cd63732a92dbde3378721b1894fcc4f68381cf9cca119a5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6629a5c50038f2d0fcaf8e2249b3cef16cff8bbae9ae0115bb028403abcfcf3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolHealthProbe, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756f5c9f505528e020df5c9c2d0c2aae58b2e38ce5989bffbc0219e06f6e7f72(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolLoadBalancing, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598c843a081037685d799399f92826beb3eeea12f6a085b446808a437e285dff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c8a97d7b73716eaa60f85aad9400f5aab9b2e364f97e6c6406e173247af05c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorFrontendEndpoint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17871732e50df8f12ce1709c8ed30a234b415887acd9a942458765452fbfc40(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorRoutingRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d0ed82978f44c8d7a55aa0372676965040429c892bc2bc848c1e89630f8dee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79241666a4e309960194d9cdd851b68e76aa8c609f2fed8f48d7718f6faa886e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3983be6fba5d8011fbf697132730a191b79e4babf65940f0cf5f33f535e123ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daee6c36c49c347a07e969b81becf56c73333d84fe841fb97807ae0e8a8d3ab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86bd579afd046ef02f26bb74054bd40c70fde424267732b5f61be941e8edd82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776865e51568e769641924d415622417c534296a6cbf871e6750ea2df9807aeb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f359faac6f4f23f294e49156f555fae1614f3c448e705b813f0ea8f4661856(
    *,
    backend: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolBackend, typing.Dict[builtins.str, typing.Any]]]],
    health_probe_name: builtins.str,
    load_balancing_name: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a6389a3f63ef4d2d3cd3366bab752dce980875089b4fa1afab228e5d50450c(
    *,
    address: builtins.str,
    host_header: builtins.str,
    http_port: jsii.Number,
    https_port: jsii.Number,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    priority: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8dccf7ec87f75ac9fd875fc2e31661dcff14219400337038ece63f46488d56f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ff8807cb2f51b404027637c00ddb8ddfbd23b80a6e0dc5d3b72e76054d1757(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8425ca3a3836056070b0b30237b7235ffe3097bef827e5ce5f75df20bbb1c099(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab558ad75339dc4a18f2ef3f68168fe61e3007737e7555e1983bf645f7192265(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9308cb9048f027a2e99cb457d800d2d15558221fce4ccaaf5720a3a0670dc1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d358ebfb1da0ee263c9fd576f451528a575e3d30bea017dc80fdc2a7bdd4b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolBackend]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef288145a14641832ce04e594fab32e910f46ce7ee3e045f8d4095b12ca3f9a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c32efb13b1263b799a2936daa78d0dd4fbd3ed4b103996bcbeed23ecc1f3e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bac2acb6c9cc85015cb70cdd1a138750d84d0f0f716edc2abed9f11d70bae34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91906bcf3ee823215d6ab9109ee1322c54315cbe019b47e4c05535ad885e407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d646ef7ad1ce05bc54032159a0ee52f4a186abad71f151645e299c48f7affa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02aaa1e8e22c969627e92678b8f47bfe3c735293d2ed1aec11c9bacf02da239(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c66a8cd9303f9a5ff63d0b15cd504af72da41e838bec9ab3ba26ca7fc2f497(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597770b5a7458868c9e407a477492302c0f1ad85267dd4b8bcce5c4210000326(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb1dc211010f981a5be54b841f0f12d1e486f47d6132401155b336c789abb75(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolBackend]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14442537f84e99e674c278d7d638509418e4e7400592a2d74baeb650e8708028(
    *,
    name: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    probe_method: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7668bb1d52a2f2d27b703d7753d368ff52ccd3f43fd76953c533e507225772(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e1d2badce026d9543e35c311e1acac6f8f5ba278ccb7aef3e922d7f5d662f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920df4986d716b737467568a68fe7e8aefa601e59b22c1164960cfb65d00d97c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9a815423a137e69eb3129386c431da4bf96efb0444017a91c21d529a292a8e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8858a65b4452d0c825a2a6e2a72ebccecc46b9d8557915585340095312848f59(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1978f9dbf0abaefa54c2e33300f72e006ec572b3d114066c7e1c8760acde7a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolHealthProbe]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a9b5ba01bee655ba03c99bf190812c0c95c5200a18828f0f9236d178464792(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef63d36858f8efb683360d2bbba3f13e4ed7b33594fc5dde0bfc6d353099091(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c09fa5e53564015de2a2f6fa47fa0f99abf1a455c4207000a3ddfb7ab2dc86(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dafb6e94380cb6259bbda9c57503b16d7ac5f13263b39922d103b48d8174599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5759da6623c2b1823430187ffcbf9709e2c7b5864d91e51b91adebeef66d3963(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b050dd08ca6e3563dd96c863b7d7e0a71185bcb9c19617b64e13494afe67642b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22ebb5fd8fb271e55ac90ef5575d45c5147934eb5e92a1eb7a5ceef573f28bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b2e26e5aa89b2b62ac63cf4664ec05529585672ab556e860f07264102979de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolHealthProbe]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25378fd2b0c884e5e5ecf31a2134b07b622fe09929a649417ae1d16125d9dcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135d529e45e2e9f45e6dcafc6129e9ff7a7e2c3df8d3bd2a3e26ae0e5faedd9f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba9b87892a5fffc80fc224e83d3439990a1a752b44df4597ba137d1ae7ae4f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7df4ee27ce0710e5f84bca114b8afa50763ef97c4a796f5df4a270bedcad80(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ee8e18e16b05915b0d63ea0d3dbb48b7f20a0ca092dc03bb9e7e205af3b6a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c905f0f26ce72c5ef541b98e15d236707716a319ec2a8d8f3b38f69f8fd23483(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21ce34d73db8856151da0982afbedcfac3411b4d0c96aacb475bf331fccd9be(
    *,
    name: builtins.str,
    additional_latency_milliseconds: typing.Optional[jsii.Number] = None,
    sample_size: typing.Optional[jsii.Number] = None,
    successful_samples_required: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142ea549aaf0e4fb427dab1ba5798594e1d313c86083cf556c062ec4a08304b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeacc38f589504952a8459516788b8dd25814d86db03b746ae8b9b8badcc8e5d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5defd5389f38ba12df9c163cb8759915e917c0c850af42d2692078fc3de55a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a944bc37b26f6c65b66466ae4280ef93466b2738b42b545aa1a1c3f13e12de48(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0480145695cd71ce4e95d52e5b083d81d55b8f66db7e4b6a46b1ea82be3e5723(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61063313f4286fdc71459a9cca4df296ffe412537364cb9eda2799d8db74f1d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolLoadBalancing]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca1e515448459faae6b42f81f83d046c6dab62f8624c904dcef76044d94f3af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59194fb5a3d0d5f037b0866b2733a7f4a92a2f2cef62b76f3bdbfd8970df471a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b73e9246ba258802b3f632b18afa27b55a8e608f604ed7ba710175fba193f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0cebbec834b839450385b7c2719e43b994a3261ba431f0391f87366b18dbb9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1810c2dcdeff67c2719e255a6438b391ee78182b22b41b56fe022a97192626(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640c857257ac05f8620fad9ea036f9230a5fb2fe4e30240daaf4b15b44b61fc8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolLoadBalancing]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6733d85131963692c4175ea4c0f4ee7776a6c1e979b699802108a5ab8b4b6432(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0deca5aef016df454873c54d23a24db52b563bb5b9e2ea3406ba68d2ca0862(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolBackend, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6eb25bdde5111ac010cecbd3a3c889518f7308b2806390993d0c4607b41385(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1af780c1c38164ca26dd14100099c8fcd7e743819d908f1ba38b3dc86f6da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b8bbd2f5439bff30ed8b43b6ce57b4aec72c04b5663ce9466aa28062771b5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb17c82482ee339664006f57f8ac7a6c624a0cddd8154f178060b3d413b9e104(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042ac0f3f31e16f9a716a856c2f097d2d9e30d6c5fd77f7e2400305f776655c4(
    *,
    enforce_backend_pools_certificate_name_check: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    backend_pools_send_receive_timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__326414ea10b6cc19d6761adbf796b71ae51aca48995301f210799b93071e3565(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4b9c13d375ecf5d9f8fb30b33d3213fbeb79049d29a732636bdd7b0e61dcb1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f9b45f5d104e0a035a6313ef89933d4b66879aeace4f52d6966e7bb9b884cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62584135bd0a35bc53507da87c08aa2b73a2f7c35b27b37b9eacc798deccc22(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b2acbdb128249cd64a4339ee23e8495fad59c118e8b97e5bb25d7cefe19457(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e12abb5b6f2d0c73fcdad552eaa9207d6073425f592cc08ecd71823cae681fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorBackendPoolSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c6925bc39727679e139d40e8718f513d6c6160471c230a7b8027a0c485c861(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec91440604f610357e659f60225168133e53d5058fe643e6dc56c1f74ed034e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5a7f04119309149dfabb818e69bde2206ca89888089c5f0e10fc4ccce4430a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d775feca8e323c2d8f3cc02894ab1826528a4170f09b513b5afa7b50c971d66(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorBackendPoolSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d11f5516722bb193798b2863c342812738cb46253aff2415f1c0806d27a399f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backend_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPool, typing.Dict[builtins.str, typing.Any]]]],
    backend_pool_health_probe: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolHealthProbe, typing.Dict[builtins.str, typing.Any]]]],
    backend_pool_load_balancing: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolLoadBalancing, typing.Dict[builtins.str, typing.Any]]]],
    frontend_endpoint: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorFrontendEndpoint, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    resource_group_name: builtins.str,
    routing_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorRoutingRule, typing.Dict[builtins.str, typing.Any]]]],
    backend_pool_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FrontdoorBackendPoolSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FrontdoorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510ce3702f062e5774b4b683bb50bfca8118105647b8b6234820a0b172768d9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16800623fe81ca7e72879c4e63707a3691d16bdcd434f64d8cff40106409a9ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67eb9c21444b331d1015e2119ef70ff390601d13b4ff712726a63cefe83da9d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4276c3d75f4bff4dbb9228b68a6450a0562c94de9f93bccfb2a917c45efa4e35(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30604151c8ae585f2b618921fc60366c99887159fb5c8642d679a43d55e73cef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c8905fef552043199714f17d3f1d5e33644bfde32b6ff74ed9115bfad5e415(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7eb2754715dcebe3d68a15a69fe651d441aaee32c95a4fe86810f31f5cedb1b(
    value: typing.Optional[FrontdoorExplicitResourceOrder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abd6b38593b789b6c46708803c3bbb9e6653f42e75778a8573a26d05327f3ad(
    *,
    host_name: builtins.str,
    name: builtins.str,
    session_affinity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_affinity_ttl_seconds: typing.Optional[jsii.Number] = None,
    web_application_firewall_policy_link_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46bbc80dfeeba610b7563a39dd54c9f97361a471cf929478649ddc6930e03bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f234e23ddc50b3b25533f2a99435c8689112095b1ca0e1b6a536240e9f9bd20a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e3f3d654a35ec2388cb644eec9c136dbc467b46de7e434f5e82be510b10a63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493533be24943b5b4e955c3322ecf727e92069abd65f52dd897d6afd6589962e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c889b74a1bf17eff03b235b7ced2230a11730586f6f95f29c6d89d77a4ce1361(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da55069c63644546a335f4e5be6e21153331fe08f7f77eb9f37522cc5bdc06fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorFrontendEndpoint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e78bed75875a40be4e91ef0502bb9b39a86fa025f6a728f53e91194adee1008(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f5e9ae6540d0d5e5bc4abc7dc0f61cf85a1575ff6fac0ec4bcc59c469294fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b1f0bb8893b1b6f2b23b7956abb53ecc29d615648d10c2ee277e6f79fcf5a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fbab8676c5870293008b26a607f08a2de5c7eeb9eb3531752e3ba873a642fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fc738f1f5643b56e28bc130d04317e44f0ca8f1fd50afcfdce14d729c3582f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604d54a2c0a01793bcaf3e25cdbce274aa6d7395d699b28ba191b3dc1caa8cb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d037381a512e8aa8cbc551cf1dabf35547161cec111dcd55407dc8c654132e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorFrontendEndpoint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d247fdfeb116cecde593bdf26fed2ce174a87874030d4952a0e21e0a464a8c38(
    *,
    accepted_protocols: typing.Sequence[builtins.str],
    frontend_endpoints: typing.Sequence[builtins.str],
    name: builtins.str,
    patterns_to_match: typing.Sequence[builtins.str],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarding_configuration: typing.Optional[typing.Union[FrontdoorRoutingRuleForwardingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect_configuration: typing.Optional[typing.Union[FrontdoorRoutingRuleRedirectConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b693881f445f86d4d4f86f49c9fa47bdd385d4b0c90652d137e3a3b66627308c(
    *,
    backend_pool_name: builtins.str,
    cache_duration: typing.Optional[builtins.str] = None,
    cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cache_query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_query_parameter_strip_directive: typing.Optional[builtins.str] = None,
    cache_use_dynamic_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_forwarding_path: typing.Optional[builtins.str] = None,
    forwarding_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96838071c367ab04ab5f4a371937b614034c8f3b84e46a952095c715a8b004ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5fc340206852f630f6879b81408b39b1bdba16e88e36301363600a48a22fb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e50ef31f6648f85ad0beea8074c264397b364175ac99cf2a32b68471e43f3c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636d232e37d405568fdfadf371eeda7546ffe5a43a23f09c08ac9894ebc9e28a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6496606f2cb415126b29a384d09d6f0714f8e38d27a96a660446e35f360bfd3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fb01975cb7cfe0573d3a3308ec9b35eb60665f09477169d40552418c343bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718a8a5289311064d4410851d941c1ea9f1652e0f89e91a4215273be6d32011b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b451098c7c05ada64ca627f925881e48b2da955b5b8f1702ecb7e19f8a2823b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9817fb46827c4497203a84c4351ef815d9d183aa5a7503c2763149b0137ef075(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df02452aa99caa8b8d1cdda1e877ff1c44c8cc96c34fb7a8cf90ae07dabf396(
    value: typing.Optional[FrontdoorRoutingRuleForwardingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1906be6682c60e871b94ce16a3d75cbea922f8c487a1feb71211883a049d470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99df99aaec782854295ffa6ecd2e6b4885a95f390636bf603107f438e7d677c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4121f3f65e7be94cb1a440b57c27f4f83edcaf1e2e51c2d1d13524e0ed77ce18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57b4a1ed203db703199c1651d681e037b2f2c6819b99e4d6766829011eae69e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455d5346066b74c9abdc416a680ea891cf1a533a87f52b5958f0ea23440a9998(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4550775b90de4efe323128170d2eecc7332d02fda025a21eacece6a9f0ddec70(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FrontdoorRoutingRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696b47c062ca32078ac13a29bcd6732efa92187e0d169701db427583f3e4ef3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd8731efc39ace697b83731770c66b1ffa6360d7252c9ad8a28c23c20426f40(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701d1376444ce88020fcc7975c065e34e8f6831173ad4ee16d2934e3bb948da3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5ef21f177b50bb3771036fc8ebe4fe502141840048206c0fd458d3a41618a7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c01e770893f8af8540626f0bb2ea9e3b9d880708b1c9d4a4ecf444963a61d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b846359a78a8819bd1aec53636eac2a113dbdc016e000b795d002c08c614bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1c450c5e71aa98153094b586dcba15d01adacb4e19556ec5481a2cc2a94360(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorRoutingRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f449a4c4d2636dfa8dd2499a00a2bef63af21a467fe30d2472f7f3ddd72e4eac(
    *,
    redirect_protocol: builtins.str,
    redirect_type: builtins.str,
    custom_fragment: typing.Optional[builtins.str] = None,
    custom_host: typing.Optional[builtins.str] = None,
    custom_path: typing.Optional[builtins.str] = None,
    custom_query_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3316bb683e2ce53cfcdc60b29cb4ae8c3537cabe0c2bd54b9585b140e4a70e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4853a41c528bfcfa0e124651e58ae0fad934f5b3cbb8526261421980eccd60c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8f08a21680f3331e314b7756946525ad1856b1cc496e425cdc3268895d0175(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6973bb1bbff1a0055654895c21aa5ef99e0c16ee96debd01d0a1d75cc16429d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8344fd9c05ab24c33ee66fbbb11982f6b793b54abfa08082a13736b3325c58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1bf3e6f4123092c3f42ee5fc452356f90a9ffb2e60dc0e45b967a1236e3d1b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d3776edbae4db6650ac23da14a770a8b1cf7c3b5a236fa50b116ab17b65d8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a023943a09c76e657b4a1dc2290203db1e42f5cbda8726e4989fe114dc7b269b(
    value: typing.Optional[FrontdoorRoutingRuleRedirectConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b04eafe27090d8db51d586a509c36e7216b0c91c6f56d166506b8e83bed62d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a584200a3458a215cbf271f4e554339e9605860f5d8b48ba40925a8371905fc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7aa9a12bbbf4ffb8f5b0f7e612e76a7ee5d70506bfbf46871f2e666040c3b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9387cac33d7b65410e7b6018ce152522ae63c05a7be4e44b47ded99abb23615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb8bed73bae47a96c47f0fd52e1e9b79d2fdc921b16cc40756ad12a756f840a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec26de00ae3fc9e93c01f41ef99b53cc156882e90e4bfc38dfe2556084e522a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ff47a7f6b459315f31345c1d3055e2f5101ea8ebf3765f1d637766c1883669(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
