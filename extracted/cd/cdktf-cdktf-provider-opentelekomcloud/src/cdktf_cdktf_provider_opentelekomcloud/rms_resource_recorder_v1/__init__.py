r'''
# `opentelekomcloud_rms_resource_recorder_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_rms_resource_recorder_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1).
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


class RmsResourceRecorderV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rmsResourceRecorderV1.RmsResourceRecorderV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1 opentelekomcloud_rms_resource_recorder_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        agency_name: builtins.str,
        selector: typing.Union["RmsResourceRecorderV1Selector", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        obs_channel: typing.Optional[typing.Union["RmsResourceRecorderV1ObsChannel", typing.Dict[builtins.str, typing.Any]]] = None,
        smn_channel: typing.Optional[typing.Union["RmsResourceRecorderV1SmnChannel", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1 opentelekomcloud_rms_resource_recorder_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#agency_name RmsResourceRecorderV1#agency_name}.
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#selector RmsResourceRecorderV1#selector}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#id RmsResourceRecorderV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param obs_channel: obs_channel block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#obs_channel RmsResourceRecorderV1#obs_channel}
        :param smn_channel: smn_channel block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#smn_channel RmsResourceRecorderV1#smn_channel}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55864d00d070c46072da6a3134ffa5e8017b39be34e2d54327f389345823ec0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RmsResourceRecorderV1Config(
            agency_name=agency_name,
            selector=selector,
            id=id,
            obs_channel=obs_channel,
            smn_channel=smn_channel,
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
        '''Generates CDKTF code for importing a RmsResourceRecorderV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RmsResourceRecorderV1 to import.
        :param import_from_id: The id of the existing RmsResourceRecorderV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RmsResourceRecorderV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f0f1c1674fdd4ce6cab51f1d916c93585d5efc1f0cdee629551a1f72e1c4b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putObsChannel")
    def put_obs_channel(
        self,
        *,
        bucket: builtins.str,
        region: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#bucket RmsResourceRecorderV1#bucket}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#region RmsResourceRecorderV1#region}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#bucket_prefix RmsResourceRecorderV1#bucket_prefix}.
        '''
        value = RmsResourceRecorderV1ObsChannel(
            bucket=bucket, region=region, bucket_prefix=bucket_prefix
        )

        return typing.cast(None, jsii.invoke(self, "putObsChannel", [value]))

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        *,
        all_supported: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all_supported: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#all_supported RmsResourceRecorderV1#all_supported}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#resource_types RmsResourceRecorderV1#resource_types}.
        '''
        value = RmsResourceRecorderV1Selector(
            all_supported=all_supported, resource_types=resource_types
        )

        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="putSmnChannel")
    def put_smn_channel(self, *, topic_urn: builtins.str) -> None:
        '''
        :param topic_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#topic_urn RmsResourceRecorderV1#topic_urn}.
        '''
        value = RmsResourceRecorderV1SmnChannel(topic_urn=topic_urn)

        return typing.cast(None, jsii.invoke(self, "putSmnChannel", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetObsChannel")
    def reset_obs_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsChannel", []))

    @jsii.member(jsii_name="resetSmnChannel")
    def reset_smn_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmnChannel", []))

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
    @jsii.member(jsii_name="obsChannel")
    def obs_channel(self) -> "RmsResourceRecorderV1ObsChannelOutputReference":
        return typing.cast("RmsResourceRecorderV1ObsChannelOutputReference", jsii.get(self, "obsChannel"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriod"))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> "RmsResourceRecorderV1SelectorOutputReference":
        return typing.cast("RmsResourceRecorderV1SelectorOutputReference", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="smnChannel")
    def smn_channel(self) -> "RmsResourceRecorderV1SmnChannelOutputReference":
        return typing.cast("RmsResourceRecorderV1SmnChannelOutputReference", jsii.get(self, "smnChannel"))

    @builtins.property
    @jsii.member(jsii_name="agencyNameInput")
    def agency_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="obsChannelInput")
    def obs_channel_input(self) -> typing.Optional["RmsResourceRecorderV1ObsChannel"]:
        return typing.cast(typing.Optional["RmsResourceRecorderV1ObsChannel"], jsii.get(self, "obsChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional["RmsResourceRecorderV1Selector"]:
        return typing.cast(typing.Optional["RmsResourceRecorderV1Selector"], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="smnChannelInput")
    def smn_channel_input(self) -> typing.Optional["RmsResourceRecorderV1SmnChannel"]:
        return typing.cast(typing.Optional["RmsResourceRecorderV1SmnChannel"], jsii.get(self, "smnChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyName")
    def agency_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyName"))

    @agency_name.setter
    def agency_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c8a776520348cc33b22c6e62aa4f2f1d2f1ed1abfa4e20bb6e2c1122a8ed6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4375494a70822785f50c70da34905989593527bbff13771990887e3ae463c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rmsResourceRecorderV1.RmsResourceRecorderV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "agency_name": "agencyName",
        "selector": "selector",
        "id": "id",
        "obs_channel": "obsChannel",
        "smn_channel": "smnChannel",
    },
)
class RmsResourceRecorderV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        agency_name: builtins.str,
        selector: typing.Union["RmsResourceRecorderV1Selector", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        obs_channel: typing.Optional[typing.Union["RmsResourceRecorderV1ObsChannel", typing.Dict[builtins.str, typing.Any]]] = None,
        smn_channel: typing.Optional[typing.Union["RmsResourceRecorderV1SmnChannel", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#agency_name RmsResourceRecorderV1#agency_name}.
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#selector RmsResourceRecorderV1#selector}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#id RmsResourceRecorderV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param obs_channel: obs_channel block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#obs_channel RmsResourceRecorderV1#obs_channel}
        :param smn_channel: smn_channel block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#smn_channel RmsResourceRecorderV1#smn_channel}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(selector, dict):
            selector = RmsResourceRecorderV1Selector(**selector)
        if isinstance(obs_channel, dict):
            obs_channel = RmsResourceRecorderV1ObsChannel(**obs_channel)
        if isinstance(smn_channel, dict):
            smn_channel = RmsResourceRecorderV1SmnChannel(**smn_channel)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bf515721b14a5f5a8bf6bc4ce202611aa027290a09655eb1fcffaa393796fb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument agency_name", value=agency_name, expected_type=type_hints["agency_name"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument obs_channel", value=obs_channel, expected_type=type_hints["obs_channel"])
            check_type(argname="argument smn_channel", value=smn_channel, expected_type=type_hints["smn_channel"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agency_name": agency_name,
            "selector": selector,
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
        if obs_channel is not None:
            self._values["obs_channel"] = obs_channel
        if smn_channel is not None:
            self._values["smn_channel"] = smn_channel

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
    def agency_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#agency_name RmsResourceRecorderV1#agency_name}.'''
        result = self._values.get("agency_name")
        assert result is not None, "Required property 'agency_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(self) -> "RmsResourceRecorderV1Selector":
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#selector RmsResourceRecorderV1#selector}
        '''
        result = self._values.get("selector")
        assert result is not None, "Required property 'selector' is missing"
        return typing.cast("RmsResourceRecorderV1Selector", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#id RmsResourceRecorderV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_channel(self) -> typing.Optional["RmsResourceRecorderV1ObsChannel"]:
        '''obs_channel block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#obs_channel RmsResourceRecorderV1#obs_channel}
        '''
        result = self._values.get("obs_channel")
        return typing.cast(typing.Optional["RmsResourceRecorderV1ObsChannel"], result)

    @builtins.property
    def smn_channel(self) -> typing.Optional["RmsResourceRecorderV1SmnChannel"]:
        '''smn_channel block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#smn_channel RmsResourceRecorderV1#smn_channel}
        '''
        result = self._values.get("smn_channel")
        return typing.cast(typing.Optional["RmsResourceRecorderV1SmnChannel"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RmsResourceRecorderV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rmsResourceRecorderV1.RmsResourceRecorderV1ObsChannel",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "region": "region",
        "bucket_prefix": "bucketPrefix",
    },
)
class RmsResourceRecorderV1ObsChannel:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        region: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#bucket RmsResourceRecorderV1#bucket}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#region RmsResourceRecorderV1#region}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#bucket_prefix RmsResourceRecorderV1#bucket_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__651ac282d695e807e37ed4ae673207cf6d27583ba21e8aa943475d989273d072)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "region": region,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#bucket RmsResourceRecorderV1#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#region RmsResourceRecorderV1#region}.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#bucket_prefix RmsResourceRecorderV1#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RmsResourceRecorderV1ObsChannel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RmsResourceRecorderV1ObsChannelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rmsResourceRecorderV1.RmsResourceRecorderV1ObsChannelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe0fa9d321fff2671b7d270c6c567fe35bf54635c166fd22367b34fc4b384e25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f84b6b25ae5875bf5dc14725d5d5f475d7a77c8b0e5c467f774a197793cd36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0df36586e22059cf3d5e1e1e0f8eacb11168f43365abec221bdc28e173cd11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cfc5039478cf9fcb100cd67b4696913193988c87152d089f491a413b2ddca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RmsResourceRecorderV1ObsChannel]:
        return typing.cast(typing.Optional[RmsResourceRecorderV1ObsChannel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RmsResourceRecorderV1ObsChannel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4d1f4dcba32b9f47b852cc02ef533007f4f22840aabe37e8562316a16c694f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rmsResourceRecorderV1.RmsResourceRecorderV1Selector",
    jsii_struct_bases=[],
    name_mapping={"all_supported": "allSupported", "resource_types": "resourceTypes"},
)
class RmsResourceRecorderV1Selector:
    def __init__(
        self,
        *,
        all_supported: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all_supported: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#all_supported RmsResourceRecorderV1#all_supported}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#resource_types RmsResourceRecorderV1#resource_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c64ce5cec43cbf42a5ea4ff4f61a591c0adb24d8fb5e3071840d1022f8d13cad)
            check_type(argname="argument all_supported", value=all_supported, expected_type=type_hints["all_supported"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "all_supported": all_supported,
        }
        if resource_types is not None:
            self._values["resource_types"] = resource_types

    @builtins.property
    def all_supported(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#all_supported RmsResourceRecorderV1#all_supported}.'''
        result = self._values.get("all_supported")
        assert result is not None, "Required property 'all_supported' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#resource_types RmsResourceRecorderV1#resource_types}.'''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RmsResourceRecorderV1Selector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RmsResourceRecorderV1SelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rmsResourceRecorderV1.RmsResourceRecorderV1SelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59ee81522c638a6c45e232bc31aea7334d8fe4621f8019e6a39f876a57622082)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResourceTypes")
    def reset_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypes", []))

    @builtins.property
    @jsii.member(jsii_name="allSupportedInput")
    def all_supported_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allSupportedInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="allSupported")
    def all_supported(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allSupported"))

    @all_supported.setter
    def all_supported(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bffec32857f5536a1b174c47b0b2202bca8ca5d20f78c6930ca35b0c144eec61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allSupported", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce7d19a9d310775163565e2e046f2cf04aed85778a1b0e927feefc398a9c24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RmsResourceRecorderV1Selector]:
        return typing.cast(typing.Optional[RmsResourceRecorderV1Selector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RmsResourceRecorderV1Selector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f515f8b3ba70997274dcaabd55077fedefc23bea044031b82a6ac0f682d57b2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rmsResourceRecorderV1.RmsResourceRecorderV1SmnChannel",
    jsii_struct_bases=[],
    name_mapping={"topic_urn": "topicUrn"},
)
class RmsResourceRecorderV1SmnChannel:
    def __init__(self, *, topic_urn: builtins.str) -> None:
        '''
        :param topic_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#topic_urn RmsResourceRecorderV1#topic_urn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30200722507b9e12588b0c8bd309906061d1cf59e492c9d9aa42e5b4251e1bd2)
            check_type(argname="argument topic_urn", value=topic_urn, expected_type=type_hints["topic_urn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_urn": topic_urn,
        }

    @builtins.property
    def topic_urn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_resource_recorder_v1#topic_urn RmsResourceRecorderV1#topic_urn}.'''
        result = self._values.get("topic_urn")
        assert result is not None, "Required property 'topic_urn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RmsResourceRecorderV1SmnChannel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RmsResourceRecorderV1SmnChannelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rmsResourceRecorderV1.RmsResourceRecorderV1SmnChannelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1f3f4050bc5315791a21ed3443c0f7fbd19188ef928cb3d3056d118a954178e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="topicUrnInput")
    def topic_urn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicUrnInput"))

    @builtins.property
    @jsii.member(jsii_name="topicUrn")
    def topic_urn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicUrn"))

    @topic_urn.setter
    def topic_urn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db830ac5b13a8b3a0778e3b38b1bd6240349f22e47aaca6be47e01966b721420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicUrn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RmsResourceRecorderV1SmnChannel]:
        return typing.cast(typing.Optional[RmsResourceRecorderV1SmnChannel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RmsResourceRecorderV1SmnChannel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d252d6d3d94ef18b4a42d4f4f002f7ccca1e9dfad7303880870294952ecfeda1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RmsResourceRecorderV1",
    "RmsResourceRecorderV1Config",
    "RmsResourceRecorderV1ObsChannel",
    "RmsResourceRecorderV1ObsChannelOutputReference",
    "RmsResourceRecorderV1Selector",
    "RmsResourceRecorderV1SelectorOutputReference",
    "RmsResourceRecorderV1SmnChannel",
    "RmsResourceRecorderV1SmnChannelOutputReference",
]

publication.publish()

def _typecheckingstub__a55864d00d070c46072da6a3134ffa5e8017b39be34e2d54327f389345823ec0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    agency_name: builtins.str,
    selector: typing.Union[RmsResourceRecorderV1Selector, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    obs_channel: typing.Optional[typing.Union[RmsResourceRecorderV1ObsChannel, typing.Dict[builtins.str, typing.Any]]] = None,
    smn_channel: typing.Optional[typing.Union[RmsResourceRecorderV1SmnChannel, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__60f0f1c1674fdd4ce6cab51f1d916c93585d5efc1f0cdee629551a1f72e1c4b8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c8a776520348cc33b22c6e62aa4f2f1d2f1ed1abfa4e20bb6e2c1122a8ed6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4375494a70822785f50c70da34905989593527bbff13771990887e3ae463c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bf515721b14a5f5a8bf6bc4ce202611aa027290a09655eb1fcffaa393796fb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    agency_name: builtins.str,
    selector: typing.Union[RmsResourceRecorderV1Selector, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    obs_channel: typing.Optional[typing.Union[RmsResourceRecorderV1ObsChannel, typing.Dict[builtins.str, typing.Any]]] = None,
    smn_channel: typing.Optional[typing.Union[RmsResourceRecorderV1SmnChannel, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651ac282d695e807e37ed4ae673207cf6d27583ba21e8aa943475d989273d072(
    *,
    bucket: builtins.str,
    region: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0fa9d321fff2671b7d270c6c567fe35bf54635c166fd22367b34fc4b384e25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f84b6b25ae5875bf5dc14725d5d5f475d7a77c8b0e5c467f774a197793cd36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0df36586e22059cf3d5e1e1e0f8eacb11168f43365abec221bdc28e173cd11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cfc5039478cf9fcb100cd67b4696913193988c87152d089f491a413b2ddca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4d1f4dcba32b9f47b852cc02ef533007f4f22840aabe37e8562316a16c694f(
    value: typing.Optional[RmsResourceRecorderV1ObsChannel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64ce5cec43cbf42a5ea4ff4f61a591c0adb24d8fb5e3071840d1022f8d13cad(
    *,
    all_supported: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ee81522c638a6c45e232bc31aea7334d8fe4621f8019e6a39f876a57622082(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffec32857f5536a1b174c47b0b2202bca8ca5d20f78c6930ca35b0c144eec61(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce7d19a9d310775163565e2e046f2cf04aed85778a1b0e927feefc398a9c24e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f515f8b3ba70997274dcaabd55077fedefc23bea044031b82a6ac0f682d57b2e(
    value: typing.Optional[RmsResourceRecorderV1Selector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30200722507b9e12588b0c8bd309906061d1cf59e492c9d9aa42e5b4251e1bd2(
    *,
    topic_urn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f3f4050bc5315791a21ed3443c0f7fbd19188ef928cb3d3056d118a954178e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db830ac5b13a8b3a0778e3b38b1bd6240349f22e47aaca6be47e01966b721420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d252d6d3d94ef18b4a42d4f4f002f7ccca1e9dfad7303880870294952ecfeda1(
    value: typing.Optional[RmsResourceRecorderV1SmnChannel],
) -> None:
    """Type checking stubs"""
    pass
