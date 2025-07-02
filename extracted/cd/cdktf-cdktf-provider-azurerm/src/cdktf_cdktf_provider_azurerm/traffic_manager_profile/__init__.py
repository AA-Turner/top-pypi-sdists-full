r'''
# `azurerm_traffic_manager_profile`

Refer to the Terraform Registry for docs: [`azurerm_traffic_manager_profile`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile).
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


class TrafficManagerProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile azurerm_traffic_manager_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dns_config: typing.Union["TrafficManagerProfileDnsConfig", typing.Dict[builtins.str, typing.Any]],
        monitor_config: typing.Union["TrafficManagerProfileMonitorConfig", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        resource_group_name: builtins.str,
        traffic_routing_method: builtins.str,
        id: typing.Optional[builtins.str] = None,
        max_return: typing.Optional[jsii.Number] = None,
        profile_status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["TrafficManagerProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_view_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile azurerm_traffic_manager_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dns_config: dns_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#dns_config TrafficManagerProfile#dns_config}
        :param monitor_config: monitor_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#monitor_config TrafficManagerProfile#monitor_config}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#name TrafficManagerProfile#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#resource_group_name TrafficManagerProfile#resource_group_name}.
        :param traffic_routing_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#traffic_routing_method TrafficManagerProfile#traffic_routing_method}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#id TrafficManagerProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_return: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#max_return TrafficManagerProfile#max_return}.
        :param profile_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#profile_status TrafficManagerProfile#profile_status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#tags TrafficManagerProfile#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#timeouts TrafficManagerProfile#timeouts}
        :param traffic_view_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#traffic_view_enabled TrafficManagerProfile#traffic_view_enabled}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7686a317afe6c1cd8affdf1f744f7c6c6733d8a2347c6bc90554bc69dc516fb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TrafficManagerProfileConfig(
            dns_config=dns_config,
            monitor_config=monitor_config,
            name=name,
            resource_group_name=resource_group_name,
            traffic_routing_method=traffic_routing_method,
            id=id,
            max_return=max_return,
            profile_status=profile_status,
            tags=tags,
            timeouts=timeouts,
            traffic_view_enabled=traffic_view_enabled,
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
        '''Generates CDKTF code for importing a TrafficManagerProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TrafficManagerProfile to import.
        :param import_from_id: The id of the existing TrafficManagerProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TrafficManagerProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf5936052999acb33613efc7139aaf565b189006d042670078cc49b4b8f07b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDnsConfig")
    def put_dns_config(self, *, relative_name: builtins.str, ttl: jsii.Number) -> None:
        '''
        :param relative_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#relative_name TrafficManagerProfile#relative_name}.
        :param ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#ttl TrafficManagerProfile#ttl}.
        '''
        value = TrafficManagerProfileDnsConfig(relative_name=relative_name, ttl=ttl)

        return typing.cast(None, jsii.invoke(self, "putDnsConfig", [value]))

    @jsii.member(jsii_name="putMonitorConfig")
    def put_monitor_config(
        self,
        *,
        port: jsii.Number,
        protocol: builtins.str,
        custom_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TrafficManagerProfileMonitorConfigCustomHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        expected_status_code_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        interval_in_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
        tolerated_number_of_failures: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#port TrafficManagerProfile#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#protocol TrafficManagerProfile#protocol}.
        :param custom_header: custom_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#custom_header TrafficManagerProfile#custom_header}
        :param expected_status_code_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#expected_status_code_ranges TrafficManagerProfile#expected_status_code_ranges}.
        :param interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#interval_in_seconds TrafficManagerProfile#interval_in_seconds}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#path TrafficManagerProfile#path}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#timeout_in_seconds TrafficManagerProfile#timeout_in_seconds}.
        :param tolerated_number_of_failures: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#tolerated_number_of_failures TrafficManagerProfile#tolerated_number_of_failures}.
        '''
        value = TrafficManagerProfileMonitorConfig(
            port=port,
            protocol=protocol,
            custom_header=custom_header,
            expected_status_code_ranges=expected_status_code_ranges,
            interval_in_seconds=interval_in_seconds,
            path=path,
            timeout_in_seconds=timeout_in_seconds,
            tolerated_number_of_failures=tolerated_number_of_failures,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitorConfig", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#create TrafficManagerProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#delete TrafficManagerProfile#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#read TrafficManagerProfile#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#update TrafficManagerProfile#update}.
        '''
        value = TrafficManagerProfileTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxReturn")
    def reset_max_return(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxReturn", []))

    @jsii.member(jsii_name="resetProfileStatus")
    def reset_profile_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileStatus", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrafficViewEnabled")
    def reset_traffic_view_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficViewEnabled", []))

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
    @jsii.member(jsii_name="dnsConfig")
    def dns_config(self) -> "TrafficManagerProfileDnsConfigOutputReference":
        return typing.cast("TrafficManagerProfileDnsConfigOutputReference", jsii.get(self, "dnsConfig"))

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="monitorConfig")
    def monitor_config(self) -> "TrafficManagerProfileMonitorConfigOutputReference":
        return typing.cast("TrafficManagerProfileMonitorConfigOutputReference", jsii.get(self, "monitorConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "TrafficManagerProfileTimeoutsOutputReference":
        return typing.cast("TrafficManagerProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dnsConfigInput")
    def dns_config_input(self) -> typing.Optional["TrafficManagerProfileDnsConfig"]:
        return typing.cast(typing.Optional["TrafficManagerProfileDnsConfig"], jsii.get(self, "dnsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReturnInput")
    def max_return_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReturnInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorConfigInput")
    def monitor_config_input(
        self,
    ) -> typing.Optional["TrafficManagerProfileMonitorConfig"]:
        return typing.cast(typing.Optional["TrafficManagerProfileMonitorConfig"], jsii.get(self, "monitorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="profileStatusInput")
    def profile_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileStatusInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TrafficManagerProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TrafficManagerProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficRoutingMethodInput")
    def traffic_routing_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trafficRoutingMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficViewEnabledInput")
    def traffic_view_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trafficViewEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445af9206e987f1ac49b2fe2d73a68e4b0f022d407a4474927c233ee37ede313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxReturn")
    def max_return(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReturn"))

    @max_return.setter
    def max_return(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea6ecd1ddcf5a39f1887ad58150084e42dab43cd219b3f88bd177c1a339122e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReturn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c2a76b67f56593f0d6e1e8e2f6b4dfb26ac331fd97b618e605bbe817d2c004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileStatus")
    def profile_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profileStatus"))

    @profile_status.setter
    def profile_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed43bb2c1a2eace71499c7256ca6b43badd0273a7d9520493d8b19140cde8dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db283c766c97cc04b71c8706f8fd18eec78066d45e566db3609b4a7838211036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943c5c15828f434385bd0881f1d631c6b9544df6b4efb9056c0082ff12d42493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trafficRoutingMethod")
    def traffic_routing_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trafficRoutingMethod"))

    @traffic_routing_method.setter
    def traffic_routing_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97577a635a6ef9c490c5451641d0432abf170aa9906f3dff98515b0b5d718ec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trafficRoutingMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trafficViewEnabled")
    def traffic_view_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trafficViewEnabled"))

    @traffic_view_enabled.setter
    def traffic_view_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ae5b8b00c034dcd750bf6c719099d6d6c907a29a29c79ced9b7424fa9ae233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trafficViewEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dns_config": "dnsConfig",
        "monitor_config": "monitorConfig",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "traffic_routing_method": "trafficRoutingMethod",
        "id": "id",
        "max_return": "maxReturn",
        "profile_status": "profileStatus",
        "tags": "tags",
        "timeouts": "timeouts",
        "traffic_view_enabled": "trafficViewEnabled",
    },
)
class TrafficManagerProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dns_config: typing.Union["TrafficManagerProfileDnsConfig", typing.Dict[builtins.str, typing.Any]],
        monitor_config: typing.Union["TrafficManagerProfileMonitorConfig", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        resource_group_name: builtins.str,
        traffic_routing_method: builtins.str,
        id: typing.Optional[builtins.str] = None,
        max_return: typing.Optional[jsii.Number] = None,
        profile_status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["TrafficManagerProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_view_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dns_config: dns_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#dns_config TrafficManagerProfile#dns_config}
        :param monitor_config: monitor_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#monitor_config TrafficManagerProfile#monitor_config}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#name TrafficManagerProfile#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#resource_group_name TrafficManagerProfile#resource_group_name}.
        :param traffic_routing_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#traffic_routing_method TrafficManagerProfile#traffic_routing_method}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#id TrafficManagerProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_return: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#max_return TrafficManagerProfile#max_return}.
        :param profile_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#profile_status TrafficManagerProfile#profile_status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#tags TrafficManagerProfile#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#timeouts TrafficManagerProfile#timeouts}
        :param traffic_view_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#traffic_view_enabled TrafficManagerProfile#traffic_view_enabled}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dns_config, dict):
            dns_config = TrafficManagerProfileDnsConfig(**dns_config)
        if isinstance(monitor_config, dict):
            monitor_config = TrafficManagerProfileMonitorConfig(**monitor_config)
        if isinstance(timeouts, dict):
            timeouts = TrafficManagerProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6792b35fc30d60c728d6ca609f9a4e89c1e9f750bcda3095fcb3651b2bd3f60)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dns_config", value=dns_config, expected_type=type_hints["dns_config"])
            check_type(argname="argument monitor_config", value=monitor_config, expected_type=type_hints["monitor_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument traffic_routing_method", value=traffic_routing_method, expected_type=type_hints["traffic_routing_method"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_return", value=max_return, expected_type=type_hints["max_return"])
            check_type(argname="argument profile_status", value=profile_status, expected_type=type_hints["profile_status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument traffic_view_enabled", value=traffic_view_enabled, expected_type=type_hints["traffic_view_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_config": dns_config,
            "monitor_config": monitor_config,
            "name": name,
            "resource_group_name": resource_group_name,
            "traffic_routing_method": traffic_routing_method,
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
        if id is not None:
            self._values["id"] = id
        if max_return is not None:
            self._values["max_return"] = max_return
        if profile_status is not None:
            self._values["profile_status"] = profile_status
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if traffic_view_enabled is not None:
            self._values["traffic_view_enabled"] = traffic_view_enabled

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
    def dns_config(self) -> "TrafficManagerProfileDnsConfig":
        '''dns_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#dns_config TrafficManagerProfile#dns_config}
        '''
        result = self._values.get("dns_config")
        assert result is not None, "Required property 'dns_config' is missing"
        return typing.cast("TrafficManagerProfileDnsConfig", result)

    @builtins.property
    def monitor_config(self) -> "TrafficManagerProfileMonitorConfig":
        '''monitor_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#monitor_config TrafficManagerProfile#monitor_config}
        '''
        result = self._values.get("monitor_config")
        assert result is not None, "Required property 'monitor_config' is missing"
        return typing.cast("TrafficManagerProfileMonitorConfig", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#name TrafficManagerProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#resource_group_name TrafficManagerProfile#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def traffic_routing_method(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#traffic_routing_method TrafficManagerProfile#traffic_routing_method}.'''
        result = self._values.get("traffic_routing_method")
        assert result is not None, "Required property 'traffic_routing_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#id TrafficManagerProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_return(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#max_return TrafficManagerProfile#max_return}.'''
        result = self._values.get("max_return")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profile_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#profile_status TrafficManagerProfile#profile_status}.'''
        result = self._values.get("profile_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#tags TrafficManagerProfile#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["TrafficManagerProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#timeouts TrafficManagerProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["TrafficManagerProfileTimeouts"], result)

    @builtins.property
    def traffic_view_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#traffic_view_enabled TrafficManagerProfile#traffic_view_enabled}.'''
        result = self._values.get("traffic_view_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrafficManagerProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileDnsConfig",
    jsii_struct_bases=[],
    name_mapping={"relative_name": "relativeName", "ttl": "ttl"},
)
class TrafficManagerProfileDnsConfig:
    def __init__(self, *, relative_name: builtins.str, ttl: jsii.Number) -> None:
        '''
        :param relative_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#relative_name TrafficManagerProfile#relative_name}.
        :param ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#ttl TrafficManagerProfile#ttl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5232b059a7905dd8a5cde29be764a38039353d61c3c3048e573da04a36f5efd)
            check_type(argname="argument relative_name", value=relative_name, expected_type=type_hints["relative_name"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "relative_name": relative_name,
            "ttl": ttl,
        }

    @builtins.property
    def relative_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#relative_name TrafficManagerProfile#relative_name}.'''
        result = self._values.get("relative_name")
        assert result is not None, "Required property 'relative_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ttl(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#ttl TrafficManagerProfile#ttl}.'''
        result = self._values.get("ttl")
        assert result is not None, "Required property 'ttl' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrafficManagerProfileDnsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TrafficManagerProfileDnsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileDnsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55380cfba86af3740dd3d3283bba62c16436dce5c47749c472a4e0040d543950)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="relativeNameInput")
    def relative_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relativeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="relativeName")
    def relative_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relativeName"))

    @relative_name.setter
    def relative_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd9def3d07fa82ccf0c6bb271aef43465025f8f8d22403b29cddc81466ec5f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d929d53d8bc87c427ba0afd21dc96428922fc8945b9650b9ef4dcdf03ee7a5d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TrafficManagerProfileDnsConfig]:
        return typing.cast(typing.Optional[TrafficManagerProfileDnsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TrafficManagerProfileDnsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf67eb7707cfab07596eba3c43a16a784223e3c1ed625c8d993fb2018234dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileMonitorConfig",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "protocol": "protocol",
        "custom_header": "customHeader",
        "expected_status_code_ranges": "expectedStatusCodeRanges",
        "interval_in_seconds": "intervalInSeconds",
        "path": "path",
        "timeout_in_seconds": "timeoutInSeconds",
        "tolerated_number_of_failures": "toleratedNumberOfFailures",
    },
)
class TrafficManagerProfileMonitorConfig:
    def __init__(
        self,
        *,
        port: jsii.Number,
        protocol: builtins.str,
        custom_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TrafficManagerProfileMonitorConfigCustomHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        expected_status_code_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        interval_in_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
        tolerated_number_of_failures: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#port TrafficManagerProfile#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#protocol TrafficManagerProfile#protocol}.
        :param custom_header: custom_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#custom_header TrafficManagerProfile#custom_header}
        :param expected_status_code_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#expected_status_code_ranges TrafficManagerProfile#expected_status_code_ranges}.
        :param interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#interval_in_seconds TrafficManagerProfile#interval_in_seconds}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#path TrafficManagerProfile#path}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#timeout_in_seconds TrafficManagerProfile#timeout_in_seconds}.
        :param tolerated_number_of_failures: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#tolerated_number_of_failures TrafficManagerProfile#tolerated_number_of_failures}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c2c1c122365509f58536d8023f1021cff416d7c4f7689a1862bbebb75b3066a)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument custom_header", value=custom_header, expected_type=type_hints["custom_header"])
            check_type(argname="argument expected_status_code_ranges", value=expected_status_code_ranges, expected_type=type_hints["expected_status_code_ranges"])
            check_type(argname="argument interval_in_seconds", value=interval_in_seconds, expected_type=type_hints["interval_in_seconds"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            check_type(argname="argument tolerated_number_of_failures", value=tolerated_number_of_failures, expected_type=type_hints["tolerated_number_of_failures"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "protocol": protocol,
        }
        if custom_header is not None:
            self._values["custom_header"] = custom_header
        if expected_status_code_ranges is not None:
            self._values["expected_status_code_ranges"] = expected_status_code_ranges
        if interval_in_seconds is not None:
            self._values["interval_in_seconds"] = interval_in_seconds
        if path is not None:
            self._values["path"] = path
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds
        if tolerated_number_of_failures is not None:
            self._values["tolerated_number_of_failures"] = tolerated_number_of_failures

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#port TrafficManagerProfile#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#protocol TrafficManagerProfile#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TrafficManagerProfileMonitorConfigCustomHeader"]]]:
        '''custom_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#custom_header TrafficManagerProfile#custom_header}
        '''
        result = self._values.get("custom_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TrafficManagerProfileMonitorConfigCustomHeader"]]], result)

    @builtins.property
    def expected_status_code_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#expected_status_code_ranges TrafficManagerProfile#expected_status_code_ranges}.'''
        result = self._values.get("expected_status_code_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#interval_in_seconds TrafficManagerProfile#interval_in_seconds}.'''
        result = self._values.get("interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#path TrafficManagerProfile#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#timeout_in_seconds TrafficManagerProfile#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tolerated_number_of_failures(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#tolerated_number_of_failures TrafficManagerProfile#tolerated_number_of_failures}.'''
        result = self._values.get("tolerated_number_of_failures")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrafficManagerProfileMonitorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileMonitorConfigCustomHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class TrafficManagerProfileMonitorConfigCustomHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#name TrafficManagerProfile#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#value TrafficManagerProfile#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031a138c62ec8fbd0999334bafdfb8b033e82223d1754d6ff8d1903bd6c4ebef)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#name TrafficManagerProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#value TrafficManagerProfile#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrafficManagerProfileMonitorConfigCustomHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TrafficManagerProfileMonitorConfigCustomHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileMonitorConfigCustomHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41e22ce38c14549ff6086f5b86d8b0a83243215f6b7290afa7ea7c263e909291)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TrafficManagerProfileMonitorConfigCustomHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028656d74a342d7d6004ccd88690e4e3f8e7c5bdc42bfa3a8cc7a39798df25ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TrafficManagerProfileMonitorConfigCustomHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30892f699eb1d65f452496747588823f02b9114630fb41bd673e2f3dce2d952)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3245f72eafe84fe567f9e34a9e9a3f506cb65f5b63be3b265d43acba74340050)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aa7ae0948920b7f9915fa750a241a6a3c3f614033c4d63045f24ada00d003c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TrafficManagerProfileMonitorConfigCustomHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TrafficManagerProfileMonitorConfigCustomHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TrafficManagerProfileMonitorConfigCustomHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b86fded94e2106addf0f7f23a3e058b70361878160be0d2247e14768715c92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TrafficManagerProfileMonitorConfigCustomHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileMonitorConfigCustomHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a17da0f8fbb0bdcda7ab84441c026e2fb50070ead5cc3e2d99fb6d5398d5f67c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea1c54374deea8447d83e7f85e2f7b1aa0611936351de2206b47aa98d4eab5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5dcce8c6513ded053927d983bfd67aa47247f72a11fce4941fada5a2550c33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TrafficManagerProfileMonitorConfigCustomHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TrafficManagerProfileMonitorConfigCustomHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TrafficManagerProfileMonitorConfigCustomHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6492b298abbb1a9602b92eab8fecbfca62179f5f823e1d230154277cbd297b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TrafficManagerProfileMonitorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileMonitorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23408f34dbe99d4e683ea3bb3ec0b90a94a6690b5a81fab83650bb0a9d1ae579)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomHeader")
    def put_custom_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TrafficManagerProfileMonitorConfigCustomHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06a02709f17fcc2623b8dfbfc68d5f30458cfb8ef1cd79c4bd94ae3389e800c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomHeader", [value]))

    @jsii.member(jsii_name="resetCustomHeader")
    def reset_custom_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomHeader", []))

    @jsii.member(jsii_name="resetExpectedStatusCodeRanges")
    def reset_expected_status_code_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedStatusCodeRanges", []))

    @jsii.member(jsii_name="resetIntervalInSeconds")
    def reset_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalInSeconds", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetTimeoutInSeconds")
    def reset_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetToleratedNumberOfFailures")
    def reset_tolerated_number_of_failures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToleratedNumberOfFailures", []))

    @builtins.property
    @jsii.member(jsii_name="customHeader")
    def custom_header(self) -> TrafficManagerProfileMonitorConfigCustomHeaderList:
        return typing.cast(TrafficManagerProfileMonitorConfigCustomHeaderList, jsii.get(self, "customHeader"))

    @builtins.property
    @jsii.member(jsii_name="customHeaderInput")
    def custom_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TrafficManagerProfileMonitorConfigCustomHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TrafficManagerProfileMonitorConfigCustomHeader]]], jsii.get(self, "customHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedStatusCodeRangesInput")
    def expected_status_code_ranges_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "expectedStatusCodeRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInSecondsInput")
    def interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInSecondsInput")
    def timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="toleratedNumberOfFailuresInput")
    def tolerated_number_of_failures_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "toleratedNumberOfFailuresInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedStatusCodeRanges")
    def expected_status_code_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "expectedStatusCodeRanges"))

    @expected_status_code_ranges.setter
    def expected_status_code_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fadb087c41eaa0669a574864133e44097ac8625d3acde229cb60fffaad6261d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedStatusCodeRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalInSeconds")
    def interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalInSeconds"))

    @interval_in_seconds.setter
    def interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a06d7676be80fe3abb1e2799ff096b59d28ea71d15a8ba8717e710c15d0af98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32a24cecda7495e36da94f170cf6b4ac2ab14c945a21107ab28b4b816290b09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5443a66c4ef98c468dd01a9771aab0875a5d7c18ac3f6b802a5265de2aa5eb94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d900d69fc22d0fd58411e735e556f199aea25d0355e500865c63041c818327d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de148fb7eff13ef04970c100ab8d0f4f2791a120f45f96c510463784239ea49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="toleratedNumberOfFailures")
    def tolerated_number_of_failures(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "toleratedNumberOfFailures"))

    @tolerated_number_of_failures.setter
    def tolerated_number_of_failures(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d58fbbb55096273d48226afc39a1ec365640755f3e9455f9eafad913c65291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toleratedNumberOfFailures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TrafficManagerProfileMonitorConfig]:
        return typing.cast(typing.Optional[TrafficManagerProfileMonitorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TrafficManagerProfileMonitorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d0bc8b6d5fc716bee3218f348abc45750db3f46abced892ecb9e227d4d7a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class TrafficManagerProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#create TrafficManagerProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#delete TrafficManagerProfile#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#read TrafficManagerProfile#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#update TrafficManagerProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f66d802e1ab062a27256af2307b4497300726dc8e456f8f4b328ed4341cd8f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#create TrafficManagerProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#delete TrafficManagerProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#read TrafficManagerProfile#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/traffic_manager_profile#update TrafficManagerProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrafficManagerProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TrafficManagerProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.trafficManagerProfile.TrafficManagerProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08ce5f6cca6b25ee01959fbceaba975173aa08970f32d9f9317dacc7ab35be3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b384594b6b542bd89ac3b3dae4a6f44667ce4f64e524446c4c48b27d424d40ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067fff489b32c3e5d9fe9bb31102223cb99669961be3acad74c4fe7b16006450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a757852523fcfda1ceb8634f4f30e7acbfcac1ba601857010e2f94a745dfe92f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804bc6ea71d70f0e3964f85e97727e69ef39267afaef4b6e57c9ca8358355d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TrafficManagerProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TrafficManagerProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TrafficManagerProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a696e3dc06c0f813ed99b8ee52b13991930b3651f7bde02ce1c1e84d628816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TrafficManagerProfile",
    "TrafficManagerProfileConfig",
    "TrafficManagerProfileDnsConfig",
    "TrafficManagerProfileDnsConfigOutputReference",
    "TrafficManagerProfileMonitorConfig",
    "TrafficManagerProfileMonitorConfigCustomHeader",
    "TrafficManagerProfileMonitorConfigCustomHeaderList",
    "TrafficManagerProfileMonitorConfigCustomHeaderOutputReference",
    "TrafficManagerProfileMonitorConfigOutputReference",
    "TrafficManagerProfileTimeouts",
    "TrafficManagerProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7686a317afe6c1cd8affdf1f744f7c6c6733d8a2347c6bc90554bc69dc516fb2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dns_config: typing.Union[TrafficManagerProfileDnsConfig, typing.Dict[builtins.str, typing.Any]],
    monitor_config: typing.Union[TrafficManagerProfileMonitorConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    resource_group_name: builtins.str,
    traffic_routing_method: builtins.str,
    id: typing.Optional[builtins.str] = None,
    max_return: typing.Optional[jsii.Number] = None,
    profile_status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[TrafficManagerProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_view_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__2bf5936052999acb33613efc7139aaf565b189006d042670078cc49b4b8f07b0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445af9206e987f1ac49b2fe2d73a68e4b0f022d407a4474927c233ee37ede313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea6ecd1ddcf5a39f1887ad58150084e42dab43cd219b3f88bd177c1a339122e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c2a76b67f56593f0d6e1e8e2f6b4dfb26ac331fd97b618e605bbe817d2c004(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed43bb2c1a2eace71499c7256ca6b43badd0273a7d9520493d8b19140cde8dc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db283c766c97cc04b71c8706f8fd18eec78066d45e566db3609b4a7838211036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943c5c15828f434385bd0881f1d631c6b9544df6b4efb9056c0082ff12d42493(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97577a635a6ef9c490c5451641d0432abf170aa9906f3dff98515b0b5d718ec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ae5b8b00c034dcd750bf6c719099d6d6c907a29a29c79ced9b7424fa9ae233(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6792b35fc30d60c728d6ca609f9a4e89c1e9f750bcda3095fcb3651b2bd3f60(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_config: typing.Union[TrafficManagerProfileDnsConfig, typing.Dict[builtins.str, typing.Any]],
    monitor_config: typing.Union[TrafficManagerProfileMonitorConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    resource_group_name: builtins.str,
    traffic_routing_method: builtins.str,
    id: typing.Optional[builtins.str] = None,
    max_return: typing.Optional[jsii.Number] = None,
    profile_status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[TrafficManagerProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_view_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5232b059a7905dd8a5cde29be764a38039353d61c3c3048e573da04a36f5efd(
    *,
    relative_name: builtins.str,
    ttl: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55380cfba86af3740dd3d3283bba62c16436dce5c47749c472a4e0040d543950(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd9def3d07fa82ccf0c6bb271aef43465025f8f8d22403b29cddc81466ec5f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d929d53d8bc87c427ba0afd21dc96428922fc8945b9650b9ef4dcdf03ee7a5d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf67eb7707cfab07596eba3c43a16a784223e3c1ed625c8d993fb2018234dfe(
    value: typing.Optional[TrafficManagerProfileDnsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2c1c122365509f58536d8023f1021cff416d7c4f7689a1862bbebb75b3066a(
    *,
    port: jsii.Number,
    protocol: builtins.str,
    custom_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TrafficManagerProfileMonitorConfigCustomHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    expected_status_code_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
    tolerated_number_of_failures: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031a138c62ec8fbd0999334bafdfb8b033e82223d1754d6ff8d1903bd6c4ebef(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e22ce38c14549ff6086f5b86d8b0a83243215f6b7290afa7ea7c263e909291(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028656d74a342d7d6004ccd88690e4e3f8e7c5bdc42bfa3a8cc7a39798df25ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30892f699eb1d65f452496747588823f02b9114630fb41bd673e2f3dce2d952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3245f72eafe84fe567f9e34a9e9a3f506cb65f5b63be3b265d43acba74340050(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa7ae0948920b7f9915fa750a241a6a3c3f614033c4d63045f24ada00d003c9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b86fded94e2106addf0f7f23a3e058b70361878160be0d2247e14768715c92(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TrafficManagerProfileMonitorConfigCustomHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17da0f8fbb0bdcda7ab84441c026e2fb50070ead5cc3e2d99fb6d5398d5f67c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea1c54374deea8447d83e7f85e2f7b1aa0611936351de2206b47aa98d4eab5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5dcce8c6513ded053927d983bfd67aa47247f72a11fce4941fada5a2550c33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6492b298abbb1a9602b92eab8fecbfca62179f5f823e1d230154277cbd297b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TrafficManagerProfileMonitorConfigCustomHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23408f34dbe99d4e683ea3bb3ec0b90a94a6690b5a81fab83650bb0a9d1ae579(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06a02709f17fcc2623b8dfbfc68d5f30458cfb8ef1cd79c4bd94ae3389e800c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TrafficManagerProfileMonitorConfigCustomHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fadb087c41eaa0669a574864133e44097ac8625d3acde229cb60fffaad6261d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a06d7676be80fe3abb1e2799ff096b59d28ea71d15a8ba8717e710c15d0af98(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a24cecda7495e36da94f170cf6b4ac2ab14c945a21107ab28b4b816290b09f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5443a66c4ef98c468dd01a9771aab0875a5d7c18ac3f6b802a5265de2aa5eb94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d900d69fc22d0fd58411e735e556f199aea25d0355e500865c63041c818327d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de148fb7eff13ef04970c100ab8d0f4f2791a120f45f96c510463784239ea49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d58fbbb55096273d48226afc39a1ec365640755f3e9455f9eafad913c65291(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d0bc8b6d5fc716bee3218f348abc45750db3f46abced892ecb9e227d4d7a2a(
    value: typing.Optional[TrafficManagerProfileMonitorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f66d802e1ab062a27256af2307b4497300726dc8e456f8f4b328ed4341cd8f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ce5f6cca6b25ee01959fbceaba975173aa08970f32d9f9317dacc7ab35be3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b384594b6b542bd89ac3b3dae4a6f44667ce4f64e524446c4c48b27d424d40ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067fff489b32c3e5d9fe9bb31102223cb99669961be3acad74c4fe7b16006450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a757852523fcfda1ceb8634f4f30e7acbfcac1ba601857010e2f94a745dfe92f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804bc6ea71d70f0e3964f85e97727e69ef39267afaef4b6e57c9ca8358355d02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a696e3dc06c0f813ed99b8ee52b13991930b3651f7bde02ce1c1e84d628816(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TrafficManagerProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
