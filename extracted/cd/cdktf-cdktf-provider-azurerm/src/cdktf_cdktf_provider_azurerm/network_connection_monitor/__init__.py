r'''
# `azurerm_network_connection_monitor`

Refer to the Terraform Registry for docs: [`azurerm_network_connection_monitor`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor).
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


class NetworkConnectionMonitor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitor",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor azurerm_network_connection_monitor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        endpoint: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorEndpoint", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        network_watcher_id: builtins.str,
        test_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorTestConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        test_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorTestGroup", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        output_workspace_resource_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectionMonitorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor azurerm_network_connection_monitor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param endpoint: endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#endpoint NetworkConnectionMonitor#endpoint}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#location NetworkConnectionMonitor#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.
        :param network_watcher_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#network_watcher_id NetworkConnectionMonitor#network_watcher_id}.
        :param test_configuration: test_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_configuration NetworkConnectionMonitor#test_configuration}
        :param test_group: test_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_group NetworkConnectionMonitor#test_group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#id NetworkConnectionMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#notes NetworkConnectionMonitor#notes}.
        :param output_workspace_resource_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#output_workspace_resource_ids NetworkConnectionMonitor#output_workspace_resource_ids}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#tags NetworkConnectionMonitor#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#timeouts NetworkConnectionMonitor#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efeb2263b9e8f2047993aa050439e63bc839de4a5f18f8698658d204ed74ac9d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkConnectionMonitorConfig(
            endpoint=endpoint,
            location=location,
            name=name,
            network_watcher_id=network_watcher_id,
            test_configuration=test_configuration,
            test_group=test_group,
            id=id,
            notes=notes,
            output_workspace_resource_ids=output_workspace_resource_ids,
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
        '''Generates CDKTF code for importing a NetworkConnectionMonitor resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkConnectionMonitor to import.
        :param import_from_id: The id of the existing NetworkConnectionMonitor that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkConnectionMonitor to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498af584221c2acbfdc17cc2d2647d00138fc0f24f538e59dd648d464a188344)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEndpoint")
    def put_endpoint(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorEndpoint", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db1b91c21b1e7526f0caedf0065081e3321d7c5397b2304cccf6aa59b68cab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEndpoint", [value]))

    @jsii.member(jsii_name="putTestConfiguration")
    def put_test_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorTestConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097a37ad95a3cb1182b06238b13ecad7b128bac37e9c40ce582bc16e97962122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTestConfiguration", [value]))

    @jsii.member(jsii_name="putTestGroup")
    def put_test_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorTestGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79716f5b53c4d3afdda540520fb0b49c0a2da07386fca1cb0892c97b7067eb99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTestGroup", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#create NetworkConnectionMonitor#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#delete NetworkConnectionMonitor#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#read NetworkConnectionMonitor#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#update NetworkConnectionMonitor#update}.
        '''
        value = NetworkConnectionMonitorTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotes")
    def reset_notes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotes", []))

    @jsii.member(jsii_name="resetOutputWorkspaceResourceIds")
    def reset_output_workspace_resource_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputWorkspaceResourceIds", []))

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
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> "NetworkConnectionMonitorEndpointList":
        return typing.cast("NetworkConnectionMonitorEndpointList", jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="testConfiguration")
    def test_configuration(self) -> "NetworkConnectionMonitorTestConfigurationList":
        return typing.cast("NetworkConnectionMonitorTestConfigurationList", jsii.get(self, "testConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="testGroup")
    def test_group(self) -> "NetworkConnectionMonitorTestGroupList":
        return typing.cast("NetworkConnectionMonitorTestGroupList", jsii.get(self, "testGroup"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkConnectionMonitorTimeoutsOutputReference":
        return typing.cast("NetworkConnectionMonitorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorEndpoint"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorEndpoint"]]], jsii.get(self, "endpointInput"))

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
    @jsii.member(jsii_name="networkWatcherIdInput")
    def network_watcher_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkWatcherIdInput"))

    @builtins.property
    @jsii.member(jsii_name="notesInput")
    def notes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notesInput"))

    @builtins.property
    @jsii.member(jsii_name="outputWorkspaceResourceIdsInput")
    def output_workspace_resource_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outputWorkspaceResourceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="testConfigurationInput")
    def test_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestConfiguration"]]], jsii.get(self, "testConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="testGroupInput")
    def test_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestGroup"]]], jsii.get(self, "testGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectionMonitorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectionMonitorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b79e871558c9611de761e5ad2efb3ab891ad24e717495a5d105b8dd5b6ac1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e06a2d242a254a9c5efa4aed4dd01d3029b88fc4528ffcb9e072c641f682d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42032b9c01e2d7eace088325fcb8bae25c931df4d596eaad779e630ba473843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkWatcherId")
    def network_watcher_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkWatcherId"))

    @network_watcher_id.setter
    def network_watcher_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b04ebc76bfac9c1153471d8c65f4de1526a5026d5bb3e343c3eb3845a38b1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkWatcherId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notes"))

    @notes.setter
    def notes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4053589c18b2fbe579f0d7857b4149c1dd6debe7a1e33ec8c6116dbdfe49684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputWorkspaceResourceIds")
    def output_workspace_resource_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outputWorkspaceResourceIds"))

    @output_workspace_resource_ids.setter
    def output_workspace_resource_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c702d0bb8ed0e6d1662ecb320791f8bed26eb192a5d159fd850574e5cb2f7381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputWorkspaceResourceIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd89808c27f222231c091e14c2e41118856ac8abec661f5115faef145f39d2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "endpoint": "endpoint",
        "location": "location",
        "name": "name",
        "network_watcher_id": "networkWatcherId",
        "test_configuration": "testConfiguration",
        "test_group": "testGroup",
        "id": "id",
        "notes": "notes",
        "output_workspace_resource_ids": "outputWorkspaceResourceIds",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class NetworkConnectionMonitorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        endpoint: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorEndpoint", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        network_watcher_id: builtins.str,
        test_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorTestConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        test_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorTestGroup", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        output_workspace_resource_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectionMonitorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param endpoint: endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#endpoint NetworkConnectionMonitor#endpoint}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#location NetworkConnectionMonitor#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.
        :param network_watcher_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#network_watcher_id NetworkConnectionMonitor#network_watcher_id}.
        :param test_configuration: test_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_configuration NetworkConnectionMonitor#test_configuration}
        :param test_group: test_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_group NetworkConnectionMonitor#test_group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#id NetworkConnectionMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#notes NetworkConnectionMonitor#notes}.
        :param output_workspace_resource_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#output_workspace_resource_ids NetworkConnectionMonitor#output_workspace_resource_ids}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#tags NetworkConnectionMonitor#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#timeouts NetworkConnectionMonitor#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetworkConnectionMonitorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e185fc9cb02694f9d4bd31eb9a48300293e8a858b1f9d4e8bee5311563e5c770)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_watcher_id", value=network_watcher_id, expected_type=type_hints["network_watcher_id"])
            check_type(argname="argument test_configuration", value=test_configuration, expected_type=type_hints["test_configuration"])
            check_type(argname="argument test_group", value=test_group, expected_type=type_hints["test_group"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notes", value=notes, expected_type=type_hints["notes"])
            check_type(argname="argument output_workspace_resource_ids", value=output_workspace_resource_ids, expected_type=type_hints["output_workspace_resource_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "location": location,
            "name": name,
            "network_watcher_id": network_watcher_id,
            "test_configuration": test_configuration,
            "test_group": test_group,
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
        if notes is not None:
            self._values["notes"] = notes
        if output_workspace_resource_ids is not None:
            self._values["output_workspace_resource_ids"] = output_workspace_resource_ids
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
    def endpoint(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorEndpoint"]]:
        '''endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#endpoint NetworkConnectionMonitor#endpoint}
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorEndpoint"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#location NetworkConnectionMonitor#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_watcher_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#network_watcher_id NetworkConnectionMonitor#network_watcher_id}.'''
        result = self._values.get("network_watcher_id")
        assert result is not None, "Required property 'network_watcher_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def test_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestConfiguration"]]:
        '''test_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_configuration NetworkConnectionMonitor#test_configuration}
        '''
        result = self._values.get("test_configuration")
        assert result is not None, "Required property 'test_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestConfiguration"]], result)

    @builtins.property
    def test_group(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestGroup"]]:
        '''test_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_group NetworkConnectionMonitor#test_group}
        '''
        result = self._values.get("test_group")
        assert result is not None, "Required property 'test_group' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestGroup"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#id NetworkConnectionMonitor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#notes NetworkConnectionMonitor#notes}.'''
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_workspace_resource_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#output_workspace_resource_ids NetworkConnectionMonitor#output_workspace_resource_ids}.'''
        result = self._values.get("output_workspace_resource_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#tags NetworkConnectionMonitor#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkConnectionMonitorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#timeouts NetworkConnectionMonitor#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkConnectionMonitorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorEndpoint",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "address": "address",
        "coverage_level": "coverageLevel",
        "excluded_ip_addresses": "excludedIpAddresses",
        "filter": "filter",
        "included_ip_addresses": "includedIpAddresses",
        "target_resource_id": "targetResourceId",
        "target_resource_type": "targetResourceType",
    },
)
class NetworkConnectionMonitorEndpoint:
    def __init__(
        self,
        *,
        name: builtins.str,
        address: typing.Optional[builtins.str] = None,
        coverage_level: typing.Optional[builtins.str] = None,
        excluded_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        filter: typing.Optional[typing.Union["NetworkConnectionMonitorEndpointFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        included_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_resource_id: typing.Optional[builtins.str] = None,
        target_resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#address NetworkConnectionMonitor#address}.
        :param coverage_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#coverage_level NetworkConnectionMonitor#coverage_level}.
        :param excluded_ip_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#excluded_ip_addresses NetworkConnectionMonitor#excluded_ip_addresses}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#filter NetworkConnectionMonitor#filter}
        :param included_ip_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#included_ip_addresses NetworkConnectionMonitor#included_ip_addresses}.
        :param target_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#target_resource_id NetworkConnectionMonitor#target_resource_id}.
        :param target_resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#target_resource_type NetworkConnectionMonitor#target_resource_type}.
        '''
        if isinstance(filter, dict):
            filter = NetworkConnectionMonitorEndpointFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a267c8456fa80545a4875041a9a1f03dc12cd0c7f7c6de585d8940fdd12467)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument coverage_level", value=coverage_level, expected_type=type_hints["coverage_level"])
            check_type(argname="argument excluded_ip_addresses", value=excluded_ip_addresses, expected_type=type_hints["excluded_ip_addresses"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument included_ip_addresses", value=included_ip_addresses, expected_type=type_hints["included_ip_addresses"])
            check_type(argname="argument target_resource_id", value=target_resource_id, expected_type=type_hints["target_resource_id"])
            check_type(argname="argument target_resource_type", value=target_resource_type, expected_type=type_hints["target_resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if address is not None:
            self._values["address"] = address
        if coverage_level is not None:
            self._values["coverage_level"] = coverage_level
        if excluded_ip_addresses is not None:
            self._values["excluded_ip_addresses"] = excluded_ip_addresses
        if filter is not None:
            self._values["filter"] = filter
        if included_ip_addresses is not None:
            self._values["included_ip_addresses"] = included_ip_addresses
        if target_resource_id is not None:
            self._values["target_resource_id"] = target_resource_id
        if target_resource_type is not None:
            self._values["target_resource_type"] = target_resource_type

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#address NetworkConnectionMonitor#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def coverage_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#coverage_level NetworkConnectionMonitor#coverage_level}.'''
        result = self._values.get("coverage_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excluded_ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#excluded_ip_addresses NetworkConnectionMonitor#excluded_ip_addresses}.'''
        result = self._values.get("excluded_ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def filter(self) -> typing.Optional["NetworkConnectionMonitorEndpointFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#filter NetworkConnectionMonitor#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["NetworkConnectionMonitorEndpointFilter"], result)

    @builtins.property
    def included_ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#included_ip_addresses NetworkConnectionMonitor#included_ip_addresses}.'''
        result = self._values.get("included_ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#target_resource_id NetworkConnectionMonitor#target_resource_id}.'''
        result = self._values.get("target_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_resource_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#target_resource_type NetworkConnectionMonitor#target_resource_type}.'''
        result = self._values.get("target_resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorEndpointFilter",
    jsii_struct_bases=[],
    name_mapping={"item": "item", "type": "type"},
)
class NetworkConnectionMonitorEndpointFilter:
    def __init__(
        self,
        *,
        item: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorEndpointFilterItem", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param item: item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#item NetworkConnectionMonitor#item}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#type NetworkConnectionMonitor#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6782b51724a65dcae9fd5b5b3910f42e1dcf143f02004de0ea6d02fdb75759cc)
            check_type(argname="argument item", value=item, expected_type=type_hints["item"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if item is not None:
            self._values["item"] = item
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def item(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorEndpointFilterItem"]]]:
        '''item block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#item NetworkConnectionMonitor#item}
        '''
        result = self._values.get("item")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorEndpointFilterItem"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#type NetworkConnectionMonitor#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorEndpointFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorEndpointFilterItem",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "type": "type"},
)
class NetworkConnectionMonitorEndpointFilterItem:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#address NetworkConnectionMonitor#address}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#type NetworkConnectionMonitor#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d28e74df6700aebdfbb91866c019055a453a71ff7dc8542ce35c2819aea35c1)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#address NetworkConnectionMonitor#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#type NetworkConnectionMonitor#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorEndpointFilterItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectionMonitorEndpointFilterItemList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorEndpointFilterItemList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bc8ae9a5cc3fdc865209dd73ff1ea9b2aa438b49a297c9eac5dd7cfc4e23186)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectionMonitorEndpointFilterItemOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b409a3827f7001c945d4ce4d1e167bcdba2e749d66548b9bcffaf6a7309fcc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectionMonitorEndpointFilterItemOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbed295c8c3fa7798c5dae775d289982b379778db3343bdc74aa61e60126747)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e1c866e03f348444eb1297f35639a4428b8a3312709b2fd2199f2c958e1c27d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1272c4227605dde1d7ad961ae33f32b15063e1aabbc8955f260d5f7d8da74692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpointFilterItem]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpointFilterItem]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpointFilterItem]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c6255305852f52ee1b43dec901d5d1d9f4e6df45875f012a03d5f539acf780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectionMonitorEndpointFilterItemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorEndpointFilterItemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f81ca72da70513a9233c9782051259e971c783b5eae8efa8506ffce38b1d4bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93899df4cb93c505fd5999c8267060b0d71cc01f8abbb69038847bc8145558ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__213376b7ca15691f096f3195ae8093e81a9fdc842bacb6c62e18dcd12afc35d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorEndpointFilterItem]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorEndpointFilterItem]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorEndpointFilterItem]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fad42b10b8900952ec2a3c130e7a5933dd8d48a75ed73e694a2805b4e8c216e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectionMonitorEndpointFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorEndpointFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff8c5ae9a6583744b4251bc9db34b1c8120d5aaa685ca3cabf2c9d84725591f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItem")
    def put_item(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorEndpointFilterItem, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8fcab7d374f6477d279cdf7826c8e9357f063f8af63620b57d4d4f2fcc28eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItem", [value]))

    @jsii.member(jsii_name="resetItem")
    def reset_item(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItem", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="item")
    def item(self) -> NetworkConnectionMonitorEndpointFilterItemList:
        return typing.cast(NetworkConnectionMonitorEndpointFilterItemList, jsii.get(self, "item"))

    @builtins.property
    @jsii.member(jsii_name="itemInput")
    def item_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpointFilterItem]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpointFilterItem]]], jsii.get(self, "itemInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cfa9fbcd40249115bd61388575a220c3252237b4dffc3a93aa3efe4c7bc7697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkConnectionMonitorEndpointFilter]:
        return typing.cast(typing.Optional[NetworkConnectionMonitorEndpointFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectionMonitorEndpointFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2b3103801e478170bd5c692619cc9a7d2cefcb623640e7d9cfa7640e09878e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectionMonitorEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b001ba5160b3a0eff34a726b77509c6877ad67e16abe245258433b3b67e9d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectionMonitorEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e188933606fabc3bd5ae482ebf6fd200d79c36f0dd8e5d034ef061b58feca1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectionMonitorEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fbb1bdd2318c1b9c5789683a7600093571a4557b12c26ad80c0cef67e07570)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3924daa10188c7db354e197bb6c9b75a9c472cbf22f729890866f61572fe420b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__428da51675a2153462da9210f35483fb54e3d57e6f56c184381f1fec1ca8dd06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpoint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpoint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e5d5c567a49c1eb738b79c906a697abd997a793fa30ddd40d5af97f62e3fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectionMonitorEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf2020bd1492a39eccc509ac9cb7d0ebef0151421459d8fa26e8446264bc5f1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        item: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorEndpointFilterItem, typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param item: item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#item NetworkConnectionMonitor#item}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#type NetworkConnectionMonitor#type}.
        '''
        value = NetworkConnectionMonitorEndpointFilter(item=item, type=type)

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetCoverageLevel")
    def reset_coverage_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoverageLevel", []))

    @jsii.member(jsii_name="resetExcludedIpAddresses")
    def reset_excluded_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedIpAddresses", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetIncludedIpAddresses")
    def reset_included_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedIpAddresses", []))

    @jsii.member(jsii_name="resetTargetResourceId")
    def reset_target_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResourceId", []))

    @jsii.member(jsii_name="resetTargetResourceType")
    def reset_target_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResourceType", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> NetworkConnectionMonitorEndpointFilterOutputReference:
        return typing.cast(NetworkConnectionMonitorEndpointFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="coverageLevelInput")
    def coverage_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coverageLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedIpAddressesInput")
    def excluded_ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedIpAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[NetworkConnectionMonitorEndpointFilter]:
        return typing.cast(typing.Optional[NetworkConnectionMonitorEndpointFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="includedIpAddressesInput")
    def included_ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedIpAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceIdInput")
    def target_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceTypeInput")
    def target_resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd244fc0eb5e1699bae99601f47494de36fa54126be7b497cc49ef44cd686e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coverageLevel")
    def coverage_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coverageLevel"))

    @coverage_level.setter
    def coverage_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c457e180a048ee7d390aa76fe98ee4b371da7c64cce435ede8ffd07aa02ee976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coverageLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedIpAddresses")
    def excluded_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedIpAddresses"))

    @excluded_ip_addresses.setter
    def excluded_ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf57d00e2d5534d395bace32fb5d82f8158e6deef69530047025dc0b0d6056e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedIpAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedIpAddresses")
    def included_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedIpAddresses"))

    @included_ip_addresses.setter
    def included_ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ac81b4752fda6bdba67ed1ffbfb919596b90724a2471e4ebefa0052713915b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedIpAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef2c01a41c337db52bf8a948eda698cf12c8e449d539cd51a7be21909b0c2cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResourceId")
    def target_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetResourceId"))

    @target_resource_id.setter
    def target_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9841bf1eb3b8f373d754fbbd9e9b77df9eb2a91f022f8cdcc0d3c3dc79e4c3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResourceType")
    def target_resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetResourceType"))

    @target_resource_type.setter
    def target_resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60cb13b9c6b7d16568478f701523243df139daf7bb886708a0c03dc748fced7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorEndpoint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorEndpoint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorEndpoint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a87bff8c85ad425dd11b1fc248a758392a5d70a680684f5d0241af6626f0e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "protocol": "protocol",
        "http_configuration": "httpConfiguration",
        "icmp_configuration": "icmpConfiguration",
        "preferred_ip_version": "preferredIpVersion",
        "success_threshold": "successThreshold",
        "tcp_configuration": "tcpConfiguration",
        "test_frequency_in_seconds": "testFrequencyInSeconds",
    },
)
class NetworkConnectionMonitorTestConfiguration:
    def __init__(
        self,
        *,
        name: builtins.str,
        protocol: builtins.str,
        http_configuration: typing.Optional[typing.Union["NetworkConnectionMonitorTestConfigurationHttpConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        icmp_configuration: typing.Optional[typing.Union["NetworkConnectionMonitorTestConfigurationIcmpConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        preferred_ip_version: typing.Optional[builtins.str] = None,
        success_threshold: typing.Optional[typing.Union["NetworkConnectionMonitorTestConfigurationSuccessThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_configuration: typing.Optional[typing.Union["NetworkConnectionMonitorTestConfigurationTcpConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        test_frequency_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#protocol NetworkConnectionMonitor#protocol}.
        :param http_configuration: http_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#http_configuration NetworkConnectionMonitor#http_configuration}
        :param icmp_configuration: icmp_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#icmp_configuration NetworkConnectionMonitor#icmp_configuration}
        :param preferred_ip_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#preferred_ip_version NetworkConnectionMonitor#preferred_ip_version}.
        :param success_threshold: success_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#success_threshold NetworkConnectionMonitor#success_threshold}
        :param tcp_configuration: tcp_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#tcp_configuration NetworkConnectionMonitor#tcp_configuration}
        :param test_frequency_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_frequency_in_seconds NetworkConnectionMonitor#test_frequency_in_seconds}.
        '''
        if isinstance(http_configuration, dict):
            http_configuration = NetworkConnectionMonitorTestConfigurationHttpConfiguration(**http_configuration)
        if isinstance(icmp_configuration, dict):
            icmp_configuration = NetworkConnectionMonitorTestConfigurationIcmpConfiguration(**icmp_configuration)
        if isinstance(success_threshold, dict):
            success_threshold = NetworkConnectionMonitorTestConfigurationSuccessThreshold(**success_threshold)
        if isinstance(tcp_configuration, dict):
            tcp_configuration = NetworkConnectionMonitorTestConfigurationTcpConfiguration(**tcp_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bc766715c695c165fa93774edc517e0fe671453cefc1273b05f09798d84606)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument http_configuration", value=http_configuration, expected_type=type_hints["http_configuration"])
            check_type(argname="argument icmp_configuration", value=icmp_configuration, expected_type=type_hints["icmp_configuration"])
            check_type(argname="argument preferred_ip_version", value=preferred_ip_version, expected_type=type_hints["preferred_ip_version"])
            check_type(argname="argument success_threshold", value=success_threshold, expected_type=type_hints["success_threshold"])
            check_type(argname="argument tcp_configuration", value=tcp_configuration, expected_type=type_hints["tcp_configuration"])
            check_type(argname="argument test_frequency_in_seconds", value=test_frequency_in_seconds, expected_type=type_hints["test_frequency_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "protocol": protocol,
        }
        if http_configuration is not None:
            self._values["http_configuration"] = http_configuration
        if icmp_configuration is not None:
            self._values["icmp_configuration"] = icmp_configuration
        if preferred_ip_version is not None:
            self._values["preferred_ip_version"] = preferred_ip_version
        if success_threshold is not None:
            self._values["success_threshold"] = success_threshold
        if tcp_configuration is not None:
            self._values["tcp_configuration"] = tcp_configuration
        if test_frequency_in_seconds is not None:
            self._values["test_frequency_in_seconds"] = test_frequency_in_seconds

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#protocol NetworkConnectionMonitor#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_configuration(
        self,
    ) -> typing.Optional["NetworkConnectionMonitorTestConfigurationHttpConfiguration"]:
        '''http_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#http_configuration NetworkConnectionMonitor#http_configuration}
        '''
        result = self._values.get("http_configuration")
        return typing.cast(typing.Optional["NetworkConnectionMonitorTestConfigurationHttpConfiguration"], result)

    @builtins.property
    def icmp_configuration(
        self,
    ) -> typing.Optional["NetworkConnectionMonitorTestConfigurationIcmpConfiguration"]:
        '''icmp_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#icmp_configuration NetworkConnectionMonitor#icmp_configuration}
        '''
        result = self._values.get("icmp_configuration")
        return typing.cast(typing.Optional["NetworkConnectionMonitorTestConfigurationIcmpConfiguration"], result)

    @builtins.property
    def preferred_ip_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#preferred_ip_version NetworkConnectionMonitor#preferred_ip_version}.'''
        result = self._values.get("preferred_ip_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_threshold(
        self,
    ) -> typing.Optional["NetworkConnectionMonitorTestConfigurationSuccessThreshold"]:
        '''success_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#success_threshold NetworkConnectionMonitor#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional["NetworkConnectionMonitorTestConfigurationSuccessThreshold"], result)

    @builtins.property
    def tcp_configuration(
        self,
    ) -> typing.Optional["NetworkConnectionMonitorTestConfigurationTcpConfiguration"]:
        '''tcp_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#tcp_configuration NetworkConnectionMonitor#tcp_configuration}
        '''
        result = self._values.get("tcp_configuration")
        return typing.cast(typing.Optional["NetworkConnectionMonitorTestConfigurationTcpConfiguration"], result)

    @builtins.property
    def test_frequency_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_frequency_in_seconds NetworkConnectionMonitor#test_frequency_in_seconds}.'''
        result = self._values.get("test_frequency_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorTestConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationHttpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "method": "method",
        "path": "path",
        "port": "port",
        "prefer_https": "preferHttps",
        "request_header": "requestHeader",
        "valid_status_code_ranges": "validStatusCodeRanges",
    },
)
class NetworkConnectionMonitorTestConfigurationHttpConfiguration:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        prefer_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        valid_status_code_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#method NetworkConnectionMonitor#method}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#path NetworkConnectionMonitor#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#port NetworkConnectionMonitor#port}.
        :param prefer_https: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#prefer_https NetworkConnectionMonitor#prefer_https}.
        :param request_header: request_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#request_header NetworkConnectionMonitor#request_header}
        :param valid_status_code_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#valid_status_code_ranges NetworkConnectionMonitor#valid_status_code_ranges}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e27ca1a1e2eeb4b2554935e9c7def257929eeb4c2062e6ba996a88ff659ffa)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument prefer_https", value=prefer_https, expected_type=type_hints["prefer_https"])
            check_type(argname="argument request_header", value=request_header, expected_type=type_hints["request_header"])
            check_type(argname="argument valid_status_code_ranges", value=valid_status_code_ranges, expected_type=type_hints["valid_status_code_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if prefer_https is not None:
            self._values["prefer_https"] = prefer_https
        if request_header is not None:
            self._values["request_header"] = request_header
        if valid_status_code_ranges is not None:
            self._values["valid_status_code_ranges"] = valid_status_code_ranges

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#method NetworkConnectionMonitor#method}.'''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#path NetworkConnectionMonitor#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#port NetworkConnectionMonitor#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefer_https(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#prefer_https NetworkConnectionMonitor#prefer_https}.'''
        result = self._values.get("prefer_https")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def request_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader"]]]:
        '''request_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#request_header NetworkConnectionMonitor#request_header}
        '''
        result = self._values.get("request_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader"]]], result)

    @builtins.property
    def valid_status_code_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#valid_status_code_ranges NetworkConnectionMonitor#valid_status_code_ranges}.'''
        result = self._values.get("valid_status_code_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorTestConfigurationHttpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectionMonitorTestConfigurationHttpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationHttpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bd0962648fa1e4fb66f4bc5fe49af0a3dffaf610466ebed75601c747fd668f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeader")
    def put_request_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b30c516c3819d550cb5a8150cc81f141bf27ed905c148a2f296716faaf8604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeader", [value]))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPreferHttps")
    def reset_prefer_https(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferHttps", []))

    @jsii.member(jsii_name="resetRequestHeader")
    def reset_request_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeader", []))

    @jsii.member(jsii_name="resetValidStatusCodeRanges")
    def reset_valid_status_code_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidStatusCodeRanges", []))

    @builtins.property
    @jsii.member(jsii_name="requestHeader")
    def request_header(
        self,
    ) -> "NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderList":
        return typing.cast("NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderList", jsii.get(self, "requestHeader"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="preferHttpsInput")
    def prefer_https_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preferHttpsInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderInput")
    def request_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader"]]], jsii.get(self, "requestHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="validStatusCodeRangesInput")
    def valid_status_code_ranges_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "validStatusCodeRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740bf26090ba20de9384db058a7b2a1e03b3d0306aadd733fc34c8cfa22d57f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7616855ea1da84edb4003d29dd51807be76e6585cf098f5aa8e88b98febae6a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db6a65daf3930aad26204ded1ed34e697394dc5f8cbcb5eb5bfac7142fefad08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferHttps")
    def prefer_https(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preferHttps"))

    @prefer_https.setter
    def prefer_https(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19951f17a5b977ba2a6342eedef6e6109a297f66fce7690c7a0c1292c9ee85e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferHttps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validStatusCodeRanges")
    def valid_status_code_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "validStatusCodeRanges"))

    @valid_status_code_ranges.setter
    def valid_status_code_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82f033932f895e023096817dc5eb14689634d31fec205e28eb5d9226cdc9b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validStatusCodeRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectionMonitorTestConfigurationHttpConfiguration]:
        return typing.cast(typing.Optional[NetworkConnectionMonitorTestConfigurationHttpConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectionMonitorTestConfigurationHttpConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40c824e7ce6531b2fdab164745a83fda8be236b1e6aaa63492770c4f3ed578d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#value NetworkConnectionMonitor#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59dbc35a057a35e23e9746ee0b1471d30bc799d32187dd22ee9377dfa2841537)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#value NetworkConnectionMonitor#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b01a3c546c3dd6b15688be750144daf257fe8a948d34a7a975e1528ee5f5cf1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c4b90e4f4dd91b54673ab786c140af52f1c21a6eab56de8ef22c5a4aab8d9d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95fb3e1590a318945b5ca3b55f8ff2c6c82af84dbbb7c63fe063a396ef6e4c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2553f25c09bd47e0f7927d9a964edf357bdb9adda9fce09b0da2227a3dbeddc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a04aaada8697edea6170fd231717cb15292f371331a87ec408002b5071a63aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8ec1e6e422597ac71ab0b0576801303d4eae7a3de6d740e8f79b8cac514615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e352fbc1b54260c52390c01c8960bcfd9f9e408b1bf2f5c5992c249876e7112)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1d42ee2a8ffb904012a0f122645d41f194674eae767006c094cf5f15af37413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baec934dc252f69de8ef65dc881a14ecee059f6e9d83c051408374f935134130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2e894ea15d5b2bf6b2d90c30afedf86e68c35d6c7f01021c4f2b18919ead74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationIcmpConfiguration",
    jsii_struct_bases=[],
    name_mapping={"trace_route_enabled": "traceRouteEnabled"},
)
class NetworkConnectionMonitorTestConfigurationIcmpConfiguration:
    def __init__(
        self,
        *,
        trace_route_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param trace_route_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#trace_route_enabled NetworkConnectionMonitor#trace_route_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2875a43d0c1407942d3755b697d5be7b36248a00ef2a7f0c6fc209d04edb52db)
            check_type(argname="argument trace_route_enabled", value=trace_route_enabled, expected_type=type_hints["trace_route_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if trace_route_enabled is not None:
            self._values["trace_route_enabled"] = trace_route_enabled

    @builtins.property
    def trace_route_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#trace_route_enabled NetworkConnectionMonitor#trace_route_enabled}.'''
        result = self._values.get("trace_route_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorTestConfigurationIcmpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectionMonitorTestConfigurationIcmpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationIcmpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7727a84c08ae71cdb3f87202c44189a7747e417e75dbc644c65fa0cbaca2136)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTraceRouteEnabled")
    def reset_trace_route_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraceRouteEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="traceRouteEnabledInput")
    def trace_route_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "traceRouteEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="traceRouteEnabled")
    def trace_route_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "traceRouteEnabled"))

    @trace_route_enabled.setter
    def trace_route_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285c03c605d7dbea3fc71a5cd9050ebd9ca91f40af524005b47f64738aff512e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceRouteEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectionMonitorTestConfigurationIcmpConfiguration]:
        return typing.cast(typing.Optional[NetworkConnectionMonitorTestConfigurationIcmpConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectionMonitorTestConfigurationIcmpConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f8e9b4f35e44bf720077f745f615a5e5ad04f29ed5540abdfcd91284b6cc03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectionMonitorTestConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39a42f6aae9d5941198b7103514b53fa9d35c41135f6323768ebf4529227efe9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectionMonitorTestConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544bac76e94c40f170a13ab55fbb5ec2f04c5cb94057267773153b47081bef45)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectionMonitorTestConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1975ed42fad1b61b6d128bc07b8aa3f79ba1af2694868c9d92fc2f2db06eeb35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abe3555fa4f54a9c83acba06f88d493e4ffc499babf2c24c1a60c159a648234a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b007edf40aa562485e9c38bb7b56dcb464b42eb14a180cebb80b75366df3cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e07f1562df7b640e66a243c8f499dca9bdf14617d2c247186a07731b48cfbe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectionMonitorTestConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ebd9aeed1e8a596d3a2a38c300ff0f56ea24efa7e535300eabd2d936f9ec0c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHttpConfiguration")
    def put_http_configuration(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        prefer_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        valid_status_code_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#method NetworkConnectionMonitor#method}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#path NetworkConnectionMonitor#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#port NetworkConnectionMonitor#port}.
        :param prefer_https: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#prefer_https NetworkConnectionMonitor#prefer_https}.
        :param request_header: request_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#request_header NetworkConnectionMonitor#request_header}
        :param valid_status_code_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#valid_status_code_ranges NetworkConnectionMonitor#valid_status_code_ranges}.
        '''
        value = NetworkConnectionMonitorTestConfigurationHttpConfiguration(
            method=method,
            path=path,
            port=port,
            prefer_https=prefer_https,
            request_header=request_header,
            valid_status_code_ranges=valid_status_code_ranges,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpConfiguration", [value]))

    @jsii.member(jsii_name="putIcmpConfiguration")
    def put_icmp_configuration(
        self,
        *,
        trace_route_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param trace_route_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#trace_route_enabled NetworkConnectionMonitor#trace_route_enabled}.
        '''
        value = NetworkConnectionMonitorTestConfigurationIcmpConfiguration(
            trace_route_enabled=trace_route_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putIcmpConfiguration", [value]))

    @jsii.member(jsii_name="putSuccessThreshold")
    def put_success_threshold(
        self,
        *,
        checks_failed_percent: typing.Optional[jsii.Number] = None,
        round_trip_time_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param checks_failed_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#checks_failed_percent NetworkConnectionMonitor#checks_failed_percent}.
        :param round_trip_time_ms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#round_trip_time_ms NetworkConnectionMonitor#round_trip_time_ms}.
        '''
        value = NetworkConnectionMonitorTestConfigurationSuccessThreshold(
            checks_failed_percent=checks_failed_percent,
            round_trip_time_ms=round_trip_time_ms,
        )

        return typing.cast(None, jsii.invoke(self, "putSuccessThreshold", [value]))

    @jsii.member(jsii_name="putTcpConfiguration")
    def put_tcp_configuration(
        self,
        *,
        port: jsii.Number,
        destination_port_behavior: typing.Optional[builtins.str] = None,
        trace_route_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#port NetworkConnectionMonitor#port}.
        :param destination_port_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#destination_port_behavior NetworkConnectionMonitor#destination_port_behavior}.
        :param trace_route_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#trace_route_enabled NetworkConnectionMonitor#trace_route_enabled}.
        '''
        value = NetworkConnectionMonitorTestConfigurationTcpConfiguration(
            port=port,
            destination_port_behavior=destination_port_behavior,
            trace_route_enabled=trace_route_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putTcpConfiguration", [value]))

    @jsii.member(jsii_name="resetHttpConfiguration")
    def reset_http_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpConfiguration", []))

    @jsii.member(jsii_name="resetIcmpConfiguration")
    def reset_icmp_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcmpConfiguration", []))

    @jsii.member(jsii_name="resetPreferredIpVersion")
    def reset_preferred_ip_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredIpVersion", []))

    @jsii.member(jsii_name="resetSuccessThreshold")
    def reset_success_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessThreshold", []))

    @jsii.member(jsii_name="resetTcpConfiguration")
    def reset_tcp_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpConfiguration", []))

    @jsii.member(jsii_name="resetTestFrequencyInSeconds")
    def reset_test_frequency_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestFrequencyInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="httpConfiguration")
    def http_configuration(
        self,
    ) -> NetworkConnectionMonitorTestConfigurationHttpConfigurationOutputReference:
        return typing.cast(NetworkConnectionMonitorTestConfigurationHttpConfigurationOutputReference, jsii.get(self, "httpConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="icmpConfiguration")
    def icmp_configuration(
        self,
    ) -> NetworkConnectionMonitorTestConfigurationIcmpConfigurationOutputReference:
        return typing.cast(NetworkConnectionMonitorTestConfigurationIcmpConfigurationOutputReference, jsii.get(self, "icmpConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(
        self,
    ) -> "NetworkConnectionMonitorTestConfigurationSuccessThresholdOutputReference":
        return typing.cast("NetworkConnectionMonitorTestConfigurationSuccessThresholdOutputReference", jsii.get(self, "successThreshold"))

    @builtins.property
    @jsii.member(jsii_name="tcpConfiguration")
    def tcp_configuration(
        self,
    ) -> "NetworkConnectionMonitorTestConfigurationTcpConfigurationOutputReference":
        return typing.cast("NetworkConnectionMonitorTestConfigurationTcpConfigurationOutputReference", jsii.get(self, "tcpConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="httpConfigurationInput")
    def http_configuration_input(
        self,
    ) -> typing.Optional[NetworkConnectionMonitorTestConfigurationHttpConfiguration]:
        return typing.cast(typing.Optional[NetworkConnectionMonitorTestConfigurationHttpConfiguration], jsii.get(self, "httpConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="icmpConfigurationInput")
    def icmp_configuration_input(
        self,
    ) -> typing.Optional[NetworkConnectionMonitorTestConfigurationIcmpConfiguration]:
        return typing.cast(typing.Optional[NetworkConnectionMonitorTestConfigurationIcmpConfiguration], jsii.get(self, "icmpConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredIpVersionInput")
    def preferred_ip_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredIpVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="successThresholdInput")
    def success_threshold_input(
        self,
    ) -> typing.Optional["NetworkConnectionMonitorTestConfigurationSuccessThreshold"]:
        return typing.cast(typing.Optional["NetworkConnectionMonitorTestConfigurationSuccessThreshold"], jsii.get(self, "successThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpConfigurationInput")
    def tcp_configuration_input(
        self,
    ) -> typing.Optional["NetworkConnectionMonitorTestConfigurationTcpConfiguration"]:
        return typing.cast(typing.Optional["NetworkConnectionMonitorTestConfigurationTcpConfiguration"], jsii.get(self, "tcpConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="testFrequencyInSecondsInput")
    def test_frequency_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "testFrequencyInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3191b005590b3bfd428aa5a27ed6c5fd8e7f1d6793aa0ae4b57908495c2755dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredIpVersion")
    def preferred_ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredIpVersion"))

    @preferred_ip_version.setter
    def preferred_ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5544c6f0995a949c61eb2c80e5a87680566e2e7b96e333a3e9188dd1ebf997a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredIpVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e42ace2a72d2abc175791e75d27e6919c4527d9a8ac760154f2afe88853d696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="testFrequencyInSeconds")
    def test_frequency_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "testFrequencyInSeconds"))

    @test_frequency_in_seconds.setter
    def test_frequency_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cbc20f7873d69b31b226c18cc268d49d837e15431b5d65e6ff111c35da0731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testFrequencyInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963ac32a3a167cb200f124b8d4d1063857ff5f895d1827db50b7bb44cfcf97b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationSuccessThreshold",
    jsii_struct_bases=[],
    name_mapping={
        "checks_failed_percent": "checksFailedPercent",
        "round_trip_time_ms": "roundTripTimeMs",
    },
)
class NetworkConnectionMonitorTestConfigurationSuccessThreshold:
    def __init__(
        self,
        *,
        checks_failed_percent: typing.Optional[jsii.Number] = None,
        round_trip_time_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param checks_failed_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#checks_failed_percent NetworkConnectionMonitor#checks_failed_percent}.
        :param round_trip_time_ms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#round_trip_time_ms NetworkConnectionMonitor#round_trip_time_ms}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f92afb86b807f8a1e9f58c9d58f126e77c858c03bf880c9c9013c84c136684cc)
            check_type(argname="argument checks_failed_percent", value=checks_failed_percent, expected_type=type_hints["checks_failed_percent"])
            check_type(argname="argument round_trip_time_ms", value=round_trip_time_ms, expected_type=type_hints["round_trip_time_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if checks_failed_percent is not None:
            self._values["checks_failed_percent"] = checks_failed_percent
        if round_trip_time_ms is not None:
            self._values["round_trip_time_ms"] = round_trip_time_ms

    @builtins.property
    def checks_failed_percent(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#checks_failed_percent NetworkConnectionMonitor#checks_failed_percent}.'''
        result = self._values.get("checks_failed_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def round_trip_time_ms(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#round_trip_time_ms NetworkConnectionMonitor#round_trip_time_ms}.'''
        result = self._values.get("round_trip_time_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorTestConfigurationSuccessThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectionMonitorTestConfigurationSuccessThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationSuccessThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea12a80cc0c8327ca68c3aa2d372a23860475725cbef4c9f5fd009aedad9b900)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChecksFailedPercent")
    def reset_checks_failed_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChecksFailedPercent", []))

    @jsii.member(jsii_name="resetRoundTripTimeMs")
    def reset_round_trip_time_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoundTripTimeMs", []))

    @builtins.property
    @jsii.member(jsii_name="checksFailedPercentInput")
    def checks_failed_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "checksFailedPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="roundTripTimeMsInput")
    def round_trip_time_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "roundTripTimeMsInput"))

    @builtins.property
    @jsii.member(jsii_name="checksFailedPercent")
    def checks_failed_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "checksFailedPercent"))

    @checks_failed_percent.setter
    def checks_failed_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7937ea7b90203410375d415e85b9d9c2390935b3a5c4058c48c62543732ef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checksFailedPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roundTripTimeMs")
    def round_trip_time_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "roundTripTimeMs"))

    @round_trip_time_ms.setter
    def round_trip_time_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb64faad1f831d0b1fb34fd08911430b36232cbc047da5e85c6383617c5a5ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roundTripTimeMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectionMonitorTestConfigurationSuccessThreshold]:
        return typing.cast(typing.Optional[NetworkConnectionMonitorTestConfigurationSuccessThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectionMonitorTestConfigurationSuccessThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac45654f793f9a640d55a9e19ea60bbb82769be2dcac8e227aa0ae5654fc0ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationTcpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "destination_port_behavior": "destinationPortBehavior",
        "trace_route_enabled": "traceRouteEnabled",
    },
)
class NetworkConnectionMonitorTestConfigurationTcpConfiguration:
    def __init__(
        self,
        *,
        port: jsii.Number,
        destination_port_behavior: typing.Optional[builtins.str] = None,
        trace_route_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#port NetworkConnectionMonitor#port}.
        :param destination_port_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#destination_port_behavior NetworkConnectionMonitor#destination_port_behavior}.
        :param trace_route_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#trace_route_enabled NetworkConnectionMonitor#trace_route_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1f3cd27e3140b5ae9035c85c266a727c61c01bb097cab1e1f8ce075c47f895)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument destination_port_behavior", value=destination_port_behavior, expected_type=type_hints["destination_port_behavior"])
            check_type(argname="argument trace_route_enabled", value=trace_route_enabled, expected_type=type_hints["trace_route_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
        }
        if destination_port_behavior is not None:
            self._values["destination_port_behavior"] = destination_port_behavior
        if trace_route_enabled is not None:
            self._values["trace_route_enabled"] = trace_route_enabled

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#port NetworkConnectionMonitor#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def destination_port_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#destination_port_behavior NetworkConnectionMonitor#destination_port_behavior}.'''
        result = self._values.get("destination_port_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trace_route_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#trace_route_enabled NetworkConnectionMonitor#trace_route_enabled}.'''
        result = self._values.get("trace_route_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorTestConfigurationTcpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectionMonitorTestConfigurationTcpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestConfigurationTcpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82387cf50b0eacb846df1f7fe90e55a3b9475189f800a8928ce3b89753b1ec7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestinationPortBehavior")
    def reset_destination_port_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationPortBehavior", []))

    @jsii.member(jsii_name="resetTraceRouteEnabled")
    def reset_trace_route_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraceRouteEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="destinationPortBehaviorInput")
    def destination_port_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationPortBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="traceRouteEnabledInput")
    def trace_route_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "traceRouteEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPortBehavior")
    def destination_port_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationPortBehavior"))

    @destination_port_behavior.setter
    def destination_port_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9357ea4de89fc6c8493046983a11bece2f14a84028ccbf000cd4f95b68c35e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPortBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618a760ace22c4fc732552d90dfddada6db9299612b06251c478dcac2fde588c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceRouteEnabled")
    def trace_route_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "traceRouteEnabled"))

    @trace_route_enabled.setter
    def trace_route_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826eaf62591488bb31021aaa6b975089c53316d976b8d20df028f15cf54b73f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceRouteEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectionMonitorTestConfigurationTcpConfiguration]:
        return typing.cast(typing.Optional[NetworkConnectionMonitorTestConfigurationTcpConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectionMonitorTestConfigurationTcpConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67d39c3caeac5cdc2fab890e3aeb7dbf76856e4a5a374279233e52cf78a623d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestGroup",
    jsii_struct_bases=[],
    name_mapping={
        "destination_endpoints": "destinationEndpoints",
        "name": "name",
        "source_endpoints": "sourceEndpoints",
        "test_configuration_names": "testConfigurationNames",
        "enabled": "enabled",
    },
)
class NetworkConnectionMonitorTestGroup:
    def __init__(
        self,
        *,
        destination_endpoints: typing.Sequence[builtins.str],
        name: builtins.str,
        source_endpoints: typing.Sequence[builtins.str],
        test_configuration_names: typing.Sequence[builtins.str],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination_endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#destination_endpoints NetworkConnectionMonitor#destination_endpoints}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.
        :param source_endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#source_endpoints NetworkConnectionMonitor#source_endpoints}.
        :param test_configuration_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_configuration_names NetworkConnectionMonitor#test_configuration_names}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#enabled NetworkConnectionMonitor#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71669e8612eff2c576fab51058c3c9bbb68b6aa573d01523f7c99b2b6dc6b8b8)
            check_type(argname="argument destination_endpoints", value=destination_endpoints, expected_type=type_hints["destination_endpoints"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_endpoints", value=source_endpoints, expected_type=type_hints["source_endpoints"])
            check_type(argname="argument test_configuration_names", value=test_configuration_names, expected_type=type_hints["test_configuration_names"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_endpoints": destination_endpoints,
            "name": name,
            "source_endpoints": source_endpoints,
            "test_configuration_names": test_configuration_names,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def destination_endpoints(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#destination_endpoints NetworkConnectionMonitor#destination_endpoints}.'''
        result = self._values.get("destination_endpoints")
        assert result is not None, "Required property 'destination_endpoints' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#name NetworkConnectionMonitor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_endpoints(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#source_endpoints NetworkConnectionMonitor#source_endpoints}.'''
        result = self._values.get("source_endpoints")
        assert result is not None, "Required property 'source_endpoints' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def test_configuration_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#test_configuration_names NetworkConnectionMonitor#test_configuration_names}.'''
        result = self._values.get("test_configuration_names")
        assert result is not None, "Required property 'test_configuration_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#enabled NetworkConnectionMonitor#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorTestGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectionMonitorTestGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a1d3813d5f4e5c2bbbf6739f37d49729c5ea4f6e8b61911f7522bcbc8b46a32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectionMonitorTestGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba7b4595cf6f98b5f1702e2687d9a145d5e03102616bc754a96bd18c1669fef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectionMonitorTestGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310c643833437df243b36103a7377084afc87c9c51437e622c94eb500f43e98b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c4cfad8b6b849258a5bdc83599e1d3e9d6c51588202ca9466ee438325df30f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d38d39e6b2d9ae3498a320a7bfb365c4b3ca189037956ade69c1438482eb9ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5ad6a427e3502ccef3392f173cf829656b456e3012c99e36a9289c2c12ef96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectionMonitorTestGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTestGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55b84812859ac30186810f11b2270d02b12df1c0d9ab2b7a0029e6ff892b0acc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="destinationEndpointsInput")
    def destination_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceEndpointsInput")
    def source_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="testConfigurationNamesInput")
    def test_configuration_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "testConfigurationNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationEndpoints")
    def destination_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationEndpoints"))

    @destination_endpoints.setter
    def destination_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497bdf2ee9343a7cd49f1ad3d056de330ee289dad23ec82de965ef6a2a325af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationEndpoints", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__96762ea24c50cfa53d00044ec13abdabfaf744d94490c0f8fbffc2f24fed1b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c1cfca57bc59b47c195e09f022a83ee386cf81d1daead574eac076f5bd4831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceEndpoints")
    def source_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceEndpoints"))

    @source_endpoints.setter
    def source_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa609ac834cb639e5f6ee1183e15c2d30b6fde51d87f084e848a701e966da62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="testConfigurationNames")
    def test_configuration_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "testConfigurationNames"))

    @test_configuration_names.setter
    def test_configuration_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c42374c6d87163e65695c532e6cdb20e079cfa5d5c1d1da10220f4fd389bce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testConfigurationNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600d345d23606cb235ecc15c8d6e935a84b553b7dc108efee5a060e7d3c240e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class NetworkConnectionMonitorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#create NetworkConnectionMonitor#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#delete NetworkConnectionMonitor#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#read NetworkConnectionMonitor#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#update NetworkConnectionMonitor#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a43be0e9ff8325e92064eeb6ca250ca411edc2def702d16a49fc46f825ead4a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#create NetworkConnectionMonitor#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#delete NetworkConnectionMonitor#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#read NetworkConnectionMonitor#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/network_connection_monitor#update NetworkConnectionMonitor#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectionMonitorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectionMonitorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkConnectionMonitor.NetworkConnectionMonitorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d09ad98f151fe36c49293efa7b917fcd1a7462d5d964910e8a3285cf3f9feb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bf95722d0979efcabbec08988bd2042363a9e4e83b0069f83dff665c4f12e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b717c03118962d9b26b3cb9306ccf2a360f2a79b83820358eac9f0e28c3c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7da23e4155d914f53d40962e3cb95e213828cc207f8f1b5b85e765257cba4e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585e4d8376bb8b5ae94f51f844e9755adfdd1c2509075d9ea4f0bad01e0aa374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deba45e4cc0f4a6dedea15b419d6875505f1c417318bb2fdca78601860b768f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkConnectionMonitor",
    "NetworkConnectionMonitorConfig",
    "NetworkConnectionMonitorEndpoint",
    "NetworkConnectionMonitorEndpointFilter",
    "NetworkConnectionMonitorEndpointFilterItem",
    "NetworkConnectionMonitorEndpointFilterItemList",
    "NetworkConnectionMonitorEndpointFilterItemOutputReference",
    "NetworkConnectionMonitorEndpointFilterOutputReference",
    "NetworkConnectionMonitorEndpointList",
    "NetworkConnectionMonitorEndpointOutputReference",
    "NetworkConnectionMonitorTestConfiguration",
    "NetworkConnectionMonitorTestConfigurationHttpConfiguration",
    "NetworkConnectionMonitorTestConfigurationHttpConfigurationOutputReference",
    "NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader",
    "NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderList",
    "NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeaderOutputReference",
    "NetworkConnectionMonitorTestConfigurationIcmpConfiguration",
    "NetworkConnectionMonitorTestConfigurationIcmpConfigurationOutputReference",
    "NetworkConnectionMonitorTestConfigurationList",
    "NetworkConnectionMonitorTestConfigurationOutputReference",
    "NetworkConnectionMonitorTestConfigurationSuccessThreshold",
    "NetworkConnectionMonitorTestConfigurationSuccessThresholdOutputReference",
    "NetworkConnectionMonitorTestConfigurationTcpConfiguration",
    "NetworkConnectionMonitorTestConfigurationTcpConfigurationOutputReference",
    "NetworkConnectionMonitorTestGroup",
    "NetworkConnectionMonitorTestGroupList",
    "NetworkConnectionMonitorTestGroupOutputReference",
    "NetworkConnectionMonitorTimeouts",
    "NetworkConnectionMonitorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__efeb2263b9e8f2047993aa050439e63bc839de4a5f18f8698658d204ed74ac9d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    endpoint: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorEndpoint, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    network_watcher_id: builtins.str,
    test_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorTestConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    test_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorTestGroup, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    output_workspace_resource_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectionMonitorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__498af584221c2acbfdc17cc2d2647d00138fc0f24f538e59dd648d464a188344(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db1b91c21b1e7526f0caedf0065081e3321d7c5397b2304cccf6aa59b68cab2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorEndpoint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097a37ad95a3cb1182b06238b13ecad7b128bac37e9c40ce582bc16e97962122(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorTestConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79716f5b53c4d3afdda540520fb0b49c0a2da07386fca1cb0892c97b7067eb99(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorTestGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b79e871558c9611de761e5ad2efb3ab891ad24e717495a5d105b8dd5b6ac1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e06a2d242a254a9c5efa4aed4dd01d3029b88fc4528ffcb9e072c641f682d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42032b9c01e2d7eace088325fcb8bae25c931df4d596eaad779e630ba473843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b04ebc76bfac9c1153471d8c65f4de1526a5026d5bb3e343c3eb3845a38b1e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4053589c18b2fbe579f0d7857b4149c1dd6debe7a1e33ec8c6116dbdfe49684(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c702d0bb8ed0e6d1662ecb320791f8bed26eb192a5d159fd850574e5cb2f7381(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd89808c27f222231c091e14c2e41118856ac8abec661f5115faef145f39d2ac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e185fc9cb02694f9d4bd31eb9a48300293e8a858b1f9d4e8bee5311563e5c770(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    endpoint: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorEndpoint, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    network_watcher_id: builtins.str,
    test_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorTestConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    test_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorTestGroup, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    output_workspace_resource_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectionMonitorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a267c8456fa80545a4875041a9a1f03dc12cd0c7f7c6de585d8940fdd12467(
    *,
    name: builtins.str,
    address: typing.Optional[builtins.str] = None,
    coverage_level: typing.Optional[builtins.str] = None,
    excluded_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    filter: typing.Optional[typing.Union[NetworkConnectionMonitorEndpointFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    included_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_resource_id: typing.Optional[builtins.str] = None,
    target_resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6782b51724a65dcae9fd5b5b3910f42e1dcf143f02004de0ea6d02fdb75759cc(
    *,
    item: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorEndpointFilterItem, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d28e74df6700aebdfbb91866c019055a453a71ff7dc8542ce35c2819aea35c1(
    *,
    address: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc8ae9a5cc3fdc865209dd73ff1ea9b2aa438b49a297c9eac5dd7cfc4e23186(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b409a3827f7001c945d4ce4d1e167bcdba2e749d66548b9bcffaf6a7309fcc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbed295c8c3fa7798c5dae775d289982b379778db3343bdc74aa61e60126747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1c866e03f348444eb1297f35639a4428b8a3312709b2fd2199f2c958e1c27d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1272c4227605dde1d7ad961ae33f32b15063e1aabbc8955f260d5f7d8da74692(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c6255305852f52ee1b43dec901d5d1d9f4e6df45875f012a03d5f539acf780(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpointFilterItem]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f81ca72da70513a9233c9782051259e971c783b5eae8efa8506ffce38b1d4bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93899df4cb93c505fd5999c8267060b0d71cc01f8abbb69038847bc8145558ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__213376b7ca15691f096f3195ae8093e81a9fdc842bacb6c62e18dcd12afc35d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fad42b10b8900952ec2a3c130e7a5933dd8d48a75ed73e694a2805b4e8c216e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorEndpointFilterItem]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8c5ae9a6583744b4251bc9db34b1c8120d5aaa685ca3cabf2c9d84725591f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8fcab7d374f6477d279cdf7826c8e9357f063f8af63620b57d4d4f2fcc28eb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorEndpointFilterItem, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfa9fbcd40249115bd61388575a220c3252237b4dffc3a93aa3efe4c7bc7697(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2b3103801e478170bd5c692619cc9a7d2cefcb623640e7d9cfa7640e09878e(
    value: typing.Optional[NetworkConnectionMonitorEndpointFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b001ba5160b3a0eff34a726b77509c6877ad67e16abe245258433b3b67e9d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e188933606fabc3bd5ae482ebf6fd200d79c36f0dd8e5d034ef061b58feca1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fbb1bdd2318c1b9c5789683a7600093571a4557b12c26ad80c0cef67e07570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3924daa10188c7db354e197bb6c9b75a9c472cbf22f729890866f61572fe420b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428da51675a2153462da9210f35483fb54e3d57e6f56c184381f1fec1ca8dd06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e5d5c567a49c1eb738b79c906a697abd997a793fa30ddd40d5af97f62e3fd1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorEndpoint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2020bd1492a39eccc509ac9cb7d0ebef0151421459d8fa26e8446264bc5f1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd244fc0eb5e1699bae99601f47494de36fa54126be7b497cc49ef44cd686e59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c457e180a048ee7d390aa76fe98ee4b371da7c64cce435ede8ffd07aa02ee976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf57d00e2d5534d395bace32fb5d82f8158e6deef69530047025dc0b0d6056e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ac81b4752fda6bdba67ed1ffbfb919596b90724a2471e4ebefa0052713915b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef2c01a41c337db52bf8a948eda698cf12c8e449d539cd51a7be21909b0c2cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9841bf1eb3b8f373d754fbbd9e9b77df9eb2a91f022f8cdcc0d3c3dc79e4c3ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60cb13b9c6b7d16568478f701523243df139daf7bb886708a0c03dc748fced7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a87bff8c85ad425dd11b1fc248a758392a5d70a680684f5d0241af6626f0e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorEndpoint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bc766715c695c165fa93774edc517e0fe671453cefc1273b05f09798d84606(
    *,
    name: builtins.str,
    protocol: builtins.str,
    http_configuration: typing.Optional[typing.Union[NetworkConnectionMonitorTestConfigurationHttpConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    icmp_configuration: typing.Optional[typing.Union[NetworkConnectionMonitorTestConfigurationIcmpConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    preferred_ip_version: typing.Optional[builtins.str] = None,
    success_threshold: typing.Optional[typing.Union[NetworkConnectionMonitorTestConfigurationSuccessThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_configuration: typing.Optional[typing.Union[NetworkConnectionMonitorTestConfigurationTcpConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    test_frequency_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e27ca1a1e2eeb4b2554935e9c7def257929eeb4c2062e6ba996a88ff659ffa(
    *,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    prefer_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    valid_status_code_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd0962648fa1e4fb66f4bc5fe49af0a3dffaf610466ebed75601c747fd668f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b30c516c3819d550cb5a8150cc81f141bf27ed905c148a2f296716faaf8604(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740bf26090ba20de9384db058a7b2a1e03b3d0306aadd733fc34c8cfa22d57f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7616855ea1da84edb4003d29dd51807be76e6585cf098f5aa8e88b98febae6a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6a65daf3930aad26204ded1ed34e697394dc5f8cbcb5eb5bfac7142fefad08(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19951f17a5b977ba2a6342eedef6e6109a297f66fce7690c7a0c1292c9ee85e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82f033932f895e023096817dc5eb14689634d31fec205e28eb5d9226cdc9b7d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40c824e7ce6531b2fdab164745a83fda8be236b1e6aaa63492770c4f3ed578d(
    value: typing.Optional[NetworkConnectionMonitorTestConfigurationHttpConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59dbc35a057a35e23e9746ee0b1471d30bc799d32187dd22ee9377dfa2841537(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01a3c546c3dd6b15688be750144daf257fe8a948d34a7a975e1528ee5f5cf1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c4b90e4f4dd91b54673ab786c140af52f1c21a6eab56de8ef22c5a4aab8d9d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95fb3e1590a318945b5ca3b55f8ff2c6c82af84dbbb7c63fe063a396ef6e4c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2553f25c09bd47e0f7927d9a964edf357bdb9adda9fce09b0da2227a3dbeddc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04aaada8697edea6170fd231717cb15292f371331a87ec408002b5071a63aa4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8ec1e6e422597ac71ab0b0576801303d4eae7a3de6d740e8f79b8cac514615(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e352fbc1b54260c52390c01c8960bcfd9f9e408b1bf2f5c5992c249876e7112(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d42ee2a8ffb904012a0f122645d41f194674eae767006c094cf5f15af37413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baec934dc252f69de8ef65dc881a14ecee059f6e9d83c051408374f935134130(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2e894ea15d5b2bf6b2d90c30afedf86e68c35d6c7f01021c4f2b18919ead74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestConfigurationHttpConfigurationRequestHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2875a43d0c1407942d3755b697d5be7b36248a00ef2a7f0c6fc209d04edb52db(
    *,
    trace_route_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7727a84c08ae71cdb3f87202c44189a7747e417e75dbc644c65fa0cbaca2136(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285c03c605d7dbea3fc71a5cd9050ebd9ca91f40af524005b47f64738aff512e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f8e9b4f35e44bf720077f745f615a5e5ad04f29ed5540abdfcd91284b6cc03(
    value: typing.Optional[NetworkConnectionMonitorTestConfigurationIcmpConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a42f6aae9d5941198b7103514b53fa9d35c41135f6323768ebf4529227efe9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544bac76e94c40f170a13ab55fbb5ec2f04c5cb94057267773153b47081bef45(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1975ed42fad1b61b6d128bc07b8aa3f79ba1af2694868c9d92fc2f2db06eeb35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe3555fa4f54a9c83acba06f88d493e4ffc499babf2c24c1a60c159a648234a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b007edf40aa562485e9c38bb7b56dcb464b42eb14a180cebb80b75366df3cea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e07f1562df7b640e66a243c8f499dca9bdf14617d2c247186a07731b48cfbe7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebd9aeed1e8a596d3a2a38c300ff0f56ea24efa7e535300eabd2d936f9ec0c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3191b005590b3bfd428aa5a27ed6c5fd8e7f1d6793aa0ae4b57908495c2755dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5544c6f0995a949c61eb2c80e5a87680566e2e7b96e333a3e9188dd1ebf997a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e42ace2a72d2abc175791e75d27e6919c4527d9a8ac760154f2afe88853d696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cbc20f7873d69b31b226c18cc268d49d837e15431b5d65e6ff111c35da0731(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963ac32a3a167cb200f124b8d4d1063857ff5f895d1827db50b7bb44cfcf97b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92afb86b807f8a1e9f58c9d58f126e77c858c03bf880c9c9013c84c136684cc(
    *,
    checks_failed_percent: typing.Optional[jsii.Number] = None,
    round_trip_time_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea12a80cc0c8327ca68c3aa2d372a23860475725cbef4c9f5fd009aedad9b900(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7937ea7b90203410375d415e85b9d9c2390935b3a5c4058c48c62543732ef3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb64faad1f831d0b1fb34fd08911430b36232cbc047da5e85c6383617c5a5ea8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac45654f793f9a640d55a9e19ea60bbb82769be2dcac8e227aa0ae5654fc0ab(
    value: typing.Optional[NetworkConnectionMonitorTestConfigurationSuccessThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1f3cd27e3140b5ae9035c85c266a727c61c01bb097cab1e1f8ce075c47f895(
    *,
    port: jsii.Number,
    destination_port_behavior: typing.Optional[builtins.str] = None,
    trace_route_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82387cf50b0eacb846df1f7fe90e55a3b9475189f800a8928ce3b89753b1ec7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9357ea4de89fc6c8493046983a11bece2f14a84028ccbf000cd4f95b68c35e4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618a760ace22c4fc732552d90dfddada6db9299612b06251c478dcac2fde588c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826eaf62591488bb31021aaa6b975089c53316d976b8d20df028f15cf54b73f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67d39c3caeac5cdc2fab890e3aeb7dbf76856e4a5a374279233e52cf78a623d(
    value: typing.Optional[NetworkConnectionMonitorTestConfigurationTcpConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71669e8612eff2c576fab51058c3c9bbb68b6aa573d01523f7c99b2b6dc6b8b8(
    *,
    destination_endpoints: typing.Sequence[builtins.str],
    name: builtins.str,
    source_endpoints: typing.Sequence[builtins.str],
    test_configuration_names: typing.Sequence[builtins.str],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1d3813d5f4e5c2bbbf6739f37d49729c5ea4f6e8b61911f7522bcbc8b46a32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba7b4595cf6f98b5f1702e2687d9a145d5e03102616bc754a96bd18c1669fef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310c643833437df243b36103a7377084afc87c9c51437e622c94eb500f43e98b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4cfad8b6b849258a5bdc83599e1d3e9d6c51588202ca9466ee438325df30f2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38d39e6b2d9ae3498a320a7bfb365c4b3ca189037956ade69c1438482eb9ea4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5ad6a427e3502ccef3392f173cf829656b456e3012c99e36a9289c2c12ef96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectionMonitorTestGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b84812859ac30186810f11b2270d02b12df1c0d9ab2b7a0029e6ff892b0acc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497bdf2ee9343a7cd49f1ad3d056de330ee289dad23ec82de965ef6a2a325af1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96762ea24c50cfa53d00044ec13abdabfaf744d94490c0f8fbffc2f24fed1b2a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c1cfca57bc59b47c195e09f022a83ee386cf81d1daead574eac076f5bd4831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa609ac834cb639e5f6ee1183e15c2d30b6fde51d87f084e848a701e966da62(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c42374c6d87163e65695c532e6cdb20e079cfa5d5c1d1da10220f4fd389bce9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600d345d23606cb235ecc15c8d6e935a84b553b7dc108efee5a060e7d3c240e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTestGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a43be0e9ff8325e92064eeb6ca250ca411edc2def702d16a49fc46f825ead4a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d09ad98f151fe36c49293efa7b917fcd1a7462d5d964910e8a3285cf3f9feb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf95722d0979efcabbec08988bd2042363a9e4e83b0069f83dff665c4f12e12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b717c03118962d9b26b3cb9306ccf2a360f2a79b83820358eac9f0e28c3c9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7da23e4155d914f53d40962e3cb95e213828cc207f8f1b5b85e765257cba4e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585e4d8376bb8b5ae94f51f844e9755adfdd1c2509075d9ea4f0bad01e0aa374(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deba45e4cc0f4a6dedea15b419d6875505f1c417318bb2fdca78601860b768f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectionMonitorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
