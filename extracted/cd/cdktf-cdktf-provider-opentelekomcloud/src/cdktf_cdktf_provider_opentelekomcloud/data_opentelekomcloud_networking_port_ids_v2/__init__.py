r'''
# `data_opentelekomcloud_networking_port_ids_v2`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_networking_port_ids_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2).
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


class DataOpentelekomcloudNetworkingPortIdsV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNetworkingPortIdsV2.DataOpentelekomcloudNetworkingPortIdsV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2 opentelekomcloud_networking_port_ids_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        device_id: typing.Optional[builtins.str] = None,
        device_owner: typing.Optional[builtins.str] = None,
        fixed_ip: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mac_address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        sort_direction: typing.Optional[builtins.str] = None,
        sort_key: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2 opentelekomcloud_networking_port_ids_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#device_id DataOpentelekomcloudNetworkingPortIdsV2#device_id}.
        :param device_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#device_owner DataOpentelekomcloudNetworkingPortIdsV2#device_owner}.
        :param fixed_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#fixed_ip DataOpentelekomcloudNetworkingPortIdsV2#fixed_ip}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#id DataOpentelekomcloudNetworkingPortIdsV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mac_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#mac_address DataOpentelekomcloudNetworkingPortIdsV2#mac_address}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#name DataOpentelekomcloudNetworkingPortIdsV2#name}.
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#network_id DataOpentelekomcloudNetworkingPortIdsV2#network_id}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#project_id DataOpentelekomcloudNetworkingPortIdsV2#project_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#region DataOpentelekomcloudNetworkingPortIdsV2#region}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#security_group_ids DataOpentelekomcloudNetworkingPortIdsV2#security_group_ids}.
        :param sort_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#sort_direction DataOpentelekomcloudNetworkingPortIdsV2#sort_direction}.
        :param sort_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#sort_key DataOpentelekomcloudNetworkingPortIdsV2#sort_key}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#status DataOpentelekomcloudNetworkingPortIdsV2#status}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#tenant_id DataOpentelekomcloudNetworkingPortIdsV2#tenant_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d345f5f7c284022b5f7abf25de00b26468f77fc9dfc1318291a3cc1a0579618c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudNetworkingPortIdsV2Config(
            device_id=device_id,
            device_owner=device_owner,
            fixed_ip=fixed_ip,
            id=id,
            mac_address=mac_address,
            name=name,
            network_id=network_id,
            project_id=project_id,
            region=region,
            security_group_ids=security_group_ids,
            sort_direction=sort_direction,
            sort_key=sort_key,
            status=status,
            tenant_id=tenant_id,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudNetworkingPortIdsV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudNetworkingPortIdsV2 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudNetworkingPortIdsV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudNetworkingPortIdsV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea66d74d3815ef1f7eecfbd56d86c35a98ed77f6a9e3971dee14ebde39d0624)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDeviceId")
    def reset_device_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceId", []))

    @jsii.member(jsii_name="resetDeviceOwner")
    def reset_device_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceOwner", []))

    @jsii.member(jsii_name="resetFixedIp")
    def reset_fixed_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIp", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMacAddress")
    def reset_mac_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacAddress", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNetworkId")
    def reset_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSortDirection")
    def reset_sort_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSortDirection", []))

    @jsii.member(jsii_name="resetSortKey")
    def reset_sort_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSortKey", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

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
    @jsii.member(jsii_name="ids")
    def ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ids"))

    @builtins.property
    @jsii.member(jsii_name="deviceIdInput")
    def device_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceOwnerInput")
    def device_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedIpInput")
    def fixed_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedIpInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="macAddressInput")
    def mac_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="sortDirectionInput")
    def sort_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="sortKeyInput")
    def sort_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceId"))

    @device_id.setter
    def device_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd18a504a719a1685546bc2e3185ba4bfdb6eb3c0bc175d1331f6b20126d2f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceOwner")
    def device_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceOwner"))

    @device_owner.setter
    def device_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88dfae120c5f49858f52958cecef6ad43b61c0b1bea059421c51f98ba0f7afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedIp")
    def fixed_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedIp"))

    @fixed_ip.setter
    def fixed_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e77ff97646607105fdb2579be34a1b1e48ae225d402ea236bcd2647f2f2db17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bcf8fe54fa9aaf879a11dc615566cb31d708f96bfe92dd0cb29a3dc39c81be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macAddress")
    def mac_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macAddress"))

    @mac_address.setter
    def mac_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5c63e854cc0f397b39da17ab57ec9d21b893fc37382ea0f8158da62ee9a1fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496b984c48ff5d03d5bd74c0b60c764369921c24fa8e3187039397274a2b3724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897652d23801758e0954206223d1ae42fa4a1a7e2c37cb8443da64dda3b0c60b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff46a7ebb36988e07313fcef311bd5d968019f775f5ef41bebd9a0483f58fcd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff4c0f2bfeffa23ea99e00879735820debd28ed5db20b6bdf07f85061eb8489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d6b8459248186b458d2f4dbcd575b3f9b83897b7fd8567b093cca25c270ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sortDirection")
    def sort_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sortDirection"))

    @sort_direction.setter
    def sort_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a31e8d0994d3a6ba15a1ec089b94de6c2fc0f16b8bd0c7cd38d14167c95c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortDirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sortKey")
    def sort_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sortKey"))

    @sort_key.setter
    def sort_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe660141faf88a55f15c12c017ee6f3fda17461b88088377aba8c3efdc9b082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc90323090653d14174cb3e81374df77c9fe24bcc7af38eb46032fb83e72948c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f7efd19e5feef01fd55f35c9a7b64c513ccc1c8a0d0b185a288fb5161087fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNetworkingPortIdsV2.DataOpentelekomcloudNetworkingPortIdsV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "device_id": "deviceId",
        "device_owner": "deviceOwner",
        "fixed_ip": "fixedIp",
        "id": "id",
        "mac_address": "macAddress",
        "name": "name",
        "network_id": "networkId",
        "project_id": "projectId",
        "region": "region",
        "security_group_ids": "securityGroupIds",
        "sort_direction": "sortDirection",
        "sort_key": "sortKey",
        "status": "status",
        "tenant_id": "tenantId",
    },
)
class DataOpentelekomcloudNetworkingPortIdsV2Config(
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
        device_id: typing.Optional[builtins.str] = None,
        device_owner: typing.Optional[builtins.str] = None,
        fixed_ip: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mac_address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        sort_direction: typing.Optional[builtins.str] = None,
        sort_key: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#device_id DataOpentelekomcloudNetworkingPortIdsV2#device_id}.
        :param device_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#device_owner DataOpentelekomcloudNetworkingPortIdsV2#device_owner}.
        :param fixed_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#fixed_ip DataOpentelekomcloudNetworkingPortIdsV2#fixed_ip}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#id DataOpentelekomcloudNetworkingPortIdsV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mac_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#mac_address DataOpentelekomcloudNetworkingPortIdsV2#mac_address}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#name DataOpentelekomcloudNetworkingPortIdsV2#name}.
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#network_id DataOpentelekomcloudNetworkingPortIdsV2#network_id}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#project_id DataOpentelekomcloudNetworkingPortIdsV2#project_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#region DataOpentelekomcloudNetworkingPortIdsV2#region}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#security_group_ids DataOpentelekomcloudNetworkingPortIdsV2#security_group_ids}.
        :param sort_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#sort_direction DataOpentelekomcloudNetworkingPortIdsV2#sort_direction}.
        :param sort_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#sort_key DataOpentelekomcloudNetworkingPortIdsV2#sort_key}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#status DataOpentelekomcloudNetworkingPortIdsV2#status}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#tenant_id DataOpentelekomcloudNetworkingPortIdsV2#tenant_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc44aa2240eee9c42def52222cc84f5497cc837274701f97079555a330c64e8d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
            check_type(argname="argument device_owner", value=device_owner, expected_type=type_hints["device_owner"])
            check_type(argname="argument fixed_ip", value=fixed_ip, expected_type=type_hints["fixed_ip"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mac_address", value=mac_address, expected_type=type_hints["mac_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument sort_direction", value=sort_direction, expected_type=type_hints["sort_direction"])
            check_type(argname="argument sort_key", value=sort_key, expected_type=type_hints["sort_key"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if device_id is not None:
            self._values["device_id"] = device_id
        if device_owner is not None:
            self._values["device_owner"] = device_owner
        if fixed_ip is not None:
            self._values["fixed_ip"] = fixed_ip
        if id is not None:
            self._values["id"] = id
        if mac_address is not None:
            self._values["mac_address"] = mac_address
        if name is not None:
            self._values["name"] = name
        if network_id is not None:
            self._values["network_id"] = network_id
        if project_id is not None:
            self._values["project_id"] = project_id
        if region is not None:
            self._values["region"] = region
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if sort_direction is not None:
            self._values["sort_direction"] = sort_direction
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if status is not None:
            self._values["status"] = status
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id

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
    def device_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#device_id DataOpentelekomcloudNetworkingPortIdsV2#device_id}.'''
        result = self._values.get("device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#device_owner DataOpentelekomcloudNetworkingPortIdsV2#device_owner}.'''
        result = self._values.get("device_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#fixed_ip DataOpentelekomcloudNetworkingPortIdsV2#fixed_ip}.'''
        result = self._values.get("fixed_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#id DataOpentelekomcloudNetworkingPortIdsV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mac_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#mac_address DataOpentelekomcloudNetworkingPortIdsV2#mac_address}.'''
        result = self._values.get("mac_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#name DataOpentelekomcloudNetworkingPortIdsV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#network_id DataOpentelekomcloudNetworkingPortIdsV2#network_id}.'''
        result = self._values.get("network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#project_id DataOpentelekomcloudNetworkingPortIdsV2#project_id}.'''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#region DataOpentelekomcloudNetworkingPortIdsV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#security_group_ids DataOpentelekomcloudNetworkingPortIdsV2#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sort_direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#sort_direction DataOpentelekomcloudNetworkingPortIdsV2#sort_direction}.'''
        result = self._values.get("sort_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#sort_key DataOpentelekomcloudNetworkingPortIdsV2#sort_key}.'''
        result = self._values.get("sort_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#status DataOpentelekomcloudNetworkingPortIdsV2#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/networking_port_ids_v2#tenant_id DataOpentelekomcloudNetworkingPortIdsV2#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudNetworkingPortIdsV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpentelekomcloudNetworkingPortIdsV2",
    "DataOpentelekomcloudNetworkingPortIdsV2Config",
]

publication.publish()

def _typecheckingstub__d345f5f7c284022b5f7abf25de00b26468f77fc9dfc1318291a3cc1a0579618c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    device_id: typing.Optional[builtins.str] = None,
    device_owner: typing.Optional[builtins.str] = None,
    fixed_ip: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mac_address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    sort_direction: typing.Optional[builtins.str] = None,
    sort_key: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__aea66d74d3815ef1f7eecfbd56d86c35a98ed77f6a9e3971dee14ebde39d0624(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd18a504a719a1685546bc2e3185ba4bfdb6eb3c0bc175d1331f6b20126d2f77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88dfae120c5f49858f52958cecef6ad43b61c0b1bea059421c51f98ba0f7afe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e77ff97646607105fdb2579be34a1b1e48ae225d402ea236bcd2647f2f2db17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bcf8fe54fa9aaf879a11dc615566cb31d708f96bfe92dd0cb29a3dc39c81be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5c63e854cc0f397b39da17ab57ec9d21b893fc37382ea0f8158da62ee9a1fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496b984c48ff5d03d5bd74c0b60c764369921c24fa8e3187039397274a2b3724(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897652d23801758e0954206223d1ae42fa4a1a7e2c37cb8443da64dda3b0c60b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff46a7ebb36988e07313fcef311bd5d968019f775f5ef41bebd9a0483f58fcd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff4c0f2bfeffa23ea99e00879735820debd28ed5db20b6bdf07f85061eb8489(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d6b8459248186b458d2f4dbcd575b3f9b83897b7fd8567b093cca25c270ef0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a31e8d0994d3a6ba15a1ec089b94de6c2fc0f16b8bd0c7cd38d14167c95c1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe660141faf88a55f15c12c017ee6f3fda17461b88088377aba8c3efdc9b082(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc90323090653d14174cb3e81374df77c9fe24bcc7af38eb46032fb83e72948c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f7efd19e5feef01fd55f35c9a7b64c513ccc1c8a0d0b185a288fb5161087fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc44aa2240eee9c42def52222cc84f5497cc837274701f97079555a330c64e8d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    device_id: typing.Optional[builtins.str] = None,
    device_owner: typing.Optional[builtins.str] = None,
    fixed_ip: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mac_address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    sort_direction: typing.Optional[builtins.str] = None,
    sort_key: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
