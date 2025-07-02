r'''
# `azurerm_cdn_frontdoor_rule`

Refer to the Terraform Registry for docs: [`azurerm_cdn_frontdoor_rule`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule).
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


class CdnFrontdoorRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule azurerm_cdn_frontdoor_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        actions: typing.Union["CdnFrontdoorRuleActions", typing.Dict[builtins.str, typing.Any]],
        cdn_frontdoor_rule_set_id: builtins.str,
        name: builtins.str,
        order: jsii.Number,
        behavior_on_match: typing.Optional[builtins.str] = None,
        conditions: typing.Optional[typing.Union["CdnFrontdoorRuleConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CdnFrontdoorRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule azurerm_cdn_frontdoor_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#actions CdnFrontdoorRule#actions}
        :param cdn_frontdoor_rule_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cdn_frontdoor_rule_set_id CdnFrontdoorRule#cdn_frontdoor_rule_set_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#name CdnFrontdoorRule#name}.
        :param order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#order CdnFrontdoorRule#order}.
        :param behavior_on_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#behavior_on_match CdnFrontdoorRule#behavior_on_match}.
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#conditions CdnFrontdoorRule#conditions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#id CdnFrontdoorRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#timeouts CdnFrontdoorRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2268aa325ff2d82b50d992b41253454ffe96c9762c180f3275fef650dd5cffd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CdnFrontdoorRuleConfig(
            actions=actions,
            cdn_frontdoor_rule_set_id=cdn_frontdoor_rule_set_id,
            name=name,
            order=order,
            behavior_on_match=behavior_on_match,
            conditions=conditions,
            id=id,
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
        '''Generates CDKTF code for importing a CdnFrontdoorRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CdnFrontdoorRule to import.
        :param import_from_id: The id of the existing CdnFrontdoorRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CdnFrontdoorRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5b53a33baa223fdc021eb286aa0dff64d1c7628c61a228e53f8d899cef51e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        request_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleActionsRequestHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleActionsResponseHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        route_configuration_override_action: typing.Optional[typing.Union["CdnFrontdoorRuleActionsRouteConfigurationOverrideAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_redirect_action: typing.Optional[typing.Union["CdnFrontdoorRuleActionsUrlRedirectAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite_action: typing.Optional[typing.Union["CdnFrontdoorRuleActionsUrlRewriteAction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param request_header_action: request_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_header_action CdnFrontdoorRule#request_header_action}
        :param response_header_action: response_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#response_header_action CdnFrontdoorRule#response_header_action}
        :param route_configuration_override_action: route_configuration_override_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#route_configuration_override_action CdnFrontdoorRule#route_configuration_override_action}
        :param url_redirect_action: url_redirect_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_redirect_action CdnFrontdoorRule#url_redirect_action}
        :param url_rewrite_action: url_rewrite_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_rewrite_action CdnFrontdoorRule#url_rewrite_action}
        '''
        value = CdnFrontdoorRuleActions(
            request_header_action=request_header_action,
            response_header_action=response_header_action,
            route_configuration_override_action=route_configuration_override_action,
            url_redirect_action=url_redirect_action,
            url_rewrite_action=url_rewrite_action,
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        *,
        client_port_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsClientPortCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cookies_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsCookiesCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host_name_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsHostNameCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_version_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsHttpVersionCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_device_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsIsDeviceCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_args_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsPostArgsCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_string_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsQueryStringCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        remote_address_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRemoteAddressCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_body_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestBodyCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestHeaderCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_method_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestMethodCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_scheme_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestSchemeCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_uri_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestUriCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        server_port_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsServerPortCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        socket_address_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsSocketAddressCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssl_protocol_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsSslProtocolCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_file_extension_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsUrlFileExtensionCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_filename_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsUrlFilenameCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_path_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsUrlPathCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param client_port_condition: client_port_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#client_port_condition CdnFrontdoorRule#client_port_condition}
        :param cookies_condition: cookies_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cookies_condition CdnFrontdoorRule#cookies_condition}
        :param host_name_condition: host_name_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#host_name_condition CdnFrontdoorRule#host_name_condition}
        :param http_version_condition: http_version_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#http_version_condition CdnFrontdoorRule#http_version_condition}
        :param is_device_condition: is_device_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#is_device_condition CdnFrontdoorRule#is_device_condition}
        :param post_args_condition: post_args_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#post_args_condition CdnFrontdoorRule#post_args_condition}
        :param query_string_condition: query_string_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string_condition CdnFrontdoorRule#query_string_condition}
        :param remote_address_condition: remote_address_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#remote_address_condition CdnFrontdoorRule#remote_address_condition}
        :param request_body_condition: request_body_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_body_condition CdnFrontdoorRule#request_body_condition}
        :param request_header_condition: request_header_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_header_condition CdnFrontdoorRule#request_header_condition}
        :param request_method_condition: request_method_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_method_condition CdnFrontdoorRule#request_method_condition}
        :param request_scheme_condition: request_scheme_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_scheme_condition CdnFrontdoorRule#request_scheme_condition}
        :param request_uri_condition: request_uri_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_uri_condition CdnFrontdoorRule#request_uri_condition}
        :param server_port_condition: server_port_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#server_port_condition CdnFrontdoorRule#server_port_condition}
        :param socket_address_condition: socket_address_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#socket_address_condition CdnFrontdoorRule#socket_address_condition}
        :param ssl_protocol_condition: ssl_protocol_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#ssl_protocol_condition CdnFrontdoorRule#ssl_protocol_condition}
        :param url_file_extension_condition: url_file_extension_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_file_extension_condition CdnFrontdoorRule#url_file_extension_condition}
        :param url_filename_condition: url_filename_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_filename_condition CdnFrontdoorRule#url_filename_condition}
        :param url_path_condition: url_path_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_path_condition CdnFrontdoorRule#url_path_condition}
        '''
        value = CdnFrontdoorRuleConditions(
            client_port_condition=client_port_condition,
            cookies_condition=cookies_condition,
            host_name_condition=host_name_condition,
            http_version_condition=http_version_condition,
            is_device_condition=is_device_condition,
            post_args_condition=post_args_condition,
            query_string_condition=query_string_condition,
            remote_address_condition=remote_address_condition,
            request_body_condition=request_body_condition,
            request_header_condition=request_header_condition,
            request_method_condition=request_method_condition,
            request_scheme_condition=request_scheme_condition,
            request_uri_condition=request_uri_condition,
            server_port_condition=server_port_condition,
            socket_address_condition=socket_address_condition,
            ssl_protocol_condition=ssl_protocol_condition,
            url_file_extension_condition=url_file_extension_condition,
            url_filename_condition=url_filename_condition,
            url_path_condition=url_path_condition,
        )

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#create CdnFrontdoorRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#delete CdnFrontdoorRule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#read CdnFrontdoorRule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#update CdnFrontdoorRule#update}.
        '''
        value = CdnFrontdoorRuleTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBehaviorOnMatch")
    def reset_behavior_on_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBehaviorOnMatch", []))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="actions")
    def actions(self) -> "CdnFrontdoorRuleActionsOutputReference":
        return typing.cast("CdnFrontdoorRuleActionsOutputReference", jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorRuleSetName")
    def cdn_frontdoor_rule_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnFrontdoorRuleSetName"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "CdnFrontdoorRuleConditionsOutputReference":
        return typing.cast("CdnFrontdoorRuleConditionsOutputReference", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CdnFrontdoorRuleTimeoutsOutputReference":
        return typing.cast("CdnFrontdoorRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional["CdnFrontdoorRuleActions"]:
        return typing.cast(typing.Optional["CdnFrontdoorRuleActions"], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="behaviorOnMatchInput")
    def behavior_on_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorOnMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorRuleSetIdInput")
    def cdn_frontdoor_rule_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnFrontdoorRuleSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(self) -> typing.Optional["CdnFrontdoorRuleConditions"]:
        return typing.cast(typing.Optional["CdnFrontdoorRuleConditions"], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CdnFrontdoorRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CdnFrontdoorRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="behaviorOnMatch")
    def behavior_on_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behaviorOnMatch"))

    @behavior_on_match.setter
    def behavior_on_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1609b117431c30de3134cd2c0cf541dc53a070fd2ecfc193746dcbae89446e57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behaviorOnMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorRuleSetId")
    def cdn_frontdoor_rule_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnFrontdoorRuleSetId"))

    @cdn_frontdoor_rule_set_id.setter
    def cdn_frontdoor_rule_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e14accd8e89951d486e0cbaa3beffb2ce1d0aad4484f684c6f8ba4d8c23c749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorRuleSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cdad9f5c828b85dacc1b064d299b567d1e5eb8faeccc7d8e1294fb201fbe7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5063eb378353b11cfceb62c1882f42deafba16829b082ed64534dd1978ee4eac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "order"))

    @order.setter
    def order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__571f55b54e60245f4fc1c8f7d542760bfcfb472d6574e1b52e405b436de405b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "request_header_action": "requestHeaderAction",
        "response_header_action": "responseHeaderAction",
        "route_configuration_override_action": "routeConfigurationOverrideAction",
        "url_redirect_action": "urlRedirectAction",
        "url_rewrite_action": "urlRewriteAction",
    },
)
class CdnFrontdoorRuleActions:
    def __init__(
        self,
        *,
        request_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleActionsRequestHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleActionsResponseHeaderAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        route_configuration_override_action: typing.Optional[typing.Union["CdnFrontdoorRuleActionsRouteConfigurationOverrideAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_redirect_action: typing.Optional[typing.Union["CdnFrontdoorRuleActionsUrlRedirectAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite_action: typing.Optional[typing.Union["CdnFrontdoorRuleActionsUrlRewriteAction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param request_header_action: request_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_header_action CdnFrontdoorRule#request_header_action}
        :param response_header_action: response_header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#response_header_action CdnFrontdoorRule#response_header_action}
        :param route_configuration_override_action: route_configuration_override_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#route_configuration_override_action CdnFrontdoorRule#route_configuration_override_action}
        :param url_redirect_action: url_redirect_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_redirect_action CdnFrontdoorRule#url_redirect_action}
        :param url_rewrite_action: url_rewrite_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_rewrite_action CdnFrontdoorRule#url_rewrite_action}
        '''
        if isinstance(route_configuration_override_action, dict):
            route_configuration_override_action = CdnFrontdoorRuleActionsRouteConfigurationOverrideAction(**route_configuration_override_action)
        if isinstance(url_redirect_action, dict):
            url_redirect_action = CdnFrontdoorRuleActionsUrlRedirectAction(**url_redirect_action)
        if isinstance(url_rewrite_action, dict):
            url_rewrite_action = CdnFrontdoorRuleActionsUrlRewriteAction(**url_rewrite_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e02a16d19f77978fee90a665cec94560e7c1d6eae0ab5660dbc1ba276d9ebb)
            check_type(argname="argument request_header_action", value=request_header_action, expected_type=type_hints["request_header_action"])
            check_type(argname="argument response_header_action", value=response_header_action, expected_type=type_hints["response_header_action"])
            check_type(argname="argument route_configuration_override_action", value=route_configuration_override_action, expected_type=type_hints["route_configuration_override_action"])
            check_type(argname="argument url_redirect_action", value=url_redirect_action, expected_type=type_hints["url_redirect_action"])
            check_type(argname="argument url_rewrite_action", value=url_rewrite_action, expected_type=type_hints["url_rewrite_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if request_header_action is not None:
            self._values["request_header_action"] = request_header_action
        if response_header_action is not None:
            self._values["response_header_action"] = response_header_action
        if route_configuration_override_action is not None:
            self._values["route_configuration_override_action"] = route_configuration_override_action
        if url_redirect_action is not None:
            self._values["url_redirect_action"] = url_redirect_action
        if url_rewrite_action is not None:
            self._values["url_rewrite_action"] = url_rewrite_action

    @builtins.property
    def request_header_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleActionsRequestHeaderAction"]]]:
        '''request_header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_header_action CdnFrontdoorRule#request_header_action}
        '''
        result = self._values.get("request_header_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleActionsRequestHeaderAction"]]], result)

    @builtins.property
    def response_header_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleActionsResponseHeaderAction"]]]:
        '''response_header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#response_header_action CdnFrontdoorRule#response_header_action}
        '''
        result = self._values.get("response_header_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleActionsResponseHeaderAction"]]], result)

    @builtins.property
    def route_configuration_override_action(
        self,
    ) -> typing.Optional["CdnFrontdoorRuleActionsRouteConfigurationOverrideAction"]:
        '''route_configuration_override_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#route_configuration_override_action CdnFrontdoorRule#route_configuration_override_action}
        '''
        result = self._values.get("route_configuration_override_action")
        return typing.cast(typing.Optional["CdnFrontdoorRuleActionsRouteConfigurationOverrideAction"], result)

    @builtins.property
    def url_redirect_action(
        self,
    ) -> typing.Optional["CdnFrontdoorRuleActionsUrlRedirectAction"]:
        '''url_redirect_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_redirect_action CdnFrontdoorRule#url_redirect_action}
        '''
        result = self._values.get("url_redirect_action")
        return typing.cast(typing.Optional["CdnFrontdoorRuleActionsUrlRedirectAction"], result)

    @builtins.property
    def url_rewrite_action(
        self,
    ) -> typing.Optional["CdnFrontdoorRuleActionsUrlRewriteAction"]:
        '''url_rewrite_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_rewrite_action CdnFrontdoorRule#url_rewrite_action}
        '''
        result = self._values.get("url_rewrite_action")
        return typing.cast(typing.Optional["CdnFrontdoorRuleActionsUrlRewriteAction"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e961a4e5e595ca7460e869428c2fcb8110b4bc907bfc35429fa5845e2056869)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeaderAction")
    def put_request_header_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleActionsRequestHeaderAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432ab9fb92d94740e93bbab862ee0fc611638275180fd7b2dae2d27182943c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaderAction", [value]))

    @jsii.member(jsii_name="putResponseHeaderAction")
    def put_response_header_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleActionsResponseHeaderAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605dee65c7fa4b004111f5bc229593ec3e0cb5accfbd6678b0f26714615b2d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResponseHeaderAction", [value]))

    @jsii.member(jsii_name="putRouteConfigurationOverrideAction")
    def put_route_configuration_override_action(
        self,
        *,
        cache_behavior: typing.Optional[builtins.str] = None,
        cache_duration: typing.Optional[builtins.str] = None,
        cdn_frontdoor_origin_group_id: typing.Optional[builtins.str] = None,
        compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarding_protocol: typing.Optional[builtins.str] = None,
        query_string_caching_behavior: typing.Optional[builtins.str] = None,
        query_string_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cache_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cache_behavior CdnFrontdoorRule#cache_behavior}.
        :param cache_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cache_duration CdnFrontdoorRule#cache_duration}.
        :param cdn_frontdoor_origin_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cdn_frontdoor_origin_group_id CdnFrontdoorRule#cdn_frontdoor_origin_group_id}.
        :param compression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#compression_enabled CdnFrontdoorRule#compression_enabled}.
        :param forwarding_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#forwarding_protocol CdnFrontdoorRule#forwarding_protocol}.
        :param query_string_caching_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string_caching_behavior CdnFrontdoorRule#query_string_caching_behavior}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string_parameters CdnFrontdoorRule#query_string_parameters}.
        '''
        value = CdnFrontdoorRuleActionsRouteConfigurationOverrideAction(
            cache_behavior=cache_behavior,
            cache_duration=cache_duration,
            cdn_frontdoor_origin_group_id=cdn_frontdoor_origin_group_id,
            compression_enabled=compression_enabled,
            forwarding_protocol=forwarding_protocol,
            query_string_caching_behavior=query_string_caching_behavior,
            query_string_parameters=query_string_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putRouteConfigurationOverrideAction", [value]))

    @jsii.member(jsii_name="putUrlRedirectAction")
    def put_url_redirect_action(
        self,
        *,
        destination_hostname: builtins.str,
        redirect_type: builtins.str,
        destination_fragment: typing.Optional[builtins.str] = None,
        destination_path: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
        redirect_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination_hostname CdnFrontdoorRule#destination_hostname}.
        :param redirect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#redirect_type CdnFrontdoorRule#redirect_type}.
        :param destination_fragment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination_fragment CdnFrontdoorRule#destination_fragment}.
        :param destination_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination_path CdnFrontdoorRule#destination_path}.
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string CdnFrontdoorRule#query_string}.
        :param redirect_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#redirect_protocol CdnFrontdoorRule#redirect_protocol}.
        '''
        value = CdnFrontdoorRuleActionsUrlRedirectAction(
            destination_hostname=destination_hostname,
            redirect_type=redirect_type,
            destination_fragment=destination_fragment,
            destination_path=destination_path,
            query_string=query_string,
            redirect_protocol=redirect_protocol,
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
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination CdnFrontdoorRule#destination}.
        :param source_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#source_pattern CdnFrontdoorRule#source_pattern}.
        :param preserve_unmatched_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#preserve_unmatched_path CdnFrontdoorRule#preserve_unmatched_path}.
        '''
        value = CdnFrontdoorRuleActionsUrlRewriteAction(
            destination=destination,
            source_pattern=source_pattern,
            preserve_unmatched_path=preserve_unmatched_path,
        )

        return typing.cast(None, jsii.invoke(self, "putUrlRewriteAction", [value]))

    @jsii.member(jsii_name="resetRequestHeaderAction")
    def reset_request_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaderAction", []))

    @jsii.member(jsii_name="resetResponseHeaderAction")
    def reset_response_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeaderAction", []))

    @jsii.member(jsii_name="resetRouteConfigurationOverrideAction")
    def reset_route_configuration_override_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteConfigurationOverrideAction", []))

    @jsii.member(jsii_name="resetUrlRedirectAction")
    def reset_url_redirect_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRedirectAction", []))

    @jsii.member(jsii_name="resetUrlRewriteAction")
    def reset_url_rewrite_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRewriteAction", []))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderAction")
    def request_header_action(self) -> "CdnFrontdoorRuleActionsRequestHeaderActionList":
        return typing.cast("CdnFrontdoorRuleActionsRequestHeaderActionList", jsii.get(self, "requestHeaderAction"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderAction")
    def response_header_action(
        self,
    ) -> "CdnFrontdoorRuleActionsResponseHeaderActionList":
        return typing.cast("CdnFrontdoorRuleActionsResponseHeaderActionList", jsii.get(self, "responseHeaderAction"))

    @builtins.property
    @jsii.member(jsii_name="routeConfigurationOverrideAction")
    def route_configuration_override_action(
        self,
    ) -> "CdnFrontdoorRuleActionsRouteConfigurationOverrideActionOutputReference":
        return typing.cast("CdnFrontdoorRuleActionsRouteConfigurationOverrideActionOutputReference", jsii.get(self, "routeConfigurationOverrideAction"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirectAction")
    def url_redirect_action(
        self,
    ) -> "CdnFrontdoorRuleActionsUrlRedirectActionOutputReference":
        return typing.cast("CdnFrontdoorRuleActionsUrlRedirectActionOutputReference", jsii.get(self, "urlRedirectAction"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteAction")
    def url_rewrite_action(
        self,
    ) -> "CdnFrontdoorRuleActionsUrlRewriteActionOutputReference":
        return typing.cast("CdnFrontdoorRuleActionsUrlRewriteActionOutputReference", jsii.get(self, "urlRewriteAction"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderActionInput")
    def request_header_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleActionsRequestHeaderAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleActionsRequestHeaderAction"]]], jsii.get(self, "requestHeaderActionInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderActionInput")
    def response_header_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleActionsResponseHeaderAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleActionsResponseHeaderAction"]]], jsii.get(self, "responseHeaderActionInput"))

    @builtins.property
    @jsii.member(jsii_name="routeConfigurationOverrideActionInput")
    def route_configuration_override_action_input(
        self,
    ) -> typing.Optional["CdnFrontdoorRuleActionsRouteConfigurationOverrideAction"]:
        return typing.cast(typing.Optional["CdnFrontdoorRuleActionsRouteConfigurationOverrideAction"], jsii.get(self, "routeConfigurationOverrideActionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirectActionInput")
    def url_redirect_action_input(
        self,
    ) -> typing.Optional["CdnFrontdoorRuleActionsUrlRedirectAction"]:
        return typing.cast(typing.Optional["CdnFrontdoorRuleActionsUrlRedirectAction"], jsii.get(self, "urlRedirectActionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteActionInput")
    def url_rewrite_action_input(
        self,
    ) -> typing.Optional["CdnFrontdoorRuleActionsUrlRewriteAction"]:
        return typing.cast(typing.Optional["CdnFrontdoorRuleActionsUrlRewriteAction"], jsii.get(self, "urlRewriteActionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CdnFrontdoorRuleActions]:
        return typing.cast(typing.Optional[CdnFrontdoorRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CdnFrontdoorRuleActions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8523ee5daad37abf47180dc32824a53ad470f732642d3d871857de16821d49e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsRequestHeaderAction",
    jsii_struct_bases=[],
    name_mapping={
        "header_action": "headerAction",
        "header_name": "headerName",
        "value": "value",
    },
)
class CdnFrontdoorRuleActionsRequestHeaderAction:
    def __init__(
        self,
        *,
        header_action: builtins.str,
        header_name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_action CdnFrontdoorRule#header_action}.
        :param header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_name CdnFrontdoorRule#header_name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#value CdnFrontdoorRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0732cb25f89b7e163f3d45f4ce5400f00f8377293314348b682878135439ef2b)
            check_type(argname="argument header_action", value=header_action, expected_type=type_hints["header_action"])
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_action": header_action,
            "header_name": header_name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def header_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_action CdnFrontdoorRule#header_action}.'''
        result = self._values.get("header_action")
        assert result is not None, "Required property 'header_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_name CdnFrontdoorRule#header_name}.'''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#value CdnFrontdoorRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleActionsRequestHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleActionsRequestHeaderActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsRequestHeaderActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__122fa70802e93870e117a5d4443bca5673763b39376e6097e3a14ba89c4a3e52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleActionsRequestHeaderActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb7b951eef5135e02c86564cb4338c002e2c73b28c6926afce3bbc0c0c927b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleActionsRequestHeaderActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2bda23502605075ac075180d32c04b7c52c7b91ca3f75518a608adfd5b0144)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d88620130a32c1aecb3e77c2832667cc8864019e2d385d5f26fc971abf25d500)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c8eb68a859a96766bc6a7359d335e3e8a5f5b8a801ea3653a02dc9ecf4484c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleActionsRequestHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleActionsRequestHeaderAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleActionsRequestHeaderAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bd7954e01c6a429ec147b1711e21aaa5d86efad7d2db105100f83038e102ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleActionsRequestHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsRequestHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__986b57257ce32ed1aa450db912c6ae84739bf0f769fe67be22943106137f620f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="headerActionInput")
    def header_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="headerAction")
    def header_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerAction"))

    @header_action.setter
    def header_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c83b391b8b0656cd52f4276551f1a7d1d2658249b9b7368935c2361ba4695cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b1568febb44cbcba9b46a78c597fed40bb891e75ee335226a8a2794931a53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f1a73a73ed6c95b248bdab39cc7629a24f2f6ff077e08d1194027e286a2b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleActionsRequestHeaderAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleActionsRequestHeaderAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleActionsRequestHeaderAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc51ec55ddfbe567e764fed765b9a3e4bddeee91d44248189987bf1baec5af35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsResponseHeaderAction",
    jsii_struct_bases=[],
    name_mapping={
        "header_action": "headerAction",
        "header_name": "headerName",
        "value": "value",
    },
)
class CdnFrontdoorRuleActionsResponseHeaderAction:
    def __init__(
        self,
        *,
        header_action: builtins.str,
        header_name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_action CdnFrontdoorRule#header_action}.
        :param header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_name CdnFrontdoorRule#header_name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#value CdnFrontdoorRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ad25c76ecfd49128dfe0aafe7b46b8e06dc7017f10fcdc22162feeb6fba1ff)
            check_type(argname="argument header_action", value=header_action, expected_type=type_hints["header_action"])
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_action": header_action,
            "header_name": header_name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def header_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_action CdnFrontdoorRule#header_action}.'''
        result = self._values.get("header_action")
        assert result is not None, "Required property 'header_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_name CdnFrontdoorRule#header_name}.'''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#value CdnFrontdoorRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleActionsResponseHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleActionsResponseHeaderActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsResponseHeaderActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__074452e35b096e9bd0be4916ca1ab15c1c27f9297f4963908baab9bb862f6048)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleActionsResponseHeaderActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28df99dd68f6a8b49e3a2f08d8c7aa07dffdd929ea999940a6fed6ad37447ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleActionsResponseHeaderActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c513fbb26e9ef63d8059f32148600a552cf1385b3f8fabf3691133f029367a00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da90663ba9f3b702c2849b70ebb63faf83320307b3da630e19a2d646f774ed70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8110889c5b72eafd43e2dafab7b0b00c730e5dd383e5e38dfae76a72ea2d8bb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleActionsResponseHeaderAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleActionsResponseHeaderAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleActionsResponseHeaderAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2cd5c03aff56ab7bd216e9535e8e1d2e1744aa5ce51f47cf4ed9f02b2356381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleActionsResponseHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsResponseHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07f4a60bcad46a46e54a3d8d519bb9349023a08c261d69acf388e3c82f2a13e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="headerActionInput")
    def header_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="headerAction")
    def header_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerAction"))

    @header_action.setter
    def header_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fbe88e09bedfc3ffd8832a84d2c54ed77d18c71c0a1978f8fb5393eb1c0674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d447c5a29975cbd2a7b6235060adf96a22c698149dae5e67d9b07a62c139c3d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de1b0b60cb8674abe9b7b9e511fbb3b3f67db624d048a888d5df60f324f96b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleActionsResponseHeaderAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleActionsResponseHeaderAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleActionsResponseHeaderAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499446ab28869fb7015ee852fb9b7fd4afad65da05c1c1301600efa78ee070d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsRouteConfigurationOverrideAction",
    jsii_struct_bases=[],
    name_mapping={
        "cache_behavior": "cacheBehavior",
        "cache_duration": "cacheDuration",
        "cdn_frontdoor_origin_group_id": "cdnFrontdoorOriginGroupId",
        "compression_enabled": "compressionEnabled",
        "forwarding_protocol": "forwardingProtocol",
        "query_string_caching_behavior": "queryStringCachingBehavior",
        "query_string_parameters": "queryStringParameters",
    },
)
class CdnFrontdoorRuleActionsRouteConfigurationOverrideAction:
    def __init__(
        self,
        *,
        cache_behavior: typing.Optional[builtins.str] = None,
        cache_duration: typing.Optional[builtins.str] = None,
        cdn_frontdoor_origin_group_id: typing.Optional[builtins.str] = None,
        compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarding_protocol: typing.Optional[builtins.str] = None,
        query_string_caching_behavior: typing.Optional[builtins.str] = None,
        query_string_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cache_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cache_behavior CdnFrontdoorRule#cache_behavior}.
        :param cache_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cache_duration CdnFrontdoorRule#cache_duration}.
        :param cdn_frontdoor_origin_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cdn_frontdoor_origin_group_id CdnFrontdoorRule#cdn_frontdoor_origin_group_id}.
        :param compression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#compression_enabled CdnFrontdoorRule#compression_enabled}.
        :param forwarding_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#forwarding_protocol CdnFrontdoorRule#forwarding_protocol}.
        :param query_string_caching_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string_caching_behavior CdnFrontdoorRule#query_string_caching_behavior}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string_parameters CdnFrontdoorRule#query_string_parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bff1a4d8ab71cb7be41e9d6f3ae1b1cb89fd50c1340ebfeaa33c659f8acdc86)
            check_type(argname="argument cache_behavior", value=cache_behavior, expected_type=type_hints["cache_behavior"])
            check_type(argname="argument cache_duration", value=cache_duration, expected_type=type_hints["cache_duration"])
            check_type(argname="argument cdn_frontdoor_origin_group_id", value=cdn_frontdoor_origin_group_id, expected_type=type_hints["cdn_frontdoor_origin_group_id"])
            check_type(argname="argument compression_enabled", value=compression_enabled, expected_type=type_hints["compression_enabled"])
            check_type(argname="argument forwarding_protocol", value=forwarding_protocol, expected_type=type_hints["forwarding_protocol"])
            check_type(argname="argument query_string_caching_behavior", value=query_string_caching_behavior, expected_type=type_hints["query_string_caching_behavior"])
            check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_behavior is not None:
            self._values["cache_behavior"] = cache_behavior
        if cache_duration is not None:
            self._values["cache_duration"] = cache_duration
        if cdn_frontdoor_origin_group_id is not None:
            self._values["cdn_frontdoor_origin_group_id"] = cdn_frontdoor_origin_group_id
        if compression_enabled is not None:
            self._values["compression_enabled"] = compression_enabled
        if forwarding_protocol is not None:
            self._values["forwarding_protocol"] = forwarding_protocol
        if query_string_caching_behavior is not None:
            self._values["query_string_caching_behavior"] = query_string_caching_behavior
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters

    @builtins.property
    def cache_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cache_behavior CdnFrontdoorRule#cache_behavior}.'''
        result = self._values.get("cache_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cache_duration CdnFrontdoorRule#cache_duration}.'''
        result = self._values.get("cache_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdn_frontdoor_origin_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cdn_frontdoor_origin_group_id CdnFrontdoorRule#cdn_frontdoor_origin_group_id}.'''
        result = self._values.get("cdn_frontdoor_origin_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#compression_enabled CdnFrontdoorRule#compression_enabled}.'''
        result = self._values.get("compression_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forwarding_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#forwarding_protocol CdnFrontdoorRule#forwarding_protocol}.'''
        result = self._values.get("forwarding_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_string_caching_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string_caching_behavior CdnFrontdoorRule#query_string_caching_behavior}.'''
        result = self._values.get("query_string_caching_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_string_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string_parameters CdnFrontdoorRule#query_string_parameters}.'''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleActionsRouteConfigurationOverrideAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleActionsRouteConfigurationOverrideActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsRouteConfigurationOverrideActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72b64df89678c6c0957a24603804488e4d863a89033e82208cc22e36d335c261)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCacheBehavior")
    def reset_cache_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheBehavior", []))

    @jsii.member(jsii_name="resetCacheDuration")
    def reset_cache_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheDuration", []))

    @jsii.member(jsii_name="resetCdnFrontdoorOriginGroupId")
    def reset_cdn_frontdoor_origin_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnFrontdoorOriginGroupId", []))

    @jsii.member(jsii_name="resetCompressionEnabled")
    def reset_compression_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionEnabled", []))

    @jsii.member(jsii_name="resetForwardingProtocol")
    def reset_forwarding_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardingProtocol", []))

    @jsii.member(jsii_name="resetQueryStringCachingBehavior")
    def reset_query_string_caching_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringCachingBehavior", []))

    @jsii.member(jsii_name="resetQueryStringParameters")
    def reset_query_string_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringParameters", []))

    @builtins.property
    @jsii.member(jsii_name="cacheBehaviorInput")
    def cache_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheDurationInput")
    def cache_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorOriginGroupIdInput")
    def cdn_frontdoor_origin_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnFrontdoorOriginGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionEnabledInput")
    def compression_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "compressionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingProtocolInput")
    def forwarding_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardingProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringCachingBehaviorInput")
    def query_string_caching_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryStringCachingBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringParametersInput")
    def query_string_parameters_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryStringParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehavior")
    def cache_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheBehavior"))

    @cache_behavior.setter
    def cache_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b98fb5d60dde9d844464007e1ee18af15f3a527cb8376574e514d932e91401c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheDuration")
    def cache_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheDuration"))

    @cache_duration.setter
    def cache_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3428f7a96b433a2a5a44c5d7722658c37abfc5d62b78894880efeebdd2b5c5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorOriginGroupId")
    def cdn_frontdoor_origin_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnFrontdoorOriginGroupId"))

    @cdn_frontdoor_origin_group_id.setter
    def cdn_frontdoor_origin_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b7e279109fc52dcffea658b82f6c41c219dcd9bbba7efd66ca5fd9a1e88608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorOriginGroupId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__df40c2431de117dc52499c16271aca4031d58e9aafbe54cd44fd014bff724710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingProtocol")
    def forwarding_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingProtocol"))

    @forwarding_protocol.setter
    def forwarding_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8e8fabc3184f1cb1b93b541c2c265dec7153f945dec26f0399b5306a83bd0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringCachingBehavior")
    def query_string_caching_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryStringCachingBehavior"))

    @query_string_caching_behavior.setter
    def query_string_caching_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b354544740a307b4c0371cea4ed759680b3455f4ebd8dcdc4ccb757f50c98c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringCachingBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringParameters")
    def query_string_parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringParameters"))

    @query_string_parameters.setter
    def query_string_parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18271e894b2cd0e0cc805427c57ca407aea13cb14a486ef7534ba10cc387d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnFrontdoorRuleActionsRouteConfigurationOverrideAction]:
        return typing.cast(typing.Optional[CdnFrontdoorRuleActionsRouteConfigurationOverrideAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnFrontdoorRuleActionsRouteConfigurationOverrideAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62e26f5f60318bc6b1ad59adadb98cf09940c32e7e422b4914c99b0460e3234b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsUrlRedirectAction",
    jsii_struct_bases=[],
    name_mapping={
        "destination_hostname": "destinationHostname",
        "redirect_type": "redirectType",
        "destination_fragment": "destinationFragment",
        "destination_path": "destinationPath",
        "query_string": "queryString",
        "redirect_protocol": "redirectProtocol",
    },
)
class CdnFrontdoorRuleActionsUrlRedirectAction:
    def __init__(
        self,
        *,
        destination_hostname: builtins.str,
        redirect_type: builtins.str,
        destination_fragment: typing.Optional[builtins.str] = None,
        destination_path: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
        redirect_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination_hostname CdnFrontdoorRule#destination_hostname}.
        :param redirect_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#redirect_type CdnFrontdoorRule#redirect_type}.
        :param destination_fragment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination_fragment CdnFrontdoorRule#destination_fragment}.
        :param destination_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination_path CdnFrontdoorRule#destination_path}.
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string CdnFrontdoorRule#query_string}.
        :param redirect_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#redirect_protocol CdnFrontdoorRule#redirect_protocol}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b436a999aa515d56ba4b3322b0b1f581ae7d2a236add4486a5635b29c7b90ba)
            check_type(argname="argument destination_hostname", value=destination_hostname, expected_type=type_hints["destination_hostname"])
            check_type(argname="argument redirect_type", value=redirect_type, expected_type=type_hints["redirect_type"])
            check_type(argname="argument destination_fragment", value=destination_fragment, expected_type=type_hints["destination_fragment"])
            check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument redirect_protocol", value=redirect_protocol, expected_type=type_hints["redirect_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_hostname": destination_hostname,
            "redirect_type": redirect_type,
        }
        if destination_fragment is not None:
            self._values["destination_fragment"] = destination_fragment
        if destination_path is not None:
            self._values["destination_path"] = destination_path
        if query_string is not None:
            self._values["query_string"] = query_string
        if redirect_protocol is not None:
            self._values["redirect_protocol"] = redirect_protocol

    @builtins.property
    def destination_hostname(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination_hostname CdnFrontdoorRule#destination_hostname}.'''
        result = self._values.get("destination_hostname")
        assert result is not None, "Required property 'destination_hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def redirect_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#redirect_type CdnFrontdoorRule#redirect_type}.'''
        result = self._values.get("redirect_type")
        assert result is not None, "Required property 'redirect_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_fragment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination_fragment CdnFrontdoorRule#destination_fragment}.'''
        result = self._values.get("destination_fragment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination_path CdnFrontdoorRule#destination_path}.'''
        result = self._values.get("destination_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string CdnFrontdoorRule#query_string}.'''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#redirect_protocol CdnFrontdoorRule#redirect_protocol}.'''
        result = self._values.get("redirect_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleActionsUrlRedirectAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleActionsUrlRedirectActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsUrlRedirectActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__882adb3b59e1b10e18919b0effe7e9ab31ed9641180b022a31af3d3068c1d1da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestinationFragment")
    def reset_destination_fragment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationFragment", []))

    @jsii.member(jsii_name="resetDestinationPath")
    def reset_destination_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationPath", []))

    @jsii.member(jsii_name="resetQueryString")
    def reset_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryString", []))

    @jsii.member(jsii_name="resetRedirectProtocol")
    def reset_redirect_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="destinationFragmentInput")
    def destination_fragment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationFragmentInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationHostnameInput")
    def destination_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPathInput")
    def destination_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationPathInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectProtocolInput")
    def redirect_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectTypeInput")
    def redirect_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationFragment")
    def destination_fragment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationFragment"))

    @destination_fragment.setter
    def destination_fragment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c72194fafcaa15d627b40bd0106dbeed4309054dde538883a5ef836d9397b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationFragment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationHostname")
    def destination_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationHostname"))

    @destination_hostname.setter
    def destination_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1945533de70b9c0868c8317520252f89361069e3fd2cb4b38b6a2364712213c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationHostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationPath")
    def destination_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationPath"))

    @destination_path.setter
    def destination_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cbf06384bffb129240be67af432013ee89214a4a248ded549602ad669b1b908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68ff960f2cac2921c2119b4a622194f61aaaa46760d1ab8b70bb90a202794e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectProtocol")
    def redirect_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectProtocol"))

    @redirect_protocol.setter
    def redirect_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3085d4955371010e98a25f988d5a4a3efeb7858bf7e1892b41d1b154d504c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectType")
    def redirect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectType"))

    @redirect_type.setter
    def redirect_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__929bd4b2d73dd08ccdf506ecf6ca5d23ed7c89e045071b4de981309d6168541e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnFrontdoorRuleActionsUrlRedirectAction]:
        return typing.cast(typing.Optional[CdnFrontdoorRuleActionsUrlRedirectAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnFrontdoorRuleActionsUrlRedirectAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aceb5ce3efac446bd27d35f610d60f124d57ca83509a39b935037daeb0cbc3fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsUrlRewriteAction",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "source_pattern": "sourcePattern",
        "preserve_unmatched_path": "preserveUnmatchedPath",
    },
)
class CdnFrontdoorRuleActionsUrlRewriteAction:
    def __init__(
        self,
        *,
        destination: builtins.str,
        source_pattern: builtins.str,
        preserve_unmatched_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination CdnFrontdoorRule#destination}.
        :param source_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#source_pattern CdnFrontdoorRule#source_pattern}.
        :param preserve_unmatched_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#preserve_unmatched_path CdnFrontdoorRule#preserve_unmatched_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa934f9848c2a60554d7ec59ad3a95bacb2edb6c868b0db614be2d062421144)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#destination CdnFrontdoorRule#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#source_pattern CdnFrontdoorRule#source_pattern}.'''
        result = self._values.get("source_pattern")
        assert result is not None, "Required property 'source_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preserve_unmatched_path(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#preserve_unmatched_path CdnFrontdoorRule#preserve_unmatched_path}.'''
        result = self._values.get("preserve_unmatched_path")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleActionsUrlRewriteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleActionsUrlRewriteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleActionsUrlRewriteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62713789306f66d32288f1c062b4497f3953d75c45f61955865439be30d94eea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5176ad265751802b4605bd6c1c7b57b262037695ebbd437f6ecb8a8de9bbfac7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74714aadfb7ce838ad6cad9b51fecd3febc86ea62ab78c140784068e5a04b7be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveUnmatchedPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePattern")
    def source_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcePattern"))

    @source_pattern.setter
    def source_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf7ec56c63488e953d48fd3e8a32cdc656b8165db063f8d62920a66ef59612a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnFrontdoorRuleActionsUrlRewriteAction]:
        return typing.cast(typing.Optional[CdnFrontdoorRuleActionsUrlRewriteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnFrontdoorRuleActionsUrlRewriteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf391bc197cfb3dae217d90d9d52560c2ac10fbe995cd0fe44fd32a1aadd97bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditions",
    jsii_struct_bases=[],
    name_mapping={
        "client_port_condition": "clientPortCondition",
        "cookies_condition": "cookiesCondition",
        "host_name_condition": "hostNameCondition",
        "http_version_condition": "httpVersionCondition",
        "is_device_condition": "isDeviceCondition",
        "post_args_condition": "postArgsCondition",
        "query_string_condition": "queryStringCondition",
        "remote_address_condition": "remoteAddressCondition",
        "request_body_condition": "requestBodyCondition",
        "request_header_condition": "requestHeaderCondition",
        "request_method_condition": "requestMethodCondition",
        "request_scheme_condition": "requestSchemeCondition",
        "request_uri_condition": "requestUriCondition",
        "server_port_condition": "serverPortCondition",
        "socket_address_condition": "socketAddressCondition",
        "ssl_protocol_condition": "sslProtocolCondition",
        "url_file_extension_condition": "urlFileExtensionCondition",
        "url_filename_condition": "urlFilenameCondition",
        "url_path_condition": "urlPathCondition",
    },
)
class CdnFrontdoorRuleConditions:
    def __init__(
        self,
        *,
        client_port_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsClientPortCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cookies_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsCookiesCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host_name_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsHostNameCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_version_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsHttpVersionCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_device_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsIsDeviceCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_args_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsPostArgsCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_string_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsQueryStringCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        remote_address_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRemoteAddressCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_body_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestBodyCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestHeaderCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_method_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestMethodCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_scheme_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestSchemeCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_uri_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestUriCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        server_port_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsServerPortCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        socket_address_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsSocketAddressCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssl_protocol_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsSslProtocolCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_file_extension_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsUrlFileExtensionCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_filename_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsUrlFilenameCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_path_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsUrlPathCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param client_port_condition: client_port_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#client_port_condition CdnFrontdoorRule#client_port_condition}
        :param cookies_condition: cookies_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cookies_condition CdnFrontdoorRule#cookies_condition}
        :param host_name_condition: host_name_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#host_name_condition CdnFrontdoorRule#host_name_condition}
        :param http_version_condition: http_version_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#http_version_condition CdnFrontdoorRule#http_version_condition}
        :param is_device_condition: is_device_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#is_device_condition CdnFrontdoorRule#is_device_condition}
        :param post_args_condition: post_args_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#post_args_condition CdnFrontdoorRule#post_args_condition}
        :param query_string_condition: query_string_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string_condition CdnFrontdoorRule#query_string_condition}
        :param remote_address_condition: remote_address_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#remote_address_condition CdnFrontdoorRule#remote_address_condition}
        :param request_body_condition: request_body_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_body_condition CdnFrontdoorRule#request_body_condition}
        :param request_header_condition: request_header_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_header_condition CdnFrontdoorRule#request_header_condition}
        :param request_method_condition: request_method_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_method_condition CdnFrontdoorRule#request_method_condition}
        :param request_scheme_condition: request_scheme_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_scheme_condition CdnFrontdoorRule#request_scheme_condition}
        :param request_uri_condition: request_uri_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_uri_condition CdnFrontdoorRule#request_uri_condition}
        :param server_port_condition: server_port_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#server_port_condition CdnFrontdoorRule#server_port_condition}
        :param socket_address_condition: socket_address_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#socket_address_condition CdnFrontdoorRule#socket_address_condition}
        :param ssl_protocol_condition: ssl_protocol_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#ssl_protocol_condition CdnFrontdoorRule#ssl_protocol_condition}
        :param url_file_extension_condition: url_file_extension_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_file_extension_condition CdnFrontdoorRule#url_file_extension_condition}
        :param url_filename_condition: url_filename_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_filename_condition CdnFrontdoorRule#url_filename_condition}
        :param url_path_condition: url_path_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_path_condition CdnFrontdoorRule#url_path_condition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d9dc83aa6d0243a218d6e3f2aff748ea87e7b633df4f7a65e4c2f44d52b0ad)
            check_type(argname="argument client_port_condition", value=client_port_condition, expected_type=type_hints["client_port_condition"])
            check_type(argname="argument cookies_condition", value=cookies_condition, expected_type=type_hints["cookies_condition"])
            check_type(argname="argument host_name_condition", value=host_name_condition, expected_type=type_hints["host_name_condition"])
            check_type(argname="argument http_version_condition", value=http_version_condition, expected_type=type_hints["http_version_condition"])
            check_type(argname="argument is_device_condition", value=is_device_condition, expected_type=type_hints["is_device_condition"])
            check_type(argname="argument post_args_condition", value=post_args_condition, expected_type=type_hints["post_args_condition"])
            check_type(argname="argument query_string_condition", value=query_string_condition, expected_type=type_hints["query_string_condition"])
            check_type(argname="argument remote_address_condition", value=remote_address_condition, expected_type=type_hints["remote_address_condition"])
            check_type(argname="argument request_body_condition", value=request_body_condition, expected_type=type_hints["request_body_condition"])
            check_type(argname="argument request_header_condition", value=request_header_condition, expected_type=type_hints["request_header_condition"])
            check_type(argname="argument request_method_condition", value=request_method_condition, expected_type=type_hints["request_method_condition"])
            check_type(argname="argument request_scheme_condition", value=request_scheme_condition, expected_type=type_hints["request_scheme_condition"])
            check_type(argname="argument request_uri_condition", value=request_uri_condition, expected_type=type_hints["request_uri_condition"])
            check_type(argname="argument server_port_condition", value=server_port_condition, expected_type=type_hints["server_port_condition"])
            check_type(argname="argument socket_address_condition", value=socket_address_condition, expected_type=type_hints["socket_address_condition"])
            check_type(argname="argument ssl_protocol_condition", value=ssl_protocol_condition, expected_type=type_hints["ssl_protocol_condition"])
            check_type(argname="argument url_file_extension_condition", value=url_file_extension_condition, expected_type=type_hints["url_file_extension_condition"])
            check_type(argname="argument url_filename_condition", value=url_filename_condition, expected_type=type_hints["url_filename_condition"])
            check_type(argname="argument url_path_condition", value=url_path_condition, expected_type=type_hints["url_path_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_port_condition is not None:
            self._values["client_port_condition"] = client_port_condition
        if cookies_condition is not None:
            self._values["cookies_condition"] = cookies_condition
        if host_name_condition is not None:
            self._values["host_name_condition"] = host_name_condition
        if http_version_condition is not None:
            self._values["http_version_condition"] = http_version_condition
        if is_device_condition is not None:
            self._values["is_device_condition"] = is_device_condition
        if post_args_condition is not None:
            self._values["post_args_condition"] = post_args_condition
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
        if server_port_condition is not None:
            self._values["server_port_condition"] = server_port_condition
        if socket_address_condition is not None:
            self._values["socket_address_condition"] = socket_address_condition
        if ssl_protocol_condition is not None:
            self._values["ssl_protocol_condition"] = ssl_protocol_condition
        if url_file_extension_condition is not None:
            self._values["url_file_extension_condition"] = url_file_extension_condition
        if url_filename_condition is not None:
            self._values["url_filename_condition"] = url_filename_condition
        if url_path_condition is not None:
            self._values["url_path_condition"] = url_path_condition

    @builtins.property
    def client_port_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsClientPortCondition"]]]:
        '''client_port_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#client_port_condition CdnFrontdoorRule#client_port_condition}
        '''
        result = self._values.get("client_port_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsClientPortCondition"]]], result)

    @builtins.property
    def cookies_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsCookiesCondition"]]]:
        '''cookies_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cookies_condition CdnFrontdoorRule#cookies_condition}
        '''
        result = self._values.get("cookies_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsCookiesCondition"]]], result)

    @builtins.property
    def host_name_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsHostNameCondition"]]]:
        '''host_name_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#host_name_condition CdnFrontdoorRule#host_name_condition}
        '''
        result = self._values.get("host_name_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsHostNameCondition"]]], result)

    @builtins.property
    def http_version_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsHttpVersionCondition"]]]:
        '''http_version_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#http_version_condition CdnFrontdoorRule#http_version_condition}
        '''
        result = self._values.get("http_version_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsHttpVersionCondition"]]], result)

    @builtins.property
    def is_device_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsIsDeviceCondition"]]]:
        '''is_device_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#is_device_condition CdnFrontdoorRule#is_device_condition}
        '''
        result = self._values.get("is_device_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsIsDeviceCondition"]]], result)

    @builtins.property
    def post_args_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsPostArgsCondition"]]]:
        '''post_args_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#post_args_condition CdnFrontdoorRule#post_args_condition}
        '''
        result = self._values.get("post_args_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsPostArgsCondition"]]], result)

    @builtins.property
    def query_string_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsQueryStringCondition"]]]:
        '''query_string_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#query_string_condition CdnFrontdoorRule#query_string_condition}
        '''
        result = self._values.get("query_string_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsQueryStringCondition"]]], result)

    @builtins.property
    def remote_address_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRemoteAddressCondition"]]]:
        '''remote_address_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#remote_address_condition CdnFrontdoorRule#remote_address_condition}
        '''
        result = self._values.get("remote_address_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRemoteAddressCondition"]]], result)

    @builtins.property
    def request_body_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestBodyCondition"]]]:
        '''request_body_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_body_condition CdnFrontdoorRule#request_body_condition}
        '''
        result = self._values.get("request_body_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestBodyCondition"]]], result)

    @builtins.property
    def request_header_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestHeaderCondition"]]]:
        '''request_header_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_header_condition CdnFrontdoorRule#request_header_condition}
        '''
        result = self._values.get("request_header_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestHeaderCondition"]]], result)

    @builtins.property
    def request_method_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestMethodCondition"]]]:
        '''request_method_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_method_condition CdnFrontdoorRule#request_method_condition}
        '''
        result = self._values.get("request_method_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestMethodCondition"]]], result)

    @builtins.property
    def request_scheme_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestSchemeCondition"]]]:
        '''request_scheme_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_scheme_condition CdnFrontdoorRule#request_scheme_condition}
        '''
        result = self._values.get("request_scheme_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestSchemeCondition"]]], result)

    @builtins.property
    def request_uri_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestUriCondition"]]]:
        '''request_uri_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#request_uri_condition CdnFrontdoorRule#request_uri_condition}
        '''
        result = self._values.get("request_uri_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestUriCondition"]]], result)

    @builtins.property
    def server_port_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsServerPortCondition"]]]:
        '''server_port_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#server_port_condition CdnFrontdoorRule#server_port_condition}
        '''
        result = self._values.get("server_port_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsServerPortCondition"]]], result)

    @builtins.property
    def socket_address_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsSocketAddressCondition"]]]:
        '''socket_address_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#socket_address_condition CdnFrontdoorRule#socket_address_condition}
        '''
        result = self._values.get("socket_address_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsSocketAddressCondition"]]], result)

    @builtins.property
    def ssl_protocol_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsSslProtocolCondition"]]]:
        '''ssl_protocol_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#ssl_protocol_condition CdnFrontdoorRule#ssl_protocol_condition}
        '''
        result = self._values.get("ssl_protocol_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsSslProtocolCondition"]]], result)

    @builtins.property
    def url_file_extension_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlFileExtensionCondition"]]]:
        '''url_file_extension_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_file_extension_condition CdnFrontdoorRule#url_file_extension_condition}
        '''
        result = self._values.get("url_file_extension_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlFileExtensionCondition"]]], result)

    @builtins.property
    def url_filename_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlFilenameCondition"]]]:
        '''url_filename_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_filename_condition CdnFrontdoorRule#url_filename_condition}
        '''
        result = self._values.get("url_filename_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlFilenameCondition"]]], result)

    @builtins.property
    def url_path_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlPathCondition"]]]:
        '''url_path_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#url_path_condition CdnFrontdoorRule#url_path_condition}
        '''
        result = self._values.get("url_path_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlPathCondition"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsClientPortCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
    },
)
class CdnFrontdoorRuleConditionsClientPortCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d157bfdbf3f48b33f5952b00f2513611b5ed91c55bad2b91e29b0a833d2656)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsClientPortCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsClientPortConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsClientPortConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6baaebe9b3b8510e40fb18b30a68c02a03c484a20badde0a972819af109696d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsClientPortConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b3cc31aa01a7f3cc9a094fee6c7cd73bb4b9a90a01d9ef1a03815a937a5f30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsClientPortConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4e39d6a168f9ffb253f41ff579fe9a1b576e686a25d2c188eaa224abe51571)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11a02129cb8f08e12f342dda7f553a8bc56e5efab1fd2b0c91dc9545ea1b0269)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fc9407120e250fb1692cc86d53f908507e7331c5fe71b235294c05e61652931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsClientPortCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsClientPortCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsClientPortCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd7a112c28235cdcc5a75aa262a7d8dda2fa8724cfee772ac5321610be6d475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsClientPortConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsClientPortConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09ad83e40b158a91447e985628268ca7b96c16e30a5182087fd18ec0be199c13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f308f9a4fb799dd691b3dfceb6a27514ccabb9c4971f1814cc6698b22929c2b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a4ab1559092fd78005cefea691113c8a9e3b597f9bfdb531dc5b43011976c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15dfb9962ff75c2174b0e6a3b2064963263055326b0b72f9c626c4d3d16d9496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsClientPortCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsClientPortCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsClientPortCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e0964a3e8ca29c094288e0acf3e4ad09ee12745d585d5b61fb7531e80cf1b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsCookiesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "cookie_name": "cookieName",
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsCookiesCondition:
    def __init__(
        self,
        *,
        cookie_name: builtins.str,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cookie_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cookie_name CdnFrontdoorRule#cookie_name}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9438bd6d58c889b0f6557dc11e0a15ac8e27ab06a80bd23496330d667ea5f44)
            check_type(argname="argument cookie_name", value=cookie_name, expected_type=type_hints["cookie_name"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cookie_name": cookie_name,
            "operator": operator,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def cookie_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cookie_name CdnFrontdoorRule#cookie_name}.'''
        result = self._values.get("cookie_name")
        assert result is not None, "Required property 'cookie_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsCookiesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsCookiesConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsCookiesConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8a868a332bbad9ad699b0ab0bad64bb121bb791727c9b75e3012045e8fae2ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsCookiesConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a2ca5b55ad8d9fc283c479e70b424b3840e45731424309e719abeceb91a069)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsCookiesConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e986dfc13e42c3bda63e609f2ba91b11bd86f77c51b2656c284666607866fb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88878c64d3761f53c2c2ecbdeb5541e2c6efa826db1542be30b8db8f08f4332c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e8a740eaa4c7ae4529577143176afcf744448afbd87263e5dc56cbc64c9c177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsCookiesCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsCookiesCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsCookiesCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa507111033c988dc44afa3663438009636166ce97fb6433dece02a6cd8892d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsCookiesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsCookiesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b9060fbcff7bfe47ad762e6535789ffe64d16f53e5eaee793e30a36cbb73f44)
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
    @jsii.member(jsii_name="cookieNameInput")
    def cookie_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cookieNameInput"))

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
    @jsii.member(jsii_name="cookieName")
    def cookie_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieName"))

    @cookie_name.setter
    def cookie_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea267df04514276f736c92f07cb79f5d7c3949bb26d4b6f182790fd5bfdcef1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74bce4f3a0839d97e1996fc26e1992cbffd54908d5d9c0e76c590b5b1a718b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51e195bf21ac1f70d30bb3843e4213d7c363a023252a7db9c7b4de08dd448318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fc11902b8a70c0fd092525944e540c6077ec48d89db28cfabb0ed5e440c2aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6953b32cc198494e9bfe5a48dea1a5ced4274e500f8dbf316aa8a3d6472409d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsCookiesCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsCookiesCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsCookiesCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbd39bbacf9a04ea67fa736b86a226c0ea29c8b24a00d255bcfdb87df666aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsHostNameCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsHostNameCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0efc2cc466b6ef7ccec360370c2c7d504590f01ac6958b7fc45c2353950b4f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsHostNameCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsHostNameConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsHostNameConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96e2d32737b9642e1263bd6208fcfe0552f7d271dde237e6bc4c25901002f6ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsHostNameConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5d70bfcee1906dc1045169bfb2815ccb9e1aaaebcaed2fabfd199f8a1b53b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsHostNameConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c400dccf3b9bfa94651176d0c75734f49d7441d4007cd6f23d78ac60b3a007b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf493b6bee6e4ae3dc3abf73ae502dc85ede51b15374077bd1736d09ceb7ac79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c21c0faa36b44d7f26f427232c89bfb840c7a84ba9b90f641cc5e7ebfcc622c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHostNameCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHostNameCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHostNameCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b70e7db5fba2f24d91bc89ce9a430c0112e7eb8ccc80d6ccec23c6dba741e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsHostNameConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsHostNameConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a28367d0a593eda2cb4ce488a19173e62289bc7cef75cdaa520d9b83c3c11fc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3d2ac631ba460674dbf97e0feff251e088fe87fd8a45e44917618e3d3ee2b42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d60f6714bf1b7cefb325736e2eccc27dddf452ef5a245242f05d561f2ac1be6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99384a7c7b932d6ef012f7055890c78265edbcc0c654c47dbeb3e9e96f20d252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753aaf839edad967fc0b5e1d20eba9c3f53a5ba91158af4fd96fda45327a6cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsHostNameCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsHostNameCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsHostNameCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__615ecbc0b8ed67eae93a8f59920c3d80ccdaa434d0b98ed8d8f41ddf9b0baf08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsHttpVersionCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnFrontdoorRuleConditionsHttpVersionCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef40d9d3f57e2533bbe22ad5faa597e5ec93ffbc58bb341070ea408e58b35abd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsHttpVersionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsHttpVersionConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsHttpVersionConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e04941bd783b7081be552d47fb0e4a00e98f1ed19adf8a6845be55a6ea9bd81f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsHttpVersionConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81cb69400367f2704e66935988fd84377d4cde62410463e085cc6f5ebc88b5d7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsHttpVersionConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a9b354a6c9c5d8ac9e1615d570a02606ef32e94b534b0d99f00980f94ec3b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__937acf85519a409a057de356dbdc25bcfb8d2036504027330e4706fad7553c40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0a929a38e5c23e963ccf35766c83d7189e1865e8f7314687aeb8e859f8a3983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHttpVersionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHttpVersionCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHttpVersionCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e97b2bf2d0492c3967f73dc0911f24a4f781d559bcb304566ed6b9e3af9e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsHttpVersionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsHttpVersionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26c938e84fde41ae92d899f08dd284acd89d055dcc65d24cc9c5ec06f7b7b754)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c1dbc26335591280a2ae0e983cd274d688621cc750f75f9a7cf6ad7dedd8bec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc93faf299e258f00d1ce59b424d1249c66867483383569f5e633f5ec1ee7ad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab72ac9b68bfc4bafc86355aaa7ec452e9bdde02db88a0f7be1ac162a4544ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsHttpVersionCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsHttpVersionCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsHttpVersionCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d31e655a7c14e4e1cd20e1af1a97cd18a0985f5d7cf3be4da1394b74df6bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsIsDeviceCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnFrontdoorRuleConditionsIsDeviceCondition:
    def __init__(
        self,
        *,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50710182b2216f73e20555a95019f78afc90bacb7d8b6af6d08ef30c23da02b)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsIsDeviceCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsIsDeviceConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsIsDeviceConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__344f840113a9fbd1c8eef5d703f68130415e0316cb3201dad70466d8b58fef1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsIsDeviceConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3711bf8ac4ea4f02c3151e6bd399ae00be640aa3eaddc1038d6866bff90f251)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsIsDeviceConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af088d6b1e58a0551ba673a69800af4ebd68b1b62f6cf07c8b0929e7b67c0c8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8db3f2f14ef5244fb756d02246ac9f690b5b8a6c51faca56a3ccb0a16d5e145b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35ac323c1d8118dea890bfd559d3780974ceda334d61530ed64c5f0e97cc6d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsIsDeviceCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsIsDeviceCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsIsDeviceCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d772e4938f0996669a8f2949f5cc4d5e073b5544441e376c55c69915415bc9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsIsDeviceConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsIsDeviceConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f27930a43df5c262c30d13381f4a449384de05c7e47a3e04ac69fa1e246236)
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
            type_hints = typing.get_type_hints(_typecheckingstub__567098854a58a16f712a17098f4e11d74630d0303bfb7cd4c4d275664f337da5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba9b52ed64649ad17a8654b12907b0f3e119cd9fe6e18f4831f585efebcc216a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058423b2d08db19b8b9715ce4a63f2bcd8225689f17e49237e9b9495943b8aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsIsDeviceCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsIsDeviceCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsIsDeviceCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4610de2f1554a069431909a20e7ed8776f4658ee98c6a053ab3c9a6a344f9810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3108b6cd1c282cf756c9505bf15864c7cd11ed305b70d4bdb7719d755cf53ede)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientPortCondition")
    def put_client_port_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsClientPortCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591b6aac9b62a7fc9362b81ff46adfc823c61028bf8e6e88cbb5b391ca58bad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClientPortCondition", [value]))

    @jsii.member(jsii_name="putCookiesCondition")
    def put_cookies_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsCookiesCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9ce9084a6c9308bb4b03fd6a22058fd589ebb1be26ef1a174455ae4c7cacbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCookiesCondition", [value]))

    @jsii.member(jsii_name="putHostNameCondition")
    def put_host_name_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsHostNameCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f46df871a8b3085e98b6124c0234135a9004076018339da82093fce2bbb915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHostNameCondition", [value]))

    @jsii.member(jsii_name="putHttpVersionCondition")
    def put_http_version_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsHttpVersionCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556feabeb891b4794ceb404f20ac58c76b0648401e6a523756f68a55f3ba7f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpVersionCondition", [value]))

    @jsii.member(jsii_name="putIsDeviceCondition")
    def put_is_device_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsIsDeviceCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc72187460f63abfc3a723ae35047037a3768b5668c85e8af630669928103db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIsDeviceCondition", [value]))

    @jsii.member(jsii_name="putPostArgsCondition")
    def put_post_args_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsPostArgsCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d6a93b5b5fda0506bb4c9f8c4cafc8614b1701d685c598cbe8da21141ef959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostArgsCondition", [value]))

    @jsii.member(jsii_name="putQueryStringCondition")
    def put_query_string_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsQueryStringCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a989343576d1adc4678924a84ec810ec5f2d43505f91333c16628e1431375248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryStringCondition", [value]))

    @jsii.member(jsii_name="putRemoteAddressCondition")
    def put_remote_address_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRemoteAddressCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535920147775bff1e1b66ff9883acd47487745d2175312fc7c5a15e50d666830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRemoteAddressCondition", [value]))

    @jsii.member(jsii_name="putRequestBodyCondition")
    def put_request_body_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestBodyCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80239b468ee20a2ef0018a83fd838b3ea85f45af5cbffaccf844b1fccedefb74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestBodyCondition", [value]))

    @jsii.member(jsii_name="putRequestHeaderCondition")
    def put_request_header_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestHeaderCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d79eeebd0c52e36102d4895f0cc0a8b19b7a80a046b0f47843e8d9eabb018c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaderCondition", [value]))

    @jsii.member(jsii_name="putRequestMethodCondition")
    def put_request_method_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestMethodCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7963da5f4bcc54412e3b61c00fa79ab8cfdf712cbaf53967fbd7382c2d4b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestMethodCondition", [value]))

    @jsii.member(jsii_name="putRequestSchemeCondition")
    def put_request_scheme_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestSchemeCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec26aa8b87ae5f49973e1cbe3c88101ccc32aafd3d0c5566c234695993efee14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestSchemeCondition", [value]))

    @jsii.member(jsii_name="putRequestUriCondition")
    def put_request_uri_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsRequestUriCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e837ce8c5a0dd4776c8f7f5bfeb9f35d5c57a6231f5f5c4d265f6ac5f477166c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestUriCondition", [value]))

    @jsii.member(jsii_name="putServerPortCondition")
    def put_server_port_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsServerPortCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325a728fc9b59b420bd562aa4a9561dfec9385faf264cbc28f6e4ffc01e17e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServerPortCondition", [value]))

    @jsii.member(jsii_name="putSocketAddressCondition")
    def put_socket_address_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsSocketAddressCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b08a9d2bdf36b21c08595975a7ac053d77ce845957108836c4096939ac4266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSocketAddressCondition", [value]))

    @jsii.member(jsii_name="putSslProtocolCondition")
    def put_ssl_protocol_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsSslProtocolCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d30aec142702e59fb4575beaeb58656890b36a455f4862d75cd48293017bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSslProtocolCondition", [value]))

    @jsii.member(jsii_name="putUrlFileExtensionCondition")
    def put_url_file_extension_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsUrlFileExtensionCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71daef5621717b9f3d74f10ff4f0d0fac4a1b3463238b9f970f117372c82d554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrlFileExtensionCondition", [value]))

    @jsii.member(jsii_name="putUrlFilenameCondition")
    def put_url_filename_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsUrlFilenameCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ac896651e0f52b965845989c58ae4ea4759a76e3335411c132e9777ee42ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrlFilenameCondition", [value]))

    @jsii.member(jsii_name="putUrlPathCondition")
    def put_url_path_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorRuleConditionsUrlPathCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299c6f4248a47aca61e307afad5baab5ff5f07801c4765d925d50450745f53a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrlPathCondition", [value]))

    @jsii.member(jsii_name="resetClientPortCondition")
    def reset_client_port_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientPortCondition", []))

    @jsii.member(jsii_name="resetCookiesCondition")
    def reset_cookies_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookiesCondition", []))

    @jsii.member(jsii_name="resetHostNameCondition")
    def reset_host_name_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostNameCondition", []))

    @jsii.member(jsii_name="resetHttpVersionCondition")
    def reset_http_version_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpVersionCondition", []))

    @jsii.member(jsii_name="resetIsDeviceCondition")
    def reset_is_device_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsDeviceCondition", []))

    @jsii.member(jsii_name="resetPostArgsCondition")
    def reset_post_args_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostArgsCondition", []))

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

    @jsii.member(jsii_name="resetServerPortCondition")
    def reset_server_port_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerPortCondition", []))

    @jsii.member(jsii_name="resetSocketAddressCondition")
    def reset_socket_address_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSocketAddressCondition", []))

    @jsii.member(jsii_name="resetSslProtocolCondition")
    def reset_ssl_protocol_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslProtocolCondition", []))

    @jsii.member(jsii_name="resetUrlFileExtensionCondition")
    def reset_url_file_extension_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlFileExtensionCondition", []))

    @jsii.member(jsii_name="resetUrlFilenameCondition")
    def reset_url_filename_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlFilenameCondition", []))

    @jsii.member(jsii_name="resetUrlPathCondition")
    def reset_url_path_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlPathCondition", []))

    @builtins.property
    @jsii.member(jsii_name="clientPortCondition")
    def client_port_condition(
        self,
    ) -> CdnFrontdoorRuleConditionsClientPortConditionList:
        return typing.cast(CdnFrontdoorRuleConditionsClientPortConditionList, jsii.get(self, "clientPortCondition"))

    @builtins.property
    @jsii.member(jsii_name="cookiesCondition")
    def cookies_condition(self) -> CdnFrontdoorRuleConditionsCookiesConditionList:
        return typing.cast(CdnFrontdoorRuleConditionsCookiesConditionList, jsii.get(self, "cookiesCondition"))

    @builtins.property
    @jsii.member(jsii_name="hostNameCondition")
    def host_name_condition(self) -> CdnFrontdoorRuleConditionsHostNameConditionList:
        return typing.cast(CdnFrontdoorRuleConditionsHostNameConditionList, jsii.get(self, "hostNameCondition"))

    @builtins.property
    @jsii.member(jsii_name="httpVersionCondition")
    def http_version_condition(
        self,
    ) -> CdnFrontdoorRuleConditionsHttpVersionConditionList:
        return typing.cast(CdnFrontdoorRuleConditionsHttpVersionConditionList, jsii.get(self, "httpVersionCondition"))

    @builtins.property
    @jsii.member(jsii_name="isDeviceCondition")
    def is_device_condition(self) -> CdnFrontdoorRuleConditionsIsDeviceConditionList:
        return typing.cast(CdnFrontdoorRuleConditionsIsDeviceConditionList, jsii.get(self, "isDeviceCondition"))

    @builtins.property
    @jsii.member(jsii_name="postArgsCondition")
    def post_args_condition(self) -> "CdnFrontdoorRuleConditionsPostArgsConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsPostArgsConditionList", jsii.get(self, "postArgsCondition"))

    @builtins.property
    @jsii.member(jsii_name="queryStringCondition")
    def query_string_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsQueryStringConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsQueryStringConditionList", jsii.get(self, "queryStringCondition"))

    @builtins.property
    @jsii.member(jsii_name="remoteAddressCondition")
    def remote_address_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsRemoteAddressConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsRemoteAddressConditionList", jsii.get(self, "remoteAddressCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyCondition")
    def request_body_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsRequestBodyConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsRequestBodyConditionList", jsii.get(self, "requestBodyCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderCondition")
    def request_header_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsRequestHeaderConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsRequestHeaderConditionList", jsii.get(self, "requestHeaderCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestMethodCondition")
    def request_method_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsRequestMethodConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsRequestMethodConditionList", jsii.get(self, "requestMethodCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestSchemeCondition")
    def request_scheme_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsRequestSchemeConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsRequestSchemeConditionList", jsii.get(self, "requestSchemeCondition"))

    @builtins.property
    @jsii.member(jsii_name="requestUriCondition")
    def request_uri_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsRequestUriConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsRequestUriConditionList", jsii.get(self, "requestUriCondition"))

    @builtins.property
    @jsii.member(jsii_name="serverPortCondition")
    def server_port_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsServerPortConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsServerPortConditionList", jsii.get(self, "serverPortCondition"))

    @builtins.property
    @jsii.member(jsii_name="socketAddressCondition")
    def socket_address_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsSocketAddressConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsSocketAddressConditionList", jsii.get(self, "socketAddressCondition"))

    @builtins.property
    @jsii.member(jsii_name="sslProtocolCondition")
    def ssl_protocol_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsSslProtocolConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsSslProtocolConditionList", jsii.get(self, "sslProtocolCondition"))

    @builtins.property
    @jsii.member(jsii_name="urlFileExtensionCondition")
    def url_file_extension_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsUrlFileExtensionConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsUrlFileExtensionConditionList", jsii.get(self, "urlFileExtensionCondition"))

    @builtins.property
    @jsii.member(jsii_name="urlFilenameCondition")
    def url_filename_condition(
        self,
    ) -> "CdnFrontdoorRuleConditionsUrlFilenameConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsUrlFilenameConditionList", jsii.get(self, "urlFilenameCondition"))

    @builtins.property
    @jsii.member(jsii_name="urlPathCondition")
    def url_path_condition(self) -> "CdnFrontdoorRuleConditionsUrlPathConditionList":
        return typing.cast("CdnFrontdoorRuleConditionsUrlPathConditionList", jsii.get(self, "urlPathCondition"))

    @builtins.property
    @jsii.member(jsii_name="clientPortConditionInput")
    def client_port_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsClientPortCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsClientPortCondition]]], jsii.get(self, "clientPortConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="cookiesConditionInput")
    def cookies_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsCookiesCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsCookiesCondition]]], jsii.get(self, "cookiesConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameConditionInput")
    def host_name_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHostNameCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHostNameCondition]]], jsii.get(self, "hostNameConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpVersionConditionInput")
    def http_version_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHttpVersionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHttpVersionCondition]]], jsii.get(self, "httpVersionConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="isDeviceConditionInput")
    def is_device_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsIsDeviceCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsIsDeviceCondition]]], jsii.get(self, "isDeviceConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="postArgsConditionInput")
    def post_args_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsPostArgsCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsPostArgsCondition"]]], jsii.get(self, "postArgsConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringConditionInput")
    def query_string_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsQueryStringCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsQueryStringCondition"]]], jsii.get(self, "queryStringConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteAddressConditionInput")
    def remote_address_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRemoteAddressCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRemoteAddressCondition"]]], jsii.get(self, "remoteAddressConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyConditionInput")
    def request_body_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestBodyCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestBodyCondition"]]], jsii.get(self, "requestBodyConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderConditionInput")
    def request_header_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestHeaderCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestHeaderCondition"]]], jsii.get(self, "requestHeaderConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestMethodConditionInput")
    def request_method_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestMethodCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestMethodCondition"]]], jsii.get(self, "requestMethodConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestSchemeConditionInput")
    def request_scheme_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestSchemeCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestSchemeCondition"]]], jsii.get(self, "requestSchemeConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriConditionInput")
    def request_uri_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestUriCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsRequestUriCondition"]]], jsii.get(self, "requestUriConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="serverPortConditionInput")
    def server_port_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsServerPortCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsServerPortCondition"]]], jsii.get(self, "serverPortConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="socketAddressConditionInput")
    def socket_address_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsSocketAddressCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsSocketAddressCondition"]]], jsii.get(self, "socketAddressConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="sslProtocolConditionInput")
    def ssl_protocol_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsSslProtocolCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsSslProtocolCondition"]]], jsii.get(self, "sslProtocolConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlFileExtensionConditionInput")
    def url_file_extension_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlFileExtensionCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlFileExtensionCondition"]]], jsii.get(self, "urlFileExtensionConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlFilenameConditionInput")
    def url_filename_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlFilenameCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlFilenameCondition"]]], jsii.get(self, "urlFilenameConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlPathConditionInput")
    def url_path_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlPathCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorRuleConditionsUrlPathCondition"]]], jsii.get(self, "urlPathConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CdnFrontdoorRuleConditions]:
        return typing.cast(typing.Optional[CdnFrontdoorRuleConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnFrontdoorRuleConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91d54a9404274751a129441c6a4561399a837611c433ab716b50144f7cad67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsPostArgsCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "post_args_name": "postArgsName",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsPostArgsCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        post_args_name: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param post_args_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#post_args_name CdnFrontdoorRule#post_args_name}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0358b8e8bda4aa95004010080528e88b7697adc4b41454718de9374087ffe67)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument post_args_name", value=post_args_name, expected_type=type_hints["post_args_name"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "post_args_name": post_args_name,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def post_args_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#post_args_name CdnFrontdoorRule#post_args_name}.'''
        result = self._values.get("post_args_name")
        assert result is not None, "Required property 'post_args_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsPostArgsCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsPostArgsConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsPostArgsConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__842f9106e00b155095089c6f8ce1793fc86ccf2d9f9320f9fee985c243baa428)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsPostArgsConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f05a3d089ac3c2dc3fa36a1df472a768b3dbd9f59acabe93a14b31b7fb14bf9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsPostArgsConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e362845a4f1b52b36852cb4a78bd5813782f8a61567db389a6d1dc10ab3f7250)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8319819291045868b1bcffdf515c1e8dc53c44b49dbb8291a94eabe36a119726)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3317431e53c99cb896e88aa389429f77ef05a1cb7df40163b8dc61601a60feac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsPostArgsCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsPostArgsCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsPostArgsCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8f3a8619bf6202a2842ea41f64f3377f3c30fefdad490d19d74404e2917e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsPostArgsConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsPostArgsConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dc8f01950ea7c5f7dd23c5eb4cdde52033a46ff71084bd851ef8ecce726d58c)
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
    @jsii.member(jsii_name="postArgsNameInput")
    def post_args_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postArgsNameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f40fe3e8f1a0da806b5e8689f18851129f6503e16bd4e21d52a214bdef91543b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7521c78be677d8784602235fc46bc1a0f30758767b24e448f68a8f14840fed0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ad23321f71e3f1ab8fa6368a2a770267e03ef0f94fef31e53accbaf12f111e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postArgsName")
    def post_args_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postArgsName"))

    @post_args_name.setter
    def post_args_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70959ee00a7477627ac46f66afc32ae50c87e36d93cf864b8363579c6fef555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postArgsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5012f1205baead8e1b518fa374a07a74158dd7948b592cc835ac36c73c1f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsPostArgsCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsPostArgsCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsPostArgsCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ad0f935e7dd4165db772427eea1a06ba9eba2f29583b86a1d0076923a09560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsQueryStringCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsQueryStringCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fab626d8b3df13a80304fdfc2164cb6770666bdc7dbbb6becff14dc5d5405c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsQueryStringCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsQueryStringConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsQueryStringConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e16f0ae3ad1b88b5f668b9747490e0df503a585b390a18c31c055af168a0a3cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsQueryStringConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3cc773b5588f3f533213b06511a1aadbfb12b317f8aea5dd91a78fe44e3da5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsQueryStringConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606c4ea895217f9d19de65f8c180326a15404f1c4dce6928eacd6bde0c28b5d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67da620429bcc7fc5bd296192ed90b50d997814d3c804328ca31106bf66571ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__568ddcdff0800668c3f5baf9983cd9546d3ef6e63d2217d7c9550ab86af7f304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsQueryStringCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsQueryStringCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsQueryStringCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4166f168c029504f759aacc1297449c43c7bec41f03dd23d43961cb294b6dc4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsQueryStringConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsQueryStringConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df5b6b2221f91af8813fa286921119292e4d2692c3a7a46a8edd6148899e2770)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5592d1b12413822cdd4b69b948b5f5473268eef3bf2b76c6ea7258d705aa52cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01547b8c4c4c700a75969c34b5ea457172847629f161976ed5ca3de98513022c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eaaa4a64a80ae2bb92f7ed77bae60d1f2b74c5b8061898289910058004787f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2540d719cf9ef9c8a68cf637a9843569f80984c54f169c53ecf2133014c33c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsQueryStringCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsQueryStringCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsQueryStringCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8f45dfe0b4fe180dd58803c24630670cc64a106d4812ba8ac4d2b695a7e78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRemoteAddressCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnFrontdoorRuleConditionsRemoteAddressCondition:
    def __init__(
        self,
        *,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758430c1cb1011ad9f1ce1bd0fcb51ec025db1aac2a2eeab72f481f9a194139f)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsRemoteAddressCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsRemoteAddressConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRemoteAddressConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a5b8ff325b7c8bfe9528f268766e63fda00e7650ce6fbf51a4c8ea53917e51f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsRemoteAddressConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4ca3b3f08e44cc5a5a2397c0c24eae069ef9014aae0c1a57c887b05ca0bda0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsRemoteAddressConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2758464286b39f56e28a7bc07d934da0486bd9a871a3375399c160ab62ac8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d070caea60b506b14d59beba39ef66065a144c43e6f3f8786f784303bdc8bbd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ce9cb3b78ca176c5938b754085e58ffad208cf9644fd2b93cfc378940299901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRemoteAddressCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRemoteAddressCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRemoteAddressCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a42281c31dfc4dfc43ec6f5cedef5236d4ddabe9be788ed668fbaec3bc49ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsRemoteAddressConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRemoteAddressConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72b30fc8a1a229a4d16460d92da1fa9498c9a596a38868f621bf78da011aebfb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__432974a32f6ddcfe711ddcd60c1641198f3ff6e9e3567f7fb36cafce58ebe042)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95b892bd06f410086774a4fa835c43413d17129e657335353b0ad0782cb2bb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7258bcd724e6d02d5d7bbc5a43254e89e858fea190b48922a56918fa887b1f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRemoteAddressCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRemoteAddressCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRemoteAddressCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2968fcd4a9d5e8c3a044df794687e987d890112805273e0b06dfc2db84302e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestBodyCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "operator": "operator",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsRequestBodyCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        operator: builtins.str,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e065db61395c1ec35598682cfaf909d70f69859abab42f915ed930583461656)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_values": match_values,
            "operator": operator,
        }
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def match_values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsRequestBodyCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsRequestBodyConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestBodyConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2158f433394568cf1753ca60dd57bdf31493144863179040258d114afdeccd76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsRequestBodyConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2bc8fadf48ae2917ca46943971041137334c3b8c22f3e1506ddb18d19987878)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsRequestBodyConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5671908fd5a9d1a77c13fbb72413cae110387291e1fb3a452625339f81916f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__824b2e308de7469624024aced6dce7c2600e376cf011c3ef1c42befe3d2eba75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aae5e5f3981d5d322ee6415c69bcb23373ea63c8467b022e375b194a12c2436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestBodyCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestBodyCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestBodyCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82ae3afaaa9eeb92ba239c4f231475311476d28502394c0b510a7002b4a0ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsRequestBodyConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestBodyConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06884059447b68defc8602f220e434169416e926ae179ebc1d8abd0160253c79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__a90cd1e6de038f6f01fd9f846a46db66264554e583f8377ebd8e7bd7701ace30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b26b6da0cb074508eea11362b951a9ee5a5e0af8eaed2f6e59799e87b50fbb75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d210c31210f27b717a9722766dbc1107daaa33d3e91094b4875fdb7bf3fda1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9481b0906899ead32632a15d89df808889eb13dbcde2d22bb256cdabdc39a57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestBodyCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestBodyCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestBodyCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0aff95821be05f436e9595c36f3db27b1f3e74c658b2e833722edc5d308785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestHeaderCondition",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsRequestHeaderCondition:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_name CdnFrontdoorRule#header_name}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a3763b40df51da402fe0493fd72ff31a4b44e967a948f475c0bbdc0903080a)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
            "operator": operator,
        }
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def header_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#header_name CdnFrontdoorRule#header_name}.'''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsRequestHeaderCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsRequestHeaderConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestHeaderConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ec3be5c37a0a372038dccc502a3dcf3b7024e3d2bbf9033c601c430c222c2e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsRequestHeaderConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74064f43ed90d52da8f44aa7f2460b5b17705d047cc1636ef1c3aeb1cc858354)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsRequestHeaderConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c213162894369e6215814637af027224e8c9297297b41336948002e2a5fac22c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__503154be7bd6ac32d9d273fb66e2124b494c82df83445a15f43ee2333edf3999)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f122fa3eff8b88807f6788ae94329aa0936fb633ecffe30559c15d01a720a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestHeaderCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestHeaderCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestHeaderCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115063ac0613a37303f098da5a797e0ce596bb94c270d38e0598be0449851703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsRequestHeaderConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestHeaderConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79ec9320d533953bfcbd696b16f941ad22f213fcc312d3f3f588a9977d1c2205)
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
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

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
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f36537890b4aedd04e18cbe07bfd7d3166bce49a5e64d0a2dec9c9603080262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchValues")
    def match_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchValues"))

    @match_values.setter
    def match_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba284bfd2189df484462978eb366abbd41d1a9d6e5bc7c6b8ba909dc5460e5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8fc11781967cd9d7ff9892cc3e350d43618bea2f563bacc4ecd72e11a8f0f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e92f70e12ac856a59dfb914cbafb3d320d76ce7b16d045281bfa9d1ae30286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4341b3640ad8b80fb774cbcbf1d963b9cb977d1dcbc0339999a2cc2d6e96d3f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestHeaderCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestHeaderCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestHeaderCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8e714b34ebeba1fcd2055f3bd3dffb1a779575370314fea8f0171212ca8ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestMethodCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnFrontdoorRuleConditionsRequestMethodCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb6101da2e465131beed5928ca9e008c0435b5cb3af0c272db489a182de5edc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsRequestMethodCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsRequestMethodConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestMethodConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d3e209e561cbd707586b2089285c512330c77bbd692c27dbf489809ed923d49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsRequestMethodConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a1dab8cdd818c6ea962c3f81677b88fd60c89d41f8eebe396cecb81dc650ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsRequestMethodConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b64660dadc055287fa67878f3ad12b91df720dc2189ba51dacfd13b3d758c78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3658157a1d9fb063a55af0fe5eaecde4646203d227ca86dbf039c7bdb4d962c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b24b4ed45dca67095f22b9a0a19179d81c6b6b85f40826f36269b51ba48dc2f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestMethodCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestMethodCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestMethodCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8cc7584832357cb5978a0472d235c09d041d1c4546be54756e4f293f1aff07d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsRequestMethodConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestMethodConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca670f56a3bba3e7e4495a07a2ad48d40152d2da12c1299ca1e323c73d0e2373)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53a8fb115cda44596397133165c25e3dd38f2ac6ca193c7eb3f8bf69f6a12331)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dac623e9f26bc7b22c8d2bef2c794629160505203cf67506806046314952f76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3590b6a8597bec05c472624c03459fbef3e88f3b03ae082f6a2bb6a36aed08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestMethodCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestMethodCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestMethodCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172524e2842efdb24ad6f4e9207841ba82bfacf5544907c20e6881bc388eb45c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestSchemeCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnFrontdoorRuleConditionsRequestSchemeCondition:
    def __init__(
        self,
        *,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebbcc27bd5f87cab032bdc32adea1c1ea5717f48a926bdf2ac73d723163e36f)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsRequestSchemeCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsRequestSchemeConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestSchemeConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d925de4121aac4d8553882fab5a568e7ff90029a135d0b53128f8ad22633ef86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsRequestSchemeConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8775ce572a1156bec68691c8cf78036cde1be4a194629c301c83af745429226)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsRequestSchemeConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138b16a25b96e16902fb64ab9c325c7f66feb6652b6cf0ad1b46d5d4c15d1e23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f60e2d16010eaf9b20cebc12cee507de32d9705947a0e7edaa461d34f4da9985)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be7b3eecc8b5f9f7bc4e196bd3ada8d93ee668be709c75235e1fbc96d98596f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestSchemeCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestSchemeCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestSchemeCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6aba6939dc15c5f13c1323b9087fff7b5496d8f243ea3c31ad2fef0d7643349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsRequestSchemeConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestSchemeConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b9090ac47d8b80a3c4a0d7accd3cf60cda0467e3112802b033fb661f4284505)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5cc51d604e826b33614abe614d2946005d4269e1add94dbb8fc0df38af442a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__163f9d51630d9ace98684be008f2e9d2511ae3900b5da9a3866faaa19ef0f7b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9455784df542412ab1c8064bd8f742dd63c0ac335f5f37d76adb862a41dc36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestSchemeCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestSchemeCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestSchemeCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ed5e96558109e7ac7c4e20cebda16126fdeb20ce00f3d57c83ba3197132c47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestUriCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsRequestUriCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a651a9d7d164bb6c9602600334c291acf1a63caa6be457bbad79bb23e1692e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsRequestUriCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsRequestUriConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestUriConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b9fe7efcfec0dc28f04de4ca280c6f29d9b45d9b062fccebc9f8fe7528a37a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsRequestUriConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5701a9a2a312a792b971aef402120bc6dca7ed221bc9ff31004c7cfac8979a1d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsRequestUriConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e82b787129c80cc7959d185601ea97f3e6e8f134b4ec924591c43d2eeaf2b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3a1158c4b4cee2fec8ca9bf6ee37342452424274c09dc1b135225363bfeed75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__128cf93fecefab0b2f8999e219eadfae5409674f0fe860028a4698b1a0631452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestUriCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestUriCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestUriCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c3ee7aad2a29f87655e4dfce9a51efc0be3f623bf5e30301c90bbb419788a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsRequestUriConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsRequestUriConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a9403b8c466a232dee50b1e2e821ec9cc66986c9df20d7f403182d434714a01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dc89878df70ee64fd889730767b74c36cccb5f22175b9e4d039a7b30771d0a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b5695d3ef346a5a55f753bb128f9764f0eaca9f03387fa89dbac8e30ceb10b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1adba2df60eae66414699de7ef066b8f6aaa82aa18eb88d21d5bfefd2d4f4b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8c3ab065453b0c609069fc9e7e40555da433c6c24b9bb0b351f218a3be1847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestUriCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestUriCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestUriCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c01a6bf1a91d83bb660c8f82f1363a6eff270e1a07a0175e600ec2b7c2c98c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsServerPortCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "operator": "operator",
        "negate_condition": "negateCondition",
    },
)
class CdnFrontdoorRuleConditionsServerPortCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        operator: builtins.str,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235b1c794fa6f0eda0ad61e2af68606691758ba6b3643a970f9543fa10e234fb)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_values": match_values,
            "operator": operator,
        }
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition

    @builtins.property
    def match_values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsServerPortCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsServerPortConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsServerPortConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b336ae668d16bb74d33bac17197436032b3f161633acd7f8439482caf96b37f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsServerPortConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd2757a10e20b62888f110d2a5e4b5497bf0be07abc71c24037ebaac66cd316)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsServerPortConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1146d3707a39f535d4a8301f3bb028d002f88726d4a5b5f99a2511174ff9d57b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__045d448bcab075a86c07af6ebb568f25bed6bcbb733646dfa4e2215cad2b0fa3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec49880239afb0fd9de9fa4cf994fac6bf2730f39b7bcc12220e316efaa973c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsServerPortCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsServerPortCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsServerPortCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282d6411e36c218bb9bbd61b9009021a6e303a1c06539b48ed6d4e621f557661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsServerPortConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsServerPortConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11fee2dac34c7e9586957b8a857394b31cc2ac9755c0ae07e303c33dd080cc58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__62f3c6f5ed04787d52e70fc43a0fa97c0f206c0c2b5fcd9fdb2608160da0213d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e2dba3639a22e1c531b2cab46b0ba9ae8b9ed0c6d7909ae91b8804c73382552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb74ee4b54fbfadbddd7c1d4941e304151f45043edeecb61a3392a95900fecfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsServerPortCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsServerPortCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsServerPortCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46f233746ce2bc2adf7f9e564adff56bcf1699d7cedab531ec68c63aa8ca832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsSocketAddressCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnFrontdoorRuleConditionsSocketAddressCondition:
    def __init__(
        self,
        *,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c21f79905ad00bc6024575296c561f84daa2eb664c84b6ccaa5a779e96ec28e)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_values is not None:
            self._values["match_values"] = match_values
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsSocketAddressCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsSocketAddressConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsSocketAddressConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bccf8d1d787e0675060e147776c02ea2febfa7b8988aec9c510272c95e1e058)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsSocketAddressConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665d5084fb1a944befea9d5aede741e5461c3e352db8cbada9a44a8769f25660)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsSocketAddressConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a20b751e6c3f22ce476068d11241f298ba6d820a2b2f87a74feb8c49bab2be00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__438e81f4b6abb1fc8f604efaf1e37b9a9f285d9f91a9b0489c61d3c4a199ed07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a754e11152bb3e1f68a9482b7751c2ccb42789c8a93b3a5935b340d03b85df37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsSocketAddressCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsSocketAddressCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsSocketAddressCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f6ddf27196aa6dd569ed60ffcc0001f8e7eea8636b947cc3f8245b7d791d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsSocketAddressConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsSocketAddressConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f7bb15bfecf841cd1e16c1a9dcb3fdb3c70295a6875fa239fc6ec3edaafc87a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3ff76ca2a47308283631452b4b761f3d0d15c03f10bc9536ec640fbc784fd7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f4d25698aa1111f060c17bdab24ad65aeea88828558225864556cd26e2a18a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2485f2eaa97490500b6cb19ee699ad8371b0c6921715007a38bf064b4a95b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsSocketAddressCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsSocketAddressCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsSocketAddressCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e1944fcf67076e5b11acb9ea36dfea952ec2263d84f581a7cd486bd9455239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsSslProtocolCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "operator": "operator",
    },
)
class CdnFrontdoorRuleConditionsSslProtocolCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e70ced3b779da4d9a50f06cf68ac34031f38c02e7023f2fe29a6df005451d9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsSslProtocolCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsSslProtocolConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsSslProtocolConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__401a3ebbdaed1f7b04907afc28741ea9acb4c4c9c375fef3c34a469cc433150a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsSslProtocolConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d5697a363371fccaec0f88ee15bd2c4baefcf8237d6e8c6f454bde93c1cb92)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsSslProtocolConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4906c2a965476231aaee92ea05813ca7a70abff7cad45e3ac23b52173a8149ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6efc55b754296367a4b94190c6357e3df2e5f56ffb65be4d78df7cf08b9ea575)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d40e45262412e5c37a6f764d614ec7d77e7c8fc774b59ecb7dc58d309d85bbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsSslProtocolCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsSslProtocolCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsSslProtocolCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1df14bd495f2dd571674e20c08ad7e625556c46fb500898c03d93d6d7865f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsSslProtocolConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsSslProtocolConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cf40e5e5e8268baf151038e040ca8fe4435b83d1614c78e6b2bf064175a7e1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b45d22ecdbb95430e2ad6836f76c3f93c22bfa35d8b7e3c8a70a34d390405699)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8b5c0a4c53420e91d2ab91cd77296d39089a9774b1b13dc3cb5cf94ee83ce6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812851b8bdef33d230e72aa73c7336507e5f829be4bbd83dae56e1ec23a2589f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsSslProtocolCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsSslProtocolCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsSslProtocolCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077586d466c7394a82be9c270a0bfe36ec0b8cd003d606b422c408be02a727a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsUrlFileExtensionCondition",
    jsii_struct_bases=[],
    name_mapping={
        "match_values": "matchValues",
        "operator": "operator",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsUrlFileExtensionCondition:
    def __init__(
        self,
        *,
        match_values: typing.Sequence[builtins.str],
        operator: builtins.str,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66871cfd9441a698eaef46901a3dcf3ecc6feaaefd2c304b21b4be443f8ebc66)
            check_type(argname="argument match_values", value=match_values, expected_type=type_hints["match_values"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument negate_condition", value=negate_condition, expected_type=type_hints["negate_condition"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_values": match_values,
            "operator": operator,
        }
        if negate_condition is not None:
            self._values["negate_condition"] = negate_condition
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def match_values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        assert result is not None, "Required property 'match_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsUrlFileExtensionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsUrlFileExtensionConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsUrlFileExtensionConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e5115daaf7fd02f5e1038ee974577c16fa2fd0d43caea6b3e2f25d24838125d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsUrlFileExtensionConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aec7de9dcfba12da3d24c359331c2a6dabf1c4a1f9b603526bb27152db02602)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsUrlFileExtensionConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f912a4214a24c7f2a145550598944e0848f0d4375be67bfd90b6bda1003bb297)
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
            type_hints = typing.get_type_hints(_typecheckingstub__531ab5aaa8b9ff046aec86cdbbe287ceb8a50373a30aad88d55c527d5121df05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d76900d4dd78d72500e23e670b809ac0e4a97b18a5faed29b0e7cdb85673e748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlFileExtensionCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlFileExtensionCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlFileExtensionCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f50e1ff111c9350aa35e5073c0161ba9198cacb02c012da51756c5b2705a269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsUrlFileExtensionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsUrlFileExtensionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__565d534bd163c0b27e4f9a1eb3c230634d9b40e9996d7561692c68e746243673)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__da35c30749544b8cde652bff69bf1f98c26c021e77829c13efa612a154b6d661)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91eb46dd6ffb7d44c88149f826a3f8f5440f67049f44dbf55134b84a2f71c606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ca0cdb60b030304892fa3ba56acd35e5a9c79e6ce9783fe0bbff167e608e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ad90b2ce2dbfb0631269bed6239e1c87865d913c145b4ecd4bc8627d5b8d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlFileExtensionCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlFileExtensionCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlFileExtensionCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a80580d3334857b254f5361692d9d95223413a892ec4521a3fa714624dd4b7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsUrlFilenameCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsUrlFilenameCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7323061299b4e3a3b42c657088947fd5fbf966153fe6663e1d92cb42d285ee4b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsUrlFilenameCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsUrlFilenameConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsUrlFilenameConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__571361d0894c987737a5e2904121cd55b4e899a58d020fd3095fafa2a5aba231)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsUrlFilenameConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04e9d3c910ab85893eabea366c2b376ba30b8d71f41f2595587d8623f178acd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsUrlFilenameConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288851e82df418d64cc818e0cfc8886c6b092dbcd28cbbafc76594eb6c4f5c48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ac4aa2693fd20570471ac0ca3bc1d130b72377883f202a1896fdf2a1e7016f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48352ff0c40e06648e3f867a7b6f152cf4c046fd3c421581ebe5b1fb967bc48b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlFilenameCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlFilenameCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlFilenameCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1ce8763ad8519bebc70bf578cdeeeeba5d8f00e6dbf21cca8e120dee856a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsUrlFilenameConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsUrlFilenameConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f964c73d82917a436197b4997bdbb3186ee1bf3b95e4953e325ef11acc77ba18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f1186a543da793efc708e68ea8f7d8a8fafc286d2c442e1a75bd67143ef8faa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2ee246c2e6a6e31d56717cb0f185e133ba6eacdfd57adbda72763cec16ebcdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe25e03f9f41508b33d130c9e4d4668d450f4c1b7be3b7b371ed63c72902475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d5a728245fee81e0126c75b0a3383182516f34f0acfacdcc350342652293f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlFilenameCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlFilenameCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlFilenameCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceef60eeffef7cf0713f68ff6244ba32239a44fefc4c68b67df92a308ac22d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsUrlPathCondition",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "match_values": "matchValues",
        "negate_condition": "negateCondition",
        "transforms": "transforms",
    },
)
class CdnFrontdoorRuleConditionsUrlPathCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.
        :param match_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.
        :param negate_condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.
        :param transforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d800eae78ee5699d187000a25555f9005170d1b26b8464aef67784a4f2030e8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#operator CdnFrontdoorRule#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#match_values CdnFrontdoorRule#match_values}.'''
        result = self._values.get("match_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#negate_condition CdnFrontdoorRule#negate_condition}.'''
        result = self._values.get("negate_condition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#transforms CdnFrontdoorRule#transforms}.'''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConditionsUrlPathCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleConditionsUrlPathConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsUrlPathConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__975ae5d67d585de55d3712d3efebb9d4fd239adf38cbdaf2b51de7b1066f67c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorRuleConditionsUrlPathConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__766efe761bfb53451fe5eaedaedef82d03d0b11735f059f39e2de36fda5b2b69)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorRuleConditionsUrlPathConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96fa6e9ace6ef26aacf0f4c74024c92915b0c614d0d70e877eee986e5c64f71c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa4e84c464476be24ef1534e19179bd7c161dba9ab59f2535f689e6732fe0d91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff0a7ce0c1b59f8819dc2b30c7b20c34a5d39d73baf3e50618058ab2dfb27c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlPathCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlPathCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlPathCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa32009938b4cb2c8726a64434c77407bfe09b71dd438b9fae929f3778ee9f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorRuleConditionsUrlPathConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConditionsUrlPathConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20ec2b5239e2bf29b529c4d376cd8390c76703c43ee47c85ef8a3aaf90c37a55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abfc810ce01de970b8bfd516e6104e6765b6c1c5e12ebce58bdc9cf1d7ef6527)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5baa923b9035ed17ee763ccd72fbad1ab0bfbee3c5234455e747942dd2014db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b121cb26aaa3148547aef55d86ef93e66d49edf557ae2213cda16122e9813f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transforms"))

    @transforms.setter
    def transforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819b5eb53420418a9a346c3920f29878585ef9968aef40ff22caa8f2e93229c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlPathCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlPathCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlPathCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c117eaf616f7ec412796a713a71225cc9a3421259f389dff9a14bf18fc57f40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "actions": "actions",
        "cdn_frontdoor_rule_set_id": "cdnFrontdoorRuleSetId",
        "name": "name",
        "order": "order",
        "behavior_on_match": "behaviorOnMatch",
        "conditions": "conditions",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class CdnFrontdoorRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        actions: typing.Union[CdnFrontdoorRuleActions, typing.Dict[builtins.str, typing.Any]],
        cdn_frontdoor_rule_set_id: builtins.str,
        name: builtins.str,
        order: jsii.Number,
        behavior_on_match: typing.Optional[builtins.str] = None,
        conditions: typing.Optional[typing.Union[CdnFrontdoorRuleConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CdnFrontdoorRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#actions CdnFrontdoorRule#actions}
        :param cdn_frontdoor_rule_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cdn_frontdoor_rule_set_id CdnFrontdoorRule#cdn_frontdoor_rule_set_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#name CdnFrontdoorRule#name}.
        :param order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#order CdnFrontdoorRule#order}.
        :param behavior_on_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#behavior_on_match CdnFrontdoorRule#behavior_on_match}.
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#conditions CdnFrontdoorRule#conditions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#id CdnFrontdoorRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#timeouts CdnFrontdoorRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(actions, dict):
            actions = CdnFrontdoorRuleActions(**actions)
        if isinstance(conditions, dict):
            conditions = CdnFrontdoorRuleConditions(**conditions)
        if isinstance(timeouts, dict):
            timeouts = CdnFrontdoorRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a04c1e68881e0dac070e5d95bd6d2e6f350ca3fc7d7385124a0240db6b61b2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument cdn_frontdoor_rule_set_id", value=cdn_frontdoor_rule_set_id, expected_type=type_hints["cdn_frontdoor_rule_set_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument behavior_on_match", value=behavior_on_match, expected_type=type_hints["behavior_on_match"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "cdn_frontdoor_rule_set_id": cdn_frontdoor_rule_set_id,
            "name": name,
            "order": order,
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
        if behavior_on_match is not None:
            self._values["behavior_on_match"] = behavior_on_match
        if conditions is not None:
            self._values["conditions"] = conditions
        if id is not None:
            self._values["id"] = id
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
    def actions(self) -> CdnFrontdoorRuleActions:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#actions CdnFrontdoorRule#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(CdnFrontdoorRuleActions, result)

    @builtins.property
    def cdn_frontdoor_rule_set_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#cdn_frontdoor_rule_set_id CdnFrontdoorRule#cdn_frontdoor_rule_set_id}.'''
        result = self._values.get("cdn_frontdoor_rule_set_id")
        assert result is not None, "Required property 'cdn_frontdoor_rule_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#name CdnFrontdoorRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def order(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#order CdnFrontdoorRule#order}.'''
        result = self._values.get("order")
        assert result is not None, "Required property 'order' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def behavior_on_match(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#behavior_on_match CdnFrontdoorRule#behavior_on_match}.'''
        result = self._values.get("behavior_on_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conditions(self) -> typing.Optional[CdnFrontdoorRuleConditions]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#conditions CdnFrontdoorRule#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[CdnFrontdoorRuleConditions], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#id CdnFrontdoorRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CdnFrontdoorRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#timeouts CdnFrontdoorRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CdnFrontdoorRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class CdnFrontdoorRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#create CdnFrontdoorRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#delete CdnFrontdoorRule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#read CdnFrontdoorRule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#update CdnFrontdoorRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f113354a11666625757e5a04dbae4d323c666e335752973ebf539340e382db16)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#create CdnFrontdoorRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#delete CdnFrontdoorRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#read CdnFrontdoorRule#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_rule#update CdnFrontdoorRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorRule.CdnFrontdoorRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21e0fd14260f3a685a42dc3a250ef69ee617544481d153a39b1f29c6c5c94ea0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90cd4ded2c15dd2bc980e9b2b6d800333c80156a0a2ddbdd7fb4343c5fe584ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c114b14ca996c9ea04ee15715f4dc800f6211b917ab59d4bed5fad8f80db82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a42a0840737d178216f77adda8eae73b8a9497ff8b1a871cac1ccda0b31856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe6b9ae54a27171984b5be3282870933d629fb89b36f6344dc4ace9d7b66aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7e40aff06cbb06f758f6754f0f5282cbc89f44ca7b0549fa3c347d08f5220b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CdnFrontdoorRule",
    "CdnFrontdoorRuleActions",
    "CdnFrontdoorRuleActionsOutputReference",
    "CdnFrontdoorRuleActionsRequestHeaderAction",
    "CdnFrontdoorRuleActionsRequestHeaderActionList",
    "CdnFrontdoorRuleActionsRequestHeaderActionOutputReference",
    "CdnFrontdoorRuleActionsResponseHeaderAction",
    "CdnFrontdoorRuleActionsResponseHeaderActionList",
    "CdnFrontdoorRuleActionsResponseHeaderActionOutputReference",
    "CdnFrontdoorRuleActionsRouteConfigurationOverrideAction",
    "CdnFrontdoorRuleActionsRouteConfigurationOverrideActionOutputReference",
    "CdnFrontdoorRuleActionsUrlRedirectAction",
    "CdnFrontdoorRuleActionsUrlRedirectActionOutputReference",
    "CdnFrontdoorRuleActionsUrlRewriteAction",
    "CdnFrontdoorRuleActionsUrlRewriteActionOutputReference",
    "CdnFrontdoorRuleConditions",
    "CdnFrontdoorRuleConditionsClientPortCondition",
    "CdnFrontdoorRuleConditionsClientPortConditionList",
    "CdnFrontdoorRuleConditionsClientPortConditionOutputReference",
    "CdnFrontdoorRuleConditionsCookiesCondition",
    "CdnFrontdoorRuleConditionsCookiesConditionList",
    "CdnFrontdoorRuleConditionsCookiesConditionOutputReference",
    "CdnFrontdoorRuleConditionsHostNameCondition",
    "CdnFrontdoorRuleConditionsHostNameConditionList",
    "CdnFrontdoorRuleConditionsHostNameConditionOutputReference",
    "CdnFrontdoorRuleConditionsHttpVersionCondition",
    "CdnFrontdoorRuleConditionsHttpVersionConditionList",
    "CdnFrontdoorRuleConditionsHttpVersionConditionOutputReference",
    "CdnFrontdoorRuleConditionsIsDeviceCondition",
    "CdnFrontdoorRuleConditionsIsDeviceConditionList",
    "CdnFrontdoorRuleConditionsIsDeviceConditionOutputReference",
    "CdnFrontdoorRuleConditionsOutputReference",
    "CdnFrontdoorRuleConditionsPostArgsCondition",
    "CdnFrontdoorRuleConditionsPostArgsConditionList",
    "CdnFrontdoorRuleConditionsPostArgsConditionOutputReference",
    "CdnFrontdoorRuleConditionsQueryStringCondition",
    "CdnFrontdoorRuleConditionsQueryStringConditionList",
    "CdnFrontdoorRuleConditionsQueryStringConditionOutputReference",
    "CdnFrontdoorRuleConditionsRemoteAddressCondition",
    "CdnFrontdoorRuleConditionsRemoteAddressConditionList",
    "CdnFrontdoorRuleConditionsRemoteAddressConditionOutputReference",
    "CdnFrontdoorRuleConditionsRequestBodyCondition",
    "CdnFrontdoorRuleConditionsRequestBodyConditionList",
    "CdnFrontdoorRuleConditionsRequestBodyConditionOutputReference",
    "CdnFrontdoorRuleConditionsRequestHeaderCondition",
    "CdnFrontdoorRuleConditionsRequestHeaderConditionList",
    "CdnFrontdoorRuleConditionsRequestHeaderConditionOutputReference",
    "CdnFrontdoorRuleConditionsRequestMethodCondition",
    "CdnFrontdoorRuleConditionsRequestMethodConditionList",
    "CdnFrontdoorRuleConditionsRequestMethodConditionOutputReference",
    "CdnFrontdoorRuleConditionsRequestSchemeCondition",
    "CdnFrontdoorRuleConditionsRequestSchemeConditionList",
    "CdnFrontdoorRuleConditionsRequestSchemeConditionOutputReference",
    "CdnFrontdoorRuleConditionsRequestUriCondition",
    "CdnFrontdoorRuleConditionsRequestUriConditionList",
    "CdnFrontdoorRuleConditionsRequestUriConditionOutputReference",
    "CdnFrontdoorRuleConditionsServerPortCondition",
    "CdnFrontdoorRuleConditionsServerPortConditionList",
    "CdnFrontdoorRuleConditionsServerPortConditionOutputReference",
    "CdnFrontdoorRuleConditionsSocketAddressCondition",
    "CdnFrontdoorRuleConditionsSocketAddressConditionList",
    "CdnFrontdoorRuleConditionsSocketAddressConditionOutputReference",
    "CdnFrontdoorRuleConditionsSslProtocolCondition",
    "CdnFrontdoorRuleConditionsSslProtocolConditionList",
    "CdnFrontdoorRuleConditionsSslProtocolConditionOutputReference",
    "CdnFrontdoorRuleConditionsUrlFileExtensionCondition",
    "CdnFrontdoorRuleConditionsUrlFileExtensionConditionList",
    "CdnFrontdoorRuleConditionsUrlFileExtensionConditionOutputReference",
    "CdnFrontdoorRuleConditionsUrlFilenameCondition",
    "CdnFrontdoorRuleConditionsUrlFilenameConditionList",
    "CdnFrontdoorRuleConditionsUrlFilenameConditionOutputReference",
    "CdnFrontdoorRuleConditionsUrlPathCondition",
    "CdnFrontdoorRuleConditionsUrlPathConditionList",
    "CdnFrontdoorRuleConditionsUrlPathConditionOutputReference",
    "CdnFrontdoorRuleConfig",
    "CdnFrontdoorRuleTimeouts",
    "CdnFrontdoorRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a2268aa325ff2d82b50d992b41253454ffe96c9762c180f3275fef650dd5cffd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    actions: typing.Union[CdnFrontdoorRuleActions, typing.Dict[builtins.str, typing.Any]],
    cdn_frontdoor_rule_set_id: builtins.str,
    name: builtins.str,
    order: jsii.Number,
    behavior_on_match: typing.Optional[builtins.str] = None,
    conditions: typing.Optional[typing.Union[CdnFrontdoorRuleConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CdnFrontdoorRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3d5b53a33baa223fdc021eb286aa0dff64d1c7628c61a228e53f8d899cef51e8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1609b117431c30de3134cd2c0cf541dc53a070fd2ecfc193746dcbae89446e57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e14accd8e89951d486e0cbaa3beffb2ce1d0aad4484f684c6f8ba4d8c23c749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cdad9f5c828b85dacc1b064d299b567d1e5eb8faeccc7d8e1294fb201fbe7c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5063eb378353b11cfceb62c1882f42deafba16829b082ed64534dd1978ee4eac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571f55b54e60245f4fc1c8f7d542760bfcfb472d6574e1b52e405b436de405b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e02a16d19f77978fee90a665cec94560e7c1d6eae0ab5660dbc1ba276d9ebb(
    *,
    request_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleActionsRequestHeaderAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_header_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleActionsResponseHeaderAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    route_configuration_override_action: typing.Optional[typing.Union[CdnFrontdoorRuleActionsRouteConfigurationOverrideAction, typing.Dict[builtins.str, typing.Any]]] = None,
    url_redirect_action: typing.Optional[typing.Union[CdnFrontdoorRuleActionsUrlRedirectAction, typing.Dict[builtins.str, typing.Any]]] = None,
    url_rewrite_action: typing.Optional[typing.Union[CdnFrontdoorRuleActionsUrlRewriteAction, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e961a4e5e595ca7460e869428c2fcb8110b4bc907bfc35429fa5845e2056869(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432ab9fb92d94740e93bbab862ee0fc611638275180fd7b2dae2d27182943c56(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleActionsRequestHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605dee65c7fa4b004111f5bc229593ec3e0cb5accfbd6678b0f26714615b2d27(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleActionsResponseHeaderAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8523ee5daad37abf47180dc32824a53ad470f732642d3d871857de16821d49e(
    value: typing.Optional[CdnFrontdoorRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0732cb25f89b7e163f3d45f4ce5400f00f8377293314348b682878135439ef2b(
    *,
    header_action: builtins.str,
    header_name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122fa70802e93870e117a5d4443bca5673763b39376e6097e3a14ba89c4a3e52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb7b951eef5135e02c86564cb4338c002e2c73b28c6926afce3bbc0c0c927b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2bda23502605075ac075180d32c04b7c52c7b91ca3f75518a608adfd5b0144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88620130a32c1aecb3e77c2832667cc8864019e2d385d5f26fc971abf25d500(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8eb68a859a96766bc6a7359d335e3e8a5f5b8a801ea3653a02dc9ecf4484c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bd7954e01c6a429ec147b1711e21aaa5d86efad7d2db105100f83038e102ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleActionsRequestHeaderAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986b57257ce32ed1aa450db912c6ae84739bf0f769fe67be22943106137f620f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c83b391b8b0656cd52f4276551f1a7d1d2658249b9b7368935c2361ba4695cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b1568febb44cbcba9b46a78c597fed40bb891e75ee335226a8a2794931a53c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f1a73a73ed6c95b248bdab39cc7629a24f2f6ff077e08d1194027e286a2b27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc51ec55ddfbe567e764fed765b9a3e4bddeee91d44248189987bf1baec5af35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleActionsRequestHeaderAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ad25c76ecfd49128dfe0aafe7b46b8e06dc7017f10fcdc22162feeb6fba1ff(
    *,
    header_action: builtins.str,
    header_name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074452e35b096e9bd0be4916ca1ab15c1c27f9297f4963908baab9bb862f6048(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28df99dd68f6a8b49e3a2f08d8c7aa07dffdd929ea999940a6fed6ad37447ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c513fbb26e9ef63d8059f32148600a552cf1385b3f8fabf3691133f029367a00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da90663ba9f3b702c2849b70ebb63faf83320307b3da630e19a2d646f774ed70(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8110889c5b72eafd43e2dafab7b0b00c730e5dd383e5e38dfae76a72ea2d8bb2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2cd5c03aff56ab7bd216e9535e8e1d2e1744aa5ce51f47cf4ed9f02b2356381(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleActionsResponseHeaderAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f4a60bcad46a46e54a3d8d519bb9349023a08c261d69acf388e3c82f2a13e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fbe88e09bedfc3ffd8832a84d2c54ed77d18c71c0a1978f8fb5393eb1c0674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d447c5a29975cbd2a7b6235060adf96a22c698149dae5e67d9b07a62c139c3d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de1b0b60cb8674abe9b7b9e511fbb3b3f67db624d048a888d5df60f324f96b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499446ab28869fb7015ee852fb9b7fd4afad65da05c1c1301600efa78ee070d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleActionsResponseHeaderAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bff1a4d8ab71cb7be41e9d6f3ae1b1cb89fd50c1340ebfeaa33c659f8acdc86(
    *,
    cache_behavior: typing.Optional[builtins.str] = None,
    cache_duration: typing.Optional[builtins.str] = None,
    cdn_frontdoor_origin_group_id: typing.Optional[builtins.str] = None,
    compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarding_protocol: typing.Optional[builtins.str] = None,
    query_string_caching_behavior: typing.Optional[builtins.str] = None,
    query_string_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b64df89678c6c0957a24603804488e4d863a89033e82208cc22e36d335c261(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b98fb5d60dde9d844464007e1ee18af15f3a527cb8376574e514d932e91401c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3428f7a96b433a2a5a44c5d7722658c37abfc5d62b78894880efeebdd2b5c5f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b7e279109fc52dcffea658b82f6c41c219dcd9bbba7efd66ca5fd9a1e88608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df40c2431de117dc52499c16271aca4031d58e9aafbe54cd44fd014bff724710(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8e8fabc3184f1cb1b93b541c2c265dec7153f945dec26f0399b5306a83bd0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b354544740a307b4c0371cea4ed759680b3455f4ebd8dcdc4ccb757f50c98c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18271e894b2cd0e0cc805427c57ca407aea13cb14a486ef7534ba10cc387d1a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e26f5f60318bc6b1ad59adadb98cf09940c32e7e422b4914c99b0460e3234b(
    value: typing.Optional[CdnFrontdoorRuleActionsRouteConfigurationOverrideAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b436a999aa515d56ba4b3322b0b1f581ae7d2a236add4486a5635b29c7b90ba(
    *,
    destination_hostname: builtins.str,
    redirect_type: builtins.str,
    destination_fragment: typing.Optional[builtins.str] = None,
    destination_path: typing.Optional[builtins.str] = None,
    query_string: typing.Optional[builtins.str] = None,
    redirect_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882adb3b59e1b10e18919b0effe7e9ab31ed9641180b022a31af3d3068c1d1da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c72194fafcaa15d627b40bd0106dbeed4309054dde538883a5ef836d9397b5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1945533de70b9c0868c8317520252f89361069e3fd2cb4b38b6a2364712213c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbf06384bffb129240be67af432013ee89214a4a248ded549602ad669b1b908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68ff960f2cac2921c2119b4a622194f61aaaa46760d1ab8b70bb90a202794e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3085d4955371010e98a25f988d5a4a3efeb7858bf7e1892b41d1b154d504c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929bd4b2d73dd08ccdf506ecf6ca5d23ed7c89e045071b4de981309d6168541e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aceb5ce3efac446bd27d35f610d60f124d57ca83509a39b935037daeb0cbc3fd(
    value: typing.Optional[CdnFrontdoorRuleActionsUrlRedirectAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa934f9848c2a60554d7ec59ad3a95bacb2edb6c868b0db614be2d062421144(
    *,
    destination: builtins.str,
    source_pattern: builtins.str,
    preserve_unmatched_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62713789306f66d32288f1c062b4497f3953d75c45f61955865439be30d94eea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5176ad265751802b4605bd6c1c7b57b262037695ebbd437f6ecb8a8de9bbfac7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74714aadfb7ce838ad6cad9b51fecd3febc86ea62ab78c140784068e5a04b7be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf7ec56c63488e953d48fd3e8a32cdc656b8165db063f8d62920a66ef59612a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf391bc197cfb3dae217d90d9d52560c2ac10fbe995cd0fe44fd32a1aadd97bb(
    value: typing.Optional[CdnFrontdoorRuleActionsUrlRewriteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d9dc83aa6d0243a218d6e3f2aff748ea87e7b633df4f7a65e4c2f44d52b0ad(
    *,
    client_port_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsClientPortCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cookies_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsCookiesCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host_name_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsHostNameCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http_version_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsHttpVersionCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_device_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsIsDeviceCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    post_args_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsPostArgsCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_string_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsQueryStringCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    remote_address_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRemoteAddressCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_body_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestBodyCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestHeaderCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_method_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestMethodCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_scheme_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestSchemeCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_uri_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestUriCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    server_port_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsServerPortCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    socket_address_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsSocketAddressCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssl_protocol_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsSslProtocolCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_file_extension_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsUrlFileExtensionCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_filename_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsUrlFilenameCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_path_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsUrlPathCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d157bfdbf3f48b33f5952b00f2513611b5ed91c55bad2b91e29b0a833d2656(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6baaebe9b3b8510e40fb18b30a68c02a03c484a20badde0a972819af109696d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b3cc31aa01a7f3cc9a094fee6c7cd73bb4b9a90a01d9ef1a03815a937a5f30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4e39d6a168f9ffb253f41ff579fe9a1b576e686a25d2c188eaa224abe51571(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a02129cb8f08e12f342dda7f553a8bc56e5efab1fd2b0c91dc9545ea1b0269(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc9407120e250fb1692cc86d53f908507e7331c5fe71b235294c05e61652931(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd7a112c28235cdcc5a75aa262a7d8dda2fa8724cfee772ac5321610be6d475(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsClientPortCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ad83e40b158a91447e985628268ca7b96c16e30a5182087fd18ec0be199c13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f308f9a4fb799dd691b3dfceb6a27514ccabb9c4971f1814cc6698b22929c2b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4ab1559092fd78005cefea691113c8a9e3b597f9bfdb531dc5b43011976c75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15dfb9962ff75c2174b0e6a3b2064963263055326b0b72f9c626c4d3d16d9496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e0964a3e8ca29c094288e0acf3e4ad09ee12745d585d5b61fb7531e80cf1b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsClientPortCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9438bd6d58c889b0f6557dc11e0a15ac8e27ab06a80bd23496330d667ea5f44(
    *,
    cookie_name: builtins.str,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a868a332bbad9ad699b0ab0bad64bb121bb791727c9b75e3012045e8fae2ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a2ca5b55ad8d9fc283c479e70b424b3840e45731424309e719abeceb91a069(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e986dfc13e42c3bda63e609f2ba91b11bd86f77c51b2656c284666607866fb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88878c64d3761f53c2c2ecbdeb5541e2c6efa826db1542be30b8db8f08f4332c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8a740eaa4c7ae4529577143176afcf744448afbd87263e5dc56cbc64c9c177(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa507111033c988dc44afa3663438009636166ce97fb6433dece02a6cd8892d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsCookiesCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9060fbcff7bfe47ad762e6535789ffe64d16f53e5eaee793e30a36cbb73f44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea267df04514276f736c92f07cb79f5d7c3949bb26d4b6f182790fd5bfdcef1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74bce4f3a0839d97e1996fc26e1992cbffd54908d5d9c0e76c590b5b1a718b6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e195bf21ac1f70d30bb3843e4213d7c363a023252a7db9c7b4de08dd448318(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fc11902b8a70c0fd092525944e540c6077ec48d89db28cfabb0ed5e440c2aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6953b32cc198494e9bfe5a48dea1a5ced4274e500f8dbf316aa8a3d6472409d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbd39bbacf9a04ea67fa736b86a226c0ea29c8b24a00d255bcfdb87df666aa8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsCookiesCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0efc2cc466b6ef7ccec360370c2c7d504590f01ac6958b7fc45c2353950b4f(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e2d32737b9642e1263bd6208fcfe0552f7d271dde237e6bc4c25901002f6ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5d70bfcee1906dc1045169bfb2815ccb9e1aaaebcaed2fabfd199f8a1b53b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c400dccf3b9bfa94651176d0c75734f49d7441d4007cd6f23d78ac60b3a007b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf493b6bee6e4ae3dc3abf73ae502dc85ede51b15374077bd1736d09ceb7ac79(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21c0faa36b44d7f26f427232c89bfb840c7a84ba9b90f641cc5e7ebfcc622c6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b70e7db5fba2f24d91bc89ce9a430c0112e7eb8ccc80d6ccec23c6dba741e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHostNameCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28367d0a593eda2cb4ce488a19173e62289bc7cef75cdaa520d9b83c3c11fc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d2ac631ba460674dbf97e0feff251e088fe87fd8a45e44917618e3d3ee2b42(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60f6714bf1b7cefb325736e2eccc27dddf452ef5a245242f05d561f2ac1be6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99384a7c7b932d6ef012f7055890c78265edbcc0c654c47dbeb3e9e96f20d252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753aaf839edad967fc0b5e1d20eba9c3f53a5ba91158af4fd96fda45327a6cfc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615ecbc0b8ed67eae93a8f59920c3d80ccdaa434d0b98ed8d8f41ddf9b0baf08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsHostNameCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef40d9d3f57e2533bbe22ad5faa597e5ec93ffbc58bb341070ea408e58b35abd(
    *,
    match_values: typing.Sequence[builtins.str],
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04941bd783b7081be552d47fb0e4a00e98f1ed19adf8a6845be55a6ea9bd81f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81cb69400367f2704e66935988fd84377d4cde62410463e085cc6f5ebc88b5d7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a9b354a6c9c5d8ac9e1615d570a02606ef32e94b534b0d99f00980f94ec3b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937acf85519a409a057de356dbdc25bcfb8d2036504027330e4706fad7553c40(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a929a38e5c23e963ccf35766c83d7189e1865e8f7314687aeb8e859f8a3983(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e97b2bf2d0492c3967f73dc0911f24a4f781d559bcb304566ed6b9e3af9e3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsHttpVersionCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c938e84fde41ae92d899f08dd284acd89d055dcc65d24cc9c5ec06f7b7b754(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1dbc26335591280a2ae0e983cd274d688621cc750f75f9a7cf6ad7dedd8bec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc93faf299e258f00d1ce59b424d1249c66867483383569f5e633f5ec1ee7ad7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab72ac9b68bfc4bafc86355aaa7ec452e9bdde02db88a0f7be1ac162a4544ee4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d31e655a7c14e4e1cd20e1af1a97cd18a0985f5d7cf3be4da1394b74df6bfe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsHttpVersionCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50710182b2216f73e20555a95019f78afc90bacb7d8b6af6d08ef30c23da02b(
    *,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344f840113a9fbd1c8eef5d703f68130415e0316cb3201dad70466d8b58fef1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3711bf8ac4ea4f02c3151e6bd399ae00be640aa3eaddc1038d6866bff90f251(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af088d6b1e58a0551ba673a69800af4ebd68b1b62f6cf07c8b0929e7b67c0c8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db3f2f14ef5244fb756d02246ac9f690b5b8a6c51faca56a3ccb0a16d5e145b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ac323c1d8118dea890bfd559d3780974ceda334d61530ed64c5f0e97cc6d26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d772e4938f0996669a8f2949f5cc4d5e073b5544441e376c55c69915415bc9fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsIsDeviceCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f27930a43df5c262c30d13381f4a449384de05c7e47a3e04ac69fa1e246236(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567098854a58a16f712a17098f4e11d74630d0303bfb7cd4c4d275664f337da5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9b52ed64649ad17a8654b12907b0f3e119cd9fe6e18f4831f585efebcc216a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058423b2d08db19b8b9715ce4a63f2bcd8225689f17e49237e9b9495943b8aa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4610de2f1554a069431909a20e7ed8776f4658ee98c6a053ab3c9a6a344f9810(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsIsDeviceCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3108b6cd1c282cf756c9505bf15864c7cd11ed305b70d4bdb7719d755cf53ede(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591b6aac9b62a7fc9362b81ff46adfc823c61028bf8e6e88cbb5b391ca58bad2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsClientPortCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9ce9084a6c9308bb4b03fd6a22058fd589ebb1be26ef1a174455ae4c7cacbd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsCookiesCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f46df871a8b3085e98b6124c0234135a9004076018339da82093fce2bbb915(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsHostNameCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556feabeb891b4794ceb404f20ac58c76b0648401e6a523756f68a55f3ba7f40(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsHttpVersionCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc72187460f63abfc3a723ae35047037a3768b5668c85e8af630669928103db3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsIsDeviceCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d6a93b5b5fda0506bb4c9f8c4cafc8614b1701d685c598cbe8da21141ef959(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsPostArgsCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a989343576d1adc4678924a84ec810ec5f2d43505f91333c16628e1431375248(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsQueryStringCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535920147775bff1e1b66ff9883acd47487745d2175312fc7c5a15e50d666830(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRemoteAddressCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80239b468ee20a2ef0018a83fd838b3ea85f45af5cbffaccf844b1fccedefb74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestBodyCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d79eeebd0c52e36102d4895f0cc0a8b19b7a80a046b0f47843e8d9eabb018c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestHeaderCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7963da5f4bcc54412e3b61c00fa79ab8cfdf712cbaf53967fbd7382c2d4b86(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestMethodCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec26aa8b87ae5f49973e1cbe3c88101ccc32aafd3d0c5566c234695993efee14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestSchemeCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e837ce8c5a0dd4776c8f7f5bfeb9f35d5c57a6231f5f5c4d265f6ac5f477166c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsRequestUriCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325a728fc9b59b420bd562aa4a9561dfec9385faf264cbc28f6e4ffc01e17e83(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsServerPortCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b08a9d2bdf36b21c08595975a7ac053d77ce845957108836c4096939ac4266(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsSocketAddressCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d30aec142702e59fb4575beaeb58656890b36a455f4862d75cd48293017bab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsSslProtocolCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71daef5621717b9f3d74f10ff4f0d0fac4a1b3463238b9f970f117372c82d554(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsUrlFileExtensionCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ac896651e0f52b965845989c58ae4ea4759a76e3335411c132e9777ee42ce3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsUrlFilenameCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299c6f4248a47aca61e307afad5baab5ff5f07801c4765d925d50450745f53a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorRuleConditionsUrlPathCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91d54a9404274751a129441c6a4561399a837611c433ab716b50144f7cad67e(
    value: typing.Optional[CdnFrontdoorRuleConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0358b8e8bda4aa95004010080528e88b7697adc4b41454718de9374087ffe67(
    *,
    operator: builtins.str,
    post_args_name: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842f9106e00b155095089c6f8ce1793fc86ccf2d9f9320f9fee985c243baa428(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f05a3d089ac3c2dc3fa36a1df472a768b3dbd9f59acabe93a14b31b7fb14bf9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e362845a4f1b52b36852cb4a78bd5813782f8a61567db389a6d1dc10ab3f7250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8319819291045868b1bcffdf515c1e8dc53c44b49dbb8291a94eabe36a119726(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3317431e53c99cb896e88aa389429f77ef05a1cb7df40163b8dc61601a60feac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8f3a8619bf6202a2842ea41f64f3377f3c30fefdad490d19d74404e2917e8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsPostArgsCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc8f01950ea7c5f7dd23c5eb4cdde52033a46ff71084bd851ef8ecce726d58c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40fe3e8f1a0da806b5e8689f18851129f6503e16bd4e21d52a214bdef91543b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7521c78be677d8784602235fc46bc1a0f30758767b24e448f68a8f14840fed0b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ad23321f71e3f1ab8fa6368a2a770267e03ef0f94fef31e53accbaf12f111e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70959ee00a7477627ac46f66afc32ae50c87e36d93cf864b8363579c6fef555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5012f1205baead8e1b518fa374a07a74158dd7948b592cc835ac36c73c1f83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ad0f935e7dd4165db772427eea1a06ba9eba2f29583b86a1d0076923a09560(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsPostArgsCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fab626d8b3df13a80304fdfc2164cb6770666bdc7dbbb6becff14dc5d5405c(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16f0ae3ad1b88b5f668b9747490e0df503a585b390a18c31c055af168a0a3cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3cc773b5588f3f533213b06511a1aadbfb12b317f8aea5dd91a78fe44e3da5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606c4ea895217f9d19de65f8c180326a15404f1c4dce6928eacd6bde0c28b5d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67da620429bcc7fc5bd296192ed90b50d997814d3c804328ca31106bf66571ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568ddcdff0800668c3f5baf9983cd9546d3ef6e63d2217d7c9550ab86af7f304(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4166f168c029504f759aacc1297449c43c7bec41f03dd23d43961cb294b6dc4d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsQueryStringCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5b6b2221f91af8813fa286921119292e4d2692c3a7a46a8edd6148899e2770(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5592d1b12413822cdd4b69b948b5f5473268eef3bf2b76c6ea7258d705aa52cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01547b8c4c4c700a75969c34b5ea457172847629f161976ed5ca3de98513022c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eaaa4a64a80ae2bb92f7ed77bae60d1f2b74c5b8061898289910058004787f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2540d719cf9ef9c8a68cf637a9843569f80984c54f169c53ecf2133014c33c42(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8f45dfe0b4fe180dd58803c24630670cc64a106d4812ba8ac4d2b695a7e78e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsQueryStringCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758430c1cb1011ad9f1ce1bd0fcb51ec025db1aac2a2eeab72f481f9a194139f(
    *,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5b8ff325b7c8bfe9528f268766e63fda00e7650ce6fbf51a4c8ea53917e51f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4ca3b3f08e44cc5a5a2397c0c24eae069ef9014aae0c1a57c887b05ca0bda0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2758464286b39f56e28a7bc07d934da0486bd9a871a3375399c160ab62ac8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d070caea60b506b14d59beba39ef66065a144c43e6f3f8786f784303bdc8bbd5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce9cb3b78ca176c5938b754085e58ffad208cf9644fd2b93cfc378940299901(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a42281c31dfc4dfc43ec6f5cedef5236d4ddabe9be788ed668fbaec3bc49ad8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRemoteAddressCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b30fc8a1a229a4d16460d92da1fa9498c9a596a38868f621bf78da011aebfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432974a32f6ddcfe711ddcd60c1641198f3ff6e9e3567f7fb36cafce58ebe042(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b892bd06f410086774a4fa835c43413d17129e657335353b0ad0782cb2bb71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7258bcd724e6d02d5d7bbc5a43254e89e858fea190b48922a56918fa887b1f2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2968fcd4a9d5e8c3a044df794687e987d890112805273e0b06dfc2db84302e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRemoteAddressCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e065db61395c1ec35598682cfaf909d70f69859abab42f915ed930583461656(
    *,
    match_values: typing.Sequence[builtins.str],
    operator: builtins.str,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2158f433394568cf1753ca60dd57bdf31493144863179040258d114afdeccd76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2bc8fadf48ae2917ca46943971041137334c3b8c22f3e1506ddb18d19987878(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5671908fd5a9d1a77c13fbb72413cae110387291e1fb3a452625339f81916f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824b2e308de7469624024aced6dce7c2600e376cf011c3ef1c42befe3d2eba75(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aae5e5f3981d5d322ee6415c69bcb23373ea63c8467b022e375b194a12c2436(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82ae3afaaa9eeb92ba239c4f231475311476d28502394c0b510a7002b4a0ea0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestBodyCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06884059447b68defc8602f220e434169416e926ae179ebc1d8abd0160253c79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90cd1e6de038f6f01fd9f846a46db66264554e583f8377ebd8e7bd7701ace30(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26b6da0cb074508eea11362b951a9ee5a5e0af8eaed2f6e59799e87b50fbb75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d210c31210f27b717a9722766dbc1107daaa33d3e91094b4875fdb7bf3fda1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9481b0906899ead32632a15d89df808889eb13dbcde2d22bb256cdabdc39a57e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0aff95821be05f436e9595c36f3db27b1f3e74c658b2e833722edc5d308785(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestBodyCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a3763b40df51da402fe0493fd72ff31a4b44e967a948f475c0bbdc0903080a(
    *,
    header_name: builtins.str,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec3be5c37a0a372038dccc502a3dcf3b7024e3d2bbf9033c601c430c222c2e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74064f43ed90d52da8f44aa7f2460b5b17705d047cc1636ef1c3aeb1cc858354(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c213162894369e6215814637af027224e8c9297297b41336948002e2a5fac22c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503154be7bd6ac32d9d273fb66e2124b494c82df83445a15f43ee2333edf3999(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f122fa3eff8b88807f6788ae94329aa0936fb633ecffe30559c15d01a720a49(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115063ac0613a37303f098da5a797e0ce596bb94c270d38e0598be0449851703(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestHeaderCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ec9320d533953bfcbd696b16f941ad22f213fcc312d3f3f588a9977d1c2205(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f36537890b4aedd04e18cbe07bfd7d3166bce49a5e64d0a2dec9c9603080262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba284bfd2189df484462978eb366abbd41d1a9d6e5bc7c6b8ba909dc5460e5c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fc11781967cd9d7ff9892cc3e350d43618bea2f563bacc4ecd72e11a8f0f53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e92f70e12ac856a59dfb914cbafb3d320d76ce7b16d045281bfa9d1ae30286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4341b3640ad8b80fb774cbcbf1d963b9cb977d1dcbc0339999a2cc2d6e96d3f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8e714b34ebeba1fcd2055f3bd3dffb1a779575370314fea8f0171212ca8ea7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestHeaderCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb6101da2e465131beed5928ca9e008c0435b5cb3af0c272db489a182de5edc(
    *,
    match_values: typing.Sequence[builtins.str],
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3e209e561cbd707586b2089285c512330c77bbd692c27dbf489809ed923d49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a1dab8cdd818c6ea962c3f81677b88fd60c89d41f8eebe396cecb81dc650ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b64660dadc055287fa67878f3ad12b91df720dc2189ba51dacfd13b3d758c78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3658157a1d9fb063a55af0fe5eaecde4646203d227ca86dbf039c7bdb4d962c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24b4ed45dca67095f22b9a0a19179d81c6b6b85f40826f36269b51ba48dc2f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8cc7584832357cb5978a0472d235c09d041d1c4546be54756e4f293f1aff07d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestMethodCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca670f56a3bba3e7e4495a07a2ad48d40152d2da12c1299ca1e323c73d0e2373(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a8fb115cda44596397133165c25e3dd38f2ac6ca193c7eb3f8bf69f6a12331(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dac623e9f26bc7b22c8d2bef2c794629160505203cf67506806046314952f76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3590b6a8597bec05c472624c03459fbef3e88f3b03ae082f6a2bb6a36aed08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172524e2842efdb24ad6f4e9207841ba82bfacf5544907c20e6881bc388eb45c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestMethodCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebbcc27bd5f87cab032bdc32adea1c1ea5717f48a926bdf2ac73d723163e36f(
    *,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d925de4121aac4d8553882fab5a568e7ff90029a135d0b53128f8ad22633ef86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8775ce572a1156bec68691c8cf78036cde1be4a194629c301c83af745429226(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138b16a25b96e16902fb64ab9c325c7f66feb6652b6cf0ad1b46d5d4c15d1e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60e2d16010eaf9b20cebc12cee507de32d9705947a0e7edaa461d34f4da9985(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7b3eecc8b5f9f7bc4e196bd3ada8d93ee668be709c75235e1fbc96d98596f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6aba6939dc15c5f13c1323b9087fff7b5496d8f243ea3c31ad2fef0d7643349(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestSchemeCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9090ac47d8b80a3c4a0d7accd3cf60cda0467e3112802b033fb661f4284505(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cc51d604e826b33614abe614d2946005d4269e1add94dbb8fc0df38af442a8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163f9d51630d9ace98684be008f2e9d2511ae3900b5da9a3866faaa19ef0f7b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9455784df542412ab1c8064bd8f742dd63c0ac335f5f37d76adb862a41dc36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ed5e96558109e7ac7c4e20cebda16126fdeb20ce00f3d57c83ba3197132c47(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestSchemeCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a651a9d7d164bb6c9602600334c291acf1a63caa6be457bbad79bb23e1692e(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b9fe7efcfec0dc28f04de4ca280c6f29d9b45d9b062fccebc9f8fe7528a37a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5701a9a2a312a792b971aef402120bc6dca7ed221bc9ff31004c7cfac8979a1d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e82b787129c80cc7959d185601ea97f3e6e8f134b4ec924591c43d2eeaf2b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a1158c4b4cee2fec8ca9bf6ee37342452424274c09dc1b135225363bfeed75(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128cf93fecefab0b2f8999e219eadfae5409674f0fe860028a4698b1a0631452(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c3ee7aad2a29f87655e4dfce9a51efc0be3f623bf5e30301c90bbb419788a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsRequestUriCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9403b8c466a232dee50b1e2e821ec9cc66986c9df20d7f403182d434714a01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc89878df70ee64fd889730767b74c36cccb5f22175b9e4d039a7b30771d0a1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5695d3ef346a5a55f753bb128f9764f0eaca9f03387fa89dbac8e30ceb10b9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1adba2df60eae66414699de7ef066b8f6aaa82aa18eb88d21d5bfefd2d4f4b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8c3ab065453b0c609069fc9e7e40555da433c6c24b9bb0b351f218a3be1847(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c01a6bf1a91d83bb660c8f82f1363a6eff270e1a07a0175e600ec2b7c2c98c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsRequestUriCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235b1c794fa6f0eda0ad61e2af68606691758ba6b3643a970f9543fa10e234fb(
    *,
    match_values: typing.Sequence[builtins.str],
    operator: builtins.str,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b336ae668d16bb74d33bac17197436032b3f161633acd7f8439482caf96b37f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd2757a10e20b62888f110d2a5e4b5497bf0be07abc71c24037ebaac66cd316(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1146d3707a39f535d4a8301f3bb028d002f88726d4a5b5f99a2511174ff9d57b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045d448bcab075a86c07af6ebb568f25bed6bcbb733646dfa4e2215cad2b0fa3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec49880239afb0fd9de9fa4cf994fac6bf2730f39b7bcc12220e316efaa973c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282d6411e36c218bb9bbd61b9009021a6e303a1c06539b48ed6d4e621f557661(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsServerPortCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fee2dac34c7e9586957b8a857394b31cc2ac9755c0ae07e303c33dd080cc58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f3c6f5ed04787d52e70fc43a0fa97c0f206c0c2b5fcd9fdb2608160da0213d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2dba3639a22e1c531b2cab46b0ba9ae8b9ed0c6d7909ae91b8804c73382552(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb74ee4b54fbfadbddd7c1d4941e304151f45043edeecb61a3392a95900fecfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46f233746ce2bc2adf7f9e564adff56bcf1699d7cedab531ec68c63aa8ca832(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsServerPortCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c21f79905ad00bc6024575296c561f84daa2eb664c84b6ccaa5a779e96ec28e(
    *,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bccf8d1d787e0675060e147776c02ea2febfa7b8988aec9c510272c95e1e058(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665d5084fb1a944befea9d5aede741e5461c3e352db8cbada9a44a8769f25660(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20b751e6c3f22ce476068d11241f298ba6d820a2b2f87a74feb8c49bab2be00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438e81f4b6abb1fc8f604efaf1e37b9a9f285d9f91a9b0489c61d3c4a199ed07(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a754e11152bb3e1f68a9482b7751c2ccb42789c8a93b3a5935b340d03b85df37(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f6ddf27196aa6dd569ed60ffcc0001f8e7eea8636b947cc3f8245b7d791d79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsSocketAddressCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7bb15bfecf841cd1e16c1a9dcb3fdb3c70295a6875fa239fc6ec3edaafc87a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ff76ca2a47308283631452b4b761f3d0d15c03f10bc9536ec640fbc784fd7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4d25698aa1111f060c17bdab24ad65aeea88828558225864556cd26e2a18a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2485f2eaa97490500b6cb19ee699ad8371b0c6921715007a38bf064b4a95b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e1944fcf67076e5b11acb9ea36dfea952ec2263d84f581a7cd486bd9455239(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsSocketAddressCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e70ced3b779da4d9a50f06cf68ac34031f38c02e7023f2fe29a6df005451d9(
    *,
    match_values: typing.Sequence[builtins.str],
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401a3ebbdaed1f7b04907afc28741ea9acb4c4c9c375fef3c34a469cc433150a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d5697a363371fccaec0f88ee15bd2c4baefcf8237d6e8c6f454bde93c1cb92(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4906c2a965476231aaee92ea05813ca7a70abff7cad45e3ac23b52173a8149ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efc55b754296367a4b94190c6357e3df2e5f56ffb65be4d78df7cf08b9ea575(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d40e45262412e5c37a6f764d614ec7d77e7c8fc774b59ecb7dc58d309d85bbd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1df14bd495f2dd571674e20c08ad7e625556c46fb500898c03d93d6d7865f8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsSslProtocolCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf40e5e5e8268baf151038e040ca8fe4435b83d1614c78e6b2bf064175a7e1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45d22ecdbb95430e2ad6836f76c3f93c22bfa35d8b7e3c8a70a34d390405699(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b5c0a4c53420e91d2ab91cd77296d39089a9774b1b13dc3cb5cf94ee83ce6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812851b8bdef33d230e72aa73c7336507e5f829be4bbd83dae56e1ec23a2589f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077586d466c7394a82be9c270a0bfe36ec0b8cd003d606b422c408be02a727a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsSslProtocolCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66871cfd9441a698eaef46901a3dcf3ecc6feaaefd2c304b21b4be443f8ebc66(
    *,
    match_values: typing.Sequence[builtins.str],
    operator: builtins.str,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5115daaf7fd02f5e1038ee974577c16fa2fd0d43caea6b3e2f25d24838125d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aec7de9dcfba12da3d24c359331c2a6dabf1c4a1f9b603526bb27152db02602(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f912a4214a24c7f2a145550598944e0848f0d4375be67bfd90b6bda1003bb297(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531ab5aaa8b9ff046aec86cdbbe287ceb8a50373a30aad88d55c527d5121df05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76900d4dd78d72500e23e670b809ac0e4a97b18a5faed29b0e7cdb85673e748(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f50e1ff111c9350aa35e5073c0161ba9198cacb02c012da51756c5b2705a269(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlFileExtensionCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565d534bd163c0b27e4f9a1eb3c230634d9b40e9996d7561692c68e746243673(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da35c30749544b8cde652bff69bf1f98c26c021e77829c13efa612a154b6d661(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91eb46dd6ffb7d44c88149f826a3f8f5440f67049f44dbf55134b84a2f71c606(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ca0cdb60b030304892fa3ba56acd35e5a9c79e6ce9783fe0bbff167e608e7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ad90b2ce2dbfb0631269bed6239e1c87865d913c145b4ecd4bc8627d5b8d1c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a80580d3334857b254f5361692d9d95223413a892ec4521a3fa714624dd4b7eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlFileExtensionCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7323061299b4e3a3b42c657088947fd5fbf966153fe6663e1d92cb42d285ee4b(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571361d0894c987737a5e2904121cd55b4e899a58d020fd3095fafa2a5aba231(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04e9d3c910ab85893eabea366c2b376ba30b8d71f41f2595587d8623f178acd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288851e82df418d64cc818e0cfc8886c6b092dbcd28cbbafc76594eb6c4f5c48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac4aa2693fd20570471ac0ca3bc1d130b72377883f202a1896fdf2a1e7016f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48352ff0c40e06648e3f867a7b6f152cf4c046fd3c421581ebe5b1fb967bc48b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1ce8763ad8519bebc70bf578cdeeeeba5d8f00e6dbf21cca8e120dee856a4e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlFilenameCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f964c73d82917a436197b4997bdbb3186ee1bf3b95e4953e325ef11acc77ba18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1186a543da793efc708e68ea8f7d8a8fafc286d2c442e1a75bd67143ef8faa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ee246c2e6a6e31d56717cb0f185e133ba6eacdfd57adbda72763cec16ebcdb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe25e03f9f41508b33d130c9e4d4668d450f4c1b7be3b7b371ed63c72902475(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d5a728245fee81e0126c75b0a3383182516f34f0acfacdcc350342652293f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceef60eeffef7cf0713f68ff6244ba32239a44fefc4c68b67df92a308ac22d60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlFilenameCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d800eae78ee5699d187000a25555f9005170d1b26b8464aef67784a4f2030e8(
    *,
    operator: builtins.str,
    match_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate_condition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transforms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975ae5d67d585de55d3712d3efebb9d4fd239adf38cbdaf2b51de7b1066f67c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766efe761bfb53451fe5eaedaedef82d03d0b11735f059f39e2de36fda5b2b69(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fa6e9ace6ef26aacf0f4c74024c92915b0c614d0d70e877eee986e5c64f71c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4e84c464476be24ef1534e19179bd7c161dba9ab59f2535f689e6732fe0d91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0a7ce0c1b59f8819dc2b30c7b20c34a5d39d73baf3e50618058ab2dfb27c58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa32009938b4cb2c8726a64434c77407bfe09b71dd438b9fae929f3778ee9f60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorRuleConditionsUrlPathCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ec2b5239e2bf29b529c4d376cd8390c76703c43ee47c85ef8a3aaf90c37a55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfc810ce01de970b8bfd516e6104e6765b6c1c5e12ebce58bdc9cf1d7ef6527(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5baa923b9035ed17ee763ccd72fbad1ab0bfbee3c5234455e747942dd2014db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b121cb26aaa3148547aef55d86ef93e66d49edf557ae2213cda16122e9813f15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819b5eb53420418a9a346c3920f29878585ef9968aef40ff22caa8f2e93229c2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c117eaf616f7ec412796a713a71225cc9a3421259f389dff9a14bf18fc57f40f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleConditionsUrlPathCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a04c1e68881e0dac070e5d95bd6d2e6f350ca3fc7d7385124a0240db6b61b2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    actions: typing.Union[CdnFrontdoorRuleActions, typing.Dict[builtins.str, typing.Any]],
    cdn_frontdoor_rule_set_id: builtins.str,
    name: builtins.str,
    order: jsii.Number,
    behavior_on_match: typing.Optional[builtins.str] = None,
    conditions: typing.Optional[typing.Union[CdnFrontdoorRuleConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CdnFrontdoorRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f113354a11666625757e5a04dbae4d323c666e335752973ebf539340e382db16(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e0fd14260f3a685a42dc3a250ef69ee617544481d153a39b1f29c6c5c94ea0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90cd4ded2c15dd2bc980e9b2b6d800333c80156a0a2ddbdd7fb4343c5fe584ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c114b14ca996c9ea04ee15715f4dc800f6211b917ab59d4bed5fad8f80db82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a42a0840737d178216f77adda8eae73b8a9497ff8b1a871cac1ccda0b31856(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe6b9ae54a27171984b5be3282870933d629fb89b36f6344dc4ace9d7b66aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7e40aff06cbb06f758f6754f0f5282cbc89f44ca7b0549fa3c347d08f5220b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
