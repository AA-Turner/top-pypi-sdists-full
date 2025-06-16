r'''
# `google_vmwareengine_external_access_rule`

Refer to the Terraform Registry for docs: [`google_vmwareengine_external_access_rule`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule).
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


class GoogleVmwareengineExternalAccessRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule google_vmwareengine_external_access_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        destination_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineExternalAccessRuleDestinationIpRanges", typing.Dict[builtins.str, typing.Any]]]],
        destination_ports: typing.Sequence[builtins.str],
        ip_protocol: builtins.str,
        name: builtins.str,
        parent: builtins.str,
        priority: jsii.Number,
        source_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineExternalAccessRuleSourceIpRanges", typing.Dict[builtins.str, typing.Any]]]],
        source_ports: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVmwareengineExternalAccessRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule google_vmwareengine_external_access_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: The action that the external access rule performs. Possible values: ["ALLOW", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#action GoogleVmwareengineExternalAccessRule#action}
        :param destination_ip_ranges: destination_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#destination_ip_ranges GoogleVmwareengineExternalAccessRule#destination_ip_ranges}
        :param destination_ports: A list of destination ports to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#destination_ports GoogleVmwareengineExternalAccessRule#destination_ports}
        :param ip_protocol: The IP protocol to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#ip_protocol GoogleVmwareengineExternalAccessRule#ip_protocol}
        :param name: The ID of the external access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#name GoogleVmwareengineExternalAccessRule#name}
        :param parent: The resource name of the network policy. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/networkPolicies/my-policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#parent GoogleVmwareengineExternalAccessRule#parent}
        :param priority: External access rule priority, which determines the external access rule to use when multiple rules apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#priority GoogleVmwareengineExternalAccessRule#priority}
        :param source_ip_ranges: source_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#source_ip_ranges GoogleVmwareengineExternalAccessRule#source_ip_ranges}
        :param source_ports: A list of source ports to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#source_ports GoogleVmwareengineExternalAccessRule#source_ports}
        :param description: User-provided description for the external access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#description GoogleVmwareengineExternalAccessRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#id GoogleVmwareengineExternalAccessRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#timeouts GoogleVmwareengineExternalAccessRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e260f2086ce46122655de069106afc538214ff7fcd2684ebdc3da1d964dde46)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVmwareengineExternalAccessRuleConfig(
            action=action,
            destination_ip_ranges=destination_ip_ranges,
            destination_ports=destination_ports,
            ip_protocol=ip_protocol,
            name=name,
            parent=parent,
            priority=priority,
            source_ip_ranges=source_ip_ranges,
            source_ports=source_ports,
            description=description,
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
        '''Generates CDKTF code for importing a GoogleVmwareengineExternalAccessRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVmwareengineExternalAccessRule to import.
        :param import_from_id: The id of the existing GoogleVmwareengineExternalAccessRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVmwareengineExternalAccessRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da14d668ac5ce2a0927c6faed7f413829c574d6e1130c8eb00f9e70e9432047)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationIpRanges")
    def put_destination_ip_ranges(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineExternalAccessRuleDestinationIpRanges", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cbf7ec885f1302e1214b0ac1d31aafe461cc8e887010dabfbe773f4e0c77c60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinationIpRanges", [value]))

    @jsii.member(jsii_name="putSourceIpRanges")
    def put_source_ip_ranges(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineExternalAccessRuleSourceIpRanges", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504ce638c242aec6d14bb003a5e8f77226184e1f8a478fc37f74c636d266007f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSourceIpRanges", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#create GoogleVmwareengineExternalAccessRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#delete GoogleVmwareengineExternalAccessRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#update GoogleVmwareengineExternalAccessRule#update}.
        '''
        value = GoogleVmwareengineExternalAccessRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="destinationIpRanges")
    def destination_ip_ranges(
        self,
    ) -> "GoogleVmwareengineExternalAccessRuleDestinationIpRangesList":
        return typing.cast("GoogleVmwareengineExternalAccessRuleDestinationIpRangesList", jsii.get(self, "destinationIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="sourceIpRanges")
    def source_ip_ranges(
        self,
    ) -> "GoogleVmwareengineExternalAccessRuleSourceIpRangesList":
        return typing.cast("GoogleVmwareengineExternalAccessRuleSourceIpRangesList", jsii.get(self, "sourceIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleVmwareengineExternalAccessRuleTimeoutsOutputReference":
        return typing.cast("GoogleVmwareengineExternalAccessRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationIpRangesInput")
    def destination_ip_ranges_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineExternalAccessRuleDestinationIpRanges"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineExternalAccessRuleDestinationIpRanges"]]], jsii.get(self, "destinationIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPortsInput")
    def destination_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIpRangesInput")
    def source_ip_ranges_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineExternalAccessRuleSourceIpRanges"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineExternalAccessRuleSourceIpRanges"]]], jsii.get(self, "sourceIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePortsInput")
    def source_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcePortsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVmwareengineExternalAccessRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVmwareengineExternalAccessRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547013b89b551c7acf6277e3c4a7475275342a5ec1fccd6857a2e2201e896c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3634866c83411953dcdd4658d44382b72e7cbdaea72e70d17c323514e09726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationPorts")
    def destination_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationPorts"))

    @destination_ports.setter
    def destination_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d205d47ffee7e81b6779a5045a4993f41a5fff6475ae03ba88316dbcadc750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8907f6ba255612e3c6c672e18bc38506be31d3f8cbd9dea44e3d60f39add0b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b19731b3d351481b14f1f6fdd2888fb7c0db4ee0620f5cbbea0dcba7733aadca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f880e6b004bbfcc0ee56db7c08e140bbc36db1e820fb030e7049dec2b345d76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe65224ffc6f309a09d26301388c88daac8b4cff523adbcca62ba6f5156e881f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec9aa3df70569c34424ec079d25a4f0d719e0852129d7db4e9809aa268ae459)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePorts")
    def source_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourcePorts"))

    @source_ports.setter
    def source_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5b978c69a9b41452130e4a2668d8287e784aca7dffef64bb204963c42949aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePorts", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRuleConfig",
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
        "destination_ip_ranges": "destinationIpRanges",
        "destination_ports": "destinationPorts",
        "ip_protocol": "ipProtocol",
        "name": "name",
        "parent": "parent",
        "priority": "priority",
        "source_ip_ranges": "sourceIpRanges",
        "source_ports": "sourcePorts",
        "description": "description",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class GoogleVmwareengineExternalAccessRuleConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        destination_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineExternalAccessRuleDestinationIpRanges", typing.Dict[builtins.str, typing.Any]]]],
        destination_ports: typing.Sequence[builtins.str],
        ip_protocol: builtins.str,
        name: builtins.str,
        parent: builtins.str,
        priority: jsii.Number,
        source_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineExternalAccessRuleSourceIpRanges", typing.Dict[builtins.str, typing.Any]]]],
        source_ports: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVmwareengineExternalAccessRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: The action that the external access rule performs. Possible values: ["ALLOW", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#action GoogleVmwareengineExternalAccessRule#action}
        :param destination_ip_ranges: destination_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#destination_ip_ranges GoogleVmwareengineExternalAccessRule#destination_ip_ranges}
        :param destination_ports: A list of destination ports to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#destination_ports GoogleVmwareengineExternalAccessRule#destination_ports}
        :param ip_protocol: The IP protocol to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#ip_protocol GoogleVmwareengineExternalAccessRule#ip_protocol}
        :param name: The ID of the external access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#name GoogleVmwareengineExternalAccessRule#name}
        :param parent: The resource name of the network policy. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/networkPolicies/my-policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#parent GoogleVmwareengineExternalAccessRule#parent}
        :param priority: External access rule priority, which determines the external access rule to use when multiple rules apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#priority GoogleVmwareengineExternalAccessRule#priority}
        :param source_ip_ranges: source_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#source_ip_ranges GoogleVmwareengineExternalAccessRule#source_ip_ranges}
        :param source_ports: A list of source ports to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#source_ports GoogleVmwareengineExternalAccessRule#source_ports}
        :param description: User-provided description for the external access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#description GoogleVmwareengineExternalAccessRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#id GoogleVmwareengineExternalAccessRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#timeouts GoogleVmwareengineExternalAccessRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleVmwareengineExternalAccessRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d99c556284904ea7ed182fd27ece45ba6cd89bc659f5e823ba209239bdaca317)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument destination_ip_ranges", value=destination_ip_ranges, expected_type=type_hints["destination_ip_ranges"])
            check_type(argname="argument destination_ports", value=destination_ports, expected_type=type_hints["destination_ports"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument source_ip_ranges", value=source_ip_ranges, expected_type=type_hints["source_ip_ranges"])
            check_type(argname="argument source_ports", value=source_ports, expected_type=type_hints["source_ports"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "destination_ip_ranges": destination_ip_ranges,
            "destination_ports": destination_ports,
            "ip_protocol": ip_protocol,
            "name": name,
            "parent": parent,
            "priority": priority,
            "source_ip_ranges": source_ip_ranges,
            "source_ports": source_ports,
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
    def action(self) -> builtins.str:
        '''The action that the external access rule performs. Possible values: ["ALLOW", "DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#action GoogleVmwareengineExternalAccessRule#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_ip_ranges(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineExternalAccessRuleDestinationIpRanges"]]:
        '''destination_ip_ranges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#destination_ip_ranges GoogleVmwareengineExternalAccessRule#destination_ip_ranges}
        '''
        result = self._values.get("destination_ip_ranges")
        assert result is not None, "Required property 'destination_ip_ranges' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineExternalAccessRuleDestinationIpRanges"]], result)

    @builtins.property
    def destination_ports(self) -> typing.List[builtins.str]:
        '''A list of destination ports to which the external access rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#destination_ports GoogleVmwareengineExternalAccessRule#destination_ports}
        '''
        result = self._values.get("destination_ports")
        assert result is not None, "Required property 'destination_ports' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The IP protocol to which the external access rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#ip_protocol GoogleVmwareengineExternalAccessRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The ID of the external access rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#name GoogleVmwareengineExternalAccessRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The resource name of the network policy. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/networkPolicies/my-policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#parent GoogleVmwareengineExternalAccessRule#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''External access rule priority, which determines the external access rule to use when multiple rules apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#priority GoogleVmwareengineExternalAccessRule#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def source_ip_ranges(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineExternalAccessRuleSourceIpRanges"]]:
        '''source_ip_ranges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#source_ip_ranges GoogleVmwareengineExternalAccessRule#source_ip_ranges}
        '''
        result = self._values.get("source_ip_ranges")
        assert result is not None, "Required property 'source_ip_ranges' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineExternalAccessRuleSourceIpRanges"]], result)

    @builtins.property
    def source_ports(self) -> typing.List[builtins.str]:
        '''A list of source ports to which the external access rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#source_ports GoogleVmwareengineExternalAccessRule#source_ports}
        '''
        result = self._values.get("source_ports")
        assert result is not None, "Required property 'source_ports' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description for the external access rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#description GoogleVmwareengineExternalAccessRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#id GoogleVmwareengineExternalAccessRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleVmwareengineExternalAccessRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#timeouts GoogleVmwareengineExternalAccessRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVmwareengineExternalAccessRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineExternalAccessRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRuleDestinationIpRanges",
    jsii_struct_bases=[],
    name_mapping={
        "external_address": "externalAddress",
        "ip_address_range": "ipAddressRange",
    },
)
class GoogleVmwareengineExternalAccessRuleDestinationIpRanges:
    def __init__(
        self,
        *,
        external_address: typing.Optional[builtins.str] = None,
        ip_address_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_address: The name of an 'ExternalAddress' resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#external_address GoogleVmwareengineExternalAccessRule#external_address}
        :param ip_address_range: An IP address range in the CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#ip_address_range GoogleVmwareengineExternalAccessRule#ip_address_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f949eda1e74f7ecb2f5e788bb18ff416a8598b5d306f04c7026711efee61099)
            check_type(argname="argument external_address", value=external_address, expected_type=type_hints["external_address"])
            check_type(argname="argument ip_address_range", value=ip_address_range, expected_type=type_hints["ip_address_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_address is not None:
            self._values["external_address"] = external_address
        if ip_address_range is not None:
            self._values["ip_address_range"] = ip_address_range

    @builtins.property
    def external_address(self) -> typing.Optional[builtins.str]:
        '''The name of an 'ExternalAddress' resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#external_address GoogleVmwareengineExternalAccessRule#external_address}
        '''
        result = self._values.get("external_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_range(self) -> typing.Optional[builtins.str]:
        '''An IP address range in the CIDR format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#ip_address_range GoogleVmwareengineExternalAccessRule#ip_address_range}
        '''
        result = self._values.get("ip_address_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineExternalAccessRuleDestinationIpRanges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareengineExternalAccessRuleDestinationIpRangesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRuleDestinationIpRangesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9da4521c657fc355e0ae1a69902d8d7ff7cc2b3e68a0f28c92e0592f1731099f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVmwareengineExternalAccessRuleDestinationIpRangesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fe6e0cc9032cc39e50863f198f988aaa1a876524c88213dcb8cb6a0de4fede)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVmwareengineExternalAccessRuleDestinationIpRangesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0e8232b387cf46a2a7a4d76a0bdf51e6a6052b5ee0cdd5bab1227a1c3f553e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd35de599bf986e5e972c9dbc08e87fa2b6eefce605a91bcc4eda99dc27a3af5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37e04780b316fcf749ace6761e885844e43db8b76ee4e9c5de37d91b4569cbda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineExternalAccessRuleDestinationIpRanges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineExternalAccessRuleDestinationIpRanges]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineExternalAccessRuleDestinationIpRanges]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac39076134d9dd24aad0216570de9ae6033cea42d5e835ef5db24dd84693c7dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareengineExternalAccessRuleDestinationIpRangesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRuleDestinationIpRangesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ec368721137a8b2de515824a92b79c3a68cc2ee901aef829747aa8baaecc276)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExternalAddress")
    def reset_external_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAddress", []))

    @jsii.member(jsii_name="resetIpAddressRange")
    def reset_ip_address_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddressRange", []))

    @builtins.property
    @jsii.member(jsii_name="externalAddressInput")
    def external_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressRangeInput")
    def ip_address_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAddress")
    def external_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAddress"))

    @external_address.setter
    def external_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f095f9ff4a37c5de0128a3412d0d2577a89f0fba66b544a5ed37b68422cbdbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressRange")
    def ip_address_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressRange"))

    @ip_address_range.setter
    def ip_address_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daaa7cf88434b1f1c25a4ef3cbff39e32d5ef0389751c902b89c546196a3360d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleDestinationIpRanges]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleDestinationIpRanges]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleDestinationIpRanges]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d448d7f9ef49dddea5431d733f061d8aeebf43e361bab86f8d3fa284b70ad73b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRuleSourceIpRanges",
    jsii_struct_bases=[],
    name_mapping={"ip_address": "ipAddress", "ip_address_range": "ipAddressRange"},
)
class GoogleVmwareengineExternalAccessRuleSourceIpRanges:
    def __init__(
        self,
        *,
        ip_address: typing.Optional[builtins.str] = None,
        ip_address_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: A single IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#ip_address GoogleVmwareengineExternalAccessRule#ip_address}
        :param ip_address_range: An IP address range in the CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#ip_address_range GoogleVmwareengineExternalAccessRule#ip_address_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de0f8bdae732330b4ca31ad1c905509d5c9357b345b82df5ba97fd56e4ee3f7)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_address_range", value=ip_address_range, expected_type=type_hints["ip_address_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if ip_address_range is not None:
            self._values["ip_address_range"] = ip_address_range

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''A single IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#ip_address GoogleVmwareengineExternalAccessRule#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_range(self) -> typing.Optional[builtins.str]:
        '''An IP address range in the CIDR format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#ip_address_range GoogleVmwareengineExternalAccessRule#ip_address_range}
        '''
        result = self._values.get("ip_address_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineExternalAccessRuleSourceIpRanges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareengineExternalAccessRuleSourceIpRangesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRuleSourceIpRangesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad806c6b9dabc4cb37d2dd4364ffeb3fd55a4ec95711a1a9eb736f6a482fa656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVmwareengineExternalAccessRuleSourceIpRangesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c502caeb8a07688baf768c4db2409810e49730b0d6a65ac7aa4d11cfcee848f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVmwareengineExternalAccessRuleSourceIpRangesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c54fd8f9dcbe75fa351c89cd91f6a87181d8af8956fb2b46bcc4e21f2ab5fa8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a68eb023e78e1f0ced5590eaa105aa4601e45f1ce9ec17d35f96403bb7cef06c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__205f0edb2ee38d414400c9732d1946aa4f97e5bc4daace1ab3e90ff256f9a266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineExternalAccessRuleSourceIpRanges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineExternalAccessRuleSourceIpRanges]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineExternalAccessRuleSourceIpRanges]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db326bd53302bd6a0b730dce7c147ff0c66055e1e1a0f61ff73fdf04c266bdcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareengineExternalAccessRuleSourceIpRangesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRuleSourceIpRangesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3db00f8344b891a5a96e1085b862ca9f929fdebc6893688a8070f2633e8083f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetIpAddressRange")
    def reset_ip_address_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddressRange", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressRangeInput")
    def ip_address_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd8d78341d5ed6ed3a1c6a9416b874be0e32aee2e02ae19963b22b95cba88c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressRange")
    def ip_address_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressRange"))

    @ip_address_range.setter
    def ip_address_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad3adcd56577f1a6f7ff54d4c6cdf477713809dd35e272bedea6c3ea1504f21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleSourceIpRanges]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleSourceIpRanges]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleSourceIpRanges]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31adca4aa4657ca6fc131f9554fd224728e32f99f1d2bc6b9f969e108d41d678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVmwareengineExternalAccessRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#create GoogleVmwareengineExternalAccessRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#delete GoogleVmwareengineExternalAccessRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#update GoogleVmwareengineExternalAccessRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd91ad852fa1b18643e0c420ef0c0886590833c986822dac0106097cd6b36cb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#create GoogleVmwareengineExternalAccessRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#delete GoogleVmwareengineExternalAccessRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_external_access_rule#update GoogleVmwareengineExternalAccessRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineExternalAccessRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareengineExternalAccessRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineExternalAccessRule.GoogleVmwareengineExternalAccessRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bd9163d7192120677b53f8b73191a9c19ea18d2dbf27e594b38ae334c1bc86e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__791e03455e78b528396dde62d9c1d427b3a88e7542d8dc375ee409bade691fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4abf82f9dfc763a5789cdb1631a69432a201a1c87251f83d72fd01e8b8912325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09dd3cd09339bc50ace9c47c1b492c58eed133ed17c287b7bf4dd008f15ec57c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a38f4b2508416af9890297bfd1738c24add6dc589a1cafe988b960d708062fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVmwareengineExternalAccessRule",
    "GoogleVmwareengineExternalAccessRuleConfig",
    "GoogleVmwareengineExternalAccessRuleDestinationIpRanges",
    "GoogleVmwareengineExternalAccessRuleDestinationIpRangesList",
    "GoogleVmwareengineExternalAccessRuleDestinationIpRangesOutputReference",
    "GoogleVmwareengineExternalAccessRuleSourceIpRanges",
    "GoogleVmwareengineExternalAccessRuleSourceIpRangesList",
    "GoogleVmwareengineExternalAccessRuleSourceIpRangesOutputReference",
    "GoogleVmwareengineExternalAccessRuleTimeouts",
    "GoogleVmwareengineExternalAccessRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6e260f2086ce46122655de069106afc538214ff7fcd2684ebdc3da1d964dde46(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    destination_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineExternalAccessRuleDestinationIpRanges, typing.Dict[builtins.str, typing.Any]]]],
    destination_ports: typing.Sequence[builtins.str],
    ip_protocol: builtins.str,
    name: builtins.str,
    parent: builtins.str,
    priority: jsii.Number,
    source_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineExternalAccessRuleSourceIpRanges, typing.Dict[builtins.str, typing.Any]]]],
    source_ports: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVmwareengineExternalAccessRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3da14d668ac5ce2a0927c6faed7f413829c574d6e1130c8eb00f9e70e9432047(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cbf7ec885f1302e1214b0ac1d31aafe461cc8e887010dabfbe773f4e0c77c60(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineExternalAccessRuleDestinationIpRanges, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504ce638c242aec6d14bb003a5e8f77226184e1f8a478fc37f74c636d266007f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineExternalAccessRuleSourceIpRanges, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547013b89b551c7acf6277e3c4a7475275342a5ec1fccd6857a2e2201e896c78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3634866c83411953dcdd4658d44382b72e7cbdaea72e70d17c323514e09726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d205d47ffee7e81b6779a5045a4993f41a5fff6475ae03ba88316dbcadc750(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8907f6ba255612e3c6c672e18bc38506be31d3f8cbd9dea44e3d60f39add0b9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19731b3d351481b14f1f6fdd2888fb7c0db4ee0620f5cbbea0dcba7733aadca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f880e6b004bbfcc0ee56db7c08e140bbc36db1e820fb030e7049dec2b345d76d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe65224ffc6f309a09d26301388c88daac8b4cff523adbcca62ba6f5156e881f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec9aa3df70569c34424ec079d25a4f0d719e0852129d7db4e9809aa268ae459(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5b978c69a9b41452130e4a2668d8287e784aca7dffef64bb204963c42949aa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99c556284904ea7ed182fd27ece45ba6cd89bc659f5e823ba209239bdaca317(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    destination_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineExternalAccessRuleDestinationIpRanges, typing.Dict[builtins.str, typing.Any]]]],
    destination_ports: typing.Sequence[builtins.str],
    ip_protocol: builtins.str,
    name: builtins.str,
    parent: builtins.str,
    priority: jsii.Number,
    source_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineExternalAccessRuleSourceIpRanges, typing.Dict[builtins.str, typing.Any]]]],
    source_ports: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVmwareengineExternalAccessRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f949eda1e74f7ecb2f5e788bb18ff416a8598b5d306f04c7026711efee61099(
    *,
    external_address: typing.Optional[builtins.str] = None,
    ip_address_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da4521c657fc355e0ae1a69902d8d7ff7cc2b3e68a0f28c92e0592f1731099f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fe6e0cc9032cc39e50863f198f988aaa1a876524c88213dcb8cb6a0de4fede(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0e8232b387cf46a2a7a4d76a0bdf51e6a6052b5ee0cdd5bab1227a1c3f553e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd35de599bf986e5e972c9dbc08e87fa2b6eefce605a91bcc4eda99dc27a3af5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e04780b316fcf749ace6761e885844e43db8b76ee4e9c5de37d91b4569cbda(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac39076134d9dd24aad0216570de9ae6033cea42d5e835ef5db24dd84693c7dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineExternalAccessRuleDestinationIpRanges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec368721137a8b2de515824a92b79c3a68cc2ee901aef829747aa8baaecc276(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f095f9ff4a37c5de0128a3412d0d2577a89f0fba66b544a5ed37b68422cbdbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daaa7cf88434b1f1c25a4ef3cbff39e32d5ef0389751c902b89c546196a3360d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d448d7f9ef49dddea5431d733f061d8aeebf43e361bab86f8d3fa284b70ad73b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleDestinationIpRanges]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de0f8bdae732330b4ca31ad1c905509d5c9357b345b82df5ba97fd56e4ee3f7(
    *,
    ip_address: typing.Optional[builtins.str] = None,
    ip_address_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad806c6b9dabc4cb37d2dd4364ffeb3fd55a4ec95711a1a9eb736f6a482fa656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c502caeb8a07688baf768c4db2409810e49730b0d6a65ac7aa4d11cfcee848f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c54fd8f9dcbe75fa351c89cd91f6a87181d8af8956fb2b46bcc4e21f2ab5fa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68eb023e78e1f0ced5590eaa105aa4601e45f1ce9ec17d35f96403bb7cef06c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205f0edb2ee38d414400c9732d1946aa4f97e5bc4daace1ab3e90ff256f9a266(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db326bd53302bd6a0b730dce7c147ff0c66055e1e1a0f61ff73fdf04c266bdcd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineExternalAccessRuleSourceIpRanges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3db00f8344b891a5a96e1085b862ca9f929fdebc6893688a8070f2633e8083f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd8d78341d5ed6ed3a1c6a9416b874be0e32aee2e02ae19963b22b95cba88c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad3adcd56577f1a6f7ff54d4c6cdf477713809dd35e272bedea6c3ea1504f21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31adca4aa4657ca6fc131f9554fd224728e32f99f1d2bc6b9f969e108d41d678(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleSourceIpRanges]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd91ad852fa1b18643e0c420ef0c0886590833c986822dac0106097cd6b36cb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd9163d7192120677b53f8b73191a9c19ea18d2dbf27e594b38ae334c1bc86e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791e03455e78b528396dde62d9c1d427b3a88e7542d8dc375ee409bade691fa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abf82f9dfc763a5789cdb1631a69432a201a1c87251f83d72fd01e8b8912325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09dd3cd09339bc50ace9c47c1b492c58eed133ed17c287b7bf4dd008f15ec57c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a38f4b2508416af9890297bfd1738c24add6dc589a1cafe988b960d708062fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineExternalAccessRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
