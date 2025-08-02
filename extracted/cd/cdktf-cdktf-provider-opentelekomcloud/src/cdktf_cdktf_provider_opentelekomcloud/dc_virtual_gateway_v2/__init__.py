r'''
# `opentelekomcloud_dc_virtual_gateway_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dc_virtual_gateway_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2).
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


class DcVirtualGatewayV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualGatewayV2.DcVirtualGatewayV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2 opentelekomcloud_dc_virtual_gateway_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        vpc_id: builtins.str,
        asn: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        device_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_ep_group: typing.Optional[typing.Union["DcVirtualGatewayV2LocalEpGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        local_ep_group_v6: typing.Optional[typing.Union["DcVirtualGatewayV2LocalEpGroupV6", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        redundant_device_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2 opentelekomcloud_dc_virtual_gateway_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#name DcVirtualGatewayV2#name}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#vpc_id DcVirtualGatewayV2#vpc_id}.
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#asn DcVirtualGatewayV2#asn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#description DcVirtualGatewayV2#description}.
        :param device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#device_id DcVirtualGatewayV2#device_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#id DcVirtualGatewayV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_ep_group: local_ep_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#local_ep_group DcVirtualGatewayV2#local_ep_group}
        :param local_ep_group_v6: local_ep_group_v6 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#local_ep_group_v6 DcVirtualGatewayV2#local_ep_group_v6}
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#project_id DcVirtualGatewayV2#project_id}.
        :param redundant_device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#redundant_device_id DcVirtualGatewayV2#redundant_device_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546614f87358f0decae45c6664ef94c2ac46691e970382aaa7aa592351a4ab5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DcVirtualGatewayV2Config(
            name=name,
            vpc_id=vpc_id,
            asn=asn,
            description=description,
            device_id=device_id,
            id=id,
            local_ep_group=local_ep_group,
            local_ep_group_v6=local_ep_group_v6,
            project_id=project_id,
            redundant_device_id=redundant_device_id,
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
        '''Generates CDKTF code for importing a DcVirtualGatewayV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DcVirtualGatewayV2 to import.
        :param import_from_id: The id of the existing DcVirtualGatewayV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DcVirtualGatewayV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088e40ae2a44aa146797846d735235ccde3640bb17dd180ae970ef1b0539ada5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLocalEpGroup")
    def put_local_ep_group(
        self,
        *,
        endpoints: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#endpoints DcVirtualGatewayV2#endpoints}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#description DcVirtualGatewayV2#description}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#name DcVirtualGatewayV2#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#type DcVirtualGatewayV2#type}.
        '''
        value = DcVirtualGatewayV2LocalEpGroup(
            endpoints=endpoints, description=description, name=name, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putLocalEpGroup", [value]))

    @jsii.member(jsii_name="putLocalEpGroupV6")
    def put_local_ep_group_v6(
        self,
        *,
        endpoints: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#endpoints DcVirtualGatewayV2#endpoints}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#description DcVirtualGatewayV2#description}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#name DcVirtualGatewayV2#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#type DcVirtualGatewayV2#type}.
        '''
        value = DcVirtualGatewayV2LocalEpGroupV6(
            endpoints=endpoints, description=description, name=name, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putLocalEpGroupV6", [value]))

    @jsii.member(jsii_name="resetAsn")
    def reset_asn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsn", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDeviceId")
    def reset_device_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocalEpGroup")
    def reset_local_ep_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalEpGroup", []))

    @jsii.member(jsii_name="resetLocalEpGroupV6")
    def reset_local_ep_group_v6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalEpGroupV6", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetRedundantDeviceId")
    def reset_redundant_device_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedundantDeviceId", []))

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
    @jsii.member(jsii_name="localEpGroup")
    def local_ep_group(self) -> "DcVirtualGatewayV2LocalEpGroupOutputReference":
        return typing.cast("DcVirtualGatewayV2LocalEpGroupOutputReference", jsii.get(self, "localEpGroup"))

    @builtins.property
    @jsii.member(jsii_name="localEpGroupId")
    def local_ep_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localEpGroupId"))

    @builtins.property
    @jsii.member(jsii_name="localEpGroupIpv6Id")
    def local_ep_group_ipv6_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localEpGroupIpv6Id"))

    @builtins.property
    @jsii.member(jsii_name="localEpGroupV6")
    def local_ep_group_v6(self) -> "DcVirtualGatewayV2LocalEpGroupV6OutputReference":
        return typing.cast("DcVirtualGatewayV2LocalEpGroupV6OutputReference", jsii.get(self, "localEpGroupV6"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceIdInput")
    def device_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localEpGroupInput")
    def local_ep_group_input(self) -> typing.Optional["DcVirtualGatewayV2LocalEpGroup"]:
        return typing.cast(typing.Optional["DcVirtualGatewayV2LocalEpGroup"], jsii.get(self, "localEpGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="localEpGroupV6Input")
    def local_ep_group_v6_input(
        self,
    ) -> typing.Optional["DcVirtualGatewayV2LocalEpGroupV6"]:
        return typing.cast(typing.Optional["DcVirtualGatewayV2LocalEpGroupV6"], jsii.get(self, "localEpGroupV6Input"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="redundantDeviceIdInput")
    def redundant_device_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redundantDeviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81acea4088268dba4286865bc365edbbe407775a5d5b84fce9a5d4ea015c6f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b42b169acce388649a785d49955e1a6a6c50735e7f539648ced85ab2b435eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceId"))

    @device_id.setter
    def device_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6a2d93e0ee8369564c03882576d2461c5aa2515a54ce0476a998037fcf7958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb8ebac5e16c1b4fa56f35445115ea0e87c4f4dba014e40436c9ea82de4a965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d18b93773afb34ab9fee77081d9e013cc0544bb3fd75b0c2f692a0e608bc353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f19216d60a6a0472054022941c9ec7c1bde6e8bbbfee589519f98e832314e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redundantDeviceId")
    def redundant_device_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redundantDeviceId"))

    @redundant_device_id.setter
    def redundant_device_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12632954751c526e5f3a4edafc15a438aee8425988862f54b3ec1b8a9e9cc2ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redundantDeviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439fbded0ddd6156e3a7b9592fc784019f1f56687763287ad3a64853682e9640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualGatewayV2.DcVirtualGatewayV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "vpc_id": "vpcId",
        "asn": "asn",
        "description": "description",
        "device_id": "deviceId",
        "id": "id",
        "local_ep_group": "localEpGroup",
        "local_ep_group_v6": "localEpGroupV6",
        "project_id": "projectId",
        "redundant_device_id": "redundantDeviceId",
    },
)
class DcVirtualGatewayV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        vpc_id: builtins.str,
        asn: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        device_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_ep_group: typing.Optional[typing.Union["DcVirtualGatewayV2LocalEpGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        local_ep_group_v6: typing.Optional[typing.Union["DcVirtualGatewayV2LocalEpGroupV6", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
        redundant_device_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#name DcVirtualGatewayV2#name}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#vpc_id DcVirtualGatewayV2#vpc_id}.
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#asn DcVirtualGatewayV2#asn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#description DcVirtualGatewayV2#description}.
        :param device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#device_id DcVirtualGatewayV2#device_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#id DcVirtualGatewayV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_ep_group: local_ep_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#local_ep_group DcVirtualGatewayV2#local_ep_group}
        :param local_ep_group_v6: local_ep_group_v6 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#local_ep_group_v6 DcVirtualGatewayV2#local_ep_group_v6}
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#project_id DcVirtualGatewayV2#project_id}.
        :param redundant_device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#redundant_device_id DcVirtualGatewayV2#redundant_device_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(local_ep_group, dict):
            local_ep_group = DcVirtualGatewayV2LocalEpGroup(**local_ep_group)
        if isinstance(local_ep_group_v6, dict):
            local_ep_group_v6 = DcVirtualGatewayV2LocalEpGroupV6(**local_ep_group_v6)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c10aa13fd78ead50e0c19d2bba69341275ab1e82365d317cc3abac2d99071c4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument local_ep_group", value=local_ep_group, expected_type=type_hints["local_ep_group"])
            check_type(argname="argument local_ep_group_v6", value=local_ep_group_v6, expected_type=type_hints["local_ep_group_v6"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument redundant_device_id", value=redundant_device_id, expected_type=type_hints["redundant_device_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vpc_id": vpc_id,
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
        if asn is not None:
            self._values["asn"] = asn
        if description is not None:
            self._values["description"] = description
        if device_id is not None:
            self._values["device_id"] = device_id
        if id is not None:
            self._values["id"] = id
        if local_ep_group is not None:
            self._values["local_ep_group"] = local_ep_group
        if local_ep_group_v6 is not None:
            self._values["local_ep_group_v6"] = local_ep_group_v6
        if project_id is not None:
            self._values["project_id"] = project_id
        if redundant_device_id is not None:
            self._values["redundant_device_id"] = redundant_device_id

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#name DcVirtualGatewayV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#vpc_id DcVirtualGatewayV2#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#asn DcVirtualGatewayV2#asn}.'''
        result = self._values.get("asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#description DcVirtualGatewayV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#device_id DcVirtualGatewayV2#device_id}.'''
        result = self._values.get("device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#id DcVirtualGatewayV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ep_group(self) -> typing.Optional["DcVirtualGatewayV2LocalEpGroup"]:
        '''local_ep_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#local_ep_group DcVirtualGatewayV2#local_ep_group}
        '''
        result = self._values.get("local_ep_group")
        return typing.cast(typing.Optional["DcVirtualGatewayV2LocalEpGroup"], result)

    @builtins.property
    def local_ep_group_v6(self) -> typing.Optional["DcVirtualGatewayV2LocalEpGroupV6"]:
        '''local_ep_group_v6 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#local_ep_group_v6 DcVirtualGatewayV2#local_ep_group_v6}
        '''
        result = self._values.get("local_ep_group_v6")
        return typing.cast(typing.Optional["DcVirtualGatewayV2LocalEpGroupV6"], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#project_id DcVirtualGatewayV2#project_id}.'''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redundant_device_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#redundant_device_id DcVirtualGatewayV2#redundant_device_id}.'''
        result = self._values.get("redundant_device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcVirtualGatewayV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualGatewayV2.DcVirtualGatewayV2LocalEpGroup",
    jsii_struct_bases=[],
    name_mapping={
        "endpoints": "endpoints",
        "description": "description",
        "name": "name",
        "type": "type",
    },
)
class DcVirtualGatewayV2LocalEpGroup:
    def __init__(
        self,
        *,
        endpoints: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#endpoints DcVirtualGatewayV2#endpoints}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#description DcVirtualGatewayV2#description}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#name DcVirtualGatewayV2#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#type DcVirtualGatewayV2#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d80ee78e6719ecd8a00ffa55fbbd94082ee08fb0ea03a4847161a9429dde9c)
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoints": endpoints,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def endpoints(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#endpoints DcVirtualGatewayV2#endpoints}.'''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#description DcVirtualGatewayV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#name DcVirtualGatewayV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#type DcVirtualGatewayV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcVirtualGatewayV2LocalEpGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcVirtualGatewayV2LocalEpGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualGatewayV2.DcVirtualGatewayV2LocalEpGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c7a228f26fbe548cae96c70fd9700a750dbcfa0e81d9cee89f78474ff78ce15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "endpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b9697cb3849ad112a44feb359e821726d9e7fbaaf83abb01426de7aaf26a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "endpoints"))

    @endpoints.setter
    def endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb4fac0fc149e2a5807022ec22015e0bb58392065fad7d24cd50d5211445baa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72d0cd7d570a9564e064235eb3d5b1947c097c8cd220836f8f763c135e1fa21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052fe2343e657e4f9864d8fc82e389f25bbca36e7f345685fe9b1208718f296b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DcVirtualGatewayV2LocalEpGroup]:
        return typing.cast(typing.Optional[DcVirtualGatewayV2LocalEpGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DcVirtualGatewayV2LocalEpGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9d20b082f6d52720a3fbbd8c242ae47ce8c29f419f3d7ccf6d3896a1343603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualGatewayV2.DcVirtualGatewayV2LocalEpGroupV6",
    jsii_struct_bases=[],
    name_mapping={
        "endpoints": "endpoints",
        "description": "description",
        "name": "name",
        "type": "type",
    },
)
class DcVirtualGatewayV2LocalEpGroupV6:
    def __init__(
        self,
        *,
        endpoints: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#endpoints DcVirtualGatewayV2#endpoints}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#description DcVirtualGatewayV2#description}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#name DcVirtualGatewayV2#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#type DcVirtualGatewayV2#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a36dff2bb2d8929b0b89a1972e34cad4f110556ff4ce5307fbe96e079896ef9)
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoints": endpoints,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def endpoints(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#endpoints DcVirtualGatewayV2#endpoints}.'''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#description DcVirtualGatewayV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#name DcVirtualGatewayV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_gateway_v2#type DcVirtualGatewayV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcVirtualGatewayV2LocalEpGroupV6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcVirtualGatewayV2LocalEpGroupV6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualGatewayV2.DcVirtualGatewayV2LocalEpGroupV6OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c92460574848e7000dbc67e8e336820c2ca65130793290dd1731bd18cf665c54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "endpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ca339366ec618a194d94e158f5e3a3b25173571aa229ce7cf1fd54c21b2e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "endpoints"))

    @endpoints.setter
    def endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723670049a4b875518ac791c21f69e1f2bd309ba29f3afe103708cd643048903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809ccd04e71af4e091c3f549bf783ea9ec96956659b3ca5621729b22c80904b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae044a93f5f324ff38cf5ac8321ca4551d5c6cb3a8aa7c39877fe2642df23db5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DcVirtualGatewayV2LocalEpGroupV6]:
        return typing.cast(typing.Optional[DcVirtualGatewayV2LocalEpGroupV6], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DcVirtualGatewayV2LocalEpGroupV6],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9594d8b42de61dcd38f0a8c2685648014576f701e93ecddf4c3694d9e298c134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DcVirtualGatewayV2",
    "DcVirtualGatewayV2Config",
    "DcVirtualGatewayV2LocalEpGroup",
    "DcVirtualGatewayV2LocalEpGroupOutputReference",
    "DcVirtualGatewayV2LocalEpGroupV6",
    "DcVirtualGatewayV2LocalEpGroupV6OutputReference",
]

publication.publish()

def _typecheckingstub__546614f87358f0decae45c6664ef94c2ac46691e970382aaa7aa592351a4ab5c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    vpc_id: builtins.str,
    asn: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_ep_group: typing.Optional[typing.Union[DcVirtualGatewayV2LocalEpGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    local_ep_group_v6: typing.Optional[typing.Union[DcVirtualGatewayV2LocalEpGroupV6, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    redundant_device_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__088e40ae2a44aa146797846d735235ccde3640bb17dd180ae970ef1b0539ada5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81acea4088268dba4286865bc365edbbe407775a5d5b84fce9a5d4ea015c6f7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b42b169acce388649a785d49955e1a6a6c50735e7f539648ced85ab2b435eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6a2d93e0ee8369564c03882576d2461c5aa2515a54ce0476a998037fcf7958(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb8ebac5e16c1b4fa56f35445115ea0e87c4f4dba014e40436c9ea82de4a965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d18b93773afb34ab9fee77081d9e013cc0544bb3fd75b0c2f692a0e608bc353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f19216d60a6a0472054022941c9ec7c1bde6e8bbbfee589519f98e832314e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12632954751c526e5f3a4edafc15a438aee8425988862f54b3ec1b8a9e9cc2ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439fbded0ddd6156e3a7b9592fc784019f1f56687763287ad3a64853682e9640(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c10aa13fd78ead50e0c19d2bba69341275ab1e82365d317cc3abac2d99071c4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    vpc_id: builtins.str,
    asn: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_ep_group: typing.Optional[typing.Union[DcVirtualGatewayV2LocalEpGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    local_ep_group_v6: typing.Optional[typing.Union[DcVirtualGatewayV2LocalEpGroupV6, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
    redundant_device_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d80ee78e6719ecd8a00ffa55fbbd94082ee08fb0ea03a4847161a9429dde9c(
    *,
    endpoints: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7a228f26fbe548cae96c70fd9700a750dbcfa0e81d9cee89f78474ff78ce15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b9697cb3849ad112a44feb359e821726d9e7fbaaf83abb01426de7aaf26a77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb4fac0fc149e2a5807022ec22015e0bb58392065fad7d24cd50d5211445baa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72d0cd7d570a9564e064235eb3d5b1947c097c8cd220836f8f763c135e1fa21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052fe2343e657e4f9864d8fc82e389f25bbca36e7f345685fe9b1208718f296b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9d20b082f6d52720a3fbbd8c242ae47ce8c29f419f3d7ccf6d3896a1343603(
    value: typing.Optional[DcVirtualGatewayV2LocalEpGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a36dff2bb2d8929b0b89a1972e34cad4f110556ff4ce5307fbe96e079896ef9(
    *,
    endpoints: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92460574848e7000dbc67e8e336820c2ca65130793290dd1731bd18cf665c54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ca339366ec618a194d94e158f5e3a3b25173571aa229ce7cf1fd54c21b2e9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723670049a4b875518ac791c21f69e1f2bd309ba29f3afe103708cd643048903(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809ccd04e71af4e091c3f549bf783ea9ec96956659b3ca5621729b22c80904b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae044a93f5f324ff38cf5ac8321ca4551d5c6cb3a8aa7c39877fe2642df23db5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9594d8b42de61dcd38f0a8c2685648014576f701e93ecddf4c3694d9e298c134(
    value: typing.Optional[DcVirtualGatewayV2LocalEpGroupV6],
) -> None:
    """Type checking stubs"""
    pass
