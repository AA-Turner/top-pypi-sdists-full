r'''
# `azurerm_stream_analytics_stream_input_blob`

Refer to the Terraform Registry for docs: [`azurerm_stream_analytics_stream_input_blob`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob).
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


class StreamAnalyticsStreamInputBlob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.streamAnalyticsStreamInputBlob.StreamAnalyticsStreamInputBlob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob azurerm_stream_analytics_stream_input_blob}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        date_format: builtins.str,
        name: builtins.str,
        path_pattern: builtins.str,
        resource_group_name: builtins.str,
        serialization: typing.Union["StreamAnalyticsStreamInputBlobSerialization", typing.Dict[builtins.str, typing.Any]],
        storage_account_key: builtins.str,
        storage_account_name: builtins.str,
        storage_container_name: builtins.str,
        stream_analytics_job_name: builtins.str,
        time_format: builtins.str,
        authentication_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StreamAnalyticsStreamInputBlobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob azurerm_stream_analytics_stream_input_blob} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param date_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#date_format StreamAnalyticsStreamInputBlob#date_format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#name StreamAnalyticsStreamInputBlob#name}.
        :param path_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#path_pattern StreamAnalyticsStreamInputBlob#path_pattern}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#resource_group_name StreamAnalyticsStreamInputBlob#resource_group_name}.
        :param serialization: serialization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#serialization StreamAnalyticsStreamInputBlob#serialization}
        :param storage_account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#storage_account_key StreamAnalyticsStreamInputBlob#storage_account_key}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#storage_account_name StreamAnalyticsStreamInputBlob#storage_account_name}.
        :param storage_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#storage_container_name StreamAnalyticsStreamInputBlob#storage_container_name}.
        :param stream_analytics_job_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#stream_analytics_job_name StreamAnalyticsStreamInputBlob#stream_analytics_job_name}.
        :param time_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#time_format StreamAnalyticsStreamInputBlob#time_format}.
        :param authentication_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#authentication_mode StreamAnalyticsStreamInputBlob#authentication_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#id StreamAnalyticsStreamInputBlob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#timeouts StreamAnalyticsStreamInputBlob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a7ea332991cb27c19c10287588e05bd6894ca7c81aefe2fb27e6a2aafdd970)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StreamAnalyticsStreamInputBlobConfig(
            date_format=date_format,
            name=name,
            path_pattern=path_pattern,
            resource_group_name=resource_group_name,
            serialization=serialization,
            storage_account_key=storage_account_key,
            storage_account_name=storage_account_name,
            storage_container_name=storage_container_name,
            stream_analytics_job_name=stream_analytics_job_name,
            time_format=time_format,
            authentication_mode=authentication_mode,
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
        '''Generates CDKTF code for importing a StreamAnalyticsStreamInputBlob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StreamAnalyticsStreamInputBlob to import.
        :param import_from_id: The id of the existing StreamAnalyticsStreamInputBlob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StreamAnalyticsStreamInputBlob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8dd0cbf18f98d625aefb153bf36dd789261884aa7a809f8e426c56c38c55e51)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSerialization")
    def put_serialization(
        self,
        *,
        type: builtins.str,
        encoding: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#type StreamAnalyticsStreamInputBlob#type}.
        :param encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#encoding StreamAnalyticsStreamInputBlob#encoding}.
        :param field_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#field_delimiter StreamAnalyticsStreamInputBlob#field_delimiter}.
        '''
        value = StreamAnalyticsStreamInputBlobSerialization(
            type=type, encoding=encoding, field_delimiter=field_delimiter
        )

        return typing.cast(None, jsii.invoke(self, "putSerialization", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#create StreamAnalyticsStreamInputBlob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#delete StreamAnalyticsStreamInputBlob#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#read StreamAnalyticsStreamInputBlob#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#update StreamAnalyticsStreamInputBlob#update}.
        '''
        value = StreamAnalyticsStreamInputBlobTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthenticationMode")
    def reset_authentication_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationMode", []))

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
    @jsii.member(jsii_name="serialization")
    def serialization(
        self,
    ) -> "StreamAnalyticsStreamInputBlobSerializationOutputReference":
        return typing.cast("StreamAnalyticsStreamInputBlobSerializationOutputReference", jsii.get(self, "serialization"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "StreamAnalyticsStreamInputBlobTimeoutsOutputReference":
        return typing.cast("StreamAnalyticsStreamInputBlobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="authenticationModeInput")
    def authentication_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="dateFormatInput")
    def date_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathPatternInput")
    def path_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serializationInput")
    def serialization_input(
        self,
    ) -> typing.Optional["StreamAnalyticsStreamInputBlobSerialization"]:
        return typing.cast(typing.Optional["StreamAnalyticsStreamInputBlobSerialization"], jsii.get(self, "serializationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountKeyInput")
    def storage_account_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountNameInput")
    def storage_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageContainerNameInput")
    def storage_container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageContainerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamAnalyticsJobNameInput")
    def stream_analytics_job_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamAnalyticsJobNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFormatInput")
    def time_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StreamAnalyticsStreamInputBlobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StreamAnalyticsStreamInputBlobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMode")
    def authentication_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationMode"))

    @authentication_mode.setter
    def authentication_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2701534f7cd5668ac3efc48d67962a6f3850073c2631f5a9f254b471046343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateFormat")
    def date_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateFormat"))

    @date_format.setter
    def date_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e9a122c202324334830d16f81cd29ab5328fb750689a1a8baf7b907354388a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f36de12d9cca0b1ca7a501e621f10f4670a8f1675533004427237ab9db027f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536eeb51646083e15d4cab3d8582ca1072cf2a03859de12f266182e1a410a50f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathPattern")
    def path_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathPattern"))

    @path_pattern.setter
    def path_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5446827e98a99e94c298418c7cb924cc1a7fbded3735012c18210b451879f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21bbf0a1de54a7a55821934a75b8289f475ebaa3327b34614e462aef9c3a7df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountKey")
    def storage_account_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountKey"))

    @storage_account_key.setter
    def storage_account_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88306b1121481fad8575c24ee86d6ef9fe6d632a729bb3e3bdde86ac7576bc05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountName")
    def storage_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountName"))

    @storage_account_name.setter
    def storage_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e266fee2abafd2b42c2871097b77fd4be2ecf0a0596d247ee52f05c85a997a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainerName")
    def storage_container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainerName"))

    @storage_container_name.setter
    def storage_container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106bfb9ad22102c6fbf3855b415b8eb5de8b35b321dea6c3f2d1b9583f67d21c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamAnalyticsJobName")
    def stream_analytics_job_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamAnalyticsJobName"))

    @stream_analytics_job_name.setter
    def stream_analytics_job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2babcd85129c204168fff7518f73886b2686c5f72135945d4bcebf46c6bcf31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamAnalyticsJobName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeFormat")
    def time_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeFormat"))

    @time_format.setter
    def time_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f261ebf29161ef6d48493f738d179c73fa951f8543bb9407e92570fd9e33d436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeFormat", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.streamAnalyticsStreamInputBlob.StreamAnalyticsStreamInputBlobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "date_format": "dateFormat",
        "name": "name",
        "path_pattern": "pathPattern",
        "resource_group_name": "resourceGroupName",
        "serialization": "serialization",
        "storage_account_key": "storageAccountKey",
        "storage_account_name": "storageAccountName",
        "storage_container_name": "storageContainerName",
        "stream_analytics_job_name": "streamAnalyticsJobName",
        "time_format": "timeFormat",
        "authentication_mode": "authenticationMode",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class StreamAnalyticsStreamInputBlobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        date_format: builtins.str,
        name: builtins.str,
        path_pattern: builtins.str,
        resource_group_name: builtins.str,
        serialization: typing.Union["StreamAnalyticsStreamInputBlobSerialization", typing.Dict[builtins.str, typing.Any]],
        storage_account_key: builtins.str,
        storage_account_name: builtins.str,
        storage_container_name: builtins.str,
        stream_analytics_job_name: builtins.str,
        time_format: builtins.str,
        authentication_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StreamAnalyticsStreamInputBlobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param date_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#date_format StreamAnalyticsStreamInputBlob#date_format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#name StreamAnalyticsStreamInputBlob#name}.
        :param path_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#path_pattern StreamAnalyticsStreamInputBlob#path_pattern}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#resource_group_name StreamAnalyticsStreamInputBlob#resource_group_name}.
        :param serialization: serialization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#serialization StreamAnalyticsStreamInputBlob#serialization}
        :param storage_account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#storage_account_key StreamAnalyticsStreamInputBlob#storage_account_key}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#storage_account_name StreamAnalyticsStreamInputBlob#storage_account_name}.
        :param storage_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#storage_container_name StreamAnalyticsStreamInputBlob#storage_container_name}.
        :param stream_analytics_job_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#stream_analytics_job_name StreamAnalyticsStreamInputBlob#stream_analytics_job_name}.
        :param time_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#time_format StreamAnalyticsStreamInputBlob#time_format}.
        :param authentication_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#authentication_mode StreamAnalyticsStreamInputBlob#authentication_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#id StreamAnalyticsStreamInputBlob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#timeouts StreamAnalyticsStreamInputBlob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(serialization, dict):
            serialization = StreamAnalyticsStreamInputBlobSerialization(**serialization)
        if isinstance(timeouts, dict):
            timeouts = StreamAnalyticsStreamInputBlobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c82b0764329f4e7e6f53d5f7532d53bc4a74805d8f17ba71a64aaf1e74a15c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument date_format", value=date_format, expected_type=type_hints["date_format"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path_pattern", value=path_pattern, expected_type=type_hints["path_pattern"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument serialization", value=serialization, expected_type=type_hints["serialization"])
            check_type(argname="argument storage_account_key", value=storage_account_key, expected_type=type_hints["storage_account_key"])
            check_type(argname="argument storage_account_name", value=storage_account_name, expected_type=type_hints["storage_account_name"])
            check_type(argname="argument storage_container_name", value=storage_container_name, expected_type=type_hints["storage_container_name"])
            check_type(argname="argument stream_analytics_job_name", value=stream_analytics_job_name, expected_type=type_hints["stream_analytics_job_name"])
            check_type(argname="argument time_format", value=time_format, expected_type=type_hints["time_format"])
            check_type(argname="argument authentication_mode", value=authentication_mode, expected_type=type_hints["authentication_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "date_format": date_format,
            "name": name,
            "path_pattern": path_pattern,
            "resource_group_name": resource_group_name,
            "serialization": serialization,
            "storage_account_key": storage_account_key,
            "storage_account_name": storage_account_name,
            "storage_container_name": storage_container_name,
            "stream_analytics_job_name": stream_analytics_job_name,
            "time_format": time_format,
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
        if authentication_mode is not None:
            self._values["authentication_mode"] = authentication_mode
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
    def date_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#date_format StreamAnalyticsStreamInputBlob#date_format}.'''
        result = self._values.get("date_format")
        assert result is not None, "Required property 'date_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#name StreamAnalyticsStreamInputBlob#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#path_pattern StreamAnalyticsStreamInputBlob#path_pattern}.'''
        result = self._values.get("path_pattern")
        assert result is not None, "Required property 'path_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#resource_group_name StreamAnalyticsStreamInputBlob#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def serialization(self) -> "StreamAnalyticsStreamInputBlobSerialization":
        '''serialization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#serialization StreamAnalyticsStreamInputBlob#serialization}
        '''
        result = self._values.get("serialization")
        assert result is not None, "Required property 'serialization' is missing"
        return typing.cast("StreamAnalyticsStreamInputBlobSerialization", result)

    @builtins.property
    def storage_account_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#storage_account_key StreamAnalyticsStreamInputBlob#storage_account_key}.'''
        result = self._values.get("storage_account_key")
        assert result is not None, "Required property 'storage_account_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#storage_account_name StreamAnalyticsStreamInputBlob#storage_account_name}.'''
        result = self._values.get("storage_account_name")
        assert result is not None, "Required property 'storage_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_container_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#storage_container_name StreamAnalyticsStreamInputBlob#storage_container_name}.'''
        result = self._values.get("storage_container_name")
        assert result is not None, "Required property 'storage_container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_analytics_job_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#stream_analytics_job_name StreamAnalyticsStreamInputBlob#stream_analytics_job_name}.'''
        result = self._values.get("stream_analytics_job_name")
        assert result is not None, "Required property 'stream_analytics_job_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#time_format StreamAnalyticsStreamInputBlob#time_format}.'''
        result = self._values.get("time_format")
        assert result is not None, "Required property 'time_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#authentication_mode StreamAnalyticsStreamInputBlob#authentication_mode}.'''
        result = self._values.get("authentication_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#id StreamAnalyticsStreamInputBlob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StreamAnalyticsStreamInputBlobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#timeouts StreamAnalyticsStreamInputBlob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StreamAnalyticsStreamInputBlobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamAnalyticsStreamInputBlobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.streamAnalyticsStreamInputBlob.StreamAnalyticsStreamInputBlobSerialization",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "encoding": "encoding",
        "field_delimiter": "fieldDelimiter",
    },
)
class StreamAnalyticsStreamInputBlobSerialization:
    def __init__(
        self,
        *,
        type: builtins.str,
        encoding: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#type StreamAnalyticsStreamInputBlob#type}.
        :param encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#encoding StreamAnalyticsStreamInputBlob#encoding}.
        :param field_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#field_delimiter StreamAnalyticsStreamInputBlob#field_delimiter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aecdd2a9669c3b297e844aa20329ab126c0e78823ff4dfba6e35d8ad159f0a8)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if encoding is not None:
            self._values["encoding"] = encoding
        if field_delimiter is not None:
            self._values["field_delimiter"] = field_delimiter

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#type StreamAnalyticsStreamInputBlob#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#encoding StreamAnalyticsStreamInputBlob#encoding}.'''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#field_delimiter StreamAnalyticsStreamInputBlob#field_delimiter}.'''
        result = self._values.get("field_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamAnalyticsStreamInputBlobSerialization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamAnalyticsStreamInputBlobSerializationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.streamAnalyticsStreamInputBlob.StreamAnalyticsStreamInputBlobSerializationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6990a6412e22075aae4b0f960480316a5e666efd4909628e29f262dbffd42ac9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetFieldDelimiter")
    def reset_field_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldDelimiter", []))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiterInput")
    def field_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec0beb1256856f5ebebd5c73499296f33cda9312d32aa3dc292e0123a97ca39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiter")
    def field_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldDelimiter"))

    @field_delimiter.setter
    def field_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8550d3150a053a6e00ba5fad0a27c2a67739731ce14f0ad68163240f32fce81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341b182b24a69cd46b502b5a22b79bc0a67519464f79701be00f9b65feb0dd91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StreamAnalyticsStreamInputBlobSerialization]:
        return typing.cast(typing.Optional[StreamAnalyticsStreamInputBlobSerialization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StreamAnalyticsStreamInputBlobSerialization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dded7dca460902549997aee1c9a357e2e51ccf737343930b19f0612e96e3634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.streamAnalyticsStreamInputBlob.StreamAnalyticsStreamInputBlobTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class StreamAnalyticsStreamInputBlobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#create StreamAnalyticsStreamInputBlob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#delete StreamAnalyticsStreamInputBlob#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#read StreamAnalyticsStreamInputBlob#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#update StreamAnalyticsStreamInputBlob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a742ccb65ae0610d45ef55dd30cbe637da2cf379660da4c660c564fd7974b382)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#create StreamAnalyticsStreamInputBlob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#delete StreamAnalyticsStreamInputBlob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#read StreamAnalyticsStreamInputBlob#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stream_analytics_stream_input_blob#update StreamAnalyticsStreamInputBlob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamAnalyticsStreamInputBlobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamAnalyticsStreamInputBlobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.streamAnalyticsStreamInputBlob.StreamAnalyticsStreamInputBlobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06f660690471f90e8696b80199bd1376c8e56fe828af541877582da9cd044738)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d7cea019d4b9bc180efa7b41d936747f866c3bd89b7c17130d151c699e8e6ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1128d6e358ee86c73231f3f65d00bf4c80f0ff4b84cbeeb83a98847981d31039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a376ba21af0da52f033e41fbfdddf10eb71d37d3e58a1a6c77e1086249fa88c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b613c2f47da0939afd618c646a1e7d28f3193325c05b6f0f92d39c12cf2619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StreamAnalyticsStreamInputBlobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StreamAnalyticsStreamInputBlobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StreamAnalyticsStreamInputBlobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421fd38cd5103d1d7232f62bf075d43f8e34e475d24bdefea06802e9ef8c9bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StreamAnalyticsStreamInputBlob",
    "StreamAnalyticsStreamInputBlobConfig",
    "StreamAnalyticsStreamInputBlobSerialization",
    "StreamAnalyticsStreamInputBlobSerializationOutputReference",
    "StreamAnalyticsStreamInputBlobTimeouts",
    "StreamAnalyticsStreamInputBlobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__96a7ea332991cb27c19c10287588e05bd6894ca7c81aefe2fb27e6a2aafdd970(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    date_format: builtins.str,
    name: builtins.str,
    path_pattern: builtins.str,
    resource_group_name: builtins.str,
    serialization: typing.Union[StreamAnalyticsStreamInputBlobSerialization, typing.Dict[builtins.str, typing.Any]],
    storage_account_key: builtins.str,
    storage_account_name: builtins.str,
    storage_container_name: builtins.str,
    stream_analytics_job_name: builtins.str,
    time_format: builtins.str,
    authentication_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StreamAnalyticsStreamInputBlobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a8dd0cbf18f98d625aefb153bf36dd789261884aa7a809f8e426c56c38c55e51(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2701534f7cd5668ac3efc48d67962a6f3850073c2631f5a9f254b471046343(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e9a122c202324334830d16f81cd29ab5328fb750689a1a8baf7b907354388a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f36de12d9cca0b1ca7a501e621f10f4670a8f1675533004427237ab9db027f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536eeb51646083e15d4cab3d8582ca1072cf2a03859de12f266182e1a410a50f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5446827e98a99e94c298418c7cb924cc1a7fbded3735012c18210b451879f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21bbf0a1de54a7a55821934a75b8289f475ebaa3327b34614e462aef9c3a7df5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88306b1121481fad8575c24ee86d6ef9fe6d632a729bb3e3bdde86ac7576bc05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e266fee2abafd2b42c2871097b77fd4be2ecf0a0596d247ee52f05c85a997a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106bfb9ad22102c6fbf3855b415b8eb5de8b35b321dea6c3f2d1b9583f67d21c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2babcd85129c204168fff7518f73886b2686c5f72135945d4bcebf46c6bcf31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f261ebf29161ef6d48493f738d179c73fa951f8543bb9407e92570fd9e33d436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c82b0764329f4e7e6f53d5f7532d53bc4a74805d8f17ba71a64aaf1e74a15c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    date_format: builtins.str,
    name: builtins.str,
    path_pattern: builtins.str,
    resource_group_name: builtins.str,
    serialization: typing.Union[StreamAnalyticsStreamInputBlobSerialization, typing.Dict[builtins.str, typing.Any]],
    storage_account_key: builtins.str,
    storage_account_name: builtins.str,
    storage_container_name: builtins.str,
    stream_analytics_job_name: builtins.str,
    time_format: builtins.str,
    authentication_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StreamAnalyticsStreamInputBlobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aecdd2a9669c3b297e844aa20329ab126c0e78823ff4dfba6e35d8ad159f0a8(
    *,
    type: builtins.str,
    encoding: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6990a6412e22075aae4b0f960480316a5e666efd4909628e29f262dbffd42ac9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec0beb1256856f5ebebd5c73499296f33cda9312d32aa3dc292e0123a97ca39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8550d3150a053a6e00ba5fad0a27c2a67739731ce14f0ad68163240f32fce81e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341b182b24a69cd46b502b5a22b79bc0a67519464f79701be00f9b65feb0dd91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dded7dca460902549997aee1c9a357e2e51ccf737343930b19f0612e96e3634(
    value: typing.Optional[StreamAnalyticsStreamInputBlobSerialization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a742ccb65ae0610d45ef55dd30cbe637da2cf379660da4c660c564fd7974b382(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f660690471f90e8696b80199bd1376c8e56fe828af541877582da9cd044738(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7cea019d4b9bc180efa7b41d936747f866c3bd89b7c17130d151c699e8e6ac1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1128d6e358ee86c73231f3f65d00bf4c80f0ff4b84cbeeb83a98847981d31039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a376ba21af0da52f033e41fbfdddf10eb71d37d3e58a1a6c77e1086249fa88c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b613c2f47da0939afd618c646a1e7d28f3193325c05b6f0f92d39c12cf2619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421fd38cd5103d1d7232f62bf075d43f8e34e475d24bdefea06802e9ef8c9bed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StreamAnalyticsStreamInputBlobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
