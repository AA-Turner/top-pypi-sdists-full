r'''
# `opentelekomcloud_compute_bms_server_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_compute_bms_server_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2).
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


class ComputeBmsServerV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2 opentelekomcloud_compute_bms_server_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: builtins.str,
        name: builtins.str,
        admin_pass: typing.Optional[builtins.str] = None,
        block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBmsServerV2BlockDevice", typing.Dict[builtins.str, typing.Any]]]]] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        flavor_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBmsServerV2Network", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeBmsServerV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_data: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2 opentelekomcloud_compute_bms_server_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#availability_zone ComputeBmsServerV2#availability_zone}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#name ComputeBmsServerV2#name}.
        :param admin_pass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#admin_pass ComputeBmsServerV2#admin_pass}.
        :param block_device: block_device block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#block_device ComputeBmsServerV2#block_device}
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#flavor_id ComputeBmsServerV2#flavor_id}.
        :param flavor_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#flavor_name ComputeBmsServerV2#flavor_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#id ComputeBmsServerV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#image_id ComputeBmsServerV2#image_id}.
        :param image_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#image_name ComputeBmsServerV2#image_name}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#key_pair ComputeBmsServerV2#key_pair}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#metadata ComputeBmsServerV2#metadata}.
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#network ComputeBmsServerV2#network}
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#region ComputeBmsServerV2#region}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#security_groups ComputeBmsServerV2#security_groups}.
        :param stop_before_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#stop_before_destroy ComputeBmsServerV2#stop_before_destroy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#tags ComputeBmsServerV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#timeouts ComputeBmsServerV2#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#user_data ComputeBmsServerV2#user_data}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2840a3a07d2bb438f83213a34a8f28a618b191662bc59c6c5b0463d312ff1d47)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeBmsServerV2Config(
            availability_zone=availability_zone,
            name=name,
            admin_pass=admin_pass,
            block_device=block_device,
            flavor_id=flavor_id,
            flavor_name=flavor_name,
            id=id,
            image_id=image_id,
            image_name=image_name,
            key_pair=key_pair,
            metadata=metadata,
            network=network,
            region=region,
            security_groups=security_groups,
            stop_before_destroy=stop_before_destroy,
            tags=tags,
            timeouts=timeouts,
            user_data=user_data,
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
        '''Generates CDKTF code for importing a ComputeBmsServerV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeBmsServerV2 to import.
        :param import_from_id: The id of the existing ComputeBmsServerV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeBmsServerV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfe5e8736f1a372222daaf164c98ee273e5ebb8f49306c06426c72f26fb515b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBlockDevice")
    def put_block_device(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBmsServerV2BlockDevice", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118f061b6edc272b32ff4e243279ef0d51447d72b52a33343ed2d3b8fa75a8c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBlockDevice", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBmsServerV2Network", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdcca0e145619c85059306fade810de0644de21a11843906677e04f14005bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#create ComputeBmsServerV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#delete ComputeBmsServerV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#update ComputeBmsServerV2#update}.
        '''
        value = ComputeBmsServerV2Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminPass")
    def reset_admin_pass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPass", []))

    @jsii.member(jsii_name="resetBlockDevice")
    def reset_block_device(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockDevice", []))

    @jsii.member(jsii_name="resetFlavorId")
    def reset_flavor_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavorId", []))

    @jsii.member(jsii_name="resetFlavorName")
    def reset_flavor_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavorName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageId")
    def reset_image_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageId", []))

    @jsii.member(jsii_name="resetImageName")
    def reset_image_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageName", []))

    @jsii.member(jsii_name="resetKeyPair")
    def reset_key_pair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPair", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetStopBeforeDestroy")
    def reset_stop_before_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopBeforeDestroy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserData")
    def reset_user_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserData", []))

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
    @jsii.member(jsii_name="accessIpV4")
    def access_ip_v4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessIpV4"))

    @builtins.property
    @jsii.member(jsii_name="accessIpV6")
    def access_ip_v6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessIpV6"))

    @builtins.property
    @jsii.member(jsii_name="blockDevice")
    def block_device(self) -> "ComputeBmsServerV2BlockDeviceList":
        return typing.cast("ComputeBmsServerV2BlockDeviceList", jsii.get(self, "blockDevice"))

    @builtins.property
    @jsii.member(jsii_name="configDrive")
    def config_drive(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "configDrive"))

    @builtins.property
    @jsii.member(jsii_name="hostId")
    def host_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostId"))

    @builtins.property
    @jsii.member(jsii_name="hostStatus")
    def host_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostStatus"))

    @builtins.property
    @jsii.member(jsii_name="kernelId")
    def kernel_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kernelId"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "ComputeBmsServerV2NetworkList":
        return typing.cast("ComputeBmsServerV2NetworkList", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeBmsServerV2TimeoutsOutputReference":
        return typing.cast("ComputeBmsServerV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="adminPassInput")
    def admin_pass_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPassInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="blockDeviceInput")
    def block_device_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBmsServerV2BlockDevice"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBmsServerV2BlockDevice"]]], jsii.get(self, "blockDeviceInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorIdInput")
    def flavor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorNameInput")
    def flavor_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageIdInput")
    def image_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPairInput")
    def key_pair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPairInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBmsServerV2Network"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBmsServerV2Network"]]], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="stopBeforeDestroyInput")
    def stop_before_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stopBeforeDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeBmsServerV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeBmsServerV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userDataInput")
    def user_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDataInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPass")
    def admin_pass(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPass"))

    @admin_pass.setter
    def admin_pass(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbfa80cb024a2887c4eda982ea6c1a608315affc9c5d8bb70a533ba8e87fa53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09eee4acd1a35cfb396c6cd77ee246d678d79f34a4879e021ae96284ffe6d86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @flavor_id.setter
    def flavor_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6ad3d070ccaa870625a4b755356dedc00ecc74b2d57a8bff360e1d9d91f259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorName")
    def flavor_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorName"))

    @flavor_name.setter
    def flavor_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6db3f2cbc423c0393916104013d1d2e082303803014608adc4e6076bf06042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e939625c0359947394b43e0fd37eb4d35497bc47fbb22ef7aed4f1203d4b1918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @image_id.setter
    def image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a22a21be3a80cc40f8bdf08ebdf7edc3beab2ca7b7671913d5f56bc907944f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3e27def3f85c8d1b0ac1c294b45eb669750123a332fdcf5dde25c8f7422706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPair")
    def key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPair"))

    @key_pair.setter
    def key_pair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2d61bcb27c9cf36a5a2c9405ed5b2e590ac987287ddf68e22797c3fa5ef56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f19707479fdd5e644dc00305bc7a7f90a84b294081d3664a252eee3fee6e373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a7166542d490a5b7bed528e4e7717b7252c89ba75737e104d812c1768c0887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa89fc97336157a0a4c7ce8cb1d6d777e22b3cecc05db0b27fa0560c7874b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3a442e331230aa47d7c32b16a974396119470e44b36ceed9152600e8a39b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopBeforeDestroy")
    def stop_before_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stopBeforeDestroy"))

    @stop_before_destroy.setter
    def stop_before_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a817be5ec5b80e6c35e50421eac11519f32b7e994a3b2af0b2a63cf1f709a3fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopBeforeDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa7d96eef15c50f7503c9af0019183eb3eac4f241c69eb5986e85e666c48901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userData"))

    @user_data.setter
    def user_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72683f48e6cfd50d9e02ad36a4ae8d1b5a0f95269ef9957cdaa163dc25141d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userData", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2BlockDevice",
    jsii_struct_bases=[],
    name_mapping={
        "source_type": "sourceType",
        "boot_index": "bootIndex",
        "delete_on_termination": "deleteOnTermination",
        "destination_type": "destinationType",
        "device_name": "deviceName",
        "guest_format": "guestFormat",
        "uuid": "uuid",
        "volume_size": "volumeSize",
        "volume_type": "volumeType",
    },
)
class ComputeBmsServerV2BlockDevice:
    def __init__(
        self,
        *,
        source_type: builtins.str,
        boot_index: typing.Optional[jsii.Number] = None,
        delete_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_type: typing.Optional[builtins.str] = None,
        device_name: typing.Optional[builtins.str] = None,
        guest_format: typing.Optional[builtins.str] = None,
        uuid: typing.Optional[builtins.str] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#source_type ComputeBmsServerV2#source_type}.
        :param boot_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#boot_index ComputeBmsServerV2#boot_index}.
        :param delete_on_termination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#delete_on_termination ComputeBmsServerV2#delete_on_termination}.
        :param destination_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#destination_type ComputeBmsServerV2#destination_type}.
        :param device_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#device_name ComputeBmsServerV2#device_name}.
        :param guest_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#guest_format ComputeBmsServerV2#guest_format}.
        :param uuid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#uuid ComputeBmsServerV2#uuid}.
        :param volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#volume_size ComputeBmsServerV2#volume_size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#volume_type ComputeBmsServerV2#volume_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9946b69b0f59b531eef2664d54c26be605a7bc5100b139eb1bbfbd4c532092ab)
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument boot_index", value=boot_index, expected_type=type_hints["boot_index"])
            check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
            check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument guest_format", value=guest_format, expected_type=type_hints["guest_format"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_type": source_type,
        }
        if boot_index is not None:
            self._values["boot_index"] = boot_index
        if delete_on_termination is not None:
            self._values["delete_on_termination"] = delete_on_termination
        if destination_type is not None:
            self._values["destination_type"] = destination_type
        if device_name is not None:
            self._values["device_name"] = device_name
        if guest_format is not None:
            self._values["guest_format"] = guest_format
        if uuid is not None:
            self._values["uuid"] = uuid
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def source_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#source_type ComputeBmsServerV2#source_type}.'''
        result = self._values.get("source_type")
        assert result is not None, "Required property 'source_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boot_index(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#boot_index ComputeBmsServerV2#boot_index}.'''
        result = self._values.get("boot_index")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_on_termination(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#delete_on_termination ComputeBmsServerV2#delete_on_termination}.'''
        result = self._values.get("delete_on_termination")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def destination_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#destination_type ComputeBmsServerV2#destination_type}.'''
        result = self._values.get("destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#device_name ComputeBmsServerV2#device_name}.'''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#guest_format ComputeBmsServerV2#guest_format}.'''
        result = self._values.get("guest_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#uuid ComputeBmsServerV2#uuid}.'''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#volume_size ComputeBmsServerV2#volume_size}.'''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#volume_type ComputeBmsServerV2#volume_type}.'''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBmsServerV2BlockDevice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBmsServerV2BlockDeviceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2BlockDeviceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b66c72a18fd8180e62efdeb02b5d464cf05ac170aa0a1897ad007b22a6e9c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeBmsServerV2BlockDeviceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abc54029a0cf3f09946bc08ad6e3a36dd07f187e52e6cf22e25ab74600ea1d6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBmsServerV2BlockDeviceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c077c88f4201f00dac43f74a2e8241e0108eacf9efc2bb34faeb06a88c8d7c63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d064adf881a6a5bfbdb64c793abe07933df656fed774668a079f930b7136120f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73dafaf9864696a2200bf6f4b8bbe5b31547bd3025d3ccecb67ef09a6710f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2BlockDevice]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2BlockDevice]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2BlockDevice]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5d8ba6f53652620e0185790f7af0de3933bcee4c0206dd3def6594acc79326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBmsServerV2BlockDeviceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2BlockDeviceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04bb474e138a28c2ae421ce5c517178a19f63d0f29800c96ad054a73e5b9ec21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBootIndex")
    def reset_boot_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootIndex", []))

    @jsii.member(jsii_name="resetDeleteOnTermination")
    def reset_delete_on_termination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteOnTermination", []))

    @jsii.member(jsii_name="resetDestinationType")
    def reset_destination_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationType", []))

    @jsii.member(jsii_name="resetDeviceName")
    def reset_device_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceName", []))

    @jsii.member(jsii_name="resetGuestFormat")
    def reset_guest_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestFormat", []))

    @jsii.member(jsii_name="resetUuid")
    def reset_uuid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUuid", []))

    @jsii.member(jsii_name="resetVolumeSize")
    def reset_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSize", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

    @builtins.property
    @jsii.member(jsii_name="bootIndexInput")
    def boot_index_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteOnTerminationInput")
    def delete_on_termination_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteOnTerminationInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationTypeInput")
    def destination_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="guestFormatInput")
    def guest_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "guestFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="uuidInput")
    def uuid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uuidInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInput")
    def volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bootIndex")
    def boot_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootIndex"))

    @boot_index.setter
    def boot_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc325003c11b1a2bcc18c57af322486d2dcb2234888269b4decd8bcc456e9eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteOnTermination")
    def delete_on_termination(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteOnTermination"))

    @delete_on_termination.setter
    def delete_on_termination(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__339819f10b6f9d62406f6d3798f0e520bfc483f3a53c80add4c673ba3fe82c13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteOnTermination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationType")
    def destination_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationType"))

    @destination_type.setter
    def destination_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979424b721207452618f0458e59a9a0bdee6c23ec20b7ff55652a93eb48acfb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a20d8c6671ca5580054b2c3b8d16a5c84402a481ecb03624ca475b8c5d8cb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestFormat")
    def guest_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guestFormat"))

    @guest_format.setter
    def guest_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671c0de81bfbd55a83faaf3a0b988773cac39cf787f7372a4a0dc9020f214ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47774c9347f159ce86dc4ec69248fd822ec74ce8e0790bbcf699a2622e9aac78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @uuid.setter
    def uuid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feed091479c384edff8ad6b165a4eb4243e240cac7daeed9574f37a5ff425a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSize")
    def volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSize"))

    @volume_size.setter
    def volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed7aee39c53d85b9b31f02c05015dd64e851409fa9c305816fc08b6b609f428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabcfdc96b82d6389559757f05944f2e67b8e665e59df7450027baef7c443bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2BlockDevice]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2BlockDevice]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2BlockDevice]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4a3c3103997bcc8cc0f9ab48adce3a372f403fe1f2a297e5f431139dcd6325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zone": "availabilityZone",
        "name": "name",
        "admin_pass": "adminPass",
        "block_device": "blockDevice",
        "flavor_id": "flavorId",
        "flavor_name": "flavorName",
        "id": "id",
        "image_id": "imageId",
        "image_name": "imageName",
        "key_pair": "keyPair",
        "metadata": "metadata",
        "network": "network",
        "region": "region",
        "security_groups": "securityGroups",
        "stop_before_destroy": "stopBeforeDestroy",
        "tags": "tags",
        "timeouts": "timeouts",
        "user_data": "userData",
    },
)
class ComputeBmsServerV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zone: builtins.str,
        name: builtins.str,
        admin_pass: typing.Optional[builtins.str] = None,
        block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBmsServerV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]]] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        flavor_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBmsServerV2Network", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeBmsServerV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#availability_zone ComputeBmsServerV2#availability_zone}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#name ComputeBmsServerV2#name}.
        :param admin_pass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#admin_pass ComputeBmsServerV2#admin_pass}.
        :param block_device: block_device block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#block_device ComputeBmsServerV2#block_device}
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#flavor_id ComputeBmsServerV2#flavor_id}.
        :param flavor_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#flavor_name ComputeBmsServerV2#flavor_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#id ComputeBmsServerV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#image_id ComputeBmsServerV2#image_id}.
        :param image_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#image_name ComputeBmsServerV2#image_name}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#key_pair ComputeBmsServerV2#key_pair}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#metadata ComputeBmsServerV2#metadata}.
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#network ComputeBmsServerV2#network}
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#region ComputeBmsServerV2#region}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#security_groups ComputeBmsServerV2#security_groups}.
        :param stop_before_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#stop_before_destroy ComputeBmsServerV2#stop_before_destroy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#tags ComputeBmsServerV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#timeouts ComputeBmsServerV2#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#user_data ComputeBmsServerV2#user_data}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeBmsServerV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7aee9a7ba6349cc1c2622c3c58449b923fc278ef9cf82eca8536512d94cc1dc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument admin_pass", value=admin_pass, expected_type=type_hints["admin_pass"])
            check_type(argname="argument block_device", value=block_device, expected_type=type_hints["block_device"])
            check_type(argname="argument flavor_id", value=flavor_id, expected_type=type_hints["flavor_id"])
            check_type(argname="argument flavor_name", value=flavor_name, expected_type=type_hints["flavor_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument stop_before_destroy", value=stop_before_destroy, expected_type=type_hints["stop_before_destroy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "name": name,
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
        if admin_pass is not None:
            self._values["admin_pass"] = admin_pass
        if block_device is not None:
            self._values["block_device"] = block_device
        if flavor_id is not None:
            self._values["flavor_id"] = flavor_id
        if flavor_name is not None:
            self._values["flavor_name"] = flavor_name
        if id is not None:
            self._values["id"] = id
        if image_id is not None:
            self._values["image_id"] = image_id
        if image_name is not None:
            self._values["image_name"] = image_name
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if metadata is not None:
            self._values["metadata"] = metadata
        if network is not None:
            self._values["network"] = network
        if region is not None:
            self._values["region"] = region
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if stop_before_destroy is not None:
            self._values["stop_before_destroy"] = stop_before_destroy
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_data is not None:
            self._values["user_data"] = user_data

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
    def availability_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#availability_zone ComputeBmsServerV2#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#name ComputeBmsServerV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_pass(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#admin_pass ComputeBmsServerV2#admin_pass}.'''
        result = self._values.get("admin_pass")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def block_device(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2BlockDevice]]]:
        '''block_device block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#block_device ComputeBmsServerV2#block_device}
        '''
        result = self._values.get("block_device")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2BlockDevice]]], result)

    @builtins.property
    def flavor_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#flavor_id ComputeBmsServerV2#flavor_id}.'''
        result = self._values.get("flavor_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flavor_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#flavor_name ComputeBmsServerV2#flavor_name}.'''
        result = self._values.get("flavor_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#id ComputeBmsServerV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#image_id ComputeBmsServerV2#image_id}.'''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#image_name ComputeBmsServerV2#image_name}.'''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#key_pair ComputeBmsServerV2#key_pair}.'''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#metadata ComputeBmsServerV2#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBmsServerV2Network"]]]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#network ComputeBmsServerV2#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBmsServerV2Network"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#region ComputeBmsServerV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#security_groups ComputeBmsServerV2#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stop_before_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#stop_before_destroy ComputeBmsServerV2#stop_before_destroy}.'''
        result = self._values.get("stop_before_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#tags ComputeBmsServerV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeBmsServerV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#timeouts ComputeBmsServerV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeBmsServerV2Timeouts"], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#user_data ComputeBmsServerV2#user_data}.'''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBmsServerV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2Network",
    jsii_struct_bases=[],
    name_mapping={
        "access_network": "accessNetwork",
        "fixed_ip_v4": "fixedIpV4",
        "fixed_ip_v6": "fixedIpV6",
        "name": "name",
        "port": "port",
        "uuid": "uuid",
    },
)
class ComputeBmsServerV2Network:
    def __init__(
        self,
        *,
        access_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fixed_ip_v4: typing.Optional[builtins.str] = None,
        fixed_ip_v6: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#access_network ComputeBmsServerV2#access_network}.
        :param fixed_ip_v4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#fixed_ip_v4 ComputeBmsServerV2#fixed_ip_v4}.
        :param fixed_ip_v6: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#fixed_ip_v6 ComputeBmsServerV2#fixed_ip_v6}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#name ComputeBmsServerV2#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#port ComputeBmsServerV2#port}.
        :param uuid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#uuid ComputeBmsServerV2#uuid}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ecfb9a03a9e980d6cba7cfe370139e95731aaf18bff0c789c15f50b30bb495)
            check_type(argname="argument access_network", value=access_network, expected_type=type_hints["access_network"])
            check_type(argname="argument fixed_ip_v4", value=fixed_ip_v4, expected_type=type_hints["fixed_ip_v4"])
            check_type(argname="argument fixed_ip_v6", value=fixed_ip_v6, expected_type=type_hints["fixed_ip_v6"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_network is not None:
            self._values["access_network"] = access_network
        if fixed_ip_v4 is not None:
            self._values["fixed_ip_v4"] = fixed_ip_v4
        if fixed_ip_v6 is not None:
            self._values["fixed_ip_v6"] = fixed_ip_v6
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if uuid is not None:
            self._values["uuid"] = uuid

    @builtins.property
    def access_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#access_network ComputeBmsServerV2#access_network}.'''
        result = self._values.get("access_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fixed_ip_v4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#fixed_ip_v4 ComputeBmsServerV2#fixed_ip_v4}.'''
        result = self._values.get("fixed_ip_v4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_ip_v6(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#fixed_ip_v6 ComputeBmsServerV2#fixed_ip_v6}.'''
        result = self._values.get("fixed_ip_v6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#name ComputeBmsServerV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#port ComputeBmsServerV2#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#uuid ComputeBmsServerV2#uuid}.'''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBmsServerV2Network(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBmsServerV2NetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2NetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fed6e18bdc34c2173787d33e7aa79f0b4dd3ef1ed32632bb828b884475e18b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeBmsServerV2NetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9c4c67d30eddfc0563e34a796e0e7242f9dcd034b77ff2e69648d812160c89)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBmsServerV2NetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2df63f4da12534bb6068f267fa73e0d9ba60bcc8a8c97073403790e47145171)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a46c20e397a5b133baeb13a8477c091344541c32e3287b440a42cf0c3899c708)
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
            type_hints = typing.get_type_hints(_typecheckingstub__544bbd28dc5cfce69cf44dc8c7dd7fb753c5292afa149e9a9e429f5bcbf329f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2Network]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2Network]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2Network]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16b436cad6515c94b267a03991bfc6e9e36c97a5d64a58f365e364bfae0a4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBmsServerV2NetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2NetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5538ae5000b3853a8c99ffcfb0438820056bb6b549d7fb9eda2cb1259f693791)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessNetwork")
    def reset_access_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessNetwork", []))

    @jsii.member(jsii_name="resetFixedIpV4")
    def reset_fixed_ip_v4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIpV4", []))

    @jsii.member(jsii_name="resetFixedIpV6")
    def reset_fixed_ip_v6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIpV6", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetUuid")
    def reset_uuid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUuid", []))

    @builtins.property
    @jsii.member(jsii_name="mac")
    def mac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mac"))

    @builtins.property
    @jsii.member(jsii_name="accessNetworkInput")
    def access_network_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedIpV4Input")
    def fixed_ip_v4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedIpV4Input"))

    @builtins.property
    @jsii.member(jsii_name="fixedIpV6Input")
    def fixed_ip_v6_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedIpV6Input"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="uuidInput")
    def uuid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uuidInput"))

    @builtins.property
    @jsii.member(jsii_name="accessNetwork")
    def access_network(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessNetwork"))

    @access_network.setter
    def access_network(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7871872cbc22237d19e0e625475197cae63b0f65028e8a25602a36ad66a75e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedIpV4")
    def fixed_ip_v4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedIpV4"))

    @fixed_ip_v4.setter
    def fixed_ip_v4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34dce8cecf399cf3cb97f09d05cafd69f2f766f770af130d13fa7b4f2bea57a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedIpV4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedIpV6")
    def fixed_ip_v6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedIpV6"))

    @fixed_ip_v6.setter
    def fixed_ip_v6(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3f3f20d96868d2aed63c5462dead4e7b9e4078e582831a710978a18672cc1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedIpV6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d862ba93050c73698043618a9e86aa844b34f577a34c38966a3e80295c16e126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a99811f3b2d686db5aa6725cef4166fe8078f3f4a69a1cb5b093407d3f2957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @uuid.setter
    def uuid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a5b9454c22947a2120be32a911b91175de987311ce0160642fc1495eac4791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2Network]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2Network]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2Network]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f5b1605bedf96547af6a2d43d550062829d46ad0bc8524db230877d0d878c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeBmsServerV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#create ComputeBmsServerV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#delete ComputeBmsServerV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#update ComputeBmsServerV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55d4a87efbb38d3c8681b6cc99262b4323deb5b205030fb08301c2f2f354d6f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#create ComputeBmsServerV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#delete ComputeBmsServerV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/compute_bms_server_v2#update ComputeBmsServerV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBmsServerV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBmsServerV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.computeBmsServerV2.ComputeBmsServerV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1de589bb17af7ca38c2f56156e2cbc39a24dacc99d63fa542a8a540761c14eb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__884b815abbd755e18a23ff7eb66bcb174c5c3252f40d03d85c3a229e3c340819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc09d247c633c198956f64e0f871f54473b60797324064a8b6b766323651af57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4540e9b50eab508ef63540df7456e2d2584a5130943f56cd80017120d38ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e35c1fd0fb5e000bee33975214a44e595b51aef48d4a3758ad39bc56b6dcc3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeBmsServerV2",
    "ComputeBmsServerV2BlockDevice",
    "ComputeBmsServerV2BlockDeviceList",
    "ComputeBmsServerV2BlockDeviceOutputReference",
    "ComputeBmsServerV2Config",
    "ComputeBmsServerV2Network",
    "ComputeBmsServerV2NetworkList",
    "ComputeBmsServerV2NetworkOutputReference",
    "ComputeBmsServerV2Timeouts",
    "ComputeBmsServerV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2840a3a07d2bb438f83213a34a8f28a618b191662bc59c6c5b0463d312ff1d47(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: builtins.str,
    name: builtins.str,
    admin_pass: typing.Optional[builtins.str] = None,
    block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBmsServerV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]]] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    flavor_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBmsServerV2Network, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeBmsServerV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__9bfe5e8736f1a372222daaf164c98ee273e5ebb8f49306c06426c72f26fb515b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118f061b6edc272b32ff4e243279ef0d51447d72b52a33343ed2d3b8fa75a8c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBmsServerV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdcca0e145619c85059306fade810de0644de21a11843906677e04f14005bb1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBmsServerV2Network, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbfa80cb024a2887c4eda982ea6c1a608315affc9c5d8bb70a533ba8e87fa53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09eee4acd1a35cfb396c6cd77ee246d678d79f34a4879e021ae96284ffe6d86e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6ad3d070ccaa870625a4b755356dedc00ecc74b2d57a8bff360e1d9d91f259(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6db3f2cbc423c0393916104013d1d2e082303803014608adc4e6076bf06042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e939625c0359947394b43e0fd37eb4d35497bc47fbb22ef7aed4f1203d4b1918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22a21be3a80cc40f8bdf08ebdf7edc3beab2ca7b7671913d5f56bc907944f5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3e27def3f85c8d1b0ac1c294b45eb669750123a332fdcf5dde25c8f7422706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2d61bcb27c9cf36a5a2c9405ed5b2e590ac987287ddf68e22797c3fa5ef56d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f19707479fdd5e644dc00305bc7a7f90a84b294081d3664a252eee3fee6e373(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a7166542d490a5b7bed528e4e7717b7252c89ba75737e104d812c1768c0887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa89fc97336157a0a4c7ce8cb1d6d777e22b3cecc05db0b27fa0560c7874b42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3a442e331230aa47d7c32b16a974396119470e44b36ceed9152600e8a39b06(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a817be5ec5b80e6c35e50421eac11519f32b7e994a3b2af0b2a63cf1f709a3fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa7d96eef15c50f7503c9af0019183eb3eac4f241c69eb5986e85e666c48901(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72683f48e6cfd50d9e02ad36a4ae8d1b5a0f95269ef9957cdaa163dc25141d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9946b69b0f59b531eef2664d54c26be605a7bc5100b139eb1bbfbd4c532092ab(
    *,
    source_type: builtins.str,
    boot_index: typing.Optional[jsii.Number] = None,
    delete_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_type: typing.Optional[builtins.str] = None,
    device_name: typing.Optional[builtins.str] = None,
    guest_format: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b66c72a18fd8180e62efdeb02b5d464cf05ac170aa0a1897ad007b22a6e9c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abc54029a0cf3f09946bc08ad6e3a36dd07f187e52e6cf22e25ab74600ea1d6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c077c88f4201f00dac43f74a2e8241e0108eacf9efc2bb34faeb06a88c8d7c63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d064adf881a6a5bfbdb64c793abe07933df656fed774668a079f930b7136120f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73dafaf9864696a2200bf6f4b8bbe5b31547bd3025d3ccecb67ef09a6710f9e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5d8ba6f53652620e0185790f7af0de3933bcee4c0206dd3def6594acc79326(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2BlockDevice]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bb474e138a28c2ae421ce5c517178a19f63d0f29800c96ad054a73e5b9ec21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc325003c11b1a2bcc18c57af322486d2dcb2234888269b4decd8bcc456e9eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339819f10b6f9d62406f6d3798f0e520bfc483f3a53c80add4c673ba3fe82c13(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979424b721207452618f0458e59a9a0bdee6c23ec20b7ff55652a93eb48acfb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a20d8c6671ca5580054b2c3b8d16a5c84402a481ecb03624ca475b8c5d8cb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671c0de81bfbd55a83faaf3a0b988773cac39cf787f7372a4a0dc9020f214ed7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47774c9347f159ce86dc4ec69248fd822ec74ce8e0790bbcf699a2622e9aac78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feed091479c384edff8ad6b165a4eb4243e240cac7daeed9574f37a5ff425a80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed7aee39c53d85b9b31f02c05015dd64e851409fa9c305816fc08b6b609f428(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabcfdc96b82d6389559757f05944f2e67b8e665e59df7450027baef7c443bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4a3c3103997bcc8cc0f9ab48adce3a372f403fe1f2a297e5f431139dcd6325(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2BlockDevice]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7aee9a7ba6349cc1c2622c3c58449b923fc278ef9cf82eca8536512d94cc1dc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: builtins.str,
    name: builtins.str,
    admin_pass: typing.Optional[builtins.str] = None,
    block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBmsServerV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]]] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    flavor_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBmsServerV2Network, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeBmsServerV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ecfb9a03a9e980d6cba7cfe370139e95731aaf18bff0c789c15f50b30bb495(
    *,
    access_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fixed_ip_v4: typing.Optional[builtins.str] = None,
    fixed_ip_v6: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fed6e18bdc34c2173787d33e7aa79f0b4dd3ef1ed32632bb828b884475e18b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9c4c67d30eddfc0563e34a796e0e7242f9dcd034b77ff2e69648d812160c89(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2df63f4da12534bb6068f267fa73e0d9ba60bcc8a8c97073403790e47145171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46c20e397a5b133baeb13a8477c091344541c32e3287b440a42cf0c3899c708(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544bbd28dc5cfce69cf44dc8c7dd7fb753c5292afa149e9a9e429f5bcbf329f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16b436cad6515c94b267a03991bfc6e9e36c97a5d64a58f365e364bfae0a4dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBmsServerV2Network]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5538ae5000b3853a8c99ffcfb0438820056bb6b549d7fb9eda2cb1259f693791(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7871872cbc22237d19e0e625475197cae63b0f65028e8a25602a36ad66a75e4b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34dce8cecf399cf3cb97f09d05cafd69f2f766f770af130d13fa7b4f2bea57a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3f3f20d96868d2aed63c5462dead4e7b9e4078e582831a710978a18672cc1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d862ba93050c73698043618a9e86aa844b34f577a34c38966a3e80295c16e126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a99811f3b2d686db5aa6725cef4166fe8078f3f4a69a1cb5b093407d3f2957(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a5b9454c22947a2120be32a911b91175de987311ce0160642fc1495eac4791(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f5b1605bedf96547af6a2d43d550062829d46ad0bc8524db230877d0d878c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2Network]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55d4a87efbb38d3c8681b6cc99262b4323deb5b205030fb08301c2f2f354d6f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de589bb17af7ca38c2f56156e2cbc39a24dacc99d63fa542a8a540761c14eb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884b815abbd755e18a23ff7eb66bcb174c5c3252f40d03d85c3a229e3c340819(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc09d247c633c198956f64e0f871f54473b60797324064a8b6b766323651af57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4540e9b50eab508ef63540df7456e2d2584a5130943f56cd80017120d38ca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e35c1fd0fb5e000bee33975214a44e595b51aef48d4a3758ad39bc56b6dcc3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBmsServerV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
