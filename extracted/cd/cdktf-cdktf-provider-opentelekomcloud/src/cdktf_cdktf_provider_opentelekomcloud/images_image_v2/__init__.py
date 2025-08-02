r'''
# `opentelekomcloud_images_image_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_images_image_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2).
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


class ImagesImageV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.imagesImageV2.ImagesImageV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2 opentelekomcloud_images_image_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        container_format: builtins.str,
        disk_format: builtins.str,
        name: builtins.str,
        hw_firmware_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_cache_path: typing.Optional[builtins.str] = None,
        image_source_url: typing.Optional[builtins.str] = None,
        local_file_path: typing.Optional[builtins.str] = None,
        min_disk_gb: typing.Optional[jsii.Number] = None,
        min_ram_mb: typing.Optional[jsii.Number] = None,
        protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ImagesImageV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2 opentelekomcloud_images_image_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param container_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#container_format ImagesImageV2#container_format}.
        :param disk_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#disk_format ImagesImageV2#disk_format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#name ImagesImageV2#name}.
        :param hw_firmware_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#hw_firmware_type ImagesImageV2#hw_firmware_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#id ImagesImageV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_cache_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#image_cache_path ImagesImageV2#image_cache_path}.
        :param image_source_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#image_source_url ImagesImageV2#image_source_url}.
        :param local_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#local_file_path ImagesImageV2#local_file_path}.
        :param min_disk_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#min_disk_gb ImagesImageV2#min_disk_gb}.
        :param min_ram_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#min_ram_mb ImagesImageV2#min_ram_mb}.
        :param protected: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#protected ImagesImageV2#protected}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#region ImagesImageV2#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#tags ImagesImageV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#timeouts ImagesImageV2#timeouts}
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#visibility ImagesImageV2#visibility}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a8b808190fc26dc9be1de1b1bef39056c398cb801ce86df1046ea17806aa17)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ImagesImageV2Config(
            container_format=container_format,
            disk_format=disk_format,
            name=name,
            hw_firmware_type=hw_firmware_type,
            id=id,
            image_cache_path=image_cache_path,
            image_source_url=image_source_url,
            local_file_path=local_file_path,
            min_disk_gb=min_disk_gb,
            min_ram_mb=min_ram_mb,
            protected=protected,
            region=region,
            tags=tags,
            timeouts=timeouts,
            visibility=visibility,
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
        '''Generates CDKTF code for importing a ImagesImageV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ImagesImageV2 to import.
        :param import_from_id: The id of the existing ImagesImageV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ImagesImageV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519aef9dc08098037c8ac72b2bd02d122e33e3bee897e66b07aa6e171af26f9b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#create ImagesImageV2#create}.
        '''
        value = ImagesImageV2Timeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetHwFirmwareType")
    def reset_hw_firmware_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHwFirmwareType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageCachePath")
    def reset_image_cache_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageCachePath", []))

    @jsii.member(jsii_name="resetImageSourceUrl")
    def reset_image_source_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageSourceUrl", []))

    @jsii.member(jsii_name="resetLocalFilePath")
    def reset_local_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalFilePath", []))

    @jsii.member(jsii_name="resetMinDiskGb")
    def reset_min_disk_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinDiskGb", []))

    @jsii.member(jsii_name="resetMinRamMb")
    def reset_min_ram_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinRamMb", []))

    @jsii.member(jsii_name="resetProtected")
    def reset_protected(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtected", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="checksum")
    def checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checksum"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ImagesImageV2TimeoutsOutputReference":
        return typing.cast("ImagesImageV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateAt")
    def update_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateAt"))

    @builtins.property
    @jsii.member(jsii_name="containerFormatInput")
    def container_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="diskFormatInput")
    def disk_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="hwFirmwareTypeInput")
    def hw_firmware_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hwFirmwareTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageCachePathInput")
    def image_cache_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageCachePathInput"))

    @builtins.property
    @jsii.member(jsii_name="imageSourceUrlInput")
    def image_source_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageSourceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="localFilePathInput")
    def local_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="minDiskGbInput")
    def min_disk_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minDiskGbInput"))

    @builtins.property
    @jsii.member(jsii_name="minRamMbInput")
    def min_ram_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRamMbInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedInput")
    def protected_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "protectedInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ImagesImageV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ImagesImageV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="containerFormat")
    def container_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerFormat"))

    @container_format.setter
    def container_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f19323c07f7eec8a087866ef9184425818f58f0072602ba5ff87061270cb282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskFormat")
    def disk_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskFormat"))

    @disk_format.setter
    def disk_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4954f38f487c5990046c55f8d7f0c618c715c132d5e094fcb444fb65597bb692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hwFirmwareType")
    def hw_firmware_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hwFirmwareType"))

    @hw_firmware_type.setter
    def hw_firmware_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb1370e3cfccff4ac3347bf210555b6f194a303da2240e763e5ca42ddbe1599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hwFirmwareType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a92dd83ce42f28d87ed6ee2b4d661d6d4b50b8d0c9a3959aea90e62b1b281dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageCachePath")
    def image_cache_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageCachePath"))

    @image_cache_path.setter
    def image_cache_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb1dc293b6577fa1b7948e4d85b937108a731b1fe4ac402a70af53bf1d5db22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageCachePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageSourceUrl")
    def image_source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageSourceUrl"))

    @image_source_url.setter
    def image_source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc6580edd8a7752b6ad4849685553cd227bce14d6c4fec4d718517a7c31a6e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageSourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localFilePath")
    def local_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localFilePath"))

    @local_file_path.setter
    def local_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f8ea20a87837ffb3f7b696140307e73ff4a486edf7d55ba990dd67409c6699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minDiskGb")
    def min_disk_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minDiskGb"))

    @min_disk_gb.setter
    def min_disk_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c0af42630b1d5f4b9593f80b22e4de9efa2507d3f00820ba36a2de34acb9191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minDiskGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRamMb")
    def min_ram_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRamMb"))

    @min_ram_mb.setter
    def min_ram_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06209b3efae653e95b11f6a7a33f5a2d381fb686c91d16e95fd65bbf52107a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRamMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed72923070366e87f5f5fae25346186f609ea9901927d1b302a2e91393b3d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protected")
    def protected(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "protected"))

    @protected.setter
    def protected(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4783cd1e252510a7ef5ea86b621e9d6cb28b02c336b2b8646f397dbf357303a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protected", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de93db97c78ecfc12537793800899a27f35ea2077838bc2af86d225c3f1f908b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68696100e88c03094726ce34ca565a95b395bb518050523ee03e95c38200a74a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2eae91f05d131b475147e01feb54a71cf8aed2a1b0a28bb41bc6be483c6823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.imagesImageV2.ImagesImageV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "container_format": "containerFormat",
        "disk_format": "diskFormat",
        "name": "name",
        "hw_firmware_type": "hwFirmwareType",
        "id": "id",
        "image_cache_path": "imageCachePath",
        "image_source_url": "imageSourceUrl",
        "local_file_path": "localFilePath",
        "min_disk_gb": "minDiskGb",
        "min_ram_mb": "minRamMb",
        "protected": "protected",
        "region": "region",
        "tags": "tags",
        "timeouts": "timeouts",
        "visibility": "visibility",
    },
)
class ImagesImageV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        container_format: builtins.str,
        disk_format: builtins.str,
        name: builtins.str,
        hw_firmware_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_cache_path: typing.Optional[builtins.str] = None,
        image_source_url: typing.Optional[builtins.str] = None,
        local_file_path: typing.Optional[builtins.str] = None,
        min_disk_gb: typing.Optional[jsii.Number] = None,
        min_ram_mb: typing.Optional[jsii.Number] = None,
        protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ImagesImageV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param container_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#container_format ImagesImageV2#container_format}.
        :param disk_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#disk_format ImagesImageV2#disk_format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#name ImagesImageV2#name}.
        :param hw_firmware_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#hw_firmware_type ImagesImageV2#hw_firmware_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#id ImagesImageV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_cache_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#image_cache_path ImagesImageV2#image_cache_path}.
        :param image_source_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#image_source_url ImagesImageV2#image_source_url}.
        :param local_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#local_file_path ImagesImageV2#local_file_path}.
        :param min_disk_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#min_disk_gb ImagesImageV2#min_disk_gb}.
        :param min_ram_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#min_ram_mb ImagesImageV2#min_ram_mb}.
        :param protected: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#protected ImagesImageV2#protected}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#region ImagesImageV2#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#tags ImagesImageV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#timeouts ImagesImageV2#timeouts}
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#visibility ImagesImageV2#visibility}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ImagesImageV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f553fd23d31b3a96d7f33c304d1c4ce254f0331e5fafc61d4f04c7cf8255c9a6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument container_format", value=container_format, expected_type=type_hints["container_format"])
            check_type(argname="argument disk_format", value=disk_format, expected_type=type_hints["disk_format"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument hw_firmware_type", value=hw_firmware_type, expected_type=type_hints["hw_firmware_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_cache_path", value=image_cache_path, expected_type=type_hints["image_cache_path"])
            check_type(argname="argument image_source_url", value=image_source_url, expected_type=type_hints["image_source_url"])
            check_type(argname="argument local_file_path", value=local_file_path, expected_type=type_hints["local_file_path"])
            check_type(argname="argument min_disk_gb", value=min_disk_gb, expected_type=type_hints["min_disk_gb"])
            check_type(argname="argument min_ram_mb", value=min_ram_mb, expected_type=type_hints["min_ram_mb"])
            check_type(argname="argument protected", value=protected, expected_type=type_hints["protected"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_format": container_format,
            "disk_format": disk_format,
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
        if hw_firmware_type is not None:
            self._values["hw_firmware_type"] = hw_firmware_type
        if id is not None:
            self._values["id"] = id
        if image_cache_path is not None:
            self._values["image_cache_path"] = image_cache_path
        if image_source_url is not None:
            self._values["image_source_url"] = image_source_url
        if local_file_path is not None:
            self._values["local_file_path"] = local_file_path
        if min_disk_gb is not None:
            self._values["min_disk_gb"] = min_disk_gb
        if min_ram_mb is not None:
            self._values["min_ram_mb"] = min_ram_mb
        if protected is not None:
            self._values["protected"] = protected
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
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
    def container_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#container_format ImagesImageV2#container_format}.'''
        result = self._values.get("container_format")
        assert result is not None, "Required property 'container_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#disk_format ImagesImageV2#disk_format}.'''
        result = self._values.get("disk_format")
        assert result is not None, "Required property 'disk_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#name ImagesImageV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hw_firmware_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#hw_firmware_type ImagesImageV2#hw_firmware_type}.'''
        result = self._values.get("hw_firmware_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#id ImagesImageV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_cache_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#image_cache_path ImagesImageV2#image_cache_path}.'''
        result = self._values.get("image_cache_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_source_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#image_source_url ImagesImageV2#image_source_url}.'''
        result = self._values.get("image_source_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_file_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#local_file_path ImagesImageV2#local_file_path}.'''
        result = self._values.get("local_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_disk_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#min_disk_gb ImagesImageV2#min_disk_gb}.'''
        result = self._values.get("min_disk_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ram_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#min_ram_mb ImagesImageV2#min_ram_mb}.'''
        result = self._values.get("min_ram_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protected(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#protected ImagesImageV2#protected}.'''
        result = self._values.get("protected")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#region ImagesImageV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#tags ImagesImageV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ImagesImageV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#timeouts ImagesImageV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ImagesImageV2Timeouts"], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#visibility ImagesImageV2#visibility}.'''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagesImageV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.imagesImageV2.ImagesImageV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class ImagesImageV2Timeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#create ImagesImageV2#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f5ba6dcf59032f522c6b852b9a1f0f523adb319d4c12fea75da922815448c5)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/images_image_v2#create ImagesImageV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagesImageV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagesImageV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.imagesImageV2.ImagesImageV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b56e8dbde28f565f48c90d2d99fcd1c78e78e29f85e303df9e605c1fa536a92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bbae000b098dde0d62ac997fe0bcd7aebc80ba012234c01eecb7a1f285fddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagesImageV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagesImageV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagesImageV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6c4f8c4f01ca467ef626a5643a76224c8b4ac179126b8693d084db4e47cda6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ImagesImageV2",
    "ImagesImageV2Config",
    "ImagesImageV2Timeouts",
    "ImagesImageV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a5a8b808190fc26dc9be1de1b1bef39056c398cb801ce86df1046ea17806aa17(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    container_format: builtins.str,
    disk_format: builtins.str,
    name: builtins.str,
    hw_firmware_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_cache_path: typing.Optional[builtins.str] = None,
    image_source_url: typing.Optional[builtins.str] = None,
    local_file_path: typing.Optional[builtins.str] = None,
    min_disk_gb: typing.Optional[jsii.Number] = None,
    min_ram_mb: typing.Optional[jsii.Number] = None,
    protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ImagesImageV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__519aef9dc08098037c8ac72b2bd02d122e33e3bee897e66b07aa6e171af26f9b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f19323c07f7eec8a087866ef9184425818f58f0072602ba5ff87061270cb282(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4954f38f487c5990046c55f8d7f0c618c715c132d5e094fcb444fb65597bb692(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb1370e3cfccff4ac3347bf210555b6f194a303da2240e763e5ca42ddbe1599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a92dd83ce42f28d87ed6ee2b4d661d6d4b50b8d0c9a3959aea90e62b1b281dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb1dc293b6577fa1b7948e4d85b937108a731b1fe4ac402a70af53bf1d5db22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc6580edd8a7752b6ad4849685553cd227bce14d6c4fec4d718517a7c31a6e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f8ea20a87837ffb3f7b696140307e73ff4a486edf7d55ba990dd67409c6699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0af42630b1d5f4b9593f80b22e4de9efa2507d3f00820ba36a2de34acb9191(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06209b3efae653e95b11f6a7a33f5a2d381fb686c91d16e95fd65bbf52107a41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed72923070366e87f5f5fae25346186f609ea9901927d1b302a2e91393b3d50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4783cd1e252510a7ef5ea86b621e9d6cb28b02c336b2b8646f397dbf357303a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de93db97c78ecfc12537793800899a27f35ea2077838bc2af86d225c3f1f908b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68696100e88c03094726ce34ca565a95b395bb518050523ee03e95c38200a74a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2eae91f05d131b475147e01feb54a71cf8aed2a1b0a28bb41bc6be483c6823(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f553fd23d31b3a96d7f33c304d1c4ce254f0331e5fafc61d4f04c7cf8255c9a6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_format: builtins.str,
    disk_format: builtins.str,
    name: builtins.str,
    hw_firmware_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_cache_path: typing.Optional[builtins.str] = None,
    image_source_url: typing.Optional[builtins.str] = None,
    local_file_path: typing.Optional[builtins.str] = None,
    min_disk_gb: typing.Optional[jsii.Number] = None,
    min_ram_mb: typing.Optional[jsii.Number] = None,
    protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ImagesImageV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f5ba6dcf59032f522c6b852b9a1f0f523adb319d4c12fea75da922815448c5(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b56e8dbde28f565f48c90d2d99fcd1c78e78e29f85e303df9e605c1fa536a92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bbae000b098dde0d62ac997fe0bcd7aebc80ba012234c01eecb7a1f285fddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6c4f8c4f01ca467ef626a5643a76224c8b4ac179126b8693d084db4e47cda6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagesImageV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
