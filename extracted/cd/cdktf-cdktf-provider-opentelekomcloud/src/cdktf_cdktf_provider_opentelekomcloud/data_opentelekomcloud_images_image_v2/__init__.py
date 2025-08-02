r'''
# `data_opentelekomcloud_images_image_v2`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_images_image_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2).
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


class DataOpentelekomcloudImagesImageV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudImagesImageV2.DataOpentelekomcloudImagesImageV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2 opentelekomcloud_images_image_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        most_recent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        name_regex: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        size_max: typing.Optional[jsii.Number] = None,
        size_min: typing.Optional[jsii.Number] = None,
        sort_direction: typing.Optional[builtins.str] = None,
        sort_key: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        visibility: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2 opentelekomcloud_images_image_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param most_recent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#most_recent DataOpentelekomcloudImagesImageV2#most_recent}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#name DataOpentelekomcloudImagesImageV2#name}.
        :param name_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#name_regex DataOpentelekomcloudImagesImageV2#name_regex}.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#owner DataOpentelekomcloudImagesImageV2#owner}.
        :param size_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#size_max DataOpentelekomcloudImagesImageV2#size_max}.
        :param size_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#size_min DataOpentelekomcloudImagesImageV2#size_min}.
        :param sort_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#sort_direction DataOpentelekomcloudImagesImageV2#sort_direction}.
        :param sort_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#sort_key DataOpentelekomcloudImagesImageV2#sort_key}.
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#tag DataOpentelekomcloudImagesImageV2#tag}.
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#visibility DataOpentelekomcloudImagesImageV2#visibility}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd976001e86cb7872251d2b0820a43d903e1684679f89e4058e4400e2060e01a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataOpentelekomcloudImagesImageV2Config(
            most_recent=most_recent,
            name=name,
            name_regex=name_regex,
            owner=owner,
            size_max=size_max,
            size_min=size_min,
            sort_direction=sort_direction,
            sort_key=sort_key,
            tag=tag,
            visibility=visibility,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataOpentelekomcloudImagesImageV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudImagesImageV2 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudImagesImageV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudImagesImageV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88fedc1e29ed121f21bd24f12a5a478171e5c91cb564d45486c47e7fa545199)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetMostRecent")
    def reset_most_recent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMostRecent", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNameRegex")
    def reset_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameRegex", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetSizeMax")
    def reset_size_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeMax", []))

    @jsii.member(jsii_name="resetSizeMin")
    def reset_size_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeMin", []))

    @jsii.member(jsii_name="resetSortDirection")
    def reset_sort_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSortDirection", []))

    @jsii.member(jsii_name="resetSortKey")
    def reset_sort_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSortKey", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

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
    @jsii.member(jsii_name="backupId")
    def backup_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupId"))

    @builtins.property
    @jsii.member(jsii_name="checksum")
    def checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checksum"))

    @builtins.property
    @jsii.member(jsii_name="containerFormat")
    def container_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerFormat"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="dataOrigin")
    def data_origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataOrigin"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="diskFormat")
    def disk_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskFormat"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="hwFirmwareType")
    def hw_firmware_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hwFirmwareType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="imageSourceType")
    def image_source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageSourceType"))

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @builtins.property
    @jsii.member(jsii_name="isRegistered")
    def is_registered(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isRegistered"))

    @builtins.property
    @jsii.member(jsii_name="loginUser")
    def login_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginUser"))

    @builtins.property
    @jsii.member(jsii_name="minDisk")
    def min_disk(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minDisk"))

    @builtins.property
    @jsii.member(jsii_name="minRam")
    def min_ram(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRam"))

    @builtins.property
    @jsii.member(jsii_name="originalImageName")
    def original_image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originalImageName"))

    @builtins.property
    @jsii.member(jsii_name="osBit")
    def os_bit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osBit"))

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="protected")
    def protected(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "protected"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="sizeBytes")
    def size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="supportDiskIntensive")
    def support_disk_intensive(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportDiskIntensive"))

    @builtins.property
    @jsii.member(jsii_name="supportHighPerformance")
    def support_high_performance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportHighPerformance"))

    @builtins.property
    @jsii.member(jsii_name="supportKvm")
    def support_kvm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportKvm"))

    @builtins.property
    @jsii.member(jsii_name="supportKvmGpuType")
    def support_kvm_gpu_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportKvmGpuType"))

    @builtins.property
    @jsii.member(jsii_name="supportKvmInfiniband")
    def support_kvm_infiniband(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportKvmInfiniband"))

    @builtins.property
    @jsii.member(jsii_name="supportLargeMemory")
    def support_large_memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportLargeMemory"))

    @builtins.property
    @jsii.member(jsii_name="supportXen")
    def support_xen(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportXen"))

    @builtins.property
    @jsii.member(jsii_name="supportXenGpuType")
    def support_xen_gpu_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportXenGpuType"))

    @builtins.property
    @jsii.member(jsii_name="supportXenHana")
    def support_xen_hana(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportXenHana"))

    @builtins.property
    @jsii.member(jsii_name="systemCmkId")
    def system_cmk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemCmkId"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="virtualEnvType")
    def virtual_env_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualEnvType"))

    @builtins.property
    @jsii.member(jsii_name="mostRecentInput")
    def most_recent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mostRecentInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameRegexInput")
    def name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeMaxInput")
    def size_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeMinInput")
    def size_min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeMinInput"))

    @builtins.property
    @jsii.member(jsii_name="sortDirectionInput")
    def sort_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="sortKeyInput")
    def sort_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="mostRecent")
    def most_recent(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mostRecent"))

    @most_recent.setter
    def most_recent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33b11b04d3c35c3a8e91ca642f9bedcd98d36f367645bdb6ce03bfa24017f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mostRecent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd47bf831d7742d98736b25c09d9e56a24d4f0d26e9db3e28d71df6834a45f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameRegex")
    def name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameRegex"))

    @name_regex.setter
    def name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed328b53a4323783ab3a0bb5d2a95426310e0cfbb6674a183deeec6ed3407ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b062326ce27436681b74d5727493ff79a0b480109681cf62886da8423c4baec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeMax")
    def size_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeMax"))

    @size_max.setter
    def size_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f4e4563b3f919c28dd0a8286c57fa459c9f4ec893eaccc15fa7628dbe96b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeMin")
    def size_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeMin"))

    @size_min.setter
    def size_min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614c9260b72fe19fdf572b56b338da9051a404e416c4e617ec3d26eeab5b012d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeMin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sortDirection")
    def sort_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sortDirection"))

    @sort_direction.setter
    def sort_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e7389d52c58b2c9e1cdbfc96ffdfea6826322d8bf2127403ab3394815b9b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortDirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sortKey")
    def sort_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sortKey"))

    @sort_key.setter
    def sort_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a59604f49be5c6e8cf7b4881cc1b735ae008ac34efdc641dc4a5984b0970af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__952c3819bc3fcbfa60d507cdbb3ff8ef2f62bd503cb9a08af0830ca3a3ebb514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ffa942c87144d2857b32d555f1f31c28258d22aebd79938f24590e52aacfa0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudImagesImageV2.DataOpentelekomcloudImagesImageV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "most_recent": "mostRecent",
        "name": "name",
        "name_regex": "nameRegex",
        "owner": "owner",
        "size_max": "sizeMax",
        "size_min": "sizeMin",
        "sort_direction": "sortDirection",
        "sort_key": "sortKey",
        "tag": "tag",
        "visibility": "visibility",
    },
)
class DataOpentelekomcloudImagesImageV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        most_recent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        name_regex: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        size_max: typing.Optional[jsii.Number] = None,
        size_min: typing.Optional[jsii.Number] = None,
        sort_direction: typing.Optional[builtins.str] = None,
        sort_key: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        visibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param most_recent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#most_recent DataOpentelekomcloudImagesImageV2#most_recent}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#name DataOpentelekomcloudImagesImageV2#name}.
        :param name_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#name_regex DataOpentelekomcloudImagesImageV2#name_regex}.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#owner DataOpentelekomcloudImagesImageV2#owner}.
        :param size_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#size_max DataOpentelekomcloudImagesImageV2#size_max}.
        :param size_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#size_min DataOpentelekomcloudImagesImageV2#size_min}.
        :param sort_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#sort_direction DataOpentelekomcloudImagesImageV2#sort_direction}.
        :param sort_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#sort_key DataOpentelekomcloudImagesImageV2#sort_key}.
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#tag DataOpentelekomcloudImagesImageV2#tag}.
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#visibility DataOpentelekomcloudImagesImageV2#visibility}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5dad2563b9db2de356dd4c3e33479955cd57145966a56a366ee74ce908c364)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument most_recent", value=most_recent, expected_type=type_hints["most_recent"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_regex", value=name_regex, expected_type=type_hints["name_regex"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument size_max", value=size_max, expected_type=type_hints["size_max"])
            check_type(argname="argument size_min", value=size_min, expected_type=type_hints["size_min"])
            check_type(argname="argument sort_direction", value=sort_direction, expected_type=type_hints["sort_direction"])
            check_type(argname="argument sort_key", value=sort_key, expected_type=type_hints["sort_key"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
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
        if most_recent is not None:
            self._values["most_recent"] = most_recent
        if name is not None:
            self._values["name"] = name
        if name_regex is not None:
            self._values["name_regex"] = name_regex
        if owner is not None:
            self._values["owner"] = owner
        if size_max is not None:
            self._values["size_max"] = size_max
        if size_min is not None:
            self._values["size_min"] = size_min
        if sort_direction is not None:
            self._values["sort_direction"] = sort_direction
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if tag is not None:
            self._values["tag"] = tag
        if visibility is not None:
            self._values["visibility"] = visibility

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
    def most_recent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#most_recent DataOpentelekomcloudImagesImageV2#most_recent}.'''
        result = self._values.get("most_recent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#name DataOpentelekomcloudImagesImageV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#name_regex DataOpentelekomcloudImagesImageV2#name_regex}.'''
        result = self._values.get("name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#owner DataOpentelekomcloudImagesImageV2#owner}.'''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#size_max DataOpentelekomcloudImagesImageV2#size_max}.'''
        result = self._values.get("size_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size_min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#size_min DataOpentelekomcloudImagesImageV2#size_min}.'''
        result = self._values.get("size_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sort_direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#sort_direction DataOpentelekomcloudImagesImageV2#sort_direction}.'''
        result = self._values.get("sort_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#sort_key DataOpentelekomcloudImagesImageV2#sort_key}.'''
        result = self._values.get("sort_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#tag DataOpentelekomcloudImagesImageV2#tag}.'''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/images_image_v2#visibility DataOpentelekomcloudImagesImageV2#visibility}.'''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudImagesImageV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpentelekomcloudImagesImageV2",
    "DataOpentelekomcloudImagesImageV2Config",
]

publication.publish()

def _typecheckingstub__cd976001e86cb7872251d2b0820a43d903e1684679f89e4058e4400e2060e01a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    most_recent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    name_regex: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    size_max: typing.Optional[jsii.Number] = None,
    size_min: typing.Optional[jsii.Number] = None,
    sort_direction: typing.Optional[builtins.str] = None,
    sort_key: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    visibility: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d88fedc1e29ed121f21bd24f12a5a478171e5c91cb564d45486c47e7fa545199(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33b11b04d3c35c3a8e91ca642f9bedcd98d36f367645bdb6ce03bfa24017f0e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd47bf831d7742d98736b25c09d9e56a24d4f0d26e9db3e28d71df6834a45f89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed328b53a4323783ab3a0bb5d2a95426310e0cfbb6674a183deeec6ed3407ae2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b062326ce27436681b74d5727493ff79a0b480109681cf62886da8423c4baec2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f4e4563b3f919c28dd0a8286c57fa459c9f4ec893eaccc15fa7628dbe96b98(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614c9260b72fe19fdf572b56b338da9051a404e416c4e617ec3d26eeab5b012d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e7389d52c58b2c9e1cdbfc96ffdfea6826322d8bf2127403ab3394815b9b80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a59604f49be5c6e8cf7b4881cc1b735ae008ac34efdc641dc4a5984b0970af2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952c3819bc3fcbfa60d507cdbb3ff8ef2f62bd503cb9a08af0830ca3a3ebb514(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ffa942c87144d2857b32d555f1f31c28258d22aebd79938f24590e52aacfa0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5dad2563b9db2de356dd4c3e33479955cd57145966a56a366ee74ce908c364(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    most_recent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    name_regex: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    size_max: typing.Optional[jsii.Number] = None,
    size_min: typing.Optional[jsii.Number] = None,
    sort_direction: typing.Optional[builtins.str] = None,
    sort_key: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    visibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
