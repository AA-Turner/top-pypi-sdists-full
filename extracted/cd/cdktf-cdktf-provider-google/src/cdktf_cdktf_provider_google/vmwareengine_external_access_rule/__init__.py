r'''
# `google_vmwareengine_external_access_rule`

Refer to the Terraform Registry for docs: [`google_vmwareengine_external_access_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule).
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


class VmwareengineExternalAccessRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule google_vmwareengine_external_access_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        destination_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineExternalAccessRuleDestinationIpRanges", typing.Dict[builtins.str, typing.Any]]]],
        destination_ports: typing.Sequence[builtins.str],
        ip_protocol: builtins.str,
        name: builtins.str,
        parent: builtins.str,
        priority: jsii.Number,
        source_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineExternalAccessRuleSourceIpRanges", typing.Dict[builtins.str, typing.Any]]]],
        source_ports: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VmwareengineExternalAccessRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule google_vmwareengine_external_access_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: The action that the external access rule performs. Possible values: ["ALLOW", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#action VmwareengineExternalAccessRule#action}
        :param destination_ip_ranges: destination_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#destination_ip_ranges VmwareengineExternalAccessRule#destination_ip_ranges}
        :param destination_ports: A list of destination ports to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#destination_ports VmwareengineExternalAccessRule#destination_ports}
        :param ip_protocol: The IP protocol to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#ip_protocol VmwareengineExternalAccessRule#ip_protocol}
        :param name: The ID of the external access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#name VmwareengineExternalAccessRule#name}
        :param parent: The resource name of the network policy. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/networkPolicies/my-policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#parent VmwareengineExternalAccessRule#parent}
        :param priority: External access rule priority, which determines the external access rule to use when multiple rules apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#priority VmwareengineExternalAccessRule#priority}
        :param source_ip_ranges: source_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#source_ip_ranges VmwareengineExternalAccessRule#source_ip_ranges}
        :param source_ports: A list of source ports to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#source_ports VmwareengineExternalAccessRule#source_ports}
        :param description: User-provided description for the external access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#description VmwareengineExternalAccessRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#id VmwareengineExternalAccessRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#timeouts VmwareengineExternalAccessRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8642c7d85fef153218859ca4ac409131dd40a936559d8e1d547828a8d6c1f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VmwareengineExternalAccessRuleConfig(
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
        '''Generates CDKTF code for importing a VmwareengineExternalAccessRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VmwareengineExternalAccessRule to import.
        :param import_from_id: The id of the existing VmwareengineExternalAccessRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VmwareengineExternalAccessRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d834136189aa413a3abc072933d219b5f0fd62c0dcd9e98710fe142ab16bd19e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationIpRanges")
    def put_destination_ip_ranges(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineExternalAccessRuleDestinationIpRanges", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3d2d71437123bb1c3b5deaac7356c1b077c818db62dcb765781417d4bca477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinationIpRanges", [value]))

    @jsii.member(jsii_name="putSourceIpRanges")
    def put_source_ip_ranges(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineExternalAccessRuleSourceIpRanges", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6488bce5e0c59e5929e3de4f8f61450a4c8fa4b44c463bd59d2b0a463da9a9b)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#create VmwareengineExternalAccessRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#delete VmwareengineExternalAccessRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#update VmwareengineExternalAccessRule#update}.
        '''
        value = VmwareengineExternalAccessRuleTimeouts(
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
    ) -> "VmwareengineExternalAccessRuleDestinationIpRangesList":
        return typing.cast("VmwareengineExternalAccessRuleDestinationIpRangesList", jsii.get(self, "destinationIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="sourceIpRanges")
    def source_ip_ranges(self) -> "VmwareengineExternalAccessRuleSourceIpRangesList":
        return typing.cast("VmwareengineExternalAccessRuleSourceIpRangesList", jsii.get(self, "sourceIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VmwareengineExternalAccessRuleTimeoutsOutputReference":
        return typing.cast("VmwareengineExternalAccessRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineExternalAccessRuleDestinationIpRanges"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineExternalAccessRuleDestinationIpRanges"]]], jsii.get(self, "destinationIpRangesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineExternalAccessRuleSourceIpRanges"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineExternalAccessRuleSourceIpRanges"]]], jsii.get(self, "sourceIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePortsInput")
    def source_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcePortsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VmwareengineExternalAccessRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VmwareengineExternalAccessRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1deb69a94c25684dbb5e4972ef08b4273d71fba185c9457cca0a65469897dbd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80029a6b8b492c66c99b598274b75da065944288405254bf694366a25dc4de14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationPorts")
    def destination_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationPorts"))

    @destination_ports.setter
    def destination_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455bb5fc64c3093194538e0413d7b7a3a6068ae95b5f12c285d430a886ccd2a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f16788c670b96427e7db55f454f83b9a4d6fa70c7cd95801a2a70e4907769c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590dc85226ed8c48a9c75763c2f6201546f830f8b5f973b3b9b8cb2e5c7a991d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e691368b6acf5a638919304c9abce04f279c9e8990886d117967d8987c9a2f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7276f585c2fd99f08eaadf76a34f7e7602baf7c9ffc2b9c1227c404c60e1552c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c311645d0e3078041fe239806662f0532b7d863534f0fc3a2a45f67475948f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePorts")
    def source_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourcePorts"))

    @source_ports.setter
    def source_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e91806b923d3acb4029774666eb1ec3c245374614969142b8b57d296c31b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePorts", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRuleConfig",
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
class VmwareengineExternalAccessRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineExternalAccessRuleDestinationIpRanges", typing.Dict[builtins.str, typing.Any]]]],
        destination_ports: typing.Sequence[builtins.str],
        ip_protocol: builtins.str,
        name: builtins.str,
        parent: builtins.str,
        priority: jsii.Number,
        source_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineExternalAccessRuleSourceIpRanges", typing.Dict[builtins.str, typing.Any]]]],
        source_ports: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VmwareengineExternalAccessRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: The action that the external access rule performs. Possible values: ["ALLOW", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#action VmwareengineExternalAccessRule#action}
        :param destination_ip_ranges: destination_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#destination_ip_ranges VmwareengineExternalAccessRule#destination_ip_ranges}
        :param destination_ports: A list of destination ports to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#destination_ports VmwareengineExternalAccessRule#destination_ports}
        :param ip_protocol: The IP protocol to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#ip_protocol VmwareengineExternalAccessRule#ip_protocol}
        :param name: The ID of the external access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#name VmwareengineExternalAccessRule#name}
        :param parent: The resource name of the network policy. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/networkPolicies/my-policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#parent VmwareengineExternalAccessRule#parent}
        :param priority: External access rule priority, which determines the external access rule to use when multiple rules apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#priority VmwareengineExternalAccessRule#priority}
        :param source_ip_ranges: source_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#source_ip_ranges VmwareengineExternalAccessRule#source_ip_ranges}
        :param source_ports: A list of source ports to which the external access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#source_ports VmwareengineExternalAccessRule#source_ports}
        :param description: User-provided description for the external access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#description VmwareengineExternalAccessRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#id VmwareengineExternalAccessRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#timeouts VmwareengineExternalAccessRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = VmwareengineExternalAccessRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81965015da74ecdb8a43e2373d343c9b454237827151a9c2f24d40fbe859b0e7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#action VmwareengineExternalAccessRule#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_ip_ranges(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineExternalAccessRuleDestinationIpRanges"]]:
        '''destination_ip_ranges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#destination_ip_ranges VmwareengineExternalAccessRule#destination_ip_ranges}
        '''
        result = self._values.get("destination_ip_ranges")
        assert result is not None, "Required property 'destination_ip_ranges' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineExternalAccessRuleDestinationIpRanges"]], result)

    @builtins.property
    def destination_ports(self) -> typing.List[builtins.str]:
        '''A list of destination ports to which the external access rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#destination_ports VmwareengineExternalAccessRule#destination_ports}
        '''
        result = self._values.get("destination_ports")
        assert result is not None, "Required property 'destination_ports' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The IP protocol to which the external access rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#ip_protocol VmwareengineExternalAccessRule#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The ID of the external access rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#name VmwareengineExternalAccessRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The resource name of the network policy. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/networkPolicies/my-policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#parent VmwareengineExternalAccessRule#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''External access rule priority, which determines the external access rule to use when multiple rules apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#priority VmwareengineExternalAccessRule#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def source_ip_ranges(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineExternalAccessRuleSourceIpRanges"]]:
        '''source_ip_ranges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#source_ip_ranges VmwareengineExternalAccessRule#source_ip_ranges}
        '''
        result = self._values.get("source_ip_ranges")
        assert result is not None, "Required property 'source_ip_ranges' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineExternalAccessRuleSourceIpRanges"]], result)

    @builtins.property
    def source_ports(self) -> typing.List[builtins.str]:
        '''A list of source ports to which the external access rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#source_ports VmwareengineExternalAccessRule#source_ports}
        '''
        result = self._values.get("source_ports")
        assert result is not None, "Required property 'source_ports' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description for the external access rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#description VmwareengineExternalAccessRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#id VmwareengineExternalAccessRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VmwareengineExternalAccessRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#timeouts VmwareengineExternalAccessRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VmwareengineExternalAccessRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineExternalAccessRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRuleDestinationIpRanges",
    jsii_struct_bases=[],
    name_mapping={
        "external_address": "externalAddress",
        "ip_address_range": "ipAddressRange",
    },
)
class VmwareengineExternalAccessRuleDestinationIpRanges:
    def __init__(
        self,
        *,
        external_address: typing.Optional[builtins.str] = None,
        ip_address_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_address: The name of an 'ExternalAddress' resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#external_address VmwareengineExternalAccessRule#external_address}
        :param ip_address_range: An IP address range in the CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#ip_address_range VmwareengineExternalAccessRule#ip_address_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10732d55b02b2fdf46bcc413be78fabb6874f1c86eaf220d946471fdbfb126ee)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#external_address VmwareengineExternalAccessRule#external_address}
        '''
        result = self._values.get("external_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_range(self) -> typing.Optional[builtins.str]:
        '''An IP address range in the CIDR format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#ip_address_range VmwareengineExternalAccessRule#ip_address_range}
        '''
        result = self._values.get("ip_address_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineExternalAccessRuleDestinationIpRanges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareengineExternalAccessRuleDestinationIpRangesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRuleDestinationIpRangesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a59b4b572126821528f85bfbb3b9f4215d725d559ec6fbba26f7a8a4fcb10b96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VmwareengineExternalAccessRuleDestinationIpRangesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85b5470259a055070e67bdbe2ede9ae10578ce1f7a67cdcb41a57a23d8f7310)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmwareengineExternalAccessRuleDestinationIpRangesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3cd10a844cb43167dc778b3b91c7d4cb9c5f35c49ee4442a10de1fa7aeb39c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36fba0f9ab1719836df170d3d1236e65ccb54a87c78591fb2e372ff9cd6044e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69b4030ffbab380eb11ab420500935af8e0b6bb811f2d4c6b796028c4a819353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineExternalAccessRuleDestinationIpRanges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineExternalAccessRuleDestinationIpRanges]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineExternalAccessRuleDestinationIpRanges]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62038af46930c47d49110c87dbec6b321193b08625f9c0470be3f8a30588971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareengineExternalAccessRuleDestinationIpRangesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRuleDestinationIpRangesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ba77ac6e35cddda5f6ca06972dbaf2e28013011b3a8dad773035094d27af781)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b772e1e486e0ed165894287bf5292d7e0ec41d14422f2bbfa7ce971759eae383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressRange")
    def ip_address_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressRange"))

    @ip_address_range.setter
    def ip_address_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fccec345538febe75fcd0faffa1231f83816d21ea545e5a9d7e4feca4e06ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleDestinationIpRanges]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleDestinationIpRanges]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleDestinationIpRanges]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25212dd65a538ce9f0b7532a66877f7e64e5c89c2db0df6984fde4d8a73c98cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRuleSourceIpRanges",
    jsii_struct_bases=[],
    name_mapping={"ip_address": "ipAddress", "ip_address_range": "ipAddressRange"},
)
class VmwareengineExternalAccessRuleSourceIpRanges:
    def __init__(
        self,
        *,
        ip_address: typing.Optional[builtins.str] = None,
        ip_address_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: A single IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#ip_address VmwareengineExternalAccessRule#ip_address}
        :param ip_address_range: An IP address range in the CIDR format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#ip_address_range VmwareengineExternalAccessRule#ip_address_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1083f99cd95e41b1801683bb945aa37bb3f09799c7c768d084a52db61926351)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#ip_address VmwareengineExternalAccessRule#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_range(self) -> typing.Optional[builtins.str]:
        '''An IP address range in the CIDR format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#ip_address_range VmwareengineExternalAccessRule#ip_address_range}
        '''
        result = self._values.get("ip_address_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineExternalAccessRuleSourceIpRanges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareengineExternalAccessRuleSourceIpRangesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRuleSourceIpRangesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2858c7810559be26fa9fde39c69a487bee30f676c79313a63d6872fd8cc1ddf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VmwareengineExternalAccessRuleSourceIpRangesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1a805938a7bd7030c85ca79acb2bf00a2234367e37e05d7ef226cc6556ba68)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmwareengineExternalAccessRuleSourceIpRangesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea0833371b104e0ca02e2dd5038e8e2e5883abd45825110489b5d3cff50269c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1f82f3d91c36511b94a371e7dc68482a98d754291d87f06db73ee4f456ed82e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ad8788e4197002d3a99b67a5d7a39f584e4d310c0c67cccda3affa489b3a6cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineExternalAccessRuleSourceIpRanges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineExternalAccessRuleSourceIpRanges]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineExternalAccessRuleSourceIpRanges]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100a3219c52db68f4ae6df0230e0c795493e2104828562314ad6535819377b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareengineExternalAccessRuleSourceIpRangesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRuleSourceIpRangesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7590a137759399606bfb797c9afaccae586ce826df591da90a634a12d07e9a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8658cf91d545a67b70828b13afa439a008d8b741cec91cbddf896db18a8818c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressRange")
    def ip_address_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressRange"))

    @ip_address_range.setter
    def ip_address_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608460dacd5a045b3872fed7324c81a7abad7ded5b3f73231c512b854c129127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleSourceIpRanges]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleSourceIpRanges]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleSourceIpRanges]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bba840c272ba63f7b561b6587cc902515bbe73053e1f3782c9245ade39d25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VmwareengineExternalAccessRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#create VmwareengineExternalAccessRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#delete VmwareengineExternalAccessRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#update VmwareengineExternalAccessRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56502cbf643fbb2062ec7f4131389b487a91dfc215148ba0ebb901af9fc99582)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#create VmwareengineExternalAccessRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#delete VmwareengineExternalAccessRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_external_access_rule#update VmwareengineExternalAccessRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineExternalAccessRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareengineExternalAccessRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineExternalAccessRule.VmwareengineExternalAccessRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__085d7aba334cf21881f598171d5799d9cf8450f0eec673697a0bf54124a2cc0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c44d60c6bacc687b5975a99918537f4d44f2d3b0a71c642f61e4acd874e75fac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32248154fee2042a2d715da47400a6f903e7c3c9657b421b280d9555f3e6e3e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd1d7991d5acc27e4077c6b21f75a7457e8a9d36ea3f012c68894860b6bef7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a95062d418113ee3a6b3f4f4e65e70ce0c63532c81bd0e2a741b0ea4e234ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VmwareengineExternalAccessRule",
    "VmwareengineExternalAccessRuleConfig",
    "VmwareengineExternalAccessRuleDestinationIpRanges",
    "VmwareengineExternalAccessRuleDestinationIpRangesList",
    "VmwareengineExternalAccessRuleDestinationIpRangesOutputReference",
    "VmwareengineExternalAccessRuleSourceIpRanges",
    "VmwareengineExternalAccessRuleSourceIpRangesList",
    "VmwareengineExternalAccessRuleSourceIpRangesOutputReference",
    "VmwareengineExternalAccessRuleTimeouts",
    "VmwareengineExternalAccessRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0f8642c7d85fef153218859ca4ac409131dd40a936559d8e1d547828a8d6c1f8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    destination_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineExternalAccessRuleDestinationIpRanges, typing.Dict[builtins.str, typing.Any]]]],
    destination_ports: typing.Sequence[builtins.str],
    ip_protocol: builtins.str,
    name: builtins.str,
    parent: builtins.str,
    priority: jsii.Number,
    source_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineExternalAccessRuleSourceIpRanges, typing.Dict[builtins.str, typing.Any]]]],
    source_ports: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VmwareengineExternalAccessRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d834136189aa413a3abc072933d219b5f0fd62c0dcd9e98710fe142ab16bd19e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3d2d71437123bb1c3b5deaac7356c1b077c818db62dcb765781417d4bca477(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineExternalAccessRuleDestinationIpRanges, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6488bce5e0c59e5929e3de4f8f61450a4c8fa4b44c463bd59d2b0a463da9a9b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineExternalAccessRuleSourceIpRanges, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1deb69a94c25684dbb5e4972ef08b4273d71fba185c9457cca0a65469897dbd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80029a6b8b492c66c99b598274b75da065944288405254bf694366a25dc4de14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455bb5fc64c3093194538e0413d7b7a3a6068ae95b5f12c285d430a886ccd2a8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f16788c670b96427e7db55f454f83b9a4d6fa70c7cd95801a2a70e4907769c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590dc85226ed8c48a9c75763c2f6201546f830f8b5f973b3b9b8cb2e5c7a991d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e691368b6acf5a638919304c9abce04f279c9e8990886d117967d8987c9a2f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7276f585c2fd99f08eaadf76a34f7e7602baf7c9ffc2b9c1227c404c60e1552c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c311645d0e3078041fe239806662f0532b7d863534f0fc3a2a45f67475948f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e91806b923d3acb4029774666eb1ec3c245374614969142b8b57d296c31b62(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81965015da74ecdb8a43e2373d343c9b454237827151a9c2f24d40fbe859b0e7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    destination_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineExternalAccessRuleDestinationIpRanges, typing.Dict[builtins.str, typing.Any]]]],
    destination_ports: typing.Sequence[builtins.str],
    ip_protocol: builtins.str,
    name: builtins.str,
    parent: builtins.str,
    priority: jsii.Number,
    source_ip_ranges: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineExternalAccessRuleSourceIpRanges, typing.Dict[builtins.str, typing.Any]]]],
    source_ports: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VmwareengineExternalAccessRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10732d55b02b2fdf46bcc413be78fabb6874f1c86eaf220d946471fdbfb126ee(
    *,
    external_address: typing.Optional[builtins.str] = None,
    ip_address_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59b4b572126821528f85bfbb3b9f4215d725d559ec6fbba26f7a8a4fcb10b96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85b5470259a055070e67bdbe2ede9ae10578ce1f7a67cdcb41a57a23d8f7310(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3cd10a844cb43167dc778b3b91c7d4cb9c5f35c49ee4442a10de1fa7aeb39c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fba0f9ab1719836df170d3d1236e65ccb54a87c78591fb2e372ff9cd6044e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b4030ffbab380eb11ab420500935af8e0b6bb811f2d4c6b796028c4a819353(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62038af46930c47d49110c87dbec6b321193b08625f9c0470be3f8a30588971(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineExternalAccessRuleDestinationIpRanges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba77ac6e35cddda5f6ca06972dbaf2e28013011b3a8dad773035094d27af781(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b772e1e486e0ed165894287bf5292d7e0ec41d14422f2bbfa7ce971759eae383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fccec345538febe75fcd0faffa1231f83816d21ea545e5a9d7e4feca4e06ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25212dd65a538ce9f0b7532a66877f7e64e5c89c2db0df6984fde4d8a73c98cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleDestinationIpRanges]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1083f99cd95e41b1801683bb945aa37bb3f09799c7c768d084a52db61926351(
    *,
    ip_address: typing.Optional[builtins.str] = None,
    ip_address_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2858c7810559be26fa9fde39c69a487bee30f676c79313a63d6872fd8cc1ddf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1a805938a7bd7030c85ca79acb2bf00a2234367e37e05d7ef226cc6556ba68(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea0833371b104e0ca02e2dd5038e8e2e5883abd45825110489b5d3cff50269c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f82f3d91c36511b94a371e7dc68482a98d754291d87f06db73ee4f456ed82e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad8788e4197002d3a99b67a5d7a39f584e4d310c0c67cccda3affa489b3a6cc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100a3219c52db68f4ae6df0230e0c795493e2104828562314ad6535819377b99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineExternalAccessRuleSourceIpRanges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7590a137759399606bfb797c9afaccae586ce826df591da90a634a12d07e9a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8658cf91d545a67b70828b13afa439a008d8b741cec91cbddf896db18a8818c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608460dacd5a045b3872fed7324c81a7abad7ded5b3f73231c512b854c129127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bba840c272ba63f7b561b6587cc902515bbe73053e1f3782c9245ade39d25c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleSourceIpRanges]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56502cbf643fbb2062ec7f4131389b487a91dfc215148ba0ebb901af9fc99582(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085d7aba334cf21881f598171d5799d9cf8450f0eec673697a0bf54124a2cc0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44d60c6bacc687b5975a99918537f4d44f2d3b0a71c642f61e4acd874e75fac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32248154fee2042a2d715da47400a6f903e7c3c9657b421b280d9555f3e6e3e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd1d7991d5acc27e4077c6b21f75a7457e8a9d36ea3f012c68894860b6bef7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a95062d418113ee3a6b3f4f4e65e70ce0c63532c81bd0e2a741b0ea4e234ef8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineExternalAccessRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
