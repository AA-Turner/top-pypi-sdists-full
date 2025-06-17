r'''
# `pagerduty_slack_connection`

Refer to the Terraform Registry for docs: [`pagerduty_slack_connection`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection).
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


class SlackConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.slackConnection.SlackConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection pagerduty_slack_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        channel_id: builtins.str,
        config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SlackConnectionConfigA", typing.Dict[builtins.str, typing.Any]]]],
        notification_type: builtins.str,
        source_id: builtins.str,
        source_type: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection pagerduty_slack_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param channel_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#channel_id SlackConnection#channel_id}.
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#config SlackConnection#config}
        :param notification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#notification_type SlackConnection#notification_type}.
        :param source_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#source_id SlackConnection#source_id}.
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#source_type SlackConnection#source_type}.
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#workspace_id SlackConnection#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#id SlackConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10944c822918bb02bc8c0da6a66b4090ef3af6a2c707640a6da2b9bcb9271f92)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = SlackConnectionConfig(
            channel_id=channel_id,
            config=config,
            notification_type=notification_type,
            source_id=source_id,
            source_type=source_type,
            workspace_id=workspace_id,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a SlackConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SlackConnection to import.
        :param import_from_id: The id of the existing SlackConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SlackConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8409ad0293f20131c08f698e59dc8f6e0f49063492094b784055d356fbfa1215)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SlackConnectionConfigA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44dceeccb0b7aa0407652f8b36e63d09b1f3fea4825107c02a50fb4680099d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

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
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelName"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "SlackConnectionConfigAList":
        return typing.cast("SlackConnectionConfigAList", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="sourceName")
    def source_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceName"))

    @builtins.property
    @jsii.member(jsii_name="channelIdInput")
    def channel_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SlackConnectionConfigA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SlackConnectionConfigA"]]], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationTypeInput")
    def notification_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIdInput")
    def source_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="channelId")
    def channel_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelId"))

    @channel_id.setter
    def channel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6a6313115d881719390681e8f213f8620bc193cc8d55251aead00e9157e01c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77afb0d3c64e5166ace3c7ba8ba0594c6d5121c664b0f4e42cad9397cb703486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationType")
    def notification_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationType"))

    @notification_type.setter
    def notification_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e6cd21b33e50cb3c82c2d7f5c5d4a648708cc6fe250f9666c1725be703c0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceId")
    def source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceId"))

    @source_id.setter
    def source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe289b221c5e8f4c805092bb1df7c7f21454e4ba2e403b3d15131d737212df08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b4c7f3cf1b21aafaf75d988ee15dbb2ce93614d09e9c6bd4f5bcded90c205f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352ee1300064f6d33c35ec5b45b8e92f9e3cff0b5a22fb539e7557abbb98a21e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.slackConnection.SlackConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "channel_id": "channelId",
        "config": "config",
        "notification_type": "notificationType",
        "source_id": "sourceId",
        "source_type": "sourceType",
        "workspace_id": "workspaceId",
        "id": "id",
    },
)
class SlackConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        channel_id: builtins.str,
        config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SlackConnectionConfigA", typing.Dict[builtins.str, typing.Any]]]],
        notification_type: builtins.str,
        source_id: builtins.str,
        source_type: builtins.str,
        workspace_id: builtins.str,
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
        :param channel_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#channel_id SlackConnection#channel_id}.
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#config SlackConnection#config}
        :param notification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#notification_type SlackConnection#notification_type}.
        :param source_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#source_id SlackConnection#source_id}.
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#source_type SlackConnection#source_type}.
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#workspace_id SlackConnection#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#id SlackConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e31a3c0900f363f44173bced37bbe7917a5bb9513f39f8c092aa29c28190255)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument notification_type", value=notification_type, expected_type=type_hints["notification_type"])
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_id": channel_id,
            "config": config,
            "notification_type": notification_type,
            "source_id": source_id,
            "source_type": source_type,
            "workspace_id": workspace_id,
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
    def channel_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#channel_id SlackConnection#channel_id}.'''
        result = self._values.get("channel_id")
        assert result is not None, "Required property 'channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SlackConnectionConfigA"]]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#config SlackConnection#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SlackConnectionConfigA"]], result)

    @builtins.property
    def notification_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#notification_type SlackConnection#notification_type}.'''
        result = self._values.get("notification_type")
        assert result is not None, "Required property 'notification_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#source_id SlackConnection#source_id}.'''
        result = self._values.get("source_id")
        assert result is not None, "Required property 'source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#source_type SlackConnection#source_type}.'''
        result = self._values.get("source_type")
        assert result is not None, "Required property 'source_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#workspace_id SlackConnection#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#id SlackConnection#id}.

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
        return "SlackConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.slackConnection.SlackConnectionConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "events": "events",
        "priorities": "priorities",
        "urgency": "urgency",
    },
)
class SlackConnectionConfigA:
    def __init__(
        self,
        *,
        events: typing.Sequence[builtins.str],
        priorities: typing.Optional[typing.Sequence[builtins.str]] = None,
        urgency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#events SlackConnection#events}.
        :param priorities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#priorities SlackConnection#priorities}.
        :param urgency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#urgency SlackConnection#urgency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da15be02e1e09e6a62d11b5322e481cbba374710c29dc9bd7ea2231db26d7de)
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument priorities", value=priorities, expected_type=type_hints["priorities"])
            check_type(argname="argument urgency", value=urgency, expected_type=type_hints["urgency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "events": events,
        }
        if priorities is not None:
            self._values["priorities"] = priorities
        if urgency is not None:
            self._values["urgency"] = urgency

    @builtins.property
    def events(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#events SlackConnection#events}.'''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def priorities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#priorities SlackConnection#priorities}.'''
        result = self._values.get("priorities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def urgency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/slack_connection#urgency SlackConnection#urgency}.'''
        result = self._values.get("urgency")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackConnectionConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SlackConnectionConfigAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.slackConnection.SlackConnectionConfigAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3a96107156a14134a3a6e3faab7b32320b4f54e7f4b1056bea46c3229d99f6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SlackConnectionConfigAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f928ff75630221e2739aecc4a278c929ef72048b7a5e476b71e6e9416b3a5871)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SlackConnectionConfigAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3899d6a1fb19a4f9c101f823dd96b866623217dbcf9dca8cee66187113c4e162)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f34665f24cb872671428f3dd5fd1b13e148538b509ac2b2e5ed752ba63e9b84c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee00ac25d2a0ebc9efdd12ea95a2db3228fac8fefe8ef28fcb67d6d4bcf5d440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SlackConnectionConfigA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SlackConnectionConfigA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SlackConnectionConfigA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df66ea48ddfa92b721808a0624fc4b7550a2d037314dd00570479378efe0fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SlackConnectionConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.slackConnection.SlackConnectionConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf174b9cc1c535bc26706931fe119747ac5df3a88427046b63e2160e7e547c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPriorities")
    def reset_priorities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriorities", []))

    @jsii.member(jsii_name="resetUrgency")
    def reset_urgency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrgency", []))

    @builtins.property
    @jsii.member(jsii_name="eventsInput")
    def events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventsInput"))

    @builtins.property
    @jsii.member(jsii_name="prioritiesInput")
    def priorities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "prioritiesInput"))

    @builtins.property
    @jsii.member(jsii_name="urgencyInput")
    def urgency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urgencyInput"))

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "events"))

    @events.setter
    def events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fad61f72a04e2e48c845934dbacace58bd5d3590ea242382d8767938cf07e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priorities")
    def priorities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "priorities"))

    @priorities.setter
    def priorities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb8f2d70fc8a638131bf2b138e8e18c83179a188edb131195dadaa25b04460b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priorities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urgency")
    def urgency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urgency"))

    @urgency.setter
    def urgency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b837b33de769e033786ff4428f442442995948bb82cca0ec91f0cf991f4c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urgency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SlackConnectionConfigA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SlackConnectionConfigA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SlackConnectionConfigA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6014cbdd0bdcd971bcf83dd513a54f9574f18626d857fa867eb108f1f81ef1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SlackConnection",
    "SlackConnectionConfig",
    "SlackConnectionConfigA",
    "SlackConnectionConfigAList",
    "SlackConnectionConfigAOutputReference",
]

publication.publish()

def _typecheckingstub__10944c822918bb02bc8c0da6a66b4090ef3af6a2c707640a6da2b9bcb9271f92(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    channel_id: builtins.str,
    config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SlackConnectionConfigA, typing.Dict[builtins.str, typing.Any]]]],
    notification_type: builtins.str,
    source_id: builtins.str,
    source_type: builtins.str,
    workspace_id: builtins.str,
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

def _typecheckingstub__8409ad0293f20131c08f698e59dc8f6e0f49063492094b784055d356fbfa1215(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44dceeccb0b7aa0407652f8b36e63d09b1f3fea4825107c02a50fb4680099d76(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SlackConnectionConfigA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6a6313115d881719390681e8f213f8620bc193cc8d55251aead00e9157e01c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77afb0d3c64e5166ace3c7ba8ba0594c6d5121c664b0f4e42cad9397cb703486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e6cd21b33e50cb3c82c2d7f5c5d4a648708cc6fe250f9666c1725be703c0c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe289b221c5e8f4c805092bb1df7c7f21454e4ba2e403b3d15131d737212df08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b4c7f3cf1b21aafaf75d988ee15dbb2ce93614d09e9c6bd4f5bcded90c205f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352ee1300064f6d33c35ec5b45b8e92f9e3cff0b5a22fb539e7557abbb98a21e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e31a3c0900f363f44173bced37bbe7917a5bb9513f39f8c092aa29c28190255(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    channel_id: builtins.str,
    config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SlackConnectionConfigA, typing.Dict[builtins.str, typing.Any]]]],
    notification_type: builtins.str,
    source_id: builtins.str,
    source_type: builtins.str,
    workspace_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da15be02e1e09e6a62d11b5322e481cbba374710c29dc9bd7ea2231db26d7de(
    *,
    events: typing.Sequence[builtins.str],
    priorities: typing.Optional[typing.Sequence[builtins.str]] = None,
    urgency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a96107156a14134a3a6e3faab7b32320b4f54e7f4b1056bea46c3229d99f6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f928ff75630221e2739aecc4a278c929ef72048b7a5e476b71e6e9416b3a5871(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3899d6a1fb19a4f9c101f823dd96b866623217dbcf9dca8cee66187113c4e162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34665f24cb872671428f3dd5fd1b13e148538b509ac2b2e5ed752ba63e9b84c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee00ac25d2a0ebc9efdd12ea95a2db3228fac8fefe8ef28fcb67d6d4bcf5d440(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df66ea48ddfa92b721808a0624fc4b7550a2d037314dd00570479378efe0fb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SlackConnectionConfigA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf174b9cc1c535bc26706931fe119747ac5df3a88427046b63e2160e7e547c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fad61f72a04e2e48c845934dbacace58bd5d3590ea242382d8767938cf07e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb8f2d70fc8a638131bf2b138e8e18c83179a188edb131195dadaa25b04460b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b837b33de769e033786ff4428f442442995948bb82cca0ec91f0cf991f4c30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6014cbdd0bdcd971bcf83dd513a54f9574f18626d857fa867eb108f1f81ef1aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SlackConnectionConfigA]],
) -> None:
    """Type checking stubs"""
    pass
