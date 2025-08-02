r'''
# `opentelekomcloud_lts_transfer_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_lts_transfer_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2).
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


class LtsTransferV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2 opentelekomcloud_lts_transfer_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        log_group_id: builtins.str,
        log_streams: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LtsTransferV2LogStreams", typing.Dict[builtins.str, typing.Any]]]],
        log_transfer_info: typing.Union["LtsTransferV2LogTransferInfo", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2 opentelekomcloud_lts_transfer_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_group_id LtsTransferV2#log_group_id}.
        :param log_streams: log_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_streams LtsTransferV2#log_streams}
        :param log_transfer_info: log_transfer_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_info LtsTransferV2#log_transfer_info}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#id LtsTransferV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efee44badb84184a22a03f208850a89b6e8633e950d6a866937a64f7b1a93693)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LtsTransferV2Config(
            log_group_id=log_group_id,
            log_streams=log_streams,
            log_transfer_info=log_transfer_info,
            id=id,
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
        '''Generates CDKTF code for importing a LtsTransferV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LtsTransferV2 to import.
        :param import_from_id: The id of the existing LtsTransferV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LtsTransferV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01603daa08e99a11dac5b424980ccb14c2af2ec3ff8cd7eccf2346986cccf95a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLogStreams")
    def put_log_streams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LtsTransferV2LogStreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea09126ac0c709d2efdd223f499e51a4eca68eecb715398d3c0dd31a578aa810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogStreams", [value]))

    @jsii.member(jsii_name="putLogTransferInfo")
    def put_log_transfer_info(
        self,
        *,
        log_storage_format: builtins.str,
        log_transfer_detail: typing.Union["LtsTransferV2LogTransferInfoLogTransferDetail", typing.Dict[builtins.str, typing.Any]],
        log_transfer_mode: builtins.str,
        log_transfer_status: builtins.str,
        log_transfer_type: builtins.str,
        log_agency_transfer: typing.Optional[typing.Union["LtsTransferV2LogTransferInfoLogAgencyTransfer", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param log_storage_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_storage_format LtsTransferV2#log_storage_format}.
        :param log_transfer_detail: log_transfer_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_detail LtsTransferV2#log_transfer_detail}
        :param log_transfer_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_mode LtsTransferV2#log_transfer_mode}.
        :param log_transfer_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_status LtsTransferV2#log_transfer_status}.
        :param log_transfer_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_type LtsTransferV2#log_transfer_type}.
        :param log_agency_transfer: log_agency_transfer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_agency_transfer LtsTransferV2#log_agency_transfer}
        '''
        value = LtsTransferV2LogTransferInfo(
            log_storage_format=log_storage_format,
            log_transfer_detail=log_transfer_detail,
            log_transfer_mode=log_transfer_mode,
            log_transfer_status=log_transfer_status,
            log_transfer_type=log_transfer_type,
            log_agency_transfer=log_agency_transfer,
        )

        return typing.cast(None, jsii.invoke(self, "putLogTransferInfo", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @builtins.property
    @jsii.member(jsii_name="logStreams")
    def log_streams(self) -> "LtsTransferV2LogStreamsList":
        return typing.cast("LtsTransferV2LogStreamsList", jsii.get(self, "logStreams"))

    @builtins.property
    @jsii.member(jsii_name="logTransferInfo")
    def log_transfer_info(self) -> "LtsTransferV2LogTransferInfoOutputReference":
        return typing.cast("LtsTransferV2LogTransferInfoOutputReference", jsii.get(self, "logTransferInfo"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupIdInput")
    def log_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamsInput")
    def log_streams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsTransferV2LogStreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsTransferV2LogStreams"]]], jsii.get(self, "logStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="logTransferInfoInput")
    def log_transfer_info_input(
        self,
    ) -> typing.Optional["LtsTransferV2LogTransferInfo"]:
        return typing.cast(typing.Optional["LtsTransferV2LogTransferInfo"], jsii.get(self, "logTransferInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__695b9f3d9ca0dbae195df7f78d1e3642258411c86a8915188620ecf661566c17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupId")
    def log_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupId"))

    @log_group_id.setter
    def log_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b4731a3028379abdc748701707f20cd235b8c83b8019452ece8c859fb7553b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2Config",
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
        "log_streams": "logStreams",
        "log_transfer_info": "logTransferInfo",
        "id": "id",
    },
)
class LtsTransferV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        log_streams: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LtsTransferV2LogStreams", typing.Dict[builtins.str, typing.Any]]]],
        log_transfer_info: typing.Union["LtsTransferV2LogTransferInfo", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_group_id LtsTransferV2#log_group_id}.
        :param log_streams: log_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_streams LtsTransferV2#log_streams}
        :param log_transfer_info: log_transfer_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_info LtsTransferV2#log_transfer_info}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#id LtsTransferV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(log_transfer_info, dict):
            log_transfer_info = LtsTransferV2LogTransferInfo(**log_transfer_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1a669818c79a57df0a6acb54a61b8349e2956d277e007f5060eca29baef4d6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument log_group_id", value=log_group_id, expected_type=type_hints["log_group_id"])
            check_type(argname="argument log_streams", value=log_streams, expected_type=type_hints["log_streams"])
            check_type(argname="argument log_transfer_info", value=log_transfer_info, expected_type=type_hints["log_transfer_info"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_id": log_group_id,
            "log_streams": log_streams,
            "log_transfer_info": log_transfer_info,
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_group_id LtsTransferV2#log_group_id}.'''
        result = self._values.get("log_group_id")
        assert result is not None, "Required property 'log_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_streams(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsTransferV2LogStreams"]]:
        '''log_streams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_streams LtsTransferV2#log_streams}
        '''
        result = self._values.get("log_streams")
        assert result is not None, "Required property 'log_streams' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsTransferV2LogStreams"]], result)

    @builtins.property
    def log_transfer_info(self) -> "LtsTransferV2LogTransferInfo":
        '''log_transfer_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_info LtsTransferV2#log_transfer_info}
        '''
        result = self._values.get("log_transfer_info")
        assert result is not None, "Required property 'log_transfer_info' is missing"
        return typing.cast("LtsTransferV2LogTransferInfo", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#id LtsTransferV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsTransferV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2LogStreams",
    jsii_struct_bases=[],
    name_mapping={"log_stream_id": "logStreamId", "log_stream_name": "logStreamName"},
)
class LtsTransferV2LogStreams:
    def __init__(
        self,
        *,
        log_stream_id: builtins.str,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_stream_id LtsTransferV2#log_stream_id}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_stream_name LtsTransferV2#log_stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447844dff92f2b05259a9ec3edde7cc46efffc6a166861b213df8d33ad881a45)
            check_type(argname="argument log_stream_id", value=log_stream_id, expected_type=type_hints["log_stream_id"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_stream_id": log_stream_id,
        }
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_stream_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_stream_id LtsTransferV2#log_stream_id}.'''
        result = self._values.get("log_stream_id")
        assert result is not None, "Required property 'log_stream_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_stream_name LtsTransferV2#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsTransferV2LogStreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsTransferV2LogStreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2LogStreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c5f0303dfcaa48b657a6fb61e4615d66655b49a138c8d57cfe6d4a8daaead24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LtsTransferV2LogStreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9445b6f3627a150de8ccd3c8a0fd409bc4aaa659c980fdbdedeae3bd235e4514)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LtsTransferV2LogStreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1716463575cb30f870c7e1323c1e974365168e907ea09eb024cd7b6db6faa10e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__004924bd0e8c536f02a9cbe9b5bc53e9d18d34ba6d8c856ee798fc6d6faf7c6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba0ccc6c85bd2ced540feb7c35dfd7798bc310ed187083ec38f8877000b7b136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsTransferV2LogStreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsTransferV2LogStreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsTransferV2LogStreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd79040cc2597efe4e05f6c393af639e18e357d591cec819bcca077e39a9b60b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LtsTransferV2LogStreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2LogStreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b2a8b4b79e8930c34ff76627c318166c922e947755dd41defcb0536303c5b0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="logStreamIdInput")
    def log_stream_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamId")
    def log_stream_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamId"))

    @log_stream_id.setter
    def log_stream_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09aa6651d8c84b4a37c5a8c42730c6e4e850e891564695cf7188b0879a6c8fb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea91ec7c9f0c6e768528c87b3c0d374dad5a5fc3fcaca00cb0f6290951de8b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsTransferV2LogStreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsTransferV2LogStreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsTransferV2LogStreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611979d54098872c57a7c976eff3023c0f817b2367f9a404e0a1a07a8b324787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2LogTransferInfo",
    jsii_struct_bases=[],
    name_mapping={
        "log_storage_format": "logStorageFormat",
        "log_transfer_detail": "logTransferDetail",
        "log_transfer_mode": "logTransferMode",
        "log_transfer_status": "logTransferStatus",
        "log_transfer_type": "logTransferType",
        "log_agency_transfer": "logAgencyTransfer",
    },
)
class LtsTransferV2LogTransferInfo:
    def __init__(
        self,
        *,
        log_storage_format: builtins.str,
        log_transfer_detail: typing.Union["LtsTransferV2LogTransferInfoLogTransferDetail", typing.Dict[builtins.str, typing.Any]],
        log_transfer_mode: builtins.str,
        log_transfer_status: builtins.str,
        log_transfer_type: builtins.str,
        log_agency_transfer: typing.Optional[typing.Union["LtsTransferV2LogTransferInfoLogAgencyTransfer", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param log_storage_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_storage_format LtsTransferV2#log_storage_format}.
        :param log_transfer_detail: log_transfer_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_detail LtsTransferV2#log_transfer_detail}
        :param log_transfer_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_mode LtsTransferV2#log_transfer_mode}.
        :param log_transfer_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_status LtsTransferV2#log_transfer_status}.
        :param log_transfer_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_type LtsTransferV2#log_transfer_type}.
        :param log_agency_transfer: log_agency_transfer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_agency_transfer LtsTransferV2#log_agency_transfer}
        '''
        if isinstance(log_transfer_detail, dict):
            log_transfer_detail = LtsTransferV2LogTransferInfoLogTransferDetail(**log_transfer_detail)
        if isinstance(log_agency_transfer, dict):
            log_agency_transfer = LtsTransferV2LogTransferInfoLogAgencyTransfer(**log_agency_transfer)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982899c585f85e61cfcb1048897f72761898d9cb3d6e6c87fcab800c759f4286)
            check_type(argname="argument log_storage_format", value=log_storage_format, expected_type=type_hints["log_storage_format"])
            check_type(argname="argument log_transfer_detail", value=log_transfer_detail, expected_type=type_hints["log_transfer_detail"])
            check_type(argname="argument log_transfer_mode", value=log_transfer_mode, expected_type=type_hints["log_transfer_mode"])
            check_type(argname="argument log_transfer_status", value=log_transfer_status, expected_type=type_hints["log_transfer_status"])
            check_type(argname="argument log_transfer_type", value=log_transfer_type, expected_type=type_hints["log_transfer_type"])
            check_type(argname="argument log_agency_transfer", value=log_agency_transfer, expected_type=type_hints["log_agency_transfer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_storage_format": log_storage_format,
            "log_transfer_detail": log_transfer_detail,
            "log_transfer_mode": log_transfer_mode,
            "log_transfer_status": log_transfer_status,
            "log_transfer_type": log_transfer_type,
        }
        if log_agency_transfer is not None:
            self._values["log_agency_transfer"] = log_agency_transfer

    @builtins.property
    def log_storage_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_storage_format LtsTransferV2#log_storage_format}.'''
        result = self._values.get("log_storage_format")
        assert result is not None, "Required property 'log_storage_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_transfer_detail(self) -> "LtsTransferV2LogTransferInfoLogTransferDetail":
        '''log_transfer_detail block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_detail LtsTransferV2#log_transfer_detail}
        '''
        result = self._values.get("log_transfer_detail")
        assert result is not None, "Required property 'log_transfer_detail' is missing"
        return typing.cast("LtsTransferV2LogTransferInfoLogTransferDetail", result)

    @builtins.property
    def log_transfer_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_mode LtsTransferV2#log_transfer_mode}.'''
        result = self._values.get("log_transfer_mode")
        assert result is not None, "Required property 'log_transfer_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_transfer_status(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_status LtsTransferV2#log_transfer_status}.'''
        result = self._values.get("log_transfer_status")
        assert result is not None, "Required property 'log_transfer_status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_transfer_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_transfer_type LtsTransferV2#log_transfer_type}.'''
        result = self._values.get("log_transfer_type")
        assert result is not None, "Required property 'log_transfer_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_agency_transfer(
        self,
    ) -> typing.Optional["LtsTransferV2LogTransferInfoLogAgencyTransfer"]:
        '''log_agency_transfer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#log_agency_transfer LtsTransferV2#log_agency_transfer}
        '''
        result = self._values.get("log_agency_transfer")
        return typing.cast(typing.Optional["LtsTransferV2LogTransferInfoLogAgencyTransfer"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsTransferV2LogTransferInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2LogTransferInfoLogAgencyTransfer",
    jsii_struct_bases=[],
    name_mapping={
        "agency_domain_id": "agencyDomainId",
        "agency_domain_name": "agencyDomainName",
        "agency_name": "agencyName",
        "agency_project_id": "agencyProjectId",
    },
)
class LtsTransferV2LogTransferInfoLogAgencyTransfer:
    def __init__(
        self,
        *,
        agency_domain_id: builtins.str,
        agency_domain_name: builtins.str,
        agency_name: builtins.str,
        agency_project_id: builtins.str,
    ) -> None:
        '''
        :param agency_domain_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_domain_id LtsTransferV2#agency_domain_id}.
        :param agency_domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_domain_name LtsTransferV2#agency_domain_name}.
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_name LtsTransferV2#agency_name}.
        :param agency_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_project_id LtsTransferV2#agency_project_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18841c1f00e8e130c0bc1ba872983b8cfce45fcb31a709ec0c7512a88c93b9dd)
            check_type(argname="argument agency_domain_id", value=agency_domain_id, expected_type=type_hints["agency_domain_id"])
            check_type(argname="argument agency_domain_name", value=agency_domain_name, expected_type=type_hints["agency_domain_name"])
            check_type(argname="argument agency_name", value=agency_name, expected_type=type_hints["agency_name"])
            check_type(argname="argument agency_project_id", value=agency_project_id, expected_type=type_hints["agency_project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agency_domain_id": agency_domain_id,
            "agency_domain_name": agency_domain_name,
            "agency_name": agency_name,
            "agency_project_id": agency_project_id,
        }

    @builtins.property
    def agency_domain_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_domain_id LtsTransferV2#agency_domain_id}.'''
        result = self._values.get("agency_domain_id")
        assert result is not None, "Required property 'agency_domain_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agency_domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_domain_name LtsTransferV2#agency_domain_name}.'''
        result = self._values.get("agency_domain_name")
        assert result is not None, "Required property 'agency_domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agency_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_name LtsTransferV2#agency_name}.'''
        result = self._values.get("agency_name")
        assert result is not None, "Required property 'agency_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agency_project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_project_id LtsTransferV2#agency_project_id}.'''
        result = self._values.get("agency_project_id")
        assert result is not None, "Required property 'agency_project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsTransferV2LogTransferInfoLogAgencyTransfer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsTransferV2LogTransferInfoLogAgencyTransferOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2LogTransferInfoLogAgencyTransferOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60e6bd4afab6a436d868a72f7807264983608e69b497a9fbef78dd55883173ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="agencyDomainIdInput")
    def agency_domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyDomainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyDomainNameInput")
    def agency_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyNameInput")
    def agency_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyProjectIdInput")
    def agency_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyDomainId")
    def agency_domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyDomainId"))

    @agency_domain_id.setter
    def agency_domain_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0fe20ca770b01eb7c49e19e7578b9ff065d892c0d9f14a462a13d0ec9ceb4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyDomainId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agencyDomainName")
    def agency_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyDomainName"))

    @agency_domain_name.setter
    def agency_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d483ff034c76257f902c3d24d96389ba0147e4e75119742ec9321640ab0ab4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agencyName")
    def agency_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyName"))

    @agency_name.setter
    def agency_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3b9ebddaa7270bcafec6f986243af066b7fd965506881b08af23a47b8108a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agencyProjectId")
    def agency_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyProjectId"))

    @agency_project_id.setter
    def agency_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185fd44843ae5b6aa55f6f4177574261293851a72f2e9be7a55a211b0e02cf62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LtsTransferV2LogTransferInfoLogAgencyTransfer]:
        return typing.cast(typing.Optional[LtsTransferV2LogTransferInfoLogAgencyTransfer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsTransferV2LogTransferInfoLogAgencyTransfer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bfec65db02b2c6e300a338dd8748fcc98c55c5d410cd68c534bb064f6d9e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2LogTransferInfoLogTransferDetail",
    jsii_struct_bases=[],
    name_mapping={
        "obs_bucket_name": "obsBucketName",
        "obs_dir_prefix_name": "obsDirPrefixName",
        "obs_encrypted_enable": "obsEncryptedEnable",
        "obs_encrypted_id": "obsEncryptedId",
        "obs_eps_id": "obsEpsId",
        "obs_period": "obsPeriod",
        "obs_period_unit": "obsPeriodUnit",
        "obs_prefix_name": "obsPrefixName",
        "obs_time_zone": "obsTimeZone",
        "obs_time_zone_id": "obsTimeZoneId",
        "obs_transfer_path": "obsTransferPath",
        "tags": "tags",
    },
)
class LtsTransferV2LogTransferInfoLogTransferDetail:
    def __init__(
        self,
        *,
        obs_bucket_name: typing.Optional[builtins.str] = None,
        obs_dir_prefix_name: typing.Optional[builtins.str] = None,
        obs_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        obs_encrypted_id: typing.Optional[builtins.str] = None,
        obs_eps_id: typing.Optional[builtins.str] = None,
        obs_period: typing.Optional[jsii.Number] = None,
        obs_period_unit: typing.Optional[builtins.str] = None,
        obs_prefix_name: typing.Optional[builtins.str] = None,
        obs_time_zone: typing.Optional[builtins.str] = None,
        obs_time_zone_id: typing.Optional[builtins.str] = None,
        obs_transfer_path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param obs_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_bucket_name LtsTransferV2#obs_bucket_name}.
        :param obs_dir_prefix_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_dir_prefix_name LtsTransferV2#obs_dir_prefix_name}.
        :param obs_encrypted_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_encrypted_enable LtsTransferV2#obs_encrypted_enable}.
        :param obs_encrypted_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_encrypted_id LtsTransferV2#obs_encrypted_id}.
        :param obs_eps_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_eps_id LtsTransferV2#obs_eps_id}.
        :param obs_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_period LtsTransferV2#obs_period}.
        :param obs_period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_period_unit LtsTransferV2#obs_period_unit}.
        :param obs_prefix_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_prefix_name LtsTransferV2#obs_prefix_name}.
        :param obs_time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_time_zone LtsTransferV2#obs_time_zone}.
        :param obs_time_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_time_zone_id LtsTransferV2#obs_time_zone_id}.
        :param obs_transfer_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_transfer_path LtsTransferV2#obs_transfer_path}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#tags LtsTransferV2#tags}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ba40ea411194e00a5727c27d5eac768afb2d35a4df05d44d572050d555f77a)
            check_type(argname="argument obs_bucket_name", value=obs_bucket_name, expected_type=type_hints["obs_bucket_name"])
            check_type(argname="argument obs_dir_prefix_name", value=obs_dir_prefix_name, expected_type=type_hints["obs_dir_prefix_name"])
            check_type(argname="argument obs_encrypted_enable", value=obs_encrypted_enable, expected_type=type_hints["obs_encrypted_enable"])
            check_type(argname="argument obs_encrypted_id", value=obs_encrypted_id, expected_type=type_hints["obs_encrypted_id"])
            check_type(argname="argument obs_eps_id", value=obs_eps_id, expected_type=type_hints["obs_eps_id"])
            check_type(argname="argument obs_period", value=obs_period, expected_type=type_hints["obs_period"])
            check_type(argname="argument obs_period_unit", value=obs_period_unit, expected_type=type_hints["obs_period_unit"])
            check_type(argname="argument obs_prefix_name", value=obs_prefix_name, expected_type=type_hints["obs_prefix_name"])
            check_type(argname="argument obs_time_zone", value=obs_time_zone, expected_type=type_hints["obs_time_zone"])
            check_type(argname="argument obs_time_zone_id", value=obs_time_zone_id, expected_type=type_hints["obs_time_zone_id"])
            check_type(argname="argument obs_transfer_path", value=obs_transfer_path, expected_type=type_hints["obs_transfer_path"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if obs_bucket_name is not None:
            self._values["obs_bucket_name"] = obs_bucket_name
        if obs_dir_prefix_name is not None:
            self._values["obs_dir_prefix_name"] = obs_dir_prefix_name
        if obs_encrypted_enable is not None:
            self._values["obs_encrypted_enable"] = obs_encrypted_enable
        if obs_encrypted_id is not None:
            self._values["obs_encrypted_id"] = obs_encrypted_id
        if obs_eps_id is not None:
            self._values["obs_eps_id"] = obs_eps_id
        if obs_period is not None:
            self._values["obs_period"] = obs_period
        if obs_period_unit is not None:
            self._values["obs_period_unit"] = obs_period_unit
        if obs_prefix_name is not None:
            self._values["obs_prefix_name"] = obs_prefix_name
        if obs_time_zone is not None:
            self._values["obs_time_zone"] = obs_time_zone
        if obs_time_zone_id is not None:
            self._values["obs_time_zone_id"] = obs_time_zone_id
        if obs_transfer_path is not None:
            self._values["obs_transfer_path"] = obs_transfer_path
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def obs_bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_bucket_name LtsTransferV2#obs_bucket_name}.'''
        result = self._values.get("obs_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_dir_prefix_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_dir_prefix_name LtsTransferV2#obs_dir_prefix_name}.'''
        result = self._values.get("obs_dir_prefix_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_encrypted_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_encrypted_enable LtsTransferV2#obs_encrypted_enable}.'''
        result = self._values.get("obs_encrypted_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def obs_encrypted_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_encrypted_id LtsTransferV2#obs_encrypted_id}.'''
        result = self._values.get("obs_encrypted_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_eps_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_eps_id LtsTransferV2#obs_eps_id}.'''
        result = self._values.get("obs_eps_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_period LtsTransferV2#obs_period}.'''
        result = self._values.get("obs_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def obs_period_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_period_unit LtsTransferV2#obs_period_unit}.'''
        result = self._values.get("obs_period_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_prefix_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_prefix_name LtsTransferV2#obs_prefix_name}.'''
        result = self._values.get("obs_prefix_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_time_zone LtsTransferV2#obs_time_zone}.'''
        result = self._values.get("obs_time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_time_zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_time_zone_id LtsTransferV2#obs_time_zone_id}.'''
        result = self._values.get("obs_time_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_transfer_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_transfer_path LtsTransferV2#obs_transfer_path}.'''
        result = self._values.get("obs_transfer_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#tags LtsTransferV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsTransferV2LogTransferInfoLogTransferDetail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsTransferV2LogTransferInfoLogTransferDetailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2LogTransferInfoLogTransferDetailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aebccb4bed376e750e72cd504b5c942d9df8c897a171e94f903a91a3f339825)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetObsBucketName")
    def reset_obs_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsBucketName", []))

    @jsii.member(jsii_name="resetObsDirPrefixName")
    def reset_obs_dir_prefix_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsDirPrefixName", []))

    @jsii.member(jsii_name="resetObsEncryptedEnable")
    def reset_obs_encrypted_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsEncryptedEnable", []))

    @jsii.member(jsii_name="resetObsEncryptedId")
    def reset_obs_encrypted_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsEncryptedId", []))

    @jsii.member(jsii_name="resetObsEpsId")
    def reset_obs_eps_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsEpsId", []))

    @jsii.member(jsii_name="resetObsPeriod")
    def reset_obs_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsPeriod", []))

    @jsii.member(jsii_name="resetObsPeriodUnit")
    def reset_obs_period_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsPeriodUnit", []))

    @jsii.member(jsii_name="resetObsPrefixName")
    def reset_obs_prefix_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsPrefixName", []))

    @jsii.member(jsii_name="resetObsTimeZone")
    def reset_obs_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsTimeZone", []))

    @jsii.member(jsii_name="resetObsTimeZoneId")
    def reset_obs_time_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsTimeZoneId", []))

    @jsii.member(jsii_name="resetObsTransferPath")
    def reset_obs_transfer_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsTransferPath", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="obsBucketNameInput")
    def obs_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsBucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="obsDirPrefixNameInput")
    def obs_dir_prefix_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsDirPrefixNameInput"))

    @builtins.property
    @jsii.member(jsii_name="obsEncryptedEnableInput")
    def obs_encrypted_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "obsEncryptedEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="obsEncryptedIdInput")
    def obs_encrypted_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsEncryptedIdInput"))

    @builtins.property
    @jsii.member(jsii_name="obsEpsIdInput")
    def obs_eps_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsEpsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="obsPeriodInput")
    def obs_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "obsPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="obsPeriodUnitInput")
    def obs_period_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsPeriodUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="obsPrefixNameInput")
    def obs_prefix_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsPrefixNameInput"))

    @builtins.property
    @jsii.member(jsii_name="obsTimeZoneIdInput")
    def obs_time_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsTimeZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="obsTimeZoneInput")
    def obs_time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsTimeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="obsTransferPathInput")
    def obs_transfer_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsTransferPathInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="obsBucketName")
    def obs_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsBucketName"))

    @obs_bucket_name.setter
    def obs_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b83b3eb5283e031039b07a7eca7633662767ecf177f2dc52c206a90a4c1c4fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsBucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsDirPrefixName")
    def obs_dir_prefix_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsDirPrefixName"))

    @obs_dir_prefix_name.setter
    def obs_dir_prefix_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb65fdf6ae1cf252af54863926e53fee83038e297df9916c17642dad9f6fd596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsDirPrefixName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsEncryptedEnable")
    def obs_encrypted_enable(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "obsEncryptedEnable"))

    @obs_encrypted_enable.setter
    def obs_encrypted_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0f37870558c40a0890210e060a96b3794bf62d91240d5464241d350cfd51b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsEncryptedEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsEncryptedId")
    def obs_encrypted_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsEncryptedId"))

    @obs_encrypted_id.setter
    def obs_encrypted_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da63f12f474aa46ab72d1511ab44415f7de8792441c9948002bd2ca0033a703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsEncryptedId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsEpsId")
    def obs_eps_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsEpsId"))

    @obs_eps_id.setter
    def obs_eps_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f93f556d97509a0f33d74c55abf935f0749c96d22a44ff37c9c862cb71da86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsEpsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsPeriod")
    def obs_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "obsPeriod"))

    @obs_period.setter
    def obs_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48da712c38493cada5c5b2615dc2be1e81a0dd89e21587c615404e7f9a4fdb0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsPeriodUnit")
    def obs_period_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsPeriodUnit"))

    @obs_period_unit.setter
    def obs_period_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e5ecf9863cd8007753b57de14865bbfb643f52027c454505296c70f4ecd8f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsPeriodUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsPrefixName")
    def obs_prefix_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsPrefixName"))

    @obs_prefix_name.setter
    def obs_prefix_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a609b33ac7d6b08fe89fb63c796f3c1ac09f702bda1e4e959383bf4e06c89123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsPrefixName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsTimeZone")
    def obs_time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsTimeZone"))

    @obs_time_zone.setter
    def obs_time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ee7061da846f6252a281263abc506b3f9e5cd49dadf8375a5eb75dd9686c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsTimeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsTimeZoneId")
    def obs_time_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsTimeZoneId"))

    @obs_time_zone_id.setter
    def obs_time_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29b1eeac613056a8d9520dd746da23088e762db40f080707e51b7a966a159e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsTimeZoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsTransferPath")
    def obs_transfer_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsTransferPath"))

    @obs_transfer_path.setter
    def obs_transfer_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e304fd2823270347262755f61fad064f6c4f5c47b9ab7aaff948610ed7c6652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsTransferPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112092f68619c7ba79e57e5c67f2c8c0f1cd5906d58206e3bb3634e6d7fa54f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LtsTransferV2LogTransferInfoLogTransferDetail]:
        return typing.cast(typing.Optional[LtsTransferV2LogTransferInfoLogTransferDetail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsTransferV2LogTransferInfoLogTransferDetail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7390b93baf2bb46d93369aaa658ee41f4ce43e3914f03c08860ecdab37defd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LtsTransferV2LogTransferInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsTransferV2.LtsTransferV2LogTransferInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5ca79bbbc56491f5a039b5eded73b957573c313d9fa2627e0772836b676d63e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLogAgencyTransfer")
    def put_log_agency_transfer(
        self,
        *,
        agency_domain_id: builtins.str,
        agency_domain_name: builtins.str,
        agency_name: builtins.str,
        agency_project_id: builtins.str,
    ) -> None:
        '''
        :param agency_domain_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_domain_id LtsTransferV2#agency_domain_id}.
        :param agency_domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_domain_name LtsTransferV2#agency_domain_name}.
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_name LtsTransferV2#agency_name}.
        :param agency_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#agency_project_id LtsTransferV2#agency_project_id}.
        '''
        value = LtsTransferV2LogTransferInfoLogAgencyTransfer(
            agency_domain_id=agency_domain_id,
            agency_domain_name=agency_domain_name,
            agency_name=agency_name,
            agency_project_id=agency_project_id,
        )

        return typing.cast(None, jsii.invoke(self, "putLogAgencyTransfer", [value]))

    @jsii.member(jsii_name="putLogTransferDetail")
    def put_log_transfer_detail(
        self,
        *,
        obs_bucket_name: typing.Optional[builtins.str] = None,
        obs_dir_prefix_name: typing.Optional[builtins.str] = None,
        obs_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        obs_encrypted_id: typing.Optional[builtins.str] = None,
        obs_eps_id: typing.Optional[builtins.str] = None,
        obs_period: typing.Optional[jsii.Number] = None,
        obs_period_unit: typing.Optional[builtins.str] = None,
        obs_prefix_name: typing.Optional[builtins.str] = None,
        obs_time_zone: typing.Optional[builtins.str] = None,
        obs_time_zone_id: typing.Optional[builtins.str] = None,
        obs_transfer_path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param obs_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_bucket_name LtsTransferV2#obs_bucket_name}.
        :param obs_dir_prefix_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_dir_prefix_name LtsTransferV2#obs_dir_prefix_name}.
        :param obs_encrypted_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_encrypted_enable LtsTransferV2#obs_encrypted_enable}.
        :param obs_encrypted_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_encrypted_id LtsTransferV2#obs_encrypted_id}.
        :param obs_eps_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_eps_id LtsTransferV2#obs_eps_id}.
        :param obs_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_period LtsTransferV2#obs_period}.
        :param obs_period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_period_unit LtsTransferV2#obs_period_unit}.
        :param obs_prefix_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_prefix_name LtsTransferV2#obs_prefix_name}.
        :param obs_time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_time_zone LtsTransferV2#obs_time_zone}.
        :param obs_time_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_time_zone_id LtsTransferV2#obs_time_zone_id}.
        :param obs_transfer_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#obs_transfer_path LtsTransferV2#obs_transfer_path}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_transfer_v2#tags LtsTransferV2#tags}.
        '''
        value = LtsTransferV2LogTransferInfoLogTransferDetail(
            obs_bucket_name=obs_bucket_name,
            obs_dir_prefix_name=obs_dir_prefix_name,
            obs_encrypted_enable=obs_encrypted_enable,
            obs_encrypted_id=obs_encrypted_id,
            obs_eps_id=obs_eps_id,
            obs_period=obs_period,
            obs_period_unit=obs_period_unit,
            obs_prefix_name=obs_prefix_name,
            obs_time_zone=obs_time_zone,
            obs_time_zone_id=obs_time_zone_id,
            obs_transfer_path=obs_transfer_path,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "putLogTransferDetail", [value]))

    @jsii.member(jsii_name="resetLogAgencyTransfer")
    def reset_log_agency_transfer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAgencyTransfer", []))

    @builtins.property
    @jsii.member(jsii_name="logAgencyTransfer")
    def log_agency_transfer(
        self,
    ) -> LtsTransferV2LogTransferInfoLogAgencyTransferOutputReference:
        return typing.cast(LtsTransferV2LogTransferInfoLogAgencyTransferOutputReference, jsii.get(self, "logAgencyTransfer"))

    @builtins.property
    @jsii.member(jsii_name="logCreatedAt")
    def log_created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="logTransferDetail")
    def log_transfer_detail(
        self,
    ) -> LtsTransferV2LogTransferInfoLogTransferDetailOutputReference:
        return typing.cast(LtsTransferV2LogTransferInfoLogTransferDetailOutputReference, jsii.get(self, "logTransferDetail"))

    @builtins.property
    @jsii.member(jsii_name="logAgencyTransferInput")
    def log_agency_transfer_input(
        self,
    ) -> typing.Optional[LtsTransferV2LogTransferInfoLogAgencyTransfer]:
        return typing.cast(typing.Optional[LtsTransferV2LogTransferInfoLogAgencyTransfer], jsii.get(self, "logAgencyTransferInput"))

    @builtins.property
    @jsii.member(jsii_name="logStorageFormatInput")
    def log_storage_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStorageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="logTransferDetailInput")
    def log_transfer_detail_input(
        self,
    ) -> typing.Optional[LtsTransferV2LogTransferInfoLogTransferDetail]:
        return typing.cast(typing.Optional[LtsTransferV2LogTransferInfoLogTransferDetail], jsii.get(self, "logTransferDetailInput"))

    @builtins.property
    @jsii.member(jsii_name="logTransferModeInput")
    def log_transfer_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logTransferModeInput"))

    @builtins.property
    @jsii.member(jsii_name="logTransferStatusInput")
    def log_transfer_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logTransferStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="logTransferTypeInput")
    def log_transfer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logTransferTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="logStorageFormat")
    def log_storage_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStorageFormat"))

    @log_storage_format.setter
    def log_storage_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973d70b0dd86d85ef3abb4605ab0af6f5411c7dc9789a873381441bca81b88d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStorageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logTransferMode")
    def log_transfer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logTransferMode"))

    @log_transfer_mode.setter
    def log_transfer_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eddae6c9bea0c4b6e6f450b7fe46e131ca0bd7536db562f8b58d699555479ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logTransferMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logTransferStatus")
    def log_transfer_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logTransferStatus"))

    @log_transfer_status.setter
    def log_transfer_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df1baab8a9a4cafc40db8be615f67b4b9248f78ae2431621f47b60e7c998c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logTransferStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logTransferType")
    def log_transfer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logTransferType"))

    @log_transfer_type.setter
    def log_transfer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd26d156d742c016cf10404ef329b9436fa22cbd13d65c4d9259b79970548af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logTransferType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LtsTransferV2LogTransferInfo]:
        return typing.cast(typing.Optional[LtsTransferV2LogTransferInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsTransferV2LogTransferInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3e5c41318738c29c4bdb7ad7d8438f8cbefc6c0e719cc3dd5a40ac26e9d766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LtsTransferV2",
    "LtsTransferV2Config",
    "LtsTransferV2LogStreams",
    "LtsTransferV2LogStreamsList",
    "LtsTransferV2LogStreamsOutputReference",
    "LtsTransferV2LogTransferInfo",
    "LtsTransferV2LogTransferInfoLogAgencyTransfer",
    "LtsTransferV2LogTransferInfoLogAgencyTransferOutputReference",
    "LtsTransferV2LogTransferInfoLogTransferDetail",
    "LtsTransferV2LogTransferInfoLogTransferDetailOutputReference",
    "LtsTransferV2LogTransferInfoOutputReference",
]

publication.publish()

def _typecheckingstub__efee44badb84184a22a03f208850a89b6e8633e950d6a866937a64f7b1a93693(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    log_group_id: builtins.str,
    log_streams: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LtsTransferV2LogStreams, typing.Dict[builtins.str, typing.Any]]]],
    log_transfer_info: typing.Union[LtsTransferV2LogTransferInfo, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__01603daa08e99a11dac5b424980ccb14c2af2ec3ff8cd7eccf2346986cccf95a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea09126ac0c709d2efdd223f499e51a4eca68eecb715398d3c0dd31a578aa810(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LtsTransferV2LogStreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695b9f3d9ca0dbae195df7f78d1e3642258411c86a8915188620ecf661566c17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b4731a3028379abdc748701707f20cd235b8c83b8019452ece8c859fb7553b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1a669818c79a57df0a6acb54a61b8349e2956d277e007f5060eca29baef4d6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_group_id: builtins.str,
    log_streams: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LtsTransferV2LogStreams, typing.Dict[builtins.str, typing.Any]]]],
    log_transfer_info: typing.Union[LtsTransferV2LogTransferInfo, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447844dff92f2b05259a9ec3edde7cc46efffc6a166861b213df8d33ad881a45(
    *,
    log_stream_id: builtins.str,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5f0303dfcaa48b657a6fb61e4615d66655b49a138c8d57cfe6d4a8daaead24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9445b6f3627a150de8ccd3c8a0fd409bc4aaa659c980fdbdedeae3bd235e4514(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1716463575cb30f870c7e1323c1e974365168e907ea09eb024cd7b6db6faa10e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004924bd0e8c536f02a9cbe9b5bc53e9d18d34ba6d8c856ee798fc6d6faf7c6f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0ccc6c85bd2ced540feb7c35dfd7798bc310ed187083ec38f8877000b7b136(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd79040cc2597efe4e05f6c393af639e18e357d591cec819bcca077e39a9b60b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsTransferV2LogStreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2a8b4b79e8930c34ff76627c318166c922e947755dd41defcb0536303c5b0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09aa6651d8c84b4a37c5a8c42730c6e4e850e891564695cf7188b0879a6c8fb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea91ec7c9f0c6e768528c87b3c0d374dad5a5fc3fcaca00cb0f6290951de8b67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611979d54098872c57a7c976eff3023c0f817b2367f9a404e0a1a07a8b324787(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsTransferV2LogStreams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982899c585f85e61cfcb1048897f72761898d9cb3d6e6c87fcab800c759f4286(
    *,
    log_storage_format: builtins.str,
    log_transfer_detail: typing.Union[LtsTransferV2LogTransferInfoLogTransferDetail, typing.Dict[builtins.str, typing.Any]],
    log_transfer_mode: builtins.str,
    log_transfer_status: builtins.str,
    log_transfer_type: builtins.str,
    log_agency_transfer: typing.Optional[typing.Union[LtsTransferV2LogTransferInfoLogAgencyTransfer, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18841c1f00e8e130c0bc1ba872983b8cfce45fcb31a709ec0c7512a88c93b9dd(
    *,
    agency_domain_id: builtins.str,
    agency_domain_name: builtins.str,
    agency_name: builtins.str,
    agency_project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e6bd4afab6a436d868a72f7807264983608e69b497a9fbef78dd55883173ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0fe20ca770b01eb7c49e19e7578b9ff065d892c0d9f14a462a13d0ec9ceb4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d483ff034c76257f902c3d24d96389ba0147e4e75119742ec9321640ab0ab4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3b9ebddaa7270bcafec6f986243af066b7fd965506881b08af23a47b8108a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185fd44843ae5b6aa55f6f4177574261293851a72f2e9be7a55a211b0e02cf62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bfec65db02b2c6e300a338dd8748fcc98c55c5d410cd68c534bb064f6d9e50(
    value: typing.Optional[LtsTransferV2LogTransferInfoLogAgencyTransfer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ba40ea411194e00a5727c27d5eac768afb2d35a4df05d44d572050d555f77a(
    *,
    obs_bucket_name: typing.Optional[builtins.str] = None,
    obs_dir_prefix_name: typing.Optional[builtins.str] = None,
    obs_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    obs_encrypted_id: typing.Optional[builtins.str] = None,
    obs_eps_id: typing.Optional[builtins.str] = None,
    obs_period: typing.Optional[jsii.Number] = None,
    obs_period_unit: typing.Optional[builtins.str] = None,
    obs_prefix_name: typing.Optional[builtins.str] = None,
    obs_time_zone: typing.Optional[builtins.str] = None,
    obs_time_zone_id: typing.Optional[builtins.str] = None,
    obs_transfer_path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aebccb4bed376e750e72cd504b5c942d9df8c897a171e94f903a91a3f339825(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b83b3eb5283e031039b07a7eca7633662767ecf177f2dc52c206a90a4c1c4fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb65fdf6ae1cf252af54863926e53fee83038e297df9916c17642dad9f6fd596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0f37870558c40a0890210e060a96b3794bf62d91240d5464241d350cfd51b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da63f12f474aa46ab72d1511ab44415f7de8792441c9948002bd2ca0033a703(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f93f556d97509a0f33d74c55abf935f0749c96d22a44ff37c9c862cb71da86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48da712c38493cada5c5b2615dc2be1e81a0dd89e21587c615404e7f9a4fdb0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5ecf9863cd8007753b57de14865bbfb643f52027c454505296c70f4ecd8f83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a609b33ac7d6b08fe89fb63c796f3c1ac09f702bda1e4e959383bf4e06c89123(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ee7061da846f6252a281263abc506b3f9e5cd49dadf8375a5eb75dd9686c5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29b1eeac613056a8d9520dd746da23088e762db40f080707e51b7a966a159e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e304fd2823270347262755f61fad064f6c4f5c47b9ab7aaff948610ed7c6652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112092f68619c7ba79e57e5c67f2c8c0f1cd5906d58206e3bb3634e6d7fa54f5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7390b93baf2bb46d93369aaa658ee41f4ce43e3914f03c08860ecdab37defd2(
    value: typing.Optional[LtsTransferV2LogTransferInfoLogTransferDetail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ca79bbbc56491f5a039b5eded73b957573c313d9fa2627e0772836b676d63e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973d70b0dd86d85ef3abb4605ab0af6f5411c7dc9789a873381441bca81b88d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eddae6c9bea0c4b6e6f450b7fe46e131ca0bd7536db562f8b58d699555479ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df1baab8a9a4cafc40db8be615f67b4b9248f78ae2431621f47b60e7c998c2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd26d156d742c016cf10404ef329b9436fa22cbd13d65c4d9259b79970548af4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3e5c41318738c29c4bdb7ad7d8438f8cbefc6c0e719cc3dd5a40ac26e9d766(
    value: typing.Optional[LtsTransferV2LogTransferInfo],
) -> None:
    """Type checking stubs"""
    pass
