r'''
# `data_opentelekomcloud_ces_event_details_v1`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_ces_event_details_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1).
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


class DataOpentelekomcloudCesEventDetailsV1(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1 opentelekomcloud_ces_event_details_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        event_name: builtins.str,
        event_type: builtins.str,
        event_level: typing.Optional[builtins.str] = None,
        event_source: typing.Optional[builtins.str] = None,
        event_state: typing.Optional[builtins.str] = None,
        event_user: typing.Optional[builtins.str] = None,
        from_: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        limit: typing.Optional[jsii.Number] = None,
        to: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1 opentelekomcloud_ces_event_details_v1} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param event_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_name DataOpentelekomcloudCesEventDetailsV1#event_name}.
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_type DataOpentelekomcloudCesEventDetailsV1#event_type}.
        :param event_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_level DataOpentelekomcloudCesEventDetailsV1#event_level}.
        :param event_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_source DataOpentelekomcloudCesEventDetailsV1#event_source}.
        :param event_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_state DataOpentelekomcloudCesEventDetailsV1#event_state}.
        :param event_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_user DataOpentelekomcloudCesEventDetailsV1#event_user}.
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#from DataOpentelekomcloudCesEventDetailsV1#from}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#id DataOpentelekomcloudCesEventDetailsV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#limit DataOpentelekomcloudCesEventDetailsV1#limit}.
        :param to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#to DataOpentelekomcloudCesEventDetailsV1#to}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade3471b1278fd9039d67b380acc9cdc2cd82feca46110733b123bfc8b6eac5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudCesEventDetailsV1Config(
            event_name=event_name,
            event_type=event_type,
            event_level=event_level,
            event_source=event_source,
            event_state=event_state,
            event_user=event_user,
            from_=from_,
            id=id,
            limit=limit,
            to=to,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudCesEventDetailsV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudCesEventDetailsV1 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudCesEventDetailsV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudCesEventDetailsV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f76ef3666e4f142a1537fea947cc63ead2cbbfc75331a6af06bcafa3619ab3d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetEventLevel")
    def reset_event_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventLevel", []))

    @jsii.member(jsii_name="resetEventSource")
    def reset_event_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventSource", []))

    @jsii.member(jsii_name="resetEventState")
    def reset_event_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventState", []))

    @jsii.member(jsii_name="resetEventUser")
    def reset_event_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventUser", []))

    @jsii.member(jsii_name="resetFrom")
    def reset_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrom", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLimit")
    def reset_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimit", []))

    @jsii.member(jsii_name="resetTo")
    def reset_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTo", []))

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
    @jsii.member(jsii_name="eventInfo")
    def event_info(self) -> "DataOpentelekomcloudCesEventDetailsV1EventInfoList":
        return typing.cast("DataOpentelekomcloudCesEventDetailsV1EventInfoList", jsii.get(self, "eventInfo"))

    @builtins.property
    @jsii.member(jsii_name="eventSources")
    def event_sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventSources"))

    @builtins.property
    @jsii.member(jsii_name="eventUsers")
    def event_users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventUsers"))

    @builtins.property
    @jsii.member(jsii_name="metaData")
    def meta_data(self) -> "DataOpentelekomcloudCesEventDetailsV1MetaDataList":
        return typing.cast("DataOpentelekomcloudCesEventDetailsV1MetaDataList", jsii.get(self, "metaData"))

    @builtins.property
    @jsii.member(jsii_name="eventLevelInput")
    def event_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="eventNameInput")
    def event_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceInput")
    def event_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="eventStateInput")
    def event_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventStateInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="eventUserInput")
    def event_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventUserInput"))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="toInput")
    def to_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "toInput"))

    @builtins.property
    @jsii.member(jsii_name="eventLevel")
    def event_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventLevel"))

    @event_level.setter
    def event_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff5c2ad59c0f0d2fcddcf71976d64864b6dc338e0976379039e1f48604dd646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventName")
    def event_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventName"))

    @event_name.setter
    def event_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e0bf800ad74944c8978089021aa480bea9d9bb318f88c8d963aec12ce3bdec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventSource")
    def event_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventSource"))

    @event_source.setter
    def event_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce155d05bd1594294f3b8d25915a38529f9e3ec57986d793540448ea59d48d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventState")
    def event_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventState"))

    @event_state.setter
    def event_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21844a0f448a8c76b1b4e489c761ef18076a125223e906fc982f13759d7aab4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd23c7e8b8e6fe682f0b667eb2dee79a93bc46710f843d7ba7e4f7d6aa82d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventUser")
    def event_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventUser"))

    @event_user.setter
    def event_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36eb94cb220edd1c5f8b3bd3b476126d5b88b72be480a276a27e6f9b1c117d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "from"))

    @from_.setter
    def from_(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a1efd9198acba0a7b93caa0d792c1fe4f9f3bcffa0c5b14dda08ae00b2b3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7e6e328401aa6e26dc88d0cf64a298996802baf7a126354e6fb5ce9c6b0792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d549e4af1b01feb1945475fb1f391420c2d0647e5f67396e5f5e5032bf989bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="to")
    def to(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "to"))

    @to.setter
    def to(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceefaf357dcc437fa8ace5347a9840cee1784bafd83209a2f53cb3c8ede16ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "to", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "event_name": "eventName",
        "event_type": "eventType",
        "event_level": "eventLevel",
        "event_source": "eventSource",
        "event_state": "eventState",
        "event_user": "eventUser",
        "from_": "from",
        "id": "id",
        "limit": "limit",
        "to": "to",
    },
)
class DataOpentelekomcloudCesEventDetailsV1Config(
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
        event_name: builtins.str,
        event_type: builtins.str,
        event_level: typing.Optional[builtins.str] = None,
        event_source: typing.Optional[builtins.str] = None,
        event_state: typing.Optional[builtins.str] = None,
        event_user: typing.Optional[builtins.str] = None,
        from_: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        limit: typing.Optional[jsii.Number] = None,
        to: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param event_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_name DataOpentelekomcloudCesEventDetailsV1#event_name}.
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_type DataOpentelekomcloudCesEventDetailsV1#event_type}.
        :param event_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_level DataOpentelekomcloudCesEventDetailsV1#event_level}.
        :param event_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_source DataOpentelekomcloudCesEventDetailsV1#event_source}.
        :param event_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_state DataOpentelekomcloudCesEventDetailsV1#event_state}.
        :param event_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_user DataOpentelekomcloudCesEventDetailsV1#event_user}.
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#from DataOpentelekomcloudCesEventDetailsV1#from}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#id DataOpentelekomcloudCesEventDetailsV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#limit DataOpentelekomcloudCesEventDetailsV1#limit}.
        :param to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#to DataOpentelekomcloudCesEventDetailsV1#to}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0d744562025444ed15e38d7ded0aae7f12f0d81796e55489fa9e26b625fad3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument event_level", value=event_level, expected_type=type_hints["event_level"])
            check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
            check_type(argname="argument event_state", value=event_state, expected_type=type_hints["event_state"])
            check_type(argname="argument event_user", value=event_user, expected_type=type_hints["event_user"])
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_name": event_name,
            "event_type": event_type,
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
        if event_level is not None:
            self._values["event_level"] = event_level
        if event_source is not None:
            self._values["event_source"] = event_source
        if event_state is not None:
            self._values["event_state"] = event_state
        if event_user is not None:
            self._values["event_user"] = event_user
        if from_ is not None:
            self._values["from_"] = from_
        if id is not None:
            self._values["id"] = id
        if limit is not None:
            self._values["limit"] = limit
        if to is not None:
            self._values["to"] = to

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
    def event_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_name DataOpentelekomcloudCesEventDetailsV1#event_name}.'''
        result = self._values.get("event_name")
        assert result is not None, "Required property 'event_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_type DataOpentelekomcloudCesEventDetailsV1#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_level DataOpentelekomcloudCesEventDetailsV1#event_level}.'''
        result = self._values.get("event_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_source DataOpentelekomcloudCesEventDetailsV1#event_source}.'''
        result = self._values.get("event_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_state DataOpentelekomcloudCesEventDetailsV1#event_state}.'''
        result = self._values.get("event_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#event_user DataOpentelekomcloudCesEventDetailsV1#event_user}.'''
        result = self._values.get("event_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def from_(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#from DataOpentelekomcloudCesEventDetailsV1#from}.'''
        result = self._values.get("from_")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#id DataOpentelekomcloudCesEventDetailsV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#limit DataOpentelekomcloudCesEventDetailsV1#limit}.'''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def to(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/ces_event_details_v1#to DataOpentelekomcloudCesEventDetailsV1#to}.'''
        result = self._values.get("to")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCesEventDetailsV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1EventInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudCesEventDetailsV1EventInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCesEventDetailsV1EventInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1EventInfoDetail",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudCesEventDetailsV1EventInfoDetail:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCesEventDetailsV1EventInfoDetail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudCesEventDetailsV1EventInfoDetailList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1EventInfoDetailList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7ba2705e9fcf4e71c5828d6e4e0c43a146c1b65a463e915ded0cd404688e750)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudCesEventDetailsV1EventInfoDetailOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367d8605f4f9cb4c3aa47f2af5103720987a9f0734c96d84f15552529f016c53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudCesEventDetailsV1EventInfoDetailOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5e4624c760d42b56971cdd870fb05452981b4713177c10332cb3361e831907)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acf33ebaeb84f1e347d4611fb98bad4c2f5b64b4d805cb50e2f525a33961ac3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c13586087b4ae537f2eb51412a0d017af1f983461f37d3c7affaa41ca56391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudCesEventDetailsV1EventInfoDetailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1EventInfoDetailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b92d49ef7796ff75672da7661e98331049bdc8e262c16346f0b81ae29c445c57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @builtins.property
    @jsii.member(jsii_name="eventLevel")
    def event_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventLevel"))

    @builtins.property
    @jsii.member(jsii_name="eventState")
    def event_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventState"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @builtins.property
    @jsii.member(jsii_name="eventUser")
    def event_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventUser"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="resourceName")
    def resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudCesEventDetailsV1EventInfoDetail]:
        return typing.cast(typing.Optional[DataOpentelekomcloudCesEventDetailsV1EventInfoDetail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudCesEventDetailsV1EventInfoDetail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c945f9ddceb6eb219ee53359363364acdbf662cb28afb9581f328b1eecc7544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudCesEventDetailsV1EventInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1EventInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74d2bb5776dcc585fc6a9cab6862cba6becbbfc28d5316b04d44e45e33793464)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudCesEventDetailsV1EventInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36ca27f7bcefa51d5d8ef441b5f7a531a507ab4f444ec5ea4c2927c9e3da22d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudCesEventDetailsV1EventInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9c0c3dbc48fc16c1d6739e7165580f0f5b3d175d6065e57f0ba94233708e60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__964d43a6561668a2bbce61c0fb604545fe565889d9e27127146f13fc842410eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9a204576764f6d6d095c30cf7b77dcda940b04a4165c62d407f5d872b07fd91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudCesEventDetailsV1EventInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1EventInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ccce179933376aae24b5a388d971d9aaff2d684608229e42ba8725e1c7ad7ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="detail")
    def detail(self) -> DataOpentelekomcloudCesEventDetailsV1EventInfoDetailList:
        return typing.cast(DataOpentelekomcloudCesEventDetailsV1EventInfoDetailList, jsii.get(self, "detail"))

    @builtins.property
    @jsii.member(jsii_name="eventId")
    def event_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventId"))

    @builtins.property
    @jsii.member(jsii_name="eventName")
    def event_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventName"))

    @builtins.property
    @jsii.member(jsii_name="eventSource")
    def event_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventSource"))

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "time"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudCesEventDetailsV1EventInfo]:
        return typing.cast(typing.Optional[DataOpentelekomcloudCesEventDetailsV1EventInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudCesEventDetailsV1EventInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9d01db9a0a8712a3b43d042cca3af0adc317224278d3348cfbe7d18db9c3e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1MetaData",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudCesEventDetailsV1MetaData:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCesEventDetailsV1MetaData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudCesEventDetailsV1MetaDataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1MetaDataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f734896b0ea1b9f1a15c71181fe6f6138a807ea3757aa9f1a9470e4a9cf7e4f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudCesEventDetailsV1MetaDataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5fe1828532a045da933589815e8be457965499359b921c25069f590eb2a6fc0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudCesEventDetailsV1MetaDataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d507b0e1441bd96fb6b1e641dcd84bf2f9c24ca69283fdb981918f9c03fa27dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79585815a7853301aaf009baea2a3b76f7e8e8761d9964cc2322e48d4c0ed0f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d4c666475f60e709541ec862c182433a54e67e85bd127a8231fd7daa595e28a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudCesEventDetailsV1MetaDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCesEventDetailsV1.DataOpentelekomcloudCesEventDetailsV1MetaDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c20bca50104b39b4b31fafb861061a38557cc6a9b589e0a15c5aab5348c5e41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="total")
    def total(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "total"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudCesEventDetailsV1MetaData]:
        return typing.cast(typing.Optional[DataOpentelekomcloudCesEventDetailsV1MetaData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudCesEventDetailsV1MetaData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173487a979e5bb19d066fa686164bf487f62c1c203c6e0414518fca38c780679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOpentelekomcloudCesEventDetailsV1",
    "DataOpentelekomcloudCesEventDetailsV1Config",
    "DataOpentelekomcloudCesEventDetailsV1EventInfo",
    "DataOpentelekomcloudCesEventDetailsV1EventInfoDetail",
    "DataOpentelekomcloudCesEventDetailsV1EventInfoDetailList",
    "DataOpentelekomcloudCesEventDetailsV1EventInfoDetailOutputReference",
    "DataOpentelekomcloudCesEventDetailsV1EventInfoList",
    "DataOpentelekomcloudCesEventDetailsV1EventInfoOutputReference",
    "DataOpentelekomcloudCesEventDetailsV1MetaData",
    "DataOpentelekomcloudCesEventDetailsV1MetaDataList",
    "DataOpentelekomcloudCesEventDetailsV1MetaDataOutputReference",
]

publication.publish()

def _typecheckingstub__ade3471b1278fd9039d67b380acc9cdc2cd82feca46110733b123bfc8b6eac5c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    event_name: builtins.str,
    event_type: builtins.str,
    event_level: typing.Optional[builtins.str] = None,
    event_source: typing.Optional[builtins.str] = None,
    event_state: typing.Optional[builtins.str] = None,
    event_user: typing.Optional[builtins.str] = None,
    from_: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    limit: typing.Optional[jsii.Number] = None,
    to: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__1f76ef3666e4f142a1537fea947cc63ead2cbbfc75331a6af06bcafa3619ab3d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff5c2ad59c0f0d2fcddcf71976d64864b6dc338e0976379039e1f48604dd646(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e0bf800ad74944c8978089021aa480bea9d9bb318f88c8d963aec12ce3bdec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce155d05bd1594294f3b8d25915a38529f9e3ec57986d793540448ea59d48d47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21844a0f448a8c76b1b4e489c761ef18076a125223e906fc982f13759d7aab4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd23c7e8b8e6fe682f0b667eb2dee79a93bc46710f843d7ba7e4f7d6aa82d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36eb94cb220edd1c5f8b3bd3b476126d5b88b72be480a276a27e6f9b1c117d4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a1efd9198acba0a7b93caa0d792c1fe4f9f3bcffa0c5b14dda08ae00b2b3df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7e6e328401aa6e26dc88d0cf64a298996802baf7a126354e6fb5ce9c6b0792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d549e4af1b01feb1945475fb1f391420c2d0647e5f67396e5f5e5032bf989bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceefaf357dcc437fa8ace5347a9840cee1784bafd83209a2f53cb3c8ede16ffb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0d744562025444ed15e38d7ded0aae7f12f0d81796e55489fa9e26b625fad3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_name: builtins.str,
    event_type: builtins.str,
    event_level: typing.Optional[builtins.str] = None,
    event_source: typing.Optional[builtins.str] = None,
    event_state: typing.Optional[builtins.str] = None,
    event_user: typing.Optional[builtins.str] = None,
    from_: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    limit: typing.Optional[jsii.Number] = None,
    to: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ba2705e9fcf4e71c5828d6e4e0c43a146c1b65a463e915ded0cd404688e750(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367d8605f4f9cb4c3aa47f2af5103720987a9f0734c96d84f15552529f016c53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5e4624c760d42b56971cdd870fb05452981b4713177c10332cb3361e831907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf33ebaeb84f1e347d4611fb98bad4c2f5b64b4d805cb50e2f525a33961ac3d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c13586087b4ae537f2eb51412a0d017af1f983461f37d3c7affaa41ca56391(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92d49ef7796ff75672da7661e98331049bdc8e262c16346f0b81ae29c445c57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c945f9ddceb6eb219ee53359363364acdbf662cb28afb9581f328b1eecc7544(
    value: typing.Optional[DataOpentelekomcloudCesEventDetailsV1EventInfoDetail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d2bb5776dcc585fc6a9cab6862cba6becbbfc28d5316b04d44e45e33793464(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36ca27f7bcefa51d5d8ef441b5f7a531a507ab4f444ec5ea4c2927c9e3da22d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9c0c3dbc48fc16c1d6739e7165580f0f5b3d175d6065e57f0ba94233708e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964d43a6561668a2bbce61c0fb604545fe565889d9e27127146f13fc842410eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a204576764f6d6d095c30cf7b77dcda940b04a4165c62d407f5d872b07fd91(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ccce179933376aae24b5a388d971d9aaff2d684608229e42ba8725e1c7ad7ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9d01db9a0a8712a3b43d042cca3af0adc317224278d3348cfbe7d18db9c3e2(
    value: typing.Optional[DataOpentelekomcloudCesEventDetailsV1EventInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f734896b0ea1b9f1a15c71181fe6f6138a807ea3757aa9f1a9470e4a9cf7e4f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5fe1828532a045da933589815e8be457965499359b921c25069f590eb2a6fc0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d507b0e1441bd96fb6b1e641dcd84bf2f9c24ca69283fdb981918f9c03fa27dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79585815a7853301aaf009baea2a3b76f7e8e8761d9964cc2322e48d4c0ed0f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4c666475f60e709541ec862c182433a54e67e85bd127a8231fd7daa595e28a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c20bca50104b39b4b31fafb861061a38557cc6a9b589e0a15c5aab5348c5e41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173487a979e5bb19d066fa686164bf487f62c1c203c6e0414518fca38c780679(
    value: typing.Optional[DataOpentelekomcloudCesEventDetailsV1MetaData],
) -> None:
    """Type checking stubs"""
    pass
