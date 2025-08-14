r'''
# `datadog_on_call_schedule`

Refer to the Terraform Registry for docs: [`datadog_on_call_schedule`](https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule).
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


class OnCallSchedule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallSchedule",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule datadog_on_call_schedule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        time_zone: builtins.str,
        layer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallScheduleLayer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule datadog_on_call_schedule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A human-readable name for the new schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#name OnCallSchedule#name}
        :param time_zone: The time zone in which the schedule is defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#time_zone OnCallSchedule#time_zone}
        :param layer: layer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#layer OnCallSchedule#layer}
        :param teams: A list of team ids associated with the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#teams OnCallSchedule#teams}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a80b51c9ea0c9b164485472d356b70140221c9fa7fb5722f508c44c3eb333c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OnCallScheduleConfig(
            name=name,
            time_zone=time_zone,
            layer=layer,
            teams=teams,
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
        '''Generates CDKTF code for importing a OnCallSchedule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OnCallSchedule to import.
        :param import_from_id: The id of the existing OnCallSchedule that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OnCallSchedule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126a79a2d1b22d79ebe23b2a7349c1c6e4298204222f6439f9e4c8071a627b7e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLayer")
    def put_layer(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallScheduleLayer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418574cb164f1182c5297e60f7902b06c3aeda2282ac047654065a8a491781db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLayer", [value]))

    @jsii.member(jsii_name="resetLayer")
    def reset_layer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLayer", []))

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="layer")
    def layer(self) -> "OnCallScheduleLayerList":
        return typing.cast("OnCallScheduleLayerList", jsii.get(self, "layer"))

    @builtins.property
    @jsii.member(jsii_name="layerInput")
    def layer_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallScheduleLayer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallScheduleLayer"]]], jsii.get(self, "layerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd9799b9ed5b822c469fe916780caa058f2fbb480e332a430fd3abfea8bc113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55123acf9d503fd56e6902a7b3f7275f0730a54a56fabbe285a1ce4201c3f8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2265961541d447465a8278ef70ec228e96b6b0e4e7f219c7bc7183153d50ff1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallScheduleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "time_zone": "timeZone",
        "layer": "layer",
        "teams": "teams",
    },
)
class OnCallScheduleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        time_zone: builtins.str,
        layer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallScheduleLayer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: A human-readable name for the new schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#name OnCallSchedule#name}
        :param time_zone: The time zone in which the schedule is defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#time_zone OnCallSchedule#time_zone}
        :param layer: layer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#layer OnCallSchedule#layer}
        :param teams: A list of team ids associated with the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#teams OnCallSchedule#teams}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1d73506c9b8364cdc2baa3b2aea01919febd88c553618542a5fe0ec36aef0b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument layer", value=layer, expected_type=type_hints["layer"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "time_zone": time_zone,
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
        if layer is not None:
            self._values["layer"] = layer
        if teams is not None:
            self._values["teams"] = teams

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
    def name(self) -> builtins.str:
        '''A human-readable name for the new schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#name OnCallSchedule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone in which the schedule is defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#time_zone OnCallSchedule#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def layer(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallScheduleLayer"]]]:
        '''layer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#layer OnCallSchedule#layer}
        '''
        result = self._values.get("layer")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallScheduleLayer"]]], result)

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of team ids associated with the schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#teams OnCallSchedule#teams}
        '''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallScheduleLayer",
    jsii_struct_bases=[],
    name_mapping={
        "effective_date": "effectiveDate",
        "name": "name",
        "rotation_start": "rotationStart",
        "users": "users",
        "end_date": "endDate",
        "interval": "interval",
        "restriction": "restriction",
    },
)
class OnCallScheduleLayer:
    def __init__(
        self,
        *,
        effective_date: builtins.str,
        name: builtins.str,
        rotation_start: builtins.str,
        users: typing.Sequence[builtins.str],
        end_date: typing.Optional[builtins.str] = None,
        interval: typing.Optional[typing.Union["OnCallScheduleLayerInterval", typing.Dict[builtins.str, typing.Any]]] = None,
        restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallScheduleLayerRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param effective_date: The date/time when this layer should become active (in ISO 8601). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#effective_date OnCallSchedule#effective_date}
        :param name: The name of this layer. Should be unique within the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#name OnCallSchedule#name}
        :param rotation_start: The date/time when the rotation for this layer starts (in ISO 8601). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#rotation_start OnCallSchedule#rotation_start}
        :param users: List of user IDs for the layer. Can either be a valid user id or null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#users OnCallSchedule#users}
        :param end_date: The date/time after which this layer no longer applies (in ISO 8601). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#end_date OnCallSchedule#end_date}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#interval OnCallSchedule#interval}
        :param restriction: restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#restriction OnCallSchedule#restriction}
        '''
        if isinstance(interval, dict):
            interval = OnCallScheduleLayerInterval(**interval)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7699e64c60ad474977827c11277798e364ee285219c06cae7aafdd9c55abf64)
            check_type(argname="argument effective_date", value=effective_date, expected_type=type_hints["effective_date"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rotation_start", value=rotation_start, expected_type=type_hints["rotation_start"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument restriction", value=restriction, expected_type=type_hints["restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effective_date": effective_date,
            "name": name,
            "rotation_start": rotation_start,
            "users": users,
        }
        if end_date is not None:
            self._values["end_date"] = end_date
        if interval is not None:
            self._values["interval"] = interval
        if restriction is not None:
            self._values["restriction"] = restriction

    @builtins.property
    def effective_date(self) -> builtins.str:
        '''The date/time when this layer should become active (in ISO 8601).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#effective_date OnCallSchedule#effective_date}
        '''
        result = self._values.get("effective_date")
        assert result is not None, "Required property 'effective_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this layer. Should be unique within the schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#name OnCallSchedule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rotation_start(self) -> builtins.str:
        '''The date/time when the rotation for this layer starts (in ISO 8601).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#rotation_start OnCallSchedule#rotation_start}
        '''
        result = self._values.get("rotation_start")
        assert result is not None, "Required property 'rotation_start' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def users(self) -> typing.List[builtins.str]:
        '''List of user IDs for the layer. Can either be a valid user id or null.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#users OnCallSchedule#users}
        '''
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def end_date(self) -> typing.Optional[builtins.str]:
        '''The date/time after which this layer no longer applies (in ISO 8601).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#end_date OnCallSchedule#end_date}
        '''
        result = self._values.get("end_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional["OnCallScheduleLayerInterval"]:
        '''interval block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#interval OnCallSchedule#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional["OnCallScheduleLayerInterval"], result)

    @builtins.property
    def restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallScheduleLayerRestriction"]]]:
        '''restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#restriction OnCallSchedule#restriction}
        '''
        result = self._values.get("restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallScheduleLayerRestriction"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallScheduleLayer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallScheduleLayerInterval",
    jsii_struct_bases=[],
    name_mapping={"days": "days", "seconds": "seconds"},
)
class OnCallScheduleLayerInterval:
    def __init__(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days: The number of full days in each rotation period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#days OnCallSchedule#days}
        :param seconds: For intervals that are not expressible in whole days, this will be added to ``days``. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#seconds OnCallSchedule#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7141aef608a69d0508ecc32cb2ce55149edbd0bdc95b6f7b56ea14e9042df125)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days is not None:
            self._values["days"] = days
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''The number of full days in each rotation period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#days OnCallSchedule#days}
        '''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''For intervals that are not expressible in whole days, this will be added to ``days``. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#seconds OnCallSchedule#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallScheduleLayerInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnCallScheduleLayerIntervalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallScheduleLayerIntervalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d828db87a577a696fcda0198cfdc35499b54580ab939da66dccefd713284424d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84626ea2bdc7ceb16d191685546f8295ab83cf2f037f5faef24829d76c401aa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94604c4f8b615c090193602c179cf826640ceb42d6761f00a4618eef66a3ad23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerInterval]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerInterval]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerInterval]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4ab228172f2d61f1b907ab1feaec39aa14268291fae826c80b981ee22cb50d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OnCallScheduleLayerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallScheduleLayerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c73cd91ff9a255b38b8cbf0af33534173d7c8134a7b7a6b082e5518644be5e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OnCallScheduleLayerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6719061017941ca98cfbac50ef1215d7724557a026ce768d228fef4293b90608)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OnCallScheduleLayerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca6b4ac296f24efa506642df41ef76c6902b93b108bc37ad225a72cf0f5b847)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a15cdb2d35903857dfd894a3150a8c698eef7cc1d2c6f5670f3e7c7a7878d641)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd0e13b83f79e7fffbce90ce2170a5f20b724207044fd6f8972e8fd65a72924b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallScheduleLayer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallScheduleLayer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallScheduleLayer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3805f9c11061960939d743e9a8862cf0378fc7d73d7cee2aa188cbe447c613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OnCallScheduleLayerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallScheduleLayerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__208642422826886a5124e835ccae46ab56ed272ad406b98137883ac60fbebb26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInterval")
    def put_interval(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days: The number of full days in each rotation period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#days OnCallSchedule#days}
        :param seconds: For intervals that are not expressible in whole days, this will be added to ``days``. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#seconds OnCallSchedule#seconds}
        '''
        value = OnCallScheduleLayerInterval(days=days, seconds=seconds)

        return typing.cast(None, jsii.invoke(self, "putInterval", [value]))

    @jsii.member(jsii_name="putRestriction")
    def put_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallScheduleLayerRestriction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__886918cfab838c60898b983e9a32d6a5d5b5a923d3fb66d71a8de0b055201496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRestriction", [value]))

    @jsii.member(jsii_name="resetEndDate")
    def reset_end_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndDate", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetRestriction")
    def reset_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestriction", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> OnCallScheduleLayerIntervalOutputReference:
        return typing.cast(OnCallScheduleLayerIntervalOutputReference, jsii.get(self, "interval"))

    @builtins.property
    @jsii.member(jsii_name="restriction")
    def restriction(self) -> "OnCallScheduleLayerRestrictionList":
        return typing.cast("OnCallScheduleLayerRestrictionList", jsii.get(self, "restriction"))

    @builtins.property
    @jsii.member(jsii_name="effectiveDateInput")
    def effective_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveDateInput"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerInterval]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerInterval]], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictionInput")
    def restriction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallScheduleLayerRestriction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallScheduleLayerRestriction"]]], jsii.get(self, "restrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationStartInput")
    def rotation_start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rotationStartInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveDate")
    def effective_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveDate"))

    @effective_date.setter
    def effective_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783d7595d90a6ff5ba904f29e7aaba2f30be3963f9895d080316bddd6e4875d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDate"))

    @end_date.setter
    def end_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd0b2849bebaca17c7ea81a7e28b9d6f1d873b3048d2e18c55f2f682c7389b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842f4ac6bd0e7d1396b16127c580e88019abec3637b01d94ac6e738f26ab9609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationStart")
    def rotation_start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationStart"))

    @rotation_start.setter
    def rotation_start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b94f91522c72e5185f4f09eecca8c773ccfc0786ca00356705c4ab8c8c69d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f56fa5fe15c1bf9bf0c24945c56f385746f20d24f826bdb459b7ee1857730a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c407cff4942ba99b5eb9ef086c20f94f134e0b3edd8979d7e8fda7cea17d7b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallScheduleLayerRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "end_day": "endDay",
        "end_time": "endTime",
        "start_day": "startDay",
        "start_time": "startTime",
    },
)
class OnCallScheduleLayerRestriction:
    def __init__(
        self,
        *,
        end_day: builtins.str,
        end_time: builtins.str,
        start_day: builtins.str,
        start_time: builtins.str,
    ) -> None:
        '''
        :param end_day: The weekday when the restriction period ends. Valid values are ``monday``, ``tuesday``, ``wednesday``, ``thursday``, ``friday``, ``saturday``, ``sunday``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#end_day OnCallSchedule#end_day}
        :param end_time: The time of day when the restriction ends (hh:mm:ss). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#end_time OnCallSchedule#end_time}
        :param start_day: The weekday when the restriction period starts. Valid values are ``monday``, ``tuesday``, ``wednesday``, ``thursday``, ``friday``, ``saturday``, ``sunday``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#start_day OnCallSchedule#start_day}
        :param start_time: The time of day when the restriction begins (hh:mm:ss). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#start_time OnCallSchedule#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6924fd28cfdda69629b09d7093caa031f89226836584a6df0b25bb25892d0f)
            check_type(argname="argument end_day", value=end_day, expected_type=type_hints["end_day"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_day", value=start_day, expected_type=type_hints["start_day"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_day": end_day,
            "end_time": end_time,
            "start_day": start_day,
            "start_time": start_time,
        }

    @builtins.property
    def end_day(self) -> builtins.str:
        '''The weekday when the restriction period ends. Valid values are ``monday``, ``tuesday``, ``wednesday``, ``thursday``, ``friday``, ``saturday``, ``sunday``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#end_day OnCallSchedule#end_day}
        '''
        result = self._values.get("end_day")
        assert result is not None, "Required property 'end_day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_time(self) -> builtins.str:
        '''The time of day when the restriction ends (hh:mm:ss).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#end_time OnCallSchedule#end_time}
        '''
        result = self._values.get("end_time")
        assert result is not None, "Required property 'end_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_day(self) -> builtins.str:
        '''The weekday when the restriction period starts. Valid values are ``monday``, ``tuesday``, ``wednesday``, ``thursday``, ``friday``, ``saturday``, ``sunday``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#start_day OnCallSchedule#start_day}
        '''
        result = self._values.get("start_day")
        assert result is not None, "Required property 'start_day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''The time of day when the restriction begins (hh:mm:ss).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_schedule#start_time OnCallSchedule#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallScheduleLayerRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnCallScheduleLayerRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallScheduleLayerRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5b84bb8295e428e28748a78f3e90ab8426920b425b91f457239bc471c923fdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OnCallScheduleLayerRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd76623050cbd3945eb2cd995907b1369feba4376e87a7f6c45ce03a7c4d945)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OnCallScheduleLayerRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e017e08dc08c1d93a5bdd4faacd7814e2e98a9d3a88384004b305e3256c268d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffe5bb586012a548db3cb3a5d821d62901f9b77cc1a228fe379e93c3b5306a74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1c1ea8980470313c98ebc8a8c35f304e4d175d56c9447d5b894696b3ce4118d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallScheduleLayerRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallScheduleLayerRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallScheduleLayerRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c21eecfc2dc05005c47c27452c6f851a3cece2ce3838357a7b0d56465384ccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OnCallScheduleLayerRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallSchedule.OnCallScheduleLayerRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c44b59ca335b6b3c152244e11a879257b4742f55bd6dca204254e4e571f31bcd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endDayInput")
    def end_day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDayInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startDayInput")
    def start_day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endDay")
    def end_day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDay"))

    @end_day.setter
    def end_day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4adceb3f6d3cc7cf811f73d2c9ba4efa26c8cafef22e662a2533afe573cee4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc481718e4341e71aaec1558a3a8aedb5c92d8b996beadb75cfd4a0b6372f432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startDay")
    def start_day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDay"))

    @start_day.setter
    def start_day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa692c92788256ba31e2768ec6c55b8a45acb55575067498a8088cb04df11c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c48bb6ae695dab3fc271ba682fcedf6116ec516672cb7aae30c0f8def73ab14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerRestriction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerRestriction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerRestriction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5144b9d3bf512ddb18744b32f32d3998c5fb72f940c7770498c98b81fe63ec6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OnCallSchedule",
    "OnCallScheduleConfig",
    "OnCallScheduleLayer",
    "OnCallScheduleLayerInterval",
    "OnCallScheduleLayerIntervalOutputReference",
    "OnCallScheduleLayerList",
    "OnCallScheduleLayerOutputReference",
    "OnCallScheduleLayerRestriction",
    "OnCallScheduleLayerRestrictionList",
    "OnCallScheduleLayerRestrictionOutputReference",
]

publication.publish()

def _typecheckingstub__a7a80b51c9ea0c9b164485472d356b70140221c9fa7fb5722f508c44c3eb333c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    time_zone: builtins.str,
    layer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallScheduleLayer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__126a79a2d1b22d79ebe23b2a7349c1c6e4298204222f6439f9e4c8071a627b7e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418574cb164f1182c5297e60f7902b06c3aeda2282ac047654065a8a491781db(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallScheduleLayer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd9799b9ed5b822c469fe916780caa058f2fbb480e332a430fd3abfea8bc113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55123acf9d503fd56e6902a7b3f7275f0730a54a56fabbe285a1ce4201c3f8f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2265961541d447465a8278ef70ec228e96b6b0e4e7f219c7bc7183153d50ff1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1d73506c9b8364cdc2baa3b2aea01919febd88c553618542a5fe0ec36aef0b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    time_zone: builtins.str,
    layer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallScheduleLayer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7699e64c60ad474977827c11277798e364ee285219c06cae7aafdd9c55abf64(
    *,
    effective_date: builtins.str,
    name: builtins.str,
    rotation_start: builtins.str,
    users: typing.Sequence[builtins.str],
    end_date: typing.Optional[builtins.str] = None,
    interval: typing.Optional[typing.Union[OnCallScheduleLayerInterval, typing.Dict[builtins.str, typing.Any]]] = None,
    restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallScheduleLayerRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7141aef608a69d0508ecc32cb2ce55149edbd0bdc95b6f7b56ea14e9042df125(
    *,
    days: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d828db87a577a696fcda0198cfdc35499b54580ab939da66dccefd713284424d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84626ea2bdc7ceb16d191685546f8295ab83cf2f037f5faef24829d76c401aa3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94604c4f8b615c090193602c179cf826640ceb42d6761f00a4618eef66a3ad23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4ab228172f2d61f1b907ab1feaec39aa14268291fae826c80b981ee22cb50d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerInterval]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c73cd91ff9a255b38b8cbf0af33534173d7c8134a7b7a6b082e5518644be5e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6719061017941ca98cfbac50ef1215d7724557a026ce768d228fef4293b90608(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca6b4ac296f24efa506642df41ef76c6902b93b108bc37ad225a72cf0f5b847(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15cdb2d35903857dfd894a3150a8c698eef7cc1d2c6f5670f3e7c7a7878d641(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0e13b83f79e7fffbce90ce2170a5f20b724207044fd6f8972e8fd65a72924b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3805f9c11061960939d743e9a8862cf0378fc7d73d7cee2aa188cbe447c613(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallScheduleLayer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208642422826886a5124e835ccae46ab56ed272ad406b98137883ac60fbebb26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886918cfab838c60898b983e9a32d6a5d5b5a923d3fb66d71a8de0b055201496(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallScheduleLayerRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783d7595d90a6ff5ba904f29e7aaba2f30be3963f9895d080316bddd6e4875d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd0b2849bebaca17c7ea81a7e28b9d6f1d873b3048d2e18c55f2f682c7389b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842f4ac6bd0e7d1396b16127c580e88019abec3637b01d94ac6e738f26ab9609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b94f91522c72e5185f4f09eecca8c773ccfc0786ca00356705c4ab8c8c69d8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f56fa5fe15c1bf9bf0c24945c56f385746f20d24f826bdb459b7ee1857730a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c407cff4942ba99b5eb9ef086c20f94f134e0b3edd8979d7e8fda7cea17d7b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6924fd28cfdda69629b09d7093caa031f89226836584a6df0b25bb25892d0f(
    *,
    end_day: builtins.str,
    end_time: builtins.str,
    start_day: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b84bb8295e428e28748a78f3e90ab8426920b425b91f457239bc471c923fdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd76623050cbd3945eb2cd995907b1369feba4376e87a7f6c45ce03a7c4d945(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e017e08dc08c1d93a5bdd4faacd7814e2e98a9d3a88384004b305e3256c268d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe5bb586012a548db3cb3a5d821d62901f9b77cc1a228fe379e93c3b5306a74(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c1ea8980470313c98ebc8a8c35f304e4d175d56c9447d5b894696b3ce4118d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c21eecfc2dc05005c47c27452c6f851a3cece2ce3838357a7b0d56465384ccb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallScheduleLayerRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44b59ca335b6b3c152244e11a879257b4742f55bd6dca204254e4e571f31bcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4adceb3f6d3cc7cf811f73d2c9ba4efa26c8cafef22e662a2533afe573cee4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc481718e4341e71aaec1558a3a8aedb5c92d8b996beadb75cfd4a0b6372f432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa692c92788256ba31e2768ec6c55b8a45acb55575067498a8088cb04df11c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c48bb6ae695dab3fc271ba682fcedf6116ec516672cb7aae30c0f8def73ab14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5144b9d3bf512ddb18744b32f32d3998c5fb72f940c7770498c98b81fe63ec6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallScheduleLayerRestriction]],
) -> None:
    """Type checking stubs"""
    pass
