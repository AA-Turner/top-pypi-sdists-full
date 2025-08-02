r'''
# `opentelekomcloud_ces_event_report_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_ces_event_report_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1).
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


class CesEventReportV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesEventReportV1.CesEventReportV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1 opentelekomcloud_ces_event_report_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        detail: typing.Union["CesEventReportV1Detail", typing.Dict[builtins.str, typing.Any]],
        event_name: builtins.str,
        event_source: builtins.str,
        time: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CesEventReportV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1 opentelekomcloud_ces_event_report_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param detail: detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#detail CesEventReportV1#detail}
        :param event_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_name CesEventReportV1#event_name}.
        :param event_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_source CesEventReportV1#event_source}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#time CesEventReportV1#time}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#id CesEventReportV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#timeouts CesEventReportV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35420e8625e09b17e10b25b15267041f67e72aa18fe826797362d801726c0d78)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CesEventReportV1Config(
            detail=detail,
            event_name=event_name,
            event_source=event_source,
            time=time,
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
        '''Generates CDKTF code for importing a CesEventReportV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CesEventReportV1 to import.
        :param import_from_id: The id of the existing CesEventReportV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CesEventReportV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7078b6c32817430e855810e6c6d617fcce6d301bc9efc845728425b4737fdbc2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDetail")
    def put_detail(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        event_level: typing.Optional[builtins.str] = None,
        event_state: typing.Optional[builtins.str] = None,
        event_type: typing.Optional[builtins.str] = None,
        event_user: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#content CesEventReportV1#content}.
        :param event_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_level CesEventReportV1#event_level}.
        :param event_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_state CesEventReportV1#event_state}.
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_type CesEventReportV1#event_type}.
        :param event_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_user CesEventReportV1#event_user}.
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#group_id CesEventReportV1#group_id}.
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#resource_id CesEventReportV1#resource_id}.
        :param resource_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#resource_name CesEventReportV1#resource_name}.
        '''
        value = CesEventReportV1Detail(
            content=content,
            event_level=event_level,
            event_state=event_state,
            event_type=event_type,
            event_user=event_user,
            group_id=group_id,
            resource_id=resource_id,
            resource_name=resource_name,
        )

        return typing.cast(None, jsii.invoke(self, "putDetail", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#create CesEventReportV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#delete CesEventReportV1#delete}.
        '''
        value = CesEventReportV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

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
    @jsii.member(jsii_name="detail")
    def detail(self) -> "CesEventReportV1DetailOutputReference":
        return typing.cast("CesEventReportV1DetailOutputReference", jsii.get(self, "detail"))

    @builtins.property
    @jsii.member(jsii_name="eventId")
    def event_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CesEventReportV1TimeoutsOutputReference":
        return typing.cast("CesEventReportV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="detailInput")
    def detail_input(self) -> typing.Optional["CesEventReportV1Detail"]:
        return typing.cast(typing.Optional["CesEventReportV1Detail"], jsii.get(self, "detailInput"))

    @builtins.property
    @jsii.member(jsii_name="eventNameInput")
    def event_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceInput")
    def event_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CesEventReportV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CesEventReportV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="eventName")
    def event_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventName"))

    @event_name.setter
    def event_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e83bf49509840742b012ba7fe90006220da0167dc2eac774841876091ad5e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventSource")
    def event_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventSource"))

    @event_source.setter
    def event_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc057c8318531b58266ab4d01cd7cbde18854aa6dbf870479e2eba31e7527a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aaf42bea9d9668a600ffee5b7b25eb91fc9f466c139641e6b4ab13cfb721215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "time"))

    @time.setter
    def time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e22790aeeb63f910eb17a8d89a0072d6cfb6aa365df9a22f41681a6a446aca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesEventReportV1.CesEventReportV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "detail": "detail",
        "event_name": "eventName",
        "event_source": "eventSource",
        "time": "time",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class CesEventReportV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        detail: typing.Union["CesEventReportV1Detail", typing.Dict[builtins.str, typing.Any]],
        event_name: builtins.str,
        event_source: builtins.str,
        time: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CesEventReportV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param detail: detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#detail CesEventReportV1#detail}
        :param event_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_name CesEventReportV1#event_name}.
        :param event_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_source CesEventReportV1#event_source}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#time CesEventReportV1#time}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#id CesEventReportV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#timeouts CesEventReportV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(detail, dict):
            detail = CesEventReportV1Detail(**detail)
        if isinstance(timeouts, dict):
            timeouts = CesEventReportV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f694d786cac7007c8fb3b0a0aebddd610a97c32495a3fbf3b6c6334008c133)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument detail", value=detail, expected_type=type_hints["detail"])
            check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
            check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "detail": detail,
            "event_name": event_name,
            "event_source": event_source,
            "time": time,
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
    def detail(self) -> "CesEventReportV1Detail":
        '''detail block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#detail CesEventReportV1#detail}
        '''
        result = self._values.get("detail")
        assert result is not None, "Required property 'detail' is missing"
        return typing.cast("CesEventReportV1Detail", result)

    @builtins.property
    def event_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_name CesEventReportV1#event_name}.'''
        result = self._values.get("event_name")
        assert result is not None, "Required property 'event_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_source CesEventReportV1#event_source}.'''
        result = self._values.get("event_source")
        assert result is not None, "Required property 'event_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#time CesEventReportV1#time}.'''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#id CesEventReportV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CesEventReportV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#timeouts CesEventReportV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CesEventReportV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesEventReportV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesEventReportV1.CesEventReportV1Detail",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "event_level": "eventLevel",
        "event_state": "eventState",
        "event_type": "eventType",
        "event_user": "eventUser",
        "group_id": "groupId",
        "resource_id": "resourceId",
        "resource_name": "resourceName",
    },
)
class CesEventReportV1Detail:
    def __init__(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        event_level: typing.Optional[builtins.str] = None,
        event_state: typing.Optional[builtins.str] = None,
        event_type: typing.Optional[builtins.str] = None,
        event_user: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#content CesEventReportV1#content}.
        :param event_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_level CesEventReportV1#event_level}.
        :param event_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_state CesEventReportV1#event_state}.
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_type CesEventReportV1#event_type}.
        :param event_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_user CesEventReportV1#event_user}.
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#group_id CesEventReportV1#group_id}.
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#resource_id CesEventReportV1#resource_id}.
        :param resource_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#resource_name CesEventReportV1#resource_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3953fa46f0610db56a89ff9de983ba00d7f9da2243ff9bab947b1b72097673)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument event_level", value=event_level, expected_type=type_hints["event_level"])
            check_type(argname="argument event_state", value=event_state, expected_type=type_hints["event_state"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument event_user", value=event_user, expected_type=type_hints["event_user"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if event_level is not None:
            self._values["event_level"] = event_level
        if event_state is not None:
            self._values["event_state"] = event_state
        if event_type is not None:
            self._values["event_type"] = event_type
        if event_user is not None:
            self._values["event_user"] = event_user
        if group_id is not None:
            self._values["group_id"] = group_id
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if resource_name is not None:
            self._values["resource_name"] = resource_name

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#content CesEventReportV1#content}.'''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_level CesEventReportV1#event_level}.'''
        result = self._values.get("event_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_state CesEventReportV1#event_state}.'''
        result = self._values.get("event_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_type CesEventReportV1#event_type}.'''
        result = self._values.get("event_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#event_user CesEventReportV1#event_user}.'''
        result = self._values.get("event_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#group_id CesEventReportV1#group_id}.'''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#resource_id CesEventReportV1#resource_id}.'''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#resource_name CesEventReportV1#resource_name}.'''
        result = self._values.get("resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesEventReportV1Detail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CesEventReportV1DetailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesEventReportV1.CesEventReportV1DetailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12ff002fcd079fc5723819441dec4ae1d760cb3b540ce5b8d60401edba42c2a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetEventLevel")
    def reset_event_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventLevel", []))

    @jsii.member(jsii_name="resetEventState")
    def reset_event_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventState", []))

    @jsii.member(jsii_name="resetEventType")
    def reset_event_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventType", []))

    @jsii.member(jsii_name="resetEventUser")
    def reset_event_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventUser", []))

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetResourceId")
    def reset_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceId", []))

    @jsii.member(jsii_name="resetResourceName")
    def reset_resource_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceName", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="eventLevelInput")
    def event_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventLevelInput"))

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
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceNameInput")
    def resource_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d0d9cd0e2356679a77a7172a02d4ad82a6aae56e8c147a58052f8d07bd0fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventLevel")
    def event_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventLevel"))

    @event_level.setter
    def event_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7017c13c77a048c45e0542eae9e2841aff15433ba0e96c7d5a0ad32951dfb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventState")
    def event_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventState"))

    @event_state.setter
    def event_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1490cbb0cd54c85a9d83b21c48f6404be378dac9603783f758b4795bbf7188f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf283650701db116aee6f2d689adf4436ae7d9442ffd0e1c0b69152c523b03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventUser")
    def event_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventUser"))

    @event_user.setter
    def event_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f208da685ba0dd7a006f7c6e273873eb186af31c6a434e5b276614ab451115ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c4545480a62c51d63d66b2f7e5dc85c97ef816bc0ca5b2b72624debe6f7a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32809fcfd3e3733209e677234bccd368626db2850debf23f9b39e1bddc0991f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceName")
    def resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceName"))

    @resource_name.setter
    def resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f3c58025547c1e46a1a7c3e719085076357158d1ccb608b354c5a95a7a6b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CesEventReportV1Detail]:
        return typing.cast(typing.Optional[CesEventReportV1Detail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CesEventReportV1Detail]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5757df74532b5aa9600453ab34ec51c4e4e0b0a4304af794ec9646e51a0de4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cesEventReportV1.CesEventReportV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class CesEventReportV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#create CesEventReportV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#delete CesEventReportV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac71935a2114f3d45f41cc39fe285506a117f613d072d297102e2e8457152486)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#create CesEventReportV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/ces_event_report_v1#delete CesEventReportV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CesEventReportV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CesEventReportV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cesEventReportV1.CesEventReportV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dce5f8611cc11da42df6b4cc987b4937431caaec0d7e35988685bb09c27a112d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b213c831471a163f0fcdc7f0baa0c5a6f40241e94ef8d9b39ad7fe0fc1f7876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757ea09122c5835374c24d8e8dcd8d4d614c47377a2830008ed3e2f0b9c9b7e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesEventReportV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesEventReportV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesEventReportV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a3efd1186a040e486c285465f3e7f9edb45ce324c6b6917bd4c4b612808049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CesEventReportV1",
    "CesEventReportV1Config",
    "CesEventReportV1Detail",
    "CesEventReportV1DetailOutputReference",
    "CesEventReportV1Timeouts",
    "CesEventReportV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__35420e8625e09b17e10b25b15267041f67e72aa18fe826797362d801726c0d78(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    detail: typing.Union[CesEventReportV1Detail, typing.Dict[builtins.str, typing.Any]],
    event_name: builtins.str,
    event_source: builtins.str,
    time: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CesEventReportV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7078b6c32817430e855810e6c6d617fcce6d301bc9efc845728425b4737fdbc2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e83bf49509840742b012ba7fe90006220da0167dc2eac774841876091ad5e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc057c8318531b58266ab4d01cd7cbde18854aa6dbf870479e2eba31e7527a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aaf42bea9d9668a600ffee5b7b25eb91fc9f466c139641e6b4ab13cfb721215(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e22790aeeb63f910eb17a8d89a0072d6cfb6aa365df9a22f41681a6a446aca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f694d786cac7007c8fb3b0a0aebddd610a97c32495a3fbf3b6c6334008c133(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    detail: typing.Union[CesEventReportV1Detail, typing.Dict[builtins.str, typing.Any]],
    event_name: builtins.str,
    event_source: builtins.str,
    time: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CesEventReportV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3953fa46f0610db56a89ff9de983ba00d7f9da2243ff9bab947b1b72097673(
    *,
    content: typing.Optional[builtins.str] = None,
    event_level: typing.Optional[builtins.str] = None,
    event_state: typing.Optional[builtins.str] = None,
    event_type: typing.Optional[builtins.str] = None,
    event_user: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ff002fcd079fc5723819441dec4ae1d760cb3b540ce5b8d60401edba42c2a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d0d9cd0e2356679a77a7172a02d4ad82a6aae56e8c147a58052f8d07bd0fb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7017c13c77a048c45e0542eae9e2841aff15433ba0e96c7d5a0ad32951dfb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1490cbb0cd54c85a9d83b21c48f6404be378dac9603783f758b4795bbf7188f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf283650701db116aee6f2d689adf4436ae7d9442ffd0e1c0b69152c523b03d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f208da685ba0dd7a006f7c6e273873eb186af31c6a434e5b276614ab451115ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c4545480a62c51d63d66b2f7e5dc85c97ef816bc0ca5b2b72624debe6f7a74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32809fcfd3e3733209e677234bccd368626db2850debf23f9b39e1bddc0991f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f3c58025547c1e46a1a7c3e719085076357158d1ccb608b354c5a95a7a6b6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5757df74532b5aa9600453ab34ec51c4e4e0b0a4304af794ec9646e51a0de4e9(
    value: typing.Optional[CesEventReportV1Detail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac71935a2114f3d45f41cc39fe285506a117f613d072d297102e2e8457152486(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce5f8611cc11da42df6b4cc987b4937431caaec0d7e35988685bb09c27a112d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b213c831471a163f0fcdc7f0baa0c5a6f40241e94ef8d9b39ad7fe0fc1f7876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757ea09122c5835374c24d8e8dcd8d4d614c47377a2830008ed3e2f0b9c9b7e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a3efd1186a040e486c285465f3e7f9edb45ce324c6b6917bd4c4b612808049(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CesEventReportV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
