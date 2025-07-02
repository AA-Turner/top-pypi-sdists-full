r'''
# `azurerm_application_gateway`

Refer to the Terraform Registry for docs: [`azurerm_application_gateway`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway).
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


class ApplicationGateway(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGateway",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway azurerm_application_gateway}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backend_address_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayBackendAddressPool", typing.Dict[builtins.str, typing.Any]]]],
        backend_http_settings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayBackendHttpSettings", typing.Dict[builtins.str, typing.Any]]]],
        frontend_ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayFrontendIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        frontend_port: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayFrontendPort", typing.Dict[builtins.str, typing.Any]]]],
        gateway_ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayGatewayIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        http_listener: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayHttpListener", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        request_routing_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRequestRoutingRule", typing.Dict[builtins.str, typing.Any]]]],
        resource_group_name: builtins.str,
        sku: typing.Union["ApplicationGatewaySku", typing.Dict[builtins.str, typing.Any]],
        authentication_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayAuthenticationCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        autoscale_configuration: typing.Optional[typing.Union["ApplicationGatewayAutoscaleConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_error_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayCustomErrorConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        firewall_policy_id: typing.Optional[builtins.str] = None,
        force_firewall_policy_association: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        global_: typing.Optional[typing.Union["ApplicationGatewayGlobal", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ApplicationGatewayIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayProbe", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redirect_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRedirectConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rewrite_rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssl_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewaySslCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssl_policy: typing.Optional[typing.Union["ApplicationGatewaySslPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_profile: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewaySslProfile", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ApplicationGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_client_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayTrustedClientCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        trusted_root_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayTrustedRootCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_path_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayUrlPathMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        waf_configuration: typing.Optional[typing.Union["ApplicationGatewayWafConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway azurerm_application_gateway} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backend_address_pool: backend_address_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_address_pool ApplicationGateway#backend_address_pool}
        :param backend_http_settings: backend_http_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_http_settings ApplicationGateway#backend_http_settings}
        :param frontend_ip_configuration: frontend_ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_ip_configuration ApplicationGateway#frontend_ip_configuration}
        :param frontend_port: frontend_port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_port ApplicationGateway#frontend_port}
        :param gateway_ip_configuration: gateway_ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#gateway_ip_configuration ApplicationGateway#gateway_ip_configuration}
        :param http_listener: http_listener block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#http_listener ApplicationGateway#http_listener}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#location ApplicationGateway#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param request_routing_rule: request_routing_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_routing_rule ApplicationGateway#request_routing_rule}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#resource_group_name ApplicationGateway#resource_group_name}.
        :param sku: sku block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#sku ApplicationGateway#sku}
        :param authentication_certificate: authentication_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#authentication_certificate ApplicationGateway#authentication_certificate}
        :param autoscale_configuration: autoscale_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#autoscale_configuration ApplicationGateway#autoscale_configuration}
        :param custom_error_configuration: custom_error_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#custom_error_configuration ApplicationGateway#custom_error_configuration}
        :param enable_http2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#enable_http2 ApplicationGateway#enable_http2}.
        :param fips_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#fips_enabled ApplicationGateway#fips_enabled}.
        :param firewall_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_policy_id ApplicationGateway#firewall_policy_id}.
        :param force_firewall_policy_association: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#force_firewall_policy_association ApplicationGateway#force_firewall_policy_association}.
        :param global_: global block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#global ApplicationGateway#global}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#id ApplicationGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#identity ApplicationGateway#identity}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_link_configuration ApplicationGateway#private_link_configuration}
        :param probe: probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#probe ApplicationGateway#probe}
        :param redirect_configuration: redirect_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#redirect_configuration ApplicationGateway#redirect_configuration}
        :param rewrite_rule_set: rewrite_rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rewrite_rule_set ApplicationGateway#rewrite_rule_set}
        :param ssl_certificate: ssl_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_certificate ApplicationGateway#ssl_certificate}
        :param ssl_policy: ssl_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_policy ApplicationGateway#ssl_policy}
        :param ssl_profile: ssl_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_profile ApplicationGateway#ssl_profile}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#tags ApplicationGateway#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#timeouts ApplicationGateway#timeouts}
        :param trusted_client_certificate: trusted_client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_client_certificate ApplicationGateway#trusted_client_certificate}
        :param trusted_root_certificate: trusted_root_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_root_certificate ApplicationGateway#trusted_root_certificate}
        :param url_path_map: url_path_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#url_path_map ApplicationGateway#url_path_map}
        :param waf_configuration: waf_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#waf_configuration ApplicationGateway#waf_configuration}
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#zones ApplicationGateway#zones}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b90d88008c9c386a35f6d2824dd78e7447e8b829eea7c6d7d23b55e0e10d89)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApplicationGatewayConfig(
            backend_address_pool=backend_address_pool,
            backend_http_settings=backend_http_settings,
            frontend_ip_configuration=frontend_ip_configuration,
            frontend_port=frontend_port,
            gateway_ip_configuration=gateway_ip_configuration,
            http_listener=http_listener,
            location=location,
            name=name,
            request_routing_rule=request_routing_rule,
            resource_group_name=resource_group_name,
            sku=sku,
            authentication_certificate=authentication_certificate,
            autoscale_configuration=autoscale_configuration,
            custom_error_configuration=custom_error_configuration,
            enable_http2=enable_http2,
            fips_enabled=fips_enabled,
            firewall_policy_id=firewall_policy_id,
            force_firewall_policy_association=force_firewall_policy_association,
            global_=global_,
            id=id,
            identity=identity,
            private_link_configuration=private_link_configuration,
            probe=probe,
            redirect_configuration=redirect_configuration,
            rewrite_rule_set=rewrite_rule_set,
            ssl_certificate=ssl_certificate,
            ssl_policy=ssl_policy,
            ssl_profile=ssl_profile,
            tags=tags,
            timeouts=timeouts,
            trusted_client_certificate=trusted_client_certificate,
            trusted_root_certificate=trusted_root_certificate,
            url_path_map=url_path_map,
            waf_configuration=waf_configuration,
            zones=zones,
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
        '''Generates CDKTF code for importing a ApplicationGateway resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApplicationGateway to import.
        :param import_from_id: The id of the existing ApplicationGateway that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApplicationGateway to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caff855b114071be2ae34045613db9e0ab26c0bc76be7b1f08b4ecf6c8f3af69)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthenticationCertificate")
    def put_authentication_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayAuthenticationCertificate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df942d41ed78b3e6e74a0e283f7a564df8400d87d84c8aad2235bd2f490b763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthenticationCertificate", [value]))

    @jsii.member(jsii_name="putAutoscaleConfiguration")
    def put_autoscale_configuration(
        self,
        *,
        min_capacity: jsii.Number,
        max_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#min_capacity ApplicationGateway#min_capacity}.
        :param max_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#max_capacity ApplicationGateway#max_capacity}.
        '''
        value = ApplicationGatewayAutoscaleConfiguration(
            min_capacity=min_capacity, max_capacity=max_capacity
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaleConfiguration", [value]))

    @jsii.member(jsii_name="putBackendAddressPool")
    def put_backend_address_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayBackendAddressPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7bf5de1733030c05f9e72582ec22ce368eeb3f62499609b20a2e61f1d686e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendAddressPool", [value]))

    @jsii.member(jsii_name="putBackendHttpSettings")
    def put_backend_http_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayBackendHttpSettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f56f8d4f489f30084b0f7be9921261575f73d1d2c642dfa19e4c3ed2ae9482b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendHttpSettings", [value]))

    @jsii.member(jsii_name="putCustomErrorConfiguration")
    def put_custom_error_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayCustomErrorConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e9b5e3632717398f4abe35653c8eee273be90377c20f2e1c91912b55f84559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomErrorConfiguration", [value]))

    @jsii.member(jsii_name="putFrontendIpConfiguration")
    def put_frontend_ip_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayFrontendIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6fe15b38f2fd6921099adbbfa888b3d885d65a45d8f9a552a6f9282388b2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFrontendIpConfiguration", [value]))

    @jsii.member(jsii_name="putFrontendPort")
    def put_frontend_port(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayFrontendPort", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd7d53509c6113830d35da6028404fc3bf67c52de9a1390105ca4c9246d78e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFrontendPort", [value]))

    @jsii.member(jsii_name="putGatewayIpConfiguration")
    def put_gateway_ip_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayGatewayIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f9b72339ee66fc6cda7f0f9dde85d6376022256d95ccca4b54905a2584728a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGatewayIpConfiguration", [value]))

    @jsii.member(jsii_name="putGlobal")
    def put_global(
        self,
        *,
        request_buffering_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        response_buffering_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param request_buffering_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_buffering_enabled ApplicationGateway#request_buffering_enabled}.
        :param response_buffering_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#response_buffering_enabled ApplicationGateway#response_buffering_enabled}.
        '''
        value = ApplicationGatewayGlobal(
            request_buffering_enabled=request_buffering_enabled,
            response_buffering_enabled=response_buffering_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putGlobal", [value]))

    @jsii.member(jsii_name="putHttpListener")
    def put_http_listener(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayHttpListener", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab57c576d77fbfb1db55047cf6d5bc8909b3c88d1357de9c76511966b03776f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpListener", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#type ApplicationGateway#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#identity_ids ApplicationGateway#identity_ids}.
        '''
        value = ApplicationGatewayIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putPrivateLinkConfiguration")
    def put_private_link_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ae7c4f9e0abbf5c3e7efd20d421342d0af36923529b6b286995bc63f5de325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrivateLinkConfiguration", [value]))

    @jsii.member(jsii_name="putProbe")
    def put_probe(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayProbe", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077d68c6f1576f95155cac0ea0f0a670e824a4ee704cfd984f6902e637ece985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProbe", [value]))

    @jsii.member(jsii_name="putRedirectConfiguration")
    def put_redirect_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRedirectConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8868548291ee93a449c0853492ad2c868b0e57369c1ad23c3f702856cb27960e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedirectConfiguration", [value]))

    @jsii.member(jsii_name="putRequestRoutingRule")
    def put_request_routing_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRequestRoutingRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993798f3b9c700f58307a7a9df2490ffffa795c4b822755c71721858d020cec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestRoutingRule", [value]))

    @jsii.member(jsii_name="putRewriteRuleSet")
    def put_rewrite_rule_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c1b2651eb6936c5bec4063b759c80393290e13c1e93e1919baa544adb51238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRewriteRuleSet", [value]))

    @jsii.member(jsii_name="putSku")
    def put_sku(
        self,
        *,
        name: builtins.str,
        tier: builtins.str,
        capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#tier ApplicationGateway#tier}.
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#capacity ApplicationGateway#capacity}.
        '''
        value = ApplicationGatewaySku(name=name, tier=tier, capacity=capacity)

        return typing.cast(None, jsii.invoke(self, "putSku", [value]))

    @jsii.member(jsii_name="putSslCertificate")
    def put_ssl_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewaySslCertificate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2474d0f79155a7b6055eccd9dc2360703df65b4f34c59c6ba101fc36711ed312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSslCertificate", [value]))

    @jsii.member(jsii_name="putSslPolicy")
    def put_ssl_policy(
        self,
        *,
        cipher_suites: typing.Optional[typing.Sequence[builtins.str]] = None,
        disabled_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        min_protocol_version: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cipher_suites: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#cipher_suites ApplicationGateway#cipher_suites}.
        :param disabled_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#disabled_protocols ApplicationGateway#disabled_protocols}.
        :param min_protocol_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#min_protocol_version ApplicationGateway#min_protocol_version}.
        :param policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_name ApplicationGateway#policy_name}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_type ApplicationGateway#policy_type}.
        '''
        value = ApplicationGatewaySslPolicy(
            cipher_suites=cipher_suites,
            disabled_protocols=disabled_protocols,
            min_protocol_version=min_protocol_version,
            policy_name=policy_name,
            policy_type=policy_type,
        )

        return typing.cast(None, jsii.invoke(self, "putSslPolicy", [value]))

    @jsii.member(jsii_name="putSslProfile")
    def put_ssl_profile(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewaySslProfile", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493bdc2bf40e815b05587e277e2f1915ef89f87b1c216a8d4440f71fce6304f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSslProfile", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#create ApplicationGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#delete ApplicationGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#read ApplicationGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#update ApplicationGateway#update}.
        '''
        value = ApplicationGatewayTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTrustedClientCertificate")
    def put_trusted_client_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayTrustedClientCertificate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851c1336c31df1030750d273b7003ebbb768984e7d878ed9652e94a0a114ffb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrustedClientCertificate", [value]))

    @jsii.member(jsii_name="putTrustedRootCertificate")
    def put_trusted_root_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayTrustedRootCertificate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53dba94acd48b63337c732a5ce45adaeab968538bee0eb2dd86f8c2a38588cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrustedRootCertificate", [value]))

    @jsii.member(jsii_name="putUrlPathMap")
    def put_url_path_map(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayUrlPathMap", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdf427d7848b2b8450395682c23e5b5a1c04fd0ad287ceb60626ff5aebd2340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrlPathMap", [value]))

    @jsii.member(jsii_name="putWafConfiguration")
    def put_waf_configuration(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        firewall_mode: builtins.str,
        rule_set_version: builtins.str,
        disabled_rule_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayWafConfigurationDisabledRuleGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayWafConfigurationExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        file_upload_limit_mb: typing.Optional[jsii.Number] = None,
        max_request_body_size_kb: typing.Optional[jsii.Number] = None,
        request_body_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rule_set_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#enabled ApplicationGateway#enabled}.
        :param firewall_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_mode ApplicationGateway#firewall_mode}.
        :param rule_set_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_set_version ApplicationGateway#rule_set_version}.
        :param disabled_rule_group: disabled_rule_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#disabled_rule_group ApplicationGateway#disabled_rule_group}
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#exclusion ApplicationGateway#exclusion}
        :param file_upload_limit_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#file_upload_limit_mb ApplicationGateway#file_upload_limit_mb}.
        :param max_request_body_size_kb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#max_request_body_size_kb ApplicationGateway#max_request_body_size_kb}.
        :param request_body_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_body_check ApplicationGateway#request_body_check}.
        :param rule_set_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_set_type ApplicationGateway#rule_set_type}.
        '''
        value = ApplicationGatewayWafConfiguration(
            enabled=enabled,
            firewall_mode=firewall_mode,
            rule_set_version=rule_set_version,
            disabled_rule_group=disabled_rule_group,
            exclusion=exclusion,
            file_upload_limit_mb=file_upload_limit_mb,
            max_request_body_size_kb=max_request_body_size_kb,
            request_body_check=request_body_check,
            rule_set_type=rule_set_type,
        )

        return typing.cast(None, jsii.invoke(self, "putWafConfiguration", [value]))

    @jsii.member(jsii_name="resetAuthenticationCertificate")
    def reset_authentication_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationCertificate", []))

    @jsii.member(jsii_name="resetAutoscaleConfiguration")
    def reset_autoscale_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaleConfiguration", []))

    @jsii.member(jsii_name="resetCustomErrorConfiguration")
    def reset_custom_error_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomErrorConfiguration", []))

    @jsii.member(jsii_name="resetEnableHttp2")
    def reset_enable_http2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHttp2", []))

    @jsii.member(jsii_name="resetFipsEnabled")
    def reset_fips_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFipsEnabled", []))

    @jsii.member(jsii_name="resetFirewallPolicyId")
    def reset_firewall_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirewallPolicyId", []))

    @jsii.member(jsii_name="resetForceFirewallPolicyAssociation")
    def reset_force_firewall_policy_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceFirewallPolicyAssociation", []))

    @jsii.member(jsii_name="resetGlobal")
    def reset_global(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobal", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetPrivateLinkConfiguration")
    def reset_private_link_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkConfiguration", []))

    @jsii.member(jsii_name="resetProbe")
    def reset_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProbe", []))

    @jsii.member(jsii_name="resetRedirectConfiguration")
    def reset_redirect_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectConfiguration", []))

    @jsii.member(jsii_name="resetRewriteRuleSet")
    def reset_rewrite_rule_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewriteRuleSet", []))

    @jsii.member(jsii_name="resetSslCertificate")
    def reset_ssl_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertificate", []))

    @jsii.member(jsii_name="resetSslPolicy")
    def reset_ssl_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslPolicy", []))

    @jsii.member(jsii_name="resetSslProfile")
    def reset_ssl_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslProfile", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrustedClientCertificate")
    def reset_trusted_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedClientCertificate", []))

    @jsii.member(jsii_name="resetTrustedRootCertificate")
    def reset_trusted_root_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedRootCertificate", []))

    @jsii.member(jsii_name="resetUrlPathMap")
    def reset_url_path_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlPathMap", []))

    @jsii.member(jsii_name="resetWafConfiguration")
    def reset_waf_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWafConfiguration", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

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
    @jsii.member(jsii_name="authenticationCertificate")
    def authentication_certificate(
        self,
    ) -> "ApplicationGatewayAuthenticationCertificateList":
        return typing.cast("ApplicationGatewayAuthenticationCertificateList", jsii.get(self, "authenticationCertificate"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleConfiguration")
    def autoscale_configuration(
        self,
    ) -> "ApplicationGatewayAutoscaleConfigurationOutputReference":
        return typing.cast("ApplicationGatewayAutoscaleConfigurationOutputReference", jsii.get(self, "autoscaleConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="backendAddressPool")
    def backend_address_pool(self) -> "ApplicationGatewayBackendAddressPoolList":
        return typing.cast("ApplicationGatewayBackendAddressPoolList", jsii.get(self, "backendAddressPool"))

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettings")
    def backend_http_settings(self) -> "ApplicationGatewayBackendHttpSettingsList":
        return typing.cast("ApplicationGatewayBackendHttpSettingsList", jsii.get(self, "backendHttpSettings"))

    @builtins.property
    @jsii.member(jsii_name="customErrorConfiguration")
    def custom_error_configuration(
        self,
    ) -> "ApplicationGatewayCustomErrorConfigurationList":
        return typing.cast("ApplicationGatewayCustomErrorConfigurationList", jsii.get(self, "customErrorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="frontendIpConfiguration")
    def frontend_ip_configuration(
        self,
    ) -> "ApplicationGatewayFrontendIpConfigurationList":
        return typing.cast("ApplicationGatewayFrontendIpConfigurationList", jsii.get(self, "frontendIpConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="frontendPort")
    def frontend_port(self) -> "ApplicationGatewayFrontendPortList":
        return typing.cast("ApplicationGatewayFrontendPortList", jsii.get(self, "frontendPort"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIpConfiguration")
    def gateway_ip_configuration(
        self,
    ) -> "ApplicationGatewayGatewayIpConfigurationList":
        return typing.cast("ApplicationGatewayGatewayIpConfigurationList", jsii.get(self, "gatewayIpConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="global")
    def global_(self) -> "ApplicationGatewayGlobalOutputReference":
        return typing.cast("ApplicationGatewayGlobalOutputReference", jsii.get(self, "global"))

    @builtins.property
    @jsii.member(jsii_name="httpListener")
    def http_listener(self) -> "ApplicationGatewayHttpListenerList":
        return typing.cast("ApplicationGatewayHttpListenerList", jsii.get(self, "httpListener"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "ApplicationGatewayIdentityOutputReference":
        return typing.cast("ApplicationGatewayIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpointConnection")
    def private_endpoint_connection(
        self,
    ) -> "ApplicationGatewayPrivateEndpointConnectionList":
        return typing.cast("ApplicationGatewayPrivateEndpointConnectionList", jsii.get(self, "privateEndpointConnection"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfiguration")
    def private_link_configuration(
        self,
    ) -> "ApplicationGatewayPrivateLinkConfigurationList":
        return typing.cast("ApplicationGatewayPrivateLinkConfigurationList", jsii.get(self, "privateLinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="probe")
    def probe(self) -> "ApplicationGatewayProbeList":
        return typing.cast("ApplicationGatewayProbeList", jsii.get(self, "probe"))

    @builtins.property
    @jsii.member(jsii_name="redirectConfiguration")
    def redirect_configuration(self) -> "ApplicationGatewayRedirectConfigurationList":
        return typing.cast("ApplicationGatewayRedirectConfigurationList", jsii.get(self, "redirectConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="requestRoutingRule")
    def request_routing_rule(self) -> "ApplicationGatewayRequestRoutingRuleList":
        return typing.cast("ApplicationGatewayRequestRoutingRuleList", jsii.get(self, "requestRoutingRule"))

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSet")
    def rewrite_rule_set(self) -> "ApplicationGatewayRewriteRuleSetList":
        return typing.cast("ApplicationGatewayRewriteRuleSetList", jsii.get(self, "rewriteRuleSet"))

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> "ApplicationGatewaySkuOutputReference":
        return typing.cast("ApplicationGatewaySkuOutputReference", jsii.get(self, "sku"))

    @builtins.property
    @jsii.member(jsii_name="sslCertificate")
    def ssl_certificate(self) -> "ApplicationGatewaySslCertificateList":
        return typing.cast("ApplicationGatewaySslCertificateList", jsii.get(self, "sslCertificate"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> "ApplicationGatewaySslPolicyOutputReference":
        return typing.cast("ApplicationGatewaySslPolicyOutputReference", jsii.get(self, "sslPolicy"))

    @builtins.property
    @jsii.member(jsii_name="sslProfile")
    def ssl_profile(self) -> "ApplicationGatewaySslProfileList":
        return typing.cast("ApplicationGatewaySslProfileList", jsii.get(self, "sslProfile"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApplicationGatewayTimeoutsOutputReference":
        return typing.cast("ApplicationGatewayTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trustedClientCertificate")
    def trusted_client_certificate(
        self,
    ) -> "ApplicationGatewayTrustedClientCertificateList":
        return typing.cast("ApplicationGatewayTrustedClientCertificateList", jsii.get(self, "trustedClientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="trustedRootCertificate")
    def trusted_root_certificate(
        self,
    ) -> "ApplicationGatewayTrustedRootCertificateList":
        return typing.cast("ApplicationGatewayTrustedRootCertificateList", jsii.get(self, "trustedRootCertificate"))

    @builtins.property
    @jsii.member(jsii_name="urlPathMap")
    def url_path_map(self) -> "ApplicationGatewayUrlPathMapList":
        return typing.cast("ApplicationGatewayUrlPathMapList", jsii.get(self, "urlPathMap"))

    @builtins.property
    @jsii.member(jsii_name="wafConfiguration")
    def waf_configuration(self) -> "ApplicationGatewayWafConfigurationOutputReference":
        return typing.cast("ApplicationGatewayWafConfigurationOutputReference", jsii.get(self, "wafConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="authenticationCertificateInput")
    def authentication_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayAuthenticationCertificate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayAuthenticationCertificate"]]], jsii.get(self, "authenticationCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleConfigurationInput")
    def autoscale_configuration_input(
        self,
    ) -> typing.Optional["ApplicationGatewayAutoscaleConfiguration"]:
        return typing.cast(typing.Optional["ApplicationGatewayAutoscaleConfiguration"], jsii.get(self, "autoscaleConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="backendAddressPoolInput")
    def backend_address_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayBackendAddressPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayBackendAddressPool"]]], jsii.get(self, "backendAddressPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettingsInput")
    def backend_http_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayBackendHttpSettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayBackendHttpSettings"]]], jsii.get(self, "backendHttpSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="customErrorConfigurationInput")
    def custom_error_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayCustomErrorConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayCustomErrorConfiguration"]]], jsii.get(self, "customErrorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHttp2Input")
    def enable_http2_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHttp2Input"))

    @builtins.property
    @jsii.member(jsii_name="fipsEnabledInput")
    def fips_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fipsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyIdInput")
    def firewall_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="forceFirewallPolicyAssociationInput")
    def force_firewall_policy_association_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceFirewallPolicyAssociationInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendIpConfigurationInput")
    def frontend_ip_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayFrontendIpConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayFrontendIpConfiguration"]]], jsii.get(self, "frontendIpConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendPortInput")
    def frontend_port_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayFrontendPort"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayFrontendPort"]]], jsii.get(self, "frontendPortInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIpConfigurationInput")
    def gateway_ip_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayGatewayIpConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayGatewayIpConfiguration"]]], jsii.get(self, "gatewayIpConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="globalInput")
    def global_input(self) -> typing.Optional["ApplicationGatewayGlobal"]:
        return typing.cast(typing.Optional["ApplicationGatewayGlobal"], jsii.get(self, "globalInput"))

    @builtins.property
    @jsii.member(jsii_name="httpListenerInput")
    def http_listener_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayHttpListener"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayHttpListener"]]], jsii.get(self, "httpListenerInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["ApplicationGatewayIdentity"]:
        return typing.cast(typing.Optional["ApplicationGatewayIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfigurationInput")
    def private_link_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayPrivateLinkConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayPrivateLinkConfiguration"]]], jsii.get(self, "privateLinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="probeInput")
    def probe_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayProbe"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayProbe"]]], jsii.get(self, "probeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectConfigurationInput")
    def redirect_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRedirectConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRedirectConfiguration"]]], jsii.get(self, "redirectConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="requestRoutingRuleInput")
    def request_routing_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRequestRoutingRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRequestRoutingRule"]]], jsii.get(self, "requestRoutingRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSetInput")
    def rewrite_rule_set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSet"]]], jsii.get(self, "rewriteRuleSetInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional["ApplicationGatewaySku"]:
        return typing.cast(typing.Optional["ApplicationGatewaySku"], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertificateInput")
    def ssl_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewaySslCertificate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewaySslCertificate"]]], jsii.get(self, "sslCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicyInput")
    def ssl_policy_input(self) -> typing.Optional["ApplicationGatewaySslPolicy"]:
        return typing.cast(typing.Optional["ApplicationGatewaySslPolicy"], jsii.get(self, "sslPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="sslProfileInput")
    def ssl_profile_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewaySslProfile"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewaySslProfile"]]], jsii.get(self, "sslProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApplicationGatewayTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApplicationGatewayTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedClientCertificateInput")
    def trusted_client_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayTrustedClientCertificate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayTrustedClientCertificate"]]], jsii.get(self, "trustedClientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedRootCertificateInput")
    def trusted_root_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayTrustedRootCertificate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayTrustedRootCertificate"]]], jsii.get(self, "trustedRootCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="urlPathMapInput")
    def url_path_map_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayUrlPathMap"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayUrlPathMap"]]], jsii.get(self, "urlPathMapInput"))

    @builtins.property
    @jsii.member(jsii_name="wafConfigurationInput")
    def waf_configuration_input(
        self,
    ) -> typing.Optional["ApplicationGatewayWafConfiguration"]:
        return typing.cast(typing.Optional["ApplicationGatewayWafConfiguration"], jsii.get(self, "wafConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHttp2")
    def enable_http2(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHttp2"))

    @enable_http2.setter
    def enable_http2(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3ef380d4f2ee8460d8ba77f88101060028a6bde900cceeb61f534d61b4d754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHttp2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fipsEnabled")
    def fips_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fipsEnabled"))

    @fips_enabled.setter
    def fips_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1639f202c20b58f94003f894ac1c7f1a2fc206c4ae2198f216432e28626de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fipsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyId")
    def firewall_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyId"))

    @firewall_policy_id.setter
    def firewall_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb627469b2dee9fbfdacd4fc20ee7a93146b5b0c5ef4236d3fc6d845eb983651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceFirewallPolicyAssociation")
    def force_firewall_policy_association(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceFirewallPolicyAssociation"))

    @force_firewall_policy_association.setter
    def force_firewall_policy_association(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a485756cd3e918bd080852852aceaf82676b7770c6a2cdc671cef2d4c06077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceFirewallPolicyAssociation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3d9e38c3ce3162be5fba6f71ceab3188b09e425754ae4ebd447d6168417c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__563b942bb2718281e3258c017a8d6e28f758a7108078e0cd42bf02f70c7aa42e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ed09c2a46d45e3a5aa79a147595968d7dafa029c49e6582f1bb561d7a410cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e10bce8e08ca6a12f27cf0667b552bdec1d54b616ef4a85f88429a8fc973ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f512089ca246cb99e3bf433e81d200b1462d26a09e8d3fc05d35e0ce07f070a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb656beb334e7e827bb27c4404d96ed8f4089860079473e37b5cade2f2276653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayAuthenticationCertificate",
    jsii_struct_bases=[],
    name_mapping={"data": "data", "name": "name"},
)
class ApplicationGatewayAuthenticationCertificate:
    def __init__(self, *, data: builtins.str, name: builtins.str) -> None:
        '''
        :param data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#data ApplicationGateway#data}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c03dc2364969cfcc4fe706e17c021b5bccd93cab50e313207bf6538aa7e062)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
            "name": name,
        }

    @builtins.property
    def data(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#data ApplicationGateway#data}.'''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayAuthenticationCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayAuthenticationCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayAuthenticationCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44c29d41728d88b126593cf4cf2e83d1116ba1d50876ea9210b78a43a7b6990c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayAuthenticationCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882007b516d3c1fb2acdc06feeeb68f9fbd17286820e540369da717502d4e174)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayAuthenticationCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e191d24b7e54a471fb1416049c49e111b766942de7bb09e68e9b0b6091d7bf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__497142c6d57a6598b6acb261004b6a2399588ad18309178dd47921b25a7e629e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f573f6fb465fee9a8aab8d7e1c0850f05f04a9d328d99b9de29101662bdee40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayAuthenticationCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayAuthenticationCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayAuthenticationCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5351eb7e69a7951986e29af4c6dc04f9f9d0db0d3f786b3ea8fad8544cf020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayAuthenticationCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayAuthenticationCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3952c7c9b69421d3f80a89ff0cd69d5d7782b5ba28956269388931cea7a4e104)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3937864721807a10d6ffc61392f9ed2af938b8dacddcfb3e824514b0869c9a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae4ddbe37730ea32919a122a8fc619bfec03f44a9f4d1c1af07584fffaeb254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayAuthenticationCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayAuthenticationCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayAuthenticationCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a394bfc2dfb63478ed28868baf71d56bee215d41cdf8e5121116b67fd21aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayAutoscaleConfiguration",
    jsii_struct_bases=[],
    name_mapping={"min_capacity": "minCapacity", "max_capacity": "maxCapacity"},
)
class ApplicationGatewayAutoscaleConfiguration:
    def __init__(
        self,
        *,
        min_capacity: jsii.Number,
        max_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#min_capacity ApplicationGateway#min_capacity}.
        :param max_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#max_capacity ApplicationGateway#max_capacity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e91ec2068e22998214b74eb5a0fd7e56617f78b27f18216e97b97add995765)
            check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "min_capacity": min_capacity,
        }
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity

    @builtins.property
    def min_capacity(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#min_capacity ApplicationGateway#min_capacity}.'''
        result = self._values.get("min_capacity")
        assert result is not None, "Required property 'min_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#max_capacity ApplicationGateway#max_capacity}.'''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayAutoscaleConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayAutoscaleConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayAutoscaleConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52c81a54c2eed9f04a07163b9e164cdac0e1ccb6ebaef2ff4d07735908affc94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxCapacity")
    def reset_max_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="maxCapacityInput")
    def max_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="minCapacityInput")
    def min_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCapacity"))

    @max_capacity.setter
    def max_capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9760ff0de2d854d6b0f279e188e9c89bb8b33e7280b30bff39b70d27a56c19e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCapacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCapacity")
    def min_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minCapacity"))

    @min_capacity.setter
    def min_capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9cddb854db08063041ba86fe0c7568c6c15e3b8c63c2a9cd4b5b70d05a05f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCapacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApplicationGatewayAutoscaleConfiguration]:
        return typing.cast(typing.Optional[ApplicationGatewayAutoscaleConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationGatewayAutoscaleConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb3b30be1cac78640696feb5e03302bbad6dc3854c3c9656f266c9bd635652fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendAddressPool",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "fqdns": "fqdns", "ip_addresses": "ipAddresses"},
)
class ApplicationGatewayBackendAddressPool:
    def __init__(
        self,
        *,
        name: builtins.str,
        fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param fqdns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#fqdns ApplicationGateway#fqdns}.
        :param ip_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ip_addresses ApplicationGateway#ip_addresses}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c3ce0810ace6665387dcd6c4932786b9e9bbd27b37c93e602fbfa8561805b3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument fqdns", value=fqdns, expected_type=type_hints["fqdns"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if fqdns is not None:
            self._values["fqdns"] = fqdns
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#fqdns ApplicationGateway#fqdns}.'''
        result = self._values.get("fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ip_addresses ApplicationGateway#ip_addresses}.'''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayBackendAddressPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayBackendAddressPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendAddressPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__448ece75ead6543c9032358f350ccab0b5fb868681a81eaae3af36a6c7fc90a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayBackendAddressPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4e8828be27887a9d92cc8fd6e31a36ea2fc433bf5603cf9df7a018a507c416)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayBackendAddressPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe5bfa10ff675fdfc97212fc14c65bbcce4acaab2b250ed55aec52d718a52bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2ef62be62640aed7147d5cc73343b7041161b22f4a301d67bb4fc751af27740)
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
            type_hints = typing.get_type_hints(_typecheckingstub__735aaed826bad39af8f77ab96470bc34938898b01e2090398eb033f6e6b386d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendAddressPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendAddressPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendAddressPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b484001450df6fb1659bebd9ca253af63c89d8b340e33632bc3b2448709196cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayBackendAddressPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendAddressPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8505eb9f460df17ffb0a37f1d3e7261a882ddcc519fca0d4d7bf90486b851e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFqdns")
    def reset_fqdns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFqdns", []))

    @jsii.member(jsii_name="resetIpAddresses")
    def reset_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddresses", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="fqdnsInput")
    def fqdns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fqdnsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressesInput")
    def ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdns")
    def fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fqdns"))

    @fqdns.setter
    def fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c0abdc89c0f797228bf66d724fdcb3c3588fb2d6ba8eb235d423e7bbc3c54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc7aad3357c7f9bba65847ccd66695ebb828ecbe935d605fc4e5372dcdb5d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bebf85af1f35266c247a49781987024127cf257c27d8b2f3f79ea085f8807bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendAddressPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendAddressPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendAddressPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b11866fa662615c8d8f0abded6633bd7a792f6076bab68759e71560614cdbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendHttpSettings",
    jsii_struct_bases=[],
    name_mapping={
        "cookie_based_affinity": "cookieBasedAffinity",
        "name": "name",
        "port": "port",
        "protocol": "protocol",
        "affinity_cookie_name": "affinityCookieName",
        "authentication_certificate": "authenticationCertificate",
        "connection_draining": "connectionDraining",
        "host_name": "hostName",
        "path": "path",
        "pick_host_name_from_backend_address": "pickHostNameFromBackendAddress",
        "probe_name": "probeName",
        "request_timeout": "requestTimeout",
        "trusted_root_certificate_names": "trustedRootCertificateNames",
    },
)
class ApplicationGatewayBackendHttpSettings:
    def __init__(
        self,
        *,
        cookie_based_affinity: builtins.str,
        name: builtins.str,
        port: jsii.Number,
        protocol: builtins.str,
        affinity_cookie_name: typing.Optional[builtins.str] = None,
        authentication_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayBackendHttpSettingsAuthenticationCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection_draining: typing.Optional[typing.Union["ApplicationGatewayBackendHttpSettingsConnectionDraining", typing.Dict[builtins.str, typing.Any]]] = None,
        host_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        pick_host_name_from_backend_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        probe_name: typing.Optional[builtins.str] = None,
        request_timeout: typing.Optional[jsii.Number] = None,
        trusted_root_certificate_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cookie_based_affinity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#cookie_based_affinity ApplicationGateway#cookie_based_affinity}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#port ApplicationGateway#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#protocol ApplicationGateway#protocol}.
        :param affinity_cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#affinity_cookie_name ApplicationGateway#affinity_cookie_name}.
        :param authentication_certificate: authentication_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#authentication_certificate ApplicationGateway#authentication_certificate}
        :param connection_draining: connection_draining block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#connection_draining ApplicationGateway#connection_draining}
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#host_name ApplicationGateway#host_name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#path ApplicationGateway#path}.
        :param pick_host_name_from_backend_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#pick_host_name_from_backend_address ApplicationGateway#pick_host_name_from_backend_address}.
        :param probe_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#probe_name ApplicationGateway#probe_name}.
        :param request_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_timeout ApplicationGateway#request_timeout}.
        :param trusted_root_certificate_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_root_certificate_names ApplicationGateway#trusted_root_certificate_names}.
        '''
        if isinstance(connection_draining, dict):
            connection_draining = ApplicationGatewayBackendHttpSettingsConnectionDraining(**connection_draining)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54bb34a2cd76b61583d3e05a7efa10d9426bbede66bde8aa6b78d3c95f70b66)
            check_type(argname="argument cookie_based_affinity", value=cookie_based_affinity, expected_type=type_hints["cookie_based_affinity"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument affinity_cookie_name", value=affinity_cookie_name, expected_type=type_hints["affinity_cookie_name"])
            check_type(argname="argument authentication_certificate", value=authentication_certificate, expected_type=type_hints["authentication_certificate"])
            check_type(argname="argument connection_draining", value=connection_draining, expected_type=type_hints["connection_draining"])
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument pick_host_name_from_backend_address", value=pick_host_name_from_backend_address, expected_type=type_hints["pick_host_name_from_backend_address"])
            check_type(argname="argument probe_name", value=probe_name, expected_type=type_hints["probe_name"])
            check_type(argname="argument request_timeout", value=request_timeout, expected_type=type_hints["request_timeout"])
            check_type(argname="argument trusted_root_certificate_names", value=trusted_root_certificate_names, expected_type=type_hints["trusted_root_certificate_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cookie_based_affinity": cookie_based_affinity,
            "name": name,
            "port": port,
            "protocol": protocol,
        }
        if affinity_cookie_name is not None:
            self._values["affinity_cookie_name"] = affinity_cookie_name
        if authentication_certificate is not None:
            self._values["authentication_certificate"] = authentication_certificate
        if connection_draining is not None:
            self._values["connection_draining"] = connection_draining
        if host_name is not None:
            self._values["host_name"] = host_name
        if path is not None:
            self._values["path"] = path
        if pick_host_name_from_backend_address is not None:
            self._values["pick_host_name_from_backend_address"] = pick_host_name_from_backend_address
        if probe_name is not None:
            self._values["probe_name"] = probe_name
        if request_timeout is not None:
            self._values["request_timeout"] = request_timeout
        if trusted_root_certificate_names is not None:
            self._values["trusted_root_certificate_names"] = trusted_root_certificate_names

    @builtins.property
    def cookie_based_affinity(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#cookie_based_affinity ApplicationGateway#cookie_based_affinity}.'''
        result = self._values.get("cookie_based_affinity")
        assert result is not None, "Required property 'cookie_based_affinity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#port ApplicationGateway#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#protocol ApplicationGateway#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def affinity_cookie_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#affinity_cookie_name ApplicationGateway#affinity_cookie_name}.'''
        result = self._values.get("affinity_cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayBackendHttpSettingsAuthenticationCertificate"]]]:
        '''authentication_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#authentication_certificate ApplicationGateway#authentication_certificate}
        '''
        result = self._values.get("authentication_certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayBackendHttpSettingsAuthenticationCertificate"]]], result)

    @builtins.property
    def connection_draining(
        self,
    ) -> typing.Optional["ApplicationGatewayBackendHttpSettingsConnectionDraining"]:
        '''connection_draining block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#connection_draining ApplicationGateway#connection_draining}
        '''
        result = self._values.get("connection_draining")
        return typing.cast(typing.Optional["ApplicationGatewayBackendHttpSettingsConnectionDraining"], result)

    @builtins.property
    def host_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#host_name ApplicationGateway#host_name}.'''
        result = self._values.get("host_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#path ApplicationGateway#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pick_host_name_from_backend_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#pick_host_name_from_backend_address ApplicationGateway#pick_host_name_from_backend_address}.'''
        result = self._values.get("pick_host_name_from_backend_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def probe_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#probe_name ApplicationGateway#probe_name}.'''
        result = self._values.get("probe_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_timeout ApplicationGateway#request_timeout}.'''
        result = self._values.get("request_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trusted_root_certificate_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_root_certificate_names ApplicationGateway#trusted_root_certificate_names}.'''
        result = self._values.get("trusted_root_certificate_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayBackendHttpSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendHttpSettingsAuthenticationCertificate",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ApplicationGatewayBackendHttpSettingsAuthenticationCertificate:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e454512442b4889147cebbff43af59389c1193a8428520e6f26b08d887dac88)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayBackendHttpSettingsAuthenticationCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayBackendHttpSettingsAuthenticationCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendHttpSettingsAuthenticationCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecf4dfc6947ee200684a7408e95ab8f24199c3724394db0c36fc82ea34b8095f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayBackendHttpSettingsAuthenticationCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03e51d9167528a1732f56419fa3ae6c644772814471b1e0c19d84248aba5224)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayBackendHttpSettingsAuthenticationCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea9eaacbc2ac7881b6fa8e6251feee55c165bb755cc51b167130495600ecef6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0bf4dbcc428c602f94ed3309bdc57df60d84cf720957e6b555ad9575aba6f52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36b5e227ce92b7ef0c1ec4a9dd05ff66f56878facc9837d514cb188048c7b5ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abf5f13c03f7f86a0bb1c311dd67e0919e5651b6be0c97492adce94525d75f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayBackendHttpSettingsAuthenticationCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendHttpSettingsAuthenticationCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__657a19cd0d702f96807f84bcf2514f929df9876ab286cb1e7a6fee2a94b94bb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__24eaa1597f9cdcff44dff737b3469e535ee2ad2771e594fe12098ebab0b9994c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081386d3be56465ac0f52b51ce78e7707716061e863b95ff90c90f799e144d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendHttpSettingsConnectionDraining",
    jsii_struct_bases=[],
    name_mapping={"drain_timeout_sec": "drainTimeoutSec", "enabled": "enabled"},
)
class ApplicationGatewayBackendHttpSettingsConnectionDraining:
    def __init__(
        self,
        *,
        drain_timeout_sec: jsii.Number,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param drain_timeout_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#drain_timeout_sec ApplicationGateway#drain_timeout_sec}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#enabled ApplicationGateway#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0011910b9a8ef2dfb486b1801bfe7b27b54594ad1a1725a93d89b2470e0f401)
            check_type(argname="argument drain_timeout_sec", value=drain_timeout_sec, expected_type=type_hints["drain_timeout_sec"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "drain_timeout_sec": drain_timeout_sec,
            "enabled": enabled,
        }

    @builtins.property
    def drain_timeout_sec(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#drain_timeout_sec ApplicationGateway#drain_timeout_sec}.'''
        result = self._values.get("drain_timeout_sec")
        assert result is not None, "Required property 'drain_timeout_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#enabled ApplicationGateway#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayBackendHttpSettingsConnectionDraining(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayBackendHttpSettingsConnectionDrainingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendHttpSettingsConnectionDrainingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f710f4bcae2ffd4f594ee63c18011b05cd21902844cadbada6676c0271559c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="drainTimeoutSecInput")
    def drain_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "drainTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="drainTimeoutSec")
    def drain_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "drainTimeoutSec"))

    @drain_timeout_sec.setter
    def drain_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2b69ba474ea646d92403170b1f6658a72d31f69dd0282a4675b11c8996d4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drainTimeoutSec", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__62499210fe84485e53c12aa766f39a9a7f7375221ab466a28136aabbe75042d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApplicationGatewayBackendHttpSettingsConnectionDraining]:
        return typing.cast(typing.Optional[ApplicationGatewayBackendHttpSettingsConnectionDraining], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationGatewayBackendHttpSettingsConnectionDraining],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea8fb84bc6fa3ff4b5bef70d4c48ead2f64110f93061558c4714622b12243d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayBackendHttpSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendHttpSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f029cbdd92ee635177a2ad305fa92f094bf03645ab73980e1f7f88e05c6f30e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayBackendHttpSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95672651b65931ce7b4fa8f59bd4d70ade7bf7b7769f64aa4705ec87835d3bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayBackendHttpSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03dfc671cbd6301987e4068d491ed60ace9876a6212ebdbc81e0f604b4080e02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbfa93077adbb278303a84e89fcb6caf950019e198dbdd19ece60c46ab3f73a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__085cdb2a75394c8980cd2feb24ffe6df4eb5b0c619a2a30ba90595adea468569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7517557a4b633524455b72c2adf2bc300921c50042bef8b184c0108aeaa79515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayBackendHttpSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayBackendHttpSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac7630ce60086c223cb8287b5a97c15a9cb19633959a7514ed312c493da3f6eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthenticationCertificate")
    def put_authentication_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendHttpSettingsAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8cbc71bcc6297842f6d722933be256acddeca1dafa3a8a9b0f82c9de4495a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthenticationCertificate", [value]))

    @jsii.member(jsii_name="putConnectionDraining")
    def put_connection_draining(
        self,
        *,
        drain_timeout_sec: jsii.Number,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param drain_timeout_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#drain_timeout_sec ApplicationGateway#drain_timeout_sec}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#enabled ApplicationGateway#enabled}.
        '''
        value = ApplicationGatewayBackendHttpSettingsConnectionDraining(
            drain_timeout_sec=drain_timeout_sec, enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putConnectionDraining", [value]))

    @jsii.member(jsii_name="resetAffinityCookieName")
    def reset_affinity_cookie_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAffinityCookieName", []))

    @jsii.member(jsii_name="resetAuthenticationCertificate")
    def reset_authentication_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationCertificate", []))

    @jsii.member(jsii_name="resetConnectionDraining")
    def reset_connection_draining(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionDraining", []))

    @jsii.member(jsii_name="resetHostName")
    def reset_host_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostName", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPickHostNameFromBackendAddress")
    def reset_pick_host_name_from_backend_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPickHostNameFromBackendAddress", []))

    @jsii.member(jsii_name="resetProbeName")
    def reset_probe_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProbeName", []))

    @jsii.member(jsii_name="resetRequestTimeout")
    def reset_request_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestTimeout", []))

    @jsii.member(jsii_name="resetTrustedRootCertificateNames")
    def reset_trusted_root_certificate_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedRootCertificateNames", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationCertificate")
    def authentication_certificate(
        self,
    ) -> ApplicationGatewayBackendHttpSettingsAuthenticationCertificateList:
        return typing.cast(ApplicationGatewayBackendHttpSettingsAuthenticationCertificateList, jsii.get(self, "authenticationCertificate"))

    @builtins.property
    @jsii.member(jsii_name="connectionDraining")
    def connection_draining(
        self,
    ) -> ApplicationGatewayBackendHttpSettingsConnectionDrainingOutputReference:
        return typing.cast(ApplicationGatewayBackendHttpSettingsConnectionDrainingOutputReference, jsii.get(self, "connectionDraining"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="probeId")
    def probe_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "probeId"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieNameInput")
    def affinity_cookie_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "affinityCookieNameInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationCertificateInput")
    def authentication_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]]], jsii.get(self, "authenticationCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionDrainingInput")
    def connection_draining_input(
        self,
    ) -> typing.Optional[ApplicationGatewayBackendHttpSettingsConnectionDraining]:
        return typing.cast(typing.Optional[ApplicationGatewayBackendHttpSettingsConnectionDraining], jsii.get(self, "connectionDrainingInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieBasedAffinityInput")
    def cookie_based_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cookieBasedAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="pickHostNameFromBackendAddressInput")
    def pick_host_name_from_backend_address_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pickHostNameFromBackendAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="probeNameInput")
    def probe_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "probeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="requestTimeoutInput")
    def request_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedRootCertificateNamesInput")
    def trusted_root_certificate_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedRootCertificateNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieName")
    def affinity_cookie_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "affinityCookieName"))

    @affinity_cookie_name.setter
    def affinity_cookie_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03a8ddcf04585fad750328639f1d28e48ba3ebcc63d30e0c8fb7f16521b80f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "affinityCookieName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cookieBasedAffinity")
    def cookie_based_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieBasedAffinity"))

    @cookie_based_affinity.setter
    def cookie_based_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3eb986d863a08fec5857052811983c7f6b44bd63949d5497399edb7834abdb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieBasedAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374723b8def63df462a30779816b16972edac61a4a7456ecf08a75a0d58d4273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe92eb4a3a7c2a96c4045c8af03b232db0a8e4060d1c7c3f6ece975152ec5d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76ef9d3cdbd9111ae5428573f69c9dba96062c27983893eedaa112ef0678be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pickHostNameFromBackendAddress")
    def pick_host_name_from_backend_address(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pickHostNameFromBackendAddress"))

    @pick_host_name_from_backend_address.setter
    def pick_host_name_from_backend_address(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31780d4e997232e1f850ad821a9e8145d5eb595de2e088babcca949c1f5532a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pickHostNameFromBackendAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fbca50917791e438b3dc35c033662b1266045a44cf40a64e003b4ff13ab6314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="probeName")
    def probe_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "probeName"))

    @probe_name.setter
    def probe_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0df4cf6f5101bb53d4903846355f2e2d0558d6ea1e26bc52650228105a7f9db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "probeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604a524a5603ca590acdb24f7d16a1fd92b51df0eebff9c6d6364ad7aec16670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestTimeout")
    def request_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requestTimeout"))

    @request_timeout.setter
    def request_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f679ffee4d2c2b0723d76ea14f4987a9bf2dec93acae64d671dcfa5a6f38a5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedRootCertificateNames")
    def trusted_root_certificate_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedRootCertificateNames"))

    @trusted_root_certificate_names.setter
    def trusted_root_certificate_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc78a358fbe5a1f9c95836435cbc7b5a0e2ce410e2613a5e14ed0bef8f7c63d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedRootCertificateNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendHttpSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendHttpSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendHttpSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c268247603edadfc62a4597145daa17506e6e0fe11f43b3a02b78aa5a6317e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backend_address_pool": "backendAddressPool",
        "backend_http_settings": "backendHttpSettings",
        "frontend_ip_configuration": "frontendIpConfiguration",
        "frontend_port": "frontendPort",
        "gateway_ip_configuration": "gatewayIpConfiguration",
        "http_listener": "httpListener",
        "location": "location",
        "name": "name",
        "request_routing_rule": "requestRoutingRule",
        "resource_group_name": "resourceGroupName",
        "sku": "sku",
        "authentication_certificate": "authenticationCertificate",
        "autoscale_configuration": "autoscaleConfiguration",
        "custom_error_configuration": "customErrorConfiguration",
        "enable_http2": "enableHttp2",
        "fips_enabled": "fipsEnabled",
        "firewall_policy_id": "firewallPolicyId",
        "force_firewall_policy_association": "forceFirewallPolicyAssociation",
        "global_": "global",
        "id": "id",
        "identity": "identity",
        "private_link_configuration": "privateLinkConfiguration",
        "probe": "probe",
        "redirect_configuration": "redirectConfiguration",
        "rewrite_rule_set": "rewriteRuleSet",
        "ssl_certificate": "sslCertificate",
        "ssl_policy": "sslPolicy",
        "ssl_profile": "sslProfile",
        "tags": "tags",
        "timeouts": "timeouts",
        "trusted_client_certificate": "trustedClientCertificate",
        "trusted_root_certificate": "trustedRootCertificate",
        "url_path_map": "urlPathMap",
        "waf_configuration": "wafConfiguration",
        "zones": "zones",
    },
)
class ApplicationGatewayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backend_address_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendAddressPool, typing.Dict[builtins.str, typing.Any]]]],
        backend_http_settings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendHttpSettings, typing.Dict[builtins.str, typing.Any]]]],
        frontend_ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayFrontendIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        frontend_port: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayFrontendPort", typing.Dict[builtins.str, typing.Any]]]],
        gateway_ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayGatewayIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        http_listener: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayHttpListener", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        request_routing_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRequestRoutingRule", typing.Dict[builtins.str, typing.Any]]]],
        resource_group_name: builtins.str,
        sku: typing.Union["ApplicationGatewaySku", typing.Dict[builtins.str, typing.Any]],
        authentication_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
        autoscale_configuration: typing.Optional[typing.Union[ApplicationGatewayAutoscaleConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_error_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayCustomErrorConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        firewall_policy_id: typing.Optional[builtins.str] = None,
        force_firewall_policy_association: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        global_: typing.Optional[typing.Union["ApplicationGatewayGlobal", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ApplicationGatewayIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayProbe", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redirect_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRedirectConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rewrite_rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssl_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewaySslCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssl_policy: typing.Optional[typing.Union["ApplicationGatewaySslPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_profile: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewaySslProfile", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ApplicationGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_client_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayTrustedClientCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        trusted_root_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayTrustedRootCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_path_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayUrlPathMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        waf_configuration: typing.Optional[typing.Union["ApplicationGatewayWafConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backend_address_pool: backend_address_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_address_pool ApplicationGateway#backend_address_pool}
        :param backend_http_settings: backend_http_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_http_settings ApplicationGateway#backend_http_settings}
        :param frontend_ip_configuration: frontend_ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_ip_configuration ApplicationGateway#frontend_ip_configuration}
        :param frontend_port: frontend_port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_port ApplicationGateway#frontend_port}
        :param gateway_ip_configuration: gateway_ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#gateway_ip_configuration ApplicationGateway#gateway_ip_configuration}
        :param http_listener: http_listener block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#http_listener ApplicationGateway#http_listener}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#location ApplicationGateway#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param request_routing_rule: request_routing_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_routing_rule ApplicationGateway#request_routing_rule}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#resource_group_name ApplicationGateway#resource_group_name}.
        :param sku: sku block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#sku ApplicationGateway#sku}
        :param authentication_certificate: authentication_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#authentication_certificate ApplicationGateway#authentication_certificate}
        :param autoscale_configuration: autoscale_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#autoscale_configuration ApplicationGateway#autoscale_configuration}
        :param custom_error_configuration: custom_error_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#custom_error_configuration ApplicationGateway#custom_error_configuration}
        :param enable_http2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#enable_http2 ApplicationGateway#enable_http2}.
        :param fips_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#fips_enabled ApplicationGateway#fips_enabled}.
        :param firewall_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_policy_id ApplicationGateway#firewall_policy_id}.
        :param force_firewall_policy_association: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#force_firewall_policy_association ApplicationGateway#force_firewall_policy_association}.
        :param global_: global block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#global ApplicationGateway#global}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#id ApplicationGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#identity ApplicationGateway#identity}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_link_configuration ApplicationGateway#private_link_configuration}
        :param probe: probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#probe ApplicationGateway#probe}
        :param redirect_configuration: redirect_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#redirect_configuration ApplicationGateway#redirect_configuration}
        :param rewrite_rule_set: rewrite_rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rewrite_rule_set ApplicationGateway#rewrite_rule_set}
        :param ssl_certificate: ssl_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_certificate ApplicationGateway#ssl_certificate}
        :param ssl_policy: ssl_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_policy ApplicationGateway#ssl_policy}
        :param ssl_profile: ssl_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_profile ApplicationGateway#ssl_profile}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#tags ApplicationGateway#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#timeouts ApplicationGateway#timeouts}
        :param trusted_client_certificate: trusted_client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_client_certificate ApplicationGateway#trusted_client_certificate}
        :param trusted_root_certificate: trusted_root_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_root_certificate ApplicationGateway#trusted_root_certificate}
        :param url_path_map: url_path_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#url_path_map ApplicationGateway#url_path_map}
        :param waf_configuration: waf_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#waf_configuration ApplicationGateway#waf_configuration}
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#zones ApplicationGateway#zones}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(sku, dict):
            sku = ApplicationGatewaySku(**sku)
        if isinstance(autoscale_configuration, dict):
            autoscale_configuration = ApplicationGatewayAutoscaleConfiguration(**autoscale_configuration)
        if isinstance(global_, dict):
            global_ = ApplicationGatewayGlobal(**global_)
        if isinstance(identity, dict):
            identity = ApplicationGatewayIdentity(**identity)
        if isinstance(ssl_policy, dict):
            ssl_policy = ApplicationGatewaySslPolicy(**ssl_policy)
        if isinstance(timeouts, dict):
            timeouts = ApplicationGatewayTimeouts(**timeouts)
        if isinstance(waf_configuration, dict):
            waf_configuration = ApplicationGatewayWafConfiguration(**waf_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2914861c7395eccfd51d347790a33a9f80e7bddea0bc020f4e8b0a9b0470bbbe)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backend_address_pool", value=backend_address_pool, expected_type=type_hints["backend_address_pool"])
            check_type(argname="argument backend_http_settings", value=backend_http_settings, expected_type=type_hints["backend_http_settings"])
            check_type(argname="argument frontend_ip_configuration", value=frontend_ip_configuration, expected_type=type_hints["frontend_ip_configuration"])
            check_type(argname="argument frontend_port", value=frontend_port, expected_type=type_hints["frontend_port"])
            check_type(argname="argument gateway_ip_configuration", value=gateway_ip_configuration, expected_type=type_hints["gateway_ip_configuration"])
            check_type(argname="argument http_listener", value=http_listener, expected_type=type_hints["http_listener"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument request_routing_rule", value=request_routing_rule, expected_type=type_hints["request_routing_rule"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument authentication_certificate", value=authentication_certificate, expected_type=type_hints["authentication_certificate"])
            check_type(argname="argument autoscale_configuration", value=autoscale_configuration, expected_type=type_hints["autoscale_configuration"])
            check_type(argname="argument custom_error_configuration", value=custom_error_configuration, expected_type=type_hints["custom_error_configuration"])
            check_type(argname="argument enable_http2", value=enable_http2, expected_type=type_hints["enable_http2"])
            check_type(argname="argument fips_enabled", value=fips_enabled, expected_type=type_hints["fips_enabled"])
            check_type(argname="argument firewall_policy_id", value=firewall_policy_id, expected_type=type_hints["firewall_policy_id"])
            check_type(argname="argument force_firewall_policy_association", value=force_firewall_policy_association, expected_type=type_hints["force_firewall_policy_association"])
            check_type(argname="argument global_", value=global_, expected_type=type_hints["global_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument private_link_configuration", value=private_link_configuration, expected_type=type_hints["private_link_configuration"])
            check_type(argname="argument probe", value=probe, expected_type=type_hints["probe"])
            check_type(argname="argument redirect_configuration", value=redirect_configuration, expected_type=type_hints["redirect_configuration"])
            check_type(argname="argument rewrite_rule_set", value=rewrite_rule_set, expected_type=type_hints["rewrite_rule_set"])
            check_type(argname="argument ssl_certificate", value=ssl_certificate, expected_type=type_hints["ssl_certificate"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
            check_type(argname="argument ssl_profile", value=ssl_profile, expected_type=type_hints["ssl_profile"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument trusted_client_certificate", value=trusted_client_certificate, expected_type=type_hints["trusted_client_certificate"])
            check_type(argname="argument trusted_root_certificate", value=trusted_root_certificate, expected_type=type_hints["trusted_root_certificate"])
            check_type(argname="argument url_path_map", value=url_path_map, expected_type=type_hints["url_path_map"])
            check_type(argname="argument waf_configuration", value=waf_configuration, expected_type=type_hints["waf_configuration"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend_address_pool": backend_address_pool,
            "backend_http_settings": backend_http_settings,
            "frontend_ip_configuration": frontend_ip_configuration,
            "frontend_port": frontend_port,
            "gateway_ip_configuration": gateway_ip_configuration,
            "http_listener": http_listener,
            "location": location,
            "name": name,
            "request_routing_rule": request_routing_rule,
            "resource_group_name": resource_group_name,
            "sku": sku,
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
        if authentication_certificate is not None:
            self._values["authentication_certificate"] = authentication_certificate
        if autoscale_configuration is not None:
            self._values["autoscale_configuration"] = autoscale_configuration
        if custom_error_configuration is not None:
            self._values["custom_error_configuration"] = custom_error_configuration
        if enable_http2 is not None:
            self._values["enable_http2"] = enable_http2
        if fips_enabled is not None:
            self._values["fips_enabled"] = fips_enabled
        if firewall_policy_id is not None:
            self._values["firewall_policy_id"] = firewall_policy_id
        if force_firewall_policy_association is not None:
            self._values["force_firewall_policy_association"] = force_firewall_policy_association
        if global_ is not None:
            self._values["global_"] = global_
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if private_link_configuration is not None:
            self._values["private_link_configuration"] = private_link_configuration
        if probe is not None:
            self._values["probe"] = probe
        if redirect_configuration is not None:
            self._values["redirect_configuration"] = redirect_configuration
        if rewrite_rule_set is not None:
            self._values["rewrite_rule_set"] = rewrite_rule_set
        if ssl_certificate is not None:
            self._values["ssl_certificate"] = ssl_certificate
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
        if ssl_profile is not None:
            self._values["ssl_profile"] = ssl_profile
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if trusted_client_certificate is not None:
            self._values["trusted_client_certificate"] = trusted_client_certificate
        if trusted_root_certificate is not None:
            self._values["trusted_root_certificate"] = trusted_root_certificate
        if url_path_map is not None:
            self._values["url_path_map"] = url_path_map
        if waf_configuration is not None:
            self._values["waf_configuration"] = waf_configuration
        if zones is not None:
            self._values["zones"] = zones

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
    def backend_address_pool(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendAddressPool]]:
        '''backend_address_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_address_pool ApplicationGateway#backend_address_pool}
        '''
        result = self._values.get("backend_address_pool")
        assert result is not None, "Required property 'backend_address_pool' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendAddressPool]], result)

    @builtins.property
    def backend_http_settings(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettings]]:
        '''backend_http_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_http_settings ApplicationGateway#backend_http_settings}
        '''
        result = self._values.get("backend_http_settings")
        assert result is not None, "Required property 'backend_http_settings' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettings]], result)

    @builtins.property
    def frontend_ip_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayFrontendIpConfiguration"]]:
        '''frontend_ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_ip_configuration ApplicationGateway#frontend_ip_configuration}
        '''
        result = self._values.get("frontend_ip_configuration")
        assert result is not None, "Required property 'frontend_ip_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayFrontendIpConfiguration"]], result)

    @builtins.property
    def frontend_port(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayFrontendPort"]]:
        '''frontend_port block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_port ApplicationGateway#frontend_port}
        '''
        result = self._values.get("frontend_port")
        assert result is not None, "Required property 'frontend_port' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayFrontendPort"]], result)

    @builtins.property
    def gateway_ip_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayGatewayIpConfiguration"]]:
        '''gateway_ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#gateway_ip_configuration ApplicationGateway#gateway_ip_configuration}
        '''
        result = self._values.get("gateway_ip_configuration")
        assert result is not None, "Required property 'gateway_ip_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayGatewayIpConfiguration"]], result)

    @builtins.property
    def http_listener(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayHttpListener"]]:
        '''http_listener block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#http_listener ApplicationGateway#http_listener}
        '''
        result = self._values.get("http_listener")
        assert result is not None, "Required property 'http_listener' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayHttpListener"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#location ApplicationGateway#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_routing_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRequestRoutingRule"]]:
        '''request_routing_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_routing_rule ApplicationGateway#request_routing_rule}
        '''
        result = self._values.get("request_routing_rule")
        assert result is not None, "Required property 'request_routing_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRequestRoutingRule"]], result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#resource_group_name ApplicationGateway#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> "ApplicationGatewaySku":
        '''sku block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#sku ApplicationGateway#sku}
        '''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast("ApplicationGatewaySku", result)

    @builtins.property
    def authentication_certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayAuthenticationCertificate]]]:
        '''authentication_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#authentication_certificate ApplicationGateway#authentication_certificate}
        '''
        result = self._values.get("authentication_certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayAuthenticationCertificate]]], result)

    @builtins.property
    def autoscale_configuration(
        self,
    ) -> typing.Optional[ApplicationGatewayAutoscaleConfiguration]:
        '''autoscale_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#autoscale_configuration ApplicationGateway#autoscale_configuration}
        '''
        result = self._values.get("autoscale_configuration")
        return typing.cast(typing.Optional[ApplicationGatewayAutoscaleConfiguration], result)

    @builtins.property
    def custom_error_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayCustomErrorConfiguration"]]]:
        '''custom_error_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#custom_error_configuration ApplicationGateway#custom_error_configuration}
        '''
        result = self._values.get("custom_error_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayCustomErrorConfiguration"]]], result)

    @builtins.property
    def enable_http2(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#enable_http2 ApplicationGateway#enable_http2}.'''
        result = self._values.get("enable_http2")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fips_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#fips_enabled ApplicationGateway#fips_enabled}.'''
        result = self._values.get("fips_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def firewall_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_policy_id ApplicationGateway#firewall_policy_id}.'''
        result = self._values.get("firewall_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_firewall_policy_association(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#force_firewall_policy_association ApplicationGateway#force_firewall_policy_association}.'''
        result = self._values.get("force_firewall_policy_association")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def global_(self) -> typing.Optional["ApplicationGatewayGlobal"]:
        '''global block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#global ApplicationGateway#global}
        '''
        result = self._values.get("global_")
        return typing.cast(typing.Optional["ApplicationGatewayGlobal"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#id ApplicationGateway#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["ApplicationGatewayIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#identity ApplicationGateway#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["ApplicationGatewayIdentity"], result)

    @builtins.property
    def private_link_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayPrivateLinkConfiguration"]]]:
        '''private_link_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_link_configuration ApplicationGateway#private_link_configuration}
        '''
        result = self._values.get("private_link_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayPrivateLinkConfiguration"]]], result)

    @builtins.property
    def probe(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayProbe"]]]:
        '''probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#probe ApplicationGateway#probe}
        '''
        result = self._values.get("probe")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayProbe"]]], result)

    @builtins.property
    def redirect_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRedirectConfiguration"]]]:
        '''redirect_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#redirect_configuration ApplicationGateway#redirect_configuration}
        '''
        result = self._values.get("redirect_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRedirectConfiguration"]]], result)

    @builtins.property
    def rewrite_rule_set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSet"]]]:
        '''rewrite_rule_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rewrite_rule_set ApplicationGateway#rewrite_rule_set}
        '''
        result = self._values.get("rewrite_rule_set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSet"]]], result)

    @builtins.property
    def ssl_certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewaySslCertificate"]]]:
        '''ssl_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_certificate ApplicationGateway#ssl_certificate}
        '''
        result = self._values.get("ssl_certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewaySslCertificate"]]], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional["ApplicationGatewaySslPolicy"]:
        '''ssl_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_policy ApplicationGateway#ssl_policy}
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional["ApplicationGatewaySslPolicy"], result)

    @builtins.property
    def ssl_profile(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewaySslProfile"]]]:
        '''ssl_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_profile ApplicationGateway#ssl_profile}
        '''
        result = self._values.get("ssl_profile")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewaySslProfile"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#tags ApplicationGateway#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApplicationGatewayTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#timeouts ApplicationGateway#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApplicationGatewayTimeouts"], result)

    @builtins.property
    def trusted_client_certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayTrustedClientCertificate"]]]:
        '''trusted_client_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_client_certificate ApplicationGateway#trusted_client_certificate}
        '''
        result = self._values.get("trusted_client_certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayTrustedClientCertificate"]]], result)

    @builtins.property
    def trusted_root_certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayTrustedRootCertificate"]]]:
        '''trusted_root_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_root_certificate ApplicationGateway#trusted_root_certificate}
        '''
        result = self._values.get("trusted_root_certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayTrustedRootCertificate"]]], result)

    @builtins.property
    def url_path_map(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayUrlPathMap"]]]:
        '''url_path_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#url_path_map ApplicationGateway#url_path_map}
        '''
        result = self._values.get("url_path_map")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayUrlPathMap"]]], result)

    @builtins.property
    def waf_configuration(
        self,
    ) -> typing.Optional["ApplicationGatewayWafConfiguration"]:
        '''waf_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#waf_configuration ApplicationGateway#waf_configuration}
        '''
        result = self._values.get("waf_configuration")
        return typing.cast(typing.Optional["ApplicationGatewayWafConfiguration"], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#zones ApplicationGateway#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayCustomErrorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "custom_error_page_url": "customErrorPageUrl",
        "status_code": "statusCode",
    },
)
class ApplicationGatewayCustomErrorConfiguration:
    def __init__(
        self,
        *,
        custom_error_page_url: builtins.str,
        status_code: builtins.str,
    ) -> None:
        '''
        :param custom_error_page_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#custom_error_page_url ApplicationGateway#custom_error_page_url}.
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#status_code ApplicationGateway#status_code}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0e06fbde9147bdd144723eebf5c530da1e2391b7cdd8479fc00cf7e2ceb031)
            check_type(argname="argument custom_error_page_url", value=custom_error_page_url, expected_type=type_hints["custom_error_page_url"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_error_page_url": custom_error_page_url,
            "status_code": status_code,
        }

    @builtins.property
    def custom_error_page_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#custom_error_page_url ApplicationGateway#custom_error_page_url}.'''
        result = self._values.get("custom_error_page_url")
        assert result is not None, "Required property 'custom_error_page_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#status_code ApplicationGateway#status_code}.'''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayCustomErrorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayCustomErrorConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayCustomErrorConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04e064bd6c2471c6a2f351cd674892a66b05be88267c11e93f97cf072d9a51f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayCustomErrorConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c11c89746e5ca15a5fa79d5a2fd34badcf699a787ab8c48ca1f66d3d7a3be20)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayCustomErrorConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc7eeb578807e6b436a0aa2f787a130d12489e7f2ea2cfdeccee8bcd0572e48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81af30144a77c153c1ec286ffd4f982ec97c17044a7f1d5c39ada0f1dd7742f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__225db7a541e4bebfa457d0528888b7815459097dcf01d7d47c331f7a40f4cf77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayCustomErrorConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayCustomErrorConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayCustomErrorConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd44b9def370b6baa5ca8a97d46b9c749cfe49996d1e6734283719a52efff8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayCustomErrorConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayCustomErrorConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79ecc9eb325e866fc71953b4bf1e0dd541f4b85f3cec201b45242c45343fd93b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="customErrorPageUrlInput")
    def custom_error_page_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customErrorPageUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="customErrorPageUrl")
    def custom_error_page_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customErrorPageUrl"))

    @custom_error_page_url.setter
    def custom_error_page_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9b52a91c63ba16ff410104fbe966c9a2bbaf6864332cfd2eb58730f3263a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customErrorPageUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fa1345040e3a95c3fe5effc1275b4f0ea4e52fa0a56bc1a75fd3d616d4ce38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayCustomErrorConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayCustomErrorConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayCustomErrorConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356f448ac6f1d10e2956ca53a74cfd28d0e800671b4f5a91d15d261924c29b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayFrontendIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "private_ip_address": "privateIpAddress",
        "private_ip_address_allocation": "privateIpAddressAllocation",
        "private_link_configuration_name": "privateLinkConfigurationName",
        "public_ip_address_id": "publicIpAddressId",
        "subnet_id": "subnetId",
    },
)
class ApplicationGatewayFrontendIpConfiguration:
    def __init__(
        self,
        *,
        name: builtins.str,
        private_ip_address: typing.Optional[builtins.str] = None,
        private_ip_address_allocation: typing.Optional[builtins.str] = None,
        private_link_configuration_name: typing.Optional[builtins.str] = None,
        public_ip_address_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_ip_address ApplicationGateway#private_ip_address}.
        :param private_ip_address_allocation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_ip_address_allocation ApplicationGateway#private_ip_address_allocation}.
        :param private_link_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_link_configuration_name ApplicationGateway#private_link_configuration_name}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#public_ip_address_id ApplicationGateway#public_ip_address_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#subnet_id ApplicationGateway#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b42ddd2f40acaf4fd04c0dfb442b055c6da5575e6f4afa0331acfbf5a879dcd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument private_ip_address_allocation", value=private_ip_address_allocation, expected_type=type_hints["private_ip_address_allocation"])
            check_type(argname="argument private_link_configuration_name", value=private_link_configuration_name, expected_type=type_hints["private_link_configuration_name"])
            check_type(argname="argument public_ip_address_id", value=public_ip_address_id, expected_type=type_hints["public_ip_address_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if private_ip_address_allocation is not None:
            self._values["private_ip_address_allocation"] = private_ip_address_allocation
        if private_link_configuration_name is not None:
            self._values["private_link_configuration_name"] = private_link_configuration_name
        if public_ip_address_id is not None:
            self._values["public_ip_address_id"] = public_ip_address_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_ip_address ApplicationGateway#private_ip_address}.'''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_address_allocation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_ip_address_allocation ApplicationGateway#private_ip_address_allocation}.'''
        result = self._values.get("private_ip_address_allocation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_link_configuration_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_link_configuration_name ApplicationGateway#private_link_configuration_name}.'''
        result = self._values.get("private_link_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ip_address_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#public_ip_address_id ApplicationGateway#public_ip_address_id}.'''
        result = self._values.get("public_ip_address_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#subnet_id ApplicationGateway#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayFrontendIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayFrontendIpConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayFrontendIpConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f50be89fb11991773105169cdaf0184c4db0598246c31740d9d6b1ec26092ba0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayFrontendIpConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def08b7efac37d1d8bc9e5d8288cc8b31a1e3096f355f4ee1020c135824387ef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayFrontendIpConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119361cb236b1816fc81dd748facfecc15f1117374686b80d5f4f6ee35357388)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43b28dd57d0084ff96ce839b086508c4e0d3566abe3437044d11d8719a6d7351)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27ee7e6f593c5cb04cfa6669dbc13e241eabed036e6cd6cd3dc30677e256e8c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayFrontendIpConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayFrontendIpConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayFrontendIpConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0557a31f712f4708b81690a0de8563cf8c788406b1595bdb19951587388c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayFrontendIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayFrontendIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a6b303c3a4ce9719acda796349acf532e987f9a0facee607525b8938bf80a77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPrivateIpAddress")
    def reset_private_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpAddress", []))

    @jsii.member(jsii_name="resetPrivateIpAddressAllocation")
    def reset_private_ip_address_allocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpAddressAllocation", []))

    @jsii.member(jsii_name="resetPrivateLinkConfigurationName")
    def reset_private_link_configuration_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkConfigurationName", []))

    @jsii.member(jsii_name="resetPublicIpAddressId")
    def reset_public_ip_address_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpAddressId", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfigurationId")
    def private_link_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateLinkConfigurationId"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressAllocationInput")
    def private_ip_address_allocation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressAllocationInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressInput")
    def private_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfigurationNameInput")
    def private_link_configuration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateLinkConfigurationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIdInput")
    def public_ip_address_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIpAddressIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d42cc8ffac5ae5aabe3d85b0c7f6f495cde5c5801d0e104753565dc82e0a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf0b1697af7fa79305f2eca0d7c12a65a5d7a376067acf8fdfc540e74d553b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressAllocation")
    def private_ip_address_allocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddressAllocation"))

    @private_ip_address_allocation.setter
    def private_ip_address_allocation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b248cfcb328407d77a78f9cccdc52c54e765b0c23fcfd47462d0d3975100481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddressAllocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfigurationName")
    def private_link_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateLinkConfigurationName"))

    @private_link_configuration_name.setter
    def private_link_configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2d9948816a2a9881d1105a73c59d6780179531a44b919497dd95633f68bfc71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkConfigurationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressId")
    def public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddressId"))

    @public_ip_address_id.setter
    def public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6788a2eec7ce987f435aab983eb4de4a8eb2a804d91af04aa7b164df632a7fdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab1b51b4de274d4f878413cf387cb7281e2f06c79ecfce602ab0fb84675d65b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayFrontendIpConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayFrontendIpConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayFrontendIpConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49acf8ae25122c55a99cf0fb7996643c94791aba4103d57fc6a7216be7bea9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayFrontendPort",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "port": "port"},
)
class ApplicationGatewayFrontendPort:
    def __init__(self, *, name: builtins.str, port: jsii.Number) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#port ApplicationGateway#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbbf343e81eb87ae42892a4ff70c2ce43e25b0003eb0446ad52673ed4177be1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "port": port,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#port ApplicationGateway#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayFrontendPort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayFrontendPortList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayFrontendPortList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b05ef4f0a7e2de33d62a4d190c05a4a4b5468dd63088b2e6360b785f9804401)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayFrontendPortOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed492f51c0f7d3e036914a77292668aacf6921b31d686ef75c0316e443014e51)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayFrontendPortOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f989fee88dc78b5861dece2986993f5b0f395bf42d5dc83acd87e267bc0859e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8de89d3e5cf9f899aa1b648d954aa12a1221632a90fda09ce3ebafaa7d920fbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fce684f486f88554a96beec5e5b030d6d9b5e79dc4124f6311cae735f3d3038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayFrontendPort]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayFrontendPort]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayFrontendPort]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a984ee003ef06d2bd30af86f831db005713770a5657482203aeb4a11cea6a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayFrontendPortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayFrontendPortOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a71fbe15a5b50ebbe41f651c10003fc78c165eba31a2e85351e3898379275245)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32429bb01f9a9935c9932a964df9fcb368422c3f0f9439bff2b2fcd112f655eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a06301f37044d074122023f74dbc5398f0ef19694c3646e36501924d6722e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayFrontendPort]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayFrontendPort]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayFrontendPort]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648f1cf7decc4ecc6d9911c34b69ceac83e6d6e870cdf94ff7cd7f0aaed6efe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayGatewayIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "subnet_id": "subnetId"},
)
class ApplicationGatewayGatewayIpConfiguration:
    def __init__(self, *, name: builtins.str, subnet_id: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#subnet_id ApplicationGateway#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb626635909190b08d09b7c3dceb7c69dd2a077bfb6a3b0d83d3a7736d24509c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "subnet_id": subnet_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#subnet_id ApplicationGateway#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayGatewayIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayGatewayIpConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayGatewayIpConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31634eeca957fd344969b1dfced9483e4d41850c4e75bcd413e092b201ee7d0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayGatewayIpConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6044dd3938205c538b7727c0990dcbf3ec06c896161917843d82d5ffde5162d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayGatewayIpConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfb50543f8702a60e1971af1d326cb6e0e469b7b232351b03467e975c4c7e43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c2dc0817350cce42e8b46d6f5b48b8cee8dd1e124b12946ccecdd043c9d205f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25ed36dc844f93d7744a8d7fae9dabc4d715e83b47842bd6d607e621b9b2c045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayGatewayIpConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayGatewayIpConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayGatewayIpConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1400b280b1814e8493aa128e48d3842f27570f02db6c2cb56ccf7fda6037e352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayGatewayIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayGatewayIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43763c84e1811b6bc60d9465480bd4cb4db13634f1e4a7b6242c912e07f04a13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2af637d695bde470773768df610b3d8bb52c87a225c77405b99d1986313e3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bdb50c3f1e256557d12eb75c83fb4f047e22dc18ce232f389a5bf290f50fca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayGatewayIpConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayGatewayIpConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayGatewayIpConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde9323940cf19e0b93ec2d6d5af44f1dd4d32a31b3efbe3fa3ac64172997bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayGlobal",
    jsii_struct_bases=[],
    name_mapping={
        "request_buffering_enabled": "requestBufferingEnabled",
        "response_buffering_enabled": "responseBufferingEnabled",
    },
)
class ApplicationGatewayGlobal:
    def __init__(
        self,
        *,
        request_buffering_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        response_buffering_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param request_buffering_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_buffering_enabled ApplicationGateway#request_buffering_enabled}.
        :param response_buffering_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#response_buffering_enabled ApplicationGateway#response_buffering_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06bed0450829d0ab40571ea14d5f3d95cc2d0f49ecccef150e46d3b520b0efe8)
            check_type(argname="argument request_buffering_enabled", value=request_buffering_enabled, expected_type=type_hints["request_buffering_enabled"])
            check_type(argname="argument response_buffering_enabled", value=response_buffering_enabled, expected_type=type_hints["response_buffering_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "request_buffering_enabled": request_buffering_enabled,
            "response_buffering_enabled": response_buffering_enabled,
        }

    @builtins.property
    def request_buffering_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_buffering_enabled ApplicationGateway#request_buffering_enabled}.'''
        result = self._values.get("request_buffering_enabled")
        assert result is not None, "Required property 'request_buffering_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def response_buffering_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#response_buffering_enabled ApplicationGateway#response_buffering_enabled}.'''
        result = self._values.get("response_buffering_enabled")
        assert result is not None, "Required property 'response_buffering_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayGlobal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayGlobalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayGlobalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f22a9e6d2156bfa937866bc69fc98458fde27aba4d861dd55622846122ab845)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="requestBufferingEnabledInput")
    def request_buffering_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestBufferingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="responseBufferingEnabledInput")
    def response_buffering_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "responseBufferingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBufferingEnabled")
    def request_buffering_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestBufferingEnabled"))

    @request_buffering_enabled.setter
    def request_buffering_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcde820483ef404974ca13d836b89535250e28513cd1182d5b7fec1aff46773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestBufferingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseBufferingEnabled")
    def response_buffering_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "responseBufferingEnabled"))

    @response_buffering_enabled.setter
    def response_buffering_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4eeb003bf2173bb9a547a687d98e2bf8b582d5e7c777fb37c6f461fbece500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseBufferingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationGatewayGlobal]:
        return typing.cast(typing.Optional[ApplicationGatewayGlobal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApplicationGatewayGlobal]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80eec620a5fada844bc18440f2b6cfcbb1d6773ae668de1f9a17bf246c716812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayHttpListener",
    jsii_struct_bases=[],
    name_mapping={
        "frontend_ip_configuration_name": "frontendIpConfigurationName",
        "frontend_port_name": "frontendPortName",
        "name": "name",
        "protocol": "protocol",
        "custom_error_configuration": "customErrorConfiguration",
        "firewall_policy_id": "firewallPolicyId",
        "host_name": "hostName",
        "host_names": "hostNames",
        "require_sni": "requireSni",
        "ssl_certificate_name": "sslCertificateName",
        "ssl_profile_name": "sslProfileName",
    },
)
class ApplicationGatewayHttpListener:
    def __init__(
        self,
        *,
        frontend_ip_configuration_name: builtins.str,
        frontend_port_name: builtins.str,
        name: builtins.str,
        protocol: builtins.str,
        custom_error_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayHttpListenerCustomErrorConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        firewall_policy_id: typing.Optional[builtins.str] = None,
        host_name: typing.Optional[builtins.str] = None,
        host_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        require_sni: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_certificate_name: typing.Optional[builtins.str] = None,
        ssl_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frontend_ip_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_ip_configuration_name ApplicationGateway#frontend_ip_configuration_name}.
        :param frontend_port_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_port_name ApplicationGateway#frontend_port_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#protocol ApplicationGateway#protocol}.
        :param custom_error_configuration: custom_error_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#custom_error_configuration ApplicationGateway#custom_error_configuration}
        :param firewall_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_policy_id ApplicationGateway#firewall_policy_id}.
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#host_name ApplicationGateway#host_name}.
        :param host_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#host_names ApplicationGateway#host_names}.
        :param require_sni: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#require_sni ApplicationGateway#require_sni}.
        :param ssl_certificate_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_certificate_name ApplicationGateway#ssl_certificate_name}.
        :param ssl_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_profile_name ApplicationGateway#ssl_profile_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4493cf1c9d9ff39967bd03e148a940036ea0a62bce26e313b379203c6680e419)
            check_type(argname="argument frontend_ip_configuration_name", value=frontend_ip_configuration_name, expected_type=type_hints["frontend_ip_configuration_name"])
            check_type(argname="argument frontend_port_name", value=frontend_port_name, expected_type=type_hints["frontend_port_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument custom_error_configuration", value=custom_error_configuration, expected_type=type_hints["custom_error_configuration"])
            check_type(argname="argument firewall_policy_id", value=firewall_policy_id, expected_type=type_hints["firewall_policy_id"])
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument host_names", value=host_names, expected_type=type_hints["host_names"])
            check_type(argname="argument require_sni", value=require_sni, expected_type=type_hints["require_sni"])
            check_type(argname="argument ssl_certificate_name", value=ssl_certificate_name, expected_type=type_hints["ssl_certificate_name"])
            check_type(argname="argument ssl_profile_name", value=ssl_profile_name, expected_type=type_hints["ssl_profile_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frontend_ip_configuration_name": frontend_ip_configuration_name,
            "frontend_port_name": frontend_port_name,
            "name": name,
            "protocol": protocol,
        }
        if custom_error_configuration is not None:
            self._values["custom_error_configuration"] = custom_error_configuration
        if firewall_policy_id is not None:
            self._values["firewall_policy_id"] = firewall_policy_id
        if host_name is not None:
            self._values["host_name"] = host_name
        if host_names is not None:
            self._values["host_names"] = host_names
        if require_sni is not None:
            self._values["require_sni"] = require_sni
        if ssl_certificate_name is not None:
            self._values["ssl_certificate_name"] = ssl_certificate_name
        if ssl_profile_name is not None:
            self._values["ssl_profile_name"] = ssl_profile_name

    @builtins.property
    def frontend_ip_configuration_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_ip_configuration_name ApplicationGateway#frontend_ip_configuration_name}.'''
        result = self._values.get("frontend_ip_configuration_name")
        assert result is not None, "Required property 'frontend_ip_configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def frontend_port_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#frontend_port_name ApplicationGateway#frontend_port_name}.'''
        result = self._values.get("frontend_port_name")
        assert result is not None, "Required property 'frontend_port_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#protocol ApplicationGateway#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_error_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayHttpListenerCustomErrorConfiguration"]]]:
        '''custom_error_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#custom_error_configuration ApplicationGateway#custom_error_configuration}
        '''
        result = self._values.get("custom_error_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayHttpListenerCustomErrorConfiguration"]]], result)

    @builtins.property
    def firewall_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_policy_id ApplicationGateway#firewall_policy_id}.'''
        result = self._values.get("firewall_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#host_name ApplicationGateway#host_name}.'''
        result = self._values.get("host_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#host_names ApplicationGateway#host_names}.'''
        result = self._values.get("host_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def require_sni(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#require_sni ApplicationGateway#require_sni}.'''
        result = self._values.get("require_sni")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_certificate_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_certificate_name ApplicationGateway#ssl_certificate_name}.'''
        result = self._values.get("ssl_certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_profile_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_profile_name ApplicationGateway#ssl_profile_name}.'''
        result = self._values.get("ssl_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayHttpListener(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayHttpListenerCustomErrorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "custom_error_page_url": "customErrorPageUrl",
        "status_code": "statusCode",
    },
)
class ApplicationGatewayHttpListenerCustomErrorConfiguration:
    def __init__(
        self,
        *,
        custom_error_page_url: builtins.str,
        status_code: builtins.str,
    ) -> None:
        '''
        :param custom_error_page_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#custom_error_page_url ApplicationGateway#custom_error_page_url}.
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#status_code ApplicationGateway#status_code}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f308de883db20092eb238fc1d37c1ba602e5695f25f27d5de65711371a1cdb88)
            check_type(argname="argument custom_error_page_url", value=custom_error_page_url, expected_type=type_hints["custom_error_page_url"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_error_page_url": custom_error_page_url,
            "status_code": status_code,
        }

    @builtins.property
    def custom_error_page_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#custom_error_page_url ApplicationGateway#custom_error_page_url}.'''
        result = self._values.get("custom_error_page_url")
        assert result is not None, "Required property 'custom_error_page_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#status_code ApplicationGateway#status_code}.'''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayHttpListenerCustomErrorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayHttpListenerCustomErrorConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayHttpListenerCustomErrorConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39acc46c00cfa46de7ae93d709a92008fc51e9c5e266d2ec0ca988bb604b1df7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayHttpListenerCustomErrorConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ab99e18dc2395d5dcf5358750e6242b187c0a34c168d19e57d1b07f67481ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayHttpListenerCustomErrorConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6e1d9dcc3f49c4d0df686ad48aa39828c1a892ba6c57a23fcd337344da5cb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9833557baf9b7eb6040aa23e8239af431ca55b0d5fccdaad505f9ee3f7bab04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d19dc11431e9c5df8cc33b672812ba73656a90c6fa857ebff0d0b41164637bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListenerCustomErrorConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListenerCustomErrorConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListenerCustomErrorConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e49b2d7adc86861ba71d3405ee89c196935867bb1b9a8e664ed670a448e9a987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayHttpListenerCustomErrorConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayHttpListenerCustomErrorConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f2abd279033f517d7267f8c10c8100261b94b04abe7f911d413eb9a4a1371cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="customErrorPageUrlInput")
    def custom_error_page_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customErrorPageUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="customErrorPageUrl")
    def custom_error_page_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customErrorPageUrl"))

    @custom_error_page_url.setter
    def custom_error_page_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140664298172cc8ad7e3cf1ce3c885715fbb54d89d5fb3311983a93b47a299ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customErrorPageUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f8f4f2e9d7d00b2205ae515d4735773ed941ceee733a1f4a42803874d49eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayHttpListenerCustomErrorConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayHttpListenerCustomErrorConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayHttpListenerCustomErrorConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c4d6fe47afafa3c76e00002cc160f3a070c026989b77d7f9807a863391a647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayHttpListenerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayHttpListenerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1c6f7b93fc6429c6f1146bb5e64e09ad9e627b35ecf4f9586acc9a0ef792851)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayHttpListenerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1e5686cce489564e7d7e85ddd20213183746bbc911ba94a2dea81a8f0cd5a2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayHttpListenerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb55da52bcdbc4334c295537b967fb1deffffb1e04d0c3b739a1b92be34d068)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a1a47b8e7a9fc40b362686b08006ec7bfebf237947b14c224418cd2046b418a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ed3879c8ab5abc45d276a09149fcc67cbbec5b5b7baad59168a3148d1a340c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListener]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListener]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListener]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af597999966cee3712b1a7449196a85fe8060865e3008cc746828a1f5d51af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayHttpListenerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayHttpListenerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d5bdf5bcf5ff5ea0720c3c40b1ef1f96b9c7f2523fa0bb687742ef9ba3d8776)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomErrorConfiguration")
    def put_custom_error_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayHttpListenerCustomErrorConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afb3e7b2b35eefdae423b8bb9f44815d9f76863e76d2caa8f0e829a237fcf40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomErrorConfiguration", [value]))

    @jsii.member(jsii_name="resetCustomErrorConfiguration")
    def reset_custom_error_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomErrorConfiguration", []))

    @jsii.member(jsii_name="resetFirewallPolicyId")
    def reset_firewall_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirewallPolicyId", []))

    @jsii.member(jsii_name="resetHostName")
    def reset_host_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostName", []))

    @jsii.member(jsii_name="resetHostNames")
    def reset_host_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostNames", []))

    @jsii.member(jsii_name="resetRequireSni")
    def reset_require_sni(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireSni", []))

    @jsii.member(jsii_name="resetSslCertificateName")
    def reset_ssl_certificate_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertificateName", []))

    @jsii.member(jsii_name="resetSslProfileName")
    def reset_ssl_profile_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslProfileName", []))

    @builtins.property
    @jsii.member(jsii_name="customErrorConfiguration")
    def custom_error_configuration(
        self,
    ) -> ApplicationGatewayHttpListenerCustomErrorConfigurationList:
        return typing.cast(ApplicationGatewayHttpListenerCustomErrorConfigurationList, jsii.get(self, "customErrorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="frontendIpConfigurationId")
    def frontend_ip_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frontendIpConfigurationId"))

    @builtins.property
    @jsii.member(jsii_name="frontendPortId")
    def frontend_port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frontendPortId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="sslCertificateId")
    def ssl_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertificateId"))

    @builtins.property
    @jsii.member(jsii_name="sslProfileId")
    def ssl_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslProfileId"))

    @builtins.property
    @jsii.member(jsii_name="customErrorConfigurationInput")
    def custom_error_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListenerCustomErrorConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListenerCustomErrorConfiguration]]], jsii.get(self, "customErrorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyIdInput")
    def firewall_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendIpConfigurationNameInput")
    def frontend_ip_configuration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frontendIpConfigurationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendPortNameInput")
    def frontend_port_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frontendPortNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNamesInput")
    def host_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="requireSniInput")
    def require_sni_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireSniInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertificateNameInput")
    def ssl_certificate_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertificateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sslProfileNameInput")
    def ssl_profile_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslProfileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyId")
    def firewall_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyId"))

    @firewall_policy_id.setter
    def firewall_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c0b40210a8af590316f00a290844dcd8d4828600a7534be3ae9353c08c6aa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendIpConfigurationName")
    def frontend_ip_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frontendIpConfigurationName"))

    @frontend_ip_configuration_name.setter
    def frontend_ip_configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85328c589aae96ca9e3509ee7d6383cd6778f2b2b0ff3b831009c76e3e772603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendIpConfigurationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendPortName")
    def frontend_port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frontendPortName"))

    @frontend_port_name.setter
    def frontend_port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1e80aa02cfdefc4cf42f2156f4d5eb2426a4ff15bc9689b89aeb10c689e022d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendPortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c464da395905681ab3118efb7c5cab73c46765670fc347168ba2d601fdc8cd32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostNames")
    def host_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostNames"))

    @host_names.setter
    def host_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693486cf847ca2e3fdefe57b7ae9b8243b8c101edb67bc4b8fd8d1b0ae05b39d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfd73014b26ebe5b46c39fbe68dae7966117b7b2a517635e474f1ecb0be9420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672130b97fcc1a960995b3e7cc6d2723337a4adf1dc74ab1214680b8057237de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireSni")
    def require_sni(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireSni"))

    @require_sni.setter
    def require_sni(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145acbad85f5b4304847ec7e9a164fdbec5d2359bc5d0ddaf82db909bd28dc64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireSni", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertificateName")
    def ssl_certificate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertificateName"))

    @ssl_certificate_name.setter
    def ssl_certificate_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba2bb4e1b8d2fd68b1511b201d48644c481137e625ae4194c6b779ac386ede2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertificateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslProfileName")
    def ssl_profile_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslProfileName"))

    @ssl_profile_name.setter
    def ssl_profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e48029a5a0036ae654c181132ea562175300f54ff606fa00200287b1f41f69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslProfileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayHttpListener]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayHttpListener]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayHttpListener]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973027468e3c94a8c965eaee54183812869491771ddd9ca7235061fc36ce5c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class ApplicationGatewayIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#type ApplicationGateway#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#identity_ids ApplicationGateway#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00060493fa92e4c69f27b912c6c8961df09126b764804ef03398d76386a4a5f8)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#type ApplicationGateway#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#identity_ids ApplicationGateway#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5685b47fbc55b88e506492e030e7dd74871e0c9b98cadc34bc0c837bb70c15b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10146d5e6005381bca1a68340bbe6401b728e599a05e8c0e5d62527ed6fd9748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9fc754d0976c6350be2cf6ca66ed61db2cf8ed31f72c964ab1566fb895a10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationGatewayIdentity]:
        return typing.cast(typing.Optional[ApplicationGatewayIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationGatewayIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974ca81a7ec0b8f659f3b14a06e6ae7532a79cba14e20677ca4d7dd62dafaa70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayPrivateEndpointConnection",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApplicationGatewayPrivateEndpointConnection:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayPrivateEndpointConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayPrivateEndpointConnectionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayPrivateEndpointConnectionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__251cdabb77b1f6a0b2e5fa406eefb23e5727cedfd46225122727743ed0088691)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayPrivateEndpointConnectionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca25085adf39653da68951a28ab3e879e0cfd55aca819926257f1ace7eba9eec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayPrivateEndpointConnectionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455a0d913a5d1d4db05c095845602f12dca2eaa2999206ca8909e29bf5b06284)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eec384649af67d45826f48fbf3e38c55782c0ac0399a38268f366a56b73287c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8faf0e6ba35a690f41cb84c39f45b083ffb8c2701ed7e454a89761e14525386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayPrivateEndpointConnectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayPrivateEndpointConnectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51079c926de10119308bed41d62aa36c6e4ecf8dac1a5c89d7df14750fee0a54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApplicationGatewayPrivateEndpointConnection]:
        return typing.cast(typing.Optional[ApplicationGatewayPrivateEndpointConnection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationGatewayPrivateEndpointConnection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a469fe9ceaddd53e9b71547b6191c52d7a204a94fae4cfecfb90cafa25ae3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayPrivateLinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"ip_configuration": "ipConfiguration", "name": "name"},
)
class ApplicationGatewayPrivateLinkConfiguration:
    def __init__(
        self,
        *,
        ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayPrivateLinkConfigurationIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
    ) -> None:
        '''
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ip_configuration ApplicationGateway#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936360ceffca64082e8feae55b720a29bc30d159f22064a3890071b303b51131)
            check_type(argname="argument ip_configuration", value=ip_configuration, expected_type=type_hints["ip_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_configuration": ip_configuration,
            "name": name,
        }

    @builtins.property
    def ip_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayPrivateLinkConfigurationIpConfiguration"]]:
        '''ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ip_configuration ApplicationGateway#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        assert result is not None, "Required property 'ip_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayPrivateLinkConfigurationIpConfiguration"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayPrivateLinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayPrivateLinkConfigurationIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "primary": "primary",
        "private_ip_address_allocation": "privateIpAddressAllocation",
        "subnet_id": "subnetId",
        "private_ip_address": "privateIpAddress",
    },
)
class ApplicationGatewayPrivateLinkConfigurationIpConfiguration:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        private_ip_address_allocation: builtins.str,
        subnet_id: builtins.str,
        private_ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#primary ApplicationGateway#primary}.
        :param private_ip_address_allocation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_ip_address_allocation ApplicationGateway#private_ip_address_allocation}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#subnet_id ApplicationGateway#subnet_id}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_ip_address ApplicationGateway#private_ip_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fba20740bdc1f1f740fd7a3fa4e6d3685d7bf1f9500cb0622d1cb5d05a4b164)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument private_ip_address_allocation", value=private_ip_address_allocation, expected_type=type_hints["private_ip_address_allocation"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "primary": primary,
            "private_ip_address_allocation": private_ip_address_allocation,
            "subnet_id": subnet_id,
        }
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#primary ApplicationGateway#primary}.'''
        result = self._values.get("primary")
        assert result is not None, "Required property 'primary' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def private_ip_address_allocation(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_ip_address_allocation ApplicationGateway#private_ip_address_allocation}.'''
        result = self._values.get("private_ip_address_allocation")
        assert result is not None, "Required property 'private_ip_address_allocation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#subnet_id ApplicationGateway#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#private_ip_address ApplicationGateway#private_ip_address}.'''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayPrivateLinkConfigurationIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayPrivateLinkConfigurationIpConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayPrivateLinkConfigurationIpConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb4fd9014a56388bc5ed58ceb16615be67b3e6a6813000e46e0cb5ec1d7732b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayPrivateLinkConfigurationIpConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe97b14a437a6de232e63e05f1b6a98669997948a599e892d575c47fdfb04ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayPrivateLinkConfigurationIpConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b49f986d50734cb73684633c9754b857caa6e94750791356faf3c6ea74682ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__997add75eba448e49fde239f605db23fc27c8d38ee79839aecfd19c57cecb03b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6b67c3c0a31edc68afca6f21b623c58e6f666176edbdb708a36298fb5b280b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfigurationIpConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfigurationIpConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfigurationIpConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135979c5dde05bce480fa5cdfeb1e8896696310264a3b778c4d3b9adf8572422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayPrivateLinkConfigurationIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayPrivateLinkConfigurationIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23956509891597efaca8596367223e09bc03d6e921e4daff6d139e5d9a0d1f3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPrivateIpAddress")
    def reset_private_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpAddress", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryInput")
    def primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressAllocationInput")
    def private_ip_address_allocation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressAllocationInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressInput")
    def private_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee668fa2e662ff78e51319fe949f90636bebf8ad44e206bcd869fe383954c078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primary"))

    @primary.setter
    def primary(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804be6f8a0d50cdfd0a2ff18eef5e62ad54358d23b32785a1c77c271c970355f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33be3d8b994906c1f6666a801d1346ecc71cd5662c5a3c814fa422891f26d0e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressAllocation")
    def private_ip_address_allocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddressAllocation"))

    @private_ip_address_allocation.setter
    def private_ip_address_allocation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17825cfe8550a1cbf40dc0e8f18873b9a3ea5d8a668fae0e2e81c18ca08c4661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddressAllocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991d9c0ca307e1994e725cb0a9d9b52ba0d6dd7e5502ed59abd3421236407b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayPrivateLinkConfigurationIpConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayPrivateLinkConfigurationIpConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayPrivateLinkConfigurationIpConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6646611441a9b8d2a53f22f1305cca0c5cd7ecb3132bae15fc86d217ddb0baa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayPrivateLinkConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayPrivateLinkConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fafd5be04062edebbd2c0c23ba5922d0009e68b2342fc2ec89ed7f5e376d851)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayPrivateLinkConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ebc9e90076826569d462b021b4fa4d268e8d5a5daaf93892f9d06063da1a87)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayPrivateLinkConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1def671665106d0a378f57a879ef56159e81dd17f2b4419bdcf9e2d7ea0cad4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b80002dfecd780deef0785383df9b4b5b47ac3e9270d3f94fdf94e339ddd44f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85dc10ba1f71467e6a70dec24bda8d8912b7cf1236671ff36843508ac692cce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73890eaf14013156d17451926c97d5bb9b3bee7c9451972b2b1f7d84966dad6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayPrivateLinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayPrivateLinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cea9df0706af3e3048eef301a4ac992db4e4b6c56d3e505c26b8c3d0c951598)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIpConfiguration")
    def put_ip_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayPrivateLinkConfigurationIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f9a87ea7441675e44d505b4d65b3da5246e7316687a61bf2715b81605db2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(
        self,
    ) -> ApplicationGatewayPrivateLinkConfigurationIpConfigurationList:
        return typing.cast(ApplicationGatewayPrivateLinkConfigurationIpConfigurationList, jsii.get(self, "ipConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfigurationIpConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfigurationIpConfiguration]]], jsii.get(self, "ipConfigurationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1f005a60e0df004f4785cfd8a615627d8c2ca233343b28babe7e4ac23efcb958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayPrivateLinkConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayPrivateLinkConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayPrivateLinkConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aca7d060816b3255144f4078f9c22e9163ac729946159326c5198af033a72d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayProbe",
    jsii_struct_bases=[],
    name_mapping={
        "interval": "interval",
        "name": "name",
        "path": "path",
        "protocol": "protocol",
        "timeout": "timeout",
        "unhealthy_threshold": "unhealthyThreshold",
        "host": "host",
        "match": "match",
        "minimum_servers": "minimumServers",
        "pick_host_name_from_backend_http_settings": "pickHostNameFromBackendHttpSettings",
        "port": "port",
    },
)
class ApplicationGatewayProbe:
    def __init__(
        self,
        *,
        interval: jsii.Number,
        name: builtins.str,
        path: builtins.str,
        protocol: builtins.str,
        timeout: jsii.Number,
        unhealthy_threshold: jsii.Number,
        host: typing.Optional[builtins.str] = None,
        match: typing.Optional[typing.Union["ApplicationGatewayProbeMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        minimum_servers: typing.Optional[jsii.Number] = None,
        pick_host_name_from_backend_http_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#interval ApplicationGateway#interval}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#path ApplicationGateway#path}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#protocol ApplicationGateway#protocol}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#timeout ApplicationGateway#timeout}.
        :param unhealthy_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#unhealthy_threshold ApplicationGateway#unhealthy_threshold}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#host ApplicationGateway#host}.
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#match ApplicationGateway#match}
        :param minimum_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#minimum_servers ApplicationGateway#minimum_servers}.
        :param pick_host_name_from_backend_http_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#pick_host_name_from_backend_http_settings ApplicationGateway#pick_host_name_from_backend_http_settings}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#port ApplicationGateway#port}.
        '''
        if isinstance(match, dict):
            match = ApplicationGatewayProbeMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc4b601cc073e15e0fd292572430a667cc8e63e5d04272aa7379c8496e86b96)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument minimum_servers", value=minimum_servers, expected_type=type_hints["minimum_servers"])
            check_type(argname="argument pick_host_name_from_backend_http_settings", value=pick_host_name_from_backend_http_settings, expected_type=type_hints["pick_host_name_from_backend_http_settings"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "name": name,
            "path": path,
            "protocol": protocol,
            "timeout": timeout,
            "unhealthy_threshold": unhealthy_threshold,
        }
        if host is not None:
            self._values["host"] = host
        if match is not None:
            self._values["match"] = match
        if minimum_servers is not None:
            self._values["minimum_servers"] = minimum_servers
        if pick_host_name_from_backend_http_settings is not None:
            self._values["pick_host_name_from_backend_http_settings"] = pick_host_name_from_backend_http_settings
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#interval ApplicationGateway#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#path ApplicationGateway#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#protocol ApplicationGateway#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeout(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#timeout ApplicationGateway#timeout}.'''
        result = self._values.get("timeout")
        assert result is not None, "Required property 'timeout' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def unhealthy_threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#unhealthy_threshold ApplicationGateway#unhealthy_threshold}.'''
        result = self._values.get("unhealthy_threshold")
        assert result is not None, "Required property 'unhealthy_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#host ApplicationGateway#host}.'''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match(self) -> typing.Optional["ApplicationGatewayProbeMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#match ApplicationGateway#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["ApplicationGatewayProbeMatch"], result)

    @builtins.property
    def minimum_servers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#minimum_servers ApplicationGateway#minimum_servers}.'''
        result = self._values.get("minimum_servers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pick_host_name_from_backend_http_settings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#pick_host_name_from_backend_http_settings ApplicationGateway#pick_host_name_from_backend_http_settings}.'''
        result = self._values.get("pick_host_name_from_backend_http_settings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#port ApplicationGateway#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayProbeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayProbeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0980ad9449c049657a84a3c696eb2b277fd697815096c13f52a6b668d178a40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApplicationGatewayProbeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693ffd566cbe474eaf30a4e3e3927fe2fe3e4dab8bc698257f84daa483c19fbe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayProbeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c4a9639ef5194bb782bda2d2a4f1265a14ac85430ff5ce5149b2b679f10a1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed81d613ff22c1ec5a23cce5d3636abc20371afbca6863097f33d9c4cded2484)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f4817fcef37724fe05f5c147e8bd42e1f402dd15d14fd896a96d88372d9151f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayProbe]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayProbe]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e9ca98ffb7b737f6ee290923ee58b951657a82d040248c9062931ac4faffed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayProbeMatch",
    jsii_struct_bases=[],
    name_mapping={"status_code": "statusCode", "body": "body"},
)
class ApplicationGatewayProbeMatch:
    def __init__(
        self,
        *,
        status_code: typing.Sequence[builtins.str],
        body: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#status_code ApplicationGateway#status_code}.
        :param body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#body ApplicationGateway#body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d98d0a77a223da60a34da6783b5fa876307ebf27340c953c893ddd253ddf28)
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status_code": status_code,
        }
        if body is not None:
            self._values["body"] = body

    @builtins.property
    def status_code(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#status_code ApplicationGateway#status_code}.'''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#body ApplicationGateway#body}.'''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayProbeMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayProbeMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayProbeMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__befaa13a0fab5a16822059510b838bd9e83bf9b52d7e5270e5dbab2cb6f9f10f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92b27b243cfaa1cb41b263388d586075f3f75f17d4bcdca6d06a1ae3efbdc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d01d845d6453ec037a56200f8fc66cc2cb226f1162ed576c0cf406f9f96519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationGatewayProbeMatch]:
        return typing.cast(typing.Optional[ApplicationGatewayProbeMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationGatewayProbeMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f526c084274ca6383d427d291f72cb82773fbac0deecaa63781f6122cc130452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19fd2bf3b838a023797eb8816c8e01912d00bc029d4840831bd94ba8cdf19da7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        status_code: typing.Sequence[builtins.str],
        body: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#status_code ApplicationGateway#status_code}.
        :param body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#body ApplicationGateway#body}.
        '''
        value = ApplicationGatewayProbeMatch(status_code=status_code, body=body)

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetMinimumServers")
    def reset_minimum_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumServers", []))

    @jsii.member(jsii_name="resetPickHostNameFromBackendHttpSettings")
    def reset_pick_host_name_from_backend_http_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPickHostNameFromBackendHttpSettings", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> ApplicationGatewayProbeMatchOutputReference:
        return typing.cast(ApplicationGatewayProbeMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[ApplicationGatewayProbeMatch]:
        return typing.cast(typing.Optional[ApplicationGatewayProbeMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumServersInput")
    def minimum_servers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumServersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="pickHostNameFromBackendHttpSettingsInput")
    def pick_host_name_from_backend_http_settings_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pickHostNameFromBackendHttpSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="unhealthyThresholdInput")
    def unhealthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unhealthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18280dfe7ddfa4969414d16455dea46b6f793a69cc89f2f5d8e8a95269c93de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d907b2aca5813556f60351ee8c04473e9a5266389563bf9fff415a3215a05c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumServers")
    def minimum_servers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumServers"))

    @minimum_servers.setter
    def minimum_servers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35d0ccec745c4857fe26912e8278f6b19112aca9a3d6f8a4a4740bd3b28dc40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d341ea4f7a1de0347b5dd9e52670bca15374ca9808d170adc9a5c2bcad6c273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84d139a225db7beb212025e47c3683759b021d5dafcbca8ce9c9f4a3b0c73d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pickHostNameFromBackendHttpSettings")
    def pick_host_name_from_backend_http_settings(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pickHostNameFromBackendHttpSettings"))

    @pick_host_name_from_backend_http_settings.setter
    def pick_host_name_from_backend_http_settings(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1377368f319a3f3693035d4750162d37764170944ccbba2da543bea8c2abea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pickHostNameFromBackendHttpSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04421f2f0fc86ab9baf28ebe334dc55d855cbb7551a6f0bfd86821224accad87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba092d9255742c2950589f8db7c9c66bc135dcfcd967171b84aecfbecdbc487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d299e0ffd5fda0083520f6940423c4ae6f4e5008432509ef636e805c9410ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unhealthyThreshold")
    def unhealthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unhealthyThreshold"))

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122bd15243902eba63d2c34af4b7939d0f1e52410af3b7fdb5aad6eee9a7b44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unhealthyThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayProbe]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayProbe]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayProbe]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0e95dbf96843a0e022d9208d41fc8311a7a702fb7805ca862668e1268da3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRedirectConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "redirect_type": "redirectType",
        "include_path": "includePath",
        "include_query_string": "includeQueryString",
        "target_listener_name": "targetListenerName",
        "target_url": "targetUrl",
    },
)
class ApplicationGatewayRedirectConfiguration:
    def __init__(
        self,
        *,
        name: builtins.str,
        redirect_type: builtins.str,
        include_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target_listener_name: typing.Optional[builtins.str] = None,
        target_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param redirect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#redirect_type ApplicationGateway#redirect_type}.
        :param include_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#include_path ApplicationGateway#include_path}.
        :param include_query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#include_query_string ApplicationGateway#include_query_string}.
        :param target_listener_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#target_listener_name ApplicationGateway#target_listener_name}.
        :param target_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#target_url ApplicationGateway#target_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efaad215a85925ab5ef0cb38081f5daf5be4bac57adb499665d5ac71eb5729b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument redirect_type", value=redirect_type, expected_type=type_hints["redirect_type"])
            check_type(argname="argument include_path", value=include_path, expected_type=type_hints["include_path"])
            check_type(argname="argument include_query_string", value=include_query_string, expected_type=type_hints["include_query_string"])
            check_type(argname="argument target_listener_name", value=target_listener_name, expected_type=type_hints["target_listener_name"])
            check_type(argname="argument target_url", value=target_url, expected_type=type_hints["target_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "redirect_type": redirect_type,
        }
        if include_path is not None:
            self._values["include_path"] = include_path
        if include_query_string is not None:
            self._values["include_query_string"] = include_query_string
        if target_listener_name is not None:
            self._values["target_listener_name"] = target_listener_name
        if target_url is not None:
            self._values["target_url"] = target_url

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def redirect_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#redirect_type ApplicationGateway#redirect_type}.'''
        result = self._values.get("redirect_type")
        assert result is not None, "Required property 'redirect_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_path(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#include_path ApplicationGateway#include_path}.'''
        result = self._values.get("include_path")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_query_string(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#include_query_string ApplicationGateway#include_query_string}.'''
        result = self._values.get("include_query_string")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def target_listener_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#target_listener_name ApplicationGateway#target_listener_name}.'''
        result = self._values.get("target_listener_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#target_url ApplicationGateway#target_url}.'''
        result = self._values.get("target_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayRedirectConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayRedirectConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRedirectConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b74e433ab980d0b1874a2aa51346ae042ee41c4d67b234960e90d7fb03ef4d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayRedirectConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ba611cb5bde98b9e187b5648abacb1b383429c8f62d35bcd4f941133e280bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayRedirectConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a830c6c46b81237173fef4f8b33ee361e3253a316f8f18f7baf059ab0dd800)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59909b019b06887d7fab4ab98542a68880d27a7b3edfb817a6d0849b57daccfd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__926569acc31440822af63d37334db5d1e74389149e3f9b5145e4b37422e8f56a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRedirectConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRedirectConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRedirectConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c9452b2401df7b9eccb86d7803484fb3a8da481ce11a709e507a2c12738ba2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayRedirectConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRedirectConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b9cc4d67c37cfbfb2aa83f4811110914576d96726658e56e28ef3824594d867)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIncludePath")
    def reset_include_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludePath", []))

    @jsii.member(jsii_name="resetIncludeQueryString")
    def reset_include_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeQueryString", []))

    @jsii.member(jsii_name="resetTargetListenerName")
    def reset_target_listener_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetListenerName", []))

    @jsii.member(jsii_name="resetTargetUrl")
    def reset_target_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="targetListenerId")
    def target_listener_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetListenerId"))

    @builtins.property
    @jsii.member(jsii_name="includePathInput")
    def include_path_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includePathInput"))

    @builtins.property
    @jsii.member(jsii_name="includeQueryStringInput")
    def include_query_string_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeQueryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectTypeInput")
    def redirect_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetListenerNameInput")
    def target_listener_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetListenerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetUrlInput")
    def target_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="includePath")
    def include_path(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includePath"))

    @include_path.setter
    def include_path(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4549e561a0218bd3ee0a298a916dfd199aee883f810e1a795fd2d07bdb35a146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeQueryString")
    def include_query_string(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeQueryString"))

    @include_query_string.setter
    def include_query_string(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14ede66756c46f44fcca671fd2b148d776bb1928c1c148fbcecae84010d30d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeQueryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264c141b3d6f3d51ecb21c2c9003bc6a2f27cb0afb04d8305a6892d832efd38f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectType")
    def redirect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectType"))

    @redirect_type.setter
    def redirect_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4979842dd8c4cf40360e5d6132252d544bcce73d8a46887ecefa224bfbca6c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetListenerName")
    def target_listener_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetListenerName"))

    @target_listener_name.setter
    def target_listener_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4298f3fb49f3cb6ea0037b95eb1f170e8725c4064c0440404387afb83e7252e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetListenerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetUrl")
    def target_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetUrl"))

    @target_url.setter
    def target_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ede044cee20df2d33e143d32ee6d43fa794307a4f72d1a6cebbfa69936e589a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRedirectConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRedirectConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRedirectConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640be759b1e6daa0e8290e598e7274352d76520ed0787c8720259192f30419f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRequestRoutingRule",
    jsii_struct_bases=[],
    name_mapping={
        "http_listener_name": "httpListenerName",
        "name": "name",
        "rule_type": "ruleType",
        "backend_address_pool_name": "backendAddressPoolName",
        "backend_http_settings_name": "backendHttpSettingsName",
        "priority": "priority",
        "redirect_configuration_name": "redirectConfigurationName",
        "rewrite_rule_set_name": "rewriteRuleSetName",
        "url_path_map_name": "urlPathMapName",
    },
)
class ApplicationGatewayRequestRoutingRule:
    def __init__(
        self,
        *,
        http_listener_name: builtins.str,
        name: builtins.str,
        rule_type: builtins.str,
        backend_address_pool_name: typing.Optional[builtins.str] = None,
        backend_http_settings_name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        redirect_configuration_name: typing.Optional[builtins.str] = None,
        rewrite_rule_set_name: typing.Optional[builtins.str] = None,
        url_path_map_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_listener_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#http_listener_name ApplicationGateway#http_listener_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param rule_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_type ApplicationGateway#rule_type}.
        :param backend_address_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_address_pool_name ApplicationGateway#backend_address_pool_name}.
        :param backend_http_settings_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_http_settings_name ApplicationGateway#backend_http_settings_name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#priority ApplicationGateway#priority}.
        :param redirect_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#redirect_configuration_name ApplicationGateway#redirect_configuration_name}.
        :param rewrite_rule_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rewrite_rule_set_name ApplicationGateway#rewrite_rule_set_name}.
        :param url_path_map_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#url_path_map_name ApplicationGateway#url_path_map_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8a623d873df6cb0e5e3eaeb9a1ba1c45cf2d3f2c557a5a3a54c1a799573abc)
            check_type(argname="argument http_listener_name", value=http_listener_name, expected_type=type_hints["http_listener_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule_type", value=rule_type, expected_type=type_hints["rule_type"])
            check_type(argname="argument backend_address_pool_name", value=backend_address_pool_name, expected_type=type_hints["backend_address_pool_name"])
            check_type(argname="argument backend_http_settings_name", value=backend_http_settings_name, expected_type=type_hints["backend_http_settings_name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument redirect_configuration_name", value=redirect_configuration_name, expected_type=type_hints["redirect_configuration_name"])
            check_type(argname="argument rewrite_rule_set_name", value=rewrite_rule_set_name, expected_type=type_hints["rewrite_rule_set_name"])
            check_type(argname="argument url_path_map_name", value=url_path_map_name, expected_type=type_hints["url_path_map_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "http_listener_name": http_listener_name,
            "name": name,
            "rule_type": rule_type,
        }
        if backend_address_pool_name is not None:
            self._values["backend_address_pool_name"] = backend_address_pool_name
        if backend_http_settings_name is not None:
            self._values["backend_http_settings_name"] = backend_http_settings_name
        if priority is not None:
            self._values["priority"] = priority
        if redirect_configuration_name is not None:
            self._values["redirect_configuration_name"] = redirect_configuration_name
        if rewrite_rule_set_name is not None:
            self._values["rewrite_rule_set_name"] = rewrite_rule_set_name
        if url_path_map_name is not None:
            self._values["url_path_map_name"] = url_path_map_name

    @builtins.property
    def http_listener_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#http_listener_name ApplicationGateway#http_listener_name}.'''
        result = self._values.get("http_listener_name")
        assert result is not None, "Required property 'http_listener_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_type ApplicationGateway#rule_type}.'''
        result = self._values.get("rule_type")
        assert result is not None, "Required property 'rule_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backend_address_pool_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_address_pool_name ApplicationGateway#backend_address_pool_name}.'''
        result = self._values.get("backend_address_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backend_http_settings_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_http_settings_name ApplicationGateway#backend_http_settings_name}.'''
        result = self._values.get("backend_http_settings_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#priority ApplicationGateway#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redirect_configuration_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#redirect_configuration_name ApplicationGateway#redirect_configuration_name}.'''
        result = self._values.get("redirect_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rewrite_rule_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rewrite_rule_set_name ApplicationGateway#rewrite_rule_set_name}.'''
        result = self._values.get("rewrite_rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url_path_map_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#url_path_map_name ApplicationGateway#url_path_map_name}.'''
        result = self._values.get("url_path_map_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayRequestRoutingRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayRequestRoutingRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRequestRoutingRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1555561371da84bc32f3c3b4735743086d9b4dcb168130670e2d35f0bd7067)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayRequestRoutingRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13bda5c08fad65ce0692813adebc3c079000c7f13962fe6f407364c7b2e3e3fc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayRequestRoutingRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f56dc840fb7ddee47f5797e67b037204db679c4933f395cbffa2c40f0d5ec1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5cd5e95e9bb473a869de5d60ca166d84523c09de4001a123b3bca4fa4c40333)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ad537fee35044a7b190e5fc98d0623091aeea2fdbc97901133e0b00b354a913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRequestRoutingRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRequestRoutingRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRequestRoutingRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bc65f93a528ab6cf7bd5db97c2441e08b45078c72bcb381e206c25c052cc286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayRequestRoutingRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRequestRoutingRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f2c7b7353b2fd401789ca3702686c3b71f286665870208aafbcd69c3e04fc47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackendAddressPoolName")
    def reset_backend_address_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendAddressPoolName", []))

    @jsii.member(jsii_name="resetBackendHttpSettingsName")
    def reset_backend_http_settings_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendHttpSettingsName", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRedirectConfigurationName")
    def reset_redirect_configuration_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectConfigurationName", []))

    @jsii.member(jsii_name="resetRewriteRuleSetName")
    def reset_rewrite_rule_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewriteRuleSetName", []))

    @jsii.member(jsii_name="resetUrlPathMapName")
    def reset_url_path_map_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlPathMapName", []))

    @builtins.property
    @jsii.member(jsii_name="backendAddressPoolId")
    def backend_address_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendAddressPoolId"))

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettingsId")
    def backend_http_settings_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendHttpSettingsId"))

    @builtins.property
    @jsii.member(jsii_name="httpListenerId")
    def http_listener_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpListenerId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="redirectConfigurationId")
    def redirect_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectConfigurationId"))

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSetId")
    def rewrite_rule_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rewriteRuleSetId"))

    @builtins.property
    @jsii.member(jsii_name="urlPathMapId")
    def url_path_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlPathMapId"))

    @builtins.property
    @jsii.member(jsii_name="backendAddressPoolNameInput")
    def backend_address_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendAddressPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettingsNameInput")
    def backend_http_settings_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendHttpSettingsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="httpListenerNameInput")
    def http_listener_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpListenerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectConfigurationNameInput")
    def redirect_configuration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectConfigurationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSetNameInput")
    def rewrite_rule_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rewriteRuleSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleTypeInput")
    def rule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="urlPathMapNameInput")
    def url_path_map_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlPathMapNameInput"))

    @builtins.property
    @jsii.member(jsii_name="backendAddressPoolName")
    def backend_address_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendAddressPoolName"))

    @backend_address_pool_name.setter
    def backend_address_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6749a5beecb1c484e0632cb1371150f2ec2702f191d33d02a99a692be3e3aad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendAddressPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettingsName")
    def backend_http_settings_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendHttpSettingsName"))

    @backend_http_settings_name.setter
    def backend_http_settings_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24533e828a74ab36ddd9575140842a91967d2cbf3e342a897d678e2f3599dbb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendHttpSettingsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpListenerName")
    def http_listener_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpListenerName"))

    @http_listener_name.setter
    def http_listener_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c652aa62ae3cf7913d1e69ce0eb787093f063fcb343c105e2318794b4db9a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpListenerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01592b1d93447aa984b240b39e8f739646c99e81b7cce986098a0a3b58077ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49df255be86421d8935ff7c7c3623bcf2759cac4cf227600075c33a500284611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectConfigurationName")
    def redirect_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectConfigurationName"))

    @redirect_configuration_name.setter
    def redirect_configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe2436dcee7e710e9aafbb4f2e70e15aa01a4e3f32cf65fb8710c9dd4c8e583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectConfigurationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSetName")
    def rewrite_rule_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rewriteRuleSetName"))

    @rewrite_rule_set_name.setter
    def rewrite_rule_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4111437fca4874554791dd9a06a9349fb37d3a59f9865cd65a9bd41dc65f7155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rewriteRuleSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9935be74c38607b70ea3300f4b3de136266bd997b35bc3604f24c360d3836222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlPathMapName")
    def url_path_map_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlPathMapName"))

    @url_path_map_name.setter
    def url_path_map_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af71631070286b0cdb37677aa38d98f8befa977eecc79baeac6a18055e73d959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlPathMapName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRequestRoutingRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRequestRoutingRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRequestRoutingRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df94d2921af9621cf5e6ecf6bfab6a804f5fd7b019752d554f594637d29835fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSet",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "rewrite_rule": "rewriteRule"},
)
class ApplicationGatewayRewriteRuleSet:
    def __init__(
        self,
        *,
        name: builtins.str,
        rewrite_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSetRewriteRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param rewrite_rule: rewrite_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rewrite_rule ApplicationGateway#rewrite_rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e93603d4b0b53808969d3f24f519271829f0b3e5f106445f297a229481402c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rewrite_rule", value=rewrite_rule, expected_type=type_hints["rewrite_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if rewrite_rule is not None:
            self._values["rewrite_rule"] = rewrite_rule

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rewrite_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRule"]]]:
        '''rewrite_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rewrite_rule ApplicationGateway#rewrite_rule}
        '''
        result = self._values.get("rewrite_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayRewriteRuleSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayRewriteRuleSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03f627fbb17b2e1cab5bdae10e2d623b8b340c1a289ced77db27544c09af92b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayRewriteRuleSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578df1f446649cff76c20e1538f51cd136f6c2e478f7c3a232918d8e568c5ddf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayRewriteRuleSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1252b2bcf713dc112c5dfe2c94ee20536a3ccdcd03ca352204643d6a824b2fa4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f6e07f535ee311ebda3983930780b9f66f42ccbbb2f737c5ac58d922e1528af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43b9f7036eee184b6c470b6d2f053ad38580ba1fce827d25fb9fc477df981d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aae324ddf1ec8d252fcae58364b6158241bece8a5c42d1a9375a5fe0931eec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayRewriteRuleSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91ae8cc613ea27f932ccef5bffb4eb6dfdfab1e063ccca4b325167bfb8cf70e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRewriteRule")
    def put_rewrite_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSetRewriteRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6bf1efc28026ea6db22223763f67c16b43bf48feab204b8a7a5173e2de28f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRewriteRule", [value]))

    @jsii.member(jsii_name="resetRewriteRule")
    def reset_rewrite_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewriteRule", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="rewriteRule")
    def rewrite_rule(self) -> "ApplicationGatewayRewriteRuleSetRewriteRuleList":
        return typing.cast("ApplicationGatewayRewriteRuleSetRewriteRuleList", jsii.get(self, "rewriteRule"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleInput")
    def rewrite_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRule"]]], jsii.get(self, "rewriteRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef97ced4d33a5065d0d789db12095db9ab89e98213b26e394835647e9a3a3c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f35930842de0c9e28378fc8bdd87e3be8ba076215312f6a3130e096b632b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRule",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "rule_sequence": "ruleSequence",
        "condition": "condition",
        "request_header_configuration": "requestHeaderConfiguration",
        "response_header_configuration": "responseHeaderConfiguration",
        "url": "url",
    },
)
class ApplicationGatewayRewriteRuleSetRewriteRule:
    def __init__(
        self,
        *,
        name: builtins.str,
        rule_sequence: jsii.Number,
        condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSetRewriteRuleCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url: typing.Optional[typing.Union["ApplicationGatewayRewriteRuleSetRewriteRuleUrl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param rule_sequence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_sequence ApplicationGateway#rule_sequence}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#condition ApplicationGateway#condition}
        :param request_header_configuration: request_header_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_header_configuration ApplicationGateway#request_header_configuration}
        :param response_header_configuration: response_header_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#response_header_configuration ApplicationGateway#response_header_configuration}
        :param url: url block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#url ApplicationGateway#url}
        '''
        if isinstance(url, dict):
            url = ApplicationGatewayRewriteRuleSetRewriteRuleUrl(**url)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc78332f92ecc0df04914459a457d7b0b16c8ec75fbd50d218848620fe8088be)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule_sequence", value=rule_sequence, expected_type=type_hints["rule_sequence"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument request_header_configuration", value=request_header_configuration, expected_type=type_hints["request_header_configuration"])
            check_type(argname="argument response_header_configuration", value=response_header_configuration, expected_type=type_hints["response_header_configuration"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "rule_sequence": rule_sequence,
        }
        if condition is not None:
            self._values["condition"] = condition
        if request_header_configuration is not None:
            self._values["request_header_configuration"] = request_header_configuration
        if response_header_configuration is not None:
            self._values["response_header_configuration"] = response_header_configuration
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_sequence(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_sequence ApplicationGateway#rule_sequence}.'''
        result = self._values.get("rule_sequence")
        assert result is not None, "Required property 'rule_sequence' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleCondition"]]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#condition ApplicationGateway#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleCondition"]]], result)

    @builtins.property
    def request_header_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration"]]]:
        '''request_header_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_header_configuration ApplicationGateway#request_header_configuration}
        '''
        result = self._values.get("request_header_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration"]]], result)

    @builtins.property
    def response_header_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration"]]]:
        '''response_header_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#response_header_configuration ApplicationGateway#response_header_configuration}
        '''
        result = self._values.get("response_header_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration"]]], result)

    @builtins.property
    def url(self) -> typing.Optional["ApplicationGatewayRewriteRuleSetRewriteRuleUrl"]:
        '''url block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#url ApplicationGateway#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional["ApplicationGatewayRewriteRuleSetRewriteRuleUrl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayRewriteRuleSetRewriteRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleCondition",
    jsii_struct_bases=[],
    name_mapping={
        "pattern": "pattern",
        "variable": "variable",
        "ignore_case": "ignoreCase",
        "negate": "negate",
    },
)
class ApplicationGatewayRewriteRuleSetRewriteRuleCondition:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        variable: builtins.str,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#pattern ApplicationGateway#pattern}.
        :param variable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#variable ApplicationGateway#variable}.
        :param ignore_case: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ignore_case ApplicationGateway#ignore_case}.
        :param negate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#negate ApplicationGateway#negate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__403c168f7b330cea50a9b9db99473b3368967d07f2c4ec0e913e5299e3e266af)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
            "variable": variable,
        }
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if negate is not None:
            self._values["negate"] = negate

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#pattern ApplicationGateway#pattern}.'''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def variable(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#variable ApplicationGateway#variable}.'''
        result = self._values.get("variable")
        assert result is not None, "Required property 'variable' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ignore_case ApplicationGateway#ignore_case}.'''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#negate ApplicationGateway#negate}.'''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayRewriteRuleSetRewriteRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayRewriteRuleSetRewriteRuleConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7651394e69084dc3b1af977e6d4bfd124f35a366c52e5db8c0dc98a0e3123f50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayRewriteRuleSetRewriteRuleConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6748a75ca09e539eda7d2f95e0f212fd270d8858543c445722bfe1261807ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayRewriteRuleSetRewriteRuleConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2ee2b88076e1ef414efd7947ca0f0c796e523bed0cb9a96181058f8632b0e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e09fc33773b63bd5468226a536a87cb2f652249a230d8a7ecb4b13a79420f614)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11a9dd5a172dbcc080d85019c87e4d3bb89d9ecc8a4d9972de2213c4fa3586bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b1d7401307f0f3176494ea82bc68c28730ad35c2013cba60ccde585ea6b163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayRewriteRuleSetRewriteRuleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02044c8dc42b30922ac022c16a18bea043247287c923131f790d59d1fbed203f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723c4cc80bf5f8c812aa326ac06f918d5382cfbcfc82cfe9c364b2cb9f538f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f509e4ed4b369eccc410259298c9373a4167def82d9811baa446e3806d26b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee868cb36a59146f10e938395048e4567bb85208d991d3b03089c807a533a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variable"))

    @variable.setter
    def variable(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01d82a5f581a9a68236b3287d2cb281d15672e0a20d103f297b9ad3980ec3f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26984563e2bfd151caff91740f0d198cdb4bc63e054e88796467424d3d04ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayRewriteRuleSetRewriteRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd42a7437d102e957bfd3e989805f2a75c28d42534a316663b3d2e8248910aef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayRewriteRuleSetRewriteRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec780c96eafb8ea92335dbc0b22dccef8593268ca300b3919bebf5cd3940e35a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayRewriteRuleSetRewriteRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8828d7c8df1ce83772e14984a25b285e9ecd36e0ad4a74a52f738870cdbe2431)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e185b4481bfa0867172ee30d6257eacf861ed778b15e5e0c70f3be76ae6d89ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebea615d6ecfb11076ed41bfba9ca62eb26d120fe14c949b08e5ae1b2df2ce49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f9b8824336c1c3a3f70381a18ca9b34867cbc4c526ee1bee47740a543d575c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayRewriteRuleSetRewriteRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6116ab2e981c4454852e78f76d1ff9d1049c4bd2d94b5a60e08faa51188b9934)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d134283562a7e938640b059f0d166653eda05dba7a6fecf374dcb88d04a2ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putRequestHeaderConfiguration")
    def put_request_header_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1ff56d3f019e4388ad23f8aa0433cec99951a386ead1f87ab2f7f2ee5c2b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaderConfiguration", [value]))

    @jsii.member(jsii_name="putResponseHeaderConfiguration")
    def put_response_header_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab437aa1ea56833080821f6016808ffc7b5f1f953dd3c6498e5a8d4527bcb74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResponseHeaderConfiguration", [value]))

    @jsii.member(jsii_name="putUrl")
    def put_url(
        self,
        *,
        components: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
        reroute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param components: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#components ApplicationGateway#components}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#path ApplicationGateway#path}.
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#query_string ApplicationGateway#query_string}.
        :param reroute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#reroute ApplicationGateway#reroute}.
        '''
        value = ApplicationGatewayRewriteRuleSetRewriteRuleUrl(
            components=components,
            path=path,
            query_string=query_string,
            reroute=reroute,
        )

        return typing.cast(None, jsii.invoke(self, "putUrl", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetRequestHeaderConfiguration")
    def reset_request_header_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaderConfiguration", []))

    @jsii.member(jsii_name="resetResponseHeaderConfiguration")
    def reset_response_header_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeaderConfiguration", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> ApplicationGatewayRewriteRuleSetRewriteRuleConditionList:
        return typing.cast(ApplicationGatewayRewriteRuleSetRewriteRuleConditionList, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderConfiguration")
    def request_header_configuration(
        self,
    ) -> "ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationList":
        return typing.cast("ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationList", jsii.get(self, "requestHeaderConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderConfiguration")
    def response_header_configuration(
        self,
    ) -> "ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationList":
        return typing.cast("ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationList", jsii.get(self, "responseHeaderConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> "ApplicationGatewayRewriteRuleSetRewriteRuleUrlOutputReference":
        return typing.cast("ApplicationGatewayRewriteRuleSetRewriteRuleUrlOutputReference", jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleCondition]]], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderConfigurationInput")
    def request_header_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration"]]], jsii.get(self, "requestHeaderConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderConfigurationInput")
    def response_header_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration"]]], jsii.get(self, "responseHeaderConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleSequenceInput")
    def rule_sequence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleSequenceInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(
        self,
    ) -> typing.Optional["ApplicationGatewayRewriteRuleSetRewriteRuleUrl"]:
        return typing.cast(typing.Optional["ApplicationGatewayRewriteRuleSetRewriteRuleUrl"], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e6a69160797acb27ec4dff559a577502c820966801487b707c11414a61563bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleSequence")
    def rule_sequence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleSequence"))

    @rule_sequence.setter
    def rule_sequence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4919048af5cf07a55f1ff00dccc0f4ae11f93d118aadf83c6c4202143b38979a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleSequence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec19c65cf5af9ad7c923dcc5793a068f1154f92cea04c962743bbd37263748cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName", "header_value": "headerValue"},
)
class ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
    ) -> None:
        '''
        :param header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#header_name ApplicationGateway#header_name}.
        :param header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#header_value ApplicationGateway#header_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f307075d0539f78381eeaad65bd4ab1064d11435c084915cbaef94b9730e02)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
            "header_value": header_value,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#header_name ApplicationGateway#header_name}.'''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#header_value ApplicationGateway#header_value}.'''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e08ee82d9bde6634f70b4bfacd365ad62b8b1170dbf92b4992ddb5f215834231)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920099104ce9dfa349979486c3b5d250924708cdfaac35bbd2bc409b4dbc62ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9c5bc8ec6046916a23a0c72b8281636a3ef886ffbfa1b36c16071fe4731ca4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c234a65ffc0e77c4e07dfc11fe970b941bf98894e645972ab0f5f1a744c704)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f63feaa74cadff2a8dac9be3a1bd0612ea843b94456bb3195c9c2d7a599bbea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4549d5bcc91f6faa706a0263372defb0e07c6cfe21925527b94650aa3898d1d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2725477f934364ee0bb39923bbec22741226f084c41d2a666fc9fef4a4554758)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__4668eb8a586d2d30acfaa67943e3d78fb8426ce79f287cf29d76ad9350c1ef6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a84946c884941c7243580941e387a4cd9450d020f0cc8a5a66a6918906d7e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970f922c3f7e7d64a63b3aabde9653aed87a2c4aa689372cadab8d87f8662883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName", "header_value": "headerValue"},
)
class ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
    ) -> None:
        '''
        :param header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#header_name ApplicationGateway#header_name}.
        :param header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#header_value ApplicationGateway#header_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb59694b2d4809fe6690311b3d45401d7ec4a340bfdec660285c17f15fd2c05)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
            "header_value": header_value,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#header_name ApplicationGateway#header_name}.'''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#header_value ApplicationGateway#header_value}.'''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__969f78427c44c610a0c18bf917cd99c40358d4e723b8c19457496163e84fdf45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5fbbc936803af4c25bb114f0fb2c3eeac0be24d373c808aae549e7002a1e9c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de01333c375125bbc2097ffdcf1d09f902fad5bbedb97c463f6e12209d2df99f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54834328c36afcad7c756d4a4e59b68518f03e0eef1b2bbaad6900eb356a6f0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__082d90396a9ff4cfe88c56ea528ca8c2260f3fd6d767cc252c4f46f195ef99ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78294eaf744312f863bf5cb8960e7703ee6befe663ff1e4a61f0cc39ab4c6955)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c59138096e8a79804e54ba4c47f926e46457dcbb184ad0c4a3b123f5ed801dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__3b8fb7b6b035b1ac9f2bc0926ec8b1698a8152fd574633374b7fe50cc7f386ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b576bd18eb9c5bd67ba70b9336c0b2a4ae326479db4fc387e4019176f85309b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c882acc884357447edcb2356b908f71a71c861567d6f9d96770d9f55e3cf1bc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleUrl",
    jsii_struct_bases=[],
    name_mapping={
        "components": "components",
        "path": "path",
        "query_string": "queryString",
        "reroute": "reroute",
    },
)
class ApplicationGatewayRewriteRuleSetRewriteRuleUrl:
    def __init__(
        self,
        *,
        components: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
        reroute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param components: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#components ApplicationGateway#components}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#path ApplicationGateway#path}.
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#query_string ApplicationGateway#query_string}.
        :param reroute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#reroute ApplicationGateway#reroute}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1cb7ab010869ba25ed7d8846f27e4f54253424a8c07c749769e09f7b49ca4b)
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument reroute", value=reroute, expected_type=type_hints["reroute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if components is not None:
            self._values["components"] = components
        if path is not None:
            self._values["path"] = path
        if query_string is not None:
            self._values["query_string"] = query_string
        if reroute is not None:
            self._values["reroute"] = reroute

    @builtins.property
    def components(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#components ApplicationGateway#components}.'''
        result = self._values.get("components")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#path ApplicationGateway#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#query_string ApplicationGateway#query_string}.'''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reroute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#reroute ApplicationGateway#reroute}.'''
        result = self._values.get("reroute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayRewriteRuleSetRewriteRuleUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayRewriteRuleSetRewriteRuleUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayRewriteRuleSetRewriteRuleUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f77dd3cb006127c60e9d988e1e79ecd65eac8011c094e78b7bbdcf566abbc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComponents")
    def reset_components(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComponents", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetQueryString")
    def reset_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryString", []))

    @jsii.member(jsii_name="resetReroute")
    def reset_reroute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReroute", []))

    @builtins.property
    @jsii.member(jsii_name="componentsInput")
    def components_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "componentsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="rerouteInput")
    def reroute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rerouteInput"))

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "components"))

    @components.setter
    def components(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ba837a7acb6bb1a6b691f8f0e2d30ed12de2ffda8291f0acc5f7cf47501ed1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b897a9abf4eea457472778999deb6da308096dda1a95003ba55a6a17d34bb770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40969d104ff18925703098e841bece4a047c5133ae10911bd5f768493c384283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reroute")
    def reroute(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reroute"))

    @reroute.setter
    def reroute(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c267f12da7f741af1a5ce411efa37099a58df7d08c426175a7a4e3988b2c095d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reroute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApplicationGatewayRewriteRuleSetRewriteRuleUrl]:
        return typing.cast(typing.Optional[ApplicationGatewayRewriteRuleSetRewriteRuleUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationGatewayRewriteRuleSetRewriteRuleUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc12b5dae79860cc86451bd9d6fd2dfec68d9db8c26eb25e0d0f6236aded3d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySku",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tier": "tier", "capacity": "capacity"},
)
class ApplicationGatewaySku:
    def __init__(
        self,
        *,
        name: builtins.str,
        tier: builtins.str,
        capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#tier ApplicationGateway#tier}.
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#capacity ApplicationGateway#capacity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebda84c61b3a52c067a899ef24c74d54270a4cc58c955017d9b2c4d98d7504b3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "tier": tier,
        }
        if capacity is not None:
            self._values["capacity"] = capacity

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#tier ApplicationGateway#tier}.'''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#capacity ApplicationGateway#capacity}.'''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewaySku(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewaySkuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySkuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7155a042d13a1ccca11d736a57d0819205e2f067b800cb4750324f1034ca67fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCapacity")
    def reset_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afd2bbe653aaa1bb6167f4f90ed7f289a6628b1a0e74d8b39b04fa3e157e933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6c228afcb31b0fa00a9821deb77d070b6a7eaa89ed4127fca0ebad2d609301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d958a98040c851f55a99e89b4372933072e598350c703c51ee05e30126e597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationGatewaySku]:
        return typing.cast(typing.Optional[ApplicationGatewaySku], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApplicationGatewaySku]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e43ef307e63590e71429f1b1f2ba713a2ac5ab7417132f5d252a0c4c4016c35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "data": "data",
        "key_vault_secret_id": "keyVaultSecretId",
        "password": "password",
    },
)
class ApplicationGatewaySslCertificate:
    def __init__(
        self,
        *,
        name: builtins.str,
        data: typing.Optional[builtins.str] = None,
        key_vault_secret_id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#data ApplicationGateway#data}.
        :param key_vault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#key_vault_secret_id ApplicationGateway#key_vault_secret_id}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#password ApplicationGateway#password}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1c4d6819bd00a3d15aa0819b49a10016aec4dfd0c0b6e2f3815a529a1c8c5e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument key_vault_secret_id", value=key_vault_secret_id, expected_type=type_hints["key_vault_secret_id"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if data is not None:
            self._values["data"] = data
        if key_vault_secret_id is not None:
            self._values["key_vault_secret_id"] = key_vault_secret_id
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#data ApplicationGateway#data}.'''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_secret_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#key_vault_secret_id ApplicationGateway#key_vault_secret_id}.'''
        result = self._values.get("key_vault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#password ApplicationGateway#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewaySslCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewaySslCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__102884559ddbcd6429de6a063a8af54559c8a8b062911ced57aca0f0a9fbd4b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewaySslCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac09cd79cd9d1ae1155aa995142b094ab195cf93a1c356c0227facfecc7f375c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewaySslCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b854f69ca946254bab0f278e950327a817f0d04be143a3729914305defe9bac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0247cafc5ecdf3ed7f26e07dca2476dc654187a21ec11989c9912b1c0467199)
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
            type_hints = typing.get_type_hints(_typecheckingstub__382ad754f79380afb81bf4e0399789d24fc7872194bec82ae5fc17db9c26407f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewaySslCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewaySslCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewaySslCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f59c6028162951766b4b6918144d55c0887a4806a8125287c8a5b6c3fa57770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewaySslCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae78be16bff9ede9874bdc999630ce0a4045fe5addc08e4bd1e5867708baa722)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetKeyVaultSecretId")
    def reset_key_vault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultSecretId", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="publicCertData")
    def public_cert_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicCertData"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretIdInput")
    def key_vault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab354965d7017a95dfae1753b58c7ab58c576727d17f6ca063dadbbb2b557869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretId")
    def key_vault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultSecretId"))

    @key_vault_secret_id.setter
    def key_vault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800abe4f8be7074c06f4e6d6c6b881468207433bd9b9850e8be40dfb7175e163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c8ce1d291e2a9e99ad6296dcfee23f29589ff8c4447e0d8d0b474cd766cbc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c74e4ddd50dce54d918e79bc73b2a975937966817c2ea51901012d20e91b2fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewaySslCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewaySslCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewaySslCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838bce3200a4da6e061fcfc759f7e917931fa3f5f56ea43eebb99dae13d42157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cipher_suites": "cipherSuites",
        "disabled_protocols": "disabledProtocols",
        "min_protocol_version": "minProtocolVersion",
        "policy_name": "policyName",
        "policy_type": "policyType",
    },
)
class ApplicationGatewaySslPolicy:
    def __init__(
        self,
        *,
        cipher_suites: typing.Optional[typing.Sequence[builtins.str]] = None,
        disabled_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        min_protocol_version: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cipher_suites: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#cipher_suites ApplicationGateway#cipher_suites}.
        :param disabled_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#disabled_protocols ApplicationGateway#disabled_protocols}.
        :param min_protocol_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#min_protocol_version ApplicationGateway#min_protocol_version}.
        :param policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_name ApplicationGateway#policy_name}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_type ApplicationGateway#policy_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d087d5be39410dc3919d40341b96b43874aa3dc35cf9633081191936b30711e)
            check_type(argname="argument cipher_suites", value=cipher_suites, expected_type=type_hints["cipher_suites"])
            check_type(argname="argument disabled_protocols", value=disabled_protocols, expected_type=type_hints["disabled_protocols"])
            check_type(argname="argument min_protocol_version", value=min_protocol_version, expected_type=type_hints["min_protocol_version"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cipher_suites is not None:
            self._values["cipher_suites"] = cipher_suites
        if disabled_protocols is not None:
            self._values["disabled_protocols"] = disabled_protocols
        if min_protocol_version is not None:
            self._values["min_protocol_version"] = min_protocol_version
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if policy_type is not None:
            self._values["policy_type"] = policy_type

    @builtins.property
    def cipher_suites(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#cipher_suites ApplicationGateway#cipher_suites}.'''
        result = self._values.get("cipher_suites")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disabled_protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#disabled_protocols ApplicationGateway#disabled_protocols}.'''
        result = self._values.get("disabled_protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def min_protocol_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#min_protocol_version ApplicationGateway#min_protocol_version}.'''
        result = self._values.get("min_protocol_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_name ApplicationGateway#policy_name}.'''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_type ApplicationGateway#policy_type}.'''
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewaySslPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewaySslPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b494a5d79f922a5bcf358c466b1a7cdd293d3deb3c88e1381a6629443cc3ff71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCipherSuites")
    def reset_cipher_suites(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCipherSuites", []))

    @jsii.member(jsii_name="resetDisabledProtocols")
    def reset_disabled_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledProtocols", []))

    @jsii.member(jsii_name="resetMinProtocolVersion")
    def reset_min_protocol_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinProtocolVersion", []))

    @jsii.member(jsii_name="resetPolicyName")
    def reset_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyName", []))

    @jsii.member(jsii_name="resetPolicyType")
    def reset_policy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyType", []))

    @builtins.property
    @jsii.member(jsii_name="cipherSuitesInput")
    def cipher_suites_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cipherSuitesInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledProtocolsInput")
    def disabled_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "disabledProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="minProtocolVersionInput")
    def min_protocol_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minProtocolVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyTypeInput")
    def policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="cipherSuites")
    def cipher_suites(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cipherSuites"))

    @cipher_suites.setter
    def cipher_suites(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b2d5cd3b3ffd582b1d614980b22306d8d35a1be0eb339339152add267c9a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cipherSuites", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabledProtocols")
    def disabled_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "disabledProtocols"))

    @disabled_protocols.setter
    def disabled_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4438cf598808111e3a19f4535ce599dc2f9842f2573e7e0a54df2ee652c36292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledProtocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minProtocolVersion")
    def min_protocol_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minProtocolVersion"))

    @min_protocol_version.setter
    def min_protocol_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8b6de7c74933f07e4e6287b4cc212ae5598af662a9bdbdf1481e989c9b0ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minProtocolVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8399c9d767445c112c3788af2528bbacff6a8125454fcfd4f0e3ad260606b47e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyType"))

    @policy_type.setter
    def policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6130f90c79fc0bc26a9e94e6d5a2dcb2a1522a92c10a2f622a0f11ef530c55b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationGatewaySslPolicy]:
        return typing.cast(typing.Optional[ApplicationGatewaySslPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationGatewaySslPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe4e125ee51e45468dcb88cb403e0e631694205559f7b9a059031589483c8b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslProfile",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "ssl_policy": "sslPolicy",
        "trusted_client_certificate_names": "trustedClientCertificateNames",
        "verify_client_certificate_revocation": "verifyClientCertificateRevocation",
        "verify_client_cert_issuer_dn": "verifyClientCertIssuerDn",
    },
)
class ApplicationGatewaySslProfile:
    def __init__(
        self,
        *,
        name: builtins.str,
        ssl_policy: typing.Optional[typing.Union["ApplicationGatewaySslProfileSslPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_client_certificate_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify_client_certificate_revocation: typing.Optional[builtins.str] = None,
        verify_client_cert_issuer_dn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param ssl_policy: ssl_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_policy ApplicationGateway#ssl_policy}
        :param trusted_client_certificate_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_client_certificate_names ApplicationGateway#trusted_client_certificate_names}.
        :param verify_client_certificate_revocation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#verify_client_certificate_revocation ApplicationGateway#verify_client_certificate_revocation}.
        :param verify_client_cert_issuer_dn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#verify_client_cert_issuer_dn ApplicationGateway#verify_client_cert_issuer_dn}.
        '''
        if isinstance(ssl_policy, dict):
            ssl_policy = ApplicationGatewaySslProfileSslPolicy(**ssl_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e5f6b4ea4c73e0d9a176a0da86c9d9c8d2393ad679658d19a475a1c55b5ed6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
            check_type(argname="argument trusted_client_certificate_names", value=trusted_client_certificate_names, expected_type=type_hints["trusted_client_certificate_names"])
            check_type(argname="argument verify_client_certificate_revocation", value=verify_client_certificate_revocation, expected_type=type_hints["verify_client_certificate_revocation"])
            check_type(argname="argument verify_client_cert_issuer_dn", value=verify_client_cert_issuer_dn, expected_type=type_hints["verify_client_cert_issuer_dn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
        if trusted_client_certificate_names is not None:
            self._values["trusted_client_certificate_names"] = trusted_client_certificate_names
        if verify_client_certificate_revocation is not None:
            self._values["verify_client_certificate_revocation"] = verify_client_certificate_revocation
        if verify_client_cert_issuer_dn is not None:
            self._values["verify_client_cert_issuer_dn"] = verify_client_cert_issuer_dn

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional["ApplicationGatewaySslProfileSslPolicy"]:
        '''ssl_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#ssl_policy ApplicationGateway#ssl_policy}
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional["ApplicationGatewaySslProfileSslPolicy"], result)

    @builtins.property
    def trusted_client_certificate_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#trusted_client_certificate_names ApplicationGateway#trusted_client_certificate_names}.'''
        result = self._values.get("trusted_client_certificate_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verify_client_certificate_revocation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#verify_client_certificate_revocation ApplicationGateway#verify_client_certificate_revocation}.'''
        result = self._values.get("verify_client_certificate_revocation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_client_cert_issuer_dn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#verify_client_cert_issuer_dn ApplicationGateway#verify_client_cert_issuer_dn}.'''
        result = self._values.get("verify_client_cert_issuer_dn")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewaySslProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewaySslProfileList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslProfileList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ae6203e7a657ddd599e483b71f1deadf136ef322afb7b0e52ef3251eb6ec7b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApplicationGatewaySslProfileOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548cd525e2eb70e5df59ff14753c794df1e1703d0db4f23b54951f2a9f062e47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewaySslProfileOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add0d612781bd0cadda72ac421271a15e5b83ea7c3239ff7098dea02954cb8df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c29b7e57d896415579648b4ce4d224d298aed094658740bf7a39c6645082aac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6420e7058f64217430d75fbe1dc64b87c87a4528eb06392140bae09e5b0a1d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewaySslProfile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewaySslProfile]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewaySslProfile]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb50d5b1d42e2b48a27133c4cb5cf3353d3bb915d5e7d61be8e932911eb873d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewaySslProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__766dc201cf797b577959ce2093651ecac76793b91c6387ce6254c29b25e7a02f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSslPolicy")
    def put_ssl_policy(
        self,
        *,
        cipher_suites: typing.Optional[typing.Sequence[builtins.str]] = None,
        disabled_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        min_protocol_version: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cipher_suites: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#cipher_suites ApplicationGateway#cipher_suites}.
        :param disabled_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#disabled_protocols ApplicationGateway#disabled_protocols}.
        :param min_protocol_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#min_protocol_version ApplicationGateway#min_protocol_version}.
        :param policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_name ApplicationGateway#policy_name}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_type ApplicationGateway#policy_type}.
        '''
        value = ApplicationGatewaySslProfileSslPolicy(
            cipher_suites=cipher_suites,
            disabled_protocols=disabled_protocols,
            min_protocol_version=min_protocol_version,
            policy_name=policy_name,
            policy_type=policy_type,
        )

        return typing.cast(None, jsii.invoke(self, "putSslPolicy", [value]))

    @jsii.member(jsii_name="resetSslPolicy")
    def reset_ssl_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslPolicy", []))

    @jsii.member(jsii_name="resetTrustedClientCertificateNames")
    def reset_trusted_client_certificate_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedClientCertificateNames", []))

    @jsii.member(jsii_name="resetVerifyClientCertificateRevocation")
    def reset_verify_client_certificate_revocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyClientCertificateRevocation", []))

    @jsii.member(jsii_name="resetVerifyClientCertIssuerDn")
    def reset_verify_client_cert_issuer_dn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyClientCertIssuerDn", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> "ApplicationGatewaySslProfileSslPolicyOutputReference":
        return typing.cast("ApplicationGatewaySslProfileSslPolicyOutputReference", jsii.get(self, "sslPolicy"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicyInput")
    def ssl_policy_input(
        self,
    ) -> typing.Optional["ApplicationGatewaySslProfileSslPolicy"]:
        return typing.cast(typing.Optional["ApplicationGatewaySslProfileSslPolicy"], jsii.get(self, "sslPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedClientCertificateNamesInput")
    def trusted_client_certificate_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedClientCertificateNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyClientCertificateRevocationInput")
    def verify_client_certificate_revocation_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "verifyClientCertificateRevocationInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyClientCertIssuerDnInput")
    def verify_client_cert_issuer_dn_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyClientCertIssuerDnInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1566322d13a054acae0826b5e8a698e9d62212f328aca7e7360a08ce43a0f71c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedClientCertificateNames")
    def trusted_client_certificate_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedClientCertificateNames"))

    @trusted_client_certificate_names.setter
    def trusted_client_certificate_names(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996f69e7d0dd0216a08bd1f47104a1085041ad7e73380bea5350db679895320e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedClientCertificateNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verifyClientCertificateRevocation")
    def verify_client_certificate_revocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verifyClientCertificateRevocation"))

    @verify_client_certificate_revocation.setter
    def verify_client_certificate_revocation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69df7c12cd59816bbcb8c26f10faca91e5deaa1601b041fbbe3026cce7c1cdd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyClientCertificateRevocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verifyClientCertIssuerDn")
    def verify_client_cert_issuer_dn(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyClientCertIssuerDn"))

    @verify_client_cert_issuer_dn.setter
    def verify_client_cert_issuer_dn(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e8664d84420c989e43f283772abf02c20f68b3b03bd97c29b5e6d39ab0d4a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyClientCertIssuerDn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewaySslProfile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewaySslProfile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewaySslProfile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3588912e4c0cbb765921246ffd76dd7327e6629459584938c13f81ee01ca7645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslProfileSslPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cipher_suites": "cipherSuites",
        "disabled_protocols": "disabledProtocols",
        "min_protocol_version": "minProtocolVersion",
        "policy_name": "policyName",
        "policy_type": "policyType",
    },
)
class ApplicationGatewaySslProfileSslPolicy:
    def __init__(
        self,
        *,
        cipher_suites: typing.Optional[typing.Sequence[builtins.str]] = None,
        disabled_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        min_protocol_version: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cipher_suites: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#cipher_suites ApplicationGateway#cipher_suites}.
        :param disabled_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#disabled_protocols ApplicationGateway#disabled_protocols}.
        :param min_protocol_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#min_protocol_version ApplicationGateway#min_protocol_version}.
        :param policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_name ApplicationGateway#policy_name}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_type ApplicationGateway#policy_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf2cdf3f24a829f952dcdb774cfe2a763d388b60675ea9c2262cf0df93180c30)
            check_type(argname="argument cipher_suites", value=cipher_suites, expected_type=type_hints["cipher_suites"])
            check_type(argname="argument disabled_protocols", value=disabled_protocols, expected_type=type_hints["disabled_protocols"])
            check_type(argname="argument min_protocol_version", value=min_protocol_version, expected_type=type_hints["min_protocol_version"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cipher_suites is not None:
            self._values["cipher_suites"] = cipher_suites
        if disabled_protocols is not None:
            self._values["disabled_protocols"] = disabled_protocols
        if min_protocol_version is not None:
            self._values["min_protocol_version"] = min_protocol_version
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if policy_type is not None:
            self._values["policy_type"] = policy_type

    @builtins.property
    def cipher_suites(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#cipher_suites ApplicationGateway#cipher_suites}.'''
        result = self._values.get("cipher_suites")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disabled_protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#disabled_protocols ApplicationGateway#disabled_protocols}.'''
        result = self._values.get("disabled_protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def min_protocol_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#min_protocol_version ApplicationGateway#min_protocol_version}.'''
        result = self._values.get("min_protocol_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_name ApplicationGateway#policy_name}.'''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#policy_type ApplicationGateway#policy_type}.'''
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewaySslProfileSslPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewaySslProfileSslPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewaySslProfileSslPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db82a3fcd33e127fda3f3d132b7c717c7f11324f1974e8c346dcb62c970d0494)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCipherSuites")
    def reset_cipher_suites(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCipherSuites", []))

    @jsii.member(jsii_name="resetDisabledProtocols")
    def reset_disabled_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledProtocols", []))

    @jsii.member(jsii_name="resetMinProtocolVersion")
    def reset_min_protocol_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinProtocolVersion", []))

    @jsii.member(jsii_name="resetPolicyName")
    def reset_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyName", []))

    @jsii.member(jsii_name="resetPolicyType")
    def reset_policy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyType", []))

    @builtins.property
    @jsii.member(jsii_name="cipherSuitesInput")
    def cipher_suites_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cipherSuitesInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledProtocolsInput")
    def disabled_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "disabledProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="minProtocolVersionInput")
    def min_protocol_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minProtocolVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyTypeInput")
    def policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="cipherSuites")
    def cipher_suites(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cipherSuites"))

    @cipher_suites.setter
    def cipher_suites(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e28f507d816b35a2856138baceb1611d8dcce7431c5b6112df499a54738913d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cipherSuites", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabledProtocols")
    def disabled_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "disabledProtocols"))

    @disabled_protocols.setter
    def disabled_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b832104a891bfbf47ae21f964b756eb4b62cdc0cd076c6a03a792dba6e03f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledProtocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minProtocolVersion")
    def min_protocol_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minProtocolVersion"))

    @min_protocol_version.setter
    def min_protocol_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c984348d89dc1ce79001f49901fcfdcca3206b03a96bb13ec1a0c5525eaf0c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minProtocolVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eab35fbbf43f7737efce44a0c92cdd025709d32db3048c93076eb21808bbc09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyType"))

    @policy_type.setter
    def policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2528bc823c37cec84e774b3e2f46c8c6c064624dfcfa79dc87e3c46441e6726f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationGatewaySslProfileSslPolicy]:
        return typing.cast(typing.Optional[ApplicationGatewaySslProfileSslPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationGatewaySslProfileSslPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b94830c3b4cb7e0e234d3c91ea9d332a12ddd2357d3a4b4b0cf1ad36fd5518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApplicationGatewayTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#create ApplicationGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#delete ApplicationGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#read ApplicationGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#update ApplicationGateway#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b4c8c749f2ea506c397a33eb582e83dfb58db0720746e13f360076750142be)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#create ApplicationGateway#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#delete ApplicationGateway#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#read ApplicationGateway#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#update ApplicationGateway#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffc94f892cbcd846c91cbf2d0e29ba1bdd9950aeed7399449a531846b859117f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42a43136e8ce07518d4f6efcc3e42c27f012310469f50d7b634c0c8b266e028d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6776159683b8a31317aa467e5b49907af4d940fa11addc794b5ed07d5899b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6525e2b414eeba28544045fa5e5c4f5f13dcaa86e3b637a6f38b75baee729902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf121334ba044f079095746dbccbc1c049c625be0c1a7c2cbe094e248bda04c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efd01c8329a8bf697749a90cf9b90a7853c684952f49dba4cd989526d51c043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayTrustedClientCertificate",
    jsii_struct_bases=[],
    name_mapping={"data": "data", "name": "name"},
)
class ApplicationGatewayTrustedClientCertificate:
    def __init__(self, *, data: builtins.str, name: builtins.str) -> None:
        '''
        :param data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#data ApplicationGateway#data}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b257997626dd239fd897f91e2a04881213d3fb82c98859392e722dbdf0f5b41)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
            "name": name,
        }

    @builtins.property
    def data(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#data ApplicationGateway#data}.'''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayTrustedClientCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayTrustedClientCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayTrustedClientCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d87d4571c553e60ba09db506ddf09b57f51e04745811d1243cce4b64465d317)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayTrustedClientCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedb78f9a860dea2b1cc2894f85213188a3b4b6d777cdc253a636afc99906994)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayTrustedClientCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129d7c05dd4d8f0de5975f7e96c6c3d7f312cc37da8061cb328325a128c28d8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12daccedf1237fec2a17c10b6e50271e22e37cc5bd4be70f63c3320a2c60837d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d25c3b0303060e055cee3b17460ddccb1e4a651e7c5d601f077f99ad10a61abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayTrustedClientCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayTrustedClientCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayTrustedClientCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c78f43604b0a58934a190765b1dc9f8c4b2d5a33a393fd4a8ef87aad91a980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayTrustedClientCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayTrustedClientCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b14f6264406e49741d9614cb1a406d03dac3fe83cb868e6be64127fd96654bf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0d60b34328212b810d1d1c35b2b03e836750d2fef3f4b6e8e87fdb01ab5276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fe4fcc3241d1faf605bb3fc1287035cc33a396a4d440fa321ab1752372b9d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTrustedClientCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTrustedClientCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTrustedClientCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b818e047e64abeed9d36919ba5aa3f673f703148c03b7f67dbdaf156e2fc02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayTrustedRootCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "data": "data",
        "key_vault_secret_id": "keyVaultSecretId",
    },
)
class ApplicationGatewayTrustedRootCertificate:
    def __init__(
        self,
        *,
        name: builtins.str,
        data: typing.Optional[builtins.str] = None,
        key_vault_secret_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#data ApplicationGateway#data}.
        :param key_vault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#key_vault_secret_id ApplicationGateway#key_vault_secret_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8985a3d01c984d29f2646c3ac56a15ffa0750a63b2ef9464454c2891fc43efd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument key_vault_secret_id", value=key_vault_secret_id, expected_type=type_hints["key_vault_secret_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if data is not None:
            self._values["data"] = data
        if key_vault_secret_id is not None:
            self._values["key_vault_secret_id"] = key_vault_secret_id

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#data ApplicationGateway#data}.'''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_secret_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#key_vault_secret_id ApplicationGateway#key_vault_secret_id}.'''
        result = self._values.get("key_vault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayTrustedRootCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayTrustedRootCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayTrustedRootCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b279f4d10dda2a1fe90af8c8e78f990183f7d26c6ba30cd586cef845f28ccaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayTrustedRootCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3343ff37998532a5ed4f22018b54c8615b274b7309f79f6086bcbc9ee23da7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayTrustedRootCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c473c902734ef3f423dcfa190b461c523e8649f0faade5221c9f7e5ba3df3049)
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
            type_hints = typing.get_type_hints(_typecheckingstub__779ea20e91c26f4790ad9eb0230690292c015ea72961852a153bd6df50f4a1ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45dd4ab637e48e32686d9360c08ef698ecb7f2d98628240a345956781e8f0fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayTrustedRootCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayTrustedRootCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayTrustedRootCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c697b8de32dcd34d9cd69939854a4e2bd3493890ab21ccca1a70c54c37288ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayTrustedRootCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayTrustedRootCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18cd6f2876dce4efa67e4f8602676a2536ed6c460809d93ef6ff0f6597bc6288)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetKeyVaultSecretId")
    def reset_key_vault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultSecretId", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretIdInput")
    def key_vault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92005415d80b82797225322072fc965a8646d5b71b6202815dc2327f9efe79ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretId")
    def key_vault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultSecretId"))

    @key_vault_secret_id.setter
    def key_vault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757c61b45a034056d69eedf4963f3f019913cada038f1af77b1e1aa1e697adf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d52e40e1699d35c90eec811109767227dafed5eb253c89e11b7d09ea41c4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTrustedRootCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTrustedRootCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTrustedRootCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27dc1f64667430b9e2214485a8bc69f957d2380d7c0d38dbc67174c13113ab49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayUrlPathMap",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "path_rule": "pathRule",
        "default_backend_address_pool_name": "defaultBackendAddressPoolName",
        "default_backend_http_settings_name": "defaultBackendHttpSettingsName",
        "default_redirect_configuration_name": "defaultRedirectConfigurationName",
        "default_rewrite_rule_set_name": "defaultRewriteRuleSetName",
    },
)
class ApplicationGatewayUrlPathMap:
    def __init__(
        self,
        *,
        name: builtins.str,
        path_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayUrlPathMapPathRule", typing.Dict[builtins.str, typing.Any]]]],
        default_backend_address_pool_name: typing.Optional[builtins.str] = None,
        default_backend_http_settings_name: typing.Optional[builtins.str] = None,
        default_redirect_configuration_name: typing.Optional[builtins.str] = None,
        default_rewrite_rule_set_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param path_rule: path_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#path_rule ApplicationGateway#path_rule}
        :param default_backend_address_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#default_backend_address_pool_name ApplicationGateway#default_backend_address_pool_name}.
        :param default_backend_http_settings_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#default_backend_http_settings_name ApplicationGateway#default_backend_http_settings_name}.
        :param default_redirect_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#default_redirect_configuration_name ApplicationGateway#default_redirect_configuration_name}.
        :param default_rewrite_rule_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#default_rewrite_rule_set_name ApplicationGateway#default_rewrite_rule_set_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2052ff898c831ab7f8d0466a21cf0a0ae5e20ad0a97b9941219e3dd31242f922)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path_rule", value=path_rule, expected_type=type_hints["path_rule"])
            check_type(argname="argument default_backend_address_pool_name", value=default_backend_address_pool_name, expected_type=type_hints["default_backend_address_pool_name"])
            check_type(argname="argument default_backend_http_settings_name", value=default_backend_http_settings_name, expected_type=type_hints["default_backend_http_settings_name"])
            check_type(argname="argument default_redirect_configuration_name", value=default_redirect_configuration_name, expected_type=type_hints["default_redirect_configuration_name"])
            check_type(argname="argument default_rewrite_rule_set_name", value=default_rewrite_rule_set_name, expected_type=type_hints["default_rewrite_rule_set_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path_rule": path_rule,
        }
        if default_backend_address_pool_name is not None:
            self._values["default_backend_address_pool_name"] = default_backend_address_pool_name
        if default_backend_http_settings_name is not None:
            self._values["default_backend_http_settings_name"] = default_backend_http_settings_name
        if default_redirect_configuration_name is not None:
            self._values["default_redirect_configuration_name"] = default_redirect_configuration_name
        if default_rewrite_rule_set_name is not None:
            self._values["default_rewrite_rule_set_name"] = default_rewrite_rule_set_name

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayUrlPathMapPathRule"]]:
        '''path_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#path_rule ApplicationGateway#path_rule}
        '''
        result = self._values.get("path_rule")
        assert result is not None, "Required property 'path_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayUrlPathMapPathRule"]], result)

    @builtins.property
    def default_backend_address_pool_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#default_backend_address_pool_name ApplicationGateway#default_backend_address_pool_name}.'''
        result = self._values.get("default_backend_address_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_backend_http_settings_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#default_backend_http_settings_name ApplicationGateway#default_backend_http_settings_name}.'''
        result = self._values.get("default_backend_http_settings_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_redirect_configuration_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#default_redirect_configuration_name ApplicationGateway#default_redirect_configuration_name}.'''
        result = self._values.get("default_redirect_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_rewrite_rule_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#default_rewrite_rule_set_name ApplicationGateway#default_rewrite_rule_set_name}.'''
        result = self._values.get("default_rewrite_rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayUrlPathMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayUrlPathMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayUrlPathMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee2b1a47fd5bb8918c2e7d83d8d4d950fb19ed737371b7320abf76492888876d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApplicationGatewayUrlPathMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb5027b3725041d10083aaaaf3947243581ddd6f156c5f0460144c681ff6bab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayUrlPathMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85194969376798eb55c9baf10030d50d43febfc97608cf7d33c01af545f358f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b7bc21897f9e0c2c1d24eb8044881555fb5df2453d68eced2b0c82dfd2ee0b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66e5ce1817013e82a47c3bd2e3201a642374658bd86d0dd667280ce7381e0d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayUrlPathMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayUrlPathMap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayUrlPathMap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__effe880be581b97f1d179b28d2069c3fb28db3ebac6e609e58c81d7de6a2708c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayUrlPathMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayUrlPathMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aac315ddbef3c69acbd0b328d45b8bda4a06d16e8c2054fac69cb91cb12e8c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPathRule")
    def put_path_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayUrlPathMapPathRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c065598070a809ae38a631974fa8257b3c11a864dd9ae7f995fc244a802918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPathRule", [value]))

    @jsii.member(jsii_name="resetDefaultBackendAddressPoolName")
    def reset_default_backend_address_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBackendAddressPoolName", []))

    @jsii.member(jsii_name="resetDefaultBackendHttpSettingsName")
    def reset_default_backend_http_settings_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBackendHttpSettingsName", []))

    @jsii.member(jsii_name="resetDefaultRedirectConfigurationName")
    def reset_default_redirect_configuration_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRedirectConfigurationName", []))

    @jsii.member(jsii_name="resetDefaultRewriteRuleSetName")
    def reset_default_rewrite_rule_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRewriteRuleSetName", []))

    @builtins.property
    @jsii.member(jsii_name="defaultBackendAddressPoolId")
    def default_backend_address_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBackendAddressPoolId"))

    @builtins.property
    @jsii.member(jsii_name="defaultBackendHttpSettingsId")
    def default_backend_http_settings_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBackendHttpSettingsId"))

    @builtins.property
    @jsii.member(jsii_name="defaultRedirectConfigurationId")
    def default_redirect_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRedirectConfigurationId"))

    @builtins.property
    @jsii.member(jsii_name="defaultRewriteRuleSetId")
    def default_rewrite_rule_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRewriteRuleSetId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="pathRule")
    def path_rule(self) -> "ApplicationGatewayUrlPathMapPathRuleList":
        return typing.cast("ApplicationGatewayUrlPathMapPathRuleList", jsii.get(self, "pathRule"))

    @builtins.property
    @jsii.member(jsii_name="defaultBackendAddressPoolNameInput")
    def default_backend_address_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBackendAddressPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBackendHttpSettingsNameInput")
    def default_backend_http_settings_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBackendHttpSettingsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRedirectConfigurationNameInput")
    def default_redirect_configuration_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultRedirectConfigurationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRewriteRuleSetNameInput")
    def default_rewrite_rule_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultRewriteRuleSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathRuleInput")
    def path_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayUrlPathMapPathRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayUrlPathMapPathRule"]]], jsii.get(self, "pathRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBackendAddressPoolName")
    def default_backend_address_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBackendAddressPoolName"))

    @default_backend_address_pool_name.setter
    def default_backend_address_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3824044fc9433b86dff201e87685f79b059bbcb779222c7e961f08fbf0318d72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBackendAddressPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultBackendHttpSettingsName")
    def default_backend_http_settings_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBackendHttpSettingsName"))

    @default_backend_http_settings_name.setter
    def default_backend_http_settings_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906300a0409ac9d66b785d40e97bd584556f0e2fca05bb8272f952578f6256b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBackendHttpSettingsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRedirectConfigurationName")
    def default_redirect_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRedirectConfigurationName"))

    @default_redirect_configuration_name.setter
    def default_redirect_configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3513c9235e179a530fcbb9b9d69b1ff558fd45ab0bf0afaf5bb0aaa60ecac05f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRedirectConfigurationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRewriteRuleSetName")
    def default_rewrite_rule_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRewriteRuleSetName"))

    @default_rewrite_rule_set_name.setter
    def default_rewrite_rule_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d70ef0cf28258159a1bff253cf8f3afdb145578d0d9c46e3b6d84bef8bb93edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRewriteRuleSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164e5457d09bb84f36d2670512aa99c7afead6aabc96f7bbaacc3802fdb51edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayUrlPathMap]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayUrlPathMap]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayUrlPathMap]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a134f9b8422eb15941692951c41305c3badb134a8225a72a2970602826d08ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayUrlPathMapPathRule",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "paths": "paths",
        "backend_address_pool_name": "backendAddressPoolName",
        "backend_http_settings_name": "backendHttpSettingsName",
        "firewall_policy_id": "firewallPolicyId",
        "redirect_configuration_name": "redirectConfigurationName",
        "rewrite_rule_set_name": "rewriteRuleSetName",
    },
)
class ApplicationGatewayUrlPathMapPathRule:
    def __init__(
        self,
        *,
        name: builtins.str,
        paths: typing.Sequence[builtins.str],
        backend_address_pool_name: typing.Optional[builtins.str] = None,
        backend_http_settings_name: typing.Optional[builtins.str] = None,
        firewall_policy_id: typing.Optional[builtins.str] = None,
        redirect_configuration_name: typing.Optional[builtins.str] = None,
        rewrite_rule_set_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#paths ApplicationGateway#paths}.
        :param backend_address_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_address_pool_name ApplicationGateway#backend_address_pool_name}.
        :param backend_http_settings_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_http_settings_name ApplicationGateway#backend_http_settings_name}.
        :param firewall_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_policy_id ApplicationGateway#firewall_policy_id}.
        :param redirect_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#redirect_configuration_name ApplicationGateway#redirect_configuration_name}.
        :param rewrite_rule_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rewrite_rule_set_name ApplicationGateway#rewrite_rule_set_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b427fbef40482ced6598a230f08325787a80212d3846e5fb8e684ccbbd44258d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument backend_address_pool_name", value=backend_address_pool_name, expected_type=type_hints["backend_address_pool_name"])
            check_type(argname="argument backend_http_settings_name", value=backend_http_settings_name, expected_type=type_hints["backend_http_settings_name"])
            check_type(argname="argument firewall_policy_id", value=firewall_policy_id, expected_type=type_hints["firewall_policy_id"])
            check_type(argname="argument redirect_configuration_name", value=redirect_configuration_name, expected_type=type_hints["redirect_configuration_name"])
            check_type(argname="argument rewrite_rule_set_name", value=rewrite_rule_set_name, expected_type=type_hints["rewrite_rule_set_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "paths": paths,
        }
        if backend_address_pool_name is not None:
            self._values["backend_address_pool_name"] = backend_address_pool_name
        if backend_http_settings_name is not None:
            self._values["backend_http_settings_name"] = backend_http_settings_name
        if firewall_policy_id is not None:
            self._values["firewall_policy_id"] = firewall_policy_id
        if redirect_configuration_name is not None:
            self._values["redirect_configuration_name"] = redirect_configuration_name
        if rewrite_rule_set_name is not None:
            self._values["rewrite_rule_set_name"] = rewrite_rule_set_name

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#name ApplicationGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#paths ApplicationGateway#paths}.'''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def backend_address_pool_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_address_pool_name ApplicationGateway#backend_address_pool_name}.'''
        result = self._values.get("backend_address_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backend_http_settings_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#backend_http_settings_name ApplicationGateway#backend_http_settings_name}.'''
        result = self._values.get("backend_http_settings_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_policy_id ApplicationGateway#firewall_policy_id}.'''
        result = self._values.get("firewall_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_configuration_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#redirect_configuration_name ApplicationGateway#redirect_configuration_name}.'''
        result = self._values.get("redirect_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rewrite_rule_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rewrite_rule_set_name ApplicationGateway#rewrite_rule_set_name}.'''
        result = self._values.get("rewrite_rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayUrlPathMapPathRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayUrlPathMapPathRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayUrlPathMapPathRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd03c0fdeface211d6c9336cd3cfe58d0f37fb2cc82bd16b987069a90df0641e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayUrlPathMapPathRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c50c36d32b17f252e8212f9cf69eb8ddf27873bee2a85ccd5ed93e287d67da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayUrlPathMapPathRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25cd9b336a85137d3bae55bb1624d5ee0d8efb006d5cefb2a1fbc718222de1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4294587a9de64d8c4fcf4701a4095e10d59a2fd1206503e8170cb2d42f8a111)
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
            type_hints = typing.get_type_hints(_typecheckingstub__667fe417f68560bfc1d94d1cd735b738b06fc224dcf4a1fed686d0b0df252df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayUrlPathMapPathRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayUrlPathMapPathRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayUrlPathMapPathRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5200fa2b684ad83ae7466311511707e2940efeb1a59e53029ef31664e7e7bb26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayUrlPathMapPathRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayUrlPathMapPathRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__478bde2ac3cdb1eacdda026028ef02e25576aa7a61271d84b4537238d5446362)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackendAddressPoolName")
    def reset_backend_address_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendAddressPoolName", []))

    @jsii.member(jsii_name="resetBackendHttpSettingsName")
    def reset_backend_http_settings_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendHttpSettingsName", []))

    @jsii.member(jsii_name="resetFirewallPolicyId")
    def reset_firewall_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirewallPolicyId", []))

    @jsii.member(jsii_name="resetRedirectConfigurationName")
    def reset_redirect_configuration_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectConfigurationName", []))

    @jsii.member(jsii_name="resetRewriteRuleSetName")
    def reset_rewrite_rule_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewriteRuleSetName", []))

    @builtins.property
    @jsii.member(jsii_name="backendAddressPoolId")
    def backend_address_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendAddressPoolId"))

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettingsId")
    def backend_http_settings_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendHttpSettingsId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="redirectConfigurationId")
    def redirect_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectConfigurationId"))

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSetId")
    def rewrite_rule_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rewriteRuleSetId"))

    @builtins.property
    @jsii.member(jsii_name="backendAddressPoolNameInput")
    def backend_address_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendAddressPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettingsNameInput")
    def backend_http_settings_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendHttpSettingsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyIdInput")
    def firewall_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectConfigurationNameInput")
    def redirect_configuration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectConfigurationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSetNameInput")
    def rewrite_rule_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rewriteRuleSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="backendAddressPoolName")
    def backend_address_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendAddressPoolName"))

    @backend_address_pool_name.setter
    def backend_address_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ecbd21cb5b886c1bbf9410e4a1267f97661ba4c8e7c5bcf7b9758f9779dc4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendAddressPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettingsName")
    def backend_http_settings_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendHttpSettingsName"))

    @backend_http_settings_name.setter
    def backend_http_settings_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d650bcdd0317a173c8050775985410e7ff37c175e23b6885b0492c0faa8993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendHttpSettingsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyId")
    def firewall_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyId"))

    @firewall_policy_id.setter
    def firewall_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8375f8c286b87aa5d4a2576340102c09e78212c37e6c1ee9112a3f2e832139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112b810c7e0e5e449b32e62c1b8642d24b43a771c892107b2061c7fa16ef7c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f65aa7aff07fde52d24d65449a941fe8a94dc0cd5b8288eb8358c076c806312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectConfigurationName")
    def redirect_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectConfigurationName"))

    @redirect_configuration_name.setter
    def redirect_configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d99322be1dd53b2bdebbe0fcb720e4082db33a8568a956e26462d06434843e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectConfigurationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSetName")
    def rewrite_rule_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rewriteRuleSetName"))

    @rewrite_rule_set_name.setter
    def rewrite_rule_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f80a3956135b6d175b6635f0c2f2b5278b414c1dcc468c03db95684b71c5351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rewriteRuleSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayUrlPathMapPathRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayUrlPathMapPathRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayUrlPathMapPathRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047ecae8bbf8fa443c06fe2b2a2703af26c7d0077f0941a61e493cf8142411b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayWafConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "firewall_mode": "firewallMode",
        "rule_set_version": "ruleSetVersion",
        "disabled_rule_group": "disabledRuleGroup",
        "exclusion": "exclusion",
        "file_upload_limit_mb": "fileUploadLimitMb",
        "max_request_body_size_kb": "maxRequestBodySizeKb",
        "request_body_check": "requestBodyCheck",
        "rule_set_type": "ruleSetType",
    },
)
class ApplicationGatewayWafConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        firewall_mode: builtins.str,
        rule_set_version: builtins.str,
        disabled_rule_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayWafConfigurationDisabledRuleGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApplicationGatewayWafConfigurationExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        file_upload_limit_mb: typing.Optional[jsii.Number] = None,
        max_request_body_size_kb: typing.Optional[jsii.Number] = None,
        request_body_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rule_set_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#enabled ApplicationGateway#enabled}.
        :param firewall_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_mode ApplicationGateway#firewall_mode}.
        :param rule_set_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_set_version ApplicationGateway#rule_set_version}.
        :param disabled_rule_group: disabled_rule_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#disabled_rule_group ApplicationGateway#disabled_rule_group}
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#exclusion ApplicationGateway#exclusion}
        :param file_upload_limit_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#file_upload_limit_mb ApplicationGateway#file_upload_limit_mb}.
        :param max_request_body_size_kb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#max_request_body_size_kb ApplicationGateway#max_request_body_size_kb}.
        :param request_body_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_body_check ApplicationGateway#request_body_check}.
        :param rule_set_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_set_type ApplicationGateway#rule_set_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea565dca3bdf049c8577e0fdc9ac97bcb1231d96fa2133643955799d892bc5c)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument firewall_mode", value=firewall_mode, expected_type=type_hints["firewall_mode"])
            check_type(argname="argument rule_set_version", value=rule_set_version, expected_type=type_hints["rule_set_version"])
            check_type(argname="argument disabled_rule_group", value=disabled_rule_group, expected_type=type_hints["disabled_rule_group"])
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
            check_type(argname="argument file_upload_limit_mb", value=file_upload_limit_mb, expected_type=type_hints["file_upload_limit_mb"])
            check_type(argname="argument max_request_body_size_kb", value=max_request_body_size_kb, expected_type=type_hints["max_request_body_size_kb"])
            check_type(argname="argument request_body_check", value=request_body_check, expected_type=type_hints["request_body_check"])
            check_type(argname="argument rule_set_type", value=rule_set_type, expected_type=type_hints["rule_set_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "firewall_mode": firewall_mode,
            "rule_set_version": rule_set_version,
        }
        if disabled_rule_group is not None:
            self._values["disabled_rule_group"] = disabled_rule_group
        if exclusion is not None:
            self._values["exclusion"] = exclusion
        if file_upload_limit_mb is not None:
            self._values["file_upload_limit_mb"] = file_upload_limit_mb
        if max_request_body_size_kb is not None:
            self._values["max_request_body_size_kb"] = max_request_body_size_kb
        if request_body_check is not None:
            self._values["request_body_check"] = request_body_check
        if rule_set_type is not None:
            self._values["rule_set_type"] = rule_set_type

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#enabled ApplicationGateway#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def firewall_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#firewall_mode ApplicationGateway#firewall_mode}.'''
        result = self._values.get("firewall_mode")
        assert result is not None, "Required property 'firewall_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_set_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_set_version ApplicationGateway#rule_set_version}.'''
        result = self._values.get("rule_set_version")
        assert result is not None, "Required property 'rule_set_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disabled_rule_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayWafConfigurationDisabledRuleGroup"]]]:
        '''disabled_rule_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#disabled_rule_group ApplicationGateway#disabled_rule_group}
        '''
        result = self._values.get("disabled_rule_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayWafConfigurationDisabledRuleGroup"]]], result)

    @builtins.property
    def exclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayWafConfigurationExclusion"]]]:
        '''exclusion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#exclusion ApplicationGateway#exclusion}
        '''
        result = self._values.get("exclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApplicationGatewayWafConfigurationExclusion"]]], result)

    @builtins.property
    def file_upload_limit_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#file_upload_limit_mb ApplicationGateway#file_upload_limit_mb}.'''
        result = self._values.get("file_upload_limit_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_request_body_size_kb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#max_request_body_size_kb ApplicationGateway#max_request_body_size_kb}.'''
        result = self._values.get("max_request_body_size_kb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def request_body_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#request_body_check ApplicationGateway#request_body_check}.'''
        result = self._values.get("request_body_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rule_set_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_set_type ApplicationGateway#rule_set_type}.'''
        result = self._values.get("rule_set_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayWafConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayWafConfigurationDisabledRuleGroup",
    jsii_struct_bases=[],
    name_mapping={"rule_group_name": "ruleGroupName", "rules": "rules"},
)
class ApplicationGatewayWafConfigurationDisabledRuleGroup:
    def __init__(
        self,
        *,
        rule_group_name: builtins.str,
        rules: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param rule_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_group_name ApplicationGateway#rule_group_name}.
        :param rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rules ApplicationGateway#rules}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6d5b56a8ca7e5d30e4bfe477d91398f4602c93e0b31c163c1499a1ac159ae9)
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_group_name": rule_group_name,
        }
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def rule_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rule_group_name ApplicationGateway#rule_group_name}.'''
        result = self._values.get("rule_group_name")
        assert result is not None, "Required property 'rule_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#rules ApplicationGateway#rules}.'''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayWafConfigurationDisabledRuleGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayWafConfigurationDisabledRuleGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayWafConfigurationDisabledRuleGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03466e1903a50984f06113cab7b97f4e32f2e98f1cd43ea2b9b07d2c1c0bc3d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayWafConfigurationDisabledRuleGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac07c7f6a5d23bdc346b209ce8bd52ce1836008861447010de122990fc75a89c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayWafConfigurationDisabledRuleGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7f47f7e8277e266376ed050830b775126a224a375d9db465e750fdba1b97e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fb77051e8226d9be7cf98d99cb5e17e9c6f2e9bc5091f281943b9e8d69599af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a71853bb343d5e3bed4e8d2e87096a9f5feba74283ef2b72f6d075002328125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationDisabledRuleGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationDisabledRuleGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationDisabledRuleGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfb1e357ee12eb045439c94ecff4cddd5193e54f2bbfe1c89f6f777b9e72642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayWafConfigurationDisabledRuleGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayWafConfigurationDisabledRuleGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__755dc482e813b1a8a97f6fb29e4a58f72d9bad6d9caa09a4743fb75644bf9c75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupNameInput")
    def rule_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleGroupName")
    def rule_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupName"))

    @rule_group_name.setter
    def rule_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3afb99fc5ceb9221eec9a36b4d25efe4d29073c62dc9b5db01ec1917fce73c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "rules"))

    @rules.setter
    def rules(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60868e9133b702e90388a7d6fcd4fb7950ab708748a9195f55e55c7d1640f12e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayWafConfigurationDisabledRuleGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayWafConfigurationDisabledRuleGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayWafConfigurationDisabledRuleGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c582591c70e6ec0a9768bbdb87fb89ed1dfb01fbb003045f320d5970912823b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayWafConfigurationExclusion",
    jsii_struct_bases=[],
    name_mapping={
        "match_variable": "matchVariable",
        "selector": "selector",
        "selector_match_operator": "selectorMatchOperator",
    },
)
class ApplicationGatewayWafConfigurationExclusion:
    def __init__(
        self,
        *,
        match_variable: builtins.str,
        selector: typing.Optional[builtins.str] = None,
        selector_match_operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_variable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#match_variable ApplicationGateway#match_variable}.
        :param selector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#selector ApplicationGateway#selector}.
        :param selector_match_operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#selector_match_operator ApplicationGateway#selector_match_operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5516339317c98ce268f2b07fb4011495fb52426021c9da8ccdd0c30632b54a40)
            check_type(argname="argument match_variable", value=match_variable, expected_type=type_hints["match_variable"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument selector_match_operator", value=selector_match_operator, expected_type=type_hints["selector_match_operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_variable": match_variable,
        }
        if selector is not None:
            self._values["selector"] = selector
        if selector_match_operator is not None:
            self._values["selector_match_operator"] = selector_match_operator

    @builtins.property
    def match_variable(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#match_variable ApplicationGateway#match_variable}.'''
        result = self._values.get("match_variable")
        assert result is not None, "Required property 'match_variable' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#selector ApplicationGateway#selector}.'''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def selector_match_operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/application_gateway#selector_match_operator ApplicationGateway#selector_match_operator}.'''
        result = self._values.get("selector_match_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationGatewayWafConfigurationExclusion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationGatewayWafConfigurationExclusionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayWafConfigurationExclusionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eca74eec5ed49495b483159d9b447b42c7789df3ca44b1e547eaf7c8d315360a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApplicationGatewayWafConfigurationExclusionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a9654d168cbc5f65536423655ddc3075448a317b6dc71c4b02f8f22f833532)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApplicationGatewayWafConfigurationExclusionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2289d4569064c36af4a3c8cef84548a0d61a8ee2113e5e84971644616ee01f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4730f3eb6b8601960f89e6c5085862c44a98860e95354d45c31236c73b6b0991)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43e2116936f53ca582abe6917e56b469dcc9b65039f464d0e68b1dac3679eedb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationExclusion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationExclusion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13b36f6722596ab1614368c26dd331285a17be5712cea03cc8d633cd2dffe4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayWafConfigurationExclusionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayWafConfigurationExclusionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e630616406e7bbd888f5f8c82ec4521b0478c30923619cfc72df676e6f949d8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @jsii.member(jsii_name="resetSelectorMatchOperator")
    def reset_selector_match_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectorMatchOperator", []))

    @builtins.property
    @jsii.member(jsii_name="matchVariableInput")
    def match_variable_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorMatchOperatorInput")
    def selector_match_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorMatchOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="matchVariable")
    def match_variable(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchVariable"))

    @match_variable.setter
    def match_variable(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e3809a2938b1d70b3ae81fd053a67ebf5e8eb3e88ebf92695d0ab31cd38600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchVariable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a3705d4dcae37e3c8458802c7e50e0517ad9ffa66fad5cff15a08cef65b721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selectorMatchOperator")
    def selector_match_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selectorMatchOperator"))

    @selector_match_operator.setter
    def selector_match_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f9a82f8ee25e31f3888ca765e8b77d0e2877ff2f026e8817fd333f142db722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectorMatchOperator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayWafConfigurationExclusion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayWafConfigurationExclusion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayWafConfigurationExclusion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b294b6cc4899029c804678cab2aaf5c48dd4252d5a3f54f1749391fd4f2b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApplicationGatewayWafConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.applicationGateway.ApplicationGatewayWafConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b9f02e5f0a63910081b252c69b470b3a8d6def8b11053e37f4713caabb4a00a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDisabledRuleGroup")
    def put_disabled_rule_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayWafConfigurationDisabledRuleGroup, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a134314d776ec48b47aeaea30f6595ed41facf9a6ea8f09891dcd25eea34755c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisabledRuleGroup", [value]))

    @jsii.member(jsii_name="putExclusion")
    def put_exclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayWafConfigurationExclusion, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29deabb4ba2df8ef2f7e6780a8b8baf9904175ddb04f7efe4ef19ca6a3ac9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusion", [value]))

    @jsii.member(jsii_name="resetDisabledRuleGroup")
    def reset_disabled_rule_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledRuleGroup", []))

    @jsii.member(jsii_name="resetExclusion")
    def reset_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusion", []))

    @jsii.member(jsii_name="resetFileUploadLimitMb")
    def reset_file_upload_limit_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUploadLimitMb", []))

    @jsii.member(jsii_name="resetMaxRequestBodySizeKb")
    def reset_max_request_body_size_kb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRequestBodySizeKb", []))

    @jsii.member(jsii_name="resetRequestBodyCheck")
    def reset_request_body_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBodyCheck", []))

    @jsii.member(jsii_name="resetRuleSetType")
    def reset_rule_set_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleSetType", []))

    @builtins.property
    @jsii.member(jsii_name="disabledRuleGroup")
    def disabled_rule_group(
        self,
    ) -> ApplicationGatewayWafConfigurationDisabledRuleGroupList:
        return typing.cast(ApplicationGatewayWafConfigurationDisabledRuleGroupList, jsii.get(self, "disabledRuleGroup"))

    @builtins.property
    @jsii.member(jsii_name="exclusion")
    def exclusion(self) -> ApplicationGatewayWafConfigurationExclusionList:
        return typing.cast(ApplicationGatewayWafConfigurationExclusionList, jsii.get(self, "exclusion"))

    @builtins.property
    @jsii.member(jsii_name="disabledRuleGroupInput")
    def disabled_rule_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationDisabledRuleGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationDisabledRuleGroup]]], jsii.get(self, "disabledRuleGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionInput")
    def exclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationExclusion]]], jsii.get(self, "exclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUploadLimitMbInput")
    def file_upload_limit_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fileUploadLimitMbInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallModeInput")
    def firewall_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallModeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRequestBodySizeKbInput")
    def max_request_body_size_kb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRequestBodySizeKbInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyCheckInput")
    def request_body_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestBodyCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleSetTypeInput")
    def rule_set_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleSetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleSetVersionInput")
    def rule_set_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleSetVersionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a879f5dac1f7927cb71759602ac36eb4756ad366f598d39903a0e70ac59dea25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUploadLimitMb")
    def file_upload_limit_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileUploadLimitMb"))

    @file_upload_limit_mb.setter
    def file_upload_limit_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6897b3e3763c3f5cabb2d108282ae35aacc450dafa177c5d21364089921a6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUploadLimitMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firewallMode")
    def firewall_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallMode"))

    @firewall_mode.setter
    def firewall_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5289d7323d4773f99a3b5c27f938e18f22f8afc8c10da579480632114af51e0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequestBodySizeKb")
    def max_request_body_size_kb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequestBodySizeKb"))

    @max_request_body_size_kb.setter
    def max_request_body_size_kb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec11a81d570cda52ef7ad878478bd207a5e41c18adde6c3d2a371567296ab42d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequestBodySizeKb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestBodyCheck")
    def request_body_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestBodyCheck"))

    @request_body_check.setter
    def request_body_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a786029f7c0ff487ebf2695f6f10606103e47ad14e5091e691fb51806f3c242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestBodyCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleSetType")
    def rule_set_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleSetType"))

    @rule_set_type.setter
    def rule_set_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36071c41bc0ac653aedc8075fb8b669cfc57f62b4162f00a85ef047ec2373414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleSetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleSetVersion")
    def rule_set_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleSetVersion"))

    @rule_set_version.setter
    def rule_set_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef56d1b5bd393cee5a46e4469744487490b943fc791d6202b90cc474445bc3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleSetVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApplicationGatewayWafConfiguration]:
        return typing.cast(typing.Optional[ApplicationGatewayWafConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApplicationGatewayWafConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d84c4961fcfd6180af753ac8d9acb4b17210688b06cf619bdb1d2f32edc881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApplicationGateway",
    "ApplicationGatewayAuthenticationCertificate",
    "ApplicationGatewayAuthenticationCertificateList",
    "ApplicationGatewayAuthenticationCertificateOutputReference",
    "ApplicationGatewayAutoscaleConfiguration",
    "ApplicationGatewayAutoscaleConfigurationOutputReference",
    "ApplicationGatewayBackendAddressPool",
    "ApplicationGatewayBackendAddressPoolList",
    "ApplicationGatewayBackendAddressPoolOutputReference",
    "ApplicationGatewayBackendHttpSettings",
    "ApplicationGatewayBackendHttpSettingsAuthenticationCertificate",
    "ApplicationGatewayBackendHttpSettingsAuthenticationCertificateList",
    "ApplicationGatewayBackendHttpSettingsAuthenticationCertificateOutputReference",
    "ApplicationGatewayBackendHttpSettingsConnectionDraining",
    "ApplicationGatewayBackendHttpSettingsConnectionDrainingOutputReference",
    "ApplicationGatewayBackendHttpSettingsList",
    "ApplicationGatewayBackendHttpSettingsOutputReference",
    "ApplicationGatewayConfig",
    "ApplicationGatewayCustomErrorConfiguration",
    "ApplicationGatewayCustomErrorConfigurationList",
    "ApplicationGatewayCustomErrorConfigurationOutputReference",
    "ApplicationGatewayFrontendIpConfiguration",
    "ApplicationGatewayFrontendIpConfigurationList",
    "ApplicationGatewayFrontendIpConfigurationOutputReference",
    "ApplicationGatewayFrontendPort",
    "ApplicationGatewayFrontendPortList",
    "ApplicationGatewayFrontendPortOutputReference",
    "ApplicationGatewayGatewayIpConfiguration",
    "ApplicationGatewayGatewayIpConfigurationList",
    "ApplicationGatewayGatewayIpConfigurationOutputReference",
    "ApplicationGatewayGlobal",
    "ApplicationGatewayGlobalOutputReference",
    "ApplicationGatewayHttpListener",
    "ApplicationGatewayHttpListenerCustomErrorConfiguration",
    "ApplicationGatewayHttpListenerCustomErrorConfigurationList",
    "ApplicationGatewayHttpListenerCustomErrorConfigurationOutputReference",
    "ApplicationGatewayHttpListenerList",
    "ApplicationGatewayHttpListenerOutputReference",
    "ApplicationGatewayIdentity",
    "ApplicationGatewayIdentityOutputReference",
    "ApplicationGatewayPrivateEndpointConnection",
    "ApplicationGatewayPrivateEndpointConnectionList",
    "ApplicationGatewayPrivateEndpointConnectionOutputReference",
    "ApplicationGatewayPrivateLinkConfiguration",
    "ApplicationGatewayPrivateLinkConfigurationIpConfiguration",
    "ApplicationGatewayPrivateLinkConfigurationIpConfigurationList",
    "ApplicationGatewayPrivateLinkConfigurationIpConfigurationOutputReference",
    "ApplicationGatewayPrivateLinkConfigurationList",
    "ApplicationGatewayPrivateLinkConfigurationOutputReference",
    "ApplicationGatewayProbe",
    "ApplicationGatewayProbeList",
    "ApplicationGatewayProbeMatch",
    "ApplicationGatewayProbeMatchOutputReference",
    "ApplicationGatewayProbeOutputReference",
    "ApplicationGatewayRedirectConfiguration",
    "ApplicationGatewayRedirectConfigurationList",
    "ApplicationGatewayRedirectConfigurationOutputReference",
    "ApplicationGatewayRequestRoutingRule",
    "ApplicationGatewayRequestRoutingRuleList",
    "ApplicationGatewayRequestRoutingRuleOutputReference",
    "ApplicationGatewayRewriteRuleSet",
    "ApplicationGatewayRewriteRuleSetList",
    "ApplicationGatewayRewriteRuleSetOutputReference",
    "ApplicationGatewayRewriteRuleSetRewriteRule",
    "ApplicationGatewayRewriteRuleSetRewriteRuleCondition",
    "ApplicationGatewayRewriteRuleSetRewriteRuleConditionList",
    "ApplicationGatewayRewriteRuleSetRewriteRuleConditionOutputReference",
    "ApplicationGatewayRewriteRuleSetRewriteRuleList",
    "ApplicationGatewayRewriteRuleSetRewriteRuleOutputReference",
    "ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration",
    "ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationList",
    "ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfigurationOutputReference",
    "ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration",
    "ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationList",
    "ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfigurationOutputReference",
    "ApplicationGatewayRewriteRuleSetRewriteRuleUrl",
    "ApplicationGatewayRewriteRuleSetRewriteRuleUrlOutputReference",
    "ApplicationGatewaySku",
    "ApplicationGatewaySkuOutputReference",
    "ApplicationGatewaySslCertificate",
    "ApplicationGatewaySslCertificateList",
    "ApplicationGatewaySslCertificateOutputReference",
    "ApplicationGatewaySslPolicy",
    "ApplicationGatewaySslPolicyOutputReference",
    "ApplicationGatewaySslProfile",
    "ApplicationGatewaySslProfileList",
    "ApplicationGatewaySslProfileOutputReference",
    "ApplicationGatewaySslProfileSslPolicy",
    "ApplicationGatewaySslProfileSslPolicyOutputReference",
    "ApplicationGatewayTimeouts",
    "ApplicationGatewayTimeoutsOutputReference",
    "ApplicationGatewayTrustedClientCertificate",
    "ApplicationGatewayTrustedClientCertificateList",
    "ApplicationGatewayTrustedClientCertificateOutputReference",
    "ApplicationGatewayTrustedRootCertificate",
    "ApplicationGatewayTrustedRootCertificateList",
    "ApplicationGatewayTrustedRootCertificateOutputReference",
    "ApplicationGatewayUrlPathMap",
    "ApplicationGatewayUrlPathMapList",
    "ApplicationGatewayUrlPathMapOutputReference",
    "ApplicationGatewayUrlPathMapPathRule",
    "ApplicationGatewayUrlPathMapPathRuleList",
    "ApplicationGatewayUrlPathMapPathRuleOutputReference",
    "ApplicationGatewayWafConfiguration",
    "ApplicationGatewayWafConfigurationDisabledRuleGroup",
    "ApplicationGatewayWafConfigurationDisabledRuleGroupList",
    "ApplicationGatewayWafConfigurationDisabledRuleGroupOutputReference",
    "ApplicationGatewayWafConfigurationExclusion",
    "ApplicationGatewayWafConfigurationExclusionList",
    "ApplicationGatewayWafConfigurationExclusionOutputReference",
    "ApplicationGatewayWafConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__27b90d88008c9c386a35f6d2824dd78e7447e8b829eea7c6d7d23b55e0e10d89(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backend_address_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendAddressPool, typing.Dict[builtins.str, typing.Any]]]],
    backend_http_settings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendHttpSettings, typing.Dict[builtins.str, typing.Any]]]],
    frontend_ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayFrontendIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    frontend_port: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayFrontendPort, typing.Dict[builtins.str, typing.Any]]]],
    gateway_ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayGatewayIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    http_listener: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayHttpListener, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    request_routing_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRequestRoutingRule, typing.Dict[builtins.str, typing.Any]]]],
    resource_group_name: builtins.str,
    sku: typing.Union[ApplicationGatewaySku, typing.Dict[builtins.str, typing.Any]],
    authentication_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscale_configuration: typing.Optional[typing.Union[ApplicationGatewayAutoscaleConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_error_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayCustomErrorConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    firewall_policy_id: typing.Optional[builtins.str] = None,
    force_firewall_policy_association: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    global_: typing.Optional[typing.Union[ApplicationGatewayGlobal, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ApplicationGatewayIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayProbe, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redirect_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRedirectConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rewrite_rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssl_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewaySslCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssl_policy: typing.Optional[typing.Union[ApplicationGatewaySslPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_profile: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewaySslProfile, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ApplicationGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_client_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayTrustedClientCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    trusted_root_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayTrustedRootCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_path_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayUrlPathMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    waf_configuration: typing.Optional[typing.Union[ApplicationGatewayWafConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__caff855b114071be2ae34045613db9e0ab26c0bc76be7b1f08b4ecf6c8f3af69(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df942d41ed78b3e6e74a0e283f7a564df8400d87d84c8aad2235bd2f490b763(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bf5de1733030c05f9e72582ec22ce368eeb3f62499609b20a2e61f1d686e68(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendAddressPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f56f8d4f489f30084b0f7be9921261575f73d1d2c642dfa19e4c3ed2ae9482b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendHttpSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e9b5e3632717398f4abe35653c8eee273be90377c20f2e1c91912b55f84559(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayCustomErrorConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6fe15b38f2fd6921099adbbfa888b3d885d65a45d8f9a552a6f9282388b2ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayFrontendIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd7d53509c6113830d35da6028404fc3bf67c52de9a1390105ca4c9246d78e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayFrontendPort, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f9b72339ee66fc6cda7f0f9dde85d6376022256d95ccca4b54905a2584728a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayGatewayIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab57c576d77fbfb1db55047cf6d5bc8909b3c88d1357de9c76511966b03776f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayHttpListener, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ae7c4f9e0abbf5c3e7efd20d421342d0af36923529b6b286995bc63f5de325(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077d68c6f1576f95155cac0ea0f0a670e824a4ee704cfd984f6902e637ece985(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayProbe, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8868548291ee93a449c0853492ad2c868b0e57369c1ad23c3f702856cb27960e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRedirectConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993798f3b9c700f58307a7a9df2490ffffa795c4b822755c71721858d020cec7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRequestRoutingRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c1b2651eb6936c5bec4063b759c80393290e13c1e93e1919baa544adb51238(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2474d0f79155a7b6055eccd9dc2360703df65b4f34c59c6ba101fc36711ed312(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewaySslCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493bdc2bf40e815b05587e277e2f1915ef89f87b1c216a8d4440f71fce6304f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewaySslProfile, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851c1336c31df1030750d273b7003ebbb768984e7d878ed9652e94a0a114ffb2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayTrustedClientCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53dba94acd48b63337c732a5ce45adaeab968538bee0eb2dd86f8c2a38588cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayTrustedRootCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdf427d7848b2b8450395682c23e5b5a1c04fd0ad287ceb60626ff5aebd2340(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayUrlPathMap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3ef380d4f2ee8460d8ba77f88101060028a6bde900cceeb61f534d61b4d754(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1639f202c20b58f94003f894ac1c7f1a2fc206c4ae2198f216432e28626de4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb627469b2dee9fbfdacd4fc20ee7a93146b5b0c5ef4236d3fc6d845eb983651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a485756cd3e918bd080852852aceaf82676b7770c6a2cdc671cef2d4c06077(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3d9e38c3ce3162be5fba6f71ceab3188b09e425754ae4ebd447d6168417c5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563b942bb2718281e3258c017a8d6e28f758a7108078e0cd42bf02f70c7aa42e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ed09c2a46d45e3a5aa79a147595968d7dafa029c49e6582f1bb561d7a410cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e10bce8e08ca6a12f27cf0667b552bdec1d54b616ef4a85f88429a8fc973ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f512089ca246cb99e3bf433e81d200b1462d26a09e8d3fc05d35e0ce07f070a2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb656beb334e7e827bb27c4404d96ed8f4089860079473e37b5cade2f2276653(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c03dc2364969cfcc4fe706e17c021b5bccd93cab50e313207bf6538aa7e062(
    *,
    data: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c29d41728d88b126593cf4cf2e83d1116ba1d50876ea9210b78a43a7b6990c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882007b516d3c1fb2acdc06feeeb68f9fbd17286820e540369da717502d4e174(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e191d24b7e54a471fb1416049c49e111b766942de7bb09e68e9b0b6091d7bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497142c6d57a6598b6acb261004b6a2399588ad18309178dd47921b25a7e629e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f573f6fb465fee9a8aab8d7e1c0850f05f04a9d328d99b9de29101662bdee40(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5351eb7e69a7951986e29af4c6dc04f9f9d0db0d3f786b3ea8fad8544cf020(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayAuthenticationCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3952c7c9b69421d3f80a89ff0cd69d5d7782b5ba28956269388931cea7a4e104(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3937864721807a10d6ffc61392f9ed2af938b8dacddcfb3e824514b0869c9a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae4ddbe37730ea32919a122a8fc619bfec03f44a9f4d1c1af07584fffaeb254(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a394bfc2dfb63478ed28868baf71d56bee215d41cdf8e5121116b67fd21aff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayAuthenticationCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e91ec2068e22998214b74eb5a0fd7e56617f78b27f18216e97b97add995765(
    *,
    min_capacity: jsii.Number,
    max_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c81a54c2eed9f04a07163b9e164cdac0e1ccb6ebaef2ff4d07735908affc94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9760ff0de2d854d6b0f279e188e9c89bb8b33e7280b30bff39b70d27a56c19e9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9cddb854db08063041ba86fe0c7568c6c15e3b8c63c2a9cd4b5b70d05a05f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3b30be1cac78640696feb5e03302bbad6dc3854c3c9656f266c9bd635652fb(
    value: typing.Optional[ApplicationGatewayAutoscaleConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c3ce0810ace6665387dcd6c4932786b9e9bbd27b37c93e602fbfa8561805b3(
    *,
    name: builtins.str,
    fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448ece75ead6543c9032358f350ccab0b5fb868681a81eaae3af36a6c7fc90a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4e8828be27887a9d92cc8fd6e31a36ea2fc433bf5603cf9df7a018a507c416(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe5bfa10ff675fdfc97212fc14c65bbcce4acaab2b250ed55aec52d718a52bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ef62be62640aed7147d5cc73343b7041161b22f4a301d67bb4fc751af27740(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735aaed826bad39af8f77ab96470bc34938898b01e2090398eb033f6e6b386d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b484001450df6fb1659bebd9ca253af63c89d8b340e33632bc3b2448709196cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendAddressPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8505eb9f460df17ffb0a37f1d3e7261a882ddcc519fca0d4d7bf90486b851e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c0abdc89c0f797228bf66d724fdcb3c3588fb2d6ba8eb235d423e7bbc3c54b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc7aad3357c7f9bba65847ccd66695ebb828ecbe935d605fc4e5372dcdb5d76(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bebf85af1f35266c247a49781987024127cf257c27d8b2f3f79ea085f8807bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b11866fa662615c8d8f0abded6633bd7a792f6076bab68759e71560614cdbf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendAddressPool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54bb34a2cd76b61583d3e05a7efa10d9426bbede66bde8aa6b78d3c95f70b66(
    *,
    cookie_based_affinity: builtins.str,
    name: builtins.str,
    port: jsii.Number,
    protocol: builtins.str,
    affinity_cookie_name: typing.Optional[builtins.str] = None,
    authentication_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendHttpSettingsAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_draining: typing.Optional[typing.Union[ApplicationGatewayBackendHttpSettingsConnectionDraining, typing.Dict[builtins.str, typing.Any]]] = None,
    host_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    pick_host_name_from_backend_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    probe_name: typing.Optional[builtins.str] = None,
    request_timeout: typing.Optional[jsii.Number] = None,
    trusted_root_certificate_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e454512442b4889147cebbff43af59389c1193a8428520e6f26b08d887dac88(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf4dfc6947ee200684a7408e95ab8f24199c3724394db0c36fc82ea34b8095f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03e51d9167528a1732f56419fa3ae6c644772814471b1e0c19d84248aba5224(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea9eaacbc2ac7881b6fa8e6251feee55c165bb755cc51b167130495600ecef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bf4dbcc428c602f94ed3309bdc57df60d84cf720957e6b555ad9575aba6f52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b5e227ce92b7ef0c1ec4a9dd05ff66f56878facc9837d514cb188048c7b5ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abf5f13c03f7f86a0bb1c311dd67e0919e5651b6be0c97492adce94525d75f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657a19cd0d702f96807f84bcf2514f929df9876ab286cb1e7a6fee2a94b94bb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24eaa1597f9cdcff44dff737b3469e535ee2ad2771e594fe12098ebab0b9994c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081386d3be56465ac0f52b51ce78e7707716061e863b95ff90c90f799e144d80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendHttpSettingsAuthenticationCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0011910b9a8ef2dfb486b1801bfe7b27b54594ad1a1725a93d89b2470e0f401(
    *,
    drain_timeout_sec: jsii.Number,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f710f4bcae2ffd4f594ee63c18011b05cd21902844cadbada6676c0271559c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2b69ba474ea646d92403170b1f6658a72d31f69dd0282a4675b11c8996d4d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62499210fe84485e53c12aa766f39a9a7f7375221ab466a28136aabbe75042d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea8fb84bc6fa3ff4b5bef70d4c48ead2f64110f93061558c4714622b12243d0(
    value: typing.Optional[ApplicationGatewayBackendHttpSettingsConnectionDraining],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f029cbdd92ee635177a2ad305fa92f094bf03645ab73980e1f7f88e05c6f30e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95672651b65931ce7b4fa8f59bd4d70ade7bf7b7769f64aa4705ec87835d3bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dfc671cbd6301987e4068d491ed60ace9876a6212ebdbc81e0f604b4080e02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfa93077adbb278303a84e89fcb6caf950019e198dbdd19ece60c46ab3f73a9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085cdb2a75394c8980cd2feb24ffe6df4eb5b0c619a2a30ba90595adea468569(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7517557a4b633524455b72c2adf2bc300921c50042bef8b184c0108aeaa79515(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayBackendHttpSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7630ce60086c223cb8287b5a97c15a9cb19633959a7514ed312c493da3f6eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8cbc71bcc6297842f6d722933be256acddeca1dafa3a8a9b0f82c9de4495a3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendHttpSettingsAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03a8ddcf04585fad750328639f1d28e48ba3ebcc63d30e0c8fb7f16521b80f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3eb986d863a08fec5857052811983c7f6b44bd63949d5497399edb7834abdb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374723b8def63df462a30779816b16972edac61a4a7456ecf08a75a0d58d4273(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe92eb4a3a7c2a96c4045c8af03b232db0a8e4060d1c7c3f6ece975152ec5d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76ef9d3cdbd9111ae5428573f69c9dba96062c27983893eedaa112ef0678be7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31780d4e997232e1f850ad821a9e8145d5eb595de2e088babcca949c1f5532a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbca50917791e438b3dc35c033662b1266045a44cf40a64e003b4ff13ab6314(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0df4cf6f5101bb53d4903846355f2e2d0558d6ea1e26bc52650228105a7f9db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604a524a5603ca590acdb24f7d16a1fd92b51df0eebff9c6d6364ad7aec16670(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f679ffee4d2c2b0723d76ea14f4987a9bf2dec93acae64d671dcfa5a6f38a5e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc78a358fbe5a1f9c95836435cbc7b5a0e2ce410e2613a5e14ed0bef8f7c63d1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c268247603edadfc62a4597145daa17506e6e0fe11f43b3a02b78aa5a6317e8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayBackendHttpSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2914861c7395eccfd51d347790a33a9f80e7bddea0bc020f4e8b0a9b0470bbbe(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backend_address_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendAddressPool, typing.Dict[builtins.str, typing.Any]]]],
    backend_http_settings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayBackendHttpSettings, typing.Dict[builtins.str, typing.Any]]]],
    frontend_ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayFrontendIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    frontend_port: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayFrontendPort, typing.Dict[builtins.str, typing.Any]]]],
    gateway_ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayGatewayIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    http_listener: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayHttpListener, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    request_routing_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRequestRoutingRule, typing.Dict[builtins.str, typing.Any]]]],
    resource_group_name: builtins.str,
    sku: typing.Union[ApplicationGatewaySku, typing.Dict[builtins.str, typing.Any]],
    authentication_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscale_configuration: typing.Optional[typing.Union[ApplicationGatewayAutoscaleConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_error_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayCustomErrorConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    firewall_policy_id: typing.Optional[builtins.str] = None,
    force_firewall_policy_association: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    global_: typing.Optional[typing.Union[ApplicationGatewayGlobal, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ApplicationGatewayIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayProbe, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redirect_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRedirectConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rewrite_rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssl_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewaySslCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssl_policy: typing.Optional[typing.Union[ApplicationGatewaySslPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_profile: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewaySslProfile, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ApplicationGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_client_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayTrustedClientCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    trusted_root_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayTrustedRootCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_path_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayUrlPathMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    waf_configuration: typing.Optional[typing.Union[ApplicationGatewayWafConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0e06fbde9147bdd144723eebf5c530da1e2391b7cdd8479fc00cf7e2ceb031(
    *,
    custom_error_page_url: builtins.str,
    status_code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e064bd6c2471c6a2f351cd674892a66b05be88267c11e93f97cf072d9a51f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c11c89746e5ca15a5fa79d5a2fd34badcf699a787ab8c48ca1f66d3d7a3be20(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc7eeb578807e6b436a0aa2f787a130d12489e7f2ea2cfdeccee8bcd0572e48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81af30144a77c153c1ec286ffd4f982ec97c17044a7f1d5c39ada0f1dd7742f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225db7a541e4bebfa457d0528888b7815459097dcf01d7d47c331f7a40f4cf77(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd44b9def370b6baa5ca8a97d46b9c749cfe49996d1e6734283719a52efff8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayCustomErrorConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ecc9eb325e866fc71953b4bf1e0dd541f4b85f3cec201b45242c45343fd93b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9b52a91c63ba16ff410104fbe966c9a2bbaf6864332cfd2eb58730f3263a3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fa1345040e3a95c3fe5effc1275b4f0ea4e52fa0a56bc1a75fd3d616d4ce38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356f448ac6f1d10e2956ca53a74cfd28d0e800671b4f5a91d15d261924c29b82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayCustomErrorConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b42ddd2f40acaf4fd04c0dfb442b055c6da5575e6f4afa0331acfbf5a879dcd(
    *,
    name: builtins.str,
    private_ip_address: typing.Optional[builtins.str] = None,
    private_ip_address_allocation: typing.Optional[builtins.str] = None,
    private_link_configuration_name: typing.Optional[builtins.str] = None,
    public_ip_address_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50be89fb11991773105169cdaf0184c4db0598246c31740d9d6b1ec26092ba0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def08b7efac37d1d8bc9e5d8288cc8b31a1e3096f355f4ee1020c135824387ef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119361cb236b1816fc81dd748facfecc15f1117374686b80d5f4f6ee35357388(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b28dd57d0084ff96ce839b086508c4e0d3566abe3437044d11d8719a6d7351(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ee7e6f593c5cb04cfa6669dbc13e241eabed036e6cd6cd3dc30677e256e8c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0557a31f712f4708b81690a0de8563cf8c788406b1595bdb19951587388c1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayFrontendIpConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6b303c3a4ce9719acda796349acf532e987f9a0facee607525b8938bf80a77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d42cc8ffac5ae5aabe3d85b0c7f6f495cde5c5801d0e104753565dc82e0a73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf0b1697af7fa79305f2eca0d7c12a65a5d7a376067acf8fdfc540e74d553b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b248cfcb328407d77a78f9cccdc52c54e765b0c23fcfd47462d0d3975100481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d9948816a2a9881d1105a73c59d6780179531a44b919497dd95633f68bfc71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6788a2eec7ce987f435aab983eb4de4a8eb2a804d91af04aa7b164df632a7fdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab1b51b4de274d4f878413cf387cb7281e2f06c79ecfce602ab0fb84675d65b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49acf8ae25122c55a99cf0fb7996643c94791aba4103d57fc6a7216be7bea9f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayFrontendIpConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbbf343e81eb87ae42892a4ff70c2ce43e25b0003eb0446ad52673ed4177be1(
    *,
    name: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b05ef4f0a7e2de33d62a4d190c05a4a4b5468dd63088b2e6360b785f9804401(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed492f51c0f7d3e036914a77292668aacf6921b31d686ef75c0316e443014e51(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f989fee88dc78b5861dece2986993f5b0f395bf42d5dc83acd87e267bc0859e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de89d3e5cf9f899aa1b648d954aa12a1221632a90fda09ce3ebafaa7d920fbf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fce684f486f88554a96beec5e5b030d6d9b5e79dc4124f6311cae735f3d3038(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a984ee003ef06d2bd30af86f831db005713770a5657482203aeb4a11cea6a61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayFrontendPort]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71fbe15a5b50ebbe41f651c10003fc78c165eba31a2e85351e3898379275245(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32429bb01f9a9935c9932a964df9fcb368422c3f0f9439bff2b2fcd112f655eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a06301f37044d074122023f74dbc5398f0ef19694c3646e36501924d6722e92(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648f1cf7decc4ecc6d9911c34b69ceac83e6d6e870cdf94ff7cd7f0aaed6efe6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayFrontendPort]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb626635909190b08d09b7c3dceb7c69dd2a077bfb6a3b0d83d3a7736d24509c(
    *,
    name: builtins.str,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31634eeca957fd344969b1dfced9483e4d41850c4e75bcd413e092b201ee7d0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6044dd3938205c538b7727c0990dcbf3ec06c896161917843d82d5ffde5162d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfb50543f8702a60e1971af1d326cb6e0e469b7b232351b03467e975c4c7e43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2dc0817350cce42e8b46d6f5b48b8cee8dd1e124b12946ccecdd043c9d205f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ed36dc844f93d7744a8d7fae9dabc4d715e83b47842bd6d607e621b9b2c045(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1400b280b1814e8493aa128e48d3842f27570f02db6c2cb56ccf7fda6037e352(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayGatewayIpConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43763c84e1811b6bc60d9465480bd4cb4db13634f1e4a7b6242c912e07f04a13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2af637d695bde470773768df610b3d8bb52c87a225c77405b99d1986313e3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdb50c3f1e256557d12eb75c83fb4f047e22dc18ce232f389a5bf290f50fca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde9323940cf19e0b93ec2d6d5af44f1dd4d32a31b3efbe3fa3ac64172997bc5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayGatewayIpConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bed0450829d0ab40571ea14d5f3d95cc2d0f49ecccef150e46d3b520b0efe8(
    *,
    request_buffering_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    response_buffering_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f22a9e6d2156bfa937866bc69fc98458fde27aba4d861dd55622846122ab845(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcde820483ef404974ca13d836b89535250e28513cd1182d5b7fec1aff46773(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4eeb003bf2173bb9a547a687d98e2bf8b582d5e7c777fb37c6f461fbece500(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80eec620a5fada844bc18440f2b6cfcbb1d6773ae668de1f9a17bf246c716812(
    value: typing.Optional[ApplicationGatewayGlobal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4493cf1c9d9ff39967bd03e148a940036ea0a62bce26e313b379203c6680e419(
    *,
    frontend_ip_configuration_name: builtins.str,
    frontend_port_name: builtins.str,
    name: builtins.str,
    protocol: builtins.str,
    custom_error_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayHttpListenerCustomErrorConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    firewall_policy_id: typing.Optional[builtins.str] = None,
    host_name: typing.Optional[builtins.str] = None,
    host_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_sni: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_certificate_name: typing.Optional[builtins.str] = None,
    ssl_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f308de883db20092eb238fc1d37c1ba602e5695f25f27d5de65711371a1cdb88(
    *,
    custom_error_page_url: builtins.str,
    status_code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39acc46c00cfa46de7ae93d709a92008fc51e9c5e266d2ec0ca988bb604b1df7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ab99e18dc2395d5dcf5358750e6242b187c0a34c168d19e57d1b07f67481ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6e1d9dcc3f49c4d0df686ad48aa39828c1a892ba6c57a23fcd337344da5cb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9833557baf9b7eb6040aa23e8239af431ca55b0d5fccdaad505f9ee3f7bab04(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19dc11431e9c5df8cc33b672812ba73656a90c6fa857ebff0d0b41164637bf8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49b2d7adc86861ba71d3405ee89c196935867bb1b9a8e664ed670a448e9a987(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListenerCustomErrorConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2abd279033f517d7267f8c10c8100261b94b04abe7f911d413eb9a4a1371cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140664298172cc8ad7e3cf1ce3c885715fbb54d89d5fb3311983a93b47a299ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f8f4f2e9d7d00b2205ae515d4735773ed941ceee733a1f4a42803874d49eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c4d6fe47afafa3c76e00002cc160f3a070c026989b77d7f9807a863391a647(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayHttpListenerCustomErrorConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c6f7b93fc6429c6f1146bb5e64e09ad9e627b35ecf4f9586acc9a0ef792851(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1e5686cce489564e7d7e85ddd20213183746bbc911ba94a2dea81a8f0cd5a2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb55da52bcdbc4334c295537b967fb1deffffb1e04d0c3b739a1b92be34d068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1a47b8e7a9fc40b362686b08006ec7bfebf237947b14c224418cd2046b418a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed3879c8ab5abc45d276a09149fcc67cbbec5b5b7baad59168a3148d1a340c6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af597999966cee3712b1a7449196a85fe8060865e3008cc746828a1f5d51af9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayHttpListener]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5bdf5bcf5ff5ea0720c3c40b1ef1f96b9c7f2523fa0bb687742ef9ba3d8776(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afb3e7b2b35eefdae423b8bb9f44815d9f76863e76d2caa8f0e829a237fcf40(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayHttpListenerCustomErrorConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c0b40210a8af590316f00a290844dcd8d4828600a7534be3ae9353c08c6aa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85328c589aae96ca9e3509ee7d6383cd6778f2b2b0ff3b831009c76e3e772603(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e80aa02cfdefc4cf42f2156f4d5eb2426a4ff15bc9689b89aeb10c689e022d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c464da395905681ab3118efb7c5cab73c46765670fc347168ba2d601fdc8cd32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693486cf847ca2e3fdefe57b7ae9b8243b8c101edb67bc4b8fd8d1b0ae05b39d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfd73014b26ebe5b46c39fbe68dae7966117b7b2a517635e474f1ecb0be9420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672130b97fcc1a960995b3e7cc6d2723337a4adf1dc74ab1214680b8057237de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145acbad85f5b4304847ec7e9a164fdbec5d2359bc5d0ddaf82db909bd28dc64(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba2bb4e1b8d2fd68b1511b201d48644c481137e625ae4194c6b779ac386ede2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e48029a5a0036ae654c181132ea562175300f54ff606fa00200287b1f41f69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973027468e3c94a8c965eaee54183812869491771ddd9ca7235061fc36ce5c44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayHttpListener]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00060493fa92e4c69f27b912c6c8961df09126b764804ef03398d76386a4a5f8(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5685b47fbc55b88e506492e030e7dd74871e0c9b98cadc34bc0c837bb70c15b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10146d5e6005381bca1a68340bbe6401b728e599a05e8c0e5d62527ed6fd9748(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9fc754d0976c6350be2cf6ca66ed61db2cf8ed31f72c964ab1566fb895a10e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974ca81a7ec0b8f659f3b14a06e6ae7532a79cba14e20677ca4d7dd62dafaa70(
    value: typing.Optional[ApplicationGatewayIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251cdabb77b1f6a0b2e5fa406eefb23e5727cedfd46225122727743ed0088691(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca25085adf39653da68951a28ab3e879e0cfd55aca819926257f1ace7eba9eec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455a0d913a5d1d4db05c095845602f12dca2eaa2999206ca8909e29bf5b06284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec384649af67d45826f48fbf3e38c55782c0ac0399a38268f366a56b73287c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8faf0e6ba35a690f41cb84c39f45b083ffb8c2701ed7e454a89761e14525386(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51079c926de10119308bed41d62aa36c6e4ecf8dac1a5c89d7df14750fee0a54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a469fe9ceaddd53e9b71547b6191c52d7a204a94fae4cfecfb90cafa25ae3e(
    value: typing.Optional[ApplicationGatewayPrivateEndpointConnection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936360ceffca64082e8feae55b720a29bc30d159f22064a3890071b303b51131(
    *,
    ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayPrivateLinkConfigurationIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fba20740bdc1f1f740fd7a3fa4e6d3685d7bf1f9500cb0622d1cb5d05a4b164(
    *,
    name: builtins.str,
    primary: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    private_ip_address_allocation: builtins.str,
    subnet_id: builtins.str,
    private_ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4fd9014a56388bc5ed58ceb16615be67b3e6a6813000e46e0cb5ec1d7732b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe97b14a437a6de232e63e05f1b6a98669997948a599e892d575c47fdfb04ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b49f986d50734cb73684633c9754b857caa6e94750791356faf3c6ea74682ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997add75eba448e49fde239f605db23fc27c8d38ee79839aecfd19c57cecb03b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b67c3c0a31edc68afca6f21b623c58e6f666176edbdb708a36298fb5b280b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135979c5dde05bce480fa5cdfeb1e8896696310264a3b778c4d3b9adf8572422(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfigurationIpConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23956509891597efaca8596367223e09bc03d6e921e4daff6d139e5d9a0d1f3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee668fa2e662ff78e51319fe949f90636bebf8ad44e206bcd869fe383954c078(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804be6f8a0d50cdfd0a2ff18eef5e62ad54358d23b32785a1c77c271c970355f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33be3d8b994906c1f6666a801d1346ecc71cd5662c5a3c814fa422891f26d0e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17825cfe8550a1cbf40dc0e8f18873b9a3ea5d8a668fae0e2e81c18ca08c4661(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991d9c0ca307e1994e725cb0a9d9b52ba0d6dd7e5502ed59abd3421236407b5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6646611441a9b8d2a53f22f1305cca0c5cd7ecb3132bae15fc86d217ddb0baa6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayPrivateLinkConfigurationIpConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fafd5be04062edebbd2c0c23ba5922d0009e68b2342fc2ec89ed7f5e376d851(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ebc9e90076826569d462b021b4fa4d268e8d5a5daaf93892f9d06063da1a87(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1def671665106d0a378f57a879ef56159e81dd17f2b4419bdcf9e2d7ea0cad4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b80002dfecd780deef0785383df9b4b5b47ac3e9270d3f94fdf94e339ddd44f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85dc10ba1f71467e6a70dec24bda8d8912b7cf1236671ff36843508ac692cce2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73890eaf14013156d17451926c97d5bb9b3bee7c9451972b2b1f7d84966dad6d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayPrivateLinkConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cea9df0706af3e3048eef301a4ac992db4e4b6c56d3e505c26b8c3d0c951598(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f9a87ea7441675e44d505b4d65b3da5246e7316687a61bf2715b81605db2f3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayPrivateLinkConfigurationIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f005a60e0df004f4785cfd8a615627d8c2ca233343b28babe7e4ac23efcb958(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aca7d060816b3255144f4078f9c22e9163ac729946159326c5198af033a72d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayPrivateLinkConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc4b601cc073e15e0fd292572430a667cc8e63e5d04272aa7379c8496e86b96(
    *,
    interval: jsii.Number,
    name: builtins.str,
    path: builtins.str,
    protocol: builtins.str,
    timeout: jsii.Number,
    unhealthy_threshold: jsii.Number,
    host: typing.Optional[builtins.str] = None,
    match: typing.Optional[typing.Union[ApplicationGatewayProbeMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    minimum_servers: typing.Optional[jsii.Number] = None,
    pick_host_name_from_backend_http_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0980ad9449c049657a84a3c696eb2b277fd697815096c13f52a6b668d178a40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693ffd566cbe474eaf30a4e3e3927fe2fe3e4dab8bc698257f84daa483c19fbe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c4a9639ef5194bb782bda2d2a4f1265a14ac85430ff5ce5149b2b679f10a1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed81d613ff22c1ec5a23cce5d3636abc20371afbca6863097f33d9c4cded2484(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4817fcef37724fe05f5c147e8bd42e1f402dd15d14fd896a96d88372d9151f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e9ca98ffb7b737f6ee290923ee58b951657a82d040248c9062931ac4faffed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayProbe]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d98d0a77a223da60a34da6783b5fa876307ebf27340c953c893ddd253ddf28(
    *,
    status_code: typing.Sequence[builtins.str],
    body: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befaa13a0fab5a16822059510b838bd9e83bf9b52d7e5270e5dbab2cb6f9f10f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92b27b243cfaa1cb41b263388d586075f3f75f17d4bcdca6d06a1ae3efbdc6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d01d845d6453ec037a56200f8fc66cc2cb226f1162ed576c0cf406f9f96519(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f526c084274ca6383d427d291f72cb82773fbac0deecaa63781f6122cc130452(
    value: typing.Optional[ApplicationGatewayProbeMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fd2bf3b838a023797eb8816c8e01912d00bc029d4840831bd94ba8cdf19da7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18280dfe7ddfa4969414d16455dea46b6f793a69cc89f2f5d8e8a95269c93de1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d907b2aca5813556f60351ee8c04473e9a5266389563bf9fff415a3215a05c4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35d0ccec745c4857fe26912e8278f6b19112aca9a3d6f8a4a4740bd3b28dc40(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d341ea4f7a1de0347b5dd9e52670bca15374ca9808d170adc9a5c2bcad6c273(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84d139a225db7beb212025e47c3683759b021d5dafcbca8ce9c9f4a3b0c73d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1377368f319a3f3693035d4750162d37764170944ccbba2da543bea8c2abea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04421f2f0fc86ab9baf28ebe334dc55d855cbb7551a6f0bfd86821224accad87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba092d9255742c2950589f8db7c9c66bc135dcfcd967171b84aecfbecdbc487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d299e0ffd5fda0083520f6940423c4ae6f4e5008432509ef636e805c9410ae5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122bd15243902eba63d2c34af4b7939d0f1e52410af3b7fdb5aad6eee9a7b44d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0e95dbf96843a0e022d9208d41fc8311a7a702fb7805ca862668e1268da3de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayProbe]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efaad215a85925ab5ef0cb38081f5daf5be4bac57adb499665d5ac71eb5729b(
    *,
    name: builtins.str,
    redirect_type: builtins.str,
    include_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    target_listener_name: typing.Optional[builtins.str] = None,
    target_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b74e433ab980d0b1874a2aa51346ae042ee41c4d67b234960e90d7fb03ef4d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ba611cb5bde98b9e187b5648abacb1b383429c8f62d35bcd4f941133e280bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a830c6c46b81237173fef4f8b33ee361e3253a316f8f18f7baf059ab0dd800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59909b019b06887d7fab4ab98542a68880d27a7b3edfb817a6d0849b57daccfd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926569acc31440822af63d37334db5d1e74389149e3f9b5145e4b37422e8f56a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9452b2401df7b9eccb86d7803484fb3a8da481ce11a709e507a2c12738ba2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRedirectConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9cc4d67c37cfbfb2aa83f4811110914576d96726658e56e28ef3824594d867(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4549e561a0218bd3ee0a298a916dfd199aee883f810e1a795fd2d07bdb35a146(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14ede66756c46f44fcca671fd2b148d776bb1928c1c148fbcecae84010d30d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264c141b3d6f3d51ecb21c2c9003bc6a2f27cb0afb04d8305a6892d832efd38f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4979842dd8c4cf40360e5d6132252d544bcce73d8a46887ecefa224bfbca6c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4298f3fb49f3cb6ea0037b95eb1f170e8725c4064c0440404387afb83e7252e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ede044cee20df2d33e143d32ee6d43fa794307a4f72d1a6cebbfa69936e589a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640be759b1e6daa0e8290e598e7274352d76520ed0787c8720259192f30419f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRedirectConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8a623d873df6cb0e5e3eaeb9a1ba1c45cf2d3f2c557a5a3a54c1a799573abc(
    *,
    http_listener_name: builtins.str,
    name: builtins.str,
    rule_type: builtins.str,
    backend_address_pool_name: typing.Optional[builtins.str] = None,
    backend_http_settings_name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    redirect_configuration_name: typing.Optional[builtins.str] = None,
    rewrite_rule_set_name: typing.Optional[builtins.str] = None,
    url_path_map_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1555561371da84bc32f3c3b4735743086d9b4dcb168130670e2d35f0bd7067(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13bda5c08fad65ce0692813adebc3c079000c7f13962fe6f407364c7b2e3e3fc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f56dc840fb7ddee47f5797e67b037204db679c4933f395cbffa2c40f0d5ec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cd5e95e9bb473a869de5d60ca166d84523c09de4001a123b3bca4fa4c40333(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad537fee35044a7b190e5fc98d0623091aeea2fdbc97901133e0b00b354a913(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc65f93a528ab6cf7bd5db97c2441e08b45078c72bcb381e206c25c052cc286(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRequestRoutingRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2c7b7353b2fd401789ca3702686c3b71f286665870208aafbcd69c3e04fc47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6749a5beecb1c484e0632cb1371150f2ec2702f191d33d02a99a692be3e3aad4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24533e828a74ab36ddd9575140842a91967d2cbf3e342a897d678e2f3599dbb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c652aa62ae3cf7913d1e69ce0eb787093f063fcb343c105e2318794b4db9a9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01592b1d93447aa984b240b39e8f739646c99e81b7cce986098a0a3b58077ec3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49df255be86421d8935ff7c7c3623bcf2759cac4cf227600075c33a500284611(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe2436dcee7e710e9aafbb4f2e70e15aa01a4e3f32cf65fb8710c9dd4c8e583(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4111437fca4874554791dd9a06a9349fb37d3a59f9865cd65a9bd41dc65f7155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9935be74c38607b70ea3300f4b3de136266bd997b35bc3604f24c360d3836222(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af71631070286b0cdb37677aa38d98f8befa977eecc79baeac6a18055e73d959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df94d2921af9621cf5e6ecf6bfab6a804f5fd7b019752d554f594637d29835fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRequestRoutingRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e93603d4b0b53808969d3f24f519271829f0b3e5f106445f297a229481402c(
    *,
    name: builtins.str,
    rewrite_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f627fbb17b2e1cab5bdae10e2d623b8b340c1a289ced77db27544c09af92b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578df1f446649cff76c20e1538f51cd136f6c2e478f7c3a232918d8e568c5ddf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1252b2bcf713dc112c5dfe2c94ee20536a3ccdcd03ca352204643d6a824b2fa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6e07f535ee311ebda3983930780b9f66f42ccbbb2f737c5ac58d922e1528af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b9f7036eee184b6c470b6d2f053ad38580ba1fce827d25fb9fc477df981d19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aae324ddf1ec8d252fcae58364b6158241bece8a5c42d1a9375a5fe0931eec6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ae8cc613ea27f932ccef5bffb4eb6dfdfab1e063ccca4b325167bfb8cf70e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6bf1efc28026ea6db22223763f67c16b43bf48feab204b8a7a5173e2de28f4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef97ced4d33a5065d0d789db12095db9ab89e98213b26e394835647e9a3a3c3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f35930842de0c9e28378fc8bdd87e3be8ba076215312f6a3130e096b632b0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc78332f92ecc0df04914459a457d7b0b16c8ec75fbd50d218848620fe8088be(
    *,
    name: builtins.str,
    rule_sequence: jsii.Number,
    condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRuleCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_header_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url: typing.Optional[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRuleUrl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403c168f7b330cea50a9b9db99473b3368967d07f2c4ec0e913e5299e3e266af(
    *,
    pattern: builtins.str,
    variable: builtins.str,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7651394e69084dc3b1af977e6d4bfd124f35a366c52e5db8c0dc98a0e3123f50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6748a75ca09e539eda7d2f95e0f212fd270d8858543c445722bfe1261807ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2ee2b88076e1ef414efd7947ca0f0c796e523bed0cb9a96181058f8632b0e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09fc33773b63bd5468226a536a87cb2f652249a230d8a7ecb4b13a79420f614(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a9dd5a172dbcc080d85019c87e4d3bb89d9ecc8a4d9972de2213c4fa3586bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b1d7401307f0f3176494ea82bc68c28730ad35c2013cba60ccde585ea6b163(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02044c8dc42b30922ac022c16a18bea043247287c923131f790d59d1fbed203f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723c4cc80bf5f8c812aa326ac06f918d5382cfbcfc82cfe9c364b2cb9f538f29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f509e4ed4b369eccc410259298c9373a4167def82d9811baa446e3806d26b9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee868cb36a59146f10e938395048e4567bb85208d991d3b03089c807a533a03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d82a5f581a9a68236b3287d2cb281d15672e0a20d103f297b9ad3980ec3f0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26984563e2bfd151caff91740f0d198cdb4bc63e054e88796467424d3d04ba4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd42a7437d102e957bfd3e989805f2a75c28d42534a316663b3d2e8248910aef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec780c96eafb8ea92335dbc0b22dccef8593268ca300b3919bebf5cd3940e35a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8828d7c8df1ce83772e14984a25b285e9ecd36e0ad4a74a52f738870cdbe2431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e185b4481bfa0867172ee30d6257eacf861ed778b15e5e0c70f3be76ae6d89ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebea615d6ecfb11076ed41bfba9ca62eb26d120fe14c949b08e5ae1b2df2ce49(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f9b8824336c1c3a3f70381a18ca9b34867cbc4c526ee1bee47740a543d575c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6116ab2e981c4454852e78f76d1ff9d1049c4bd2d94b5a60e08faa51188b9934(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d134283562a7e938640b059f0d166653eda05dba7a6fecf374dcb88d04a2ccc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1ff56d3f019e4388ad23f8aa0433cec99951a386ead1f87ab2f7f2ee5c2b9b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab437aa1ea56833080821f6016808ffc7b5f1f953dd3c6498e5a8d4527bcb74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6a69160797acb27ec4dff559a577502c820966801487b707c11414a61563bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4919048af5cf07a55f1ff00dccc0f4ae11f93d118aadf83c6c4202143b38979a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec19c65cf5af9ad7c923dcc5793a068f1154f92cea04c962743bbd37263748cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f307075d0539f78381eeaad65bd4ab1064d11435c084915cbaef94b9730e02(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08ee82d9bde6634f70b4bfacd365ad62b8b1170dbf92b4992ddb5f215834231(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920099104ce9dfa349979486c3b5d250924708cdfaac35bbd2bc409b4dbc62ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9c5bc8ec6046916a23a0c72b8281636a3ef886ffbfa1b36c16071fe4731ca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c234a65ffc0e77c4e07dfc11fe970b941bf98894e645972ab0f5f1a744c704(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63feaa74cadff2a8dac9be3a1bd0612ea843b94456bb3195c9c2d7a599bbea1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4549d5bcc91f6faa706a0263372defb0e07c6cfe21925527b94650aa3898d1d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2725477f934364ee0bb39923bbec22741226f084c41d2a666fc9fef4a4554758(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4668eb8a586d2d30acfaa67943e3d78fb8426ce79f287cf29d76ad9350c1ef6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a84946c884941c7243580941e387a4cd9450d020f0cc8a5a66a6918906d7e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970f922c3f7e7d64a63b3aabde9653aed87a2c4aa689372cadab8d87f8662883(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleRequestHeaderConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb59694b2d4809fe6690311b3d45401d7ec4a340bfdec660285c17f15fd2c05(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969f78427c44c610a0c18bf917cd99c40358d4e723b8c19457496163e84fdf45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5fbbc936803af4c25bb114f0fb2c3eeac0be24d373c808aae549e7002a1e9c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de01333c375125bbc2097ffdcf1d09f902fad5bbedb97c463f6e12209d2df99f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54834328c36afcad7c756d4a4e59b68518f03e0eef1b2bbaad6900eb356a6f0a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082d90396a9ff4cfe88c56ea528ca8c2260f3fd6d767cc252c4f46f195ef99ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78294eaf744312f863bf5cb8960e7703ee6befe663ff1e4a61f0cc39ab4c6955(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c59138096e8a79804e54ba4c47f926e46457dcbb184ad0c4a3b123f5ed801dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8fb7b6b035b1ac9f2bc0926ec8b1698a8152fd574633374b7fe50cc7f386ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b576bd18eb9c5bd67ba70b9336c0b2a4ae326479db4fc387e4019176f85309b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c882acc884357447edcb2356b908f71a71c861567d6f9d96770d9f55e3cf1bc2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayRewriteRuleSetRewriteRuleResponseHeaderConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1cb7ab010869ba25ed7d8846f27e4f54253424a8c07c749769e09f7b49ca4b(
    *,
    components: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    query_string: typing.Optional[builtins.str] = None,
    reroute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f77dd3cb006127c60e9d988e1e79ecd65eac8011c094e78b7bbdcf566abbc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ba837a7acb6bb1a6b691f8f0e2d30ed12de2ffda8291f0acc5f7cf47501ed1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b897a9abf4eea457472778999deb6da308096dda1a95003ba55a6a17d34bb770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40969d104ff18925703098e841bece4a047c5133ae10911bd5f768493c384283(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c267f12da7f741af1a5ce411efa37099a58df7d08c426175a7a4e3988b2c095d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc12b5dae79860cc86451bd9d6fd2dfec68d9db8c26eb25e0d0f6236aded3d2c(
    value: typing.Optional[ApplicationGatewayRewriteRuleSetRewriteRuleUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebda84c61b3a52c067a899ef24c74d54270a4cc58c955017d9b2c4d98d7504b3(
    *,
    name: builtins.str,
    tier: builtins.str,
    capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7155a042d13a1ccca11d736a57d0819205e2f067b800cb4750324f1034ca67fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afd2bbe653aaa1bb6167f4f90ed7f289a6628b1a0e74d8b39b04fa3e157e933(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6c228afcb31b0fa00a9821deb77d070b6a7eaa89ed4127fca0ebad2d609301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d958a98040c851f55a99e89b4372933072e598350c703c51ee05e30126e597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e43ef307e63590e71429f1b1f2ba713a2ac5ab7417132f5d252a0c4c4016c35(
    value: typing.Optional[ApplicationGatewaySku],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1c4d6819bd00a3d15aa0819b49a10016aec4dfd0c0b6e2f3815a529a1c8c5e(
    *,
    name: builtins.str,
    data: typing.Optional[builtins.str] = None,
    key_vault_secret_id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102884559ddbcd6429de6a063a8af54559c8a8b062911ced57aca0f0a9fbd4b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac09cd79cd9d1ae1155aa995142b094ab195cf93a1c356c0227facfecc7f375c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b854f69ca946254bab0f278e950327a817f0d04be143a3729914305defe9bac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0247cafc5ecdf3ed7f26e07dca2476dc654187a21ec11989c9912b1c0467199(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382ad754f79380afb81bf4e0399789d24fc7872194bec82ae5fc17db9c26407f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f59c6028162951766b4b6918144d55c0887a4806a8125287c8a5b6c3fa57770(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewaySslCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae78be16bff9ede9874bdc999630ce0a4045fe5addc08e4bd1e5867708baa722(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab354965d7017a95dfae1753b58c7ab58c576727d17f6ca063dadbbb2b557869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800abe4f8be7074c06f4e6d6c6b881468207433bd9b9850e8be40dfb7175e163(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c8ce1d291e2a9e99ad6296dcfee23f29589ff8c4447e0d8d0b474cd766cbc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c74e4ddd50dce54d918e79bc73b2a975937966817c2ea51901012d20e91b2fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838bce3200a4da6e061fcfc759f7e917931fa3f5f56ea43eebb99dae13d42157(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewaySslCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d087d5be39410dc3919d40341b96b43874aa3dc35cf9633081191936b30711e(
    *,
    cipher_suites: typing.Optional[typing.Sequence[builtins.str]] = None,
    disabled_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    min_protocol_version: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b494a5d79f922a5bcf358c466b1a7cdd293d3deb3c88e1381a6629443cc3ff71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b2d5cd3b3ffd582b1d614980b22306d8d35a1be0eb339339152add267c9a91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4438cf598808111e3a19f4535ce599dc2f9842f2573e7e0a54df2ee652c36292(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8b6de7c74933f07e4e6287b4cc212ae5598af662a9bdbdf1481e989c9b0ea7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8399c9d767445c112c3788af2528bbacff6a8125454fcfd4f0e3ad260606b47e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6130f90c79fc0bc26a9e94e6d5a2dcb2a1522a92c10a2f622a0f11ef530c55b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe4e125ee51e45468dcb88cb403e0e631694205559f7b9a059031589483c8b5(
    value: typing.Optional[ApplicationGatewaySslPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e5f6b4ea4c73e0d9a176a0da86c9d9c8d2393ad679658d19a475a1c55b5ed6(
    *,
    name: builtins.str,
    ssl_policy: typing.Optional[typing.Union[ApplicationGatewaySslProfileSslPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_client_certificate_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    verify_client_certificate_revocation: typing.Optional[builtins.str] = None,
    verify_client_cert_issuer_dn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae6203e7a657ddd599e483b71f1deadf136ef322afb7b0e52ef3251eb6ec7b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548cd525e2eb70e5df59ff14753c794df1e1703d0db4f23b54951f2a9f062e47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add0d612781bd0cadda72ac421271a15e5b83ea7c3239ff7098dea02954cb8df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c29b7e57d896415579648b4ce4d224d298aed094658740bf7a39c6645082aac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6420e7058f64217430d75fbe1dc64b87c87a4528eb06392140bae09e5b0a1d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb50d5b1d42e2b48a27133c4cb5cf3353d3bb915d5e7d61be8e932911eb873d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewaySslProfile]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766dc201cf797b577959ce2093651ecac76793b91c6387ce6254c29b25e7a02f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1566322d13a054acae0826b5e8a698e9d62212f328aca7e7360a08ce43a0f71c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996f69e7d0dd0216a08bd1f47104a1085041ad7e73380bea5350db679895320e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69df7c12cd59816bbcb8c26f10faca91e5deaa1601b041fbbe3026cce7c1cdd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e8664d84420c989e43f283772abf02c20f68b3b03bd97c29b5e6d39ab0d4a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3588912e4c0cbb765921246ffd76dd7327e6629459584938c13f81ee01ca7645(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewaySslProfile]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2cdf3f24a829f952dcdb774cfe2a763d388b60675ea9c2262cf0df93180c30(
    *,
    cipher_suites: typing.Optional[typing.Sequence[builtins.str]] = None,
    disabled_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    min_protocol_version: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db82a3fcd33e127fda3f3d132b7c717c7f11324f1974e8c346dcb62c970d0494(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e28f507d816b35a2856138baceb1611d8dcce7431c5b6112df499a54738913d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b832104a891bfbf47ae21f964b756eb4b62cdc0cd076c6a03a792dba6e03f6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c984348d89dc1ce79001f49901fcfdcca3206b03a96bb13ec1a0c5525eaf0c22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eab35fbbf43f7737efce44a0c92cdd025709d32db3048c93076eb21808bbc09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2528bc823c37cec84e774b3e2f46c8c6c064624dfcfa79dc87e3c46441e6726f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b94830c3b4cb7e0e234d3c91ea9d332a12ddd2357d3a4b4b0cf1ad36fd5518(
    value: typing.Optional[ApplicationGatewaySslProfileSslPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b4c8c749f2ea506c397a33eb582e83dfb58db0720746e13f360076750142be(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc94f892cbcd846c91cbf2d0e29ba1bdd9950aeed7399449a531846b859117f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a43136e8ce07518d4f6efcc3e42c27f012310469f50d7b634c0c8b266e028d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6776159683b8a31317aa467e5b49907af4d940fa11addc794b5ed07d5899b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6525e2b414eeba28544045fa5e5c4f5f13dcaa86e3b637a6f38b75baee729902(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf121334ba044f079095746dbccbc1c049c625be0c1a7c2cbe094e248bda04c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efd01c8329a8bf697749a90cf9b90a7853c684952f49dba4cd989526d51c043(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b257997626dd239fd897f91e2a04881213d3fb82c98859392e722dbdf0f5b41(
    *,
    data: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d87d4571c553e60ba09db506ddf09b57f51e04745811d1243cce4b64465d317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedb78f9a860dea2b1cc2894f85213188a3b4b6d777cdc253a636afc99906994(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129d7c05dd4d8f0de5975f7e96c6c3d7f312cc37da8061cb328325a128c28d8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12daccedf1237fec2a17c10b6e50271e22e37cc5bd4be70f63c3320a2c60837d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25c3b0303060e055cee3b17460ddccb1e4a651e7c5d601f077f99ad10a61abd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c78f43604b0a58934a190765b1dc9f8c4b2d5a33a393fd4a8ef87aad91a980(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayTrustedClientCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14f6264406e49741d9614cb1a406d03dac3fe83cb868e6be64127fd96654bf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0d60b34328212b810d1d1c35b2b03e836750d2fef3f4b6e8e87fdb01ab5276(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fe4fcc3241d1faf605bb3fc1287035cc33a396a4d440fa321ab1752372b9d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b818e047e64abeed9d36919ba5aa3f673f703148c03b7f67dbdaf156e2fc02(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTrustedClientCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8985a3d01c984d29f2646c3ac56a15ffa0750a63b2ef9464454c2891fc43efd(
    *,
    name: builtins.str,
    data: typing.Optional[builtins.str] = None,
    key_vault_secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b279f4d10dda2a1fe90af8c8e78f990183f7d26c6ba30cd586cef845f28ccaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3343ff37998532a5ed4f22018b54c8615b274b7309f79f6086bcbc9ee23da7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c473c902734ef3f423dcfa190b461c523e8649f0faade5221c9f7e5ba3df3049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779ea20e91c26f4790ad9eb0230690292c015ea72961852a153bd6df50f4a1ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dd4ab637e48e32686d9360c08ef698ecb7f2d98628240a345956781e8f0fca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c697b8de32dcd34d9cd69939854a4e2bd3493890ab21ccca1a70c54c37288ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayTrustedRootCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cd6f2876dce4efa67e4f8602676a2536ed6c460809d93ef6ff0f6597bc6288(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92005415d80b82797225322072fc965a8646d5b71b6202815dc2327f9efe79ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757c61b45a034056d69eedf4963f3f019913cada038f1af77b1e1aa1e697adf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d52e40e1699d35c90eec811109767227dafed5eb253c89e11b7d09ea41c4f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27dc1f64667430b9e2214485a8bc69f957d2380d7c0d38dbc67174c13113ab49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayTrustedRootCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2052ff898c831ab7f8d0466a21cf0a0ae5e20ad0a97b9941219e3dd31242f922(
    *,
    name: builtins.str,
    path_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayUrlPathMapPathRule, typing.Dict[builtins.str, typing.Any]]]],
    default_backend_address_pool_name: typing.Optional[builtins.str] = None,
    default_backend_http_settings_name: typing.Optional[builtins.str] = None,
    default_redirect_configuration_name: typing.Optional[builtins.str] = None,
    default_rewrite_rule_set_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2b1a47fd5bb8918c2e7d83d8d4d950fb19ed737371b7320abf76492888876d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb5027b3725041d10083aaaaf3947243581ddd6f156c5f0460144c681ff6bab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85194969376798eb55c9baf10030d50d43febfc97608cf7d33c01af545f358f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7bc21897f9e0c2c1d24eb8044881555fb5df2453d68eced2b0c82dfd2ee0b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e5ce1817013e82a47c3bd2e3201a642374658bd86d0dd667280ce7381e0d22(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effe880be581b97f1d179b28d2069c3fb28db3ebac6e609e58c81d7de6a2708c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayUrlPathMap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aac315ddbef3c69acbd0b328d45b8bda4a06d16e8c2054fac69cb91cb12e8c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c065598070a809ae38a631974fa8257b3c11a864dd9ae7f995fc244a802918(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayUrlPathMapPathRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3824044fc9433b86dff201e87685f79b059bbcb779222c7e961f08fbf0318d72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906300a0409ac9d66b785d40e97bd584556f0e2fca05bb8272f952578f6256b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3513c9235e179a530fcbb9b9d69b1ff558fd45ab0bf0afaf5bb0aaa60ecac05f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d70ef0cf28258159a1bff253cf8f3afdb145578d0d9c46e3b6d84bef8bb93edb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164e5457d09bb84f36d2670512aa99c7afead6aabc96f7bbaacc3802fdb51edc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a134f9b8422eb15941692951c41305c3badb134a8225a72a2970602826d08ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayUrlPathMap]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b427fbef40482ced6598a230f08325787a80212d3846e5fb8e684ccbbd44258d(
    *,
    name: builtins.str,
    paths: typing.Sequence[builtins.str],
    backend_address_pool_name: typing.Optional[builtins.str] = None,
    backend_http_settings_name: typing.Optional[builtins.str] = None,
    firewall_policy_id: typing.Optional[builtins.str] = None,
    redirect_configuration_name: typing.Optional[builtins.str] = None,
    rewrite_rule_set_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd03c0fdeface211d6c9336cd3cfe58d0f37fb2cc82bd16b987069a90df0641e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c50c36d32b17f252e8212f9cf69eb8ddf27873bee2a85ccd5ed93e287d67da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25cd9b336a85137d3bae55bb1624d5ee0d8efb006d5cefb2a1fbc718222de1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4294587a9de64d8c4fcf4701a4095e10d59a2fd1206503e8170cb2d42f8a111(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667fe417f68560bfc1d94d1cd735b738b06fc224dcf4a1fed686d0b0df252df7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5200fa2b684ad83ae7466311511707e2940efeb1a59e53029ef31664e7e7bb26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayUrlPathMapPathRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478bde2ac3cdb1eacdda026028ef02e25576aa7a61271d84b4537238d5446362(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ecbd21cb5b886c1bbf9410e4a1267f97661ba4c8e7c5bcf7b9758f9779dc4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d650bcdd0317a173c8050775985410e7ff37c175e23b6885b0492c0faa8993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8375f8c286b87aa5d4a2576340102c09e78212c37e6c1ee9112a3f2e832139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112b810c7e0e5e449b32e62c1b8642d24b43a771c892107b2061c7fa16ef7c61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f65aa7aff07fde52d24d65449a941fe8a94dc0cd5b8288eb8358c076c806312(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d99322be1dd53b2bdebbe0fcb720e4082db33a8568a956e26462d06434843e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f80a3956135b6d175b6635f0c2f2b5278b414c1dcc468c03db95684b71c5351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047ecae8bbf8fa443c06fe2b2a2703af26c7d0077f0941a61e493cf8142411b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayUrlPathMapPathRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea565dca3bdf049c8577e0fdc9ac97bcb1231d96fa2133643955799d892bc5c(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    firewall_mode: builtins.str,
    rule_set_version: builtins.str,
    disabled_rule_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayWafConfigurationDisabledRuleGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayWafConfigurationExclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    file_upload_limit_mb: typing.Optional[jsii.Number] = None,
    max_request_body_size_kb: typing.Optional[jsii.Number] = None,
    request_body_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rule_set_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6d5b56a8ca7e5d30e4bfe477d91398f4602c93e0b31c163c1499a1ac159ae9(
    *,
    rule_group_name: builtins.str,
    rules: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03466e1903a50984f06113cab7b97f4e32f2e98f1cd43ea2b9b07d2c1c0bc3d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac07c7f6a5d23bdc346b209ce8bd52ce1836008861447010de122990fc75a89c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7f47f7e8277e266376ed050830b775126a224a375d9db465e750fdba1b97e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb77051e8226d9be7cf98d99cb5e17e9c6f2e9bc5091f281943b9e8d69599af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a71853bb343d5e3bed4e8d2e87096a9f5feba74283ef2b72f6d075002328125(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfb1e357ee12eb045439c94ecff4cddd5193e54f2bbfe1c89f6f777b9e72642(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationDisabledRuleGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755dc482e813b1a8a97f6fb29e4a58f72d9bad6d9caa09a4743fb75644bf9c75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afb99fc5ceb9221eec9a36b4d25efe4d29073c62dc9b5db01ec1917fce73c95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60868e9133b702e90388a7d6fcd4fb7950ab708748a9195f55e55c7d1640f12e(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c582591c70e6ec0a9768bbdb87fb89ed1dfb01fbb003045f320d5970912823b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayWafConfigurationDisabledRuleGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5516339317c98ce268f2b07fb4011495fb52426021c9da8ccdd0c30632b54a40(
    *,
    match_variable: builtins.str,
    selector: typing.Optional[builtins.str] = None,
    selector_match_operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca74eec5ed49495b483159d9b447b42c7789df3ca44b1e547eaf7c8d315360a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a9654d168cbc5f65536423655ddc3075448a317b6dc71c4b02f8f22f833532(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2289d4569064c36af4a3c8cef84548a0d61a8ee2113e5e84971644616ee01f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4730f3eb6b8601960f89e6c5085862c44a98860e95354d45c31236c73b6b0991(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e2116936f53ca582abe6917e56b469dcc9b65039f464d0e68b1dac3679eedb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13b36f6722596ab1614368c26dd331285a17be5712cea03cc8d633cd2dffe4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApplicationGatewayWafConfigurationExclusion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e630616406e7bbd888f5f8c82ec4521b0478c30923619cfc72df676e6f949d8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e3809a2938b1d70b3ae81fd053a67ebf5e8eb3e88ebf92695d0ab31cd38600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a3705d4dcae37e3c8458802c7e50e0517ad9ffa66fad5cff15a08cef65b721(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f9a82f8ee25e31f3888ca765e8b77d0e2877ff2f026e8817fd333f142db722(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b294b6cc4899029c804678cab2aaf5c48dd4252d5a3f54f1749391fd4f2b39(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApplicationGatewayWafConfigurationExclusion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9f02e5f0a63910081b252c69b470b3a8d6def8b11053e37f4713caabb4a00a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a134314d776ec48b47aeaea30f6595ed41facf9a6ea8f09891dcd25eea34755c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayWafConfigurationDisabledRuleGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29deabb4ba2df8ef2f7e6780a8b8baf9904175ddb04f7efe4ef19ca6a3ac9bc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApplicationGatewayWafConfigurationExclusion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a879f5dac1f7927cb71759602ac36eb4756ad366f598d39903a0e70ac59dea25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6897b3e3763c3f5cabb2d108282ae35aacc450dafa177c5d21364089921a6b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5289d7323d4773f99a3b5c27f938e18f22f8afc8c10da579480632114af51e0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec11a81d570cda52ef7ad878478bd207a5e41c18adde6c3d2a371567296ab42d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a786029f7c0ff487ebf2695f6f10606103e47ad14e5091e691fb51806f3c242(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36071c41bc0ac653aedc8075fb8b669cfc57f62b4162f00a85ef047ec2373414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef56d1b5bd393cee5a46e4469744487490b943fc791d6202b90cc474445bc3fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d84c4961fcfd6180af753ac8d9acb4b17210688b06cf619bdb1d2f32edc881(
    value: typing.Optional[ApplicationGatewayWafConfiguration],
) -> None:
    """Type checking stubs"""
    pass
