r'''
# `opentelekomcloud_lts_host_access_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_lts_host_access_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3).
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


class LtsHostAccessV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3 opentelekomcloud_lts_host_access_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_config: typing.Union["LtsHostAccessV3AccessConfig", typing.Dict[builtins.str, typing.Any]],
        log_group_id: builtins.str,
        log_stream_id: builtins.str,
        name: builtins.str,
        binary_collect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        log_split: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3 opentelekomcloud_lts_host_access_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#access_config LtsHostAccessV3#access_config}
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#log_group_id LtsHostAccessV3#log_group_id}.
        :param log_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#log_stream_id LtsHostAccessV3#log_stream_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#name LtsHostAccessV3#name}.
        :param binary_collect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#binary_collect LtsHostAccessV3#binary_collect}.
        :param host_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#host_group_ids LtsHostAccessV3#host_group_ids}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#id LtsHostAccessV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_split: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#log_split LtsHostAccessV3#log_split}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#tags LtsHostAccessV3#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81f1ef4c7b082cbf13a5f2c0da269b41821404cf82ee429c44c060e9e85a6a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LtsHostAccessV3Config(
            access_config=access_config,
            log_group_id=log_group_id,
            log_stream_id=log_stream_id,
            name=name,
            binary_collect=binary_collect,
            host_group_ids=host_group_ids,
            id=id,
            log_split=log_split,
            tags=tags,
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
        '''Generates CDKTF code for importing a LtsHostAccessV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LtsHostAccessV3 to import.
        :param import_from_id: The id of the existing LtsHostAccessV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LtsHostAccessV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2cea6c67d4498fe46a37433cb094b6bea4fc76801a7b535c4b93dd3bd2d230f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        *,
        paths: typing.Sequence[builtins.str],
        black_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        multi_log_format: typing.Optional[typing.Union["LtsHostAccessV3AccessConfigMultiLogFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        single_log_format: typing.Optional[typing.Union["LtsHostAccessV3AccessConfigSingleLogFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_log_info: typing.Optional[typing.Union["LtsHostAccessV3AccessConfigWindowsLogInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#paths LtsHostAccessV3#paths}.
        :param black_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#black_paths LtsHostAccessV3#black_paths}.
        :param multi_log_format: multi_log_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#multi_log_format LtsHostAccessV3#multi_log_format}
        :param single_log_format: single_log_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#single_log_format LtsHostAccessV3#single_log_format}
        :param windows_log_info: windows_log_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#windows_log_info LtsHostAccessV3#windows_log_info}
        '''
        value = LtsHostAccessV3AccessConfig(
            paths=paths,
            black_paths=black_paths,
            multi_log_format=multi_log_format,
            single_log_format=single_log_format,
            windows_log_info=windows_log_info,
        )

        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="resetBinaryCollect")
    def reset_binary_collect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryCollect", []))

    @jsii.member(jsii_name="resetHostGroupIds")
    def reset_host_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostGroupIds", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogSplit")
    def reset_log_split(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogSplit", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="accessConfig")
    def access_config(self) -> "LtsHostAccessV3AccessConfigOutputReference":
        return typing.cast("LtsHostAccessV3AccessConfigOutputReference", jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessType")
    def access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessType"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(self) -> typing.Optional["LtsHostAccessV3AccessConfig"]:
        return typing.cast(typing.Optional["LtsHostAccessV3AccessConfig"], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryCollectInput")
    def binary_collect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "binaryCollectInput"))

    @builtins.property
    @jsii.member(jsii_name="hostGroupIdsInput")
    def host_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupIdInput")
    def log_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logSplitInput")
    def log_split_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logSplitInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamIdInput")
    def log_stream_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryCollect")
    def binary_collect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "binaryCollect"))

    @binary_collect.setter
    def binary_collect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0240b8849f86a9f527430f9055847448b977dcb5ad317671b7699fa82b01eb64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryCollect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostGroupIds")
    def host_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostGroupIds"))

    @host_group_ids.setter
    def host_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bde640140a593a3f92072269136b7e7a146c0643078e5dc96c086b948724de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011747f55073debe9d6f606a26c2efa880add98c4c51c5337e42da8d405d1e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupId")
    def log_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupId"))

    @log_group_id.setter
    def log_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54aeb092c2472d5da28f514c2d920e109e537f06c230942b022688e48c745069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logSplit")
    def log_split(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logSplit"))

    @log_split.setter
    def log_split(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fe7072c8759043790215c248c3e1932a9a759f62c217ba6620601e782648b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logSplit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamId")
    def log_stream_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamId"))

    @log_stream_id.setter
    def log_stream_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cb3f7173910110bfd1a5cf32662b14ec5028b1e1b6e48ea10c2f1e42784429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a120f53aa9ef5b8f91a58d7f298c4a5bd4d8ea67b466d352bf0c68ae26092ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04a3952586e89e8cbfc7b5a8cd1952f48c6a8336d6362d50b527d4754904f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3AccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "paths": "paths",
        "black_paths": "blackPaths",
        "multi_log_format": "multiLogFormat",
        "single_log_format": "singleLogFormat",
        "windows_log_info": "windowsLogInfo",
    },
)
class LtsHostAccessV3AccessConfig:
    def __init__(
        self,
        *,
        paths: typing.Sequence[builtins.str],
        black_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        multi_log_format: typing.Optional[typing.Union["LtsHostAccessV3AccessConfigMultiLogFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        single_log_format: typing.Optional[typing.Union["LtsHostAccessV3AccessConfigSingleLogFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_log_info: typing.Optional[typing.Union["LtsHostAccessV3AccessConfigWindowsLogInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#paths LtsHostAccessV3#paths}.
        :param black_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#black_paths LtsHostAccessV3#black_paths}.
        :param multi_log_format: multi_log_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#multi_log_format LtsHostAccessV3#multi_log_format}
        :param single_log_format: single_log_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#single_log_format LtsHostAccessV3#single_log_format}
        :param windows_log_info: windows_log_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#windows_log_info LtsHostAccessV3#windows_log_info}
        '''
        if isinstance(multi_log_format, dict):
            multi_log_format = LtsHostAccessV3AccessConfigMultiLogFormat(**multi_log_format)
        if isinstance(single_log_format, dict):
            single_log_format = LtsHostAccessV3AccessConfigSingleLogFormat(**single_log_format)
        if isinstance(windows_log_info, dict):
            windows_log_info = LtsHostAccessV3AccessConfigWindowsLogInfo(**windows_log_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf53e888fda8fe7296289c37e1df814470d8e5f43443d341a477a2cb6bab71d)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument black_paths", value=black_paths, expected_type=type_hints["black_paths"])
            check_type(argname="argument multi_log_format", value=multi_log_format, expected_type=type_hints["multi_log_format"])
            check_type(argname="argument single_log_format", value=single_log_format, expected_type=type_hints["single_log_format"])
            check_type(argname="argument windows_log_info", value=windows_log_info, expected_type=type_hints["windows_log_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "paths": paths,
        }
        if black_paths is not None:
            self._values["black_paths"] = black_paths
        if multi_log_format is not None:
            self._values["multi_log_format"] = multi_log_format
        if single_log_format is not None:
            self._values["single_log_format"] = single_log_format
        if windows_log_info is not None:
            self._values["windows_log_info"] = windows_log_info

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#paths LtsHostAccessV3#paths}.'''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def black_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#black_paths LtsHostAccessV3#black_paths}.'''
        result = self._values.get("black_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def multi_log_format(
        self,
    ) -> typing.Optional["LtsHostAccessV3AccessConfigMultiLogFormat"]:
        '''multi_log_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#multi_log_format LtsHostAccessV3#multi_log_format}
        '''
        result = self._values.get("multi_log_format")
        return typing.cast(typing.Optional["LtsHostAccessV3AccessConfigMultiLogFormat"], result)

    @builtins.property
    def single_log_format(
        self,
    ) -> typing.Optional["LtsHostAccessV3AccessConfigSingleLogFormat"]:
        '''single_log_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#single_log_format LtsHostAccessV3#single_log_format}
        '''
        result = self._values.get("single_log_format")
        return typing.cast(typing.Optional["LtsHostAccessV3AccessConfigSingleLogFormat"], result)

    @builtins.property
    def windows_log_info(
        self,
    ) -> typing.Optional["LtsHostAccessV3AccessConfigWindowsLogInfo"]:
        '''windows_log_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#windows_log_info LtsHostAccessV3#windows_log_info}
        '''
        result = self._values.get("windows_log_info")
        return typing.cast(typing.Optional["LtsHostAccessV3AccessConfigWindowsLogInfo"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsHostAccessV3AccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3AccessConfigMultiLogFormat",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class LtsHostAccessV3AccessConfigMultiLogFormat:
    def __init__(
        self,
        *,
        mode: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#mode LtsHostAccessV3#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#value LtsHostAccessV3#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8252e993620600ab124e34587a8649666ece3e954fc97e873e40ee6e9f7bd29c)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#mode LtsHostAccessV3#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#value LtsHostAccessV3#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsHostAccessV3AccessConfigMultiLogFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsHostAccessV3AccessConfigMultiLogFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3AccessConfigMultiLogFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__153641afdc959d4b395dd2ad5df597f6c73fae7ba43c0bc93e203bdcb22c2306)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6e290a8deb6ddeb45f542da2547237a78dd38d273f3f5d73b9c70250fd5d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3660efcd744dfb05669c6022817d07b379c01d924741ff592503943c3091baf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LtsHostAccessV3AccessConfigMultiLogFormat]:
        return typing.cast(typing.Optional[LtsHostAccessV3AccessConfigMultiLogFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsHostAccessV3AccessConfigMultiLogFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6a1538817f36995355930699602c2e699f2ef7c2f343e7b03cfe405baf5bd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LtsHostAccessV3AccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3AccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3318bb55b9544dc6f7ed4efc418576f24a507af1118041852ad3988f1a86d7c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMultiLogFormat")
    def put_multi_log_format(
        self,
        *,
        mode: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#mode LtsHostAccessV3#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#value LtsHostAccessV3#value}.
        '''
        value_ = LtsHostAccessV3AccessConfigMultiLogFormat(mode=mode, value=value)

        return typing.cast(None, jsii.invoke(self, "putMultiLogFormat", [value_]))

    @jsii.member(jsii_name="putSingleLogFormat")
    def put_single_log_format(
        self,
        *,
        mode: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#mode LtsHostAccessV3#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#value LtsHostAccessV3#value}.
        '''
        value_ = LtsHostAccessV3AccessConfigSingleLogFormat(mode=mode, value=value)

        return typing.cast(None, jsii.invoke(self, "putSingleLogFormat", [value_]))

    @jsii.member(jsii_name="putWindowsLogInfo")
    def put_windows_log_info(
        self,
        *,
        categories: typing.Sequence[builtins.str],
        event_level: typing.Sequence[builtins.str],
        time_offset: jsii.Number,
        time_offset_unit: builtins.str,
    ) -> None:
        '''
        :param categories: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#categories LtsHostAccessV3#categories}.
        :param event_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#event_level LtsHostAccessV3#event_level}.
        :param time_offset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#time_offset LtsHostAccessV3#time_offset}.
        :param time_offset_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#time_offset_unit LtsHostAccessV3#time_offset_unit}.
        '''
        value = LtsHostAccessV3AccessConfigWindowsLogInfo(
            categories=categories,
            event_level=event_level,
            time_offset=time_offset,
            time_offset_unit=time_offset_unit,
        )

        return typing.cast(None, jsii.invoke(self, "putWindowsLogInfo", [value]))

    @jsii.member(jsii_name="resetBlackPaths")
    def reset_black_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlackPaths", []))

    @jsii.member(jsii_name="resetMultiLogFormat")
    def reset_multi_log_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiLogFormat", []))

    @jsii.member(jsii_name="resetSingleLogFormat")
    def reset_single_log_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleLogFormat", []))

    @jsii.member(jsii_name="resetWindowsLogInfo")
    def reset_windows_log_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsLogInfo", []))

    @builtins.property
    @jsii.member(jsii_name="multiLogFormat")
    def multi_log_format(
        self,
    ) -> LtsHostAccessV3AccessConfigMultiLogFormatOutputReference:
        return typing.cast(LtsHostAccessV3AccessConfigMultiLogFormatOutputReference, jsii.get(self, "multiLogFormat"))

    @builtins.property
    @jsii.member(jsii_name="singleLogFormat")
    def single_log_format(
        self,
    ) -> "LtsHostAccessV3AccessConfigSingleLogFormatOutputReference":
        return typing.cast("LtsHostAccessV3AccessConfigSingleLogFormatOutputReference", jsii.get(self, "singleLogFormat"))

    @builtins.property
    @jsii.member(jsii_name="windowsLogInfo")
    def windows_log_info(
        self,
    ) -> "LtsHostAccessV3AccessConfigWindowsLogInfoOutputReference":
        return typing.cast("LtsHostAccessV3AccessConfigWindowsLogInfoOutputReference", jsii.get(self, "windowsLogInfo"))

    @builtins.property
    @jsii.member(jsii_name="blackPathsInput")
    def black_paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "blackPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="multiLogFormatInput")
    def multi_log_format_input(
        self,
    ) -> typing.Optional[LtsHostAccessV3AccessConfigMultiLogFormat]:
        return typing.cast(typing.Optional[LtsHostAccessV3AccessConfigMultiLogFormat], jsii.get(self, "multiLogFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="singleLogFormatInput")
    def single_log_format_input(
        self,
    ) -> typing.Optional["LtsHostAccessV3AccessConfigSingleLogFormat"]:
        return typing.cast(typing.Optional["LtsHostAccessV3AccessConfigSingleLogFormat"], jsii.get(self, "singleLogFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsLogInfoInput")
    def windows_log_info_input(
        self,
    ) -> typing.Optional["LtsHostAccessV3AccessConfigWindowsLogInfo"]:
        return typing.cast(typing.Optional["LtsHostAccessV3AccessConfigWindowsLogInfo"], jsii.get(self, "windowsLogInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="blackPaths")
    def black_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "blackPaths"))

    @black_paths.setter
    def black_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15954ab9e1b76c4ce27d3a255cfb6b51a9dbdcfb55aceee6c392b5ae0c949851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blackPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797999db353a642318270f95e46ce738bb9ca95c59d631cd12a92efa19151a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LtsHostAccessV3AccessConfig]:
        return typing.cast(typing.Optional[LtsHostAccessV3AccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsHostAccessV3AccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817e4f63f1c7693ef38aa811b6d72c350f7da60193bcadf18f60dc1b45e6d694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3AccessConfigSingleLogFormat",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class LtsHostAccessV3AccessConfigSingleLogFormat:
    def __init__(
        self,
        *,
        mode: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#mode LtsHostAccessV3#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#value LtsHostAccessV3#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e77952a6807bc0226512e43f6e122d276bde4cf88f6fff4de7b9adf8de2b83)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#mode LtsHostAccessV3#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#value LtsHostAccessV3#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsHostAccessV3AccessConfigSingleLogFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsHostAccessV3AccessConfigSingleLogFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3AccessConfigSingleLogFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf798fc551f95e22a645cd29abaa69d15f5cbae9522ddc92df50592db7dcbe33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cca796378c3f2ba3b0d2be31e49fa27079cabf028c7e648fa666b8c518d9580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8b8894a0e3811382fe3bbf19a7284587e647871aef9a9553b2baec0b12e9e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LtsHostAccessV3AccessConfigSingleLogFormat]:
        return typing.cast(typing.Optional[LtsHostAccessV3AccessConfigSingleLogFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsHostAccessV3AccessConfigSingleLogFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fdce42aa7a1103cf688556f8e1949f0b01f453d91c0adcd9d21d766407a5f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3AccessConfigWindowsLogInfo",
    jsii_struct_bases=[],
    name_mapping={
        "categories": "categories",
        "event_level": "eventLevel",
        "time_offset": "timeOffset",
        "time_offset_unit": "timeOffsetUnit",
    },
)
class LtsHostAccessV3AccessConfigWindowsLogInfo:
    def __init__(
        self,
        *,
        categories: typing.Sequence[builtins.str],
        event_level: typing.Sequence[builtins.str],
        time_offset: jsii.Number,
        time_offset_unit: builtins.str,
    ) -> None:
        '''
        :param categories: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#categories LtsHostAccessV3#categories}.
        :param event_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#event_level LtsHostAccessV3#event_level}.
        :param time_offset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#time_offset LtsHostAccessV3#time_offset}.
        :param time_offset_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#time_offset_unit LtsHostAccessV3#time_offset_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e44abeacb5c127bdee363e2cbdcd50e16f649da11d3e7b830e151c7eafa622)
            check_type(argname="argument categories", value=categories, expected_type=type_hints["categories"])
            check_type(argname="argument event_level", value=event_level, expected_type=type_hints["event_level"])
            check_type(argname="argument time_offset", value=time_offset, expected_type=type_hints["time_offset"])
            check_type(argname="argument time_offset_unit", value=time_offset_unit, expected_type=type_hints["time_offset_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "categories": categories,
            "event_level": event_level,
            "time_offset": time_offset,
            "time_offset_unit": time_offset_unit,
        }

    @builtins.property
    def categories(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#categories LtsHostAccessV3#categories}.'''
        result = self._values.get("categories")
        assert result is not None, "Required property 'categories' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def event_level(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#event_level LtsHostAccessV3#event_level}.'''
        result = self._values.get("event_level")
        assert result is not None, "Required property 'event_level' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def time_offset(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#time_offset LtsHostAccessV3#time_offset}.'''
        result = self._values.get("time_offset")
        assert result is not None, "Required property 'time_offset' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time_offset_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#time_offset_unit LtsHostAccessV3#time_offset_unit}.'''
        result = self._values.get("time_offset_unit")
        assert result is not None, "Required property 'time_offset_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsHostAccessV3AccessConfigWindowsLogInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsHostAccessV3AccessConfigWindowsLogInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3AccessConfigWindowsLogInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e0327e88fe87156039bd59c1798cae277b8a505d189d8bd1e3e656e130c4067)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="categoriesInput")
    def categories_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "categoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="eventLevelInput")
    def event_level_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="timeOffsetInput")
    def time_offset_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeOffsetUnitInput")
    def time_offset_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeOffsetUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="categories")
    def categories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "categories"))

    @categories.setter
    def categories(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808795a7ab1dbabd7a55a55c0414e6e81a64b0439b162b305ab00078c246403d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "categories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventLevel")
    def event_level(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventLevel"))

    @event_level.setter
    def event_level(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc78a39b8babc134d1cd08caa50bc12ebaa67cb5be50b6dd0d391488f7f76c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeOffset")
    def time_offset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeOffset"))

    @time_offset.setter
    def time_offset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8367935b4d579aafbc3f5dafa8af7c7313cc1edf8fd2bd76ae2c9bea697d8d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeOffsetUnit")
    def time_offset_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeOffsetUnit"))

    @time_offset_unit.setter
    def time_offset_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8fba9882e73d70f4db68a053a57478df572a0b1372a63105955107315ee0871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeOffsetUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LtsHostAccessV3AccessConfigWindowsLogInfo]:
        return typing.cast(typing.Optional[LtsHostAccessV3AccessConfigWindowsLogInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsHostAccessV3AccessConfigWindowsLogInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3903c293d545b99465801106ea8aab596dba9de367de948f690571d45bbb7345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsHostAccessV3.LtsHostAccessV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_config": "accessConfig",
        "log_group_id": "logGroupId",
        "log_stream_id": "logStreamId",
        "name": "name",
        "binary_collect": "binaryCollect",
        "host_group_ids": "hostGroupIds",
        "id": "id",
        "log_split": "logSplit",
        "tags": "tags",
    },
)
class LtsHostAccessV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_config: typing.Union[LtsHostAccessV3AccessConfig, typing.Dict[builtins.str, typing.Any]],
        log_group_id: builtins.str,
        log_stream_id: builtins.str,
        name: builtins.str,
        binary_collect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        log_split: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#access_config LtsHostAccessV3#access_config}
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#log_group_id LtsHostAccessV3#log_group_id}.
        :param log_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#log_stream_id LtsHostAccessV3#log_stream_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#name LtsHostAccessV3#name}.
        :param binary_collect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#binary_collect LtsHostAccessV3#binary_collect}.
        :param host_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#host_group_ids LtsHostAccessV3#host_group_ids}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#id LtsHostAccessV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_split: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#log_split LtsHostAccessV3#log_split}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#tags LtsHostAccessV3#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_config, dict):
            access_config = LtsHostAccessV3AccessConfig(**access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98cee6bba30302222f7152365fa965afd7425733ae2f93caeb030035534dc46)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument log_group_id", value=log_group_id, expected_type=type_hints["log_group_id"])
            check_type(argname="argument log_stream_id", value=log_stream_id, expected_type=type_hints["log_stream_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument binary_collect", value=binary_collect, expected_type=type_hints["binary_collect"])
            check_type(argname="argument host_group_ids", value=host_group_ids, expected_type=type_hints["host_group_ids"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_split", value=log_split, expected_type=type_hints["log_split"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_config": access_config,
            "log_group_id": log_group_id,
            "log_stream_id": log_stream_id,
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
        if binary_collect is not None:
            self._values["binary_collect"] = binary_collect
        if host_group_ids is not None:
            self._values["host_group_ids"] = host_group_ids
        if id is not None:
            self._values["id"] = id
        if log_split is not None:
            self._values["log_split"] = log_split
        if tags is not None:
            self._values["tags"] = tags

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
    def access_config(self) -> LtsHostAccessV3AccessConfig:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#access_config LtsHostAccessV3#access_config}
        '''
        result = self._values.get("access_config")
        assert result is not None, "Required property 'access_config' is missing"
        return typing.cast(LtsHostAccessV3AccessConfig, result)

    @builtins.property
    def log_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#log_group_id LtsHostAccessV3#log_group_id}.'''
        result = self._values.get("log_group_id")
        assert result is not None, "Required property 'log_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#log_stream_id LtsHostAccessV3#log_stream_id}.'''
        result = self._values.get("log_stream_id")
        assert result is not None, "Required property 'log_stream_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#name LtsHostAccessV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def binary_collect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#binary_collect LtsHostAccessV3#binary_collect}.'''
        result = self._values.get("binary_collect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#host_group_ids LtsHostAccessV3#host_group_ids}.'''
        result = self._values.get("host_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#id LtsHostAccessV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_split(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#log_split LtsHostAccessV3#log_split}.'''
        result = self._values.get("log_split")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_host_access_v3#tags LtsHostAccessV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsHostAccessV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LtsHostAccessV3",
    "LtsHostAccessV3AccessConfig",
    "LtsHostAccessV3AccessConfigMultiLogFormat",
    "LtsHostAccessV3AccessConfigMultiLogFormatOutputReference",
    "LtsHostAccessV3AccessConfigOutputReference",
    "LtsHostAccessV3AccessConfigSingleLogFormat",
    "LtsHostAccessV3AccessConfigSingleLogFormatOutputReference",
    "LtsHostAccessV3AccessConfigWindowsLogInfo",
    "LtsHostAccessV3AccessConfigWindowsLogInfoOutputReference",
    "LtsHostAccessV3Config",
]

publication.publish()

def _typecheckingstub__d81f1ef4c7b082cbf13a5f2c0da269b41821404cf82ee429c44c060e9e85a6a3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_config: typing.Union[LtsHostAccessV3AccessConfig, typing.Dict[builtins.str, typing.Any]],
    log_group_id: builtins.str,
    log_stream_id: builtins.str,
    name: builtins.str,
    binary_collect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    log_split: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__e2cea6c67d4498fe46a37433cb094b6bea4fc76801a7b535c4b93dd3bd2d230f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0240b8849f86a9f527430f9055847448b977dcb5ad317671b7699fa82b01eb64(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bde640140a593a3f92072269136b7e7a146c0643078e5dc96c086b948724de8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011747f55073debe9d6f606a26c2efa880add98c4c51c5337e42da8d405d1e59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54aeb092c2472d5da28f514c2d920e109e537f06c230942b022688e48c745069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fe7072c8759043790215c248c3e1932a9a759f62c217ba6620601e782648b1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cb3f7173910110bfd1a5cf32662b14ec5028b1e1b6e48ea10c2f1e42784429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a120f53aa9ef5b8f91a58d7f298c4a5bd4d8ea67b466d352bf0c68ae26092ca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04a3952586e89e8cbfc7b5a8cd1952f48c6a8336d6362d50b527d4754904f13(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf53e888fda8fe7296289c37e1df814470d8e5f43443d341a477a2cb6bab71d(
    *,
    paths: typing.Sequence[builtins.str],
    black_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    multi_log_format: typing.Optional[typing.Union[LtsHostAccessV3AccessConfigMultiLogFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    single_log_format: typing.Optional[typing.Union[LtsHostAccessV3AccessConfigSingleLogFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    windows_log_info: typing.Optional[typing.Union[LtsHostAccessV3AccessConfigWindowsLogInfo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8252e993620600ab124e34587a8649666ece3e954fc97e873e40ee6e9f7bd29c(
    *,
    mode: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153641afdc959d4b395dd2ad5df597f6c73fae7ba43c0bc93e203bdcb22c2306(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6e290a8deb6ddeb45f542da2547237a78dd38d273f3f5d73b9c70250fd5d77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3660efcd744dfb05669c6022817d07b379c01d924741ff592503943c3091baf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6a1538817f36995355930699602c2e699f2ef7c2f343e7b03cfe405baf5bd2(
    value: typing.Optional[LtsHostAccessV3AccessConfigMultiLogFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3318bb55b9544dc6f7ed4efc418576f24a507af1118041852ad3988f1a86d7c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15954ab9e1b76c4ce27d3a255cfb6b51a9dbdcfb55aceee6c392b5ae0c949851(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797999db353a642318270f95e46ce738bb9ca95c59d631cd12a92efa19151a3d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817e4f63f1c7693ef38aa811b6d72c350f7da60193bcadf18f60dc1b45e6d694(
    value: typing.Optional[LtsHostAccessV3AccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e77952a6807bc0226512e43f6e122d276bde4cf88f6fff4de7b9adf8de2b83(
    *,
    mode: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf798fc551f95e22a645cd29abaa69d15f5cbae9522ddc92df50592db7dcbe33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cca796378c3f2ba3b0d2be31e49fa27079cabf028c7e648fa666b8c518d9580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8b8894a0e3811382fe3bbf19a7284587e647871aef9a9553b2baec0b12e9e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fdce42aa7a1103cf688556f8e1949f0b01f453d91c0adcd9d21d766407a5f2(
    value: typing.Optional[LtsHostAccessV3AccessConfigSingleLogFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e44abeacb5c127bdee363e2cbdcd50e16f649da11d3e7b830e151c7eafa622(
    *,
    categories: typing.Sequence[builtins.str],
    event_level: typing.Sequence[builtins.str],
    time_offset: jsii.Number,
    time_offset_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0327e88fe87156039bd59c1798cae277b8a505d189d8bd1e3e656e130c4067(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808795a7ab1dbabd7a55a55c0414e6e81a64b0439b162b305ab00078c246403d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc78a39b8babc134d1cd08caa50bc12ebaa67cb5be50b6dd0d391488f7f76c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8367935b4d579aafbc3f5dafa8af7c7313cc1edf8fd2bd76ae2c9bea697d8d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fba9882e73d70f4db68a053a57478df572a0b1372a63105955107315ee0871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3903c293d545b99465801106ea8aab596dba9de367de948f690571d45bbb7345(
    value: typing.Optional[LtsHostAccessV3AccessConfigWindowsLogInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98cee6bba30302222f7152365fa965afd7425733ae2f93caeb030035534dc46(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_config: typing.Union[LtsHostAccessV3AccessConfig, typing.Dict[builtins.str, typing.Any]],
    log_group_id: builtins.str,
    log_stream_id: builtins.str,
    name: builtins.str,
    binary_collect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    log_split: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
