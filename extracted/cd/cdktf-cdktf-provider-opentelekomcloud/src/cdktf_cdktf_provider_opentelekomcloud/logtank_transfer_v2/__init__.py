r'''
# `opentelekomcloud_logtank_transfer_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_logtank_transfer_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2).
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


class LogtankTransferV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.logtankTransferV2.LogtankTransferV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2 opentelekomcloud_logtank_transfer_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        log_group_id: builtins.str,
        log_stream_ids: typing.Sequence[builtins.str],
        obs_bucket_name: builtins.str,
        period: jsii.Number,
        period_unit: builtins.str,
        storage_format: builtins.str,
        dir_prefix_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        prefix_name: typing.Optional[builtins.str] = None,
        switch_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2 opentelekomcloud_logtank_transfer_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#log_group_id LogtankTransferV2#log_group_id}.
        :param log_stream_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#log_stream_ids LogtankTransferV2#log_stream_ids}.
        :param obs_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#obs_bucket_name LogtankTransferV2#obs_bucket_name}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#period LogtankTransferV2#period}.
        :param period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#period_unit LogtankTransferV2#period_unit}.
        :param storage_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#storage_format LogtankTransferV2#storage_format}.
        :param dir_prefix_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#dir_prefix_name LogtankTransferV2#dir_prefix_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#id LogtankTransferV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param prefix_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#prefix_name LogtankTransferV2#prefix_name}.
        :param switch_on: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#switch_on LogtankTransferV2#switch_on}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9409101bb106b2b1ba0950b11e0661987fc8151fdec29513c52a1e8d78a37dad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LogtankTransferV2Config(
            log_group_id=log_group_id,
            log_stream_ids=log_stream_ids,
            obs_bucket_name=obs_bucket_name,
            period=period,
            period_unit=period_unit,
            storage_format=storage_format,
            dir_prefix_name=dir_prefix_name,
            id=id,
            prefix_name=prefix_name,
            switch_on=switch_on,
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
        '''Generates CDKTF code for importing a LogtankTransferV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LogtankTransferV2 to import.
        :param import_from_id: The id of the existing LogtankTransferV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LogtankTransferV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a84b9a4c747f6c9fbb1f8f2e53c6c38b3038babdb128f07deb245f8a7d7d100)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDirPrefixName")
    def reset_dir_prefix_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirPrefixName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPrefixName")
    def reset_prefix_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixName", []))

    @jsii.member(jsii_name="resetSwitchOn")
    def reset_switch_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwitchOn", []))

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
    def create_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @builtins.property
    @jsii.member(jsii_name="logTransferMode")
    def log_transfer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logTransferMode"))

    @builtins.property
    @jsii.member(jsii_name="logTransferType")
    def log_transfer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logTransferType"))

    @builtins.property
    @jsii.member(jsii_name="obsEncryptionEnable")
    def obs_encryption_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "obsEncryptionEnable"))

    @builtins.property
    @jsii.member(jsii_name="obsEncryptionId")
    def obs_encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsEncryptionId"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="dirPrefixNameInput")
    def dir_prefix_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dirPrefixNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupIdInput")
    def log_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamIdsInput")
    def log_stream_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logStreamIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="obsBucketNameInput")
    def obs_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsBucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="periodUnitInput")
    def period_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixNameInput")
    def prefix_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageFormatInput")
    def storage_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="switchOnInput")
    def switch_on_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "switchOnInput"))

    @builtins.property
    @jsii.member(jsii_name="dirPrefixName")
    def dir_prefix_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dirPrefixName"))

    @dir_prefix_name.setter
    def dir_prefix_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b797c5b3501698e494778d9cee6753fb8e475e946c3d01ebf42940d1df9e51fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dirPrefixName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b19b5c48e69c990f61828303c6dda37a5b9c64a56fd54266aac211ad5bfa2a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupId")
    def log_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupId"))

    @log_group_id.setter
    def log_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b34eadb2e74c1098293a29642af47ca27e15767745b82bde476bf5bde366fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamIds")
    def log_stream_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "logStreamIds"))

    @log_stream_ids.setter
    def log_stream_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67536d39432119c63d303f7edddb162e297c8571563c5616631ddc78a524772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsBucketName")
    def obs_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsBucketName"))

    @obs_bucket_name.setter
    def obs_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1889f3c3e47b1bd25581ca5972e5d154081859496400bbbf0f92dc63cd5d537a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsBucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "period"))

    @period.setter
    def period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5aa11983367978c1d46330b0b83cd94d262e9cbd48557b1d92240efb275121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodUnit")
    def period_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "periodUnit"))

    @period_unit.setter
    def period_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87af61e48c9eb2858c9024a870eb2d55aae410e567be21f27d551665a483e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixName")
    def prefix_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixName"))

    @prefix_name.setter
    def prefix_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f32a0569529a7ca64732cc95c046df775001c66eebb55d7d4ede937366fabd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageFormat")
    def storage_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageFormat"))

    @storage_format.setter
    def storage_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2855f1cfca81e75ad1b2e2fda5c80fd6959b2d102c791a168562a0bc2bc277b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="switchOn")
    def switch_on(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "switchOn"))

    @switch_on.setter
    def switch_on(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b547c00012078ab9b30beb3ef5d9c2ef146af930c11f35ae70bc11322a0aba81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "switchOn", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.logtankTransferV2.LogtankTransferV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "log_group_id": "logGroupId",
        "log_stream_ids": "logStreamIds",
        "obs_bucket_name": "obsBucketName",
        "period": "period",
        "period_unit": "periodUnit",
        "storage_format": "storageFormat",
        "dir_prefix_name": "dirPrefixName",
        "id": "id",
        "prefix_name": "prefixName",
        "switch_on": "switchOn",
    },
)
class LogtankTransferV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        log_group_id: builtins.str,
        log_stream_ids: typing.Sequence[builtins.str],
        obs_bucket_name: builtins.str,
        period: jsii.Number,
        period_unit: builtins.str,
        storage_format: builtins.str,
        dir_prefix_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        prefix_name: typing.Optional[builtins.str] = None,
        switch_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#log_group_id LogtankTransferV2#log_group_id}.
        :param log_stream_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#log_stream_ids LogtankTransferV2#log_stream_ids}.
        :param obs_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#obs_bucket_name LogtankTransferV2#obs_bucket_name}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#period LogtankTransferV2#period}.
        :param period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#period_unit LogtankTransferV2#period_unit}.
        :param storage_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#storage_format LogtankTransferV2#storage_format}.
        :param dir_prefix_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#dir_prefix_name LogtankTransferV2#dir_prefix_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#id LogtankTransferV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param prefix_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#prefix_name LogtankTransferV2#prefix_name}.
        :param switch_on: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#switch_on LogtankTransferV2#switch_on}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509046eb46bc63d0db6919041bba398ba3f103e83e54de5eb3891f66da8ec645)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument log_group_id", value=log_group_id, expected_type=type_hints["log_group_id"])
            check_type(argname="argument log_stream_ids", value=log_stream_ids, expected_type=type_hints["log_stream_ids"])
            check_type(argname="argument obs_bucket_name", value=obs_bucket_name, expected_type=type_hints["obs_bucket_name"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument period_unit", value=period_unit, expected_type=type_hints["period_unit"])
            check_type(argname="argument storage_format", value=storage_format, expected_type=type_hints["storage_format"])
            check_type(argname="argument dir_prefix_name", value=dir_prefix_name, expected_type=type_hints["dir_prefix_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument prefix_name", value=prefix_name, expected_type=type_hints["prefix_name"])
            check_type(argname="argument switch_on", value=switch_on, expected_type=type_hints["switch_on"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_id": log_group_id,
            "log_stream_ids": log_stream_ids,
            "obs_bucket_name": obs_bucket_name,
            "period": period,
            "period_unit": period_unit,
            "storage_format": storage_format,
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
        if dir_prefix_name is not None:
            self._values["dir_prefix_name"] = dir_prefix_name
        if id is not None:
            self._values["id"] = id
        if prefix_name is not None:
            self._values["prefix_name"] = prefix_name
        if switch_on is not None:
            self._values["switch_on"] = switch_on

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
    def log_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#log_group_id LogtankTransferV2#log_group_id}.'''
        result = self._values.get("log_group_id")
        assert result is not None, "Required property 'log_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#log_stream_ids LogtankTransferV2#log_stream_ids}.'''
        result = self._values.get("log_stream_ids")
        assert result is not None, "Required property 'log_stream_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def obs_bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#obs_bucket_name LogtankTransferV2#obs_bucket_name}.'''
        result = self._values.get("obs_bucket_name")
        assert result is not None, "Required property 'obs_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#period LogtankTransferV2#period}.'''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def period_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#period_unit LogtankTransferV2#period_unit}.'''
        result = self._values.get("period_unit")
        assert result is not None, "Required property 'period_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#storage_format LogtankTransferV2#storage_format}.'''
        result = self._values.get("storage_format")
        assert result is not None, "Required property 'storage_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dir_prefix_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#dir_prefix_name LogtankTransferV2#dir_prefix_name}.'''
        result = self._values.get("dir_prefix_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#id LogtankTransferV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#prefix_name LogtankTransferV2#prefix_name}.'''
        result = self._values.get("prefix_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def switch_on(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/logtank_transfer_v2#switch_on LogtankTransferV2#switch_on}.'''
        result = self._values.get("switch_on")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogtankTransferV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LogtankTransferV2",
    "LogtankTransferV2Config",
]

publication.publish()

def _typecheckingstub__9409101bb106b2b1ba0950b11e0661987fc8151fdec29513c52a1e8d78a37dad(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    log_group_id: builtins.str,
    log_stream_ids: typing.Sequence[builtins.str],
    obs_bucket_name: builtins.str,
    period: jsii.Number,
    period_unit: builtins.str,
    storage_format: builtins.str,
    dir_prefix_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    prefix_name: typing.Optional[builtins.str] = None,
    switch_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__8a84b9a4c747f6c9fbb1f8f2e53c6c38b3038babdb128f07deb245f8a7d7d100(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b797c5b3501698e494778d9cee6753fb8e475e946c3d01ebf42940d1df9e51fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19b5c48e69c990f61828303c6dda37a5b9c64a56fd54266aac211ad5bfa2a49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b34eadb2e74c1098293a29642af47ca27e15767745b82bde476bf5bde366fb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67536d39432119c63d303f7edddb162e297c8571563c5616631ddc78a524772(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1889f3c3e47b1bd25581ca5972e5d154081859496400bbbf0f92dc63cd5d537a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5aa11983367978c1d46330b0b83cd94d262e9cbd48557b1d92240efb275121(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87af61e48c9eb2858c9024a870eb2d55aae410e567be21f27d551665a483e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f32a0569529a7ca64732cc95c046df775001c66eebb55d7d4ede937366fabd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2855f1cfca81e75ad1b2e2fda5c80fd6959b2d102c791a168562a0bc2bc277b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b547c00012078ab9b30beb3ef5d9c2ef146af930c11f35ae70bc11322a0aba81(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509046eb46bc63d0db6919041bba398ba3f103e83e54de5eb3891f66da8ec645(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_group_id: builtins.str,
    log_stream_ids: typing.Sequence[builtins.str],
    obs_bucket_name: builtins.str,
    period: jsii.Number,
    period_unit: builtins.str,
    storage_format: builtins.str,
    dir_prefix_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    prefix_name: typing.Optional[builtins.str] = None,
    switch_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
